# -*- coding: utf-8 -*-
import serial
import struct
import logging
import time


logger = logging.getLogger(__name__)

class Protocol:
    def __init__(self, port="com27", baudrate=9600):
        '''Протокол управления сервами'''
        try:
            logger.debug("->")
            self.serial = None
            self.connect(port, baudrate)
        finally:
            logger.debug("<-")

    def connect(self, port, baudrate):
        try:
            logger.debug("->")

            if self.serial is not None:
                self.serial.close()
                self.serial = None

            self.serial = serial.Serial(port=port, baudrate=baudrate)
        finally:
            logger.debug("<-")

    def close(self):
        try:
            logger.debug("->")
            if self.serial is not None:
                self.serial.close()
                self.serial = None
        finally:
            logger.debug("<-")
        
    def is_connected(self):
        return self.serial is not None

    def move_servo(self, ch, pulse_width_us, time_move_sec=1):
        '''
            ch - Servo number, range 1~32 (decimal number)
            pw - Pulse width (servo position), range: 500~2500. Unit: us (microseconds)
            time -  Time used to move to the position, effective for all servos.
        '''
        if self.serial is not None:
            self.serial.write('#{}P{}T{}\n\r'.format(int(ch), int(pulse_width_us), int(time_move_sec * 100)))
            logger.debug("ch:{} pw:{} time:{}".format(ch, pulse_width_us, time_move_sec))
            time.sleep(time_move_sec)

    def move_servos(self, data, time_move_sec=1):
        '''
            data - list of servos params [[ch, ps]...]
            time -  Time used to move to the position, effective for all servos.
        '''
        if self.serial is not None:
            logger.debug("move_servos(data:{} time:{}) ->".format(data, time_move_sec))
            s = '{}T{}\n\r'.format("".join(["#{}P{}".format(int(ch), int(pw)) for ch, pw in data]), int(time_move_sec * 100))
            self.serial.write(s)
            logger.debug("move_servos <-")
            time.sleep(time_move_sec)

if __name__ == "__main__":
    import math
    logging.basicConfig(level=logging.INFO)
    proto = Protocol("COM27", 115200)
    period = 5.
    border = [500 + 100, 2500 - 100]
    border2 = [500 + 500, 2500 - 500]
    s_time = time.time()
    
    while 1:
        k = (math.cos((time.time() - s_time) / period * math.pi) + 1.0) / 2.0
        pw = border[0]  + k * (border[1] - border[0])
        pw2 = border2[0]  + k * (border2[1] - border2[0])
        #proto.move_servo(1, pw, 0.1)
        proto.move_servos(((1, pw),(2, pw),(3, pw),(5, pw),(6, pw2)), 0.05)

