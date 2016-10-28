# -*- coding: utf-8 -*-
import logging
import math
import threading
from robothand import protocol


LOG = logging.getLogger(__name__)


class HandProtocol(protocol.Protocol):
    limmits = {
        1: [[-65 / 180. * math.pi, 2395], [90 / 180. * math.pi, 543]],
        2: [[-135 / 180. * math.pi, 543], [0 / 180. * math.pi, 2065]],
        3: [[-150 / 180. * math.pi, 2500], [0 / 180. * math.pi, 804]],
        4: [[0 / 180. * math.pi, 1000], [110 / 180. * math.pi, 2300]],
        5: [[-105 / 180. * math.pi, 2500], [90 / 180. * math.pi, 870]],
        6: [[0 / 180. * math.pi, 1239], [85 / 180. * math.pi, 1913]]}

    def __init__(self, **kwargs):
        protocol.Protocol.__init__(self, **kwargs)
        self.lock = threading.Lock()

    def set_limmit(self, index, limmits):
        with self.lock:
            if index in self.limmits:
                self.limmits[index] = limmits

    def rotate(self, index, angle):
        with self.lock:
            if index not in self.limmits:
                RuntimeError("wrong index:{}".format(index))

        limmit = self.limmits[index]

        if angle < limmit[0][0]:
            angle = limmit[0][0]

        if angle > limmit[1][0]:
            angle = limmit[1][0]

        # делаем поворот
        v = (angle - limmit[0][0]) / (limmit[1][0] - limmit[0][0]) *\
            (limmit[1][1] - limmit[0][1]) + limmit[0][1]
        self.move_servo(index, int(v), time_move_sec=0.1)

    def get_angle(self, index, angle):
        if index not in self.limmits:
            RuntimeError("wrong index:{}".format(index))

        limmit = self.limmits[index]

        if angle < limmit[0][0]:
            angle = limmit[0][0]

        if angle > limmit[1][0]:
            angle = limmit[1][0]

        # делаем поворот
        return index, (angle - limmit[0][0]) / (limmit[1][0] - limmit[0][0]) *\
            (limmit[1][1] - limmit[0][1]) + limmit[0][1]

    def move_hand(self, angles):
        with self.lock:
            data = [self.get_angle(index, angle) for index, angle in angles]
        self.move_servos(data, 0.1)


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
    proto.rotate(1, -90 / 180. * math.pi)
    time.sleep(1)
    proto.rotate(1, 0 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(1, -90 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(2, 0 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(2, -90.0 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(1, 0 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(0, -45 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(3, 0 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(3, 90 / 180. * math.pi)

    time.sleep(1)
    proto.rotate(3, 120 / 180. * math.pi)
