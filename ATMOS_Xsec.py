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

import os
import sys
import cPickle as pickle
from scipy.special import wofz

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../..'))

from ATMOS_Calc import *
from SEAS_Main.atmosphere_effects.biosig_molecule import biosig_interpolate


VERBOSE = False


def V(x, alpha, gamma):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.

    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return np.real(wofz((x + 1j*gamma)/sigma/np.sqrt(2))) / sigma\
                                                           /np.sqrt(2*np.pi)



class ATMOS_1_Simulator():
    
    def __init__(self, molecule_smile, atmosphere_window, pressure, temperature):
        
        self.smiles = molecule_smile
        self.windows = atmosphere_window
        self.pressure = pressure
        self.temperature = temperature
    
    def get_cross_section(self, nu):

        self.load_functional_dictionary()
        self.load_plotables()
        self.load_molecules()
        self.load_atmosphere_windows()

        #self.calculate_detection()

        selected = self.molecules[self.smiles]
        
        xs, ys = zip(*set(selected.average_points()))


        # making a fake profile over the molecule
        alpha, gamma = 5, 5
        xsec = np.zeros(len(nu))
        orig_array = np.linspace(-100,100,1000)
        for i,x in enumerate(xs):
            x_array = orig_array + x
            y_array = V(orig_array, alpha, gamma)*ys[i]*alpha*4.5
            yinterp = biosig_interpolate(x_array,y_array,nu,"C")
            xsec += yinterp
        
        return xsec


    def load_functional_dictionary(self):
    
        # Load Functionals
        
        # Example data
        # COC C-O-C sbend 2500 2720 weak
        # COC C-O-C abend 2800 2920 strong
        
        functional_dictionary = {}
        #functional_data = open('func_table_reliable.txt', "r")
        
        with open('../../SEAS_Aux/ATMOS_1/func_testvim.spaces') as f:
            functional_data = f.readlines()
        
        if VERBOSE:
            print len(functional_data)
            
        #this bit isnt working, maybe because the file does not have normal spacing?
        for line in functional_data:
            
            if VERBOSE:
                print line
            columns = line.strip().split()
            
            code = columns[0]
        #    name = columns[1]
            symmetry_name = columns[1]
            low = float(columns[2])
            high = float(columns[3])
            intensity = Intensity.fromString(columns[4])
        
            if not functional_dictionary.has_key(code):
                # Extra logic for determining which type of functional we are dealing with.
                if "CF" in code:
                    f = ExpFunctional(code, 2) # in this case we are setting 'a' for this functional's graphing function to 2.
                else:
                    f = Functional(code)
        
                functional_dictionary[code] = f
        
            symmetry = Symmetry(symmetry_name)
            property = Property(low, high, intensity)
        
            functional_dictionary[code].addSymmetry(symmetry)
            symmetry.addProperty(property)    
        
        self.functional_dictionary = functional_dictionary
        return functional_dictionary
    
    def load_plotables(self):
    
        #looks through all of the plottable molecules
        plotables = []
        plotable_molecules = open('../../SEAS_Aux/ATMOS_1/plotable_molecules', "r")
        for line in plotable_molecules:
            columns = line.strip().split()
            
            plotables.append(columns[0])
        #print 'Plotables', plotables
    
        self.plotables = plotables
        return plotables
    
    def load_molecules(self):
        
        # Load Molecules
        if VERBOSE:
            print self.functional_dictionary.keys()
        
        molecules = {}
        #molecule_dictionary = pickle.load(open("dict_sorted_results_func_intra_test2_numbers.p", "rb"))
        molecule_dictionary = pickle.load(open("../../SEAS_Aux/ATMOS_1/dict_sorted_results_func_intra_table_part.p", "rb"))
        
        if VERBOSE:
            print 'Molecule dictionary sample', molecule_dictionary.items()[:5]
            print 'Functional for molecule SCC(NN)=O', molecule_dictionary.get('SCC(NN)=O')
            print '\n', 'Number of molecules', len(molecule_dictionary.items())
    
        for molecule_code, molecule_functionals in molecule_dictionary.iteritems():
            molecule = Molecule(molecule_code,self.functional_dictionary)
            molecule.load_atmosphere_parameters(self.pressure, self.temperature)
            for functional_tuple in molecule_functionals:
                if '#' in functional_tuple[0]:
                    
                    functional_code = functional_tuple[0]
                    functional_incidence = functional_tuple[1]
                    molecule.addFunctional(functional_code, functional_incidence)
        
            molecules[molecule_code] = molecule    
    
        self.molecules = molecules
        return molecules
    
    
    def load_atmosphere_windows(self):
        """
        need to completely rework this part
        """
    
        #co2 atmosphere
        co2_atmosphere= [(420.4,524.0),(822.4,922.8),(992.8,1092.8),(1099.6,1890.0),(1941.6,2042.0),(2162.0,2262.0),
                      (2420.0,3482.0),(3784.0,4736.0),(5172.0,6072.0),(6122.0,6222.0),(6266.0,6366.0),
                      (6386.0,6892.0),(7014.0,8176.0),(8208.0,8308.0)]
        # print co2_windows[0][0] gives the first item of the first tuple (low freq of the first window)
          
        #Earth atmosphere
        earth_atmosphere = [(430.4,530.4),(530.8,630.8),(705.2,1335.6),(1344.0,1444.0),(1585.6,1685.6),
                            (1816.0,1916.0),(1928.0,2284.0),(2404.0,3504.0),(3514.0,3614.0),
                            (3976.0,5208.0),(5490.0,7116.0),(7132.0,7232.0)]
        earth2_atmosphere = [(802.8,972.4),(2402.0,2796.0),(4434.0,4806.0),(5626.0,6702.0)] #plus out of range windows between 7540.0-14765.0
        
    
        #Methane atmosphere
        methane_atmosphere= [(420.4,1042.4),(1044.4,1144.4),(1861.6,2272.0),(3320.0,3636.0),
                            (4754.0,5082.0),(5158.0,5258.0),(6268.0,6610.0),(6612.0,6712.0),
                            (7704.0,8116.0),(8144.0,8244.0),(9058.0,11020.0)]
    
        if self.windows == "earth2_atmosphere":
            atmosphere = earth2_atmosphere
            
        return atmosphere
    
    
    def calculate_detection(self):
    
        window_molecules = []
        strong_window_molecules = []
        
        for molecule_code in self.molecules:
            molecule = self.molecules[molecule_code]
        
            for window in self.windows:
                
                window_low = window[0]
                window_high = window[1]
                for molecule_point in molecule.high_and_low_frequencies():
                    low_frequency = molecule_point[0]
                    high_frequency = molecule_point[1]
                    point_intensity = molecule_point[2]
                    if window_low < low_frequency < window_high and window_low < high_frequency < window_high:
                        window_molecules.append(molecule.code)
                        if  point_intensity >= 3:
                            strong_window_molecules.append(molecule_code)

        if VERBOSE:                            
            print 'Window range: from ',self.windows[0][0], ' to ', self.windows[-1][1]
            print 'Number of molecules in window', len(set(window_molecules))
            print 'Number of strong molecules in window', len(set(strong_window_molecules))
                            
        #looks through all of the plottable molecules and sees which exist in window
        count_exists = 0
        count_doesnt_exist = 0
        for mol in set(strong_window_molecules):
            if mol in self.plotables:
                count_exists = count_exists + 1
            else:
                count_doesnt_exist = count_doesnt_exist + 1
        
        if VERBOSE:
            print count_doesnt_exist, 'do not have linelists'
            print count_exists, 'have a linelist'





