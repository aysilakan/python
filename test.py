import simulasyon

izgara, baslangic = simulasyon.harita_oku("deneme_verileri/veri_1/harita.txt")
print("Başlangıç:", baslangic)
print("Yol:", simulasyon.en_kisa_yol(izgara, baslangic, (3, 2)))
print("Duvara yol:", simulasyon.en_kisa_yol(izgara, baslangic, (0, 0)))
