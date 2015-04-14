__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class ThroughputTime(IEvaluatorBehavior):
    def __init__(self, node_id, time):
        self.node_id = int(node_id)
        self.time = time

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyze(self, data, short):
        try:
            node_data = data[self.node_id]
        except KeyError:
            return

        # Filter input data
        node_data = filter(lambda date: 'status' in date and 'received_time' in date and date['status'] == '\x00',
                           node_data)

        start = node_data[0]['received_time'] if len(node_data) > 0 else 0
        payload = 0
        throughput = []

        if short:
            start = node_data[-1]['received_time'] if len(node_data) > 0 else 0
            node_data = reversed(node_data)

        for date in node_data:
            if not short and start + self.time < date['received_time']:
                throughput.append(
                    8 * payload / self.time / 1000)
                start = date['received_time']
                payload = 0

            if short and start - self.time > date['received_time']:
                throughput.append(
                    8 * payload / self.time / 1000)
                break

            payload += date['payload']

        result = dict(data=throughput,
                      dimension='kbits')

        return result