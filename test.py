import simulasyon

izgara, baslangic = simulasyon.harita_oku("paket_ornek/test03/harita.txt")
ayarlar = simulasyon.ayarlari_oku("paket_ornek/test03/ayarlar.json")
durum = simulasyon.yeni_durum(izgara, baslangic, ayarlar)

print("Boş yerde AL:", simulasyon.al(durum))
print("Elim boşken BIRAK:", simulasyon.birak(durum))
print("S olmayan yerde SARJ:", simulasyon.sarj(durum))

durum["x"] = 5
print("Kutunun üstünde AL:", simulasyon.al(durum), "| yük:", durum["yuk"])

durum["x"] = 9
print("T'de BIRAK:", simulasyon.birak(durum), "| teslim:", durum["teslim"])