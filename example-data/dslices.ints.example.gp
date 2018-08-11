set output 'dslices-ints-example.pdf'
set term pdf enhanced size 6.0 in, 1.5 in font 'Palatino, 12'
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
set palette maxcolors 7
set cbrange [0:600]
set cblabel 'ns omitted'
p for [i = 0:600:100] 'GUAAUA.all/GUAAUA.all.stdev-fecD.label.'.(600-i).'_ints.dat' u ($1):2:3 w boxes lc palette
