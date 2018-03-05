# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:45:49 2017

@author: cssilva

Version
"""

# ATMOS 1 - plotting the spectral features of individual functionals within molecules

import cPickle as pickle
from ATMOS_Functional_Parser import Functional_Parser
from ATMOS_Molecule_Parser import Molecule_Parser
from ATMOS_Plotter import Plotter
from ATMOS_Molecule_Filter import Molecule_Filter


import NIST_spectra


import NIST_spectra


# Load Functionals
# Example data
# COC C-O-C sbend 2500 2720 weak
# COC C-O-C abend 2800 2920 strong
with open('functionals_formatted.csv','rU') as f:
    functional_data = f.readlines()
    functional_parser = Functional_Parser()
    functional_dictionary = functional_parser.functional_dictionary_for(functional_data)

functional_to_check = functional_dictionary['[!#1]N(=O)=O']
print 'functional_to_check', len(functional_to_check.symmetries)

print 'Functional dictionary sample', len(functional_dictionary)

# Load Molecules
#Molecule dictionary sample [('C(C1)(C1F)(CC)', [('[H]C([H])(C)C', 2), ('[H]C([H])([!#1])[!#1]', 2),('[H]C([H])([H])C', 1), ('[H]C([H])([H])[!#1]', 1)]),...]
molecule_file_name = "dict_funct_ATMOS_Feb2018.p"
molecule_dictionary = pickle.load(open(molecule_file_name, "rb"))
molecule_parser = Molecule_Parser()
molecules = molecule_parser.molecules_for(molecule_dictionary, functional_dictionary)


print 'Molecule dictionary sample', molecule_dictionary.items()[:5]
#print 'Functionals for molecule C(C)NCC(O)', molecule_dictionary.get('C(C)NCC(O)')


# for molecule_code, molecule_functionals in molecule_dictionary.iteritems():
#     if len(molecule_dictionary.get(molecule_code)) >= 12:
#         if molecule_code in plotables:
#             print molecule_code, ' with ',len(molecule_dictionary.get(molecule_code)), ' functionals'
#         else:
#             print molecule_code, 'no linelist but these functionals:', molecule_dictionary.get(molecule_code)


# looks through all of the plottable molecules
plotables = []
plotable_molecules = open('plotable_molecules', "r")
for line in plotable_molecules:
    columns = line.strip().split()

    plotables.append(columns[0])
# print 'Plotables', plotables

#[H]OP([H])([!#1])=O
#Functional for HCN, specifically for the ≡C-H bending and stretching motions, is '[H]C#C[!#1]'

for molecule_code, molecule_functionals in molecule_dictionary.iteritems():
     if len(molecule_dictionary.get(molecule_code)) >= 1:
        if any('[H]OP(=O)(O[H])OC([H])([H])[H]' in s for s in molecule_dictionary.get(molecule_code)) :
            if molecule_code in plotables:
                print molecule_code, ' with ', len(molecule_dictionary.get(molecule_code)), ' functionals'
            else:
                print molecule_code, 'no linelist but these functionals:', molecule_dictionary.get(molecule_code)

molecules_with_triplebondCH = []
for molecule_code, molecule_functionals in molecule_dictionary.iteritems():
     if any('[H]C#C[!#1]' in s for s in molecule_dictionary.get(molecule_code)):
         #print molecule_code, 'has ≡C-H functional and all these other functionals:', molecule_dictionary.get(molecule_code)
         molecules_with_triplebondCH.append(molecule_code)

#print len(molecules_with_triplebondCH), 'molecules have a similar ≡C-H functional'
#print molecules_with_triplebondCH

molecules_with_triplebondCH_and_spectra = []
for molecule_code in molecules_with_triplebondCH:
    if molecule_code in plotables:
#        print molecule_code, 'has spectra'
        molecules_with_triplebondCH_and_spectra.append(molecule_code)
#    else:
#        print molecule_code, 'no linelist '

#print len(molecules_with_triplebondCH_and_spectra), 'molecules have a similar ≡C-H functional and spectra'
#print molecules_with_triplebondCH_and_spectra


#co2 atmosphere
co2_atmosphere= [(420.4,524.0),(822.4,922.8),(992.8,1092.8),(1099.6,1890.0),(1941.6,2042.0),(2162.0,2262.0),
              (2420.0,3482.0),(3784.0,4736.0),(5172.0,6072.0),(6122.0,6222.0),(6266.0,6366.0),
              (6386.0,6892.0),(7014.0,8176.0),(8208.0,8308.0)]

#Earth atmosphere
earth_atmosphere = [(430.4,530.4),(530.8,630.8),(705.2,1335.6),(1344.0,1444.0),(1585.6,1685.6),
                    (1816.0,1916.0),(1928.0,2284.0),(2404.0,3504.0),(3514.0,3614.0),
                    (3976.0,5208.0),(5490.0,7116.0),(7132.0,7232.0)]
earth2_atmosphere = [(802.8,972.4),(2402.0,2796.0),(4434.0,4806.0),(5626.0,6702.0)] #plus out of range windows between 7540.0-14765.0



#Methane atmosphere
methane_atmosphere= [(420.4,1042.4),(1044.4,1144.4),(1861.6,2272.0),(3320.0,3636.0),
                    (4754.0,5082.0),(5158.0,5258.0),(6268.0,6610.0),(6612.0,6712.0),
                    (7704.0,8116.0),(8144.0,8244.0),(9058.0,11020.0)]

methane2 = [(420.4,992.4),(1902.8,2282.0),(3362.0,3534.0),(4894.0,5002.0),(7920.0,8022.0),(9186.0,10900.0),(11545.0,14350.0)]

#Prebiotic Earth-like windows
prebio_earth = [(5178.0,5278.0),(6550.0,6866.0),(7630.0,8132.0),(8946.0,11175.0),(11380.0,12315.0)]

prebio_earth2 = [(420.4, 525.6), (1632.0, 1885.6), (2414.0, 2546.0), (3206.0, 3360.0), (3366.0, 3482.0),
                 (3934.0, 4034.0), (4630.0, 4736.0), (5166.0, 5316.0), (5320.0, 5558.0), (6374.0, 6892.0),
                 (7462.0, 8472.0), (8730.0, 15830.0)]

#features of HCN, approximately. See hcn.agr for spectra at three resolutions
hcn_regions= [(0.0,100.0),(600.0,820.0),(1340.0,1500.0),(3200.0,3400.0)]
hcn_strong = [(0.0,100.0),(600.0,820.0)]
hcn_strong_infrared = [(600.0,820.0)]

#test_window
test_window = [(600,950),(1400,1500)]

# print co2_windows[0][0] gives the first item of the first tuple (low freq of the first window)

# Finds all the strong features whose average frequency is within a window
atmosphere = methane2
intensity = 3

molecule_filter = Molecule_Filter(molecules)
#filtered_molecules = molecule_filter.filter_for_region(atmosphere)


strength_filtered_molecules = molecule_filter.filter_for_region_and_intensity(atmosphere, intensity)
print "our return", len(strength_filtered_molecules)



#strong_window_molecules = filtered_molecules[1]



                    
#                for point in window_filtered_list:
#  #      print point
#                window_molecules.append(molecule.code)
#                if point[1] >= 3:
                    
 #           window_filtered_list = list(filter(lambda x: ((window_low < low_frequency < window_high) and (window_low < high_frequency < window_high)), molecule.high_and_low_frequencies()))
            #print molecule.high_and_low_frequencies()[0][0],molecule.high_and_low_frequencies()[0][1], molecule.average_points()[0][0]
#    low_filtered_list = list(filter(lambda x: 600 < x[0] < 800, molecule.high_and_low_frequencies()[0]))
 

#and window_low < x[1] < window_high


#            print point
               
#    if len(window_filtered_list) > 0:
#        window_molecules.append(molecule.code)
#        print points
#        strong_filtered_list = list(filter(lambda y: y[1] == 3, points))
#        if len(strong_filtered_list) > 0:
#            strong_window_molecules.append(molecule_code)
        
#        print 'Molecule exits in window', molecule.code, (filtered_list)

#print 'List of Molecules', strong_window_molecules


#looks through all of the plottable molecules and sees which exist in window
count_exists = 0
count_doesnt_exist = 0
for mol in set(strength_filtered_molecules):
    if mol in plotables:
        count_exists = count_exists + 1
    else:
        count_doesnt_exist = count_doesnt_exist + 1
        
print count_doesnt_exist, 'do not have linelists'
print count_exists, 'have a linelist'

#plot experimental data together with ATMOS data
#molecule_code = "CCCCC#N"
print molecule_code, ' with ', molecule_dictionary.get(molecule_code), ' functionals'


#experimental_points = NIST_spectra.nist_spectrum(molecule_code)
#plt.plot(experimental_points[0], experimental_points[1])

#molecule_to_plot = molecules[molecule_code]
plotter = Plotter()

#plotter.plot_molecule_band_centers(molecule_to_plot)
#plotter.plot_NIST_spectrum(molecule_code)
#plotter.plot_ATMOS_crosssections(molecule_code)


#plotter.show(molecule_code)


#[H]OP([H])([!#1])=O
#Functional for HCN, specifically for the ≡C-H bending and stretching motions, is '[H]C#C[!#1]'


#Code to plot all molecules with NIST spectra alongside ATMOS
for molecule_code, molecule_functionals in molecule_dictionary.iteritems():
      if molecule_code in plotables:
          print 'plotting', molecule_code
          plotter.plot_molecule_band_centers(molecules[molecule_code])
          plotter.plot_NIST_spectrum(molecule_code)

          plotter.show(molecule_code)

plotter.show(molecule_code)


