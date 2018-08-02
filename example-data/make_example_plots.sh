#!/usr/bin/env bash

font=Palatino
fwfontsize=12

# Slice data filename info (filename should indicate slicing)
slicemin=0
slicemax=500
slicestep=100
m=GUAAUA
for slice in $(seq $slicemin $slicestep $slicemax); do
	../derivative-stats.py $m.all/$m.sem-fecD.$slice 46 \
	$m.all/$m.all.$slice.dat $m.{1..4}/$m.ff12sb.e.pmf.$slice.ns.cut.dat
done

#cat > $m.dslices.ints.example.gp <<-EOF
#    set output '$m-dslices-ints-all.pdf'
#    set term pdf enhanced font 'Palatino, 12'
#    set encoding iso_8859_1
#    set title '$m F.E.C. derivative standard deviation sliced from end'
#    set xlabel 'Distance ({\305})'
#    set ylabel 'Force, kcal/(mol{\305})'
#    set y2label 'Energy per Window, kcal/mol'
#    set y2tics
#    set ytics nomirror
#    set style fill transparent solid noborder
#    set boxwidth 1 relative
#    set style data histogram
#    set style histogram rowstacked
#    set key right width 1
#    set xrange [15:60]
#    # color scheme
#    # load '~/gnuplot-palettes/viridis.pal'
#    p for [i = $slicemin:$slicemax:$slicestep] 'GUAAUA.all/GUAAUA.all.e.'.($slicemax-i).'_ints.dat' \
#    u (\$1+0.5):2 w boxes axes x1y2 lt (6-i/100) t 'excluding '.($slicemax - i).' ns', \
#    'GUAAUA.all/GUAAUA.all.e.$slicemin.dat' u  1:2 w l lw 0.5 lc 'black' axes x1y1 t 'Derivative SD'
#EOF
#
#gnuplot $m.dslices.ints.example.gp
#
#cat > dslices.example.gp <<-EOF
#	set output 'all-dslices-pub.pdf'
#	set term pdf enhanced size 5.3 in, 1.5 in font '$font, $fwfontsize'
#	set notitle
#	set encoding iso_8859_1
#	set xlabel 'Distance ({\305})'
#	set ylabel "{/Symbol s}(Force)\n(kcal{\327}mol^{-1}{\305}^{-1})"
#	set key right width 1
#	set yrange [0:0.6]
#	set xrange [15:60]
#	# color scheme
#	# load '~/gnuplot-palettes/viridis.pal'
#	p '$m.all/$m.sem-fecD.e.$slicemin.dat' u  1:2 w l lw 1 t '$m'
#EOF
#
#gnuplot dslices.example.gp