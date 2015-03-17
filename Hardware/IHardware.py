__author__ = 'Malte-Christian Scharenberg'


class IHardware:
    def __init__(self):
        raise NotImplementedError("Should have implemented this")

    def register_node(self, node):
        raise NotImplementedError("Should have implemented this")

    def run(self):
        """
        This method get's invoked after process fork.
        Serial Port association, etc, should be implemented here.
        """
        raise NotImplementedError("Should have implemented this")

    def stop(self):
        """
        This method get's invoked when process shuts down.
        """
        raise NotImplementedError("Should have implemented this")

    def send_packet(self, frame_id, packet, dest, ack=1):
        raise NotImplementedError("Should have implemented this")

    def check_channel(self):
        """
        This method get's invoked on a regular basis.
        You can use this to handle incoming packets.
        Ignore this method if you are working with callbacks.
        (pass)
        """
        raise NotImplementedError("Should have implemented this")

    def set_address(self, address):
        raise NotImplementedError("Should have implemented this")