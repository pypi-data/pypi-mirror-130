import requests
from bs4 import BeautifulSoup


def extraksi_data():
    """

    Tanggal: 06 Desember 2021
    Waktu: 21:24:11 WIB
    magnitudo: 4.5
    Kedalaman: 15 km
    Lokasi :7.74 LS - 119.03 BT
    Keterangan: Pusat gempa berada di laut 85 km TimurLaut Bima
    Dirasakan: Dirasakan (Skala MMI): III Bima
    :return:
    """
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(',')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        print(result)

        i=0
        magnitudo =None
        kedalaman =None
        ls = None
        bt = None
        lokasi = None
        dirasakan =None


        for data in result:
            if i == 1:
                magnitudo = data.text
            elif i == 2:
                kedalaman = data.text
            elif i == 3:
                koordinat = data.text.split (' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = data.text
            elif i == 5:
                dirasakan = data.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal #"06 Desember 2021"
        hasil['waktu'] = waktu #"21:24:11 WIB"
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {"ls": ls, "bt": bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan

        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("Data tidak bisa ditampilkan")
        return

    print(f"Tanggal {result['tanggal']}")
    print(f"Waktu {result['waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"Koordinat: LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Dirasakan{result['dirasakan']}")
    print(f"Lokasi{result['lokasi']}")


