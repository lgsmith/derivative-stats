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
fig, ax = plt.subplots(1,2, figsize=size, gridspec_kw = {'width_ratios':[7, 1]})
slices = np.arange(slicemin, slicemax + slicewidth, slicewidth)
cmap = colors.ListedColormap([plt.cm.viridis(norm(s)) for s in slices])
for s in range(slicemax, slicemin - slicewidth, -slicewidth):
    data = np.genfromtxt(m + '.' + str(s) + '-int.asc')
    color = plt.cm.viridis(norm(s))
    ax[0].bar(edges[:-1], data[:, 1], widths, align='edge', color=color)


cbar  = mpl.colorbar.ColorbarBase(ax[1], cmap=cmap, ticks=slices, orientation='vertical', norm=norm)
cbar.ax.set_yticklabels(slices)
cbar.ax.set_ylabel('ns omitted')
ax[0].set_xlabel(xlabel)
ax[0].set_ylabel(ylabel)
ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)
fig.suptitle('The Standard Deviation in the Window Integrals of the Derivatives of the FECs')
plt.savefig('example-ints.pdf', format='pdf', bbox_inches='tight', transparent=True)
plt.show()