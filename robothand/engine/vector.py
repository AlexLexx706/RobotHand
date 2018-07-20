# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import scipy.linalg
import math


def mag(A):
    return np.linalg.norm(A)


def mag2(A):
    r = np.linalg.norm(A)
    return r * r


def norm(A):
    return A / np.linalg.norm(A)


def dot(A, B):
    return np.dot(A, B)


def cross(A, B):
    return np.cross(A, B).view(Vector)


def proj(A, B):
    return dot(A, norm(B)) * norm(B)


def comp(A, B):
    return dot(A, norm(B))


def diff_angle(A, B):
    return math.acos(np.dot(norm(A), norm(B)))


def rotate(A, theta, B):
    return np.dot(
        scipy.linalg.expm3(np.cross(
            np.eye(3), B / scipy.linalg.norm(B) * theta)), A).view(Vector)


def astuple(A):
    try:
        return tuple(astuple(i) for i in A)
    except TypeError:
        return A


class Vector(np.ndarray):
    def __new__(subtype, data_x=1.0, y=0.0, z=0.0):

        if isinstance(data_x, Vector):
            return data_x.copy()

        if isinstance(data_x, np.ndarray):
            new = data_x.copy().view(subtype)
            intype = np.dtype(float)

            if intype != data_x.dtype:
                return new.astype(intype)
            return new

        if not(isinstance(data_x, list) or isinstance(data_x, tuple)):
            data_x = (data_x, y, z)

        return np.array(data_x, dtype=np.dtype(float)).view(subtype)

    def cross(self, v):
        return np.cross(self, v).view(Vector)

    def __getattr__(self, name):
        if name == "mag":
            return np.linalg.norm(self)
        elif name == "mag2":
            r = np.linalg.norm(self)
            return r * r
        raise AttributeError()

    def norm(self):
        if self.mag == 0:
            raise RuntimeError()
        self /= self.mag
        return self

    def dot(self, B):
        return dot(self, B)

    def proj(self, B):
        return proj(self, B)

    def comp(self, B):
        return comp(self, B)

    def diff_angle(self, B):
        return diff_angle(self, B)

    def rotate(self, theta, B):
        self = rotate(self, theta, B)
        return self

    def astuple(self):
        return astuple(self)


if __name__ == "__main__":
    from visual_common.cvisual import vector as v_vector

    print(type(mag(Vector(2, 0, 0))))
    print(type(mag2(Vector(2, 0, 0))))
    print(type(norm(Vector(2, 0, 0))))
    print(type(dot(Vector(1, 0, 0), Vector(0.3, 1, 0))))
    print(type(cross(Vector(1, 0, 0), Vector(0.3, 1, 0))))
    print(type(proj(Vector(1, 0, 0), Vector(0.3, 1, 0))))
    print(type(comp(Vector(1, 0, 0), Vector(0.3, 1, 0))))
    print(type(diff_angle(Vector(1, 0, 0), vector(-1, 1, 0))))
    print(type(rotate(Vector(1, 0, 0), 1, Vector(0, 1, 0))))
    print(type(astuple(Vector(1, 0, 0))))

    print (Vector(2, 0, 0).mag, v_vector(2, 0, 0).mag)
    print (Vector(2, 0, 0).mag2, v_vector(2, 0, 0).mag2)
    print (Vector(2, 0, 0).norm(), v_vector(2, 0, 0).norm())
    print(
        Vector(1, 0, 0).dot(Vector(0.3, 1, 0)),
        v_vector(1, 0, 0).dot(Vector(0.3, 1, 0)))

    print(
        Vector(1, 0, 0).cross(Vector(0.3, 1, 0)),
        v_vector(1, 0, 0).cross(Vector(0.3, 1, 0)))
    print(
        Vector(1, 0, 0).proj(Vector(0.3, 1, 0)),
        v_vector(1, 0, 0).proj(Vector(0.3, 1, 0)))
    print(
        Vector(1, 0, 0).comp(Vector(0.3, 1, 0)),
        v_vector(1, 0, 0).comp(v_vector(0.3, 1, 0)))
    print(
        Vector(1, 0, 0).diff_angle(vector(-1, 1, 0)),
        v_vector(1, 0, 0).diff_angle(vector(-1, 1, 0)))
    print(
        Vector(1, 0, 0).rotate(1, Vector(0, 1, 0)),
        v_vector(1, 0, 0).rotate(1, v_vector(0, 1, 0)))
    print(
        Vector(1, 0, 0).astuple(),
        v_vector(1, 0, 0).astuple())
