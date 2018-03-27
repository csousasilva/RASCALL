import matplotlib.pyplot as plt
#import seaborn as sns
import NIST_spectra
import ATMOS_crosssections
import numpy as np

class Plotter:
    def plot_molecule_band_centers(self, molecule):
        # print len(example.functionals)

        # Plot points
        xs, ys = zip(*molecule.average_points())
        # print 'points', example.points()
        # plt.plot(xs, ys, linestyle='None', marker='o', color='black', linewidth=2)

        # window = range(3250, 3450)
        filtered_list = list(filter(lambda x: 1600 < x[0] < 1900, molecule.average_points()))
        # print 'filter:',(filtered_list)

        #print xs, ys
        markerline, stemlines, baseline = plt.stem(xs, ys, '-')
        plt.setp(baseline, 'color', 'r', 'linewidth', 1)

        # Plot branches
        # for line in example.branches():
        #     x, y = line
        #     markerline, stemlines, baseline = plt.stem(x, y, '-')
        #     plt.setp(baseline, color='r', linewidth=1, marker='None')

        # plt.xlim(1459,1459.5)
        print 'Molecule below : ', molecule.code


        # Plot lines
        # for line in example.lines():
        #    x, y = line

        #    plt.plot(x, y)

    def plot_NIST_spectrum(self, molecule_smile):
        Absorption_Boost = 3
        nu, coef = NIST_spectra.nist_spectrum(molecule_smile)

        abfix = []
        for i in coef:
            if i > 2:
                abfix.append(2)
            else:
                abfix.append(i)
        coef = np.array(abfix)
        absorb_baseline = 0.001  # baseline_als(absorb1, 10**6, 0.001, niter=10)
        absorb2 = coef - absorb_baseline
        coef2 = absorb2 / max(absorb2) * Absorption_Boost


        plt.plot(nu, coef2)


    def plot_ATMOS_crosssections(self, molecule_smile):

        nu, xsec = ATMOS_crosssections.ATMOS_crosssection(molecule_smile)
        plt.plot(nu, xsec, label="ATMOS")

    def show(self, molecule_smile):
        plt.xlabel('Wavenumbers')
        plt.ylabel('Intensity')
        plt.title(molecule_smile)
        plt.show()

