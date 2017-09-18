# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright (C) 2017 - Massachusetts Institute of Technology (MIT)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""

Loader for ATMOS molecular cross sections


TODO:

    1. Need Code Documentation

@author: cssilva
@editor: Zhuchang Zhan


"""

import re
import os
import sys
import numpy as np
from enum import Enum

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../..'))

from SEAS_Utils.common_utils.constants import *




class Molecule:
    
    def __init__(self, code, functional_dictionary):
        self.code = code
        self.functional_dictionary = functional_dictionary
        self.functionals = []
        
    def load_atmosphere_parameters(self, pressure, temperature):
        self.pressure = pressure
        self.temperature = temperature
            
    def addFunctional(self, functional, number):
        self.functionals.append((functional, number))

    def contains(self, element_name):
        return self.code.contains(elements[element_name])

    def line_shapes(self):
        lines = []

        for functional_tuple in self.functionals:
            functional = self.functional_dictionary[functional_tuple[0]]
            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    x = np.linspace(property.low, property.high)
                    y = functional.line_function(x, property.frequency_average(), property.intensity.value)
                    lines.append((x, y))
                    
        return lines

    def branches(self):
        branches = []

        for functional_tuple in self.functionals:
            functional = self.functional_dictionary[functional_tuple[0]]
            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    branches.append(self.prBranches(property))

        return branches

    def atom_count(self):
        atoms = len(re.sub(r"[^A-Z]+",'',self.code))

        return atoms

    def prBranches(self, property):
        pr_branch_x = []
        pr_branch_y = []

        bcon = float(HPlanck / (8 * np.pi * np.pi * c * self.atom_count() * 10**(-44)))
        jmax = int(np.sqrt((BoltK * self.temperature)/(2 * HPlanck * c * bcon)) - 0.5)

        for j in range(0, jmax):
            dcon = (bcon * 10 ** (-3)) / (j + 1)
            dcon_plus = (bcon * 10 ** (-3)) / (j + 2)
            spacing = 2 * bcon - ((4 * dcon_plus) * ((j + 2) ** 3)) + ((4 * dcon) * ((j + 1) ** 3))
            intensity_j = property.intensity.value * ((2* j) + 1) * np.e**(-((HPlanck * c * bcon * j * (j + 1))/(BoltK * self.temperature)))

            position_j_pbranch = property.frequency_average() - spacing
            position_j_rbranch = property.frequency_average() + spacing
            pr_branch_x.append(position_j_pbranch)
            pr_branch_y.append(intensity_j)
            pr_branch_x.append(position_j_rbranch)
            pr_branch_y.append(intensity_j)

        return (pr_branch_x, pr_branch_y)

    def average_points(self):
        points = []

        for functional_tuple in self.functionals:
            functional_code = functional_tuple[0]
            if functional_code in self.functional_dictionary.keys():
                functional = self.functional_dictionary[functional_code]
                for symmetry in functional.symmetries:
                    for property in symmetry.properties:
                        points.append((property.frequency_average(), property.intensity.value))
                
        return points
    
    def high_and_low_frequencies(self):
        frequencies = []

        for functional_tuple in self.functionals:
            functional_code = functional_tuple[0]
            if functional_code in self.functional_dictionary.keys():
                functional = self.functional_dictionary[functional_code]
                for symmetry in functional.symmetries:
                    for property in symmetry.properties:
                        frequencies.append((property.low, property.high, property.intensity.value))
                    
        return frequencies
    

class Functional:
    
    def __init__(self, code, a = 1, b = 1):
        self.code = code
        self.a = a
        self.b = b
        self.symmetries = []

    def addSymmetry(self, symmetry):
        symmetry.functional = self
        self.symmetries.append(symmetry)

    def line_function(self, x, translateX, scaleY):
        print("Calculating graph for functional '" + self.code + "': using default f()")

        return (1/(1+pow((x - translateX),2))) * scaleY



# Specify a subclass of functional that has a different graphing function
class ExpFunctional(Functional):
    
    def line_function(self, x, translateX, scaleY):
        print("Calculating graph for functional '" + self.code + "': using exp f()")
        return (self.a * np.exp(-pow((x - translateX), 2))) * scaleY

class Symmetry:
    
    def __init__(self, type):
        self.type = type
        self.properties = []

    def addProperty(self, property):
        property.symmetry = self
        self.properties.append(property)

class Property:
    
    def __init__(self, low, high, intensity):
        self.low = low
        self.high = high
        self.intensity = intensity

    def frequency_average(self):
        return np.mean([self.high,self.low])
#        return self.low + ((self.high - self.low) / 2)

class Intensity(Enum):
    
    w,w_m,m,m_s,s = 1,1.5,2,2.5,3

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














