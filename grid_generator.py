import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches
from matplotlib.collections import PatchCollection

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

n_x = 3
n_y = 4

image_size = (100, 200)

fig = plt.figure()

fig = gcf()
DPI = fig.get_dpi()
fig.set_size_inches(image_size[0]/float(DPI), image_size[1]/float(DPI))

currentAxis = plt.gca()


dx = image_size[0]/n_x
dy = image_size[1]/n_y

for i in range(n_x):
    for j in range(n_y):

        xy = (i*dx, j*dy)
        currentAxis.add_patch(Rectangle(xy, width=dx, height=dy,
                                        alpha=1.0, fill=None))
    


plt.axis('off')

plt.show()

plt.savefig("slm3.png", bbox_inches='tight')





