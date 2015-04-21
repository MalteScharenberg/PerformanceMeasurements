import time
import random
import string
import math

from Node.NodeBehaviorBase import NodeBehaviorBase


__author__ = 'Malte-Christian Scharenberg'


class Source(NodeBehaviorBase):
    def __init__(self, quantity, payload, dest, ack=1, full_buffer=True, max_speed=False, increase_payload=False):
        self.quantity = quantity
        self.increase_payload = increase_payload
        self.payload = payload
        self.dest = dest
        self.ack = ack
        self.full_buffer = full_buffer
        self.max_speed = max_speed
        self.log_id = 0
        self.frame_ids = [None] * 255  # Preallocate list for frame id translation
        self.node = None
        self.start_frame = time.time()
        self.payload_counter = 0

    def received_packet(self, src, packet):
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

            if self.max_speed and not self.check_speed():
                return True

            frame_id = self.register_frame_id(self.log_id)

            if frame_id is False:  # Wait for frame_id
                return True

            last = self.log_id == self.quantity

            last = False  # do not shout down

            header = Source.encode_sender_information(self.node.get_id(), self.log_id, last)
            data = header + self.generate_data(self.get_payload() - len(header))

            if self.max_speed:
                self.payload_counter += len(data)

            send_time = time.time()
            self.node.send_packet(frame_id, data, self.dest, self.ack)
            self.node.set_log_data(self.node.get_id(), self.log_id, dict(send_time=send_time,
                                                                         payload=len(data)))
            self.log_id += 1
            return True
        else:
            return not all(frame_id is None for frame_id in
                           self.frame_ids)  # Remove behavior after all status messages are collected

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

    def check_speed(self):
        duration = time.time() - self.start_frame
        current_speed = (self.payload_counter + 100) / duration / 1000

        if duration > 5:
            self.start_frame = time.time()
            self.payload_counter = 0

        return current_speed < self.max_speed
