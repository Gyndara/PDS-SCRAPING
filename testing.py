import pandas as pd

# Ganti 'file.xlsx' dengan nama file Excel kamu
df = pd.read_excel('scraping_kosan.xlsx')
jumlah_kota = df['Kota'].value_counts()
print(jumlah_kota)
