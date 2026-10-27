import simulasyon

izgara, baslangic = simulasyon.harita_oku("paket_ornek/test01/harita.txt")
print("Robot burada:", baslangic)
print("Ayarlar:", simulasyon.ayarlari_oku("paket_ornek/test01/ayarlar.json"))

try:
    simulasyon.harita_oku("paket_ornek/test06/harita.txt")
except ValueError as hata:
    print("Hata yakalandı:", hata)