import numpy as np
import re
import math
from . import constants

class Molecule:
    def __init__(self, code):
        self.code = code
        self.functionals = []

    @property
    def isHydrogenMuting(self):
        tripleBond = '[H]C#[!#1]'
        chBond = 'C[H]'
        functionals = list(map(lambda functionalTuple: functionalTuple[0], self.functionals))
        functionalCodes = list(map(lambda functional: functional.code, functionals))
        return tripleBond in functionalCodes and chBond in functionalCodes

    def addFunctional(self, functional, number):
        self.functionals.append((functional, number))


    def high_and_low_frequencies(self):
        frequencies = []

        for functional_tuple in self.functionals:
            functional = functional_tuple[0]

            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    if property.low != 'UNK':
                        frequencies.append((float(property.low), float(property.high), float(property.intensity.value)))

        return frequencies

    def muted_intensities(self):
        triple_bond = '[H]C#[!#1]'
        c_h_bond = 'C[H]'
        frequencies = []

        for functional_tuple in self.functionals:
            functional = functional_tuple[0]
            incidence = functional_tuple[1]

            if any(triple_bond in s for s in self.functionals):
                if any(c_h_bond in s for s in self.functionals):
                    c_h_bond.incidence = c_h_bond.incidence - triple_bond.incidence
                    if c_h_bond.incidence < 0:
                        c_h_bond.incidence = 0

            if incidence == 0:
                for symmetry in functional.symmetries:
                    for property in symmetry.properties:
                        frequencies.append((float(property.low), float(property.high), float(0.01)))

        return frequencies






