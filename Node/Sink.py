import time
from Node.NodeBehaviorBase import NodeBehaviorBase


__author__ = 'Malte-Christian Scharenberg'


class Sink(NodeBehaviorBase):
    def __init__(self):
        self.last = False
        self.last_received_time = time.time()

    def received_packet(self, packet):
        received_time = time.time()
        data = Sink.decode_sender_information(packet)

        if data['last']:
            self.last = True

        self.node.set_log_data(data['node_id'],
                               data['log_id'],
                               {'received_time': received_time})

        self.last_received_time = received_time

    def received_status(self, frame_id, status):
        pass

    def action(self):
        self.node.check_channel()

        # Remove behavior if 'last' identifier in packet or if no packet was received for more than 10 seconds
        return not (self.last or time.time() - self.last_received_time > 10)

    def get_max_sleep_time(self):
        return 1