import requests
from owslib.wfs import WebFeatureService

def download_and_save_file(input, output):
    response = requests.get(input)

    if response.status_code != 200:
        raise Exception(f"Nie udało się pobrać pliku z {input}. Kod błędu: {response.status_code}.")

    with open(output, "wb") as file:
        file.write(response.content)
 
def wfs_get_service_name(url, version="1.0.0"):
    try:
        wfs = WebFeatureService(url=url, version=version)
        return wfs.identification.title
    except Exception as e:
        raise Exception(f"Nie udało się pobrać nazwy serwisu. Błąd: {e}")

if __name__ == '__main__':
    # Testy pobierania
    download_and_save_file("https://bi.im-g.pl/im/e3/12/14/z21048035AMP.jpg", "doggo.jpg")
    download_and_save_file("https://opendata.geoportal.gov.pl/NumDaneWys/NMT/77218/77218_1301111_N-34-139-C-b-1-4.asc", "nmt.asc")

    try:
        download_and_save_file("bledny_adres.png", "xd.png")
    except Exception as e:
        print("Pobieranie z błędnego URL się nie udało. Sukces!")
        print("Wyjątek:", e)
    else:
        print("Ups...")

    # Testy WFS
    print("NMT", wfs_get_service_name("https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelTerenuEVRF2007/WFS/Skorowidze"))
    print("NMPT", wfs_get_service_name("https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelPokryciaTerenuEVRF2007/WFS/Skorowidze"))
    print("BDOT 10k", wfs_get_service_name("https://mapy.geoportal.gov.pl/wss/service/PZGIK/BDOT10k/WFS/StatystykiSieciWodnej", "2.0.0"))
    
    try:
        wfs_get_service_name("bledny_adres")
    except Exception as e:
        print("Zapytanie do błędnego serwisu nie przeszło. Sukces!")
        print("Wyjątek:", e)
    else:
        print("Ups...")
    