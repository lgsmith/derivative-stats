#!/usr/bin/env bash

font=Palatino
fwfontsize=12

# Slice data filename info (filename should indicate slicing)
slicemin=0
slicemax=600
slicestep=100
slicecount=7
m=GUAAUA
prefix=$m.all.stdev-fecD
datafileprefix=$m.all/$prefix.label.
for slice in $(seq $slicemin $slicestep $slicemax); do
	../derivative-stats.py $m.all/$prefix.$slice 46 \
	$m.all/$m.all.$slice.dat $m.{1..4}/$m.ff12sb.e.pmf.$slice.ns.cut.dat
	./colstacker.py $m.all/$prefix.${slice}_ints.dat $datafileprefix${slice}_ints.dat $slice
	./colstacker.py $m.all/$prefix.$slice.dat $datafileprefix$slice.dat $slice
done


cat > dslices.example.gp <<-EOF
	set output 'dslices-example.pdf'
	set term pdf enhanced size 5.3 in, 1.5 in font '$font, $fwfontsize'
	set notitle
	set encoding iso_8859_1
	set xlabel 'Distance ({\305})'
	set ylabel "{/Symbol s}(Force)\n(kcal{\327}mol^{-1}{\305}^{-1})"
	set key right width 1
	set yrange [0:0.6]
	set xrange [15:60]
	# color scheme
	load 'viridis.pal'
	unset key
	set palette maxcolors $slicecount
	set cbrange [$slicemin:$slicemax]
	set cblabel 'ns omitted'
	p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix'.i.'.dat' u  (\$1):2:3 w l lw 2 lc palette 
EOF
gnuplot dslices.example.gp

cat > dslices.ints.example.gp <<-EOF
	set output 'dslices-ints-example.pdf'
	set term pdf enhanced size 6.0 in, 1.5 in font '$font, $fwfontsize'
	set encoding iso_8859_1
	set notitle
	set xlabel 'Distance ({\305})'
	set ylabel "{/Symbol s}(window)\n(kcal/mol)"
	set style fill transparent solid noborder
	set boxwidth 1 relative
	set style data histogram 
	set style histogram rowstacked
	set xrange [15:60]
	set yrange [0:0.6]
	unset key
	# color scheme
	load 'viridis.pal'
	set palette maxcolors $slicecount
	set cbrange [$slicemin:$slicemax]
	set cblabel 'ns omitted'
	p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix'.($slicemax-i).'_ints.dat' u (\$1):2:3 w boxes lc palette
EOF
gnuplot dslices.ints.example.gp