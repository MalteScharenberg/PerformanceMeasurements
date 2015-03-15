import time
import random
import string

from Node.NodeBehaviorBase import NodeBehaviorBase


__author__ = 'Malte-Christian Scharenberg'


class Source(NodeBehaviorBase):
    def __init__(self, quantity, payload, dest, ack=1, full_buffer=True):
        self.quantity = quantity
        self.payload = payload
        self.dest = dest
        self.ack = ack
        self.full_buffer = full_buffer
        self.log_id = 0
        self.frame_ids = [None] * 255  # Preallocate list for frame id translation
        self.node = None

    def received_packet(self, packet):
        pass

    def received_status(self, frame_id, status):
        status_time = time.time()
        log_id = self.frame_ids[int(frame_id) - 1]
        self.frame_ids[int(frame_id) - 1] = None
        if log_id is None:
            print frame_id, 'not found'
            return
        log_data = {'status_time': status_time,
                    'status': status}

        self.node.set_log_data(self.node.get_id(), log_id, log_data)

    def action(self):
        if self.log_id <= self.quantity:
            frame_id = self.register_frame_id(self.log_id)
            if frame_id is False:  # Wait for frame_id
                return True
            header = Source.encode_sender_information(self.node.get_id(), self.log_id)
            data = header + self.generate_data(self.payload - len(header))
            send_time = time.time()
            self.node.send_packet(frame_id, data, self.dest, self.ack)
            self.node.set_log_data(self.node.get_id(), self.log_id, {'send_time': send_time,
                                                                     'payload': len(data)})
            self.log_id += 1
            return True
        else:
            return not all(frame_id is None for frame_id in self.frame_ids)  # Remove behavior

    def get_max_sleep_time(self):
        if self.log_id <= self.quantity:
            return 0
        else:
            return 1

    def generate_data(self, size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    def register_frame_id(self, new_log_id):
        new_frame_id = False
        if self.full_buffer:
            for frame_id, log_id in enumerate(self.frame_ids):
                if log_id is None:
                    new_frame_id = frame_id + 1
                    self.frame_ids[frame_id] = new_log_id
                    break
        else:
            if self.frame_ids[0] is None:
                new_frame_id = 1
                self.frame_ids[0] = new_log_id

        return new_frame_id
