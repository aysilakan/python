import simulasyon


izgara, baslangic = simulasyon.harita_oku("paket_ornek/test01/harita.txt")
ayarlar = simulasyon.ayarlari_oku("paket_ornek/test01/ayarlar.json")
durum = simulasyon.yeni_durum(izgara, baslangic, ayarlar)
olay = simulasyon.ilerle(durum, 8)
print("Test1:", olay, durum["x"], durum["y"], durum["batarya"], durum["toplam_adim"])


izgara, baslangic = simulasyon.harita_oku("paket_ornek/test02/harita.txt")
ayarlar = simulasyon.ayarlari_oku("paket_ornek/test02/ayarlar.json")
durum = simulasyon.yeni_durum(izgara, baslangic, ayarlar)
olay = simulasyon.ilerle(durum, 7)
print("Test2:", olay, durum["x"], durum["y"], durum["batarya"], durum["carpisma"])
