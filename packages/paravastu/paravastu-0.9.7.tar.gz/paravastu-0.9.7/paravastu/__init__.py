from biopandas.pdb import PandasPdb
import pandas
import numpy
import dtale
import glob
import os
import ipywidgets
from IPython.display import display
import sys
from scipy.spatial.distance import cdist, pdist
from matplotlib import rcParams
import matplotlib.pyplot as plt


def ReadPDBintoDataFrame(PDBfileNameString):
    DataFrame = pandas.DataFrame(PandasPdb().read_pdb(PDBfileNameString).df["ATOM"])
    file = open(PDBfileNameString,'r')
    text = file.readlines()
    file.close()
    DataFrame.text = text
    DataFrame.path = PDBfileNameString
    return DataFrame
def GetAtomPosition(PDBDataFrame, SegmentID, ResidueNumber, AtomName):
    DataFrame = PDBDataFrame.loc[PDBDataFrame["segment_id"]== SegmentID]
    DataFrame= DataFrame.loc[PDBDataFrame["residue_number"]==ResidueNumber]
    DataFrame = DataFrame.loc[PDBDataFrame["atom_name"]==AtomName]
    DataFrame= DataFrame[["x_coord", "y_coord","z_coord"]]
    return DataFrame.to_numpy()
def GetSegmentIDs(PDBDataFrame):
    SegmentSet = PDBDataFrame.segment_id.unique()
    return SegmentSet
def EuclideanDistance(coords1, coords2):
    return numpy.linalg.norm(coords1-coords2)

protein_letters = "ACDEFGHIKLMNPQRSTVWY"
extended_protein_letters = "ACDEFGHIKLMNPQRSTVWYBXZJUO"
protein_letters_1to3 = {
    "A": "Ala",
    "C": "Cys",
    "D": "Asp",
    "E": "Glu",
    "F": "Phe",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "K": "Lys",
    "L": "Leu",
    "M": "Met",
    "N": "Asn",
    "P": "Pro",
    "Q": "Gln",
    "R": "Arg",
    "S": "Ser",
    "T": "Thr",
    "V": "Val",
    "W": "Trp",
    "Y": "Tyr",
}
protein_letters_1to3_extended = dict(
    list(protein_letters_1to3.items())
    + list(
        {"B": "Asx", "X": "Xaa", "Z": "Glx", "J": "Xle", "U": "Sec", "O": "Pyl"}.items()
    )
)

protein_letters_3to1 = {x[1]: x[0] for x in protein_letters_1to3.items()}
protein_letters_3to1_extended = {
    x[1]: x[0] for x in protein_letters_1to3_extended.items()
}

def ConvertToOneLetter(Sequence, custom_map=None, undef_code="X"):

    if custom_map is None:
        custom_map = {"Ter": "*"}
    # reverse map of threecode
    # upper() on all keys to enable caps-insensitive input seq handling
    onecode = {k.upper(): v for k, v in protein_letters_3to1_extended.items()}
    # add the given termination codon code and custom maps
    onecode.update((k.upper(), v) for k, v in custom_map.items())
    SequenceList = [Sequence[3 * i : 3 * (i + 1)] for i in range(len(Sequence) // 3)]
    return "".join(onecode.get(aa.upper(), undef_code) for aa in SequenceList)

def ConvertToThreeLetter(Sequence, custom_map=None, undef_code="Xaa"):
    if custom_map is None:
        custom_map = {"*": "Ter"}
    # not doing .update() on IUPACData dict with custom_map dict
    # to preserve its initial state (may be imported in other modules)
    threecode = dict(
        list(protein_letters_1to3_extended.items()) + list(custom_map.items())
    )
    # We use a default of 'Xaa' for undefined letters
    # Note this will map '-' to 'Xaa' which may be undesirable!
    return "".join(threecode.get(aa, undef_code) for aa in Sequence)

def GetHydrogenBondDistances(PDBDataFrame, resstart, resstop):
    segments = GetSegmentIDs(PDBDataFrame)
    index = [i for i  in range(0, len(segments))]
    segstart = index[0]
    segstop = index[-1]
    residues2check = numpy.arange(resstart, resstop+1, 2)
    HBondDistances= numpy.zeros((segstop-segstart, len(residues2check)))
    for i in range(segstart, segstop):
        for j in residues2check:
            HN = GetAtomPosition(PDBDataFrame, segments[i+1],j+1,'HN')
            CO = GetAtomPosition(PDBDataFrame, segments[i],j,'O')
            HBondDistances[i-1, int(numpy.where(residues2check == j)[0])]=EuclideanDistance(HN, CO)
    return HBondDistances

def FindAngle(u,v):
    """
    Calculates the angle (degrees) between two vectors (as 1-d arrays) using
    dot product.
    """

    V1 = u / numpy.linalg.norm(u)
    V2 = v/ numpy.linalg.norm(v)
    return 180/numpy.pi * numpy.arccos(numpy.dot(V1,V2))

def CalculateDihedrals(prevCO,currN,currCA,currCO,nextN,cutoff=6.5):
    """
    Calculates phi and psi angles for an individual residue.
    """

    # Set CA coordinates to origin
    A = [prevCO[i] - currCA[i] for i in range(3)]
    B = [currN[i] - currCA[i] for i in range(3)]
    C = [currCO[i] - currCA[i] for i in range(3)]
    D = [nextN[i] - currCA[i] for i in range(3)]

    # Make sure the atoms are close enough
    #if max([dist_sq(x) for x in [A,B,C,D]]) > cutoff:
    #    err = "Atoms too far apart to be bonded!"
    #    raise ValueError(err)

    # Calculate necessary cross products (define vectors normal to planes)
    V1 = numpy.cross(A,B)
    V2 = numpy.cross(C,B)
    V3 = numpy.cross(C,D)

    # Determine scalar angle between normal vectors
    phi = FindAngle(V1,V2)
    if numpy.dot(A,V2) > 0: phi = -phi

    psi = FindAngle(V2,V3)
    if numpy.dot(D,V2) < 0: psi = -psi

    return phi, psi



def CalculateTorsion(PDBDataFrame):
    """
    Calculate the backbone torsion angles for a pdb file.
    """
    pdb = PDBDataFrame.text
    residue_list = []
    N = []
    CO = []
    CA = []

    resid_contents = {}
    current_residue = None
    to_take = ["N  ","CA ","C  "]
    for line in pdb:
        if line[0:4] == "ATOM" or (line[0:6] == "HETATM" and line[17:20] == "MSE"):

            if line[13:16] in to_take:

                # First residue
                if current_residue == None:
                    current_residue = line[17:26]
                    

                # If we're switching to a new residue, record the previously
                # recorded one.
                if current_residue != line[17:26]:

                    try:
                        N.append([float(resid_contents["N  "][30+8*i:38+8*i])
                                  for i in range(3)])
                        CO.append([float(resid_contents["C  "][30+8*i:38+8*i])
                                   for i in range(3)])
                        CA.append([float(resid_contents["CA "][30+8*i:38+8*i])
                                   for i in range(3)])
                        residue_list.append(current_residue)

                    except KeyError:
                        err = "Residue %s has missing atoms: skipping.\n" % current_residue
                        sys.stderr.write(err)

                    # Reset resid contents dictionary
                    current_residue = line[17:26]
                    resid_contents = {}

                # Now record N, C, and CA entries.  Take only a unique one from
                # each residue to deal with multiple conformations etc.
                if line[13:16] not in resid_contents:
                    resid_contents[line[13:16]] = line
                else:
                    err = "Warning: %s has repeated atoms!\n" % current_residue
                    sys.stderr.write(err)

    # Record the last residue
    try:
        N.append([float(resid_contents["N  "][30+8*i:38+8*i])
                  for i in range(3)])
        CO.append([float(resid_contents["C  "][30+8*i:38+8*i])
                   for i in range(3)])
        CA.append([float(resid_contents["CA "][30+8*i:38+8*i])
                   for i in range(3)])
        residue_list.append(current_residue)

    except KeyError:
        err = "Residue %s has missing atoms: skipping.\n" % current_residue
        sys.stderr.write(err)


    # Calculate phi and psi for each residue.  If the calculation fails, write
    # that to standard error and move on.
    labels = []
    dihedrals = []
    for i in range(1,len(residue_list)-1):
        try:
            dihedrals.append(CalculateDihedrals(CO[i-1],N[i],CA[i],CO[i],
                                                    N[i+1]))
            labels.append(residue_list[i])
        except ValueError:
            err = "Dihedral calculation failed for %s\n" % residue_list[i]
            sys.stderr.write(err)
    torsion_angles = pandas.DataFrame(dihedrals, columns = ["Phi", "Psi"])
    torsion_angles["resdata"] = labels
    torsion_angles["resdata"] = torsion_angles.resdata.apply(lambda x: ''.join([str(i) for i in x]))
    torsion_angles[["Residue Name", "Chain ID", "Residue Number"]] = torsion_angles.resdata.str.split(expand=True)
    torsion_angles.drop("resdata", axis = 1, inplace = True)
    torsion_angles["Residue Number"] = pandas.to_numeric(torsion_angles["Residue Number"])
    return torsion_angles


def DisplayDataFrame(DataFrame):                                                    
    DisplayFrame = dtale.show(DataFrame)
    return DisplayFrame
def GetChainIDs(PDBDataFrame):
    return PDBDataFrame.chain_id.unique()

def ListFileType(FileType, ReturnAsList = False):
    if ("*" in FileType) is False:
        FileType = "*" + FileType
    if ReturnAsList is True:
        FileList = [file for file in glob.glob(FileType)]
        return FileList
    for file in glob.glob(FileType):
        print(file)

def ListDirectory():
    files = os.listdir(os.getcwd())
    for f in files:
	    print(f)
def DoubleClickButton(FileName):
    button = ipywidgets.Button(description=FileName, tooltip='launch ' + FileName)
    display(button)

    def button_eventhandler(obj):
        os.system(FileName)
    button.on_click(button_eventhandler)
def DoubleClick(FileName):
    os.system(FileName)

def RamachandranPlot(TorsionAngleDataFrame, ResidueRange = 1, ChainIDsToExclude = [], Name = ''):
    if type(ResidueRange) is int :
        ResidueStart = ResidueRange
        ResidueStop = TorsionAngleDataFrame["Residue Number"].max()
    elif type(ResidueRange) is list and len(ResidueRange) == 1:
        ResidueStart = ResidueRange[0]
        ResidueStop = TorsionAngleDataFrame["Residue Number"].max()
    else:
        ResidueStart = ResidueRange[0]
        ResidueStop =  ResidueRange[1]
    residues = list(numpy.linspace(ResidueStart, ResidueStop, dtype=numpy.integer))
    TorsionAngleDataFrame = TorsionAngleDataFrame[TorsionAngleDataFrame["Residue Number"].isin(residues)]
    TorsionAngleDataFrame = TorsionAngleDataFrame[~TorsionAngleDataFrame["Chain ID"].isin(ChainIDsToExclude)]
    rcParams.update({'text.usetex': False, "svg.fonttype": 'none' })
    ticks = numpy.arange(-180, 181, 30)
    plt.xlim([-180, 180])
    plt.ylim([-180, 180])
    plt.xlabel('phi')
    plt.ylabel('psi')
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.grid()
    if ResidueStart == ResidueStop:
        plt.title(Name + " Torsion Angles for Residue " + str(ResidueStart))
    else:
        plt.title(Name + " Torsion Angles from Residues " + str(ResidueStart) + " to " + str(ResidueStop))
    plt.scatter(TorsionAngleDataFrame.Phi, TorsionAngleDataFrame.Psi, alpha=0.5)
def FindPotentialClashes(PDBDataFrame, Atom1Name, Atom2Name, DistanceLimit):
    PDBDataFrame["atom_name"] = PDBDataFrame.atom_name.str.slice(stop=1)
    Atom1Array = PDBDataFrame.loc[PDBDataFrame["atom_name"] == Atom1Name][["x_coord", "y_coord", "z_coord"]]
    Atom2Array = PDBDataFrame.loc[PDBDataFrame["atom_name"] == Atom2Name][["x_coord", "y_coord", "z_coord"]]
    if(Atom1Name != Atom2Name): Distances = cdist(Atom1Array, Atom2Array, metric = "euclidean") 
    elif(Atom1Name == Atom2Name): Distances = pdist(Atom1Array)
    Distances = Distances[Distances < DistanceLimit]
    Histogram = plt.hist(Distances)
    plt.xlabel(Atom1Name+  "-"+ Atom2Name +  " Distances up to " +str(DistanceLimit) + " angstroms")
    return Histogram, pandas.DataFrame(Distances)