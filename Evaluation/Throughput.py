__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.EvaluatorBehaviorBase import EvaluatorBehaviorBase


class Throughput(EvaluatorBehaviorBase):
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
        throughput = []
        for n in range(start, end):
            # Calculate transferred data
            payload = 0
            for i in range(n * self.block_size + 1, (n + 1) * self.block_size + 1):
                if 'status' in node_data[i] and node_data[i]['status'] == '\x00':
                    payload += node_data[i]['payload']
            try:
                throughput.append(
                    payload / (node_data[(n + 1) * self.block_size]['send_time'] - node_data[n * self.block_size + 1][
                        'send_time']) / 1000)
            except KeyError, e:
                print e, node_data, n

        result = {'data': throughput, 'dimension': 'kbits'}

        return result