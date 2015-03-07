
from Node.NodeBehaviorInterface import NodeBehaviorInterface


__author__ = 'Malte-Christian'


class Sink(NodeBehaviorInterface):
    def __init__(self):
        pass

    def received_packet(self, packet):
        pass

    def received_status(self, status):
        pass

    def action(self):
        pass
