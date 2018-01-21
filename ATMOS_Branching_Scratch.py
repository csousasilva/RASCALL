# intensity_centre = 1.0
# freq_centre = 0.0
# bcon = float(10**(45)*(plank/(8*math.pi*math.pi*light_speed*5)))
# jmax = int(0.5 * (np.sqrt(((2*boltzmann*temperature)/(bcon*10**(-24))))) - 0.5)
# #
# for j in range(0, jmax):
#     dcon = (bcon * 10 ** (-3)) / (j + 1)
#     dcon_plus = (bcon * 10 ** (-3)) / (j + 2)
#     spacing = 2*bcon - ((4 * dcon_plus)*((j + 2)**3)) + ((4 * dcon)*((j + 1)**3))
#     intensity_j = intensity_centre * 5 * ((2 * j) + 1) * (10 ** (-2)) * np.e**(-(((bcon*10**(-24)) * (2 * j) * ((2*j) + 1)) / (boltzmann * temperature)))
#     position_j_pbranch = freq_centre - spacing
#     position_j_qbranch = freq_centre + spacing
#     print 'pbranch', j, position_j_pbranch, intensity_j
#     print 'qbranch', j, position_j_qbranch, intensity_j
# #


#in class molecule

# def containsElement(self, element_name):
#     # this assumes elements are a dictionary of the periodic table
#     return self.code.contains(elements[element_name])
#
#
# def line_shapes(self):
#     lines = []
#
#     for functional_tuple in self.functionals:
#         functional = functional_tuple[0]
#         for symmetry in functional.symmetries:
#             for property in symmetry.properties:
#                 x = np.linspace(property.low, property.high)
#                 y = functional.line_function(x, property.frequency_average(), property.intensity.value)
#                 lines.append((x, y))
#
#     return lines
#
#
# def branches(self):
#     branches = []
#
#     for functional_tuple in self.functionals:
#         functional = functional_tuple[0]
#         for symmetry in functional.symmetries:
#             for property in symmetry.properties:
#                 branches.append(self.prBranches(property))
#
#     return branches
#
#
# def atom_count(self):
#     atoms = len(re.sub(r"[^A-Z]+", '', self.code))
#
#     return atoms
#
#
# def prBranches(self, property):
#     pr_branch_x = []
#     pr_branch_y = []
#
#     bcon = float(constants.plank / (8 * math.pi * math.pi * constants.light_speed * self.atom_count() * 10 ** (-44)))
#     jmax = int(np.sqrt(
#         (constants.boltzmann * constants.temperature) / (2 * constants.plank * constants.light_speed * bcon)) - 0.5)
#
#     for j in range(0, jmax):
#         dcon = (bcon * 10 ** (-3)) / (j + 1)
#         dcon_plus = (bcon * 10 ** (-3)) / (j + 2)
#         spacing = 2 * bcon - ((4 * dcon_plus) * ((j + 2) ** 3)) + ((4 * dcon) * ((j + 1) ** 3))
#         intensity_j = property.intensity.value * ((2 * j) + 1) * np.e ** (
#             -((constants.plank * constants.light_speed * bcon * j * (j + 1)) / (
#             constants.boltzmann * constants.temperature)))
#
#         position_j_pbranch = property.frequency_average() - spacing
#         position_j_rbranch = property.frequency_average() + spacing
#         pr_branch_x.append(position_j_pbranch)
#         pr_branch_y.append(intensity_j)
#         pr_branch_x.append(position_j_rbranch)
#         pr_branch_y.append(intensity_j)
#
#     return (pr_branch_x, pr_branch_y)

#In class Functional
# def line_function(self, x, translateX, scaleY):
#     print("Calculating graph for functional '" + self.code + "': using default f()")
#
#     return (1 / (1 + pow((x - translateX), 2))) * scaleY


