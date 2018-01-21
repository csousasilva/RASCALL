from ATMOS_Functional import Functional

class Functional_Parser:

    def functional_dictionary_for(self, functional_data):
        functional_dictionary = {}
        print "func rows ", len(functional_data)

        for line in functional_data:
            columns = line.strip().split()

            functional = Functional(columns)

            if functional_dictionary.has_key(functional.code):
                for symmetry in functional.symmetries:
                    functional_dictionary[functional.code].addSymmetry(symmetry)
            else:
                functional_dictionary[functional.code] = functional

        return functional_dictionary