import geopandas as gpd
import pandas as pd
import shapely

if __name__ == "__main__":

    aoi = shapely.Polygon()
    features = gpd.GeoDataFrame()
    
    features = features.clip(aoi)

    
    # features = pd.DataFrame()
    # features["nazwa"] = [str(x) for x in range(100)]
    # features["wartosc"] = [x for x in range(100)]
    
    # bin_mask = features["wartosc"] > 10
    # features = features[bin_mask]
    # print(features)