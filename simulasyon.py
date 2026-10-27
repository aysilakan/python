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
   
