import csv
import json
import sys


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


        elif komut_adi == "GIT":
            if len(parcalar) != 3 or not parcalar[1].isdigit() or not parcalar[2].isdigit():
                hatalar.append({"satir": satir_no, "icerik": satir,
                                "neden": "GIT'ten sonra iki tane pozitif tam sayı olmalı (x y)"})
            else:
                komutlar.append(("GIT", (int(parcalar[1]), int(parcalar[2]))))

           
        else:
            hatalar.append({"satir": satir_no, "icerik": satir,
                            "neden": "bilinmeyen komut"})

    return komutlar, hatalar



YONLER=["K", "D", "G", "B"]
YON_FARK={"K": (0, -1), "D": (1, 0), "G": (0, 1), "B": (-1, 0)}

def yeni_durum(izgara, baslangic, ayarlar):
    x, y = baslangic
    return{
        "izgara": [satir[:] for satir in izgara],
        "x": x,
        "y": y,
        "yon": ayarlar["baslangic_yonu"],
        "batarya": ayarlar["batarya_kapasitesi"],
        "yuk": False,
        "teslim": 0,
        "carpisma": 0,
        "toplam_adim": 0,
        "bitti": False,
        "ziyaret": {(x, y): 1},
        "ayarlar": ayarlar,
   }


def don(durum, komut_adi):
    maliyet= durum["ayarlar"]["donus_maliyeti"]
    if maliyet> durum["batarya"]:
        durum["bitti"]= True
        return "BATARYA_BITTI"
    sira= YONLER.index(durum["yon"])
    if komut_adi== "SAG":
        sira= (sira + 1) % 4
    else:
        sira =(sira - 1) % 4
    durum["yon"]=   YONLER[sira]
    durum["batarya"] -= maliyet
    return "DONUS"



def al(durum):
    hucre = durum["izgara"][durum["y"]][durum["x"]]
    if hucre =="K" and not durum ["yuk"]:
        durum["yuk"]= True
        durum["izgara"][durum["y"]][durum["x"]]= "."
        return "AL"
    return "GECERSİZ"


def birak(durum):
    if not durum["yuk"]:
        return "GECERSİZ"
    hucre = durum["izgara"][durum["y"]][durum["x"]]
    if hucre == "T":
        durum["yuk"]= False
        durum["teslim"] += 1
        return "TESLIM"
    if hucre == ".":
        durum["yuk"]= "False"
        durum["izgara"][durum["y"]][durum["x"]] = "K"
        return "BIRAK"
    return "GECERSİZ"


def sarj(durum):
    hucre = durum["izgara"][durum["y"]][durum["x"]]
    if hucre == "S":
        durum["batarya"] = durum["ayarlar"]["batarya_kapasitesi"]
        return "SARJ"
    return "GECERSIZ"



def ilerle(durum, n):
    ayarlar = durum["ayarlar"]
    izgara = durum["izgara"]
    dx, dy = YON_FARK[durum["yon"]]

    for _ in range(n):
        yeni_x = durum["x"] + dx
        yeni_y = durum["y"] + dy

        disarida= yeni_y < 0 or yeni_y>= len(izgara) or yeni_x< 0 or yeni_x >= len(izgara[0])
        if disarida or izgara[yeni_y][yeni_x]== "#":
            durum["carpisma"] += 1
            ceza= ayarlar["carpisma_cezasi"]
            if ceza> durum["batarya"]:
                durum["batarya"]= 0
                durum["bitti"]= True
            else:
                durum["batarya"] -= ceza
            return "CARPISMA"

        maliyet= ayarlar["adim_maliyeti"]
        if durum["yuk"]:
            maliyet= maliyet * ayarlar["yuk_carpani"]
        if maliyet> durum["batarya"]:
            durum["bitti"]= True
            return "BATARYA_BITTI"

        durum["x"]= yeni_x
        durum["y"]= yeni_y
        durum["batarya"] -= maliyet
        durum["toplam_adim"] += 1
        konum= (yeni_x, yeni_y)
        durum["ziyaret"][konum] = durum["ziyaret"].get(konum, 0) + 1

    return "HAREKET"



def komut_uygula(durum, komut):
    if durum["bitti"]:
        return "DURDU"
    komut_adi, sayi= komut
    if komut_adi== "ILERI":
        return ilerle(durum, sayi)
    if komut_adi== "SAG" or komut_adi== "SOL":
        return don(durum, komut_adi)
    if komut_adi== "AL":
        return al(durum)
    if komut_adi== "BIRAK":
        return birak(durum)
    if komut_adi== "SARJ":
        return sarj(durum)
    if komut_adi == "GIT":
        return git(durum, sayi)
    return "GECERSİZ"


def en_cok_ziyaret(ziyaret):
    en_iyi= None
    for konum, sayi in ziyaret.items():
        if en_iyi is None:
            en_iyi= konum
            continue
        en_iyi_sayi= ziyaret[en_iyi]
        if sayi> en_iyi_sayi:
            en_iyi= konum
        elif sayi== en_iyi_sayi:
            if (konum[1], konum[0])< (en_iyi[1], en_iyi[0]):
                en_iyi= konum
    return [en_iyi[0], en_iyi[1]]


def komut_metni(komut):
    komut_adi, sayi= komut
    if sayi is None:
        return komut_adi
    if komut_adi == "GIT":
        return "GIT " + str(sayi[0]) + " " + str(sayi[1])
    return komut_adi + " " + str(sayi)
    


def simulasyonu_calistir(izgara, baslangic, komutlar, ayarlar):
    durum= yeni_durum(izgara, baslangic, ayarlar)
    log= []

    for sira, komut in enumerate(komutlar, start=1):
        if durum["bitti"]:
            break
        olay= komut_uygula(durum, komut)
        log.append({
            "adim": sira,
            "komut": komut_metni(komut),
            "x": durum["x"],
            "y": durum["y"],
            "yon": durum["yon"],
            "batarya": durum["batarya"],
            "olay": olay,
        })

    sonuc={
        "konum": [durum["x"], durum["y"]],
        "yon": durum["yon"],
        "batarya": durum["batarya"],
        "yuk": durum["yuk"],
        "teslim": durum["teslim"],
        "carpisma": durum["carpisma"],
        "toplam_adim": durum["toplam_adim"],
        "batarya_bitti": durum["bitti"],
        "en_cok_ziyaret": en_cok_ziyaret(durum["ziyaret"]),

    }
    return sonuc, log

def en_kisa_yol(izgara, baslangic, hedef):
    hx, hy = hedef
    if hy < 0 or hy >= len(izgara) or hx < 0 or hx >= len(izgara[0]):
        return None
    if izgara[hy][hx] == "#":
        return None

    nereden = {baslangic: None}
    kuyruk = [baslangic]

    while len(kuyruk) > 0:
        simdiki = kuyruk.pop(0)
        if simdiki == hedef:
            break
        for yon in YONLER:
            dx, dy = YON_FARK[yon]
            x = simdiki[0] + dx
            y = simdiki[1] + dy
            if y < 0 or y >= len(izgara) or x < 0 or x >= len(izgara[0]):
                continue
            if izgara[y][x] == "#":
                continue
            if (x, y) in nereden:
                continue
            nereden[(x, y)] = simdiki
            kuyruk.append((x, y))

    if hedef not in nereden:
        return None

    yol = []
    kare = hedef
    while kare != baslangic:
        yol.append(kare)
        kare = nereden[kare]
    yol.reverse()
    return yol

def git(durum, hedef):
    yol = en_kisa_yol(durum["izgara"], (durum["x"], durum["y"]), hedef)
    if yol is None:
        return "YOL_YOK"

    for kare in yol:
        dx = kare[0] - durum["x"]
        dy = kare[1] - durum["y"]
        for yon in YONLER:
            if YON_FARK[yon] == (dx, dy):
                istenen = yon

        while durum["yon"] != istenen:
            fark = (YONLER.index(istenen) - YONLER.index(durum["yon"])) % 4
            if fark == 3:
                olay = don(durum, "SOL")
            else:
                olay = don(durum, "SAG")
            if olay != "DONUS":
                return olay

        olay = ilerle(durum, 1)
        if olay != "HAREKET":
            return olay

    return "HAREKET"

def harita_metni(durum):
    oklar = {"K": "^", "D": ">", "G": "v", "B": "<"}
    satirlar = []
    for y in range(len(durum["izgara"])):
        satir = ""
        for x in range(len(durum["izgara"][y])):
            if x == durum["x"] and y == durum["y"]:
                satir += oklar[durum["yon"]]
            else:
                satir += durum["izgara"][y][x]
        satirlar.append(satir)
    return "\n".join(satirlar)



def sonuc_yaz(sonuc, dosya_yolu):
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=2)


def log_yaz(log, dosya_yolu):
    with open(dosya_yolu, "w", encoding="utf-8", newline="") as f:
        yazici = csv.writer(f)
        yazici.writerow(["adim", "komut", "x", "y", "yon", "batarya", "olay"])
        for satir in log:
            yazici.writerow([satir["adim"], satir["komut"], satir["x"], satir["y"],
                             satir["yon"], satir["batarya"], satir["olay"]])



def calistir_ve_kaydet(klasor):
    izgara, baslangic = harita_oku(klasor + "/harita.txt")
    ayarlar = ayarlari_oku(klasor + "/ayarlar.json")
    komutlar, hatalar = komutlari_oku(klasor + "/komutlar.txt")
    sonuc, log = simulasyonu_calistir(izgara, baslangic, komutlar, ayarlar)
    sonuc["hatali_satirlar"] = hatalar
    sonuc_yaz(sonuc, klasor + "/sonuc.json")
    log_yaz(log, klasor + "/log.csv")
    return sonuc


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanim: python simulasyon.py <klasor>")
    else:
        try:
            sonuc = calistir_ve_kaydet(sys.argv[1])
            print("Bitti! sonuc.json ve log.csv yazildi.")
            print("Konum:", sonuc["konum"], "Batarya:", sonuc["batarya"], "Teslim:", sonuc["teslim"])
        except FileNotFoundError as hata:
            print("Dosya bulunamadi:", hata.filename)
        except ValueError as hata:
            print("Harita hatali:", hata)
