#!/usr/bin/env python3
import numpy as np
from sys import argv

array = np.genfromtxt(argv[1])
collength = array.shape[0]
label = np.repeat(int(argv[3]), collength)
np.savetxt(argv[2], np.column_stack((label, array)))