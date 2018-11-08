import numpy as np

# INPUT
# what region, e.g. a specific atmosphere
# what molecules - e.g. all, Carbon-molecules
# how strong, e.g. all features, or just the strong ones

# OUTPUT
# Molecules that fulfill criteria
# Number of these that have spectra in SQL database

class Molecule_Filter:
    def __init__(self, molecules):
        self.molecules = molecules

    def filter_for_region_and_intensity(self, region, intensity):
        filtered_by_region = self.filter_for_region(region)
        filtered_by_intensity = self.filter_for_intensity(intensity)

        filtered_by_region_and_intensity = []

        for molecule_code in self.molecules.keys():
            if filtered_by_region.__contains__(molecule_code) and filtered_by_intensity.__contains__(molecule_code):
                filtered_by_region_and_intensity.append(molecule_code)

        print ('Number of molecules in window above', intensity, "strength:", len(set(filtered_by_region_and_intensity)))
        return filtered_by_region_and_intensity


    def filter_for_region(self, region):
        window_molecules = []

        for molecule in self.molecules.values():
            for window in region:

                window_low = window[0]
                window_high = window[1]

                for molecule_point in molecule.high_and_low_frequencies():
                    low_frequency = molecule_point[0]
                    high_frequency = molecule_point[1]
                    #           print ("If statement contents \n", window_low, low_frequency, high_frequency, window_high)

                    if window_low < low_frequency < window_high and window_low < high_frequency < window_high:
                        window_molecules.append(molecule.code)




        print ('Window range: from ', region[0][0], ' to ', region[-1][1])
        print ('Number of molecules in window', len(set(window_molecules)))


        return (window_molecules)

    def filter_for_intensity(self, intensity):
        window_molecules_above_strength = []
        for molecule in self.molecules.values():
            for molecule_point in molecule.high_and_low_frequencies():
                point_intensity = molecule_point[2]
                if point_intensity >= intensity:
                    window_molecules_above_strength.append(molecule.code)


        return set(window_molecules_above_strength)

