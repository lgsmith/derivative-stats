#!/bin/bash

# Slice data filename info (filename should indicate slicing)
slicemin=0
slicemax=600
slicestep=100
slicecount=7
m=GUAAUA
prefix=$m.all.stdev-fecD
datafileprefix=$m.all/$prefix.label.
for slice in $(seq $slicemin $slicestep $slicemax); do
	../derivative-stats.py -OD -p $m.$slice -b $m.all/$m.all.e.$slice.dat \
	-e edges.txt $m.{1..4}/$m.ff12sb.e.pmf.$slice.ns.cut.dat
done

echo 'plotting data...'

# comment the following lines if you don't want this script to make plots
python3 sd-plotter.py & # this generates a plot of the SD of the force
python3 int-plotter.py & # this generates a plot of the SD of the window integral
