import json


def harita_oku(dosya_yolu):
    with open(dosya_yolu, encoding="utf-8") as f:
        satirlar= f.read().splitlines()

    satirlar = [s for s in satirlar if s.strip() != ""]
    if len(satirlar)==0:
        raise ValueError("harita dosyası boş")

    izgara= []
    for satir in satirlar:
        izgara.append(list(satir))

    ilk_uzunluk=len(izgara[0])
    for satir in izgara:
        if len(satir) !=ilk_uzunluk:
            raise ValueError("haritada ki satırların uzunlukları farklı")

    robotlar= []
    for y in range(len(izgara)):
        for x in range(len(izgara[y])):
            if izgara[y][x]== "R":
                robotlar.append((x,y))

    if len(robotlar)==0:
        raise ValueError("haritada robot (R) yok")
    if len(robotlar)>1:
        raise ValueError("haritada birden fazla robot (R) var")

    x, y = robotlar[0]
    izgara[y][x]= "."
    return izgara, (x, y)

def ayarlari_oku(dosya_yolu):
    with open (dosya_yolu, encoding="utf-8") as f:
        return json.load(f)



def komutlari_oku(dosya_yolu):
    komutlar = []
    hatalar = []

    with open(dosya_yolu, encoding="utf-8") as f:
        satirlar = f.read().splitlines()

    for satir_no, satir in enumerate(satirlar, start=1):
        parcalar= satir.split()

        if len(parcalar) ==0:
            continue

        komut_adi= parcalar[0]

        if komut_adi== "ILERI":
            if len(parcalar) !=2:
                hatalar.append({"satir": satir_no, "icerik": satir,
                                "neden": "ILERI'den sonra tek bir sayı olmalı"})
                
            elif not parcalar[1].isdigit() or int(parcalar[1])== 0:
                hatalar.append({"satir": satir_no, "icerik": satir,
                                "neden":"adım sayısı pozitif tam sayı olmalı"})
                
            else:
                komutlar.append(("ILERI", int(parcalar[1])))

        elif komut_adi in ["SAG", "SOL", "AL", "BIRAK", "SARJ"]:
            if len(parcalar) !=1:
                hatalar.append({"satir": satir_no, "icerik": satir,
                                "neden": komut_adi + " komutundan sonra bir şey yazılmaz"})

            else:
                komutlar.append((komut_adi, None))

        else:
            hatalar.append({"satir": satir_no, "icerik": satir,
                            "neden": "bilinmeyen komut"})

    return komutlar, hatalar
              