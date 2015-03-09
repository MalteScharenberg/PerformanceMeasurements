import time
import random
import string

from Node.NodeBehaviorBase import NodeBehaviorBase


__author__ = 'Malte-Christian'


class Source(NodeBehaviorBase):
    def __init__(self, quantity, payload, dest, ack=1):
        self.quantity = quantity
        self.payload = payload
        self.dest = dest
        self.ack = ack
        self.log_id = 0
        self.frame_ids = [None] * 255  # Preallocate list for frame id translation
        self.frame_id = 0
        self.node = None

    def received_packet(self, packet):
        pass

    def received_status(self, frame_id, status):
        status_time = time.time()
        log_id = self.frame_ids[frame_id]
        log_data = {'status_time': status_time,
                    'status': status}

        self.node.set_log_data(self.node.get_id(), log_id, log_data)

    def action(self):
        self.quantity -= 1
        self.log_id += 1
        header = self.encode_sender_information(self.node.get_id(), self.log_id)
        data = header + self.generate_data(self.payload - len(header))
        frame_id = self.get_frame_id(self.log_id)
        send_time = time.time()
        self.node.send_packet(frame_id, data, self.dest, self.ack)
        self.node.set_log_data(self.node.get_id(), self.log_id, {'send_time': send_time})

        # if use_buffer == 0:
        # while n > 1 and 'status' not in self.dataLog[round][n - 1]:
        # time.sleep(0.00001)

        return self.quantity > 0

    def generate_data(self, size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    def get_frame_id(self, log_id):
        if self.frame_id < 255:
            self.frame_id += 1
        else:
            self.frame_id = 1
        self.frame_ids[self.frame_id] = log_id
        return self.frame_id
