    set output 'GUAAUA-dslices-ints-example.pdf'
    set term pdf enhanced font 'Palatino, 12'
    set encoding iso_8859_1
    set title 'GUAAUA F.E.C. derivative standard deviation sliced from end'
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
    # load '~/gnuplot-palettes/viridis.pal'
    p for [i = 0:500:100] 'GUAAUA.all/GUAAUA.all.e.'.(500-i).'_ints.dat'     u ($1+0.5):2 w boxes axes x1y2 lt (6-i/100) t 'excluding '.(500 - i).' ns',     'GUAAUA.all/GUAAUA.all.e.0.dat' u  1:2 w l lw 0.5 lc 'black' axes x1y1 t 'Derivative SD'
