__author__ = 'Malte-Christian Scharenberg'


class HardwareBase:
    def __init__(self):
        pass

    def send_packet(self, frame_id, packet, dest, ack=1):
        pass
    
    def check_channel(self):
        pass