import requests
import pandas as pd

url = "https://api.rukita.co/v2/discovery/search"

cookies = {
    "_rt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkX3RpbWVfbXMiOjE3NjkyMjMwNTAyNzUsImlkIjoiVkdWdVlXNTBUbTlrWlRvek9UY3lOVEU9IiwidG9rZW5faWQiOiIxZTFlMDEzOS1iOTA1LTRmMTctOGE2Zi0yM2JlNDE4NGRiMjQ0MTY4OGYyMS1hNGVkLTQ3MzAtOTliYy01MjAxNWFiOTZkZjYifQ.UNMYF-uydDp1-O5gd3Nf4wrG5g7fFDzwV4LbHxRZRV0",
    "_t": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRpc2NvcmR0YWkzQGdtYWlsLmNvbSIsImV4cCI6MTc2OTIzMDA3MCwiaWQiOiJWR1Z1WVc1MFRtOWtaVG96T1RjeU5URT0iLCJzZWN1cml0eSI6IiIsInR5cGUiOiJURU5BTlQifQ.T05xLmFNOBQQub7rpi1o0riKAQGx1kKDUnPq7CctOIM"
}

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://www.rukita.co",
    "referer": "https://www.rukita.co/",
    "user-agent": "Mozilla/5.0"
}

# ===============================
# KONFIGURASI
# ===============================
TARGET_ATTR_IDS = {"CCTV", "DINING_ROOM"}
all_units = []
page = 1
last_ids = set()

# ===============================
# PAGINATION LOOP
# ===============================
while True:
    payload = {
        "appVersion": "2.24.1",
        "filter": {
            "checkInDate": "2026-01-21",
            "locationId": 3273,
            "locationType": "CITY",
            "citySlug": "bandung",
            "types": ["1_CO_LIVING"]
        },
        "itemsPerPage": 24,
        "locale": "id_ID",
        "page": page,
        "platform": "WEB",
        "sort": "POPULARITY"
    }

    print(f"Mengirim request page {page}...")
    r = requests.post(url, json=payload, headers=headers, cookies=cookies)

    if r.status_code != 200:
        print("Error:", r.text)
        break

    data = r.json()
    units = data.get("list", [])

    if not units:
        print("Tidak ada data lagi. Stop.")
        break

    current_ids = {item.get("id") for item in units}

    if current_ids == last_ids:
        print("Halaman berhenti karena API mengulang data.")
        break

    all_units.extend(units)
    last_ids = current_ids
    page += 1

# ===============================
# EKSTRAKSI DATA
# ===============================
hasil_ekstraksi = []

for item in all_units:

    # Nama Properti
    nama = item.get("name", "N/A")

    # Harga
    harga = item.get("salePrice") or item.get("normalPrice") or 0

    # Jarak (meter → km)
    jarak_km = round(item.get("distance", 0) / 1000, 2)

    # Koordinat
    coord = item.get("coordinate", {})
    lat = coord.get("latitude")
    lng = coord.get("longitude")

    # Lokasi
    alamat = f"{item.get('districtName', '')}, {item.get('cityName', '')}"

    # Gender
    gender = item.get("gender", "Campur")

    # ===============================
    # FILTER ATRIBUT BERDASARKAN attrId
    # ===============================
    fasilitas = []

    for attr in item.get("assetAttributes", []):
        if (
            attr.get("attrId") in TARGET_ATTR_IDS and
            attr.get("valueBool") is True
        ):
            fasilitas.append(attr.get("name"))

    hasil_ekstraksi.append({
        "Nama Properti": nama,
        "Harga (Rp)": harga,
        "Jarak (KM)": jarak_km,
        "Latitude": lat,
        "Longitude": lng,
        "Lokasi": alamat,
        "Gender": gender,
        "Fasilitas": ", ".join(fasilitas) if fasilitas else "-"
    })

# ===============================
# EXPORT KE EXCEL
# ===============================
df = pd.DataFrame(hasil_ekstraksi)
file_name = "rukita_bandung_fasilitas.xlsx"
df.to_excel(file_name, index=False)

print(f"\nTotal properti disimpan: {len(df)}")
print(f"File berhasil dibuat → {file_name}")
