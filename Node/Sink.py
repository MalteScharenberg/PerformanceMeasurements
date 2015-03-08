
import time
from Node.NodeBehaviorInterface import NodeBehaviorInterface


__author__ = 'Malte-Christian'


class Sink(NodeBehaviorInterface):
    def __init__(self):
        pass

    def received_packet(self, packet):
        status_time = time.time()
        data = self.decode_sender_information(packet)
        self.node.set_log_data(data['node_id'], data['log_id'], {'received_time': status_time})

    def received_status(self, status):
        pass

    def action(self):
        self.node.check_channel()
        return True