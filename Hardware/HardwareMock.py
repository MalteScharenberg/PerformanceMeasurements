__author__ = 'Malte-Christian Scharenberg'

import time
import random
import multiprocessing
from Hardware.IHardware import IHardware


class HardwareMock(IHardware):
    channel = multiprocessing.Queue()

    def __init__(self):
        self.node = None

    def register_node(self, node):
        self.node = node

    def send_packet(self, frame_id, packet, dest, ack=True):
        # time.sleep(0.0025)
        HardwareMock.channel.put(packet)

    def check_channel(self):
        while True:
            try:
                data = HardwareMock.channel.get(block=False)
                self.node.received_packet(data)
            except Exception:
                break

    def run(self):
        pass

    def stop(self):
        pass