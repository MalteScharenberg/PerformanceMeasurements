from performanceMeasurement.Hardware.HardwareInterface import HardwareInterface

__author__ = 'Malte-Christian'


class HardwareMock(HardwareInterface):
    def __init__(self, port):
        self._port = port

    def register_node(self, node):
        self.node = node

    def run(self):
        pass

    def stop(self):
        pass