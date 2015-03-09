__author__ = 'Malte-Christian'


class EvaluatorBehaviorBase:
    def __init__(self):
        pass

    def get_name(self):
        return self.__class__.__name__