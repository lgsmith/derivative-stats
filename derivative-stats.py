#!/usr/bin/env python3
from typing import List

import numpy as np
import scipy.integrate as integrate
import argparse
from os import stat

helpstr = """
AS YET UNFINISHED. 
"""

# Takes a file name for a FEC, and the tuple of columns.
# Returns the nd array of reaction coordinate positions.
def get_rxn_coord(fec, cols):
    # prevents returning double-nested single column for 1D fecs.
    rxn_coord_cols = cols[:-1]
    if len(rxn_coord_cols) == 1:
        retval = fec[:, rxn_coord_cols[0]]
    else:
        retval = np.array([fec[:, i] for i in rxn_coord_cols])
    return retval


# takes a FEC and  a column,
# returns an array of that column, the free energy
def get_free_e(fec, col):
    return fec[:, col]  # reads in the file as 1d np array, data in col


# take standard deviation of sets of arrays using 'best' as the mean
# returns arrays of point-by variances.
def stdev_from_best(arrays, best_est):
    a_squared = np.zeros_like(best_est)
    count = 0
    for a in arrays:
        a_squared += np.square(a - best_est)
        count += 1
    return np.sqrt(a_squared / count)


# Takes a tuple of arrays, rearranges them so that each array will become a column
# returns the nd array of columns.
def v_to_col(tuple_of_arrays):
    return np.vstack(tuple_of_arrays).T


# Takes a string file name, an array to use with savetxt, and the overwrite boolean
# saves the array to the file of name fname if the file is of size zero or
# if there is no such file saves the array regardless of the status of
# the file if overwrite is True.
# Doesn't return anything.
def check_overwrite_save(fname, data_tuple, overwrite_bool):
    if overwrite_bool:
        np.savetxt(fname, v_to_col(data_tuple))
    else:
        try:
            if stat(fname).st_size == 0:
                np.savetxt(fname, v_to_col(data_tuple))
        except FileNotFoundError:
            np.savetxt(fname, v_to_col(data_tuple))
        else:
            print("You tried to overwrite a non-empty file but are not in overwrite mode.\n\
            Check your file naming scheme or throw the -O flag. Data not written for file:\n" + fname)


# fecfilen is the name of the file containing the FEC. cols is the tuple of columns to use
# based on the expected input the last element in cols should be the index of the column with the freeE
def stack_fec(fecfilen, cols):
    ncols = len(cols)
    fec = np.genfromtxt(fecfilen)[:,cols]
    free_e = fec[:, -1]  # shallow copy, last col is free E col
    unique_cols = []
    rxn_coord_len = []
    for c in range(ncols - 1):  # all but last col, which is free E col
        u, index = np.unique(fec[:, c], return_index=True)
        unique_cols.append(u[np.argsort(index)])
        rxn_coord_len.append(len(u))
    stacked_fec = np.zeros_like(free_e).reshape(rxn_coord_len)
    tracked_index = np.zeros(ncols - 1, dtype=int)
    prevrow = fec[0].copy()  # Deep copy
    for row in fec:
        index = tuple(tracked_index)
        stacked_fec[index] = row[-1]
        ix_changed = np.argwhere(np.isin(row[:-1], prevrow[:-1]))
        tracked_index[ix_changed] += 1
        prevrow = row.copy()
    return stacked_fec, tuple(unique_cols)  # tuple for indexing gradient


# needed because np.grad doesn't allow you to pass an n-element list or array, where each element is ith rxn coordinate
n_gradient_fxns = [lambda f, x: np.gradient(f, x),
               lambda f, x: np.gradient(f, x[0], x[1]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]),
               lambda f, x: np.gradient(f, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12])
               ]

d_infix = "-deriv-"
int_infix = "-int"
fec_sd_infix = "-sd"
file_extension = ".asc"

# set up command line I/O
parser = argparse.ArgumentParser(description=helpstr)
parser.add_argument("-b", "--best-estimate", default=None,
                    help="The free energy curve to be used as the best estimate.\n\
                    If none then the mean is taken.")
parser.add_argument("-p", "--prefix", type=str, default='dstats',
                    help="A prefix string used to name all output files.")
parser.add_argument( "-e", "--integral-edges", default=None,
                    help="A file containing the window edges for computing a window integral.\n\
                    If None, then no window integral is computed.")
parser.add_argument("-c", "--cols", type=tuple, default=(0, 1),
                    help="A tuple listing the columns to use in the free energy curve file.\n\
                    Last element of the tuple should be the free energy column.")
parser.add_argument("-O", "--overwrite", action="store_true", default=False,
                    help="If thrown, will overwrite output files. Complains and exits otherwise.")
parser.add_argument("-D", "--derivs", action="store_true", default=False,
                    help="Save derivatives to file using"+d_infix+" infix.")
parser.add_argument("fecs", nargs='+',
                    help="The free energy curves across which to compute statistics.")

# for debugging
argv = '../derivative-stats.py -O -b example-data/GUAAUA.all/GUAAUA.all.0.dat -p test/test -e example-data/edges.txt'.split()
argv += ['example-data/GUAAUA.' + str(i) + '/GUAAUA.ff12sb.e.pmf.0.ns.cut.dat' for i in range(1, 5)]
args = parser.parse_args(argv[1:])

# use the list of file names to create an array of arrays representing each fec.
fecs = np.array([np.genfromtxt(fec) for fec in args.fecs])
# slice through the first two layers of the array of arrays to obtain the free energy column vectors
free_energies = fecs[:, :, args.cols[-1]]

# define the discretized reaction coordinate as the domain of our free energy surfaces
rxn_coord = get_rxn_coord(fecs[0], args.cols)
# compute the gradient with respect to the reaction coordinate for each free energy curve
gradients = np.array([np.gradient(freeE, rxn_coord) for freeE in free_energies])

# load the best-estimate array into best
if args.best_estimate:
    best = np.genfromtxt(args.best_estimate)[:, args.cols[-1]]
    best_grad = np.gradient(best, rxn_coord)
    fec_sd = stdev_from_best(gradients, best_grad)
else:
    fec_sd = np.std(gradients, axis=0)
# merge the rxn coordinate array and the fec_sd array, then save them to file
check_overwrite_save(args.prefix + fec_sd_infix + file_extension,
                     (rxn_coord, fec_sd), args.overwrite)

if args.derivs:
    count = 0
    for d in gradients:
        check_overwrite_save(args.prefix + d_infix + str(count) + file_extension,
                             (rxn_coord, d), args.overwrite)
        count += 1

# if integral edges were provided, take integrals over the segments then compute variance.
if args.integral_edges:
    edges = np.genfromtxt(args.integral_edges)
    # edges must be of the same dimensionality as rxn_coord
    indexes, = np.where(np.isin(rxn_coord, edges))
    # use the edge indexes to split up rxn coord and fecs
    segmented_rxn_coord = np.split(rxn_coord, indexes)
    segmented_grad = np.split(gradients, indexes, axis=1)
    ints = np.array([integrate.simps(seg[0], seg[1], axis=1) for seg in zip(segmented_grad, segmented_rxn_coord)])
    if args.best_estimate:
        segmented_best = np.split(best_grad, indexes)
        best_ints = np.array([integrate.simps(seg[0], seg[1]) for seg in zip(segmented_best, segmented_rxn_coord)])
        ints_sd = stdev_from_best(ints, best_ints)
    else:
        ints_sd = np.std(ints, axis=0)
    check_overwrite_save(args.prefix + int_infix + file_extension, (segmented_rxn_coord, ints_sd), args.overwrite)

