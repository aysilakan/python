import tkinter as tk
from tkinter import filedialog, messagebox
import simulasyon

# ===== 1) AYARLAR =====
HUCRE = 40
RENKLER = {"#": "#4a4a4a", ".": "#ffffff", "K": "#a0522d", "T": "#4caf50", "S": "#ffd54f"}
YON_ADLARI = {"K": "Kuzey (yukarı)", "D": "Doğu (sağ)", "G": "Güney (aşağı)", "B": "Batı (sol)"}

veri = {
    "klasor": None,
    "izgara": None,
    "baslangic": None,
    "ayarlar": None,
    "komutlar": [],
    "hatalar": [],
    "durum": None,
    "sira": 0,
    "log": [],
}


# ===== 2) FONKSIYONLAR =====
def haritayi_ciz():
    tuval.delete("all")
    durum = veri["durum"]
    if durum is None:
        return
    izgara = durum["izgara"]
    tuval.config(width=len(izgara[0]) * HUCRE, height=len(izgara) * HUCRE)

    for y in range(len(izgara)):
        for x in range(len(izgara[y])):
            harf = izgara[y][x]
            x1 = x * HUCRE
            y1 = y * HUCRE
            renk = RENKLER.get(harf, "#ffffff")
            tuval.create_rectangle(x1, y1, x1 + HUCRE, y1 + HUCRE, fill=renk, outline="#cccccc")
            if harf in "KTS":
                tuval.create_text(x1 + HUCRE / 2, y1 + HUCRE / 2, text=harf,
                                  fill="black", font=("Arial", 14, "bold"))

    robotu_ciz(durum["x"], durum["y"], durum["yon"], durum["yuk"])


def robotu_ciz(x, y, yon, yuk):
    sol = x * HUCRE + 6
    ust = y * HUCRE + 6
    sag = (x + 1) * HUCRE - 6
    alt = (y + 1) * HUCRE - 6
    orta_x = (sol + sag) / 2
    orta_y = (ust + alt) / 2

    if yon == "K":
        noktalar = [orta_x, ust, sag, alt, sol, alt]
    elif yon == "D":
        noktalar = [sag, orta_y, sol, alt, sol, ust]
    elif yon == "G":
        noktalar = [orta_x, alt, sol, ust, sag, ust]
    else:
        noktalar = [sol, orta_y, sag, ust, sag, alt]

    tuval.create_polygon(noktalar, fill="#1e88e5", outline="#0d47a1", width=2)

    if yuk:
        tuval.create_rectangle(orta_x - 6, orta_y - 6, orta_x + 6, orta_y + 6,
                               fill=RENKLER["K"], outline="black")


def bilgileri_guncelle(son_olay=""):
    durum = veri["durum"]
    if durum is None:
        return
    kapasite = veri["ayarlar"]["batarya_kapasitesi"]
    etiket_batarya.config(text="Batarya: " + str(durum["batarya"]) + " / " + str(kapasite))
    etiket_yon.config(text="Yön: " + YON_ADLARI[durum["yon"]])
    etiket_yuk.config(text="Yük: " + ("Var" if durum["yuk"] else "Yok"))
    etiket_teslim.config(text="Teslim: " + str(durum["teslim"]))
    etiket_carpisma.config(text="Çarpışma: " + str(durum["carpisma"]))

    if durum["bitti"]:
        siradaki = "- (batarya bitti)"
    elif veri["sira"] < len(veri["komutlar"]):
        siradaki = simulasyon.komut_metni(veri["komutlar"][veri["sira"]])
    else:
        siradaki = "- (komutlar bitti)"
    etiket_siradaki.config(text="Sıradaki komut: " + siradaki)
    etiket_ilerleme.config(text="Komut: " + str(veri["sira"]) + " / " + str(len(veri["komutlar"])))
    etiket_log.config(text=son_olay)


def bitti_mi():
    return veri["durum"]["bitti"] or veri["sira"] >= len(veri["komutlar"])


def tek_adim():
    komut = veri["komutlar"][veri["sira"]]
    olay = simulasyon.komut_uygula(veri["durum"], komut)
    veri["sira"] += 1
    durum = veri["durum"]
    veri["log"].append({
        "adim": veri["sira"],
        "komut": simulasyon.komut_metni(komut),
        "x": durum["x"],
        "y": durum["y"],
        "yon": durum["yon"],
        "batarya": durum["batarya"],
        "olay": olay,
    })
    return simulasyon.komut_metni(komut) + "  ->  " + olay


def adim_butonu():
    if veri["durum"] is None:
        messagebox.showwarning("Uyarı", "Önce 'Dosyaları Yükle' ile bir klasör seçin.")
        return
    if bitti_mi():
        messagebox.showinfo("Bilgi", "Simülasyon bitti. Baştan izlemek için 'Sıfırla'ya basın.")
        return
    son_olay = tek_adim()
    haritayi_ciz()
    bilgileri_guncelle(son_olay)
    if bitti_mi():
        sonuclari_kaydet()


def tumunu_calistir_butonu():
    if veri["durum"] is None:
        messagebox.showwarning("Uyarı", "Önce 'Dosyaları Yükle' ile bir klasör seçin.")
        return
    son_olay = ""
    while not bitti_mi():
        son_olay = tek_adim()
    haritayi_ciz()
    bilgileri_guncelle(son_olay)
    sonuclari_kaydet()


def sifirla_butonu():
    if veri["izgara"] is None:
        return
    veri["durum"] = simulasyon.yeni_durum(veri["izgara"], veri["baslangic"], veri["ayarlar"])
    veri["sira"] = 0
    veri["log"] = []
    haritayi_ciz()
    bilgileri_guncelle("Sıfırlandı.")


def sonuclari_kaydet():
    durum = veri["durum"]
    sonuc = {
        "konum": [durum["x"], durum["y"]],
        "yon": durum["yon"],
        "batarya": durum["batarya"],
        "yuk": durum["yuk"],
        "teslim": durum["teslim"],
        "carpisma": durum["carpisma"],
        "toplam_adim": durum["toplam_adim"],
        "batarya_bitti": durum["bitti"],
        "en_cok_ziyaret": simulasyon.en_cok_ziyaret(durum["ziyaret"]),
        "hatali_satirlar": veri["hatalar"],
    }
    try:
        simulasyon.sonuc_yaz(sonuc, veri["klasor"] + "/sonuc.json")
        simulasyon.log_yaz(veri["log"], veri["klasor"] + "/log.csv")
        messagebox.showinfo("Bitti", "Simülasyon bitti.\nsonuc.json ve log.csv klasöre kaydedildi.")
    except OSError as hata:
        messagebox.showerror("Kayıt hatası", "Dosyalar yazılamadı:\n" + str(hata))


# ===== 3) PENCERE =====
pencere = tk.Tk()
pencere.title("Depo Robotu Simülatörü")

butonlar = tk.Frame(pencere)
butonlar.pack(side="top", fill="x", padx=10, pady=10)
tk.Button(butonlar, text="Adım", command=adim_butonu).pack(side="left", padx=4)
tk.Button(butonlar, text="Tümünü Çalıştır", command=tumunu_calistir_butonu).pack(side="left", padx=4)
tk.Button(butonlar, text="Sıfırla", command=sifirla_butonu).pack(side="left", padx=4)

orta = tk.Frame(pencere)
orta.pack(side="top", padx=10, pady=10)

tuval = tk.Canvas(orta, width=480, height=320, bg="#eeeeee")
tuval.pack(side="left")

panel = tk.Frame(orta, padx=15)
panel.pack(side="left", anchor="n")
tk.Label(panel, text="Robot Bilgileri", font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 8))
etiket_batarya = tk.Label(panel, text="Batarya: -", font=("Arial", 11))
etiket_batarya.pack(anchor="w")
etiket_yon = tk.Label(panel, text="Yön: -", font=("Arial", 11))
etiket_yon.pack(anchor="w")
etiket_yuk = tk.Label(panel, text="Yük: -", font=("Arial", 11))
etiket_yuk.pack(anchor="w")
etiket_teslim = tk.Label(panel, text="Teslim: -", font=("Arial", 11))
etiket_teslim.pack(anchor="w")
etiket_carpisma = tk.Label(panel, text="Çarpışma: -", font=("Arial", 11))
etiket_carpisma.pack(anchor="w")
etiket_siradaki = tk.Label(panel, text="Sıradaki komut: -", font=("Arial", 11))
etiket_siradaki.pack(anchor="w", pady=(8, 0))
etiket_ilerleme = tk.Label(panel, text="Komut: -", font=("Arial", 11))
etiket_ilerleme.pack(anchor="w")

etiket_log = tk.Label(pencere, text="Başlamak için 'Dosyaları Yükle'ye basın.", font=("Arial", 11), fg="#333333")
etiket_log.pack(side="top", anchor="w", padx=10, pady=10)

# --- GECICI DENEME (sonra silinecek) ---
veri["klasor"] = "deneme_verileri/veri_1"
veri["izgara"], veri["baslangic"] = simulasyon.harita_oku(veri["klasor"] + "/harita.txt")
veri["ayarlar"] = simulasyon.ayarlari_oku(veri["klasor"] + "/ayarlar.json")
veri["komutlar"], veri["hatalar"] = simulasyon.komutlari_oku(veri["klasor"] + "/komutlar.txt")
veri["durum"] = simulasyon.yeni_durum(veri["izgara"], veri["baslangic"], veri["ayarlar"])
haritayi_ciz()
bilgileri_guncelle("Deneme haritası yüklendi.")
# --- GECICI DENEME SONU ---

pencere.mainloop()