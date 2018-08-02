set output 'dslices-example.pdf'
set term pdf enhanced size 5.3 in, 1.5 in font 'Palatino, 12'
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
set palette maxcolors 7
set cbrange [0:600]
set cblabel 'ns omitted'
p for [i = 0:600:100] 'GUAAUA.all/GUAAUA.all.stdev-fecD.label.'.i.'.dat' u  ($1):2:3 w l lw 2 lc palette 
