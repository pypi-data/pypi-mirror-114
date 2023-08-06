from .relax import relax
from .common import protein
import sys

def main():
    RELAX_MAX_ITERATIONS = 0
    RELAX_ENERGY_TOLERANCE = 2.39
    RELAX_STIFFNESS = 10.0
    RELAX_EXCLUDE_RESIDUES = []
    RELAX_MAX_OUTER_ITERATIONS = 20
    pdbname=sys.argv[1]
    pdboptname=pdbname.split(".")[0]+"_opt"+".pdb"
    prot = protein.from_pdb_string(open(sys.argv[1], "r").read())
    out=relax.AmberRelaxation(
        max_iterations=RELAX_MAX_ITERATIONS,
        tolerance=RELAX_ENERGY_TOLERANCE,
        stiffness=RELAX_STIFFNESS,
        exclude_residues=RELAX_EXCLUDE_RESIDUES,
        max_outer_iterations=RELAX_MAX_OUTER_ITERATIONS
    ).process(prot=prot)
    print(out[0],file=open(pdboptname,"w"))

if __name__=="__main__":
    main()