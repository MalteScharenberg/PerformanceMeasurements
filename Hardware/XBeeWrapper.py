import serial
from xbee import XBee
from xbee.helpers.dispatch import Dispatch

from Hardware import HardwareBase


__author__ = 'Malte-Christian'


class XBeeWrapper(HardwareBase):
    def __init__(self, port):
        self._port = port
        self._serial = serial.Serial()
        self._xbee = XBee()
        self._dispatcher = Dispatch()
        self.node = None

        # Init the dispatcher
        self.dispatcher.register(
            "tx_status",
            self.status_handler,
            lambda packet: packet['id'] == 'tx_status'
        )

        self.dispatcher.register(
            "rx",
            self.rx_handler,
            lambda packet: packet['id'] == 'rx'
        )

    def register_node(self, node):
        self.node = node

    def run(self):
        self._serial = serial.Serial(self._port, 115000, stopbits=serial.STOPBITS_ONE, rtscts=1)
        self._xbee = XBee(self._serial, callback=self._dispatcher.dispatch)

    def stop(self):
        self._xbee.halt()
        self._serial.close()

    def status_handler(self, name, packet):
        if self.node is not None:
            self.node.received_status(packet)

    def rx_handler(self, name, packet):
        if self.node is not None:
            self.node.received_packet(packet)

    def send_data(self, frame_id, data, dest, ack=1):
        self._xbee.tx(frame_id=chr(frame_id), dest_addr='\x00' + chr(dest), data=data, options=chr(ack))
