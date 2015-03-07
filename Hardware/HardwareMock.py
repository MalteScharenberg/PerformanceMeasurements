from Hardware.HardwareInterface import HardwareInterface

__author__ = 'Malte-Christian'


class HardwareMock(HardwareInterface):
    def __init__(self, port):
        self._port = port
        self.node = None

    def register_node(self, node):
        self.node = node

    def send_packet(self, frame_id, packet, dest, ack=1):
        pass

    def run(self):
        pass

    def stop(self):
        pass