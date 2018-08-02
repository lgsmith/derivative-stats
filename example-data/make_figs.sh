
#!/bin/bash

# NOTE in the event that we have to abandon cairolatex,
# the angstrom symbol can be made in gnuplot by delcaring
# set encoding iso_8859_1
# and then using {\305} as a stand in for the angstrom symbol

# define an AA that translates system names into loop names
declare -A molnames
molnames=([GUAAUA]=GUAAUA [1hs3]=UUAAUU [1aqo_mut]=CAGUGC)
# Slice data filename info (filename should indicate slicing)
slicemin=0
slicemax=600
slicestep=100
slicecount=$(((slicemax-slicemin)/slicestep + 1)) # evals to int; shell has no decimals
bore=e

# font size, half width figures
fontsize=20
# font size, full width figures
fwfontsize=12
# font type
font=Palatino

# CHANGE THIS BEFORE ANYTHING
workdir=/media/louis/storage_1/hairpin_unwind/analysis
figsdir=/home/louis/Dropbox/louis.smith88/writing/hppull/figures
rmsdir=$workdir/p_rmsds
hbsdir=$workdir/hbonds
cd $workdir

for m in GUAAUA 1hs3 1aqo_mut; do
	cd $m.all
	# filetitle=$m-dslices-ints-pub.pdf
	# datafileprefix=$workdir/$m.all/$m.fecDSD.$bore.
	# cat > $m.dslices.ints.pub.gp <<-EOF
	# 	set output '$filetitle'
	# 	set term pdf enhanced size 6.0 in, 1.5 in font '$font, $fwfontsize'
	# 	set encoding iso_8859_1
	# 	set notitle
	# 	set xlabel 'Distance ({\305})'
	# 	set ylabel "{/Symbol s}(window)\n(kcal/mol)"
	# 	set style fill transparent solid noborder
	# 	set boxwidth 1 relative
	# 	set style data histogram 
	# 	set style histogram rowstacked
	# 	set xrange [15:60]
	# 	set yrange [0:0.6]
	# 	unset key
	# 	# color scheme
	# 	load '~/gnuplot-palettes/viridis.pal'
	# 	set palette maxcolors $slicecount
	# 	set cbrange [$slicemin:$slicemax]
	# 	set cblabel 'ns omitted'
	# 	p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix'.($slicemax-i).'_ints.dat' \
	# 	u (\$1):2:3 w boxes lc palette
	# EOF
	# gnuplot $m.dslices.ints.pub.gp
	# cp $filetitle $figsdir
	filetitle=$m-slices-all-pub.pdf
	datafileprefix=$workdir/$m.all/$m.all.$bore
	ymax=18
	cat > $m.slices.pub.gp <<-EOF
		set output '$filetitle'
		set term pdf enhanced font '$font, $fontsize'
		set notitle
		set encoding iso_8859_1
		set xlabel 'Distance ({\305})' 
		set ylabel 'Free Energy (kcal/mol)'
		set key horizontal top width -1
		set key samplen 1.5
		set yrange [0:$ymax]
		# color scheme
		load '~/gnuplot-palettes/viridis.pal'
		p for [i = $slicemin:$slicemax:$slicestep] '$datafileprefix.'.i.'.dat' \
		u 1:2 w l lw 2 t ''.i.' ns'
		EOF
	gnuplot $m.slices.pub.gp
	cp $filetitle $figsdir
	# Go back to the top level to do the full length TR overlays
	cd $workdir
	filetitle=$m-troverlay-pub.pdf
	datafileprefix=$workdir/$m.
	datafilesuffix=$m.ff12sb.$bore.pmf.0.ns.cut.dat
	cat > $m.troverlay.pub.gp <<-EOF
		set output '$filetitle'
		set term pdf enhanced font '$font, $fontsize'
		set notitle
		set encoding iso_8859_1
		set xlabel 'Distance ({\305})'
		set ylabel 'Free Energy (kcal/mol)'
		set key horizontal top 
		set key samplen 2 width -1
		set yrange [0:$ymax]
		# color scheme
		load '~/gnuplot-palettes/viridis.pal'
		p for [i = 1:4] '$datafileprefix'.i.'/$datafilesuffix' \
		u 1:2 w l lw 2 t 'Replica '.i , \
		'$m.all/$m.all.$bore.0.dat' u 1:2 w l lw 2 lt rgb 'black' t 'Pooled'
		EOF
	gnuplot $m.troverlay.pub.gp
	cp $filetitle $figsdir
	filetitle=$m-rmsoverlap-pub.pdf
	cat > $m.rmsd-overlap.gp <<-EOF
		set output '$filetitle'
		set term pdf enhanced font '$font, $fontsize'
		set encoding iso_8859_1
		set notitle
		set ytics nomirror
		set y2tics
		set xlabel 'Distance, ({\305})'
		set ylabel 'F(w,w+1)'
		set y2label 'R(w,w+1)'
		set yrange [0:0.3]
		set y2range [0:1]
		set datafile missing 'NaN'
		set style fill solid noborder
		set key width 1 above
		# color scheme
		load '~/gnuplot-palettes/viridis.pal'
		p '$rmsdir/stats.$m.plot.out' u (\$1-0.5):3 w p pointtype 7 axes x1y1 t 'neighbors', \
		  '' u (\$1-0.5):4 w p pointtype 7 axes x1y2 t 'neighbors, relative'
	EOF
	gnuplot $m.rmsd-overlap.gp
	cp $filetitle $figsdir
done

# dG slicetrend figure
cat > dG-slicetrend.gp <<-EOF
	set term pdf enhanced font '$font, $fontsize' 
	set out 'dG-slicetrend.pdf'
	unset key
	set notitle 
	set yrange [5:13]
	set xlabel 'ns omitted from the beginning'
	set ylabel '{/Symbol D}G{/Symbol \260}_{stretch} (kcal/mol)'
	set style fill transparent solid 0.3 noborder
	# colorscheme
	load '~/gnuplot-palettes/viridis.pal'
	p '1aqo_mut.all/1aqo_mut.all.dg-slices.dat' u 1:2:(\$2-\$3) w filledcurves above lt 1 notitle, \
	'' u 1:2:(\$2+\$3) w filledcurves below lt 1 notitle, \
	'' u 1:2 w lines lw 2 lt 1 title 'CAGUGC', \
	'GUAAUA.all/GUAAUA.all.dg-slices.dat' u 1:2:(\$2-\$3) w filledcurves above lt 2 notitle, \
	'' u 1:2:(\$2+\$3) w filledcurves below lt 2 notitle, \
	'' u 1:2 w lines lw 2 lt 2 title 'GUAAUA', \
	'1hs3.all/1hs3.all.dg-slices.dat' u 1:2:(\$2-\$3) w filledcurves above lt 3 notitle, \
	'' u 1:2:(\$2+\$3) w filledcurves below lt 3 notitle, \
	'' u 1:2 w lines lw 2 lt 3 title 'UUAAUU'
EOF
gnuplot dG-slicetrend.gp
cp dG-slicetrend.pdf $figsdir
# dG slicetrend from end, eqx data
cat > dG-slicetrend-e.gp <<-EOF
	set term pdf enhanced font '$font, $fontsize' 
	set out 'dG-slicetrend-e.pdf'
	set key above width 3
	set notitle 
	set yrange [5:13]
	set xlabel 'ns omitted from the end'
	set ylabel '{/Symbol D}G{/Symbol \260}_{stretch} (kcal/mol)'
	set style fill transparent solid 0.3 noborder
	# colorscheme
	load '~/gnuplot-palettes/viridis.pal'
	p '1aqo_mut-1hs3-ddg-trend-e.dat' u 1:(-\$2):(-\$2-\$5) w filledcurves above lt 1 notitle, \
	'' u 1:(-\$2):(-\$2+\$5) w filledcurves below lt 1 notitle, \
	'' u 1:(-\$2) w lines lw 2 lt 1 title 'CAGUGC', \
	'GUAAUA-1aqo_mut-ddg-trend-e.dat' u 1:(-\$2):(-\$2-\$5) w filledcurves above lt 2 notitle, \
	'' u 1:(-\$2):(-\$2+\$5) w filledcurves below lt 2 notitle, \
	'' u 1:(-\$2) w lines lw 2 lt 2 title 'GUAAUA', \
	'1hs3-GUAAUA-ddg-trend-e.dat' u 1:(-\$2):(-\$2-\$5) w filledcurves above lt 3 notitle, \
	'' u 1:(-\$2):(-\$2+\$5) w filledcurves below lt 3 notitle, \
	'' u 1:(-\$2) w lines lw 2 lt 3 title 'UUAAUU'
EOF
gnuplot dG-slicetrend-e.gp
cp dG-slicetrend-e.pdf $figsdir

(
cat << 'EOF' 
set term pdf enhanced font 'FONT, FSZ'
set out 'slicetrend-pub.pdf'
set key left width 4 samplen 1 horizontal outside
set xlabel 'ns Omitted from End'
set ylabel '{/Symbol D}{/Symbol D}G{/Symbol \260} (kcal/mol)'
unset title
set yrange [-5:3]
set style fill transparent solid 0.3 noborder
p \
'1aqo_mut-1hs3-ddg-trend-e.dat' u 1:4:($4-$7) w filledcurves above lc 3 notitle, \
'' u 1:4:($4+$7) w filledcurves below lc 3 notitle, \
'' u 1:4 w l lw 2 lc 3 title 'CAGUGC - UUAAUU', \
'GUAAUA-1aqo_mut-ddg-trend-e.dat' u 1:4:($4-$7) w filledcurves above lc 1 notitle, \
'' u 1:4:($4+$7) w filledcurves below lc 1 notitle, \
'' u 1:4 w l lw 2 lc 1 title 'GUAAUA - CAGUGC', \
'1hs3-GUAAUA-ddg-trend-e.dat' u 1:4:($4-$7) w filledcurves above lc 2 notitle, \
'' u 1:4:($4+$7) w filledcurves below lc 2 notitle, \
'' u 1:4 w l lw 2 lc 2 title 'UUAAUU - GUAAUA'
EOF
) | sed "s/FONT/$font/" | sed "s/FSZ/$fwfontsize/" > slicetrend.pub.gp 
gnuplot slicetrend.pub.gp
cp slicetrend-pub.pdf $figsdir

(
cat << 'EOF' 
set term pdf enhanced font 'FONT, FSZ'
set out 'slicetrend-res-pub.pdf'
unset key
#set key bottom width 1 samplen 1 horizontal outside
set yrange [-5:3]
set xlabel 'ns Omitted from End'
set ylabel '{/Symbol D}{/Symbol D}{/Symbol D}G{/Symbol \260} (kcal/mol)'
set notitle
set style fill transparent solid 0.3 noborder
p \
'1aqo_mut-1hs3-ddg-trend-e.dat' u 1:($4-2.15):($4-2.15-sqrt($7**2+0.52**2)) w filledcurves above lc 3 notitle, \
'' u 1:($4-(2.15)):($4-2.15+sqrt($7**2+0.52**2)) w filledcurves below lc 3 notitle, \
'' u 1:($4-(2.15)) w l lw 2 lc 3 title 'CAGUGC - UUAAUU', \
'GUAAUA-1aqo_mut-ddg-trend-e.dat' u 1:($4--3.26):($4--3.26-sqrt($7**2+0.46**2)) w filledcurves above lc 1 notitle, \
'' u 1:($4-(-3.26)):($4--3.26+sqrt($7**2+0.46**2)) w filledcurves below lc 1 notitle, \
'' u 1:($4-(-3.26)) w l lw 2 lc 1 title 'GUAAUA - CAGUGC', \
'1hs3-GUAAUA-ddg-trend-e.dat' u 1:($4-1.11):($4-1.11-sqrt($7**2+0.40**2)) w filledcurves above lc 2 notitle, \
'' u 1:($4-(1.11)):($4-1.11+sqrt($7**2+0.40**2)) w filledcurves below lc 2 notitle, \
'' u 1:($4-(1.11)) w l lw 2 lc 2 title 'UUAAUU - GUAAUA'
EOF
) | sed "s/FONT/$font/" | sed "s/FSZ/$fwfontsize/" > slicetrend.res.pub.gp 
gnuplot slicetrend.res.pub.gp
cp slicetrend-res-pub.pdf $figsdir

(
cat << 'EOF'
	set term pdf enhanced font 'FONT, FSZ'
	set out 'coverlap-hppull-pub.pdf'
	set key left width 3
	set notitle
	set encoding iso_8859_1
	set xlabel 'Distance, ({\305})'
	set ylabel '{/Symbol W}'
	set style fill transparent solid 0.3 noborder
	set yrange [0:1]
	# color scheme
	load '~/gnuplot-palettes/viridis.pal'
	p '1aqo_mut.plot.dat' u 1:2:($2-sqrt($3)/2) w filledcurves above lt 1 notitle, \
	  ''              u 1:2:($2+sqrt($3)/2) w filledcurves below lt 1 notitle, \
	  ''              u 1:2 w lines lw 2 lt 1 title 'CAGUGC', \
	  'GUAAUA.plot.dat' u 1:2:($2-sqrt($3)/2) w filledcurves above lt 2 notitle, \
	  ''              u 1:2:($2+sqrt($3)/2) w filledcurves below lt 2 notitle, \
	  ''              u 1:2 w lines lw 2 lt 2 title 'GUAAUA', \
	  '1hs3.plot.dat' u 1:2:($2-sqrt($3)/2) w filledcurves above lt 3 notitle, \
	  ''              u 1:2:($2+sqrt($3)/2) w filledcurves below lt 3 notitle, \
	  ''              u 1:2 w lines lw 2 lt 3 title 'UUAAUU'
EOF
) | sed "s/FONT/$font/" | sed "s/FSZ/$fwfontsize/" > covpub.gp
gnuplot covpub.gp
cp coverlap-hppull-pub.pdf $figsdir

# make aggregate HB plots
cd $hbsdir
(
cat << 'EOF'
	set term pdf enhanced font 'FONT, FSZ'
	set out 'comp-hbs-pub.pdf'
	set key right width 3
	set notitle
	set encoding iso_8859_1
	set xlabel 'Distance, ({\305})'
	set ylabel 'Average HB Count'
	set yrange [0:13]
	set style fill transparent solid 0.3 noborder
	set arrow from 15,0.3 to 60,0.3 lc rgb 'black' nohead
	set arrow from 17,0 to 17,13 lc rgb 'black' nohead
	# color scheme
	load '~/gnuplot-palettes/viridis.pal'
	p '1aqo_mut.hbplot.dat' u 1:2:($2-sqrt($3)/2) w filledcurves above lt 1 notitle, \
	  ''              u 1:2:($2+sqrt($3)/2) w filledcurves below lt 1 notitle, \
	  ''              u 1:2 w lines lw 2 lt 1 title 'CAGUGC', \
	  'GUAAUA.hbplot.dat' u 1:2:($2-sqrt($3)/2) w filledcurves above lt 2 notitle, \
	  ''              u 1:2:($2+sqrt($3)/2) w filledcurves below lt 2 notitle, \
	  ''              u 1:2 w lines lw 2 lt 2 title 'GUAAUA', \
	  '1hs3.hbplot.dat' u 1:2:($2-sqrt($3)/2) w filledcurves above lt 3 notitle, \
	  ''              u 1:2:($2+sqrt($3)/2) w filledcurves below lt 3 notitle, \
	  ''              u 1:2 w lines lw 2 lt 3 title 'UUAAUU'
EOF
) | sed "s/FONT/$font/" | sed "s/FSZ/$fwfontsize/" > comp-hbs-pub.gp
gnuplot comp-hbs-pub.gp
cp comp-hbs-pub.pdf $figsdir
cd $workdir

cat > all.dslices.pub.gp <<-EOF
	set output 'all-dslices-pu.pdf'
	set term pdf enhanced size 5.3 in, 1.5 in font '$font, $fwfontsize'
	set notitle
	set encoding iso_8859_1
	set xlabel 'Distance ({\305})'
	set ylabel "{/Symbol s}(Force)\n(kcal{\327}mol^{-1}{\305}^{-1})"
	set key right width 1
	set yrange [0:0.6]
	set xrange [15:60]
	# color scheme
	load '~/gnuplot-palettes/viridis.pal'
	p '$workdir/1aqo_mut.all/1aqo_mut.sem-fecD.$bore.$slicemin.dat' u  1:2 w l lw 1 t 'CAGUGC', \
	  '$workdir/GUAAUA.all/GUAAUA.sem-fecD.$bore.$slicemin.dat' u  1:2 w l lw 1 t 'GUAAUA', \
	  '$workdir/1hs3.all/1hs3.sem-fecD.$bore.$slicemin.dat' u 1:2 w l lw 1 t 'UUAAUU'
EOF

gnuplot all.dslices.pub.gp
cp all-dslices-pub.pdf $figsdir