import unittest
import pickle as pickle
from rascall.molecule_parser import Molecule_Parser
from rascall.molecule import Molecule

from rascall import get_file
from rascall.functional_parser import Functional_Parser


def get_functionals(filename='functionals_formatted_eye_edit.csv'):
    # Load Functionals
    # Example data
    # COC C-O-C sbend 2500 2720 weak
    # COC C-O-C abend 2800 2920 strong
    with open(get_file('functionals.csv'), 'rU') as fhl:
        return Functional_Parser().functional_dictionary_for(fhl.readlines())

#print 'Total number of unique functionals', len(functional_dictionary)

def get_molecules(filename=get_file('dictfunct.p')):
    # Load Molecules
    #Molecule dictionary sample [('C(C1)(C1F)(CC)', [('[H]C([H])(C)C', 2), ('[H]C([H])([!#1])[!#1]', 2),('[H]C([H])([H])C', 1), ('[H]C([H])([H])[!#1]', 1)]),...]
    return pickle.load(open(filename, "rb"))

class MolecularParserTest(unittest.TestCase):
    def test_parsing(self):
        mpt = Molecule_Parser()
        functional_dictionary = get_functionals()
        molecule_dictionary = get_molecules()
        mpt.molecules_for(molecule_dictionary, functional_dictionary)


 #   def test_equality(self):
 #       self.assertEquals
 #       self.assertR