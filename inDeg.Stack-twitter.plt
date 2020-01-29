#
# Stack-twitter In Degree. G(12777, 10730). 906 (0.0709) nodes with in-deg > avg deg (1.7), 333 (0.0261) with >2*avg.deg (Wed Jan 29 00:46:17 2020)
#

set title "Stack-twitter In Degree. G(12777, 10730). 906 (0.0709) nodes with in-deg > avg deg (1.7), 333 (0.0261) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'inDeg.Stack-twitter.png'
plot 	"inDeg.Stack-twitter.tab" using 1:2 title "" with linespoints pt 6
