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


# Global Map
plt.imshow(pixel_map, extent=(-180, 180, -80, 80))

citys = pd.read_csv('Py4_Task5_worldcities.csv')
citys
# /5 so that dots are not overlapping one another.
log10Population = np.log10(citys['population'])

plt.title("Team 2 Global Population Heat Map")
plt.scatter(x=citys['lng'], y=citys['lat'],
            s=5, c=log10Population, cmap='coolwarm')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.savefig('Py4_Task5_worldmap_2.png', dpi=200, bbox_inches='tight')

# %%

# United States Map
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.tight_layout(pad=4)

# USA
usa_map = axes[0]
usa_map.imshow(pixel_map, extent=[-180, 180, -80, 80])
usa_map.scatter(citys['lng'], citys['lat'],
                c=log10Population, cmap='coolwarm', s=5)
usa_map.set_xlim(-125, -65)
usa_map.set_ylim(23, 52)
usa_map.set_xlabel('Longitude')
usa_map.set_ylabel('Latitude')
usa_map.set_title('Team 2 USA Population Heat Map')


# Subplot 2: Indiana
indiana_map = axes[1]
indiana_map.imshow(pixel_map, extent=[-180, 180, -80, 80])
indiana_map.scatter(citys['lng'], citys['lat'],
                    c=log10Population, cmap='coolwarm', s=5)
indiana_map.set_xlim(-88, -84)
indiana_map.set_ylim(37, 42)
indiana_map.set_xlabel('Longitude')
indiana_map.set_ylabel('Latitude')
indiana_map.set_title('Team 2 Indiana Population Heat Map')

fig.savefig("Py4_Task5_USAmap_2.png", dpi=200, bbox_inches='tight')

# %%
