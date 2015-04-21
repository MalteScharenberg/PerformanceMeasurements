__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class ThroughputTime(IEvaluatorBehavior):
    def __init__(self, node_id, time, group_by=False):
        self.node_id = int(node_id)
        self.time = time
        self.group_by = group_by

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyze(self, data, short):
        try:
            node_data = data[self.node_id]
        except KeyError:
            return

        # Filter input data
        node_data = filter(lambda date: 'status' in date and 'status_time' in date
                                        and date['status'] == '\x00'
                                        and (not self.group_by or (self.group_by in date)),
                           node_data)

        start = node_data[0]['status_time'] if len(node_data) > 0 else 0
        payload = 0
        group_param = node_data[0][self.group_by] if self.group_by and len(node_data) > 0 else False
        throughput = []

        if short:
            start = node_data[-1]['status_time'] if len(node_data) > 0 else 0
            node_data = reversed(node_data)
            group_param = False

        for date in node_data:
            if self.group_by and group_param and group_param != date[self.group_by]:
                start = date['status_time']
                payload = 0
                group_param = date[self.group_by]

            if not short and start + self.time < date['status_time']:
                if self.group_by:
                    desc = date[self.group_by]
                else:
                    desc = ''

                throughput.append(dict(
                    data=8 * payload / self.time / 1000,
                    desc=desc))

                start = date['status_time']
                payload = 0

                if self.group_by:
                    group_param = date[self.group_by]

            if short and start - self.time > date['status_time']:
                throughput.append(
                    8 * payload / self.time / 1000)
                break

            payload += date['payload']

        result = dict(data=throughput,
                      dimension='kbits')

        return result