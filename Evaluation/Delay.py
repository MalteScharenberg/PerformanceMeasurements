__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class Delay(IEvaluatorBehavior):
    def __init__(self, node_id, block_size, group_by=False):
        self.node_id = int(node_id)
        self.block_size = block_size
        self.group_by = group_by

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyse(self, data, short):
        try:
            node_data = data[self.node_id]
        except KeyError:
            return

        # Filter input data
        node_data = filter(lambda date: 'received_time' in date
                                        and (not self.group_by or (self.group_by in date)),
                           # if 'group_by' is set, it should be a key in date
                           node_data)

        size = len(node_data)
        end = int(math.floor(size / self.block_size))
        start = end - 1 if short else 1

        if start < 0:
            return

        if self.group_by:
            pass

        delay = []
        for n in range(start, end):

            # Sum up delays
            delay_sum = 0
            received_packets = 0
            for i in range(n * self.block_size, (n + 1) * self.block_size):
                try:
                    delay_sum += node_data[i]['received_time'] - node_data[i]['send_time']
                    received_packets += 1
                except KeyError, e:
                    print 'Key error: %s' % e.message
            try:
                delay.append(dict(data=delay_sum / received_packets,
                                  desc=''))
            except KeyError, e:
                print e, node_data, n

        result = dict(data=delay,
                      dimension='s')

        return result

    def computation_callback(self, data):
        pass