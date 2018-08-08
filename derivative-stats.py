#!/usr/bin/env python3

import numpy as np
import argparse
# from sys import argv

helpstr = """
AS YET UNFINISHED. 
"""

# takes trajectory name (from cmd line) and a column, returns numpy array for that column
def fec_to_arr(name, col):
    column_vec = np.genfromtxt(name)[:,col] # reads in the file as 1d np array, data in col
    return column_vec

# takes a numpy array, returns a numpy array that contains
# the differences between neighboring elts in the array
def arr_num_deriv(fec_arr, bin_width):
    # copy of input arr with first elt duplicated and last elt deleted.
    trans_arr = np.delete(np.insert(fec_arr, 0, fec_arr[0]), len(fec_arr))
    # return difference in array and shifted array, with the 0 element deleted (it is zero by construction)
    return np.delete(fec_arr - trans_arr, 0)/bin_width

# composition of the above two functions, takes a fec name and a column, returns array array of diferences
def fec_to_d(name, col, width):
    return arr_num_deriv(fec_to_arr(name, col), width)


# prints the contents of an iterable next to the index of the contents.
# designed to diagnose errors in the case where script is inappropriately fed.
def puke(argvector):
    l = len(argvector)
    for i in range(l):
        print(i, argvector[i])
# set up command line I/O
parser = argparse.ArgumentParser(description=helpstr)
parser.add_argument("fecs", nargs='+',
                    help="The free energy curves across which to compute statistics.")
parser.add_argument("--best-estimate","-b", default=None,
                    help="The free energy curve to be used as the best estimate.\n\
                    If none then the mean is taken.")
parser.add_argument("--bin-edges","-e", default=None,
                    help="A file containing the window edges for computing a window integral.\
                    \nIf None, then no window integral is computed.")
parser.add_argument("--cols","-c", type=tuple, default=(0,1),
                    help="A tuple listing the columns in the free energy file.\
                    \nLast element of the tuple should be the free energy column.\n\
                    Preceeding columns indicated should contain the reaction coordinates.")

# usage string, part of help prompt.
usage = 'usage:\nderivative-stats.py outfile window_count average_fec replica_1_fec replica_2_fec ...'


argv = ['../derivative-stats.py','test','46', 'example-data/GUAAUA.all/GUAAUA.all.0.dat']
argv += ['example-data/GUAAUA.'+str(i)+'/GUAAUA.ff12sb.e.pmf.0.ns.cut.dat' for i in range(1,5)]


if window_edges:


unified = np.genfromtxt(argv[3])

# assuming bin distances are in first column:
bin_width = unified[1][0] - unified[0][0]
unified_inds = unified[:,0]
window_width = (unified_inds[-1] - unified_inds[0]) / (window_count - 1)

# make a numerical deriv array out of bin free E array
unified_fec_d = arr_num_deriv(unified[:,1], bin_width)

# Bin distance from alan's wham code; will result in errors if indices
# in merged file are not the same as those from other files
# (but I think that'd be a problem for many reasons)
length_raw = len(unified)


# compute the SAMPLE (ddof=1) standard deviation per bin of the free energy curve
fecD_arr = np.array([fec_to_d(fec,1,bin_width) for fec in argv[4:]]) - unified_fec_d
sample_count = len(fecD_arr)
stdev = np.std(fecD_arr,axis=0,ddof=1)

# Define index used for the FEC derivative variance
# needed for plotting. End indices are removed, because
# no value is defined there, The indices are moved over
# half a bin width to indicate the quantity is defined between bins.
index = np.delete(unified_inds + np.repeat(bin_width/2.0, length_raw), length_raw - 1)

# compute the integrals of the derivatives
window_integrals = np.array([integrate_windows(np.delete(unified_inds, length_raw - 1), fecD, window_width, bin_width) for fecD in fecD_arr])

integral_edges = np.around(window_integrals[0][:,0], decimals=0)
print(integral_edges)
# compute the sample standard deviation of the integrals
window_integral_SD = np.std(window_integrals, axis=0,ddof=1)

# write the data to a file as ascii matrix for plotting
np.savetxt(argv[1] + '.dat', np.column_stack((index,stdev)), delimiter='\t' )
np.savetxt(argv[1] + '_ints.dat', np.column_stack((integral_edges,window_integral_SD[:,1])), delimiter='\t')
