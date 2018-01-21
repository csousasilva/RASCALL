from ATMOS_Symmetry import Symmetry
from ATMOS_Symmetry import Intensity
from ATMOS_Symmetry import Property


class Functional:

    def __init__(self, functional_row):
        self.code = functional_row[0]
        symmetry = Symmetry(functional_row[1])
        self.symmetries = []

        low = functional_row[2]
        high = functional_row[3]
        intensity = Intensity.fromString(functional_row[4])

        property = Property(low, high, intensity)
        symmetry.addProperty(property)

        self.addSymmetry(symmetry)

    def addSymmetry(self, symmetry):
        self.symmetries.append(symmetry)



