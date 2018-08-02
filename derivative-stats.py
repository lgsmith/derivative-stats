#!/usr/bin/env python3

import numpy as np
from sys import argv

helpstr = """
This script takes arbitrary numbers of files containing your Free Energy
Curves (FECs) a file prefix to write output files to and a window count (to
obtain the number of windows). The output file must be the first argument;
the average/unified FEC must be the second. The leading bin edge is expected
to be in the first column and the free energy of that bin is expected to be
the second. None of the other columns, if there are any, are used.

This script computes a difference between neighboring points on an FEC,
scaled by the distance between points (a numerical derivative), from a FEC
between each replica and the FEC representing pooled/unified/average values.
The distance between points (bin width) is assumed to be constant. It uses
these deviations to calculate a standard deviation for each difference,
writes that standard error to a file. Note it will have one fewer entry than
the number of bins provided.

It also calculates a collection of integrals (using the trapezoid method)
over the windows used to produce the reaction coordinate, then computes their
standard deviation. This is an approximate way of associating variability to
a particular window. Because the integrals are over segments of the
derivative they are in free energy units. This script assumes your windows
are evenly spaced along the reaction coordinate, computing where their
'edges' are by subtracting the first bin from the last bin to determine the
length of the reaction coordinate, then dividing by the window count. It also
assumes that you've dropped half a window at each end of the reaction
coordinate to avoid edge effects. Future schemes will allow user
specification of 'bin edges' for this purpose.

NOTE: ORDER IS IMPORTANT. THE OUTFILE IS OVERWRITTEN IN AN INDISCRIMINATE
FASHION. DON'T PUT A FILE IN THE OUTFILE POSITION IF YOU WANT TO KEEP IT.
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


# takes a bins array, a bin values array, a bin width and a window width and chunk count
# returns an array containing the integrals of the chunks of the xy pairs. (even sized chunks)
def integrate_windows(x_array, y_array, window_width, bin_width):
    hwc = int(window_width/(2*bin_width))
    head_half_window = (x_array[0], np.trapz(y_array[0:hwc], x_array[0:hwc]))
    tail_half_window = (x_array[-hwc], np.trapz(y_array[-hwc:], x_array[-hwc:]))
    # split array into that many equal-sized chunks
    x_chunks = np.array_split(x_array[hwc:-hwc], window_count-1)
    y_chunks = np.array_split(y_array[hwc:-hwc], window_count-1)
    accum = [head_half_window]
    for i in range(window_count-1):
        accum.append((x_chunks[i][0], np.trapz(y_chunks[i], x_chunks[i])))
    accum.append(tail_half_window)
    return np.array(accum)


# prints the contents of an iterable next to the index of the contents.
# designed to diagnose errors in the case where script is inappropriately fed.
def puke(argvector, argcount):
    for i in range(argc):
        print(i, argvector[i])


# usage string, part of help prompt.
usage = 'usage:\nderivative-stats.py outfile_prefix window_count average_fec replica_1_fec replica_2_fec ...'

#argv = ['../derivative-stats.py','test','46', 'example-data/GUAAUA.all/GUAAUA.all.0.dat']
#argv += ['example-data/GUAAUA.'+str(i)+'/GUAAUA.ff12sb.e.pmf.0.ns.cut.dat' for i in range(1,5)]
argc = len(argv)
# do some IO scrutinizing
if argc < 2:
    print(usage)
    puke(argv, argc)
    exit(-1)

if 'help' in argv[1] or argv[1] == '-h':
    print(helpstr)
    print(usage)
    exit(0)

if argc < 5:
    print(usage)
    puke(argv, argc)
    exit(-1)

# IO stuff
# read in the average or unified FEC to calculate deviations from
window_count = int(argv[2])
unified = np.genfromtxt(argv[3])

# assuming bin distances are in first column:
bin_width = unified[1][0] - unified[0][0]
unified_inds = unified[:,0]
# assumes half a window is dropped on each end of the reaction coordinate to eliminate edge effects
window_width = (unified_inds[-1] - unified_inds[0]) / (window_count - 1)

# make a numerical deriv array out of bin free E array
unified_fec_d = arr_num_deriv(unified[:,1], bin_width)

# Bin distance from alan's wham code; will result in errors if indices
# in merged file are not the same as those from other files
# (but I think that'd be a problem for many reasons)
length_raw = len(unified)

# compute the SAMPLE (ddof=1) standard deviation per bin of the free energy curve
fecD_arr = np.array([fec_to_d(fec,1,bin_width) for fec in argv[4:]])
centered_fecDs = fecD_arr - unified_fec_d
sample_count = len(fecD_arr)
# loop over fecD_arr and accumulate un-normalized variance. normalize and get standard dev at end
variance = np.zeros_like(unified_fec_d)
for centered_fecD in centered_fecDs:
    variance += centered_fecD**2
stdev = np.sqrt(variance/(sample_count-1))

# Define index used for the FEC derivative variance
# needed for plotting. End indices are removed, because
# no value is defined there, The indices are moved over
# half a bin width to indicate the quantity is defined between bins.
index = np.delete(unified_inds + np.repeat(bin_width/2.0, length_raw), length_raw - 1)

# compute the integrals of the derivatives
x_edges = np.delete(unified_inds, length_raw - 1)
window_integrals = np.array([integrate_windows(x_edges, fecD, window_width, bin_width) for fecD in fecD_arr])
# 'center' window integrals on the unified best estimate
unified_integrals = integrate_windows(x_edges, unified_fec_d, window_width, bin_width)[:,1]

integral_edges = np.around(window_integrals[0][:,0], decimals=1)
# compute the sample standard deviation of the integrals
integral_variance = np.zeros_like(window_integrals[0][:,1])
for window_integral in window_integrals:
    integral_variance += window_integral[:,1]**2
window_integral_SD = np.sqrt(integral_variance/(sample_count - 1))

# write the data to a file as ascii matrix for plotting
np.savetxt(argv[1] + '.dat', np.column_stack((index,stdev)), delimiter='\t' )
# np.savetxt(argv[1] + '_derivs.dat', fecD_arr, delimiter='\t')
np.savetxt(argv[1] + '_derivs.dat', np.column_stack((index, fecD_arr.T)), delimiter='\t')
np.savetxt(argv[1] + '_ints.dat', np.column_stack((integral_edges, window_integral_SD)), delimiter='\t')
