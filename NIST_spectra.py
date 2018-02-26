
import os
import sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(DIR, '../../../SEAS/BioSig_SEAS/'))

import SEAS_Utils.common_utils.db_management2 as dbm
from SEAS_Main.atmosphere_effects.biosig_molecule import load_NIST_spectra

import jdx
import matplotlib.pyplot as plt
import numpy as np


def NIST_Smile_List(expect="all"):
    kwargs = {"db_name": "Molecule_DB.db",
              "user": "azariven",
              "dir": "../../../SEAS/BioSig_SEAS/input/molecule_info",
              "DEBUG": False, "REMOVE": False, "BACKUP": False, "OVERWRITE": False}

    cross_db = dbm.database(**kwargs)
    cross_db.access_db()

    cmd = 'SELECT ID.SMILES, ID.inchikey, Spectra.CAS, ID.Formula, ID.IUPAC_chemical_name  \
            FROM ID,Spectra WHERE ID.SMILES=Spectra.Smiles AND Spectra.Is_Gas="Y"'

    result = cross_db.c.execute(cmd)
    data = np.array(result.fetchall()).T

    smiles = data[0]
    inchikeys = data[1]
    CAS = data[2]
    formula = data[3]
    name = data[4]
    if expect == "all":
        return smiles, inchikeys, CAS, formula, name


def test_nist():

    file = "c2h2_test.jdx"
    data = jdx.JdxFile(file)

    info = NIST_Smile_List()
    smiles = info[0]

    print smiles, len(smiles)
# wn, wl, T, A
# True means it's a smile, if false, add 4th parameter with Inchikey or CAS
#nu, coef = load_NIST_spectra(smiles[0], ["wn","A"], True)


def nist_spectrum(molecule_smile):

    #nu, coef = load_NIST_spectra('C=CC(C)=O', ["wn","A"], True)
    nu, coef = load_NIST_spectra(molecule_smile, ["wn","A"], True)

    return nu, coef

#    plt.plot(nu,coef)
#    plt.show()


# for wavenumber, wavelenth, transmission, absorption.
#print data.wn(), data.wl(), data.trans(), data.absorb()

# points = []
# for i in range(0, 10):
#     points.append((float(data.wn()[i]), float(data.absorb()[i])))

#print(len(data.absorb()))

#plt.plot(data.wn(), data.absorb())

#plt.show()