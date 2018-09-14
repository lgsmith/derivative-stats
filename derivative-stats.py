#!/usr/bin/env python3
import numpy as np
import scipy.integrate as integrate
import argparse
from os import stat
import textwrap

description = """
This tool takes files containing free energy curves and 
computes the standard deviation of their derivatives.
It writes these to an output file with an specifiable prefix.
It can also optionally write the derivative to file, 
and can integrate over segments of the free energy curves.
The edges of the segments, except the outer boundaries
of the curve, can be provided to the script in a space delimited
text file.
"""

# note, everything else is reformatted but this is WYSIWYG.
# wrap to 70 chars to match width of other help statements.
fullhelpstr = """
This tool takes arbitrary numbers of files containing your Free Energy Curves
(FECs) and computes their derivatives numerically. It then computes the
standard deviation of the derivative at each point along the curve, writing
those values to a specified output file. It will optionally alsonumerically
re-integrate segments of the curve, then compute their standard deviation, to
associate each segment with an accumulation of variance across that segment.
The edges of these segments are user specified, though the customary use for
them would be integrating over each window from which the curve is built to
associate accumulations of variance to particular window positions along the
reaction coordinate.

This tool computes the numerical derivative as implemented in the numpy
gradient method, which is an order 2 accurate method for numerical
differentiation that uses forward/backward methods for the boundary points so
the gradient has the same number of elements as the input. It uses the scipy
implementation of Simpson's method to integrate the curve segments, if they
are provided by the user.

This tool can optionally compute the standard deviation from a best estimate
that is not the mean of the data, and can also save the raw derivatives
trace. If these behaviors are desired, inspect the flags section

SAMPLE INPUTS. The simplest possible command line might have nothing on it
other than the free energy curves you'd like to compare:

./derivative-stats.py curve-1.dat curve-2.dat curve-3.dat

If you run this command again you'll find you get an error; this is a safety
built in to prevent your overwriting files you've created previously using
this script in a blind fashion. To switch the safety off, throw the O fla:

./derivative-stats.py --overwrite curve-1.dat curve-2.dat curve-3.dat

where the curve-i.dat files are placeholders for the files containing the
FECs. To change the prefix for this file, add the --prefix flag:

./derivative-stats.py --prefix example curve-1.dat curve-2.dat curve-3.dat

If you ran this command, you should get a file called example-sd.dat because
dstats is the default prefix but you've supplied your own.
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


d_infix = "-deriv-"
int_infix = "-int"
fec_sd_infix = "-sd"
file_extension = ".asc"

# set up command line I/O
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-b", "--best-estimate", default=None,
                    help="The free energy curve to be used as the best estimate.\
                    If none then the mean is taken.")
parser.add_argument("-p", "--prefix", type=str, default='dstats',
                    help="A prefix string used to name all output files.")
parser.add_argument("-e", "--integral-edges", default=None,
                    help="A file containing the window edges for computing a window integral.\
                    If None, then no window integral is computed.")
parser.add_argument("-c", "--cols", type=int, default=(0, 1), nargs=2,
                    help="A tuple listing the columns to use in the free energy curve file.\
                    Last element of the tuple should be the free energy column.")
parser.add_argument("-O", "--overwrite", action="store_true", default=False,
                    help="If thrown, will overwrite output files. Complains and exits otherwise.")
parser.add_argument("-D", "--derivs", action="store_true", default=False,
                    help="Save derivatives to file using" + d_infix + " infix.")
parser.add_argument("fecs", nargs='*',
                    help="The free energy curves across which to compute statistics.")
parser.add_argument("--fullhelp", action="store_true", default=False,
                    help="If thrown, prints multi-paragraph description with sample command-line statements.")
args = parser.parse_args()

# for debugging
# argv = '../derivative-stats.py -O -b example-data/GUAAUA.all/GUAAUA.all.0.dat -p test/test -e example-data/edges.txt'.split()
# argv += ['example-data/GUAAUA.' + str(i) + '/GUAAUA.ff12sb.e.pmf.0.ns.cut.dat' for i in range(1, 5)]
# args = parser.parse_args(argv[1:])

# check for fullhelp, then print it
if args.fullhelp:
    print(fullhelpstr)
    exit(0)

# make sure we have some fecs to work with
if len(args.fecs) < 2:
    print("Error: Cannot compute a standard deviation for fewer than two curves.\n"
          "\tprovide at least two like-binned curve files.")
    exit(-1)

# use the list of file names to create an array of arrays representing each fec.
fecs = np.array([np.genfromtxt(fec) for fec in args.fecs])
# slice through the first two layers of the array of arrays to obtain the free energy column vectors
free_energies = fecs[:, :, args.cols[-1]]

# get reaction coordinate from first FEC in list.
# If reaction coordinates are somehow different, breaks.
# Calculating the variance across FECs that don't have
# exactly the same bins is an ill defined problem anyway.
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
    # drop the first and last edge, so np.split doesn't make zero length arrays for those
    no_boundary_edges = np.delete(edges.copy(), (0, len(edges) - 1))
    # edges must be of the same dimensionality as rxn_coord
    indexes, = np.where(np.isin(rxn_coord, no_boundary_edges))
    # use the edge indexes to split up rxn coord and fecs
    segmented_rxn_coord = np.split(rxn_coord, indexes)
    segmented_grad = np.split(gradients, indexes, axis=1)
    ints = np.array([integrate.simps(seg[0], seg[1], axis=1)
                     for seg in zip(segmented_grad, segmented_rxn_coord)])
    if args.best_estimate:
        segmented_best = np.split(best_grad, indexes)
        best_ints = np.array([integrate.simps(seg[0], seg[1])
                              for seg in zip(segmented_best, segmented_rxn_coord)])
        ints_sd = stdev_from_best(ints.T, best_ints)
    else:
        ints_sd = np.std(ints, axis=0)
    check_overwrite_save(args.prefix + int_infix + file_extension,
                         (np.delete(edges, -1), ints_sd), args.overwrite)
