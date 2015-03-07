__author__ = 'Malte-Christian'


class NodeBehaviorInterface:
    def __init__(self):
        self.node = None
        raise NotImplementedError("Should have implemented this")

    def register_node(self, node):
        self.node = node

    def received_packet(self, packet):
        raise NotImplementedError("Should have implemented this")

    def received_status(self, frame_id, status):
        raise NotImplementedError("Should have implemented this")

    def action(self):
        raise NotImplementedError("Should have implemented this")

    def encode_sender_information(self, node_id, log_id):
        return str(node_id) + ',' + str(log_id) + ','

    def decode_sender_information(self, data):
        result = str.split(',', data)
        return {'node_id': result[0], 'log_id': result[1]}