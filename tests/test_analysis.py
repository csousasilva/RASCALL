from rascall.analysis import filter_halo, filter_hydro
import unittest

class MoleculeFamFilterTest(unittest.TestCase):
    def test_hydro(self):
        self.assertTrue(filter_hydro('CC#CC'))
        self.assertFalse(filter_hydro('OC(C#CC)C'))
        self.assertTrue(filter_hydro('CC#CC#CC'))
        self.assertFalse(filter_hydro('OC(=O)C#C(C)'))
        self.assertFalse(filter_hydro('C(CCl)#C(CCl)'))

    def test_halo(self):
        self.assertFalse(filter_halo('CC#CC'))
        self.assertTrue(filter_halo('C(CCl)#C(CCl)'))
        self.assertFalse(filter_halo('OC(=O)C#C(C)'))
        self.assertFalse(filter_halo('CC#CCC'))


