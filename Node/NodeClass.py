import multiprocessing
from Hardware.HardwareInterface import HardwareInterface

__author__ = 'Malte-Christian'


class NodeClass(multiprocessing.Process):
    counter = 0

    def __init__(self, log_data_queue, hardware_interface):
        super(NodeClass, self).__init__()
        NodeClass.counter += 1
        self.id = NodeClass.counter
        self._behaviors = []
        self._log_data_queue = log_data_queue

        assert isinstance(hardware_interface, HardwareInterface)
        self._hardware_interface = hardware_interface
        self._hardware_interface.register_node(self)

    def run(self):
        self._hardware_interface.run()  # open serial port in child process (after fork)

        while len(self._behaviors) > 0:
            # invoke action() on each behavior and remove behavior from list if action() returns 'false'
            self._behaviors = [behavior for behavior in self._behaviors if behavior.action()]

        self._hardware_interface.stop()

    """
    Adds behavior to node (e.g. source, sink,...)
    """

    def add_behavior(self, behavior):
        # assert isinstance(behavior, NodeBehaviorInterface)
        behavior.register_node(self)
        self._behaviors.append(behavior)

    """
    Should be invoked by behavior class
    """

    def send_packet(self, frame_id, packet, dest, ack=1):
        self._hardware_interface.send_packet(frame_id, packet, dest, ack)

    """
    Should be invoked by hardware interface
    """

    def received_packet(self, packet):
        for behavior in self._behaviors:
            behavior.received_packet(packet)

    """
    Should be invoked by hardware interface
    """

    def received_status(self, status):
        for behavior in self._behaviors:
            behavior.received_status(status)

    def set_address(self):
        pass

    """
    Should be invoked by behavior class
    """

    def set_log_data(self, node_id, log_id, data):
        self._log_data_queue.put({'node_id': int(node_id),
                                  'log_id': int(log_id),
                                  'data': data})

    def check_channel(self):
        self._hardware_interface.check_channel()

    def get_id(self):
        return self.id