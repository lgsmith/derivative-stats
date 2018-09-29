import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

slicemin = 0
slicemax = 3
slicewidth = 1

xlim = (15.0, 60.0)
# in inches
size = (6.5, 5)
fig, ax = plt.subplots(1,2,figsize=size,gridspec_kw = {'width_ratios':[7, 1]})
m = 'GUAAUA'
norm = colors.Normalize(slicemin, slicemax)
slices = np.arange(slicemin, slicemax+slicewidth, slicewidth)
cmap = colors.ListedColormap([plt.cm.viridis(norm(s)) for s in slices])
for s in range(slicemax, slicemin - slicewidth, -slicewidth):
    data = np.genfromtxt(m + '.0-deriv-'+str(s)+'.asc')
    color = plt.cm.viridis(norm(s)) 
    ax[0].plot(
        data[:, 0],
        data[:, 1],
        color=color,
        linewidth=1)

cbar  = mpl.colorbar.ColorbarBase(ax[1], cmap=cmap, ticks=slices, orientation='vertical', norm=norm)
cbar.ax.set_yticklabels(slices)
cbar.ax.set_ylabel('replica')
ax[0].set_xlabel('Distance($\mathrm{\AA}$)')
ax[0].set_ylabel(
    'Force $(\mathrm{kcal}\\times\mathrm{mol}^{-1}\mathrm{\AA}^{-1})$'
)
ax[0].set_xlim(xlim)
fig.suptitle('The Numerical Derivative of Four Replica FECs')
plt.savefig(
    'example-derivs.pdf', format='pdf', bbox_inches='tight', transparent=True)
plt.show()
