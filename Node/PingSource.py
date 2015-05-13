import time
import random
import string
import math

from Node.NodeBehaviorBase import NodeBehaviorBase


__author__ = 'Malte-Christian Scharenberg'


class PingSource(NodeBehaviorBase):
    def __init__(self, quantity, payload, dest, ack=1, increase_payload=False):
        self.quantity = quantity
        self.increase_payload = increase_payload
        self.payload = payload
        self.dest = dest
        self.ack = ack
        self.log_id = 0
        self.node = None
        self.start_frame = time.time()
        self.payload_counter = 0
        self.clear_to_send = True
        self.last = False
        self.last_received_time = time.time()

    def received_packet(self, src, data):
        self.clear_to_send = True

        received_time = time.time()
        info = PingSource.decode_sender_information(data)

        if info['last']:
            self.last = True

        self.node.set_log_data(info['node_id'],
                               info['log_id'],
                               {'received_time': received_time})

        self.last_received_time = received_time

    def received_status(self, frame_id, status):
        status_time = time.time()
        log_id = self.log_id - 1

        if log_id is None:
            print frame_id, 'not found'
            return
        log_data = {'status_time': status_time,
                    'status': status}

        self.node.set_log_data(self.node.get_id(), log_id, log_data)

    def action(self):
        if self.clear_to_send and self.log_id <= self.quantity:

            frame_id = 1
            last = self.log_id == self.quantity

            # last = False  # do not shout down
            header = PingSource.encode_sender_information(self.node.get_id(), self.log_id, last)
            data = header + self.generate_data(self.get_payload() - len(header))

            send_time = time.time()
            self.node.send_packet(frame_id, data, self.dest, self.ack)
            self.node.set_log_data(self.node.get_id(), self.log_id, dict(send_time=send_time,
                                                                         payload=len(data)))
            self.log_id += 1

            self.clear_to_send = False  # Block and wait for ping

            return True
        else:
            return not (self.last or time.time() - self.last_received_time > 10)

    def get_max_sleep_time(self):
        if self.log_id <= self.quantity:
            return 0
        else:
            return 1

    def get_payload(self):
        if self.increase_payload:
            steps = math.floor(self.payload / 10)
            step_size = math.floor(self.quantity / steps)
            payload = int((math.floor(self.log_id / step_size) + 1) * self.payload / steps)

            return payload if payload <= 100 else 100
        else:
            return self.payload

    def generate_data(self, size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
