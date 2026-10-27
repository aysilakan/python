import simulasyon

komutlar, hatalar = simulasyon.komutlari_oku("paket_ornek/test05/komutlar.txt")

print("DOĞRU KOMUTLAR:")
for k in komutlar:
    print("  ", k)

print("HATALI SATIRLAR:")
for h in hatalar:
    print("  ", h)