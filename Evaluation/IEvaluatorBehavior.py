__author__ = 'Malte-Christian Scharenberg'


class IEvaluatorBehavior:
    def __init__(self):
        pass

    def get_name(self):
        raise NotImplementedError("Should have implemented this")

    def analyse(self, data, short):
        raise NotImplementedError("Should have implemented this")