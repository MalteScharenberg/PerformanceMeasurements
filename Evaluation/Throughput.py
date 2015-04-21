__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class Throughput(IEvaluatorBehavior):
    def __init__(self, node_id, block_size):
        self.node_id = int(node_id)
        self.block_size = block_size

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyze(self, data, short):
        try:
            node_data = data[self.node_id]
        except KeyError:
            return

        # Filter input data
        node_data = filter(lambda date: 'status' in date,
                           node_data)

        size = len(node_data)
        end = int(math.ceil(size / self.block_size))
        start = end - 1 if short else 0

        if start < 0:
            return
        throughput = []
        for n in range(start, end):

            # Calculate transferred data
            payload = 0
            for i in range(n * self.block_size,
                           (n + 1) * self.block_size):
                if node_data[i]['status'] == '\x00':
                    payload += node_data[i]['payload']
            try:
                throughput.append(
                    8 * payload / (node_data[(n + 1) * self.block_size - 1]['status_time']
                                   - node_data[n * self.block_size]['status_time']) / 1000)
            except KeyError, e:
                print e, node_data, n

        result = dict(data=throughput,
                      dimension='kbits')

        return result