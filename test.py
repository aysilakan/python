import simulasyon

izgara, baslangic = simulasyon.harita_oku("paket_ornek/test03/harita.txt")
ayarlar = simulasyon.ayarlari_oku("paket_ornek/test03/ayarlar.json")
durum = simulasyon.yeni_durum(izgara, baslangic, ayarlar)

print(simulasyon.harita_metni(durum))
simulasyon.ilerle(durum, 3)
simulasyon.al(durum)
print()
print(simulasyon.harita_metni(durum))