__author__ = 'Malte-Christian Scharenberg'


class NodeBehaviorBase:
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

    def get_max_sleep_time(self):
        raise NotImplementedError("Should have implemented this")

    @staticmethod
    def encode_sender_information(node_id, log_id, last=False):
        return str(node_id) + ',' + str(log_id) + ',' + ('1,' if last else '')

    @staticmethod
    def decode_sender_information(data):
        result = data.split(',')
        return {'node_id': int(result[0]),
                'log_id': int(result[1]),
                'last': result[2] == '1'}