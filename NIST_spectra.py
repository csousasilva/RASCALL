
import os
import sys

#DIR = os.path.abspath(os.path.dirname(__file__))
#sys.path.insert(0, os.path.join(DIR, '../../../SEAS/BioSig_SEAS/'))

#import SEAS_Utils.common_utils.db_management2 as dbm
#from SEAS_Main.atmosphere_effects.biosig_molecule import load_NIST_spectra

import db_management2 as dbm
from plot_NIST_transmission_spectra import load_NIST_spectra


import jdx_Reader as jdx
from ATMOS_Plotter import plt
import numpy as np


def NIST_Smile_List(expect="all"):
    kwargs = {"db_name": "Molecule_DB.db",
              "user": "azariven",
              "dir": "",
              "DEBUG": False, "REMOVE": False, "BACKUP": False, "OVERWRITE": False}
    "../../../BiosigSeas2/BioSig_SEAS-master/input/molecule_info"
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

    NIST_data = NIST_Smile_List()
    NIST_Smiles = NIST_data[0]
    CAS = NIST_data[2]

    #Smiles = "CCCCC"

    if molecule_smile == "CSC":
        cas = "C75183"
    else:
        cas = CAS[list(NIST_Smiles).index(molecule_smile)]


    nu, absorb = np.load("NIST_Spectra_Smile_Calibrated/%s.npy" % cas)

    return nu, absorb

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



#from scipy import sparse
#import scipy.sparse.linalg.spsolve as spsolve
"""
def baseline_als(y, lam, p, niter=10):
    L = len(y)
    D = sparse.csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in xrange(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z
"""
def check_NIST_db():
    
    
    Smiles = "OC(=O)C(Cl)"
    Absorption_Boost = 3
    
    nu1, absorb1 = load_NIST_spectra(Smiles,["wn","A"],is_smile=True,NIST_Spectra="NIST_Spectra")
    
    abfix = []
    for i in absorb1:
        if i >2:
            abfix.append(2)
        else:
            abfix.append(i)
    absorb1 = np.array(abfix)    
    absorb_baseline = 0.001#baseline_als(absorb1, 10**6, 0.001, niter=10)
    absorb2 = absorb1-absorb_baseline
    absorb2_calibrated = absorb2/max(absorb2)*Absorption_Boost

    plt.plot(nu1,absorb1)
    plt.plot(nu1,absorb2_calibrated)
    plt.show()
    

if __name__ == "__main__":
    check_NIST_db()

