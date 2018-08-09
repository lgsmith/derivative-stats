#!/usr/bin/env python3
from typing import List

import numpy as np
import argparse

# from sys import argv

helpstr = """
AS YET UNFINISHED. 
"""

# Takes a file name for a FEC, and the tuple of columns.
# Returns the nd array of reaction coordinate positions.
def get_rxn_coord(fec, cols):
    return np.array([fec[:,i] for i in cols])


# takes a FEC and  a column,
# returns an array of that column, the free energy
def get_free_e(fec, col):
    return fec[:, col]  # reads in the file as 1d np array, data in col


# prints the contents of an iterable next to the index of the contents.
# designed to diagnose errors in the case where script is inappropriately fed.
def puke(argvector):
    l = len(argvector)
    for i in range(l):
        print(i, argvector[i])

d_infix = "-deriv"
int_infix = "-int"
file_extension = ".asc"

# set up command line I/O
parser = argparse.ArgumentParser(description=helpstr)
parser.add_argument("fecs", nargs='+',
                    help="The free energy curves across which to compute statistics.")
parser.add_argument("--best-estimate", "-b", default=None,
                    help="The free energy curve to be used as the best estimate.\n\
                    If none then the mean is taken.")
parser.add_argument("--prefix","-p", type=str, default='dstats',
                    help="A prefix string used to name all output files.")
parser.add_argument("--bin-edges", "-e", default=None,
                    help="A file containing the window edges for computing a window integral.\n\
                    If None, then no window integral is computed.")
parser.add_argument("--cols", "-c", type=tuple, default=(0, 1),
                    help="A tuple listing the columns to use in the free energy curve file.\n\
                    Last element of the tuple should be the free energy column.")
parser.add_argument("--overwrite","-O", action="store_true", default=False,
                    help="If thrown, will overwrite output files. Complains and exits otherwise.")
parser.add_argument("--derivs", "-D", action="store_true", default=false,
                    help="Save derivatives to file using 'prefix_d'.")
parser.add_argument("--plots","-P", action="store_true", default=False)
# for testing
argv: List[str] = ['../derivative-stats.py', 'test', '46', 'example-data/GUAAUA.all/GUAAUA.all.0.dat']
argv += ['example-data/GUAAUA.' + str(i) + '/GUAAUA.ff12sb.e.pmf.0.ns.cut.dat' for i in range(1, 5)]

args = parser.parse_args(argv)

# use the list of file names to create an array of arrays representing each fec.
fecs = np.array([np.genfromtxt(fec) for fec in args.fecs])
# slice through the first two layers of the array of arrays to obtain the free energy column vectors
free_energies = fecs[:, :, args.cols[-1]]

rxn_coord = get_rxn_coord(fecs[0], args.cols)

# load the best-estimate array into best
if args.best_estimate:
    best = np.genfromtxt(args.best_estimate)[:, args.cols[-1]]

gradients = np.array((np.gradient(freeE, rxn_coord) for freeE in free_energies))

if args.derivs:
    count = 0
    for d in gradients:
        np.savetxt(args.prefix + d_infix + str(count) + file_extension, d)
        count += 1