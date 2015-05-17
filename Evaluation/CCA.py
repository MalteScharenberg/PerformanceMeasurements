__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class CCA(IEvaluatorBehavior):
    def __init__(self, node_id):
        self.node_id = int(node_id)

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyze(self, data, short):
        try:
            node_data = data[self.node_id]
        except KeyError:
            return

        # Filter input data
        node_data = filter(lambda date: 'status' in date
                                        and date['status'] == '\x02',
                           node_data)
        cca_failurs = len(node_data)

        result = dict(data=[cca_failurs],
                      dimension='packets')

        return result
