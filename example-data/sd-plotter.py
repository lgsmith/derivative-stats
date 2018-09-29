import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

slicemin = 0
slicemax = 600
slicewidth = 100

# make it this way to extend to non-like named sequences/filenames
seq = {'GUAAUA': 'GUAAUA'}
xlim = (15.0, 60.0)
ylim = (0.0, 0.6)
# in inches
size = (6.5, 5)
fig, ax = plt.subplots(1,2,figsize=size,gridspec_kw = {'width_ratios':[5, 1]})
m = 'GUAAUA'
norm = colors.Normalize(slicemin, slicemax)
slices = np.arange(slicemin, slicemax+slicewidth, slicewidth)
cmap = colors.ListedColormap([plt.cm.viridis(norm(s)) for s in slices])
for s in range(slicemax, slicemin - slicewidth, -slicewidth):
    data = np.genfromtxt(m + '.'+str(s)+'-sd.asc')
    color = plt.cm.viridis(norm(s)) 
    ax[0].plot(
        data[:, 0],
        data[:, 1],
        color=color,
        linewidth=1)

cbar  = mpl.colorbar.ColorbarBase(ax[1], cmap=cmap, ticks=slices, orientation='vertical', norm=norm)
cbar.ax.set_yticklabels(slices)
cbar.ax.set_ylabel('ns omitted')
ax[0].set_xlabel('Distance($\mathrm{\AA}$)')
ax[0].set_ylabel(
    '$\sigma(\mathrm{Force}) (\mathrm{kcal}\\times\mathrm{mol}^{-1}\mathrm{\AA}^{-1})$',
)
ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)
plt.savefig(
    'all-sd-pub.pdf', format='pdf', bbox_inches='tight', transparent=True)
plt.show()
