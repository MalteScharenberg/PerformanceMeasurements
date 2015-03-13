__author__ = 'Malte-Christian Scharenberg'


class EvaluatorBehaviorBase:
    def __init__(self):
        pass

    def get_name(self):
        raise NotImplementedError("Should have implemented this")