import math
from Evaluation.EvaluatorBehaviorBase import EvaluatorBehaviorBase

__author__ = 'Malte-Christian'


class Throughput(EvaluatorBehaviorBase):
    def __init__(self, node_id, block_size):
        self.node_id = int(node_id)
        self.block_size = block_size

    def analyse(self, data, short):
        try:
            node_data = data[self.node_id]
            size = len(node_data)
        except KeyError:
            return
        end = int(math.floor(size / self.block_size)) + 1
        start = end - 1 if short else 1
        if start < 1:
            return
        throughput = []
        for n in range(start, end):
            # Calculate transferred data
            payload = 0
            for i in range(1, self.block_size + 1):
                if 'received_time' in node_data[i]:
                    payload += node_data[i]['payload']
            try:
                throughput.append(
                    payload / (node_data[n + self.block_size - 1]['send_time'] - node_data[n]['send_time']) / 1000)
            except KeyError, e:
                print e, node_data, n

        result = {'data': throughput, 'dimension': 'kbits'}

        return result