import numpy as np
import re
import math
import ATMOS_constants as constants

class Molecule:
    def __init__(self, code):
        self.code = code
        self.functionals = []

    def addFunctional(self, functional, number):
        self.functionals.append((functional, number))

    def average_points(self):
        points = []

        for functional_tuple in self.functionals:
            functional = functional_tuple[0]
            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    points.append((property.frequency_average(), property.intensity.value))

        return points

    def high_and_low_frequencies(self):
        frequencies = []

        for functional_tuple in self.functionals:
            functional = functional_tuple[0]

            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    if property.low != 'UNK':
                        frequencies.append((float(property.low), float(property.high), float(property.intensity.value)))

        return frequencies
