"""
Serial communication class
"""

import serial
import time
import config


class Arduino(object):
    def __init__(self):
        try:
            self.arduino = serial.Serial(config.SERIAL_PORT, 115200, timeout=.1)
        except serial.serialutil.SerialException:
            raise RuntimeError('Impossible to connect to Arduino')

        time.sleep(1)

    def write(self, msg):
        # "#" is termination char
        msg = str(msg) + '#'
        self.arduino.write(msg)