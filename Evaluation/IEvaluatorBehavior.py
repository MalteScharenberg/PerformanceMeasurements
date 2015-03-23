__author__ = 'Malte-Christian Scharenberg'


class IEvaluatorBehavior:
    def __init__(self):
        pass

    def get_name(self):
        raise NotImplementedError("Should have implemented this")

    def analyze(self, data, short):
        raise NotImplementedError("Should have implemented this")