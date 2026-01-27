import requests
import pandas as pd
import time

#API
url = "https://api.rukita.co/v2/discovery/search"

#login session
cookies = {
    "_rt": "",
    "_t": ""
}

#menghindari deteksi bot (penyamaran)
headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://www.rukita.co",
    "referer": "https://www.rukita.co/",
    "user-agent": "Mozilla/5.0"
}

#filtering fasilitas kosan yang diambil
TARGET_ATTR_IDS = {
    "WIFI", "CCTV", "DINING_ROOM", "KITCHEN_ROOM", "LIVING_ROOM",
    "PARKING_CAR", "PARKING_MOTORBIKE", "SERVICE_LAUNDRY",
    "SERVICE_CLEANING", "REFRIGERATOR", "DISPENSER", "SOFA",
    "TABLE", "STOVE", "COOKING_UTENSIL"
}

#filtering kosan berdasarkan penyedia (rukita/uma/info kost/RUPARTNER)
INFOKOST_TYPES = [
    "RUPARTNER",
    "RUPARTNER_PLUS",
    "INFOKOST_PRO",
    "INFOKOST_PRO_PREVIOUSLY_RUPARTNER_PLUS"
]

#menghindari duplikat data
MAX_PAGE = 34
ITEMS_PER_PAGE = 24

#rate limit API
SLEEP = 0.3

all_units = []
#cek duplikat
seen_ids = set()

#proses scraping data
for page in range(1, MAX_PAGE + 1):
    #data request hanya menggunakan filter tipe komersial
    payload = {
        "appVersion": "2.25.1",
        "filter": {
            "locationId": 84,
            "locationType": "COUNTRY",
            "poiId": 0,
            "checkInDate": "2026-01-25",
            "priceGte": 0,
            "priceLte": 30000000,
            "roomPax": 0,
            "commercialType": INFOKOST_TYPES,
            "types": ["1_CO_LIVING"]
        },
        "sort": "POPULARITY",
        "page": page,
        "itemsPerPage": ITEMS_PER_PAGE,
        "platform": "WEB",
        "locale": "id_ID"
    }
    print(f"[PAGE KE-{page}]")

    r = requests.post(url, json=payload, headers=headers, cookies=cookies)
    #kondisional jika terjadi gagal request
    if r.status_code != 200:
        print("Error:", r.text)
        break
    
    data = r.json()
    units = data.get("list", [])

    if not units:
        print("data kosong")
        time.sleep(SLEEP)
        continue

    #menampung berapa data yang didapat dari setiap page
    new_count = 0
    for item in units:
        item_id = item.get("id")
        #kondisional untuk mengecek data sudah ada atau belum
        if item_id not in seen_ids:
            seen_ids.add(item_id)
            all_units.append(item)
            new_count += 1

    print(f"Data page: {len(units)} | Data baru: {new_count} | Total data: {len(seen_ids)}")
    time.sleep(SLEEP)

#menyimpan data hasil scraping
hasil_ekstraksi = []

for item in all_units:
    #mengambil data fasilitas dari setiap kosan, berdasarkan filter id yang sudah dibuat
    fasilitas = []
    for attr in item.get("assetAttributes", []):
        if attr.get("attrId") in TARGET_ATTR_IDS and attr.get("valueBool"):
            fasilitas.append(attr.get("name"))

    #mengambil nilai lat dan long
    coord = item.get("coordinate", {})

    #menyimpan data dari hasil scraping
    hasil_ekstraksi.append({
        "Nama Properti": item.get("name", "N/A"),
        "Commercial Type": item.get("commercialType"),
        "Harga (Rp)": item.get("salePrice") or item.get("normalPrice") or 0,
        "Latitude": coord.get("latitude"),
        "Longitude": coord.get("longitude"),
        "Lokasi": f"{item.get('districtName', '')}, {item.get('cityName', '')}",
        "Kota": f'{item.get('cityName')}',
        "Fasilitas": ", ".join(fasilitas) if fasilitas else "-"
    })

#mengexport data menjadi file excel
df = pd.DataFrame(hasil_ekstraksi)
df.to_excel("infoKost_scraping.xlsx", index=False)