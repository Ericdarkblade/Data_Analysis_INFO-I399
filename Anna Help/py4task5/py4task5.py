# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

# %%
pixel_map = imread('Py4_Task5_map.png')

# %%
# Top left pixel
# [1.        , 0.22745098, 0.22745098, 1.        ]


plt.imshow(pixel_map, extent=(-180, 180, -80, 80))

citys = pd.read_csv('Py4_Task5_worldcities.csv')
citys
# /5 so that dots are not overlapping one another.
log10Population = np.log10(citys['population'])/5

plt.title("Team 2 Global Population Heat Map")
plt.scatter(x=citys['lng'], y=citys['lat'],
            s=log10Population, c=log10Population, cmap='coolwarm')

plt.savefig('Py4_Task5_worldmap_2.png', dpi=200, bbox_inches='tight')
