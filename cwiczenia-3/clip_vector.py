import geopandas as gpd
import shapely
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    clip_bounds = [567125.22, 244329.42, 567238.30, 244377.77]
    aoi_polygon = shapely.Polygon.from_bounds(*clip_bounds)

    buildings = gpd.read_file("bubd_a_testowa.fgb")
    buildings_clipped = buildings.clip(aoi_polygon, keep_geom_type=True)

    buildings.plot()
    buildings_clipped.plot()
    plt.show()
