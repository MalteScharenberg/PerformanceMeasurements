import time
from Node.NodeBehaviorBase import NodeBehaviorBase


__author__ = 'Malte-Christian Scharenberg'


class Sink(NodeBehaviorBase):
    def __init__(self):
        self.last = False

    def received_packet(self, packet):
        status_time = time.time()
        data = Sink.decode_sender_information(packet)
        if data['last']:
            self.last = True
        self.node.set_log_data(data['node_id'],
                               data['log_id'],
                               {'received_time': status_time})

    def received_status(self, status):
        pass

    def action(self):
        self.node.check_channel()

        return not self.last

    def get_max_sleep_time(self):
        return 1