#!/usr/bin/env python3

import numpy as np
from sys import argv

helpstr = """
 Script takes arbitrary numbers of 
 files containing your FECs
 and one filename to write to.
 The output file must be the first argument;
 the average/unified FEC must be the second.
 Parsed to match output from WHAM as coded up
 by Alan Grossfield from U. of Rochester.

 Computes a difference between neighboring
 points on an FEC, scaled by the distance 
 between points (a numerical derivative),
 from a FEC between each replica and 
 the FEC representing pooled/unified/average
 values. Uses these deviations to calculate
 a standard error for each difference,
 writes that standard error to a file. Note
 it will have one fewer entry than the 
 number of bins provided. 

 NOTE: ORDER IS IMPORTANT. THE OUTFILE IS 
 OVERWRITTEN IN AN INDISCRIMINATE FASHION.
 DON'T PUT A FILE IN THE OUTFILE POSITION
 IF YOU WANT TO KEEP IT.
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

# takes an array of dependent variable values, an array of corresponding independent varable values and chunk count
# returns an array containing the integrals of the chunks of the xy pairs. (even sized chunks)
def integrate_windows(x_array, y_array, window_width, bin_width):
    hwc = int(window_width/(2*bin_width))
    head_half_window = (x_array[0], np.trapz(y_array[0:hwc], x_array[0:hwc]))
    tail_half_window = (x_array[-hwc], np.trapz(y_array[-hwc:], x_array[-hwc:]))
    x_chunks = np.array_split(x_array[hwc:-hwc], window_count-1) #split array into that many equal-sized chunks
    y_chunks = np.array_split(y_array[hwc:-hwc], window_count-1)
    accum = [head_half_window]
    for i in range(window_count-1):
        accum.append((x_chunks[i][0], np.trapz(y_chunks[i], x_chunks[i])))
    accum.append(tail_half_window)
    return np.array(accum)


# prints the contents of an iterable next to the index of the contents.
# designed to diagnose errors in the case where script is inappropriately fed.
def puke(argvector):
    l = len(argvector)
    for i in range(l):
        print(i, argvector[i])


# usage string, part of help prompt.
usage = 'usage:\nstdev-int-fecD.py outfile window_count average_fec replica_1_fec replica_2_fec ...'



# do some IO scrutinizing
if len(argv) < 2:
    print(usage)
    puke(argv)
    exit(-1)

if 'help' in argv[1] or argv[1] == '-h':
    print(helpstr)
    print(usage)
    exit(0)

if len(argv) < 5:
    print(usage)
    puke(argv)
    exit(-1)

# IO stuff
# read in the average or unified FEC to calculate deviations from
window_count = int(argv[2])
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
