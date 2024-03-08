import requests
from owslib.wfs import WebFeatureService

def download_file(url):
    url = "https://opendata.geoportal.gov.pl/bdot10k/schemat2021/SHP/22/2209_SHP.zip"

    response = requests.get(url)

    with open("pobrany.zip", "wb") as file:
        file.write(response.content)

if __name__ == '__main__':
    wfs_service_url = 'https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WFS/SkorowidzPrawdziwejOrtofotomapy'
    wfs11 = WebFeatureService(url=wfs_service_url)
    
    response = wfs11.getfeature(
        bbox=(521726, 672247,5500500)
        )
