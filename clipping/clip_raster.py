import rasterio
from rasterio.mask import mask

if __name__ == '__main__':
    # buildings = gpd.read_file(r"D:\_WILK_\sik_3d\dane\bdot_10k\bubd_a_clip.fgb")
    # buildings = buildings.to_crs(epsg="2178")
    # shapes = [x for x in buildings["geometry"]]
    with rasterio.open("nmt/77912_1384996_7.125.11.13.asc", 'r') as src:
        out_image, out_transform = mask(src, shapes, crop=True)
        out_meta = src.meta
    
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    output_file = 'masked.tif'
    with rasterio.open(output_file, "w", **out_meta) as dest:
        dest.write(out_image)