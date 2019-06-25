from .functional import Functional

class Functional_Parser:

    def functional_dictionary_for(self, functional_data):
        functional_dictionary = {}
        print ("Total Number of Functional Groups", len(functional_data))

        for line in functional_data:
            columns = line.strip().split(',')

            functional = Functional(columns)


            if functional.code in functional_dictionary:

                for symmetry in functional.symmetries:
                    functional_dictionary[functional.code].addSymmetry(symmetry)
            else:
                functional_dictionary[functional.code] = functional

        self.replaceUnkowns(functional_dictionary)
        return functional_dictionary


    def replaceUnkowns(self, functional_dictionary):
        for functional in functional_dictionary.values():
            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    if property.low == 'UNK':
                        principal_functional = property.functional_class.strip().split(' ')[1]
                        functionalToCopy = functional_dictionary[principal_functional]

                        functional.symmetries = functionalToCopy.symmetries