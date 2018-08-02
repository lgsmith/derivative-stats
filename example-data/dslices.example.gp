set output 'all-dslices-pub.pdf'
set term pdf enhanced size 5.3 in, 1.5 in font 'Palatino, 12'
set notitle
set encoding iso_8859_1
set xlabel 'Distance ({\305})'
set ylabel "{/Symbol s}(Force)\n(kcal{\327}mol^{-1}{\305}^{-1})"
set key right width 1
set yrange [0:0.6]
set xrange [15:60]
# color scheme
# load '~/gnuplot-palettes/viridis.pal'
p 'GUAAUA.all/GUAAUA.sem-fecD.e.0.dat' u  1:2 w l lw 1 t 'GUAAUA'
