#!/bin/bash


# define an AA that translates system names into loop names
declare -A molnames
molnames=([GUAAUA]=GUAAUA [1hs3]=UUAAUU [1aqo_mut]=CAGUGC)
# Slice data filename info (filename should indicate slicing)
slicemin=0
slicemax=500
slicestep=100

# CHANGE THIS BEFORE ANYTHING
workdir=/media/louis/storage_1/hairpin_unwind/analysis
figsdir=/home/louis/Dropbox/louis.smith88/writing/hppull/figures
cd $workdir

for m in GUAAUA 1hs3 1aqo_mut; do 
	datafileprefix=$workdir/$m.all/$m.sem-fecD.
	# uncomment the following if recalculating the datafiles. Otherwise proceed to plots.
	# for slice in $(seq $slicemin $slicestep $slicemax); do
	#	./stdev-int-fecD.py $m.all/$m.sem-fecD.$slice 46 $m.all/$m.all.$slice.dat $m.{1..4}/$m.ff12sb.b.pmf.$slice.ns.cut.dat
	# done
	# Go into the pooled fec data directory
	cd $m.all
	# filetitle=$m-dslices-all.pdf
	# cat > $m.dslices.gp <<-EOF
	# 	set output '$filetitle'
	# 	set term pdf enhanced font 'Palatino, 14'
	# 	set encoding iso_8859_1
	# 	set title '${molnames[$m]} F.E.C. derivative standard deviation sliced from beginning'
	# 	set xlabel 'Distance ({\305})'
	# 	set ylabel 'Force, kcal/(mol{\305})'
	# 	set key right width 1
	# 	set xrange [15:60]
	# 	# color scheme
	# 	load '~/gnuplot-palettes/viridis.pal'
	# 	p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix'.i.'.dat' \
	# 	u 1:2 w l lw 1 t 'excluding '.i.' ns'
	# EOF
	# gnuplot $m.dslices.gp
	# cp $filetitle $figsdir
	filetitle=$m-dslices-ints-all.pdf
	cat > $m.dslices.ints.gp <<-EOF
		set output '$filetitle'
		set term pdf enhanced font 'Palatino, 12'
		set encoding iso_8859_1
		set title '${molnames[$m]} F.E.C. derivative standard deviation sliced from beginning'
		set xlabel 'Distance ({\305})'
		set ylabel 'Force, kcal/(mol{\305})'
		set y2label 'Energy per Window, kcal/mol'
		set y2tics
		set ytics nomirror
		set style fill transparent solid noborder
		set boxwidth 1 relative
		set style data histogram 
		set style histogram rowstacked
		set key right width 1
		set xrange [15:60]
		# color scheme
		load '~/gnuplot-palettes/viridis.pal'
		p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix'.($slicemax-i).'_ints.dat' \
		u (\$1+0.5):2 w boxes axes x1y2 lt (6-i/100) t 'excluding '.($slicemax - i).' ns', \
		'$datafileprefix$slicemin.dat' u  1:2 w l lw 0.5 lc 'black' axes x1y1 t 'Derivative SD'
		  
	EOF
	gnuplot $m.dslices.ints.gp
	cp $filetitle $figsdir
	filetitle=$m-dslices-ints-pub.pdf
	cat > $m.dslices.ints.pub.gp <<-EOF
		set output '$filetitle'
		set term pdf size 6.0 in, 1.5 in enhanced font 'Palatino, 12'
		set encoding iso_8859_1
		set notitle
		set xlabel 'Distance ({\305})'
		set ylabel 'Energy per Window, kcal/mol'
		set style fill transparent solid noborder
		set boxwidth 1 relative
		set style data histogram 
		set style histogram rowstacked
		set key right width 1
		set xrange [15:60]
		set yrange [0:0.6]
		# color scheme
		load '~/gnuplot-palettes/viridis.pal'
		p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix'.($slicemax-i).'_ints.dat' \
		u (\$1+0.5):2 w boxes lt (6-i/100) t 'excluding '.($slicemax - i).' ns'
	EOF
	gnuplot $m.dslices.ints.pub.gp
	cp $filetitle $figsdir
	cd $workdir
done

cat > all.dslices.pub.gp <<-EOF
	set output 'all-dslices-pub.pdf'
	set term pdf size 6. in, 1.5 in enhanced font 'Palatino, 12'
	set encoding iso_8859_1
	set notitle
	set xlabel 'Distance ({\305})'
	set ylabel 'Force, kcal/(mol{\305})'
	set key right width 1
	set yrange [0:0.6]
	set xrange [15:60]
	# color scheme
	load '~/gnuplot-palettes/viridis.pal'
	p '$workdir/1aqo_mut.all/1aqo_mut.sem-fecD.$slicemin.dat' u  1:2 w l lw 1 t 'CAGUGC', \
	  '$workdir/GUAAUA.all/GUAAUA.sem-fecD.$slicemin.dat' u  1:2 w l lw 1 t 'GUAAUA', \
	  '$workdir/1hs3.all/1hs3.sem-fecD.$slicemin.dat' u 1:2 w l lw 1 t 'UUAAUU'
EOF

gnuplot all.dslices.pub.gp
cp all-dslices-pub.pdf $figsdir