from typing import Optional


def try_to_import_package(package_name: str) -> Optional[Exception]:
    try:
        __import__(package_name)
    except Exception as e:
        return e
    else:
        return None


def test_requests():
    result = try_to_import_package("requests")
    assert result is None, result


def test_numpy():
    result = try_to_import_package("numpy")
    assert result is None, result


def test_pandas():
    result = try_to_import_package("pandas")
    assert result is None, result


def test_tqdm():
    result = try_to_import_package("tqdm")
    assert result is None, result


def test_geopandas():
    import geopandas as gpd
    features = gpd.read_file("data/test_vector_data.shp")
    assert len(features) == 18


def test_gdal():
    from osgeo import gdal
    raster: gdal.Dataset = gdal.Open("data/test_raster.tif")
    assert raster.RasterXSize == 434
    assert raster.RasterYSize == 471
    assert raster.RasterCount == 1


def test_rasterio():
    import rasterio
    with rasterio.open("data/test_raster.tif") as raster:
        assert raster.height == 471
        assert raster.width == 434


def test_open3d():
    import open3d
    mesh = open3d.geometry.TriangleMesh.create_sphere()
    assert True


def test_laspy():
    import laspy
    las_data = laspy.read("data/test_point_cloud.laz")
    assert len(las_data) == 439_777
