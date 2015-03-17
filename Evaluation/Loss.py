__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.EvaluatorBehaviorBase import EvaluatorBehaviorBase


class Loss(EvaluatorBehaviorBase):
    def __init__(self, node_id):
        self.node_id = int(node_id)

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyse(self, data, short):
        try:
            node_data = data[self.node_id]
            node_data = filter(lambda date: 'status' in date and date['status'] != '\x00',
                               node_data)  # Filter input data
            loss = len(node_data)
        except KeyError:
            return

        result = {'data': loss, 'dimension': 'packets'}

        return result
