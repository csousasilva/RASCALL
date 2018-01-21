import matplotlib.pyplot as plt
#import seaborn as sns


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

        print xs, ys
        markerline, stemlines, baseline = plt.stem(xs, ys, '-')
        plt.setp(baseline, 'color', 'r', 'linewidth', 1)

        # Plot branches
        # for line in example.branches():
        #     x, y = line
        #     markerline, stemlines, baseline = plt.stem(x, y, '-')
        #     plt.setp(baseline, color='r', linewidth=1, marker='None')

        # plt.xlim(1459,1459.5)
        print 'Molecule below : ', molecule.code
        plt.show()

        # Plot lines
        # for line in example.lines():
        #    x, y = line

        #    plt.plot(x, y)