from http.client import RemoteDisconnected
from pathlib import Path
from time import sleep
from typing import Union

import requests
from owslib.feature.wfs100 import WebFeatureService_1_0_0
from owslib.feature.wfs110 import WebFeatureService_1_1_0
from owslib.feature.wfs200 import WebFeatureService_2_0_0
from owslib.wfs import WebFeatureService

WfsType = Union[WebFeatureService_1_0_0, WebFeatureService_1_1_0, WebFeatureService_2_0_0]


def download_and_save_file(download_url: str, save_path: Union[Path, str]) -> None:
    response = requests.get(download_url)

    if response.status_code != 200:
        raise Exception(f"Failed to download {download_url}. Status code: {response.status_code}")

    with open(save_path, "wb") as file:
        file.write(response.content)


def wfs_connect_to_service(wfs_url: str, version: str = '1.0.0', number_of_retries: int = 10) -> WfsType:
    wfs_service = None
    for _ in range(number_of_retries):
        try:
            wfs_service = WebFeatureService(url=wfs_url, version=version)
        except (ConnectionError, RemoteDisconnected):
            sleep(1)
        else:
            break

    if wfs_service is None:
        raise Exception(f"Failed to communicate with WFS service {wfs_url}")

    return wfs_service

import geopandas as gpd


if __name__ == '__main__':
    wfs_service_url = "https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelTerenuEVRF2007/WFS/Skorowidze"
    wfs_service = wfs_connect_to_service(wfs_service_url, version='2.0.0')

    aoi_bounds = [566894.9, 244146.1, 567550.6, 244605.2]
    response = wfs_service.getfeature(
        bbox=tuple(aoi_bounds),
        typename=["gugik:SkorowidzNMT2023"]
    )

    with open("dane.xml", "wb") as file:
        file.write(response.read())

    
    sections = gpd.read_file("dane.xml")
    print(sections["url_do_pobrania"])

    # https://owslib.readthedocs.io/en/latest/usage.html#wfs

"""
def get_sample_aoi_bounds() -> shapely.Polygon:
    aoi_bounds = [566894.9, 244146.1, 567550.6, 244605.2]
    aoi_polygon = shapely.Polygon.from_bounds(*aoi_bounds)
    return aoi_polygon
"""

