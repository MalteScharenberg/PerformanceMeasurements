__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.EvaluatorBehaviorBase import EvaluatorBehaviorBase


class Delay(EvaluatorBehaviorBase):
    def __init__(self, node_id, block_size):
        self.node_id = int(node_id)
        self.block_size = block_size

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyse(self, data, short):
        try:
            node_data = data[self.node_id]
            size = len(node_data)
        except KeyError:
            return
        end = int(math.floor(size / self.block_size))
        start = end - 1 if short else 1
        if start < 0:
            return

        delay = []
        for n in range(start, end):
            # Sum up delays
            delay_sum = 0
            received_packets = 0
            for i in range(n * self.block_size + 1, (n + 1) * self.block_size + 1):
                try:
                    delay_sum += node_data[i]['received_time'] - node_data[i]['send_time']
                    received_packets += 1
                except KeyError, e:
                    print 'Key error: %s' % e.message
            try:
                delay.append(delay_sum / received_packets)
            except KeyError, e:
                print e, node_data, n

        result = {'data': delay, 'dimension': 's'}

        return result