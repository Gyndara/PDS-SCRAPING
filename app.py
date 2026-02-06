import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Analisis Harga Kosan Rukita",
    layout="wide"
)

df = pd.read_excel('data/scraping_kosan.xlsx')
polygon = pd.read_excel('data/kordinat_polygon.xlsx')
grafik = pd.read_excel('data/UMR.xlsx')
grafikMakan = pd.read_excel('data/BiayaMakan.xlsx')
rumah = pd.read_excel('data/HargaRumah.xlsx')

avg_harga_per_kota = df.groupby("Kota")["Harga (Rp)"].mean().to_dict()
jumlah_kosan_per_kota = df["Kota"].value_counts()

kelas1 = 84
kelas2 = 156
kelas3 = 180

# Gabungan wilayah
gabungan_kota = {
    "Bandung": ["Bandung", "Kabupaten Bandung", "Kabupaten Bandung Barat"],
    "Yogyakarta": ["Yogyakarta", "Kabupaten Bantul"],
    "Solo (Surakarta)": ["Solo (Surakarta)", "Kabupaten Karanganyar"]
}

gabungan_fasilitas = {
    "Bandung": ["Bandung", "Kabupaten Bandung", "Kabupaten Bandung Barat", "Kabupaten Sumedang"],
    "Yogyakarta": ["Yogyakarta", "Kabupaten Sleman"],
    "Solo (Surakarta)": ["Solo (Surakarta)", "Kabupaten Karanganyar"],
    "Jakarta" : ["Kabupaten Tangerang", "Tangerang", "Jakarta Barat", "Jakarta Utara", "Jakarta Pusat", "Jakarta Timur", "Bekasi", "Jakarta Selatan", "Tangerang Selatan", "Depok", 'Kabupaten Bekasi' ],
    "Bogor" : ["Kabupaten Bogor", "Bogor"],
    "Solo (Surakarta)": ['Solo (Surakarta)', "Kabupaten Sukoharjo"],
    "Denpasar": ['Kabupaten Badung', 'Denpasar'],
    "Malang": ["Kabupaten Malang", "Malang"],
    "Surabaya": ["Surabaya", "Kabupaten Sidoarjo"]
}

# Koordinat awal map
kota_map = {
    '': {'lat': -0.19164045731720974, 'lon': 110.16835376392196, 'zoom': 5},
    'Jakarta': {'lat': -6.2661, 'lon': 106.7832, 'zoom': 10.5},
    'Bandung': {'lat': -6.9240, 'lon': 107.6806, 'zoom': 12},
    'Bogor': {'lat': -6.5467, 'lon': 106.8258, 'zoom': 12},
    'Yogyakarta': {'lat': -7.7384, 'lon': 110.3976, 'zoom': 12},
    'Semarang': {'lat': -7.0017, 'lon': 110.3976, 'zoom': 12},
    'Medan': {'lat': 3.5702987393965637,'lon': 98.64896053476728,'zoom': 12},
    'Serang': {'lat': -6.1259, 'lon': 106.1403,'zoom': 12},
    'Malang': {'lat': -7.9664, 'lon': 112.6315, 'zoom': 12},
    'Surabaya': {'lat': -7.30859275938801, 'lon': 112.73223806582098, 'zoom': 10.5},
    'Solo (Surakarta)': {'lat': -7.568031155668305, 'lon': 110.81161555233238, 'zoom': 12},
    'Denpasar': {'lat': -8.69020045581404, 'lon':115.20786276395158, 'zoom': 12}
}

st.title('ANALISIS KECOCOKAN HUNIAN BERDASARKAN UMR')
st.write(
    'Hasil analisis ini memberikan informasi kepada masyarakat berapa uang yang perlu dikeluarkan untuk membayar sewa tempat tinggal disetiap daerahnya dan fasilitas apa saja yand didapatkan, serta memperhitungkan gaji UMR yand dimiliki dan biaya tempat tinggal yang perlu dibayar'
)

st.subheader("Pilih Kota")

selected_city = st.selectbox(
    "-",
    list(kota_map.keys())
)

if selected_city in gabungan_fasilitas:
    df_filtered = df[df["Kota"].isin(gabungan_fasilitas[selected_city])]
    grafik_filtered = grafik[grafik["Kota"].isin(gabungan_fasilitas[selected_city])]
    grafikMakan_filtered = grafikMakan[grafikMakan["Kota"].isin(gabungan_fasilitas[selected_city])]
    df_HargaRumah = rumah[rumah['Kota'].isin(gabungan_fasilitas[selected_city])]
else:
    df_filtered = df[df["Kota"] == selected_city]
    grafik_filtered = grafik[grafik["Kota"] == selected_city]
    grafikMakan_filtered = grafikMakan[grafikMakan["Kota"] == selected_city]
    df_HargaRumah = rumah[rumah['Kota'] == selected_city]

rumah_filtered = rumah.copy()

lat = kota_map[selected_city]['lat']
lon = kota_map[selected_city]['lon']
zoom = kota_map[selected_city]['zoom']

m = folium.Map(location=[lat, lon], zoom_start=zoom)

legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 200px;
    height: 170px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 14px;
    color : black;
    padding: 10px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
<b>Legenda Kepadatan Kosan</b><br><br>
<i style="background:blue; width:18px; height:18px; float:left; margin-right:8px;"></i>
Sangat Rendah (&le; 50)<br>

<i style="background:yellow; width:18px; height:18px; float:left; margin-right:8px;"></i>
Rendah (51–80)<br>

<i style="background:orange; width:18px; height:18px; float:left; margin-right:8px;"></i>
Padat (81–150)<br>

<i style="background:red; width:18px; height:18px; float:left; margin-right:8px;"></i>
Sangat Padat (> 150)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

for kota, group in polygon.groupby("Kota"):

    coords = group[["Latitude", "Longitude"]].values.tolist()

    # hitung kosan gabungan
    if kota in gabungan_kota:
        jumlah_kosan = sum(
            jumlah_kosan_per_kota.get(k, 0)
            for k in gabungan_kota[kota]
        )
    else:
        jumlah_kosan = jumlah_kosan_per_kota.get(kota, 0)

    # warna polygon
    if jumlah_kosan <= 50:
        color = "blue"
    elif jumlah_kosan <= 80:
        color = "yellow"
    elif jumlah_kosan <= 150:
        color = "orange"
    else:
        color = "red"

    if len(coords) >= 3:
        folium.Polygon(
            locations=coords,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.4
        ).add_to(m)

    avg_harga = avg_harga_per_kota.get(kota, 0)

    popup_info = f"""
    <b>{kota}</b><br>
    Jumlah kosan: {jumlah_kosan}<br>
    Rata-rata harga: Rp {avg_harga:,.0f}
    """

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        popup=popup_info,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Peta Persebaran Kosan – {selected_city}")
    st_folium(m, use_container_width=True, height=650)


df_tabel_fasilitas = (
    df_filtered
    .groupby("Kota")["Fasilitas"]
    .apply(lambda x: ", ".join(
        sorted(set(", ".join(x.astype(str)).split(", ")))
    ))
    .reset_index()
)

with col2:
    st.subheader(f"Rata-rata fasilitas yang disediakan di area {selected_city}")
    st.dataframe(
        df_tabel_fasilitas,
        width="stretch",
        use_container_width=True,
        hide_index=True
    )

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader('Grafik UMR dan rata-rata harga kosan')
    st.write('Berasal dari website pinhome yang membahas mengenai "Panduan Biaya Sewa Tempat Tinggal Idel Sesuai Pendapatan" Biaya sewa yang ideal adalah 30-40% dari gaji yang kita miliki agar tetap aman secara finansial.')
    grafik_filtered = grafik_filtered.copy()

    grafik_filtered["Batas 30% UMR"] = grafik_filtered["UMK"] * 0.3
    grafik_filtered["Batas 40% UMR"] = grafik_filtered["UMK"] * 0.4
    #grafik
    plt.figure(figsize=(10, 4))

    plt.plot(
        grafik_filtered["Kota"],
        grafik_filtered["UMK"],
        marker="o",
        label="UMR",
        color='green'
    )

    plt.plot(
        grafik_filtered["Kota"],
        grafik_filtered["ratarata"],
        marker="o",
        label="Rata-rata Harga Kos",
        color='orange'
    )

    plt.plot(
        grafik_filtered["Kota"],
        grafik_filtered["Batas 30% UMR"],
        marker="o",
        linestyle="--",
        color="blue",
        label="Minimum sewa 30% UMR"
    )

    plt.plot(
        grafik_filtered["Kota"],
        grafik_filtered["Batas 40% UMR"],
        marker="o",
        linestyle="--",
        color="red",
        label="Maksimum sewa 40% UMR"
    )

    plt.ylabel("Rupiah (Rp)")
    plt.xlabel("Kota")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    st.pyplot(plt)

with col4:
    st.subheader('Grafik pengeluaran biaya makan perbulan')
    st.write('Grafik ini bertujuan untuk memberikan gambaran berapa biaya dari gaji UMR yang terpotong untuk membayar biaya makan per-bulan, data pengeluaran per-bulan untuk makan per-daerahnya kami dapatkan dari BPS (Badan Pusat Statistik)')
    fig2 = plt.figure(figsize=(10, 4))

    x = range(len(grafik_filtered["Kota"]))
    width = 0.35

    plt.bar(
        x,
        grafik_filtered["UMK"],
        width=width,
        label="UMR"
    )

    plt.bar(
        [i + width for i in x],
        grafikMakan_filtered["Biaya Makan"],
        width=width,
        label="Biaya Makan"
    )

    plt.xticks(
        [i + width / 2 for i in x],
        grafik_filtered["Kota"],
        rotation=45
    )

    plt.ylabel("Rupiah (Rp)")
    plt.xlabel("Kota")
    plt.legend()
    plt.grid(axis="y")

    st.pyplot(fig2)

st.divider()

st.subheader('Lama pelunasan Rumah')
st.write('Perhitungan ini didapatkan dengan cara menghitung sisa gaji setelah membayar biaya sewa rumah dan juga biaya makan perbulan, lalu membagi harga rumah dengan sisa gaji')
# Gabungkan UMR + harga kos + biaya makan
df_keuangan = (
    grafik_filtered[["Kota", "UMK", "ratarata"]]
    .merge(
        grafikMakan_filtered[["Kota", "Biaya Makan"]],
        on="Kota",
        how="inner"
    )
)

# Hitung sisa gaji per bulan
df_keuangan["Sisa UMR / Bulan"] = (
    df_keuangan["UMK"]
    - (df_keuangan["ratarata"] + df_keuangan["Biaya Makan"])
)

# Gabungkan dengan harga rumah
df_lama_pelunasan = (
    df_keuangan[["Kota", "Sisa UMR / Bulan"]]
    .merge(
        df_HargaRumah[["Kota", "Harga"]],
        on="Kota",
        how="inner"
    )
)

# Hitung lama pelunasan (tahun)
df_lama_pelunasan["Lama Pelunasan (Tahun)"] = (
    df_lama_pelunasan["Harga"]
    / df_lama_pelunasan["Sisa UMR / Bulan"]
    / 12
).round(1)

df_lama_pelunasan = df_lama_pelunasan[[
    "Kota",
    "Sisa UMR / Bulan",
    "Harga",
    "Lama Pelunasan (Tahun)"
]]

st.dataframe(
    df_lama_pelunasan,
    use_container_width=True,
    hide_index=True
)

st.subheader('UMR ideal ditiap daerah')
st.write('perhitungan ideal ini berdasarkan biaya yang dikeluarkan untuk sewa tempat tinggal, biaya makan perbulan')

rumah_kelas1 = rumah[rumah["Kelas"] == "Kelas 1"]

df_ideal = (
    grafik_filtered[["Kota", "UMK", "ratarata"]]
    .merge(
        grafikMakan_filtered[["Kota", "Biaya Makan"]],
        on="Kota",
        how="inner"
    )
    .merge(
        rumah_kelas1[["Kota", "Harga"]],
        on="Kota",
        how="inner"
    )
)

target_bulan = 7 * 12

df_ideal["Sisa Ideal / Bulan"] = df_ideal["Harga"] / target_bulan

df_ideal["UMR Baru"] = (
    df_ideal["Sisa Ideal / Bulan"]
    + df_ideal["ratarata"]
    + df_ideal["Biaya Makan"]
).round(0)

df_ideal["Nilai Kenaikan (Rp)"] = (
    df_ideal["UMR Baru"] - df_ideal["UMK"]
)

df_umr_ideal = df_ideal[[
    "Kota",
    "UMK",
    "Nilai Kenaikan (Rp)",
    "UMR Baru"
]]

st.dataframe(
    df_umr_ideal,
    use_container_width=True,
    hide_index=True
)