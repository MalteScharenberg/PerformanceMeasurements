import math
from Evaluation.EvaluatorBehaviorInterface import EvaluatorBehaviorInterface

__author__ = 'Malte-Christian'


class Throughput(EvaluatorBehaviorInterface):
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
        result = []
        for n in range(start, end):
            # Calculate transferred data
            payload = 0
            for i in range(1, self.block_size):
                if 'received_time' in node_data[i]:
                    payload += node_data[i]['payload']
            result.append(payload / (node_data[n + self.block_size]['send_time'] - node_data[n]['send_time']))
        return result