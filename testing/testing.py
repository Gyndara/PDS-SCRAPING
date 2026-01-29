import pandas as pd

df = pd.read_excel('data/scraping_kosan.xlsx')
jumlah_kota = df['Kota'].value_counts()
print(jumlah_kota)
