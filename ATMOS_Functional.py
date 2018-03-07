from ATMOS_Symmetry import Symmetry
from ATMOS_Symmetry import Intensity
from ATMOS_Symmetry import Property
import numpy as np


class Functional:

    def __init__(self, functional_row):
        self.code = functional_row[0]
        symmetry = Symmetry(functional_row[1])
        self.symmetries = []

        low = functional_row[2]
        high = functional_row[3]
        intensity = Intensity.fromString(functional_row[4])
        intensity_quant = functional_row[4]
        line_shape = functional_row[5]
        source = functional_row[6]
        functional_class = functional_row[7]
        functional_type = functional_row[8]
        notes = functional_row[9]


        property = Property(low, high, intensity)
        symmetry.addProperty(property)

        self.addSymmetry(symmetry)

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
            if likeSymmetries[0].properties[0].low == 'UNK': continue

            allLows = list(map(lambda symmetry: float(symmetry.properties[0].low), likeSymmetries))
            allHighs = list(map(lambda symmetry: float(symmetry.properties[0].high), likeSymmetries))
            allInts = list(map(lambda symmetry: float(symmetry.properties[0].intensity.value), likeSymmetries))
            averageLow = np.mean(allLows)
            averageHigh = np.mean(allHighs)
            averageInt = np.mean(allInts)
            averageSymmetry = Symmetry(likeSymmetries[0].type)
            averageProperty = Property(averageLow, averageHigh, averageInt)
            averageSymmetry.addProperty(averageProperty)
            averageSymmetries.append(averageSymmetry)

        return averageSymmetries





