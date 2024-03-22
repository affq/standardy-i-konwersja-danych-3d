import rasterio
from rasterio.mask import mask
import shapely
import pyproj

def pl92_to_pl2000(xy):
    transformer = pyproj.Transformer.from_crs(2180, 2178, always_xy=True)
    new_xy = transformer.transform(*xy)
    return new_xy

if __name__ == '__main__':
    clip_bounds = [567125.22, 244329.42, 567238.30, 244377.77]
    clip_bounds = pl92_to_pl2000(clip_bounds[:2]) + pl92_to_pl2000(clip_bounds[2:])
    aoi_polygon = shapely.Polygon.from_bounds(*clip_bounds)
    print(aoi_polygon.representative_point())

    with rasterio.open("nmt.tif", 'r') as src:
        out_image, out_transform = mask(src, [aoi_polygon], crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    output_file = 'masked.tif'
    with rasterio.open(output_file, "w", **out_meta) as dest:
        dest.write(out_image)