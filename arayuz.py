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


# ===== 3) PENCERE =====
pencere = tk.Tk()
pencere.title("Depo Robotu Simülatörü")

orta = tk.Frame(pencere)
orta.pack(side="top", padx=10, pady=10)

tuval = tk.Canvas(orta, width=480, height=320, bg="#eeeeee")
tuval.pack(side="left")

# --- GECICI DENEME (sonra silinecek) ---
veri["klasor"] = "deneme_verileri/veri_1"
veri["izgara"], veri["baslangic"] = simulasyon.harita_oku(veri["klasor"] + "/harita.txt")
veri["ayarlar"] = simulasyon.ayarlari_oku(veri["klasor"] + "/ayarlar.json")
veri["komutlar"], veri["hatalar"] = simulasyon.komutlari_oku(veri["klasor"] + "/komutlar.txt")
veri["durum"] = simulasyon.yeni_durum(veri["izgara"], veri["baslangic"], veri["ayarlar"])
haritayi_ciz()
# --- GECICI DENEME SONU ---

pencere.mainloop()