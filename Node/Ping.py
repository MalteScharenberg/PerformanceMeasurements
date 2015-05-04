import time
from Node.NodeBehaviorBase import NodeBehaviorBase
from Node.Sink import Sink
from Node.Source import Source


__author__ = 'Malte-Christian Scharenberg'


class Ping(NodeBehaviorBase):
    def __init__(self):
        self.last = False
        self.last_received_time = time.time()
        self.source = Source()
        self.sink = Sink()

    def received_packet(self, src, data):
        received_time = time.time()
        info = Ping.decode_sender_information(data)

        if info['last']:
            self.last = True

        frame_id = 1  # TODO: use frame id of incomming packet

        self.node.send_packet(frame_id, data, src, True)
        self.last_received_time = received_time

    def received_status(self, frame_id, status):
        pass

    def action(self):
        self.node.check_channel()

        # Remove behavior if 'last' identifier in packet or if no packet was received for more than 10 seconds
        return not (self.last or time.time() - self.last_received_time > 10)

    def get_max_sleep_time(self):
        return 1