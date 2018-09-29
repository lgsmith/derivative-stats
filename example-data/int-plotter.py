import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

slicemin = 0
slicemax = 600
slicewidth = 100

xlim = (15.0, 60.0)
ylim = (0.0, 0.6)
# need to write in tex for the default nonmathtext to be palatino, matching other figs.
ylabel = '$\sigma\mathrm{(window)}$ (kcal/mol)'
xlabel = 'Distance ($\mathrm{\AA}$)'
size = (6.5, 5)
edges = np.genfromtxt('edges.txt')
widths = np.trim_zeros(np.append(edges, edges[-1]) - np.append(0, edges))[1:]
centers = edges[:-1] + widths / 2
norm = colors.Normalize(slicemin, slicemax)
m = 'GUAAUA'
plt.figure(figsize=size)
for s in range(slicemax, slicemin - slicewidth, -slicewidth):
    data = np.genfromtxt(m + '.' + str(s) + '-int.asc')
    color = plt.cm.viridis(norm(s))
    plt.bar(edges[:-1], data[:, 1], widths, align='edge', color=color)
plt.ylabel(ylabel)
plt.xlabel(xlabel)
plt.ylim(ylim)
plt.xlim(xlim)
plt.savefig(m + '-ints.pdf', format='pdf', bbox_inches='tight', transparent=True)
plt.show()