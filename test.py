import simulasyon

izgara, baslangic = simulasyon.harita_oku("paket_ornek/test01/harita.txt")
ayarlar = simulasyon.ayarlari_oku("paket_ornek/test01/ayarlar.json")
durum = simulasyon.yeni_durum(izgara, baslangic, ayarlar)

print("Başlangıç:", durum["yon"], durum["batarya"])
simulasyon.don(durum, "SAG")
print("SAG sonrası:", durum["yon"], durum["batarya"])
simulasyon.don(durum, "SOL")
simulasyon.don(durum, "SOL")
print("2 SOL sonrası:", durum["yon"], durum["batarya"])