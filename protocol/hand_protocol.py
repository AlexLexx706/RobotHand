# -*- coding: utf-8 -*-
import serial
import struct
import logging
import protocol
import math
import threading

logger = logging.getLogger(__name__)

class HandProtocol(protocol.Protocol):
    def __init__(self, **kwargs):
        protocol.Protocol.__init__(self, **kwargs)
        self.lock = threading.Lock()

        self.limmits = [[[-65 / 180. * math.pi, 2395], [90 / 180. * math.pi, 543], 1],
                        [[-135 / 180. * math.pi, 543], [0 / 180. * math.pi, 2065], 2],
                        [[-150 / 180. * math.pi, 2500], [0 / 180. * math.pi, 804], 3],
                        [[0 / 180. * math.pi, 1000], [110 / 180. * math.pi, 2300], 4],
                        [[-105 / 180. * math.pi, 2500], [90 / 180. * math.pi, 870], 5],
                        [[0 / 180. * math.pi, 1239], [85 / 180. * math.pi, 1913], 6]]
    
    def set_limmits(self, limmits):
        with self.lock:
            self.limmits = limmits
    
    def rotate(self, id, angle):
        with self.lock:
            if id < 0 or id >= len(self.limmits):
                return

            limmit = self.limmits[id]

        if angle < limmit[0][0]:
            angle = limmit[0][0] 

        if angle > limmit[1][0]:
            angle = limmit[1][0]
        
        #делаем поворот
        v = (angle - limmit[0][0]) / (limmit[1][0] - limmit[0][0]) * (limmit[1][1] - limmit[0][1]) + limmit[0][1]
        self.move_servo(limmit[2], int(v), time_move_sec=0.05)

    def get_angle(self, id, angle):
        limmit = self.limmits[id]

        if angle < limmit[0][0]:
            angle = limmit[0][0]

        if angle > limmit[1][0]:
            angle = limmit[1][0]

        #делаем поворот
        return limmit[2], (angle - limmit[0][0]) / (limmit[1][0] - limmit[0][0]) * (limmit[1][1] - limmit[0][1]) + limmit[0][1]


    def move_hand(self, angles):
        with self.lock:
            if len(angles) != len(self.limmits):
                return
            data = [self.get_angle(i, a) for i, a in enumerate(angles)]
        
        self.move_servos(data, 0.05)

if __name__ == "__main__":
    import time
    import math
    import sys
    logging.basicConfig(level=logging.DEBUG)
    proto = HandProtocol(port="COM27", baudrate=128000)
    proto.rotate(5, 45 / 180. * math.pi)
    sys.exit()
    
    proto.rotate(0, 0 / 180. * math.pi)
    time.sleep(1)
    proto.rotate(0, -45 / 180. * math.pi)
    time.sleep(1)
    proto.rotate(0, 45 / 180. * math.pi)
    time.sleep(1)
    proto.rotate(0, 0 / 180. * math.pi)

    proto.rotate(1, 0 / 180. * math.pi)
    time.sleep(1)
    proto.rotate(1, -90/ 180. * math.pi)
    time.sleep(1)
    proto.rotate(1, 0/180. * math.pi)

    time.sleep(1)
    proto.rotate(1, -90/180. * math.pi)


    time.sleep(1)
    proto.rotate(2, 0 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(2, -90.0 / 180. * math.pi)


    time.sleep(1)
    proto.rotate(1, 0/180. * math.pi)

    time.sleep(1)
    proto.rotate(0, -45/180. * math.pi)


    time.sleep(1)
    proto.rotate(3, 0/180. * math.pi)

    time.sleep(1)
    proto.rotate(3, 90/180. * math.pi)

    time.sleep(1)
    proto.rotate(3, 120/180. * math.pi)

