
import os
import sys
import numpy as np
import db_management2 as dbm
import matplotlib.pyplot as plt
import jdx_Reader as jdx



def load_NIST_spectra(molecule,return_param,is_smile=False,name="",NIST_Spectra=""):

    kwargs = {"dir":"",
              "db_name":"Molecule_DB.db",
              "user":"azariven",
              "DEBUG":False,"REMOVE":False,"BACKUP":False,"OVERWRITE":False}
    
    cross_db = dbm.database(**kwargs)   
    cross_db.access_db()   

    if is_smile:
        cmd = "SELECT Path from Spectra Where Smiles='%s'"%molecule
    else:
        if name == "CAS":
            cmd = "SELECT Path from Spectra Where CAS='%s'"%molecule
        elif name == "Inchikey":
            cmd = "SELECT Path from Spectra Where Inchikey='%s'"%molecule
        else:
            print "unknown name, simulation terminated"
            sys.exit()
        
    result = cross_db.c.execute(cmd)
    
    try:
        fetch = result.fetchall()[0][0]
    except:
        print "Molecule %s Doesn't Exist in NIST Database"%molecule
        sys.exit()
    
    filename = os.path.join(NIST_Spectra,fetch)
    #print filename
    
    data = jdx.JdxFile(filename)    
   
    
    if return_param[0] == "wl":
        x = data.wl()
    elif return_param[0] == "wn":
        x = data.wn()
        
    if return_param[1] == "T":
        y = data.trans()
    elif return_param[1] == "A":
        y = data.absorb()


    return x,y

def NIST_Smile_List(expect="All"):


    kwargs = {"db_name":"Molecule_DB.db",
              "user":"azariven",
              "dir":"",
              "DEBUG":False,"REMOVE":False,"BACKUP":False,"OVERWRITE":False}
    
    cross_db = dbm.database(**kwargs)   
    cross_db.access_db()   
    
    cmd = 'SELECT ID.SMILES, ID.InChiKey, Spectra.CAS, ID.Formula, ID.IUPAC_chemical_name FROM ID,Spectra WHERE ID.SMILES=Spectra.Smiles AND Spectra.Is_Gas="Y"'
    
    result = cross_db.c.execute(cmd)
    data = np.array(result.fetchall()).T

    smiles = data[0]
    inchikeys = data[1]
    CAS = data[2]
    formula = data[3]
    name = data[4]
    
    if expect == "All":
        return smiles, inchikeys,CAS,formula,name
    elif expect == "Smiles":
        return smiles
    elif expect == "Inchikey":
        return inchikeys
    elif expect == "CAS":
        return CAS
    else:
        print "Unknown NIST output data type, Simulation Terminated"
        sys.exit()


def plot_NIST_transmission_spectra():


    Smiles_List = NIST_Smile_List("Smiles")
    
    
    Halo_NIST_Smiles = []
    for i,info in enumerate(Smiles_List):
        if "Cl" in info or "Br" in info or "F" in info or "I" in info:
            Halo_NIST_Smiles.append(info)
            
    print len(Halo_NIST_Smiles)

    Smiles = Halo_NIST_Smiles[0]
    
    print Smiles
    
    Smiles = "CC"
    
    nu, trans = load_NIST_spectra(Smiles,["wn","T"],is_smile=True,NIST_Spectra="NIST_Spectra")
    
    
    
    plt.title("NIST transmission spectra for %s"%Smiles)
    plt.xlabel("Wavenumber")
    plt.ylabel("Transmittance")
    plt.plot(nu,trans)
    plt.show()
    
    
    


if __name__ == "__main__":
    plot_NIST_transmission_spectra()