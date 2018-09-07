#!/usr/bin/env python3
import numpy as np

ndatasets = 4
translations = np.linspace(-0.1, 0.1, ndatasets)
twodlabel = 'test2d-'
threedlabel = 'test3d-'
# for 2D
bincount = 200
x2, y2 = np.meshgrid(np.linspace(-np.pi, np.pi, bincount), np.linspace(-np.pi, np.pi, bincount))
range2d = np.sqrt(x2 * x2 + y2 * y2)
# for 3D
x3, y3, z3 = np.meshgrid(np.linspace(-np.pi, np.pi, bincount), np.linspace(-np.pi, np.pi, bincount),
                              np.linspace(-np.pi, np.pi, bincount))
range3d = np.sqrt(x3 * x3 + y3 * y3 + z3 * z3)

for t in range(ndatasets):
    # 2D
    trans = translations[t]
    with open(twodlabel + str(t) + ".dat", 'w') as f:
        f.write("# offset_zero " + str(trans)+"\n")
        sigma, mu = 1.0, 0.0 + trans
        g2 = np.exp(-(range2d - mu) ** 2 / (2.0 * sigma ** 2))
        for i in range(bincount):
            for j in range(bincount):
                outstr = '\t'.join(map(str, [x2[i, j], y2[i, j], g2[i, j]]))+"\n"
                f.write(outstr)
    # 3D
    with open(threedlabel + str(t) +  ".dat", 'w') as f:
        f.write("# offset_zero " + str(trans)+"\n")
        sigma, mu = 1.0, 0.0 + trans
        g3 = np.exp(-(range3d - mu) ** 2 / (2.0 * sigma ** 2))
        for i in range(bincount):
            for j in range(bincount):
                for k in range(bincount):
                    outstr = '\t'.join(map(str, [x3[i, j, k], y3[i, j, k], z3[i, j, k], g3[i, j, k]])) + "\n"
                    f.write(outstr)
