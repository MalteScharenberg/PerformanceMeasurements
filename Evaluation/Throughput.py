from Evaluation.EvaluatorBehaviorInterface import EvaluatorBehaviorInterface

__author__ = 'Malte-Christian'


class Throughput(EvaluatorBehaviorInterface):
    def __init__(self):
        pass

    def analyse(self, data, short):
        print data