from enum import Enum
import numpy as np

class Symmetry:
    def __init__(self, type):
        self.type = type
        self.properties = []

    def addProperty(self, property):
        self.properties.append(property)


class Property:
    def __init__(self, low, high, intensity):
        self.low = low
        self.high = high
        self.intensity = intensity

    def frequency_average(self):
        return np.mean([float(self.high), float(self.low)])

class Intensity(Enum):
    w, w_m, m, m_s, s = 1, 1.5, 2, 2.5, 3

    @classmethod
    def fromString(self, str):
        if str == 's':
            return Intensity.s
        elif str == 'm_s':
            return Intensity.m_s
        elif str == 'm':
            return Intensity.m
        elif str == 'w_m':
            return Intensity.w_m
        elif str == 'w':
            return Intensity.w
