from .symmetry import Symmetry
from .symmetry import Intensity
from .symmetry import Property
import numpy as np


class Functional:

    def __init__(self, functional_row):
        self.code = functional_row[0]
        symmetry = Symmetry(functional_row[1])
        self.symmetries = []

        low = functional_row[2]
        high = functional_row[3]
        intensity = Intensity.fromString(functional_row[4])
        intensity_quant = functional_row[5]
        line_shape = functional_row[6]
        self.source = functional_row[7]
        functional_class = functional_row[8]
        functional_type = functional_row[9]
        notes = functional_row[10]


        property = Property(low, high, intensity, functional_class)
        symmetry.addProperty(property)

        self.addSymmetry(symmetry)
        # (self.code, self.symmetries)

    def addSymmetry(self, symmetry):
        self.symmetries.append(symmetry)

    def averageSymmetries(self):
        uniqueSymmetries = set(map(lambda symmetry: symmetry.type, self.symmetries))

        filteredSymmetries = []
        averageSymmetries = []

        for uniqueSymmetry in uniqueSymmetries:
            matchingSymmetries = list(filter(lambda symmetry: symmetry.type == uniqueSymmetry, self.symmetries))
            filteredSymmetries.append(matchingSymmetries)

        for likeSymmetries in filteredSymmetries:
            if likeSymmetries[0].properties[0].low == 'UNK':
                continue
            else:
                allLows = list(map(lambda symmetry: float(symmetry.properties[0].low), likeSymmetries))
                allHighs = list(map(lambda symmetry: float(symmetry.properties[0].high), likeSymmetries))
                allInts = list(map(lambda symmetry: float(symmetry.properties[0].intensity.value), likeSymmetries))
                averageLow = np.mean(allLows)
                averageHigh = np.mean(allHighs)
                averageInt = np.mean(allInts)
                averageSymmetry = Symmetry(likeSymmetries[0].type)
                averageProperty = Property(averageLow, averageHigh, averageInt, likeSymmetries[0].properties[0].functional_class)
                averageSymmetry.addProperty(averageProperty)
                averageSymmetries.append(averageSymmetry)

        return averageSymmetries

    # __repr__ is what defines the description of an object when it is printed.
    def __repr__(self):
        property_descriptions = []
        for symmetry in self.averageSymmetries():
            for property in symmetry.properties:
                if property.low != 'UNK':
                    functional_string = (self.code, symmetry.type, int(property.frequency_average()),\
                            "{0:.2g}".format(property.intensity), self.source)
                    functional_string = str(functional_string)
                    property_descriptions.append(functional_string)
                elif property.low == 'UNK':
                    functional_string = (self.code, "unknown properties")
                    functional_string = str(functional_string)
                    property_descriptions.append(functional_string)

        property_descriptions = '\n'.join(property_descriptions)
        property_descriptions_string = str(property_descriptions)
        return property_descriptions_string

    __str__ = __repr__






