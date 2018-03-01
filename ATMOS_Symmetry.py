from enum import Enum
import numpy as np

class Symmetry:
    def __init__(self, type):
        self.type = type
        self.properties = []

    def addProperty(self, property):
        self.properties.append(property)
        #print property.low, property.high, property.intensity.value


class Property:
    def __init__(self, low, high, intensity):
        self.low = low
        self.high = high
        self.intensity = intensity

    def frequency_average(self):
        return np.mean([float(self.high), float(self.low)])

class Intensity(Enum):
    w, w_m, m, m_s, s, UNK = 1, 1.5, 2, 2.5, 3, 0

    @classmethod
    def fromString(self, str):
        string = str.lower()
        if string == 's':
            return Intensity.s
        elif string == 'm-s' or 'm_s' :
            return Intensity.m_s
        elif string == 'm':
            return Intensity.m
        elif string == 'w-m' or 'w_m':
            return Intensity.w_m
        elif string == 'w':
            return Intensity.w
        elif string == 'UNK':
            return Intensity.UNK
