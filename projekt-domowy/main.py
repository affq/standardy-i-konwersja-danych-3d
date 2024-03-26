import geopandas as gpd
import matplotlib.pyplot as plt
from owslib.wfs import WebFeatureService
from http.client import RemoteDisconnected
from time import sleep
import requests
from owslib.wfs import WebFeatureService

def download_and_save_file(download_url, save_path) -> None:
    response = requests.get(download_url)

    if response.status_code != 200:
        raise Exception(f"Failed to download {download_url}. Status code: {response.status_code}")

    with open(save_path, "wb") as file:
        file.write(response.content)

def wfs_connect_to_service(wfs_url: str, version: str = '1.0.0', number_of_retries: int = 10):
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

if __name__ == '__main__':
    file = "G:\Mój dysk\studia\SEMESTR IV\Standardy i konwersja danych 3D\standardy-i-konwersja-danych-3d\projekt-domowy\hextiles 1.fgb"
    index = 3
    folder = "G:\Mój dysk\studia\SEMESTR IV\Standardy i konwersja danych 3D\standardy-i-konwersja-danych-3D\projekt-domowy\output"

    tiles = gpd.read_file(file)
    tile = tiles.iloc[[index]]

    bbox = tile.total_bounds
    bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
    bbox = tuple(bbox)

    nmt_url = "https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelTerenuEVRF2007/WFS/Skorowidze"
    nmt_wfs = wfs_connect_to_service(nmt_url, version='2.0.0')
    nmt_response = nmt_wfs.getfeature(
        bbox=bbox,
        typename=["gugik:SkorowidzNMT2023"]
    )

    with open(f"{folder}/nmt.xml", "wb") as file:
        file.write(nmt_response.read())
    
    # nmt_sections = gpd.read_file(f"{folder}/nmt.xml")
    # nmt_url_hex = nmt_sections["url_do_pobrania"]
    # download_and_save_file(nmt_url_hex, f"{folder}/nmt.asc")

    nmpt_url = "https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelPokryciaTerenuEVRF2007/WFS/Skorowidze"
    nmpt_wfs = wfs_connect_to_service(nmpt_url, version='2.0.0')
    nmpt_response = nmpt_wfs.getfeature(
        bbox=bbox,
        typename=["gugik:SkorowidzNMPT2023"]
    )

    with open(f"{folder}/nmpt.xml", "wb") as file:
        file.write(nmpt_response.read())
    
    # nmpt_sections = gpd.read_file(f"{folder}/nmpt.xml")
    # nmpt_url_hex = nmpt_sections["url_do_pobrania"]
    # download_and_save_file(nmpt_url_hex, f"{folder}/nmpt.tif")

    bdot_url = "https://mapy.geoportal.gov.pl/wss/service/PZGIK/BDOT/WFS/PobieranieBDOT10k"
    bdot_wfs = wfs_connect_to_service(bdot_url, version='2.0.0')
    bdot_response = bdot_wfs.getfeature(
        bbox=bbox,
        typename=["ms:BDOT10k_powiaty"]
    )

    with open(f"{folder}/bdot.xml", "wb") as file:
        file.write(bdot_response.read())
    
    # bbox_sections = gpd.read_file(f"{folder}/bbox.xml")
    # bbox_url_hex = bbox_sections["URL_GML"]
    # download_and_save_file(bbox_url_hex, f"{folder}/bbox.zip")

    tile.plot()
    plt.show()