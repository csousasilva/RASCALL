import unittest

from test import test_support

class ImportTest(unittest.TestCase):
    def test_00_rascall(self):
        import rascall
    def test_analysis(self):
        import rascall.analysis
    def test_branching_scratch(self):
        import rascall.branching_scratch
    def test_calc(self):
        import rascall.calc
    def test_catalogue(self):
        import rascall.catalogue
    def test_constants(self):
        import rascall.constants
    def test_crosssections(self):
        import rascall.crosssections
    def test_database(self):
        import rascall.database
    def test_db_management(self):
        import rascall.db_management
    def test_functional(self):
        import rascall.functional
    def test_functional_parser(self):
        import rascall.functional_parser
    def test_interpolate(self):
        import rascall.interpolate
    def test_jdx_reader(self):
        import rascall.jdx_Reader
    def test_molecule(self):
        import rascall.molecule
    def test_molecule_filter(self):
        import rascall.molecule_filter
    def test_molecule_parser(self):
        import rascall.molecule_parser
    def test_NIST_spectra(self):
        import rascall.NIST_spectra
    def test_plot_NIST(self):
        import rascall.plot_NIST
    def test_plotter(self):
        import rascall.plotter
    def test_symmetry(self):
        import rascall.symmetry
    def test_xsec(self):
        import rascall.xsec

