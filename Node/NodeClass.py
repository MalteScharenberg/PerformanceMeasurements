__author__ = 'Malte-Christian Scharenberg'

import multiprocessing
import time
from Hardware.IHardware import IHardware, HardwareException


class NodeClass(multiprocessing.Process):
    counter = 0

    def __init__(self, log_data_queue, hardware_interface):
        super(NodeClass, self).__init__()
        NodeClass.counter += 1
        self.id = NodeClass.counter
        self._behaviorList = []
        self._log_data_queue = log_data_queue

        assert isinstance(hardware_interface, IHardware)
        self._hardware_interface = hardware_interface
        self._hardware_interface.register_node(self)

    def run(self):
        try:
            self._hardware_interface.run()  # open serial port at child process (after fork)
        except HardwareException, e:
            print e
            return  # Kill process

        try:
            while len(self._behaviorList) > 0:
                # invoke action() on each behavior and remove behavior from list if action() returns 'false'
                # self._behaviors = [behavior for behavior in self._behaviors if behavior.action()]

                sleep = False
                behaviors = []
                for behavior in self._behaviorList:
                    if behavior.action():  # remove behavior if return value is false
                        behaviors.append(behavior)

                    if sleep is False or behavior.get_max_sleep_time() < sleep:
                        sleep = float(behavior.get_max_sleep_time())

                self._behaviorList = behaviors

                if sleep and len(self._behaviorList):
                    time.sleep(sleep)  # Sleep to avoid busy waiting

        except KeyboardInterrupt:
            pass

        print '\nShutting down node %d...' % self.get_id()
        self._hardware_interface.stop()

    """
    Adds behavior to node (e.g. source, sink,...)
    """

    def add_behavior(self, behavior):
        # assert isinstance(behavior, NodeBehaviorInterface)
        behavior.register_node(self)
        self._behaviorList.append(behavior)

    """
    Should be invoked by behavior class
    """

    def send_packet(self, frame_id, packet, dest, ack=1):
        self._hardware_interface.send_packet(frame_id, packet, dest, ack)

    """
    Should be invoked by hardware interface
    """

    def received_packet(self, packet):
        for behavior in self._behaviorList:
            behavior.received_packet(packet)

    """
    Should be invoked by hardware interface
    """

    def received_status(self, frame_id, status):
        for behavior in self._behaviorList:
            behavior.received_status(frame_id, status)

    """
    Should be invoked by behavior class
    """

    def set_log_data(self, node_id, log_id, data):
        self._log_data_queue.put(dict(node_id=int(node_id),
                                      log_id=int(log_id),
                                      data=data))

    def check_channel(self):
        self._hardware_interface.check_channel()

    def get_id(self):
        return self.id
