# -*- coding: utf-8 -*-
"""
🐼 PandaCode — kodlardan yapılmış bir pandanın terminali (the terminal of a panda made of code)

Çalıştır :  python pandacode.py
Komutlar :  'help' (ya da 'yardim') yaz  →  ok tuşlarıyla gez, q ile çık
Dil      :  varsayılan İngilizce; 'dil' yazınca Türkçe olur, tekrar yazınca İngilizceye döner
"""
import ast
import base64
import calendar
import codecs
import datetime
import difflib
import getpass
import hashlib
import json
import math
import operator
import os
import platform
import random
import re
import secrets
import shutil
import socket
import statistics
import string
import sys
import textwrap
import time
import uuid
from collections import Counter, deque

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    import select
    import termios
    import tty
    WINDOWS = False

os.system("")  # Windows terminalinde ANSI renklerini açar
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

SURUM = "2.1"

# ═══════════════════════════════ RENKLER ═══════════════════════════════
RESET = "\033[0m"
KALIN = "\033[1m"
SIYAH_YAZI = "\033[30m"
TERS = "\033[7m"
BEYAZ = "\033[97m"
ACIK_GRI = "\033[37m"
GRI = "\033[90m"
KIRMIZI = "\033[91m"
YESIL = "\033[92m"
SARI = "\033[93m"
MAVI = "\033[94m"
MOR = "\033[95m"
CAMGOBEGI = "\033[96m"
GOKKUSAGI = [KIRMIZI, SARI, YESIL, CAMGOBEGI, MAVI, MOR]

TEMALAR = {
    "yesil": ("\033[92m", "\033[32m"),
    "mavi": ("\033[94m", "\033[34m"),
    "mor": ("\033[95m", "\033[35m"),
    "kirmizi": ("\033[91m", "\033[31m"),
    "sari": ("\033[93m", "\033[33m"),
    "camgobegi": ("\033[96m", "\033[36m"),
}
TEMA_ADLARI = {"yesil": "green", "mavi": "blue", "mor": "purple", "kirmizi": "red", "sari": "yellow",
               "camgobegi": "cyan"}  # temaların İngilizce adları


class T:
    """Aktif tema renkleri ('tema' komutuyla değişir)."""
    ANA, KOYU = TEMALAR["yesil"]


# ═══════════════════════════ EKRAN YARDIMCILARI ═══════════════════════════
def ekrani_temizle():
    os.system("cls" if WINDOWS else "clear")


def imlec(gorunsun):
    sys.stdout.write("\033[?25h" if gorunsun else "\033[?25l")
    sys.stdout.flush()


def git(satir, sutun):
    """İmleci ekranda (satır, sütun) konumuna götüren kod (1'den başlar)."""
    return f"\033[{satir};{sutun}H"


def genislik():
    return shutil.get_terminal_size().columns


def yukseklik():
    return shutil.get_terminal_size().lines


def ansi_sil(metin):
    return re.sub(r"\033\[[0-9;?]*[A-Za-z]", "", metin)


def kes(metin, en):
    """Renk kodlarını bozmadan metni 'en' görünür karaktere kırpar."""
    sonuc, sayac = "", 0
    for parca in re.split(r"(\033\[[0-9;?]*[A-Za-z])", metin):
        if parca.startswith("\033"):
            sonuc += parca
        else:
            kalan = max(0, en - sayac)
            sonuc += parca[:kalan]
            sayac += min(len(parca), kalan)
    return sonuc


def yaz(metin, renk=None, hiz=0.012):
    """Metni daktilo gibi harf harf yazar."""
    sys.stdout.write(renk or T.ANA)
    for harf in metin:
        sys.stdout.write(harf)
        sys.stdout.flush()
        time.sleep(hiz)
    print(RESET)


def soyle(metin, renk=None):
    print(f"  {renk or T.ANA}{metin}{RESET}")


def hata(metin):
    print(f"  {KIRMIZI}✗ {metin}{RESET}")


def sor(soru):
    return input(f"  {SARI}{soru}{RESET}").strip()


def kutu(satirlar, baslik="", renk=None):
    """Satırları çerçeveli bir kutu içinde basar."""
    renk = renk or T.ANA
    en = max([len(ansi_sil(s)) for s in satirlar] + [len(baslik) + 2])
    ust = f"─ {baslik} " if baslik else ""
    print(f"  {renk}┌{ust}{'─' * (en + 2 - len(ust))}┐{RESET}")
    for s in satirlar:
        print(f"  {renk}│{RESET} {s}{' ' * (en - len(ansi_sil(s)))} {renk}│{RESET}")
    print(f"  {renk}└{'─' * (en + 2)}┘{RESET}")


def yerinde_yaz(satirlar, ilk_kez):
    """Aynı satırları ekranda kaydırmadan yeniden çizer (canlı paneller için)."""
    if not ilk_kez:
        sys.stdout.write(f"\033[{len(satirlar)}F")
    for s in satirlar:
        sys.stdout.write(s + "\033[K\n")
    sys.stdout.flush()


def cubuk(oran, en=24):
    """Doluluk oranına göre renk değiştiren bir çubuk."""
    oran = min(max(oran, 0), 1)
    dolu = int(round(oran * en))
    renk = YESIL if oran < 0.6 else SARI if oran < 0.85 else KIRMIZI
    return f"{renk}{'█' * dolu}{GRI}{'░' * (en - dolu)}{RESET} {oran * 100:5.1f}%"


def yukleme_cubugu(etiket, sure=1.2):
    uzunluk = 30
    for i in range(uzunluk + 1):
        sys.stdout.write(f"\r  {T.KOYU}{etiket:<26}{T.ANA}[{'█' * i}{'░' * (uzunluk - i)}] "
                         f"{int(i / uzunluk * 100)}%{RESET}")
        sys.stdout.flush()
        time.sleep(sure / uzunluk)
    print()


def terminal_mi():
    return sys.stdin.isatty() and sys.stdout.isatty()


# ═══════════════════════════ DİL: İNGİLİZCE / TÜRKÇE ═══════════════════════════
def dil():
    """Aktif dil: 'en' (varsayılan) ya da 'tr'. 'dil' komutuyla değişir, VERI içinde saklanır."""
    return "tr" if VERI.get("dil") == "tr" else "en"


def tr_en(tr, en):
    """Aktif dile göre Türkçesini ya da İngilizcesini seçer: tr_en("Merhaba", "Hello")"""
    return tr if dil() == "tr" else en


# ═══════════════════════════ TÜRKÇE YARDIMCILARI ═══════════════════════════
TR_SADE = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def sadelestir(metin):
    """'Yardım' → 'yardim' : komutları Türkçe karakterle de yazabilesin diye."""
    return metin.translate(TR_SADE).lower()


def tr_buyuk(metin):
    return metin.replace("i", "İ").replace("ı", "I").upper()


def tr_kucuk(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def buyuk_harf(metin):
    """Dile göre büyük harf: Türkçede 'i' → 'İ', İngilizcede 'i' → 'I'."""
    return tr_buyuk(metin) if dil() == "tr" else metin.upper()


def kucuk_harf(metin):
    return tr_kucuk(metin) if dil() == "tr" else metin.lower()


def sayi(metin):
    """'3,5' ya da '3.5' → 3.5 ; tam sayıysa int döner."""
    deger = float(metin.replace(",", "."))
    return int(deger) if deger.is_integer() else deger


def sayilar(metin):
    """'1 2 3', '1, 2, 3' ya da '1,2,3' → [1, 2, 3]"""
    parcalar = [p.strip(",") for p in re.split(r"[\s;]+", metin) if p.strip(",")]
    if len(parcalar) == 1 and "," in parcalar[0]:
        parcalar = parcalar[0].split(",")
    return [sayi(p) for p in parcalar]


def sure_yaz(saniye):
    saniye = int(saniye)
    gun, saniye = divmod(saniye, 86400)
    saat, saniye = divmod(saniye, 3600)
    dakika, saniye = divmod(saniye, 60)
    birim = tr_en((" gün", " sa", " dk", " sn"), ("d", "h", "m", "s"))
    parcalar = [f"{gun}{birim[0]}" if gun else "", f"{saat}{birim[1]}" if saat else "",
                f"{dakika}{birim[2]}" if dakika else "", f"{saniye}{birim[3]}"]
    return " ".join(p for p in parcalar if p)


def boyut_yaz(bayt):
    for birim in ("B", "KB", "MB", "GB", "TB"):
        if bayt < 1024:
            return f"{bayt:.1f} {birim}"
        bayt /= 1024
    return f"{bayt:.1f} PB"


def binlik(sayi):
    """Binlik ayraç: 12345 → '12.345' (Türkçe) ya da '12,345' (İngilizce)"""
    metin = f"{sayi:,.0f}"
    return tr_en(metin.replace(",", "."), metin)


def cogul(sayi, kelime):
    """İngilizce çoğul eki: cogul(1, 'day') → '1 day', cogul(1500, 'day') → '1,500 days'"""
    return f"{sayi:,} {kelime}{'' if sayi == 1 else 's'}"


GUNLER = {"tr": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
          "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
AYLAR = {"tr": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
                "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
         "en": ["January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"]}


def gun_adi(tarih):
    return GUNLER[dil()][tarih.weekday()]


def ay_adi(ay):
    return AYLAR[dil()][ay - 1]


def tarih_coz(metin):
    for bicim in ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(metin.strip(), bicim).date()
        except ValueError:
            pass
    raise ValueError(tr_en("tarih GG.AA.YYYY şeklinde olmalı", "the date must look like DD.MM.YYYY"))


# ═══════════════════════════ KLAVYE (OK TUŞLARI) ═══════════════════════════
WIN_OKLAR = {"H": "YUKARI", "P": "ASAGI", "K": "SOL", "M": "SAG",
             "I": "PGUP", "Q": "PGDN", "G": "HOME", "O": "END"}
UNIX_OKLAR = {"A": "YUKARI", "B": "ASAGI", "D": "SOL", "C": "SAG", "5~": "PGUP",
              "6~": "PGDN", "H": "HOME", "F": "END", "1~": "HOME", "4~": "END"}


class HamMod:
    """Tuşları Enter beklemeden okuyabilmek için terminali 'ham' moda alır (Linux/macOS)."""

    def __enter__(self):
        self.eski = None
        if not WINDOWS and sys.stdin.isatty():
            self.eski = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, *_):
        if self.eski:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.eski)


def tus_var():
    if WINDOWS:
        return msvcrt.kbhit()
    return bool(select.select([sys.stdin], [], [], 0)[0])


def _unix_karakter():
    return os.read(sys.stdin.fileno(), 1).decode(errors="ignore")


def tus_oku():
    """Bir tuş okur: 'YUKARI', 'ASAGI', 'ENTER', 'ESC'... ya da basılan harf."""
    if WINDOWS:
        tus = msvcrt.getwch()
        if tus in ("\x00", "\xe0"):
            return WIN_OKLAR.get(msvcrt.getwch(), "")
    else:
        tus = _unix_karakter()
        if tus == "\x1b":
            if not select.select([sys.stdin], [], [], 0.05)[0]:
                return "ESC"
            _unix_karakter()  # '[' ya da 'O'
            kod = _unix_karakter()
            while kod[-1:].isdigit():
                kod += _unix_karakter()
            return UNIX_OKLAR.get(kod, "")
    if tus == "\x03":
        raise KeyboardInterrupt
    return {"\r": "ENTER", "\n": "ENTER", "\x1b": "ESC", "\x08": "SIL",
            "\x7f": "SIL", " ": "BOSLUK"}.get(tus, tus)


def tus_bekle(sure):
    """'sure' saniye tuş bekler; basılırsa tuşu, basılmazsa None döndürür."""
    bitis = time.time() + sure
    while time.time() < bitis:
        if tus_var():
            return tus_oku()
        time.sleep(0.01)
    return None


def tuslari_bosalt():
    if WINDOWS:
        while msvcrt.kbhit():
            msvcrt.getwch()
    elif sys.stdin.isatty():
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


class Sahne:
    """Animasyonlar için: imleci gizler, istenirse ayrı bir ekrana geçer, çıkışta her şeyi toparlar."""

    def __init__(self, tam_ekran=False):
        self.tam_ekran = tam_ekran
        self.ham = HamMod()

    def __enter__(self):
        self.ham.__enter__()
        if self.tam_ekran:
            sys.stdout.write("\033[?1049h\033[2J\033[H")
        imlec(False)
        return self

    def __exit__(self, *hata_bilgisi):
        if self.tam_ekran:
            sys.stdout.write("\033[?1049l")
        sys.stdout.write(RESET)
        imlec(True)
        self.ham.__exit__(*hata_bilgisi)
        tuslari_bosalt()


# ═══════════════════════════ KAYITLI VERİLER ═══════════════════════════
KLASOR = os.path.dirname(os.path.abspath(__file__))
VERI_DOSYASI = os.path.join(KLASOR, "pandacode_veri.json")
VERI = {"notlar": [], "tema": "yesil", "isim": "panda", "rekorlar": {}, "dil": "en"}
BASLANGIC = time.time()
GECMIS = []


def veri_yukle():
    try:
        with open(VERI_DOSYASI, encoding="utf-8") as dosya:
            VERI.update(json.load(dosya))
    except (OSError, ValueError):
        pass
    if VERI.get("tema") in TEMALAR:
        T.ANA, T.KOYU = TEMALAR[VERI["tema"]]


def veri_kaydet():
    try:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as dosya:
            json.dump(VERI, dosya, ensure_ascii=False, indent=2)
    except OSError:
        hata(tr_en("Veriler kaydedilemedi.", "Couldn't save your data."))


def rekor_kontrol(oyun, puan, buyuk_iyi=True):
    """Yeni rekorsa kaydeder ve True döner."""
    eski = VERI["rekorlar"].get(oyun)
    if eski is None or (puan > eski if buyuk_iyi else puan < eski):
        VERI["rekorlar"][oyun] = puan
        veri_kaydet()
        return True
    return False


# ═══════════════════════════ KOMUT SİSTEMİ ═══════════════════════════
KATEGORILER = {"Sistem": "System", "Araçlar": "Tools", "Şifreleme": "Ciphers", "Eğlence": "Fun",
               "Görsel Şov": "Visuals", "Oyunlar": "Games", "Öğren": "Learn"}  # Türkçe adı → İngilizce adı
KOMUTLAR = {}
TAKMA_ADLAR = {}


class Cikis(Exception):
    """'cikis' komutu bunu fırlatır, ana döngü de vedalaşıp kapanır."""


def komut(tr_adlar, en_adlar, kategori, tr_aciklama, en_aciklama, tr_kullanim="", en_kullanim=""):
    """Bir fonksiyonu PandaCode komutu olarak kaydeden süsleyici (decorator).

    Adlar boşlukla ayrılır: ilki komutun asıl adı, gerisi takma adlarıdır ("sezar", "caesar").
    Hangi dil seçili olursa olsun Türkçe ve İngilizce adların hepsi çalışır.
    Kullanım sadece argümanları anlatır ("<metin>"); komutun adı başına kendiliğinden eklenir.
    """
    tr_adlar, en_adlar = tr_adlar.split(), en_adlar.split()

    def kaydet(fonksiyon):
        isim = tr_adlar[0]
        KOMUTLAR[isim] = {"fonksiyon": fonksiyon, "kategori": kategori, "ad": (isim, en_adlar[0]),
                          "aciklama": (tr_aciklama, en_aciklama), "kullanim": (tr_kullanim, en_kullanim),
                          "takma": (tr_adlar[1:], en_adlar[1:])}
        for ad in tr_adlar[1:] + en_adlar:
            TAKMA_ADLAR[ad] = isim
        return fonksiyon
    return kaydet


def komut_coz(yazilan):
    """Yazılanı komutun asıl adına çevirir: 'help' → 'yardim', '/Yardım' → 'yardim'"""
    ad = sadelestir(yazilan).lstrip("/")
    return TAKMA_ADLAR.get(ad, ad)


def komut_adi(isim):
    """Komutun aktif dildeki adı: 'yardim' → 'help'"""
    return tr_en(*KOMUTLAR[isim]["ad"])


def komut_aciklamasi(isim):
    return tr_en(*KOMUTLAR[isim]["aciklama"])


def komut_kullanimi(isim):
    return f"{komut_adi(isim)} {tr_en(*KOMUTLAR[isim]['kullanim'])}".strip()


def takma_adlari(isim):
    """Yardımda gösterilen diğer adlar: Türkçede İngilizce adlar da gösterilir, İngilizcede sadece İngilizceler."""
    tr_takma, en_takma = KOMUTLAR[isim]["takma"]
    if dil() == "en":
        return en_takma
    en_ad = KOMUTLAR[isim]["ad"][1]
    return tr_takma + ([en_ad] if en_ad != isim else []) + en_takma


def kategori_adi(kategori):
    return tr_en(kategori, KATEGORILER[kategori])


def kullanim(isim):
    hata(tr_en("Kullanım: ", "Usage: ") + komut_kullanimi(isim))


def cikis_ipucu():
    return tr_en("çıkmak için bir tuşa bas", "press any key to exit")


# ═══════════════════════════ DEV YAZI TİPİ ═══════════════════════════
FONT = {
    "A": " ███ |█   █|█████|█   █|█   █", "B": "████ |█   █|████ |█   █|████ ",
    "C": " ████|█    |█    |█    | ████", "D": "████ |█   █|█   █|█   █|████ ",
    "E": "█████|█    |████ |█    |█████", "F": "█████|█    |████ |█    |█    ",
    "G": " ████|█    |█  ██|█   █| ████", "H": "█   █|█   █|█████|█   █|█   █",
    "I": "███| █ | █ | █ |███", "J": "  ███|   █ |   █ |█  █ | ██  ",
    "K": "█   █|█  █ |███  |█  █ |█   █", "L": "█    |█    |█    |█    |█████",
    "M": "█   █|██ ██|█ █ █|█   █|█   █", "N": "█   █|██  █|█ █ █|█  ██|█   █",
    "O": " ███ |█   █|█   █|█   █| ███ ", "P": "████ |█   █|████ |█    |█    ",
    "Q": " ███ |█   █|█ █ █|█  █ | ██ █", "R": "████ |█   █|████ |█  █ |█   █",
    "S": " ████|█    | ███ |    █|████ ", "T": "█████|  █  |  █  |  █  |  █  ",
    "U": "█   █|█   █|█   █|█   █| ███ ", "V": "█   █|█   █|█   █| █ █ |  █  ",
    "W": "█   █|█   █|█ █ █|██ ██|█   █", "X": "█   █| █ █ |  █  | █ █ |█   █",
    "Y": "█   █| █ █ |  █  |  █  |  █  ", "Z": "█████|   █ |  █  | █   |█████",
    "0": " ███ |█  ██|█ █ █|██  █| ███ ", "1": "  █  | ██  |  █  |  █  | ███ ",
    "2": "████ |    █| ███ |█    |█████", "3": "████ |    █| ███ |    █|████ ",
    "4": "█   █|█   █|█████|    █|    █", "5": "█████|█    |████ |    █|████ ",
    "6": " ███ |█    |████ |█   █| ███ ", "7": "█████|    █|   █ |  █  |  █  ",
    "8": " ███ |█   █| ███ |█   █| ███ ", "9": " ███ |█   █| ████|    █| ███ ",
    " ": "   |   |   |   |   ", "!": "█|█|█| |█", "?": "████ |    █|  ██ |     |  █  ",
    ".": " | | | |█", ",": "  |  |  | █|█ ", ":": " |█| |█| ", "-": "    |    |████|    |    ",
    "+": "     |  █  |█████|  █  |     ", "=": "    |████|    |████|    ",
    "_": "    |    |    |    |████", "/": "    █|   █ |  █  | █   |█    ",
    "<": "  █| █ |█  | █ |  █", ">": "█  | █ |  █| █ |█  ",
    "(": " █|█ |█ |█ | █", ")": "█ | █| █| █|█ ", "'": "█| | | | ",
    "#": " █ █ |█████| █ █ |█████| █ █ ",
}


def buyuk_yazi(metin, renkler=None):
    """Metni 5 satırlık dev harflere çevirir. 'renkler' verilirse her harf başka renk olur."""
    metin = tr_buyuk(metin).translate(str.maketrans("ÇĞİÖŞÜ", "CGIOSU"))
    satirlar = [""] * 5
    for sira, harf in enumerate(metin):
        glif = FONT.get(harf, FONT["?"]).split("|")
        renk = renkler[sira % len(renkler)] if renkler else ""
        for i in range(5):
            satirlar[i] += renk + glif[i] + " "
    return [s + RESET for s in satirlar]


def buyuk_yazi_genisligi(metin):
    metin = tr_buyuk(metin).translate(str.maketrans("ÇĞİÖŞÜ", "CGIOSU"))
    return sum(len(FONT.get(h, FONT["?"]).split("|")[0]) + 1 for h in metin)


# ═══════════════════════════ KODLARDAN PANDA ═══════════════════════════
# '#' = siyah tüy, 'o' = beyaz tüy, 'e' = gözün parıltısı. Her biri kod karakterleriyle doldurulur.
PANDA_KALIBI = r"""
        ####                                  ####
   ##############                        ##############
  ################                      ################
 ##################oooooooooooooooooooo##################
 #############oooooooooooooooooooooooooooooo#############
  ########oooooooooooooooooooooooooooooooooooooo########
     ##oooooooooooooooooooooooooooooooooooooooooooo##
     oooooooooooooooooooooooooooooooooooooooooooooooo
    oooooooooooooooooooooooooooooooooooooooooooooooooo
  oooooooooooooo##########oooooo##########oooooooooooooo
  oooooooooooo####eeee#####oooo#####eeee####oooooooooooo
 oooooooooooo#####eeee#####oooo#####eeee#####oooooooooooo
 ooooooooooo##############oooooo##############ooooooooooo
 oooooooooooo###########oooooooooo###########oooooooooooo
  ooooooooooooo######oooooooooooooooo######ooooooooooooo
  oooooooooooooooooooooooo######oooooooooooooooooooooooo
    oooooooooooooooooooooo######oooooooooooooooooooooo
     ooooooooooooooooooo###oooo###ooooooooooooooooooo
       oooooooooooooooooooooooooooooooooooooooooooo
          oooooooooooooooooooooooooooooooooooooo
              oooooooooooooooooooooooooooooo
                   oooooooooooooooooooo""".strip("\n").splitlines()

# Tüylere doldurulan kodlar: (Türkçe, İngilizce)
SIYAH_KOD = ("while(panda.aç){bambu.ye();}if(kod){çalış();}else{uyu(8);}",
             "while(panda.hungry){bamboo.eat();}if(code){work();}else{sleep(8);}")
BEYAZ_KOD = ("def pandacode():print('merhaba_dünya');return 0x1F43C;import bambu;01101011",
             "def pandacode():print('hello_world');return 0x1F43C;import bamboo;01101011")


def arkaplan(renk):
    """Yazı rengi kodunu arka plan rengine çevirir: 92 (yeşil yazı) → 102 (yeşil zemin)"""
    return re.sub(r"\[(\d+)m", lambda m: f"[{int(m.group(1)) + 10}m", renk)


def panda_satirlari():
    siyah, beyaz = 0, 0
    siyah_kod, beyaz_kod = tr_en(*SIYAH_KOD), tr_en(*BEYAZ_KOD)
    satirlar = []
    for kalip in PANDA_KALIBI:
        satir = ""
        for c in kalip:
            if c == "#":  # siyah tüy: tema renginde blok, kod içine oyulmuş gibi
                satir += arkaplan(T.ANA) + SIYAH_YAZI + siyah_kod[siyah % len(siyah_kod)] + RESET
                siyah += 1
            elif c == "o":
                satir += ACIK_GRI + beyaz_kod[beyaz % len(beyaz_kod)]
                beyaz += 1
            elif c == "e":
                satir += BEYAZ + KALIN + "@" + RESET
            else:
                satir += " "
        satirlar.append(satir + RESET)
    return satirlar


def panda_ciz(animasyonlu=True):
    """Pandayı satır satır 'derlenir' gibi ekrana basar."""
    animasyonlu = animasyonlu and sys.stdout.isatty()
    for satir, kalip in zip(panda_satirlari(), PANDA_KALIBI):
        if animasyonlu:
            karisik = "".join(random.choice("01<>{}[]#$%&*") if c != " " else " " for c in kalip)
            sys.stdout.write(f"  {T.KOYU}{karisik}{RESET}\r")
            sys.stdout.flush()
            time.sleep(0.03)
        print("  " + satir)


MINI_PANDA = r"""
  ▄██▄         ▄██▄
  ████▀▀▀▀▀▀▀▀▀████
   ▀█           █▀
    █  ▄██ ██▄  █
    █  ▀▀   ▀▀  █
    █     ▼     █
     ▀▄  ═══  ▄▀
       ▀▀▀▀▀▀▀""".strip("\n").splitlines()


# ═══════════════════════════ SAYFALI GÖSTERİCİ ═══════════════════════════
def sayfali_goster(satirlar, baslik, bolumler=None):
    """Uzun listeleri ok tuşlarıyla kaydırılabilir tam ekranda gösterir."""
    if not terminal_mi():
        print("\n".join(satirlar))
        return
    bolumler = bolumler or {}
    ust = 0
    with Sahne(tam_ekran=True):
        while True:
            en, boy = genislik(), yukseklik()
            alan = max(3, boy - 4)
            son = max(0, len(satirlar) - alan)
            ust = min(max(0, ust), son)

            cikti = [git(1, 1), f"{T.ANA}{KALIN} 🐼 {baslik}{RESET}\033[K\n",
                     f"{T.KOYU}{'─' * (en - 1)}{RESET}\033[K\n"]
            tutamac_boy = max(1, alan * alan // len(satirlar)) if satirlar else alan
            tutamac_bas = (alan - tutamac_boy) * ust // son if son else 0
            for i in range(alan):
                j = ust + i
                satir = satirlar[j] if j < len(satirlar) else ""
                cikti.append(kes(satir, en - 3) + RESET + "\033[K")
                if son:
                    dolu = tutamac_bas <= i < tutamac_bas + tutamac_boy
                    cikti.append(f"\033[{en - 1}G" + (T.ANA + "█" if dolu else GRI + "│") + RESET)
                cikti.append("\n")
            bitis = min(ust + alan, len(satirlar))
            cikti.append(f"{T.KOYU}{'─' * (en - 1)}{RESET}\033[K")
            ipucu = tr_en("↑↓ kaydır  ←→ sayfa  Home/End  ", "↑↓ scroll  ←→ page  Home/End  ")
            if bolumler:
                ipucu += f"1-{len(bolumler)} " + tr_en("kategori  ", "category  ")
            ipucu += tr_en("q çık", "q quit")
            konum = f"{ust + 1}-{bitis} / {len(satirlar)}"
            cikti.append(git(boy, 1) + kes(f" {GRI}{ipucu}{RESET}   {SARI}{konum}{RESET}", en - 1) + "\033[K")
            sys.stdout.write("".join(cikti))
            sys.stdout.flush()

            tus = tus_oku()
            if tus in ("q", "Q", "ESC"):
                break
            elif tus in ("YUKARI", "w", "k"):
                ust -= 1
            elif tus in ("ASAGI", "s", "j"):
                ust += 1
            elif tus in ("PGUP", "SOL", "a"):
                ust -= alan
            elif tus in ("PGDN", "SAG", "BOSLUK", "d"):
                ust += alan
            elif tus == "ENTER":
                if ust >= son:
                    break
                ust += alan
            elif tus in ("HOME", "g"):
                ust = 0
            elif tus in ("END", "G"):
                ust = son
            elif tus.isdigit() and 1 <= int(tus) <= len(bolumler):
                ust = list(bolumler.values())[int(tus) - 1]


# ═══════════════════════════ KOMUTLAR: SİSTEM ═══════════════════════════
def yardim_satirlari():
    satirlar, bolumler = [], {}
    for sira, kategori in enumerate(KATEGORILER, 1):
        komutlar = [ad for ad, k in KOMUTLAR.items() if k["kategori"] == kategori]
        bolumler[kategori] = len(satirlar)
        baslik = f"[{sira}] {buyuk_harf(kategori_adi(kategori))} ({len(komutlar)} {tr_en('komut', 'commands')}) "
        satirlar.append(f"{SARI}{KALIN}━━ {baslik}{'━' * max(0, 60 - len(baslik))}{RESET}")
        for ad in komutlar:
            takma = f" {GRI}(= {', '.join(takma_adlari(ad))}){RESET}" if takma_adlari(ad) else ""
            satirlar.append(f"   {T.ANA}{komut_kullanimi(ad):<30}{RESET} {komut_aciklamasi(ad)}{takma}")
        satirlar.append("")
    satirlar.append(GRI + tr_en("   İpucu: 'yardim <komut>' o komutun detayını, 'yardim <kelime>' arama sonucunu gösterir.",
                                "   Tip: 'help <command>' shows the details of a command, 'help <word>' searches.") + RESET)
    return satirlar, bolumler


def komut_detayi(ad):
    satirlar = [f"{BEYAZ}{komut_aciklamasi(ad)}{RESET}", "",
                f"{GRI}{tr_en('Kategori :', 'Category :')}{RESET} {kategori_adi(KOMUTLAR[ad]['kategori'])}",
                f"{GRI}{tr_en('Kullanım :', 'Usage    :')}{RESET} {T.ANA}{komut_kullanimi(ad)}{RESET}"]
    if takma_adlari(ad):
        satirlar.append(f"{GRI}{tr_en('Diğer adı:', 'Aliases  :')}{RESET} {', '.join(takma_adlari(ad))}")
    kutu(satirlar, buyuk_harf(komut_adi(ad)))


@komut("yardim komutlar", "help ? commands", "Sistem",
       "Tüm komutları kaydırılabilir listede gösterir", "Shows every command in a scrollable list",
       "[komut|kelime]", "[command|word]")
def k_yardim(arg):
    if not arg:
        satirlar, bolumler = yardim_satirlari()
        sayfali_goster(satirlar, tr_en(f"PANDACODE KOMUTLARI — toplam {len(KOMUTLAR)} komut",
                                       f"PANDACODE COMMANDS — {len(KOMUTLAR)} in total"), bolumler)
        return
    ad = komut_coz(arg.split()[0])
    if ad in KOMUTLAR:
        komut_detayi(ad)
        return
    aranan = sadelestir(arg)
    for kategori, en_kategori in KATEGORILER.items():
        if aranan in (sadelestir(kategori), sadelestir(en_kategori)):
            bulunan = [ad for ad, k in KOMUTLAR.items() if k["kategori"] == kategori]
            break
    else:
        bulunan = [ad for ad, k in KOMUTLAR.items()
                   if any(aranan in sadelestir(metin) for metin in k["ad"] + k["aciklama"])]
    if not bulunan:
        hata(tr_en(f"'{arg}' ile ilgili bir komut bulamadım.", f"I couldn't find any command about '{arg}'."))
        return
    kutu([f"{T.ANA}{komut_kullanimi(ad):<26}{RESET} {komut_aciklamasi(ad)}" for ad in bulunan],
         tr_en(f"'{arg}' için {len(bulunan)} sonuç", f"{cogul(len(bulunan), 'result')} for '{arg}'"))


@komut("temizle", "clear cls", "Sistem", "Ekranı temizler", "Clears the screen")
def k_temizle(arg):
    ekrani_temizle()
    print(f"  {T.ANA}{KALIN}🐼 PandaCode{RESET} {GRI}— "
          + tr_en("komutlar için 'yardim' yaz", "type 'help' for commands") + f"{RESET}\n")


@komut("cikis", "exit quit q", "Sistem", "PandaCode'u kapatır", "Closes PandaCode")
def k_cikis(arg):
    raise Cikis


def cpu_zamanlari():
    """(boşta geçen, toplam) işlemci zamanı; bulunamazsa None."""
    try:
        if WINDOWS:
            import ctypes

            class Zaman(ctypes.Structure):
                _fields_ = [("dusuk", ctypes.c_uint32), ("yuksek", ctypes.c_uint32)]

            bos, cekirdek, kullanici = Zaman(), Zaman(), Zaman()
            ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(bos), ctypes.byref(cekirdek),
                                                  ctypes.byref(kullanici))
            deger = lambda z: (z.yuksek << 32) | z.dusuk
            return deger(bos), deger(cekirdek) + deger(kullanici)  # çekirdek zamanı boşu da içerir
        with open("/proc/stat") as dosya:
            parcalar = [int(p) for p in dosya.readline().split()[1:]]
        return parcalar[3] + parcalar[4], sum(parcalar)
    except (OSError, AttributeError, IndexError, ValueError):
        return None


def ram_bilgisi():
    """(toplam, kullanılan) bayt; bulunamazsa None."""
    try:
        if WINDOWS:
            import ctypes

            class Bellek(ctypes.Structure):
                _fields_ = [("uzunluk", ctypes.c_ulong), ("yuk", ctypes.c_ulong),
                            ("toplam", ctypes.c_ulonglong), ("bos", ctypes.c_ulonglong)] + \
                           [(f"x{i}", ctypes.c_ulonglong) for i in range(5)]

            bellek = Bellek()
            bellek.uzunluk = ctypes.sizeof(Bellek)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(bellek))
            return bellek.toplam, bellek.toplam - bellek.bos
        bilgi = {}
        with open("/proc/meminfo") as dosya:
            for satir in dosya:
                ad, deger = satir.split(":")
                bilgi[ad] = int(deger.split()[0]) * 1024
        return bilgi["MemTotal"], bilgi["MemTotal"] - bilgi.get("MemAvailable", bilgi["MemFree"])
    except (OSError, AttributeError, KeyError, ValueError):
        return None


def islemci_adi():
    if WINDOWS:
        try:
            import winreg
            anahtar = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            return winreg.QueryValueEx(anahtar, "ProcessorNameString")[0].strip()
        except OSError:
            pass
    return platform.processor() or platform.machine()


def acik_kalma_suresi():
    try:
        if WINDOWS:
            import ctypes
            ctypes.windll.kernel32.GetTickCount64.restype = ctypes.c_ulonglong
            return ctypes.windll.kernel32.GetTickCount64() / 1000
        with open("/proc/uptime") as dosya:
            return float(dosya.read().split()[0])
    except (OSError, AttributeError, ValueError):
        return None


@komut("sistem", "system sys neofetch", "Sistem",
       "İşletim sistemi, CPU, RAM, disk ve saati CANLI gösterir", "Shows the OS, CPU, RAM, disk and time LIVE")
def k_sistem(arg):
    etiket = lambda tr, en: f"{GRI}{tr_en(tr, en):<11}:{RESET}"
    cekirdek = tr_en(f"{os.cpu_count()} çekirdek", cogul(os.cpu_count() or 0, "core"))
    sabit = [
        f"{etiket('Sistem', 'System')} {platform.system()} {platform.release()} ({platform.machine()})",
        f"{etiket('Bilgisayar', 'Computer')} {socket.gethostname()}",
        f"{etiket('İşlemci', 'Processor')} {islemci_adi()[:48]} — {cekirdek}",
        f"{etiket('Python', 'Python')} {platform.python_version()}",
    ]
    onceki = cpu_zamanlari()
    ilk = True
    with Sahne():
        while True:
            simdi = cpu_zamanlari()
            if onceki and simdi and simdi[1] != onceki[1]:
                cpu = f"{cubuk(1 - (simdi[0] - onceki[0]) / (simdi[1] - onceki[1]))}"
            else:
                cpu = f"{GRI}{tr_en('ölçülüyor...', 'measuring...')}{RESET}"
            onceki = simdi
            ram = ram_bilgisi()
            ram_satiri = (f"{cubuk(ram[1] / ram[0])} {GRI}{boyut_yaz(ram[1])} / {boyut_yaz(ram[0])}{RESET}"
                          if ram else f"{GRI}{tr_en('bilinmiyor', 'unknown')}{RESET}")
            disk = shutil.disk_usage(os.path.abspath(os.sep))
            acik = acik_kalma_suresi()
            baslik = tr_en("SİSTEM PANELİ", "SYSTEM PANEL")
            satirlar = [f"  {T.ANA}{KALIN}╔═ 🐼 {baslik} {'═' * (38 - len(baslik))}{RESET}"]
            satirlar += [f"  {T.ANA}║{RESET} {s}" for s in sabit]
            satirlar += [
                f"  {T.ANA}║{RESET} {etiket('CPU', 'CPU')} {cpu}",
                f"  {T.ANA}║{RESET} {etiket('RAM', 'RAM')} {ram_satiri}",
                f"  {T.ANA}║{RESET} {etiket('Disk', 'Disk')} {cubuk(disk.used / disk.total)} "
                f"{GRI}{boyut_yaz(disk.free)} {tr_en('boş', 'free')}{RESET}",
                f"  {T.ANA}║{RESET} {etiket('Açık kalma', 'Uptime')} {sure_yaz(acik) if acik else '?'}",
                f"  {T.ANA}║{RESET} {etiket('Saat', 'Time')} {BEYAZ}{KALIN}{time.strftime('%H:%M:%S')}{RESET}  "
                f"{time.strftime('%d.%m.%Y')} {gun_adi(datetime.date.today())}",
                f"  {T.ANA}{KALIN}╚═ {cikis_ipucu()} {'═' * (43 - len(cikis_ipucu()))}{RESET}",
            ]
            yerinde_yaz(satirlar, ilk)
            ilk = False
            if not terminal_mi() or tus_bekle(0.7):
                break


@komut("saat", "time", "Sistem", "Şu anki saati gösterir", "Shows the current time")
def k_saat(arg):
    soyle(f"🕒 {BEYAZ}{KALIN}{time.strftime('%H:%M:%S')}")


@komut("tarih", "date", "Sistem", "Bugünün tarihini ve yılın kaçıncı günü olduğunu gösterir",
       "Shows today's date and which day of the year it is")
def k_tarih(arg):
    bugun = datetime.date.today()
    yil_gunu = bugun.timetuple().tm_yday
    yil_uzunlugu = 366 if calendar.isleap(bugun.year) else 365
    hafta, biten = bugun.isocalendar()[1], yil_gunu / yil_uzunlugu * 100
    soyle(f"📅 {BEYAZ}{KALIN}" + tr_en(f"{bugun.day} {ay_adi(bugun.month)} {bugun.year}, {gun_adi(bugun)}",
                                      f"{gun_adi(bugun)}, {bugun.day} {ay_adi(bugun.month)} {bugun.year}"))
    soyle(tr_en(f"Yılın {yil_gunu}. günü, {hafta}. haftası. Yılın %{biten:.1f}'i bitti.",
                f"Day {yil_gunu} of the year, week {hafta}. {biten:.1f}% of the year is done."), GRI)


@komut("takvim", "calendar cal", "Sistem", "Aylık takvim gösterir (bugün işaretli)",
       "Shows a monthly calendar (today is highlighted)", "[ay] [yıl]", "[month] [year]")
def k_takvim(arg):
    bugun = datetime.date.today()
    ay, yil = bugun.month, bugun.year
    try:
        parcalar = [int(p) for p in arg.split()]
        if parcalar:
            ay = parcalar[0]
        if len(parcalar) > 1:
            yil = parcalar[1]
        if not 1 <= ay <= 12:
            raise ValueError
    except ValueError:
        kullanim("takvim")
        return
    print(f"\n  {T.ANA}{KALIN}{(ay_adi(ay) + ' ' + str(yil)).center(20)}{RESET}")
    print(f"  {SARI}{tr_en('Pt Sa Ça Pe Cu', 'Mo Tu We Th Fr')} {KIRMIZI}{tr_en('Ct Pz', 'Sa Su')}{RESET}")
    for hafta in calendar.monthcalendar(yil, ay):
        satir = ""
        for i, gun in enumerate(hafta):
            if gun == 0:
                satir += "   "
            elif (gun, ay, yil) == (bugun.day, bugun.month, bugun.year):
                satir += f"{TERS}{T.ANA}{gun:>2}{RESET} "
            else:
                satir += f"{KIRMIZI if i >= 5 else BEYAZ}{gun:>2}{RESET} "
        print("  " + satir)
    print()


@komut("oturum", "session uptime", "Sistem", "PandaCode ne zamandır açık, kaç komut yazdın",
       "How long PandaCode has been open and how many commands you typed")
def k_oturum(arg):
    sure = sure_yaz(time.time() - BASLANGIC)
    soyle(tr_en(f"⏱  Oturum süresi: {BEYAZ}{sure}{T.ANA}, yazılan komut: {BEYAZ}{len(GECMIS)}",
                f"⏱  Session time: {BEYAZ}{sure}{T.ANA}, commands typed: {BEYAZ}{len(GECMIS)}"))


@komut("gecmis", "history", "Sistem", "Bu oturumda yazdığın komutları listeler",
       "Lists the commands you typed this session")
def k_gecmis(arg):
    if not GECMIS:
        soyle(tr_en("Henüz komut yazmadın.", "You haven't typed any commands yet."), GRI)
        return
    for i, satir in enumerate(GECMIS[-30:], max(1, len(GECMIS) - 29)):
        print(f"  {GRI}{i:>3}{RESET}  {satir}")


@komut("tekrar", "repeat !!", "Sistem", "Son komutu tekrar çalıştırır", "Runs the last command again")
def k_tekrar(arg):
    if not GECMIS:
        hata(tr_en("Tekrarlanacak komut yok.", "There's no command to repeat."))
        return
    soyle(f"↻ {GECMIS[-1]}", GRI)
    calistir(GECMIS[-1])


@komut("dizin", "pwd", "Sistem", "Şu an hangi klasörde olduğunu gösterir", "Shows which folder you're in")
def k_dizin(arg):
    soyle(f"📁 {os.getcwd()}", BEYAZ)


@komut("listele", "ls dir", "Sistem", "Klasördeki dosyaları boyutlarıyla listeler",
       "Lists the files in a folder with their sizes", "[klasör]", "[folder]")
def k_listele(arg):
    yol = arg or "."
    try:
        ogeler = sorted(os.scandir(yol), key=lambda o: (not o.is_dir(), o.name.lower()))
    except OSError as e:
        hata(tr_en(f"Açılamadı: {e.strerror}", f"Couldn't open it: {e.strerror}"))
        return
    for oge in ogeler[:60]:
        if oge.is_dir():
            print(f"  {MAVI}{KALIN}📁 {oge.name}/{RESET}")
        else:
            try:
                boyut = boyut_yaz(oge.stat().st_size)
            except OSError:
                boyut = "?"
            print(f"  📄 {oge.name:<40} {GRI}{boyut:>10}{RESET}")
    if len(ogeler) > 60:
        soyle(tr_en(f"... ve {len(ogeler) - 60} öğe daha", f"... and {len(ogeler) - 60} more"), GRI)
    soyle(tr_en(f"Toplam {len(ogeler)} öğe.", f"{cogul(len(ogeler), 'item')} in total."), GRI)


@komut("disk", "disk", "Sistem", "Disk doluluğunu gösterir", "Shows how full the disk is")
def k_disk(arg):
    disk = shutil.disk_usage(os.path.abspath(os.sep))
    soyle(f"💾 {cubuk(disk.used / disk.total, 30)}")
    toplam, dolu, bos = boyut_yaz(disk.total), boyut_yaz(disk.used), boyut_yaz(disk.free)
    soyle(tr_en(f"Toplam {toplam}  •  Dolu {dolu}  •  Boş {bos}", f"Total {toplam}  •  Used {dolu}  •  Free {bos}"), GRI)


@komut("ip", "ip", "Sistem", "Bilgisayarın yerel ağ (IP) adresini gösterir", "Shows the computer's local network (IP) address")
def k_ip(arg):
    soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soket.connect(("10.255.255.255", 1))  # paket gönderilmez, sadece hangi ağ kartı kullanılır diye bakar
        ip = soket.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        soket.close()
    soyle(tr_en(f"🌐 Yerel IP: {BEYAZ}{KALIN}{ip}{RESET}   {GRI}Bilgisayar adı: {socket.gethostname()}",
                f"🌐 Local IP: {BEYAZ}{KALIN}{ip}{RESET}   {GRI}Computer name: {socket.gethostname()}"))


@komut("kullanici", "whoami", "Sistem", "Oturum açmış kullanıcıyı gösterir", "Shows the logged-in user")
def k_kullanici(arg):
    soyle(f"👤 {BEYAZ}{getpass.getuser()}{T.ANA} @ {socket.gethostname()}  {GRI}"
          + tr_en(f"(PandaCode'daki adın: {VERI['isim']})", f"(your PandaCode name: {VERI['isim']})"))


@komut("tema renk", "theme", "Sistem", "Terminalin rengini değiştirir (kalıcı)", "Changes the terminal's color (saved)",
       "[renk adı]", "[color name]")
def k_tema(arg):
    secim = sadelestir(arg)
    secim = next((ad for ad, en_ad in TEMA_ADLARI.items() if en_ad == secim), secim)  # 'purple' → 'mor'
    if secim not in TEMALAR:
        if arg:
            hata(tr_en(f"'{arg}' diye bir tema yok.", f"There's no theme called '{arg}'."))
        for ad, (ana, koyu) in TEMALAR.items():
            isaret = tr_en(" ◀ şu an", " ◀ current") if ad == VERI["tema"] else ""
            print(f"  {ana}{KALIN}██{RESET}{koyu}██{RESET}  {ana}{tr_en(ad, TEMA_ADLARI[ad])}{RESET}{GRI}{isaret}{RESET}")
        soyle(tr_en("Örnek: tema mor", "Example: theme purple"), GRI)
        return
    T.ANA, T.KOYU = TEMALAR[secim]
    VERI["tema"] = secim
    veri_kaydet()
    ad = tr_en(secim, TEMA_ADLARI[secim])
    soyle(tr_en(f"🎨 Tema '{ad}' oldu! Panda yeni rengini beğendi.", f"🎨 The theme is now '{ad}'! The panda loves its new color."))


@komut("isim", "name nick", "Sistem", "Komut satırındaki adını değiştirir (kalıcı)",
       "Changes your name in the prompt (saved)", "<yeni ad>", "<new name>")
def k_isim(arg):
    if not arg:
        kullanim("isim")
        return
    VERI["isim"] = re.sub(r"\s+", "_", arg)[:16]
    veri_kaydet()
    soyle(tr_en(f"Tamamdır, artık sen {BEYAZ}{KALIN}{VERI['isim']}{RESET}{T.ANA}'sın! 🐼",
                f"Done, from now on you're {BEYAZ}{KALIN}{VERI['isim']}{RESET}{T.ANA}! 🐼"))


@komut("dil", "lang language", "Sistem", "Dili değiştirir: Türkçe ↔ İngilizce (kalıcı)",
       "Switches the language: English ↔ Turkish (saved)", "[tr|en]", "[en|tr]")
def k_dil(arg):
    diller = {"tr": "tr", "turkce": "tr", "turkish": "tr", "en": "en", "ingilizce": "en", "english": "en"}
    secim = sadelestir(arg)
    if secim and secim not in diller:
        kullanim("dil")
        return
    VERI["dil"] = diller.get(secim, "en" if dil() == "tr" else "tr")  # boş yazılırsa öbür dile geçer
    veri_kaydet()
    soyle(tr_en("🌐 Dil: Türkçe. İngilizce için tekrar 'dil' yaz.", "🌐 Language: English. Type 'lang' again for Turkish."))


@komut("hakkinda surum", "about version", "Sistem", "PandaCode hakkında bilgi", "About PandaCode")
def k_hakkinda(arg):
    bilgiler = [(tr_en("Komut sayısı", "Commands"), len(KOMUTLAR)),
                (tr_en("Kategoriler", "Categories"), ", ".join(kategori_adi(k) for k in KATEGORILER)),
                (tr_en("Dil", "Language"), tr_en("Türkçe", "English")),
                (tr_en("Veri dosyası", "Data file"), "pandacode_veri.json"),
                (tr_en("Geçmişi", "History"), tr_en("PandaHack v1.0'dan evrildi", "Evolved from PandaHack v1.0"))]
    kutu([f"{T.ANA}{KALIN}PandaCode v{SURUM}{RESET}",
          tr_en("Kodlardan yapılmış bir pandanın terminali.", "The terminal of a panda made of code."),
          ""] + [f"{GRI}{ad:<13}:{RESET} {deger}" for ad, deger in bilgiler] +
         ["", SARI + tr_en("Kodla, öğren, bambu ye. 🎋", "Code, learn, eat bamboo. 🎋") + RESET], tr_en("HAKKINDA", "ABOUT"))


@komut("istatistik", "stats", "Sistem", "En çok kullandığın komutları gösterir", "Shows the commands you use the most")
def k_istatistik(arg):
    if not GECMIS:
        soyle(tr_en("Henüz istatistik yok, biraz komut yaz!", "No stats yet, type some commands!"), GRI)
        return
    sayac = Counter(komut_coz(s.split()[0]) for s in GECMIS)
    en_cok = sayac.most_common(1)[0][1]
    for ad, adet in sayac.most_common(8):
        print(f"  {T.ANA}{komut_adi(ad):<12}{RESET} {'█' * max(1, adet * 25 // en_cok)} {GRI}{adet}{RESET}")


@komut("python", "python py", "Sistem", "Python sürümünü ve yerini gösterir", "Shows the Python version and where it lives")
def k_python(arg):
    soyle(f"🐍 Python {BEYAZ}{platform.python_version()}{T.ANA} ({platform.python_implementation()})")
    soyle(sys.executable, GRI)


@komut("ekran", "screen", "Sistem", "Terminal penceresinin boyutunu gösterir", "Shows the size of the terminal window")
def k_ekran(arg):
    soyle(tr_en(f"🖥  {genislik()} sütun × {yukseklik()} satır", f"🖥  {genislik()} columns × {yukseklik()} rows"))


# ═══════════════════════════ KOMUTLAR: ARAÇLAR ═══════════════════════════
HESAP_ISLEMLERI = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                   ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
                   ast.Mod: operator.mod, ast.Pow: operator.pow}
HESAP_SABITLERI = {"pi": math.pi, "e": math.e, "tau": math.tau}
HESAP_FONKSIYONLARI = {
    "kok": math.sqrt, "sqrt": math.sqrt, "abs": abs, "mutlak": abs, "round": round, "yuvarla": round,
    "sin": lambda x: math.sin(math.radians(x)), "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)), "log": math.log10, "ln": math.log,
    "floor": math.floor, "ceil": math.ceil, "max": max, "min": min,
}


def hesap_coz(dugum):
    """Sadece matematiğe izin veren güvenli hesaplayıcı (eval kullanmaz)."""
    if isinstance(dugum, ast.Constant) and type(dugum.value) in (int, float):
        return dugum.value
    if isinstance(dugum, ast.BinOp) and type(dugum.op) in HESAP_ISLEMLERI:
        sol, sag = hesap_coz(dugum.left), hesap_coz(dugum.right)
        if isinstance(dugum.op, ast.Pow) and abs(sag) > 1000:
            raise ValueError(tr_en("üs çok büyük, bilgisayarı yakmayalım", "the exponent is too big, let's not fry the computer"))
        return HESAP_ISLEMLERI[type(dugum.op)](sol, sag)
    if isinstance(dugum, ast.UnaryOp) and isinstance(dugum.op, (ast.USub, ast.UAdd)):
        deger = hesap_coz(dugum.operand)
        return -deger if isinstance(dugum.op, ast.USub) else deger
    if isinstance(dugum, ast.Name) and dugum.id in HESAP_SABITLERI:
        return HESAP_SABITLERI[dugum.id]
    if (isinstance(dugum, ast.Call) and isinstance(dugum.func, ast.Name)
            and dugum.func.id in HESAP_FONKSIYONLARI and not dugum.keywords):
        return HESAP_FONKSIYONLARI[dugum.func.id](*[hesap_coz(a) for a in dugum.args])
    raise ValueError(tr_en("bunu anlayamadım", "I couldn't understand that"))


def sayi_bicimle(deger):
    if isinstance(deger, float):
        if deger.is_integer() and abs(deger) < 1e15:
            return str(int(deger))
        return f"{deger:.10g}"
    metin = str(deger)
    return metin if len(metin) <= 60 else f"{metin[:25]}... ({len(metin.lstrip('-'))} {tr_en('basamak', 'digits')})"


@komut("hesapla", "calc calculate =", "Araçlar", "Matematik işlemi çözer: + - * / ^ % kok() sin() log() pi",
       "Solves math: + - * / ^ % sqrt() sin() log() pi", "<işlem>", "<expression>")
def k_hesapla(arg):
    if not arg:
        kullanim("hesapla")
        soyle(tr_en("Örnek: hesapla (3+4)*2^3   •   hesapla kok(144)   •   hesapla sin(30)",
                    "Example: calc (3+4)*2^3   •   calc sqrt(144)   •   calc sin(30)"), GRI)
        return
    ifade = arg.replace("^", "**").replace("×", "*").replace("÷", "/")
    try:
        sonuc = hesap_coz(ast.parse(ifade, mode="eval").body)
    except ZeroDivisionError:
        hata(tr_en("Sıfıra bölme! Evren az kalsın çöküyordu. 🌌", "Division by zero! The universe almost collapsed. 🌌"))
        return
    except (SyntaxError, ValueError, TypeError, OverflowError) as e:
        hata(tr_en(f"Hesaplayamadım: {e}", f"Couldn't calculate that: {e}"))
        return
    if isinstance(sonuc, complex):
        hata(tr_en("Sonuç karmaşık sayı çıktı, o işler biraz ileri seviye. 😅",
                   "The result is a complex number, that's a bit too advanced for me. 😅"))
        return
    soyle(f"{GRI}{arg} ={RESET} {BEYAZ}{KALIN}{sayi_bicimle(sonuc)}")


def sifre_olustur(uzunluk):
    havuzlar = [string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%&*?-_+="]
    tumu = "".join(havuzlar)
    karakterler = [secrets.choice(h) for h in havuzlar] + [secrets.choice(tumu) for _ in range(uzunluk - 4)]
    random.SystemRandom().shuffle(karakterler)
    return "".join(karakterler)


def sifre_puanla(sifre):
    havuz = 0
    for desen, boyut in ((r"[a-zçğıöşü]", 26), (r"[A-ZÇĞİÖŞÜ]", 26), (r"\d", 10), (r"[^\w]|_", 33)):
        if re.search(desen, sifre):
            havuz += boyut
    entropi = len(sifre) * math.log2(havuz) if havuz else 0
    yaygin = {"123456", "12345678", "123456789", "password", "sifre", "parola", "qwerty", "111111",
              "abc123", "iloveyou", "admin", "galatasaray", "fenerbahce", "besiktas", "trabzonspor"}
    if sifre.lower() in yaygin or len(set(sifre)) <= 2:
        entropi = min(entropi, 5)
    return entropi


def kirilma_suresi(entropi):
    saniye = 2 ** entropi / 1e10  # saniyede 10 milyar deneme yapan güçlü bir bilgisayar
    for sinir, bolen, birim, en_birim in ((1, 1, "anında", ""), (60, 1, "saniye", "second"),
                                          (3600, 60, "dakika", "minute"), (86400, 3600, "saat", "hour"),
                                          (31536000, 86400, "gün", "day"), (31536000 * 1.4e10, 31536000, "yıl", "year")):
        if saniye < sinir:
            if not en_birim:
                return tr_en("anında 💥", "instantly 💥")
            deger = round(saniye / bolen)
            return tr_en(f"{binlik(deger)} {birim}", cogul(deger, en_birim))
    return tr_en("evrenin yaşından uzun 🌌", "longer than the age of the universe 🌌")


@komut("sifre sifreuret", "password", "Araçlar", "Gerçekten güçlü, rastgele bir şifre üretir",
       "Generates a truly strong random password", "[uzunluk]", "[length]")
def k_sifre(arg):
    try:
        uzunluk = int(arg) if arg else 16
    except ValueError:
        kullanim("sifre")
        return
    uzunluk = min(max(uzunluk, 6), 128)
    sifre = sifre_olustur(uzunluk)
    soyle(f"🔑 {BEYAZ}{KALIN}{sifre}")
    sure = kirilma_suresi(sifre_puanla(sifre))
    soyle(tr_en(f"{uzunluk} karakter • kırılma süresi: {sure}", f"{uzunluk} characters • time to crack: {sure}"), GRI)


@komut("sifreguc sifrekontrol", "pwcheck", "Araçlar",
       "Bir şifrenin ne kadar sağlam olduğunu ölçer (boş bırakırsan gizli yazarsın)",
       "Measures how strong a password is (leave it empty to type it hidden)", "[şifre]", "[password]")
def k_sifreguc(arg):
    sifre = arg or getpass.getpass(f"  {SARI}{tr_en('Şifre (ekranda görünmez): ', 'Password (hidden): ')}{RESET}")
    if not sifre:
        return
    entropi = sifre_puanla(sifre)
    seviyeler = [(28, tr_en("ÇOK ZAYIF", "VERY WEAK"), KIRMIZI), (36, tr_en("ZAYIF", "WEAK"), KIRMIZI),
                 (60, tr_en("ORTA", "MEDIUM"), SARI), (80, tr_en("GÜÇLÜ", "STRONG"), YESIL),
                 (float("inf"), tr_en("ÇOK GÜÇLÜ", "VERY STRONG"), CAMGOBEGI)]
    ad, renk = next((a, r) for s, a, r in seviyeler if entropi < s)
    dolu = min(20, int(entropi / 5))
    soyle(f"{renk}{'█' * dolu}{GRI}{'░' * (20 - dolu)}{RESET}  {renk}{KALIN}{ad}{RESET}")
    soyle(tr_en(f"Tahmini kırılma süresi: {kirilma_suresi(entropi)}", f"Estimated time to crack: {kirilma_suresi(entropi)}"), BEYAZ)
    tavsiyeler = []
    if len(sifre) < 12:
        tavsiyeler.append(tr_en("En az 12 karakter kullan", "Use at least 12 characters"))
    if not re.search(r"[A-Z]", sifre):
        tavsiyeler.append(tr_en("Büyük harf ekle", "Add uppercase letters"))
    if not re.search(r"\d", sifre):
        tavsiyeler.append(tr_en("Rakam ekle", "Add numbers"))
    if not re.search(r"[^\w]", sifre):
        tavsiyeler.append(tr_en("!@#$ gibi sembol ekle", "Add symbols like !@#$"))
    for tavsiye in tavsiyeler:
        soyle(f"💡 {tavsiye}", GRI)


@komut("not", "note", "Araçlar", "Hızlı not alır (kapatsan da kaybolmaz)", "Takes a quick note (it stays even after you quit)",
       "<metin>", "<text>")
def k_not(arg):
    if not arg:
        kullanim("not")
        return
    VERI["notlar"].append({"metin": arg, "tarih": time.strftime("%d.%m.%Y %H:%M")})
    veri_kaydet()
    soyle(tr_en(f"📝 Not #{len(VERI['notlar'])} kaydedildi.", f"📝 Note #{len(VERI['notlar'])} saved."))


@komut("notlar", "notes", "Araçlar", "Aldığın notları listeler", "Lists your notes")
def k_notlar(arg):
    if not VERI["notlar"]:
        soyle(tr_en("Hiç notun yok. 'not <metin>' ile ekleyebilirsin.", "You have no notes yet. Add one with 'note <text>'."), GRI)
        return
    kutu([f"{T.ANA}{i:>2}.{RESET} {n['metin']}  {GRI}({n['tarih']}){RESET}"
          for i, n in enumerate(VERI["notlar"], 1)], tr_en("NOTLAR", "NOTES") + f" ({len(VERI['notlar'])})")


@komut("notsil", "delnote", "Araçlar", "Bir notu ya da tüm notları siler", "Deletes one note or all of them",
       "<no|hepsi>", "<number|all>")
def k_notsil(arg):
    if sadelestir(arg) in ("hepsi", "all"):
        if sadelestir(sor(tr_en("Tüm notlar silinsin mi? (e/h): ", "Delete all notes? (y/n): "))) in ("e", "evet", "y", "yes"):
            VERI["notlar"].clear()
            veri_kaydet()
            soyle(tr_en("🗑  Tüm notlar silindi.", "🗑  All notes deleted."))
        return
    try:
        silinen = VERI["notlar"].pop(int(arg) - 1)
    except (ValueError, IndexError):
        kullanim("notsil")
        return
    veri_kaydet()
    soyle(tr_en(f"🗑  Silindi: {silinen['metin']}", f"🗑  Deleted: {silinen['metin']}"))


@komut("uuid", "uuid", "Araçlar", "Benzersiz bir kimlik (UUID) üretir", "Generates a unique ID (UUID)")
def k_uuid(arg):
    soyle(f"🆔 {BEYAZ}{uuid.uuid4()}")


@komut("rastgele", "random", "Araçlar", "İki sayı arasında rastgele sayı seçer", "Picks a random number between two numbers",
       "[en_az] [en_çok]", "[min] [max]")
def k_rastgele(arg):
    try:
        sinirlar = [int(p) for p in arg.split()] or [1, 100]
        alt, ust = (1, sinirlar[0]) if len(sinirlar) == 1 else sorted(sinirlar[:2])
    except ValueError:
        kullanim("rastgele")
        return
    soyle(tr_en(f"🎰 {alt}-{ust} arası: ", f"🎰 Between {alt} and {ust}: ") + f"{BEYAZ}{KALIN}{random.randint(alt, ust)}")


@komut("sec karar", "pick", "Araçlar", "Kararsız kaldığında senin yerine seçer", "Chooses for you when you can't decide",
       "<a, b, c>", "<a, b, c>")
def k_sec(arg):
    secenekler = [s.strip() for s in (arg.split(",") if "," in arg else arg.split()) if s.strip()]
    if len(secenekler) < 2:
        kullanim("sec")
        soyle(tr_en("Örnek: sec pizza, lahmacun, dürüm", "Example: pick pizza, burger, tacos"), GRI)
        return
    for i in range(18):
        sys.stdout.write(f"\r  {GRI}🤔 {random.choice(secenekler):<30}{RESET}")
        sys.stdout.flush()
        time.sleep(0.03 + i * 0.012)
    sys.stdout.write(f"\r  {T.ANA}{tr_en('🐼 Panda diyor ki:', '🐼 The panda says:')} "
                     f"{BEYAZ}{KALIN}{random.choice(secenekler)}{RESET}\033[K\n")


@komut("hash", "hash", "Araçlar", "Metnin MD5 / SHA1 / SHA256 özetini çıkarır", "Shows the MD5 / SHA1 / SHA256 hash of a text",
       "<metin>", "<text>")
def k_hash(arg):
    if not arg:
        kullanim("hash")
        return
    for ad in ("md5", "sha1", "sha256"):
        print(f"  {T.ANA}{ad:<7}{RESET} {hashlib.new(ad, arg.encode()).hexdigest()}")


@komut("taban", "base", "Araçlar", "Sayıyı ikilik, sekizlik, onluk ve on altılık tabanda gösterir",
       "Shows a number in binary, octal, decimal and hexadecimal", "<sayı|0b1010|0xff>", "<number|0b1010|0xff>")
def k_taban(arg):
    try:
        n = int(arg.strip(), 0)
    except ValueError:
        kullanim("taban")
        return
    ikili = format(abs(n), "b")
    ikili = " ".join(ikili[max(0, i - 4):i] for i in range(len(ikili), 0, -4)[::-1])
    for ad, deger in ((tr_en("Onluk (10)", "Decimal (10)"), n),
                      (tr_en("İkilik (2)", "Binary (2)"), ("-" if n < 0 else "") + ikili),
                      (tr_en("Sekizlik (8)", "Octal (8)"), oct(n)),
                      (tr_en("On altılık (16)", "Hexadecimal (16)"), hex(n).upper().replace("0X", "0x"))):
        print(f"  {T.ANA}{ad:<17}{RESET} {BEYAZ}{deger}{RESET}")


@komut("asal", "prime", "Araçlar", "Sayı asal mı bakar, değilse çarpanlarına ayırır",
       "Checks if a number is prime; if not, splits it into prime factors", "<sayı>", "<number>")
def k_asal(arg):
    try:
        n = int(arg)
        if not 2 <= n <= 10 ** 13:
            raise ValueError
    except ValueError:
        hata(tr_en("2 ile 10 trilyon arasında bir tam sayı yaz. Örnek: asal 97",
                   "Enter a whole number between 2 and 10 trillion. Example: prime 97"))
        return
    carpanlar, kalan, bolen = Counter(), n, 2
    while bolen * bolen <= kalan:
        while kalan % bolen == 0:
            carpanlar[bolen] += 1
            kalan //= bolen
        bolen += 1 if bolen == 2 else 2
    if kalan > 1:
        carpanlar[kalan] += 1
    if carpanlar[n] == 1:
        soyle(tr_en(f"✓ {BEYAZ}{KALIN}{n}{RESET}{T.ANA} bir ASAL sayı! 💎", f"✓ {BEYAZ}{KALIN}{n}{RESET}{T.ANA} is a PRIME number! 💎"))
    else:
        yazim = " × ".join(f"{p}^{u}" if u > 1 else str(p) for p, u in sorted(carpanlar.items()))
        soyle(tr_en(f"✗ {n} asal değil  =  ", f"✗ {n} is not prime  =  ") + f"{BEYAZ}{KALIN}{yazim}", SARI)


@komut("fib", "fib fibonacci", "Araçlar", "Fibonacci dizisinin ilk n terimini yazar", "Prints the first n Fibonacci numbers",
       "[n]", "[n]")
def k_fib(arg):
    try:
        n = min(max(int(arg or 15), 1), 100)
    except ValueError:
        kullanim("fib")
        return
    a, b, dizi = 0, 1, []
    for _ in range(n):
        dizi.append(str(a))
        a, b = b, a + b
    print(textwrap.fill(", ".join(dizi), genislik() - 4, initial_indent="  ", subsequent_indent="  "))


@komut("faktoriyel fakt", "factorial", "Araçlar", "n! hesaplar", "Calculates n!", "<n>", "<n>")
def k_faktoriyel(arg):
    try:
        n = int(arg)
        if not 0 <= n <= 1000:
            raise ValueError
    except ValueError:
        hata(tr_en("0 ile 1000 arasında bir sayı yaz. Örnek: faktoriyel 10",
                   "Enter a number between 0 and 1000. Example: factorial 10"))
        return
    soyle(f"{n}! = {BEYAZ}{KALIN}{sayi_bicimle(math.factorial(n))}")


@komut("yuzde", "percent", "Araçlar", "Yüzde hesabı yapar", "Does percentage math", "<a> <b>", "<a> <b>")
def k_yuzde(arg):
    try:
        a, b = sayilar(arg)[:2]
    except ValueError:
        kullanim("yuzde")
        soyle(tr_en("Örnek: yuzde 20 150  →  150'nin %20'si ve 20'nin 150 içindeki payı",
                    "Example: percent 20 150  →  20% of 150, and how much of 150 is 20"), GRI)
        return
    soyle(tr_en(f"{b} × %{a}  = ", f"{a}% of {b}  = ") + f"{BEYAZ}{KALIN}{sayi_bicimle(b * a / 100)}")
    if b:
        soyle(f"{a} / {b}  = " + tr_en(f"%{BEYAZ}{KALIN}{a / b * 100:.2f}", f"{BEYAZ}{KALIN}{a / b * 100:.2f}%"))
    if a:
        soyle(tr_en(f"{a} → {b} değişimi: %{(b - a) / a * 100:+.2f}", f"Change from {a} → {b}: {(b - a) / a * 100:+.2f}%"), GRI)


@komut("istat ortalama", "average stat", "Araçlar", "Sayıların ortalaması, medyanı, en büyüğü...",
       "Mean, median, largest... of a list of numbers", "<sayılar>", "<numbers>")
def k_istat(arg):
    try:
        liste = sayilar(arg)
        if not liste:
            raise ValueError
    except ValueError:
        kullanim("istat")
        soyle(tr_en("Örnek: istat 70 85 90 45 100", "Example: average 70 85 90 45 100"), GRI)
        return
    degerler = [(tr_en("Adet", "Count"), len(liste)), (tr_en("Toplam", "Sum"), sum(liste)),
                (tr_en("Ortalama", "Mean"), statistics.mean(liste)), (tr_en("Medyan", "Median"), statistics.median(liste)),
                (tr_en("En küçük", "Smallest"), min(liste)), (tr_en("En büyük", "Largest"), max(liste))]
    if len(liste) > 1:
        degerler.append((tr_en("Std. sapma", "Std. dev."), statistics.stdev(liste)))
    for ad, deger in degerler:
        print(f"  {T.ANA}{ad:<11}{RESET} {BEYAZ}{sayi_bicimle(round(deger, 4) if isinstance(deger, float) else deger)}{RESET}")


@komut("sirala", "sort", "Araçlar", "Sayıları ya da kelimeleri sıralar", "Sorts numbers or words", "<öğeler>", "<items>")
def k_sirala(arg):
    if not arg:
        kullanim("sirala")
        return
    try:
        sonuc = [sayi_bicimle(s) for s in sorted(sayilar(arg))]
    except ValueError:
        sonuc = sorted(re.split(r"[,\s]+", arg.strip()), key=sadelestir)
    soyle("↑ " + ", ".join(sonuc), BEYAZ)


@komut("sicaklik derece", "temp", "Araçlar", "Sıcaklığı °C / °F / K birimlerine çevirir",
       "Converts a temperature between °C / °F / K", "<değer>[c|f|k]", "<value>[c|f|k]")
def k_sicaklik(arg):
    eslesme = re.fullmatch(r"\s*(-?[\d.,]+)\s*°?\s*([cfkCFK]?)\s*", arg)
    if not eslesme:
        kullanim("sicaklik")
        soyle(tr_en("Örnek: sicaklik 36.6   •   sicaklik 100f   •   sicaklik 300k",
                    "Example: temp 36.6   •   temp 100f   •   temp 300k"), GRI)
        return
    deger, birim = float(eslesme.group(1).replace(",", ".")), (eslesme.group(2) or "c").lower()
    c = {"c": deger, "f": (deger - 32) * 5 / 9, "k": deger - 273.15}[birim]
    if c < -273.15:
        hata(tr_en("Mutlak sıfırın altı yok aga, fizik buna izin vermiyor. 🥶",
                   "Nothing is colder than absolute zero, buddy. Physics won't allow it. 🥶"))
        return
    soyle(f"🌡  {BEYAZ}{c:.2f} °C{RESET}   {T.ANA}{c * 9 / 5 + 32:.2f} °F{RESET}   {CAMGOBEGI}{c + 273.15:.2f} K")


@komut("vki", "bmi", "Araçlar", "Vücut kitle indeksini hesaplar", "Calculates your body mass index (BMI)",
       "<kilo> <boy_cm>", "<weight_kg> <height_cm>")
def k_vki(arg):
    try:
        kilo, boy = sayilar(arg)[:2]
        boy = boy / 100 if boy > 3 else boy
        vki = kilo / boy ** 2
    except (ValueError, ZeroDivisionError):
        kullanim("vki")
        return
    for sinir, ad, renk in ((18.5, tr_en("Zayıf", "Underweight"), SARI), (25, "Normal", YESIL),
                            (30, tr_en("Fazla kilolu", "Overweight"), SARI), (float("inf"), tr_en("Obez", "Obese"), KIRMIZI)):
        if vki < sinir:
            soyle(f"⚖  {tr_en('VKİ', 'BMI')}: {BEYAZ}{KALIN}{vki:.1f}{RESET}  →  {renk}{ad}")
            break
    soyle(tr_en("Bilgi amaçlıdır, doktor tavsiyesi değildir.", "For information only, not medical advice."), GRI)


@komut("yas", "age", "Araçlar", "Yaşını ve yaşadığın gün sayısını hesaplar",
       "Calculates your age and how many days you've been alive", "<GG.AA.YYYY | yıl>", "<DD.MM.YYYY | year>")
def k_yas(arg):
    bugun = datetime.date.today()
    if arg.strip().isdigit() and len(arg.strip()) == 4:
        yas = bugun.year - int(arg)
        soyle(tr_en(f"🎂 Bu yıl {BEYAZ}{KALIN}{yas}{RESET}{T.ANA} yaşına giriyorsun/girdin.",
                    f"🎂 You turn (or turned) {BEYAZ}{KALIN}{yas}{RESET}{T.ANA} this year."))
        return
    try:
        dogum = tarih_coz(arg)
    except ValueError:
        kullanim("yas")
        return
    yas = bugun.year - dogum.year - ((bugun.month, bugun.day) < (dogum.month, dogum.day))
    try:
        sonraki = dogum.replace(year=bugun.year)
    except ValueError:  # 29 Şubat doğumlular
        sonraki = datetime.date(bugun.year, 3, 1)
    if sonraki < bugun:
        sonraki = sonraki.replace(year=bugun.year + 1)
    gun_sayisi = (bugun - dogum).days
    soyle(tr_en(f"🎂 {BEYAZ}{KALIN}{yas}{RESET}{T.ANA} yaşındasın, tam {binlik(gun_sayisi)} gündür yaşıyorsun!",
                f"🎂 You are {BEYAZ}{KALIN}{cogul(yas, 'year')}{RESET}{T.ANA} old and have been alive for "
                f"{cogul(gun_sayisi, 'day')}!"))
    kalan = (sonraki - bugun).days
    soyle(tr_en("🎉 İYİ Kİ DOĞDUN! 🎉", "🎉 HAPPY BIRTHDAY! 🎉") if kalan == 0 else
          tr_en(f"Bir sonraki doğum gününe {kalan} gün var.", f"{cogul(kalan, 'day')} until your next birthday."), SARI)


@komut("gun gunsay", "days", "Araçlar", "Bir tarihe kaç gün kaldığını / geçtiğini söyler",
       "Tells how many days are left until a date / have passed since it", "<GG.AA.YYYY>", "<DD.MM.YYYY>")
def k_gun(arg):
    try:
        hedef = tarih_coz(arg)
    except ValueError:
        kullanim("gun")
        return
    fark = (hedef - datetime.date.today()).days
    tarih = f"{hedef:%d.%m.%Y} ({gun_adi(hedef)})"
    if fark > 0:
        soyle(tr_en(f"⏳ {tarih} tarihine {BEYAZ}{KALIN}{fark}{RESET}{T.ANA} gün var.",
                    f"⏳ {tarih} is {BEYAZ}{KALIN}{cogul(fark, 'day')}{RESET}{T.ANA} away."))
    elif fark < 0:
        soyle(tr_en(f"⌛ {tarih} üzerinden {BEYAZ}{KALIN}{-fark}{RESET}{T.ANA} gün geçti.",
                    f"⌛ {tarih} was {BEYAZ}{KALIN}{cogul(-fark, 'day')}{RESET}{T.ANA} ago."))
    else:
        soyle(tr_en("📌 O gün bugün!", "📌 That's today!"))


@komut("unix", "unix timestamp", "Araçlar", "Unix zaman damgasını gösterir / çevirir", "Shows / converts a Unix timestamp",
       "[zaman_damgası]", "[timestamp]")
def k_unix(arg):
    if not arg:
        soyle(tr_en(f"⏲  Şu an: {BEYAZ}{KALIN}{int(time.time())}{RESET}  {GRI}(1 Ocak 1970'ten beri geçen saniye)",
                    f"⏲  Now: {BEYAZ}{KALIN}{int(time.time())}{RESET}  {GRI}(seconds since 1 January 1970)"))
        return
    try:
        an = datetime.datetime.fromtimestamp(float(arg))
    except (ValueError, OverflowError, OSError):
        kullanim("unix")
        return
    soyle(f"⏲  {arg} = {BEYAZ}{an:%d.%m.%Y %H:%M:%S}")


@komut("sayac geri", "timer", "Araçlar", "Dev rakamlarla geri sayım yapar", "Counts down with giant digits",
       "<saniye | dk:sn>", "<seconds | min:sec>")
def k_sayac(arg):
    try:
        if ":" in arg:
            dk, sn = arg.split(":")
            toplam = int(dk) * 60 + int(sn)
        else:
            toplam = int(arg)
        if not 0 < toplam <= 5999:
            raise ValueError
    except ValueError:
        kullanim("sayac")
        soyle(tr_en("Örnek: sayac 10   •   sayac 2:30", "Example: timer 10   •   timer 2:30"), GRI)
        return
    bitis = time.time() + toplam
    ilk = True
    with Sahne():
        while True:
            kalan = max(0, math.ceil(bitis - time.time()))
            renk = KIRMIZI if kalan <= 5 else SARI if kalan <= 10 else T.ANA
            yerinde_yaz(["  " + renk + s for s in buyuk_yazi(f"{kalan // 60:02d}:{kalan % 60:02d}")]
                        + [f"  {GRI}{tr_en('iptal için bir tuşa bas', 'press any key to cancel')}{RESET}"], ilk)
            ilk = False
            if kalan == 0:
                break
            if tus_bekle(0.2):
                soyle(tr_en("Geri sayım iptal edildi.", "Countdown cancelled."), SARI)
                return
    for _ in range(3):
        sys.stdout.write("\a")
        soyle(tr_en("⏰ SÜRE DOLDU! ⏰", "⏰ TIME'S UP! ⏰"), KIRMIZI + KALIN)
        time.sleep(0.3)


@komut("kronometre", "stopwatch", "Araçlar", "Kronometre: boşluk = tur, başka tuş = durdur",
       "Stopwatch: space = lap, any other key = stop")
def k_kronometre(arg):
    baslangic = time.time()
    turlar = []
    ilk = True
    with Sahne():
        while True:
            gecen = time.time() - baslangic
            metin = f"{int(gecen // 60):02d}:{int(gecen % 60):02d}.{int(gecen * 10 % 10)}"
            son_tur = f"  {GRI}{tr_en('tur', 'lap')} {len(turlar)}: {turlar[-1]:.1f} {tr_en('sn', 's')}{RESET}" if turlar else ""
            yerinde_yaz(["  " + T.ANA + s for s in buyuk_yazi(metin)]
                        + [f"  {GRI}{tr_en('[boşluk] tur   [başka tuş] durdur', '[space] lap   [any other key] stop')}"
                           f"{RESET}{son_tur}"], ilk)
            ilk = False
            tus = tus_bekle(0.05)
            if tus == "BOSLUK":
                turlar.append(gecen)
            elif tus:
                break
    soyle(tr_en(f"⏱  Toplam: {BEYAZ}{KALIN}{gecen:.2f} saniye", f"⏱  Total: {BEYAZ}{KALIN}{gecen:.2f} seconds"))
    for i, tur in enumerate(turlar, 1):
        soyle(tr_en(f"Tur {i}: {tur:.2f} sn", f"Lap {i}: {tur:.2f} s"), GRI)


@komut("say", "count wc", "Araçlar", "Metindeki harf, kelime ve sesli harfleri sayar",
       "Counts the letters, words and vowels in a text", "<metin>", "<text>")
def k_say(arg):
    if not arg:
        kullanim("say")
        return
    sesliler = tr_en("aeıioöuüAEIİOÖUÜ", "aeiouAEIOU")
    for ad, deger in ((tr_en("Karakter", "Characters"), len(arg)), (tr_en("Boşluksuz", "No spaces"), len(arg.replace(" ", ""))),
                      (tr_en("Kelime", "Words"), len(arg.split())), (tr_en("Sesli harf", "Vowels"), sum(h in sesliler for h in arg)),
                      (tr_en("Rakam", "Digits"), sum(h.isdigit() for h in arg))):
        print(f"  {T.ANA}{ad:<11}{RESET} {BEYAZ}{deger}{RESET}")


@komut("ters", "reverse", "Araçlar", "Metni tersten yazar", "Writes a text backwards", "<metin>", "<text>")
def k_ters(arg):
    soyle(arg[::-1], BEYAZ) if arg else kullanim("ters")


@komut("buyuk", "upper", "Araçlar", "METNİ BÜYÜK HARFE ÇEVİRİR (Türkçe uyumlu)", "CONVERTS TEXT TO UPPERCASE",
       "<metin>", "<text>")
def k_buyuk(arg):
    soyle(buyuk_harf(arg), BEYAZ) if arg else kullanim("buyuk")


@komut("kucuk", "lower", "Araçlar", "metni küçük harfe çevirir (türkçe uyumlu)", "converts text to lowercase",
       "<metin>", "<text>")
def k_kucuk(arg):
    soyle(kucuk_harf(arg), BEYAZ) if arg else kullanim("kucuk")


@komut("palindrom", "palindrome", "Araçlar", "Metin tersten de aynı mı okunuyor?", "Does the text read the same backwards?",
       "<metin>", "<text>")
def k_palindrom(arg):
    if not arg:
        kullanim("palindrom")
        return
    sade = re.sub(r"[^\w]", "", kucuk_harf(arg))
    if sade and sade == sade[::-1]:
        soyle(tr_en(f"✓ '{arg}' bir palindrom! Tersten de aynı. 🔁", f"✓ '{arg}' is a palindrome! Same backwards. 🔁"))
    else:
        soyle(tr_en(f"✗ Palindrom değil. Tersi: {arg[::-1]}", f"✗ Not a palindrome. Backwards: {arg[::-1]}"), SARI)
        soyle(tr_en("Örnek palindromlar: ey edip adanada pide ye • kabak • 12321",
                    "Example palindromes: never odd or even • racecar • 12321"), GRI)


LOREM = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore "
         "et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip "
         "ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla "
         "pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim "
         "id est laborum").split()


@komut("lorem", "lorem", "Araçlar", "Deneme amaçlı sahte yazı (lorem ipsum) üretir", "Generates placeholder text (lorem ipsum)",
       "[kelime sayısı]", "[word count]")
def k_lorem(arg):
    try:
        adet = min(max(int(arg or 40), 1), 500)
    except ValueError:
        kullanim("lorem")
        return
    kelimeler = LOREM[:8] + [random.choice(LOREM) for _ in range(max(0, adet - 8))]
    metin = " ".join(kelimeler[:adet]).capitalize() + "."
    print(textwrap.fill(metin, min(80, genislik() - 4), initial_indent="  ", subsequent_indent="  "))


@komut("hexrenk", "hexcolor color", "Araçlar", "Bir renk kodunu (#ff8800) ekranda boyar",
       "Paints a color code (#ff8800) on the screen", "[#RRGGBB]", "[#RRGGBB]")
def k_hexrenk(arg):
    kod = arg.strip().lstrip("#") or "".join(random.choice("0123456789abcdef") for _ in range(6))
    if len(kod) == 3:
        kod = "".join(h * 2 for h in kod)
    try:
        r, g, b = (int(kod[i:i + 2], 16) for i in (0, 2, 4))
        if len(kod) != 6:
            raise ValueError
    except ValueError:
        kullanim("hexrenk")
        return
    zit = f"#{255 - r:02x}{255 - g:02x}{255 - b:02x}"
    for _ in range(3):
        print(f"  \033[48;2;{r};{g};{b}m{' ' * 24}{RESET}  \033[48;2;{255 - r};{255 - g};{255 - b}m{' ' * 6}{RESET}")
    soyle(f"#{kod.lower()}  •  rgb({r}, {g}, {b})  •  {tr_en('zıt renk', 'inverted')}: {zit}", BEYAZ)


# ═══════════════════════════ KOMUTLAR: ŞİFRELEME ═══════════════════════════
def metin_gerekli(isim):
    """Argümansız çağrılan şifreleme komutları için ortak kontrol."""
    def sarici(fonksiyon):
        def ic(arg):
            if not arg:
                kullanim(isim)
                return
            fonksiyon(arg)
        return ic
    return sarici


def cevir_ve_goster(etiket, sonuc):
    soyle(f"{GRI}{etiket}:{RESET}")
    print(textwrap.fill(sonuc, genislik() - 4, initial_indent="  ", subsequent_indent="  ",
                        break_on_hyphens=False) if sonuc else "")


@komut("ikili", "binary", "Şifreleme", "Metni 0 ve 1'lere (binary) çevirir", "Turns text into 0s and 1s (binary)",
       "<metin>", "<text>")
@metin_gerekli("ikili")
def k_ikili(arg):
    cevir_ve_goster(tr_en("İkilik", "Binary"), " ".join(f"{b:08b}" for b in arg.encode()))


@komut("ikilicoz binarycoz", "unbinary", "Şifreleme", "0 ve 1'leri tekrar metne çevirir", "Turns 0s and 1s back into text",
       "<01000001 ...>", "<01000001 ...>")
@metin_gerekli("ikilicoz")
def k_ikilicoz(arg):
    bitler = re.sub(r"[^01]", "", arg)
    if len(bitler) % 8:
        hata(tr_en("Bit sayısı 8'in katı olmalı.", "The number of bits must be a multiple of 8."))
        return
    veri = bytes(int(bitler[i:i + 8], 2) for i in range(0, len(bitler), 8))
    cevir_ve_goster(tr_en("Metin", "Text"), veri.decode("utf-8", errors="replace"))


@komut("hex", "hex", "Şifreleme", "Metni on altılık (hex) koda çevirir", "Turns text into hexadecimal (hex) code",
       "<metin>", "<text>")
@metin_gerekli("hex")
def k_hex(arg):
    cevir_ve_goster("Hex", arg.encode().hex(" "))


@komut("hexcoz", "unhex", "Şifreleme", "Hex kodunu metne çevirir", "Turns hex code back into text",
       "<48 65 6c 6c 6f>", "<48 65 6c 6c 6f>")
@metin_gerekli("hexcoz")
def k_hexcoz(arg):
    try:
        cevir_ve_goster(tr_en("Metin", "Text"),
                        bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", arg)).decode("utf-8", errors="replace"))
    except ValueError:
        hata(tr_en("Geçersiz hex kodu.", "Invalid hex code."))


@komut("base64", "base64 b64", "Şifreleme", "Metni Base64 ile kodlar", "Encodes text with Base64", "<metin>", "<text>")
@metin_gerekli("base64")
def k_base64(arg):
    cevir_ve_goster("Base64", base64.b64encode(arg.encode()).decode())


@komut("base64coz b64coz", "unbase64", "Şifreleme", "Base64 kodunu çözer", "Decodes Base64 code", "<kod>", "<code>")
@metin_gerekli("base64coz")
def k_base64coz(arg):
    try:
        cevir_ve_goster(tr_en("Metin", "Text"),
                        base64.b64decode(arg.strip() + "=" * (-len(arg.strip()) % 4)).decode("utf-8", errors="replace"))
    except ValueError:
        hata(tr_en("Geçersiz Base64 kodu.", "Invalid Base64 code."))


# Sezar şifresi dile göre alfabe seçer: Türkçede 29 harfli Türk alfabesi, İngilizcede A-Z
ALFABELER = {"tr": ("abcçdefgğhıijklmnoöprsştuüvyz", "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"),
             "en": (string.ascii_lowercase, string.ascii_uppercase)}


def sezar_kaydir(metin, adim):
    sonuc = ""
    for harf in metin:
        for alfabe in ALFABELER[dil()]:
            if harf in alfabe:
                harf = alfabe[(alfabe.index(harf) + adim) % len(alfabe)]
                break
        sonuc += harf
    return sonuc


@komut("sezar", "caesar", "Şifreleme", "Sezar şifresi: her harfi n adım kaydırır (Türk alfabesi)",
       "Caesar cipher: shifts every letter n steps (A-Z)", "<adım> <metin>", "<shift> <text>")
def k_sezar(arg):
    parcalar = arg.split(maxsplit=1)
    try:
        adim, metin = int(parcalar[0]), parcalar[1]
    except (ValueError, IndexError):
        kullanim("sezar")
        soyle(tr_en("Örnek: sezar 3 merhaba   (çözmek için: sezar -3 ...)",
                    "Example: caesar 3 hello   (to decode: caesar -3 ...)"), GRI)
        return
    cevir_ve_goster(tr_en(f"Sezar ({adim:+d})", f"Caesar ({adim:+d})"), sezar_kaydir(metin, adim))


YAYGIN_KELIMELER = {  # Sezar kırıcı, bu kelimelerden en çok içeren çözümü seçer
    "tr": {"ve", "bir", "bu", "da", "de", "ne", "ben", "sen", "biz", "merhaba", "selam", "panda", "kod",
           "gizli", "mesaj", "için", "ile", "çok", "var", "yok", "nasılsın", "iyi", "evet", "hayır",
           "ama", "gibi", "şifre", "bambu", "dünya", "the", "and", "hello", "yarın", "bugün", "saat",
           "okul", "gel", "git", "buluşalım", "seni", "beni", "hadi", "tamam"},
    "en": {"the", "and", "is", "a", "i", "you", "to", "of", "in", "it", "hello", "hi", "panda", "code",
           "secret", "message", "meet", "me", "at", "tomorrow", "today", "school", "yes", "no", "not", "this",
           "that", "for", "with", "are", "was", "bamboo", "world", "good", "we", "see", "go", "come", "let",
           "time", "password", "my", "your", "ok"},
}


@komut("sezarkir caesarkir", "caesarcrack", "Şifreleme", "Sezar şifresini tüm ihtimalleri deneyerek kırar",
       "Cracks a Caesar cipher by trying every possible shift", "<şifreli metin>", "<encrypted text>")
@metin_gerekli("sezarkir")
def k_sezarkir(arg):
    adaylar = []
    for adim in range(1, len(ALFABELER[dil()][0])):
        aday = sezar_kaydir(arg, -adim)
        puan = sum(k in YAYGIN_KELIMELER[dil()] for k in re.findall(r"\w+", kucuk_harf(aday)))
        adaylar.append((puan, adim, aday))
    en_iyi = max(adaylar)
    for puan, adim, aday in adaylar:
        isaret = (f"  {YESIL}{KALIN}◀ {tr_en('büyük ihtimalle bu!', 'most likely this one!')}{RESET}"
                  if puan and (puan, adim, aday) == en_iyi else "")
        print(f"  {GRI}{adim:>2}{RESET} {BEYAZ if isaret else ACIK_GRI}{aday[:genislik() - 30]}{RESET}{isaret}")


@komut("rot13", "rot13", "Şifreleme", "ROT13: İngiliz alfabesini 13 kaydırır (iki kere yaparsan geri döner)",
       "ROT13: shifts the English alphabet by 13 (do it twice to get the original back)", "<metin>", "<text>")
@metin_gerekli("rot13")
def k_rot13(arg):
    cevir_ve_goster("ROT13", codecs.encode(arg, "rot13"))


MORS = {"A": ".-", "B": "-...", "C": "-.-.", "Ç": "-.-..", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
        "Ğ": "--.-.", "H": "....", "I": "..", "İ": ".-..-", "J": ".---", "K": "-.-", "L": ".-..", "M": "--",
        "N": "-.", "O": "---", "Ö": "---.", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "Ş": ".--..",
        "T": "-", "U": "..-", "Ü": "..--", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
        "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....",
        "7": "--...", "8": "---..", "9": "----.", ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--"}
MORS_TERS = {v: k for k, v in MORS.items()}


@komut("mors", "morse", "Şifreleme", "Metni mors alfabesine çevirir", "Turns text into Morse code", "<metin>", "<text>")
@metin_gerekli("mors")
def k_mors(arg):
    kelimeler = [" ".join(MORS[h] for h in kelime if h in MORS) for kelime in buyuk_harf(arg).split()]
    cevir_ve_goster(tr_en("Mors", "Morse"), " / ".join(kelimeler))


@komut("morscoz", "unmorse", "Şifreleme", "Mors kodunu metne çevirir ('/' kelime ayırır)",
       "Turns Morse code back into text ('/' separates words)", "<.-- ...>", "<.-- ...>")
@metin_gerekli("morscoz")
def k_morscoz(arg):
    kelimeler = ["".join(MORS_TERS.get(k, "?") for k in kelime.split()) for kelime in arg.split("/")]
    cevir_ve_goster(tr_en("Metin", "Text"), " ".join(kelimeler))


def vigenere(metin, anahtar, yon):
    anahtar = [ord(h) - 97 for h in sadelestir(anahtar) if "a" <= h <= "z"]
    if not anahtar:
        raise ValueError
    sonuc, i = "", 0
    for harf in metin:
        if harf.isascii() and harf.isalpha():
            taban = 65 if harf.isupper() else 97
            harf = chr((ord(harf) - taban + yon * anahtar[i % len(anahtar)]) % 26 + taban)
            i += 1
        sonuc += harf
    return sonuc


@komut("vigenere", "vigenere", "Şifreleme", "Vigenère şifresi: anahtar kelimeyle şifreler",
       "Vigenère cipher: encrypts with a keyword", "<anahtar> <metin>", "<key> <text>")
def k_vigenere(arg, yon=1):
    parcalar = arg.split(maxsplit=1)
    try:
        cevir_ve_goster("Vigenère", vigenere(parcalar[1], parcalar[0], yon))
    except (IndexError, ValueError):
        kullanim("vigenerecoz" if yon < 0 else "vigenere")


@komut("vigenerecoz", "unvigenere", "Şifreleme", "Vigenère şifresini anahtarla çözer",
       "Decrypts a Vigenère cipher with its key", "<anahtar> <metin>", "<key> <text>")
def k_vigenerecoz(arg):
    k_vigenere(arg, -1)


@komut("ascii", "ascii ord", "Şifreleme", "Her harfin bilgisayardaki sayı kodunu gösterir",
       "Shows the number code of every character", "<metin>", "<text>")
@metin_gerekli("ascii")
def k_ascii(arg):
    print(f"  {GRI}{tr_en('Harf   Onluk   Hex     İkilik', 'Char   Dec     Hex     Binary')}{RESET}")
    for harf in arg[:30]:
        kod = ord(harf)
        print(f"  {T.ANA}{harf!r:<6}{RESET} {BEYAZ}{kod:<7}{RESET} {kod:<#7x} {GRI}{kod:08b}{RESET}")


@komut("asciitablo", "asciitable", "Şifreleme", "Tüm ASCII karakter tablosunu gösterir", "Shows the whole ASCII table")
def k_asciitablo(arg):
    kodlar = list(range(32, 127))
    sutun = max(1, min(8, (genislik() - 2) // 10))
    satir_sayisi = math.ceil(len(kodlar) / sutun)
    for r in range(satir_sayisi):
        print("  " + "".join(f"{GRI}{kodlar[i]:>3}{RESET} {T.ANA}{chr(kodlar[i])!s:<5}{RESET} "
                             for i in range(r, len(kodlar), satir_sayisi)))


# ═══════════════════════════ KOMUTLAR: EĞLENCE ═══════════════════════════
SOZLER = {"tr": [
    "Önce çalıştır, sonra düzelt, sonra hızlandır.",
    "Kod bir kere yazılır, yüz kere okunur. Okuyanı düşün.",
    "Hata mesajı düşmanın değil, en dürüst arkadaşındır.",
    "Her uzman bir zamanlar 'print(\"merhaba\")' yazan bir acemiydi.",
    "Bilgisayar ne dediysen onu yapar; ne demek istediğini değil.",
    "Bugün yazdığın çirkin kod, yarın düzelteceğin güzel koddur.",
    "Kopyala-yapıştır öğrenmez; yazan öğrenir.",
    "Bir problemi çözemiyorsan, onu daha küçük parçalara böl.",
    "En iyi hata ayıklayıcı: bir bardak çay ve 5 dakikalık mola.",
    "Kodun çalışmıyorsa sorun yok. Neden çalışmadığını bulunca öğreniyorsun.",
    "Yavaş ama her gün kodlayan, hızlı ama bir gün kodlayanı geçer.",
    "Değişken adını düzgün koy; gelecekteki sen teşekkür edecek.",
    "Sistem 'hacklenmez', dikkatsizlik hacklenir.",
    "Klavyen kılıcın, mantığın kalkanın.",
    "Soru sormaktan korkma; Stack Overflow'daki herkes bir zamanlar soru sordu.",
    "Mükemmel kod yoktur; çalışan ve anlaşılan kod vardır.",
    "Bir panda günde 12 saat bambu yer. Sen de günde 12 dakika kod ye.",
    "Hata yapmayan program yazamaz. Hata yapmaktan korkan hiç yazamaz.",
    "İlk sürüm her zaman utandırır. Utandırmıyorsa geç çıkardın demektir.",
    "Bilgi paylaştıkça çoğalır; kodunu paylaş.",
    "Terminali seven, terminal tarafından sevilir.",
    "Önce düşün, sonra yaz. Ya da önce yaz, sonra çok düşün.",
    "Şifren '123456' ise, hacker'a zahmet etme demişsin demektir.",
    "Kod yazmak bir dil öğrenmek gibidir: konuştukça akıcılaşırsın.",
    "Git commit'lerin, günlüğün gibidir. Güzel yaz.",
], "en": [
    "Make it work, then make it right, then make it fast.",
    "Code is written once and read a hundred times. Think of the reader.",
    "An error message isn't your enemy; it's your most honest friend.",
    "Every expert was once a beginner who wrote 'print(\"hello\")'.",
    "A computer does what you tell it to do, not what you meant.",
    "The ugly code you write today is the nice code you'll fix tomorrow.",
    "Copy-paste doesn't learn anything; typing does.",
    "If you can't solve a problem, break it into smaller pieces.",
    "The best debugger: a cup of tea and a 5-minute break.",
    "Your code doesn't work? No problem. You learn when you find out why.",
    "Coding a little every day beats coding a lot once in a while.",
    "Give your variables good names; future you will thank you.",
    "Systems don't get 'hacked'; carelessness does.",
    "Your keyboard is your sword, your logic is your shield.",
    "Don't be afraid to ask; everyone on Stack Overflow asked a question once.",
    "There's no perfect code, only code that works and can be understood.",
    "A panda eats bamboo 12 hours a day. You can munch on code for 12 minutes.",
    "If you never make mistakes, you're not writing programs. If you fear mistakes, you'll never write one.",
    "The first version is always embarrassing. If it isn't, you shipped it too late.",
    "Knowledge grows when you share it; share your code.",
    "Love the terminal and the terminal will love you back.",
    "Think first, then write. Or write first, then think a lot.",
    "If your password is '123456', you've done the hacker's job for them.",
    "Writing code is like learning a language: the more you speak, the more fluent you get.",
    "Your git commits are like a diary. Write them well.",
]}

FIKRALAR = {"tr": [
    ("Programcı neden gözlük takar?", "Çünkü C# göremiyor! 👓"),
    ("Bir SQL sorgusu bara girer, iki masaya yaklaşır ve sorar:", "'JOIN'leyebilir miyim?' 🍻"),
    ("Programcının en sevdiği yer neresi?", "Foo Bar. 🍺"),
    ("Neden programcılar karanlıkta çalışmayı sever?", "Çünkü ışık (light) bug'ları çeker! 🐛"),
    ("Annesi programcıya: 'Markete git, 1 ekmek al, yumurta varsa 6 tane al.'",
     "Programcı 6 ekmekle döner: 'Yumurta vardı.' 🥚"),
    ("Pandanın bilgisayarı neden hiç bozulmaz?", "Çünkü her şeyi BAMBU-tstrap'le yükler. 🎋"),
    ("Kaç programcı bir ampulü değiştirebilir?", "Hiç, o bir donanım sorunu. 💡"),
    ("Programcı ile denizci arasındaki fark ne?", "Denizci ipi (rope) bağlar, programcı pipe'ı bağlar: |  ⚓"),
    ("Java geliştiricisi neden psikoloğa gitti?", "Çünkü çok fazla 'class' sorunu vardı."),
    ("Bir byte diğerine ne demiş?", "'Bit'tin mi artık benden?' 💔"),
    ("Neden Python'cular yılandan korkmaz?", "Çünkü onlar Monty Python izleyip gülüyor."),
    ("Programcının duası nedir?", "'Tanrım, lütfen production'da çalışsın.' 🙏"),
    ("'Benim bilgisayarımda çalışıyordu' diyen programcıya ne dendi?",
     "'Tamam, o zaman senin bilgisayarını müşteriye gönderiyoruz.' 📦"),
    ("0 ile 1 kavga etmiş, kim kazanmış?", "Hiçbiri, sonuç boolean çıkmış. ⚖️"),
    ("Recursion'ı anlamak için ne yapmalısın?", "Önce recursion'ı anlamalısın. 🔁"),
], "en": [
    ("Why do programmers wear glasses?", "Because they can't C#! 👓"),
    ("An SQL query walks into a bar, goes up to two tables and asks:", "'Can I JOIN you?' 🍻"),
    ("Where do programmers like to hang out?", "The Foo Bar. 🍺"),
    ("Why do programmers prefer dark mode?", "Because light attracts bugs! 🐛"),
    ("A programmer's mom says: 'Go to the store and buy a loaf of bread. If they have eggs, get 6.'",
     "The programmer comes back with 6 loaves: 'They had eggs.' 🥚"),
    ("Why does the panda's computer never break down?", "Because it loads everything with BAMBOOtstrap. 🎋"),
    ("How many programmers does it take to change a light bulb?", "None, that's a hardware problem. 💡"),
    ("Why did the programmer quit their job?", "Because they didn't get arrays. 💸"),
    ("Why did the Java developer go to therapy?", "Too many 'class' issues."),
    ("One byte asks another: 'Are you feeling okay?'", "'Not really, I'm a bit off today.' 🤒"),
    ("Why aren't Python programmers afraid of snakes?", "Because they're too busy laughing at Monty Python."),
    ("What is a programmer's prayer?", "'Please, please let it work in production.' 🙏"),
    ("A programmer says: 'But it worked on my machine!'",
     "'Great, then we'll ship your machine to the customer.' 📦"),
    ("0 and 1 got into a fight. Who won?", "Neither. The result was a boolean. ⚖️"),
    ("What do you need to do to understand recursion?", "First, you need to understand recursion. 🔁"),
]}

BILGILER = {"tr": [
    "İlk bilgisayar 'bug'ı 1947'de Harvard Mark II bilgisayarının içinde bulunan gerçek bir güveydi. 🦋",
    "Python adını yılandan değil, İngiliz komedi grubu Monty Python'dan alır.",
    "Tarihteki ilk programcı Ada Lovelace kabul edilir; 1840'larda ilk algoritmayı yazdı. 👩‍💻",
    "JavaScript'in ilk sürümü 1995'te sadece 10 günde yazıldı. ⚡",
    "Dünyanın ilk web sitesi hâlâ yayında: info.cern.ch 🌐",
    "Linux'u Linus Torvalds 1991'de, 21 yaşındayken hobi olarak başlattı. 🐧",
    "Git'i de Linus Torvalds yazdı (2005). İlk sürümü yaklaşık iki haftada hazırdı. 🔀",
    "Apollo 11'i Ay'a götüren bilgisayarın belleği yaklaşık 4 KB'tı. Telefonun milyonlarca katı güçlü. 🚀",
    "İlk bilgisayar faresi 1960'larda Douglas Engelbart tarafından tahtadan yapıldı. 🖱",
    "1 bayt = 8 bit. 1 kilobayt = 1024 bayt. 🔢",
    "CAPTCHA'nın açılımı 'bilgisayarlarla insanları ayırt etmek için tamamen otomatik Turing testi'dir. 🤖",
    "2038 problemi: 32 bitlik Unix saati 19 Ocak 2038'de taşacak. 'unix' komutuyla şu anki değere bak! ⏰",
    "Pandalar günde 10-16 saat yemek yer ve günde 12-38 kg bambu tüketebilir. 🎋",
    "Pandaların bileğinde bambuyu tutmaya yarayan bir 'sahte başparmak' vardır. 🐼",
    "Yeni doğan bir panda yavrusu yaklaşık 100 gram gelir; annesinin 1/900'ü kadar! 🍼",
    "İlk kayıtlı alan adı symbolics.com'dur (1985). 🏷",
    "Python'da 'import this' yazarsan Python'un felsefesi (Zen of Python) ekrana çıkar. 🧘",
    "'Hello, World!' geleneğini 1970'lerde Brian Kernighan yaygınlaştırdı. 👋",
    "QR kod 1994'te Japonya'da, araba parçalarını takip etmek için icat edildi. 📱",
    "İlk emoji seti 1999'da Japonya'da 176 küçük resimle yapıldı. 😀",
], "en": [
    "The first computer 'bug' was a real moth found inside the Harvard Mark II computer in 1947. 🦋",
    "Python is named after the British comedy group Monty Python, not the snake.",
    "Ada Lovelace is considered the first programmer; she wrote the first algorithm in the 1840s. 👩‍💻",
    "The first version of JavaScript was written in just 10 days in 1995. ⚡",
    "The world's first website is still online: info.cern.ch 🌐",
    "Linus Torvalds started Linux in 1991 as a hobby, when he was 21. 🐧",
    "Linus Torvalds wrote Git too (2005). The first version was ready in about two weeks. 🔀",
    "The computer that flew Apollo 11 to the Moon had about 4 KB of memory. Your phone is millions of times more powerful. 🚀",
    "The first computer mouse was made of wood by Douglas Engelbart in the 1960s. 🖱",
    "1 byte = 8 bits. 1 kilobyte = 1024 bytes. 🔢",
    "CAPTCHA stands for 'Completely Automated Public Turing test to tell Computers and Humans Apart'. 🤖",
    "The Year 2038 problem: 32-bit Unix time overflows on 19 January 2038. Check the current value with 'unix'! ⏰",
    "Pandas spend 10-16 hours a day eating and can get through 12-38 kg of bamboo daily. 🎋",
    "Pandas have a 'false thumb' on their wrist that helps them hold bamboo. 🐼",
    "A newborn panda cub weighs about 100 grams, roughly 1/900 of its mother! 🍼",
    "The first domain name ever registered was symbolics.com (1985). 🏷",
    "Type 'import this' in Python and it prints its philosophy, the Zen of Python. 🧘",
    "Brian Kernighan made the 'Hello, World!' tradition popular in the 1970s. 👋",
    "The QR code was invented in Japan in 1994 to keep track of car parts. 📱",
    "The first emoji set was made in Japan in 1999 with 176 tiny pictures. 😀",
]}

FALLAR = {"tr": [
    "Yakında çok zor bir bug'ı tek satırla çözeceksin. 🔮",
    "Kodun ilk denemede çalışacak... ve bu seni korkutacak. 😱",
    "Bir sonraki projen seni çok ileri götürecek. Başla artık! 🚀",
    "Önümüzdeki günlerde bir noktalı virgül hayatını kurtaracak. ;",
    "Bugün öğrendiğin küçük bir şey, yıllar sonra büyük işe yarayacak. 🌱",
    "Yakında bir arkadaşına kod öğreteceksin ve kendin daha çok öğreneceksin. 🤝",
    "Şans rakamın: 42. Neden mi? Evrenin cevabı o. 🌌",
    "Kahve falında bir yılan görüyorum... Python öğrenmeye devam!",
    "Kısmetinde bir 'Merge successful' mesajı var. ✅",
    "Bu hafta klavyene dökülecek bir içecek görmüyorum. Rahat ol. ☕",
    "Bambu yolun açık, panda gibi sakin ol. 🐼",
    "Yakında Stack Overflow'da bir sorunun cevabını SEN yazacaksın. 🏆",
    "Gelecekte adın bir programın 'Hakkında' sayfasında yazacak. ✨",
], "en": [
    "Soon you'll fix a really nasty bug with a single line. 🔮",
    "Your code will work on the first try... and that will scare you. 😱",
    "Your next project will take you far. Start it already! 🚀",
    "In the coming days, a semicolon will save your life. ;",
    "Something small you learn today will pay off big years from now. 🌱",
    "Soon you'll teach a friend to code and learn even more yourself. 🤝",
    "Your lucky number is 42. Why? It's the answer to the universe. 🌌",
    "I see a snake in your coffee cup... keep learning Python!",
    "A 'Merge successful' message is in your future. ✅",
    "I see no drinks spilling on your keyboard this week. Relax. ☕",
    "Your bamboo path is clear; stay calm like a panda. 🐼",
    "Soon YOU will write the answer to a question on Stack Overflow. 🏆",
    "One day your name will appear on a program's 'About' page. ✨",
]}

SEKIZ_TOP = {"tr": ["Kesinlikle evet! ✅", "Hiç şüphe yok.", "Büyük ihtimalle.", "Bambular öyle diyor. 🎋",
                    "Belirtiler evet diyor.", "Şimdi söyleyemem, tekrar sor.", "Sonra tekrar sor, panda uyuyor. 😴",
                    "Buna odaklanıp tekrar sor.", "Pek sanmıyorum.", "Kaynaklarım hayır diyor.", "Hiç sanmam. ❌",
                    "Kod derlenmedi, cevap belirsiz. 🤷"],
             "en": ["Definitely yes! ✅", "Without a doubt.", "Most likely.", "The bamboo says yes. 🎋",
                    "Signs point to yes.", "Can't tell you now, ask again.", "Ask again later, the panda is napping. 😴",
                    "Concentrate and ask again.", "I don't think so.", "My sources say no.", "Very doubtful. ❌",
                    "The code didn't compile, the answer is unclear. 🤷"]}


@komut("panda", "panda logo", "Eğlence", "Kodlardan yapılmış pandayı tekrar çizer", "Draws the panda made of code again")
def k_panda(arg):
    panda_ciz()
    yaz(tr_en("  Şef Panda seni izliyor... 👀", "  Chief Panda is watching you... 👀"), T.ANA)


@komut("pandade", "pandasay", "Eğlence", "Panda senin yerine konuşur (cowsay gibi)", "The panda says what you type (like cowsay)",
       "<metin>", "<text>")
def k_pandade(arg):
    metin = arg or random.choice(SOZLER[dil()])
    satirlar = textwrap.wrap(metin, 40) or [""]
    en = max(len(s) for s in satirlar)
    print(f"   {BEYAZ} {'_' * (en + 2)}")
    for i, s in enumerate(satirlar):
        sol, sag = ("<", ">") if len(satirlar) == 1 else ("/", "\\") if i == 0 else \
                   ("\\", "/") if i == len(satirlar) - 1 else ("|", "|")
        print(f"   {sol} {s:<{en}} {sag}")
    print(f"    {'-' * (en + 2)}{RESET}")
    print(f"{BEYAZ}          \\{RESET}")
    print(f"{BEYAZ}           \\{RESET}")
    for satir in MINI_PANDA:
        print("        " + T.ANA + satir + RESET)


@komut("soz motivasyon", "quote", "Eğlence", "Rastgele motivasyon / kodlama sözü", "A random motivational / coding quote")
def k_soz(arg):
    yaz(f"  💬 \"{random.choice(SOZLER[dil()])}\"", BEYAZ, 0.02)


@komut("fikra saka", "joke", "Eğlence", "Programcı fıkrası anlatır", "Tells a programmer joke")
def k_fikra(arg):
    soru, cevap = random.choice(FIKRALAR[dil()])
    yaz(f"  {soru}", BEYAZ, 0.02)
    time.sleep(1.2)
    yaz(f"  {cevap}", SARI, 0.03)


@komut("bilgi biliyormuydun", "fact", "Eğlence", "Rastgele bilim / teknoloji / panda bilgisi",
       "A random science / tech / panda fact")
def k_bilgi(arg):
    yaz(tr_en("  💡 Biliyor muydun? ", "  💡 Did you know? ") + random.choice(BILGILER[dil()]), BEYAZ, 0.015)


@komut("fal", "fortune", "Eğlence", "Kod falına bakar", "Reads your coding fortune from a coffee cup")
def k_fal(arg):
    for nokta in (tr_en("Fincan çevriliyor", "Turning the coffee cup"), ".", ".", "."):
        sys.stdout.write(f"{GRI}{'  ' if nokta != '.' else ''}{nokta}{RESET}")
        sys.stdout.flush()
        time.sleep(0.4)
    print()
    yaz(f"  🔮 {random.choice(FALLAR[dil()])}", MOR, 0.025)


@komut("8top sihirlitop", "8ball", "Eğlence", "Sihirli 8 topuna evet/hayır sorusu sor",
       "Ask the magic 8-ball a yes/no question", "<soru>", "<question>")
def k_8top(arg):
    if not arg:
        kullanim("8top")
        return
    sys.stdout.write(f"  {GRI}{tr_en('🎱 Top sallanıyor', '🎱 Shaking the ball')}")
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.4)
    print(RESET)
    yaz(f"  🎱 {random.choice(SEKIZ_TOP[dil()])}", BEYAZ, 0.03)


ZAR_YUZLERI = {1: ["       ", "   ●   ", "       "], 2: [" ●     ", "       ", "     ● "],
               3: [" ●     ", "   ●   ", "     ● "], 4: [" ●   ● ", "       ", " ●   ● "],
               5: [" ●   ● ", "   ●   ", " ●   ● "], 6: [" ●   ● ", " ●   ● ", " ●   ● "]}


def zar_satirlari(degerler):
    satirlar = ["  " + "  ".join("┌───────┐" for _ in degerler)]
    for i in range(3):
        satirlar.append("  " + "  ".join(f"│{ZAR_YUZLERI[d][i]}│" for d in degerler))
    satirlar.append("  " + "  ".join("└───────┘" for _ in degerler))
    return [BEYAZ + s + RESET for s in satirlar]


@komut("zar", "dice", "Eğlence", "Zar atar (1-6 tane)", "Rolls dice (1 to 6 of them)", "[adet]", "[count]")
def k_zar(arg):
    try:
        adet = min(max(int(arg or 1), 1), 6)
    except ValueError:
        kullanim("zar")
        return
    for i in range(10):
        degerler = [random.randint(1, 6) for _ in range(adet)]
        yerinde_yaz(zar_satirlari(degerler), i == 0)
        time.sleep(0.05 + i * 0.02)
    soyle(f"🎲 {' + '.join(map(str, degerler))}" + (f" = {BEYAZ}{KALIN}{sum(degerler)}" if adet > 1 else ""))


@komut("yazitura", "coin", "Eğlence", "Yazı tura atar", "Flips a coin")
def k_yazitura(arg):
    donen = "|/-\\"
    yuzler = tr_en(("YAZI", "TURA"), ("HEADS", "TAILS"))
    for i in range(14):
        sys.stdout.write(f"\r  {SARI}{donen[i % 4]} {yuzler[i % 2]}{RESET}  ")
        sys.stdout.flush()
        time.sleep(0.04 + i * 0.015)
    sys.stdout.write(f"\r  🪙 {BEYAZ}{KALIN}{random.choice(yuzler)}!{RESET}\033[K\n")


def gokkusagi_metin(metin, kaydir=0):
    renkli, i = "", kaydir
    for harf in metin:
        if harf.strip():
            renkli += GOKKUSAGI[i % len(GOKKUSAGI)] + harf
            i += 1
        else:
            renkli += harf
    return renkli + RESET


@komut("gokkusagi", "rainbow", "Eğlence", "Metni gökkuşağı renklerine boyar", "Paints text in rainbow colors",
       "<metin>", "<text>")
def k_gokkusagi(arg):
    metin = arg or tr_en("PandaCode gökkuşağı modu!", "PandaCode rainbow mode!")
    if not terminal_mi():
        print("  " + gokkusagi_metin(metin))
        return
    for i in range(18):
        sys.stdout.write("\r  " + gokkusagi_metin(metin, i))
        sys.stdout.flush()
        time.sleep(0.07)
    print()


@komut("glitch", "glitch", "Eğlence", "Metni bozuk-sinyal efektiyle yazar", "Writes text with a broken-signal effect",
       "<metin>", "<text>")
def k_glitch(arg):
    metin = arg or tr_en("SİSTEME HOŞ GELDİN", "WELCOME TO THE SYSTEM")
    semboller = "!@#$%^&*<>?/\\|█▓▒░"
    for adim in range(16):
        oran = 1 - adim / 15
        kare = "".join(random.choice(GOKKUSAGI) + random.choice(semboller)
                       if h.strip() and random.random() < oran else BEYAZ + h for h in metin)
        sys.stdout.write("\r  " + kare + RESET + "\033[K")
        sys.stdout.flush()
        time.sleep(0.06)
    sys.stdout.write(f"\r  {T.ANA}{KALIN}{metin}{RESET}\033[K\n")


@komut("daktilo", "typewriter", "Eğlence", "Metni eski daktilo gibi tık tık yazar",
       "Types text out click-clack, like an old typewriter", "<metin>", "<text>")
def k_daktilo(arg):
    for harf in "  " + (arg or tr_en("Merhaba dünya, ben PandaCode.", "Hello world, I'm PandaCode.")):
        sys.stdout.write(BEYAZ + harf)
        sys.stdout.flush()
        time.sleep(random.uniform(0.03, 0.12))
    print(RESET)


@komut("banner afis buyukyaz", "banner", "Eğlence", "Yazdığını DEV harflerle çizer", "Draws your text in GIANT letters",
       "<metin>", "<text>")
def k_banner(arg):
    metin = arg or "PANDA"
    sinir = genislik() - 4
    satir = ""
    for kelime in metin.split():
        deneme = f"{satir} {kelime}".strip()
        if satir and buyuk_yazi_genisligi(deneme) > sinir:
            for s in buyuk_yazi(satir, GOKKUSAGI):
                print("  " + s)
            print()
            satir = kelime
        else:
            satir = deneme
    for s in buyuk_yazi(satir, GOKKUSAGI):
        print("  " + kes(s, sinir))


@komut("hack nostalji", "hack", "Eğlence", "PandaHack'ten kalma nostalji: tamamen sahte, zararsız bir 'hack' şovu",
       "Nostalgia from PandaHack: a totally fake, harmless 'hacking' show")
def k_hack(arg):
    hedefler = tr_en(["Mahalle bakkalının veresiye defteri", "Komşunun Wi-Fi şifresi",
                      "Okulun karne sistemi", "Kebapçının gizli acı sos tarifi", "Pandanın bambu deposu"],
                     ["The corner shop's IOU notebook", "The neighbor's Wi-Fi password",
                      "The school's report card system", "The kebab shop's secret hot sauce recipe",
                      "The panda's bamboo stash"])
    ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
    yaz(tr_en("  Hedef kilitlendi: ", "  Target locked: ") + random.choice(hedefler), SARI)
    yaz(tr_en(f"  IP adresi: {ip}", f"  IP address: {ip}"), T.KOYU, 0.01)
    for _ in range(8):
        print(T.KOYU + "  " + " ".join(secrets.token_hex(2).upper() for _ in range(12)) + RESET)
        time.sleep(0.08)
    yukleme_cubugu(tr_en("Şifre kırılıyor", "Cracking the password"))
    if random.random() < 0.7:
        yaz(tr_en("  [✓] SIZMA BAŞARILI! (şaka şaka, hiçbir şey yapmadık 😄)",
                  "  [✓] ACCESS GRANTED! (just kidding, we didn't touch anything 😄)"), T.ANA)
    else:
        yaz(tr_en("  [!] YAKALANDIK! Panda kaçıyor... 🐼💨", "  [!] BUSTED! The panda is running away... 🐼💨"), KIRMIZI)


# ═══════════════════════════ KOMUTLAR: GÖRSEL ŞOV ═══════════════════════════
def ekran_gerekli():
    if not terminal_mi():
        hata(tr_en("Bu komut gerçek bir terminal penceresinde çalışır.", "This command needs a real terminal window."))
        return False
    return True


def matrix_yagmuru(sure=None):
    """Tam ekran Matrix yağmuru. 'sure' yoksa bir tuşa basılana kadar yağar."""
    if not terminal_mi():
        return
    karakterler = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789<>{}[]=+*$#"
    en, boy = genislik(), yukseklik()
    sutunlar = list(range(0, en - 1, 2))
    bas = {x: random.randint(-boy, 0) for x in sutunlar}
    uzunluk = {x: random.randint(6, boy) for x in sutunlar}
    hiz = {x: random.choice([1, 1, 1, 2]) for x in sutunlar}
    bitis = time.time() + sure if sure else None
    kare = 0
    with Sahne(tam_ekran=True):
        while True:
            cikti = []
            kare += 1
            for x in sutunlar:
                if kare % hiz[x]:
                    continue
                y = bas[x]
                if 0 <= y < boy:
                    cikti.append(f"{git(y + 1, x + 1)}{BEYAZ}{KALIN}{random.choice(karakterler)}{RESET}")
                if 0 <= y - 1 < boy:
                    cikti.append(f"{git(y, x + 1)}{T.ANA}{random.choice(karakterler)}")
                if 0 <= y - 4 < boy:
                    cikti.append(f"{git(y - 3, x + 1)}{T.KOYU}{random.choice(karakterler)}")
                kuyruk = y - uzunluk[x]
                if 0 <= kuyruk < boy:
                    cikti.append(f"{git(kuyruk + 1, x + 1)} ")
                bas[x] += 1
                if kuyruk >= boy:
                    bas[x] = random.randint(-10, 0)
                    uzunluk[x] = random.randint(6, boy)
            sys.stdout.write("".join(cikti) + RESET)
            sys.stdout.flush()
            if bitis and time.time() > bitis:
                break
            if tus_bekle(0.045):
                break


@komut("matrix", "matrix", "Görsel Şov", "Ekrana Matrix kodu yağdırır (çıkmak için bir tuşa bas)",
       "Makes Matrix code rain down the screen (press any key to exit)", "[saniye]", "[seconds]")
def k_matrix(arg):
    try:
        sure = float(arg) if arg else None
    except ValueError:
        sure = None
    if ekran_gerekli():
        matrix_yagmuru(sure)


@komut("kar", "snow", "Görsel Şov", "Ekrana kar yağdırır, yerde birikir", "Lets it snow; the snow piles up on the ground")
def k_kar(arg):
    if not ekran_gerekli():
        return
    en, boy = genislik(), yukseklik()
    zemin = [boy] * (en + 1)  # her sütunda karın ulaştığı en üst satır
    taneler = []
    onceki = set()
    with Sahne(tam_ekran=True):
        sys.stdout.write(git(1, 2) + GRI + "❄ " + cikis_ipucu() + RESET)
        while True:
            for _ in range(2):
                taneler.append([random.randint(1, en - 1), 2.0, random.uniform(0.15, 0.5), random.choice("*·•+")])
            cizim = {}
            for tane in taneler[:]:
                tane[1] += tane[2]
                if random.random() < 0.3:
                    tane[0] = min(max(1, tane[0] + random.choice((-1, 1))), en - 1)
                x, y = tane[0], int(tane[1])
                if y >= zemin[x] - 1:
                    if zemin[x] > boy - 8:
                        zemin[x] -= 1
                        sys.stdout.write(git(zemin[x], x) + BEYAZ + "█")
                    taneler.remove(tane)
                    continue
                cizim[(y, x)] = tane[3]
            sys.stdout.write("".join(git(y, x) + " " for (y, x) in onceki - set(cizim)))
            sys.stdout.write("".join(f"{git(y, x)}{BEYAZ}{c}" for (y, x), c in cizim.items()) + RESET)
            sys.stdout.flush()
            onceki = set(cizim)
            if tus_bekle(0.06):
                break


@komut("dna", "dna helix", "Görsel Şov", "Dönen bir DNA sarmalı çizer", "Draws a spinning DNA helix")
def k_dna(arg):
    if not ekran_gerekli():
        return
    orta, genlik = 22, 14
    renkler = {"A": KIRMIZI, "T": SARI, "G": CAMGOBEGI, "C": MOR}
    t = 0.0
    with Sahne():
        soyle("🧬 " + cikis_ipucu(), GRI)
        while True:
            x1 = int(orta + genlik * math.sin(t))
            x2 = int(orta - genlik * math.sin(t))
            satir = [" "] * (orta + genlik + 2)
            sol, sag = sorted((x1, x2))
            if sag - sol > 2:
                for x in range(sol + 1, sag):
                    satir[x] = GRI + "─"
            baz = random.choice(["AT", "TA", "GC", "CG"])
            satir[x1] = renkler[baz[0]] + KALIN + baz[0] + RESET
            satir[x2] = renkler[baz[1]] + KALIN + baz[1] + RESET
            print("  " + "".join(satir) + RESET)
            t += 0.28
            if tus_bekle(0.06):
                break


@komut("dalga", "wave", "Görsel Şov", "Ekranda renkli sinüs dalgaları dans eder", "Colorful sine waves dance across the screen")
def k_dalga(arg):
    if not ekran_gerekli():
        return
    en, boy = genislik(), yukseklik()
    orta = boy // 2
    dalgalar = [(boy * 0.35, 0.08, 0, CAMGOBEGI), (boy * 0.25, 0.13, 2, MOR), (boy * 0.15, 0.2, 4, T.ANA)]
    t, onceki = 0.0, set()
    with Sahne(tam_ekran=True):
        while True:
            cizim = {}
            for genlik, frekans, faz, renk in dalgalar:
                for x in range(1, en):
                    y = int(orta + genlik * math.sin(x * frekans + t + faz))
                    if 1 <= y < boy:
                        cizim[(y, x)] = renk
            sys.stdout.write("".join(git(y, x) + " " for (y, x) in onceki - set(cizim)))
            sys.stdout.write("".join(f"{git(y, x)}{r}•" for (y, x), r in cizim.items()) + RESET)
            sys.stdout.write(git(boy, 2) + GRI + cikis_ipucu() + RESET)
            sys.stdout.flush()
            onceki = set(cizim)
            t += 0.15
            if tus_bekle(0.04):
                break


@komut("havaifisek fisek", "fireworks", "Görsel Şov", "Havai fişek gösterisi", "A fireworks show")
def k_havaifisek(arg):
    if not ekran_gerekli():
        return
    en, boy = genislik(), yukseklik()
    roketler, parcaciklar, onceki = [], [], set()
    with Sahne(tam_ekran=True):
        while True:
            if random.random() < 0.07 or not (roketler or parcaciklar):
                roketler.append({"x": random.randint(8, max(9, en - 8)), "y": float(boy - 1),
                                 "hedef": random.randint(3, max(4, boy // 2)), "renk": random.choice(GOKKUSAGI)})
            cizim = {}
            for roket in roketler[:]:
                roket["y"] -= 0.9
                if roket["y"] <= roket["hedef"]:
                    roketler.remove(roket)
                    for i in range(36):
                        aci, guc = 2 * math.pi * i / 36, random.uniform(0.4, 1.1)
                        parcaciklar.append([float(roket["x"]), roket["y"], math.cos(aci) * guc * 2,
                                            math.sin(aci) * guc, random.randint(12, 22), roket["renk"]])
                else:
                    cizim[(int(roket["y"]), roket["x"])] = (BEYAZ, "|")
            for p in parcaciklar[:]:
                p[0] += p[2]
                p[1] += p[3]
                p[2] *= 0.95
                p[3] += 0.05
                p[4] -= 1
                x, y = int(p[0]), int(p[1])
                if p[4] <= 0 or not (1 <= x < en and 1 <= y < boy):
                    parcaciklar.remove(p)
                    continue
                cizim[(y, x)] = (p[5], "*" if p[4] > 12 else "+" if p[4] > 6 else ".")
            sys.stdout.write("".join(git(y, x) + " " for (y, x) in onceki - set(cizim)))
            sys.stdout.write("".join(f"{git(y, x)}{r}{c}" for (y, x), (r, c) in cizim.items()) + RESET)
            sys.stdout.flush()
            onceki = set(cizim)
            if tus_bekle(0.05):
                break


@komut("dijital buyuksaat", "clock", "Görsel Şov", "Dev rakamlı canlı dijital saat", "A live digital clock with giant digits")
def k_dijital(arg):
    ilk = True
    with Sahne():
        while True:
            simdi = time.localtime()
            ayirici = ":" if simdi.tm_sec % 2 == 0 else " "
            metin = time.strftime(f"%H{ayirici}%M{ayirici}%S", simdi)
            yerinde_yaz(["  " + T.ANA + KALIN + s for s in buyuk_yazi(metin)]
                        + [f"  {GRI}{gun_adi(datetime.date.today())}, {time.strftime('%d.%m.%Y')}"
                           f"  —  {cikis_ipucu()}{RESET}"], ilk)
            ilk = False
            if not terminal_mi() or tus_bekle(0.25):
                break


@komut("hayat", "life", "Görsel Şov", "Conway'in Hayat Oyunu: hücreler doğar, yaşar, ölür",
       "Conway's Game of Life: cells are born, live and die")
def k_hayat(arg):
    if not ekran_gerekli():
        return
    en, boy = genislik() - 1, yukseklik() - 2
    yeni_dunya = lambda: [[random.random() < 0.25 for _ in range(en)] for _ in range(boy)]
    dunya, nesil = yeni_dunya(), 0
    with Sahne(tam_ekran=True):
        while True:
            cizim = "\n".join("".join("█" if h else " " for h in satir) for satir in dunya)
            canli = sum(map(sum, dunya))
            sys.stdout.write(git(1, 1) + T.ANA + cizim + RESET + git(boy + 1, 1) + GRI +
                             tr_en(f"Nesil: {nesil}  Canlı hücre: {canli}   [r] yeniden başlat  [q] çık",
                                   f"Generation: {nesil}  Live cells: {canli}   [r] restart  [q] quit") + f"{RESET}\033[K")
            sys.stdout.flush()
            yeni = []
            for y in range(boy):
                ust, orta, alt = dunya[y - 1], dunya[y], dunya[(y + 1) % boy]
                satir = []
                for x in range(en):
                    sol, sag = x - 1, (x + 1) % en
                    komsu = ust[sol] + ust[x] + ust[sag] + orta[sol] + orta[sag] + alt[sol] + alt[x] + alt[sag]
                    satir.append(komsu == 3 or (orta[x] and komsu == 2))
                yeni.append(satir)
            dunya, nesil = yeni, nesil + 1
            tus = tus_bekle(0.07)
            if tus in ("r", "R"):
                dunya, nesil = yeni_dunya(), 0
            elif tus:
                break


@komut("labirent", "maze", "Görsel Şov", "Rastgele labirent üretir ve kendi kendine çözer",
       "Generates a random maze and solves it by itself")
def k_labirent(arg):
    if not ekran_gerekli():
        return
    en = min(genislik() - 2, 99) // 2 * 2 - 1
    boy = (yukseklik() - 3) // 2 * 2 - 1
    if en < 11 or boy < 7:
        hata(tr_en("Pencere çok küçük, biraz büyüt.", "The window is too small, make it a bit bigger."))
        return
    izgara = [["█"] * en for _ in range(boy)]
    ciz = lambda x, y, metin: sys.stdout.write(git(y + 2, x + 2) + metin)
    with Sahne(tam_ekran=True):
        sys.stdout.write(git(1, 2) + f"{T.ANA}{KALIN}🧩 {tr_en('Labirent kazılıyor...', 'Digging the maze...')}{RESET}")
        for y in range(boy):
            ciz(0, y, T.KOYU + "".join(izgara[y]))
        yigin, animasyon, adim = [(1, 1)], True, 0
        izgara[1][1] = " "
        while yigin:
            x, y = yigin[-1]
            komsular = [(x + dx, y + dy, dx, dy) for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2))
                        if 0 < x + dx < en - 1 and 0 < y + dy < boy - 1 and izgara[y + dy][x + dx] == "█"]
            if not komsular:
                yigin.pop()
                continue
            nx, ny, dx, dy = random.choice(komsular)
            izgara[y + dy // 2][x + dx // 2] = izgara[ny][nx] = " "
            ciz(x + dx // 2, y + dy // 2, " ")
            ciz(nx, ny, " ")
            yigin.append((nx, ny))
            adim += 1
            if animasyon and adim % 3 == 0:
                sys.stdout.flush()
                if tus_bekle(0.004):
                    animasyon = False
        baslangic, hedef = (1, 1), (en - 2, boy - 2)
        onceki, kuyruk = {baslangic: None}, deque([baslangic])
        while kuyruk:
            x, y = kuyruk.popleft()
            if (x, y) == hedef:
                break
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                komsu = (x + dx, y + dy)
                if izgara[komsu[1]][komsu[0]] == " " and komsu not in onceki:
                    onceki[komsu] = (x, y)
                    kuyruk.append(komsu)
        yol, nokta = [], hedef
        while nokta:
            yol.append(nokta)
            nokta = onceki[nokta]
        sys.stdout.write(git(1, 2) + f"{T.ANA}{KALIN}🧩 {tr_en('Panda çıkışı arıyor...', 'The panda is looking for the exit...')}"
                                     f"\033[K{RESET}")
        for x, y in reversed(yol):
            ciz(x, y, SARI + KALIN + "•")
            sys.stdout.flush()
            time.sleep(0.01)
        ciz(*baslangic, T.ANA + KALIN + "@")
        ciz(*hedef, KIRMIZI + KALIN + "X")
        sys.stdout.write(git(1, 2) + f"{T.ANA}{KALIN}🧩 "
                         + tr_en(f"Çözüldü! Yol uzunluğu: {len(yol)} adım. ", f"Solved! Path length: {len(yol)} steps. ")
                         + f"{GRI}{tr_en('(bir tuşa bas)', '(press any key)')}{RESET}\033[K")
        sys.stdout.flush()
        tus_oku()


@komut("mandelbrot fraktal", "mandelbrot fractal", "Görsel Şov", "Ünlü Mandelbrot fraktalını renkli çizer",
       "Draws the famous Mandelbrot fractal in color")
def k_mandelbrot(arg):
    en = min(genislik() - 2, 140)
    adim_x = 3.3 / en
    adim_y = adim_x * 2.1
    boy = min(yukseklik() - 3, int(2.5 / adim_y))
    palet = [17, 18, 19, 20, 21, 27, 33, 39, 45, 51, 50, 49, 48, 47, 46, 82, 118, 154, 190, 226, 220, 214, 208, 202, 196]
    karakterler = ".:-=+*#%@"
    en_fazla = 60
    for satir in range(boy):
        ci = (satir - boy / 2) * adim_y
        cikti = ""
        for sutun in range(en):
            c = complex(-2.35 + sutun * adim_x, ci)
            z, n = 0j, 0
            while abs(z) <= 2 and n < en_fazla:
                z = z * z + c
                n += 1
            if n == en_fazla:
                cikti += " "
            else:
                cikti += f"\033[38;5;{palet[n % len(palet)]}m{karakterler[min(n // 3, len(karakterler) - 1)]}"
        print("  " + cikti + RESET)


@komut("renkler palet", "colors palette", "Görsel Şov", "Terminalinin gösterebildiği renk paletini sergiler",
       "Shows off the colors your terminal can display")
def k_renkler(arg):
    soyle(tr_en("16 temel renk:", "16 basic colors:"), GRI)
    print("  " + "".join(f"\033[48;5;{i}m   " for i in range(16)) + RESET)
    soyle(tr_en("256 renk paleti:", "256-color palette:"), GRI)
    for satir in range(6):
        print("  " + "".join(f"\033[48;5;{16 + satir * 36 + i}m  " for i in range(36)) + RESET)
    print("  " + "".join(f"\033[48;5;{i}m  " for i in range(232, 256)) + RESET)
    soyle(tr_en("Gerçek renk (true color) geçişi:", "True color gradient:"), GRI)
    en = min(72, genislik() - 4)
    gecis = ""
    for i in range(en):
        r, g, b = (int(127 + 127 * math.sin(i / en * 2 * math.pi + faz)) for faz in (0, 2.1, 4.2))
        gecis += f"\033[48;2;{r};{g};{b}m "
    print("  " + gecis + RESET)


@komut("yukleniyor", "loading spinner", "Görsel Şov", "Bir sürü havalı yükleme animasyonu", "A bunch of cool loading animations")
def k_yukleniyor(arg):
    donguler = [(tr_en("Bambu toplanıyor", "Gathering bamboo"), "|/-\\"),
                (tr_en("Panda düşünüyor", "The panda is thinking"), "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"),
                (tr_en("Kod derleniyor", "Compiling code"), "▁▂▃▄▅▆▇█▇▆▅▄▃▂"),
                (tr_en("Dünya dönüyor", "Spinning the globe"), "◐◓◑◒"),
                (tr_en("Veri aktarılıyor", "Transferring data"),
                 ["[=    ]", "[ =   ]", "[  =  ]", "[   = ]", "[    =]", "[   = ]", "[  =  ]", "[ =   ]"]),
                (tr_en("Sinyal aranıyor", "Searching for a signal"), ["▂   ", "▂▄  ", "▂▄▆ ", "▂▄▆█", "    "])]
    with Sahne():
        for etiket, kareler in donguler:
            for i in range(24):
                sys.stdout.write(f"\r  {T.ANA}{kareler[i % len(kareler)]}{RESET} {BEYAZ}{etiket}...{RESET}\033[K")
                sys.stdout.flush()
                if tus_bekle(0.07):
                    print()
                    return
            sys.stdout.write(f"\r  {YESIL}✓{RESET} {etiket} {GRI}{tr_en('tamam', 'done')}{RESET}\033[K\n")
    yukleme_cubugu(tr_en("Her şey hazır", "All set"))


DANS_KARELERI = [
    ["   \\ʕ•ᴥ•ʔ/  ", "     |  |    ", "    _/  \\_   "],
    ["    ʕ•ᴥ•ʔ    ", "   /|  |\\   ", "    _/  \\_   "],
    ["   \\ʕ•ᴥ•ʔ   ", "     |  |\\  ", "     /  \\_   "],
    ["    ʕ•ᴥ•ʔ/  ", "   /|  |     ", "   _/  \\    "],
    ["   \\ʕ-ᴥ-ʔ/  ", "     |  |    ", "    <  >     "],
]


@komut("dans", "dance", "Görsel Şov", "Panda dans eder", "The panda dances")
def k_dans(arg):
    ilk, i = True, 0
    notalar = ["♪", "♫", "♬", " "]
    with Sahne():
        while True:
            kare = DANS_KARELERI[i % len(DANS_KARELERI)]
            nota = lambda: random.choice(GOKKUSAGI) + random.choice(notalar) + RESET
            yerinde_yaz([f"  {nota()}  {T.ANA}{KALIN}{kare[0]}{RESET}  {nota()}",
                         f"     {BEYAZ}{kare[1]}{RESET}",
                         f"     {BEYAZ}{kare[2]}{RESET}",
                         f"  {GRI}{cikis_ipucu()}{RESET}"], ilk)
            ilk, i = False, i + 1
            if not terminal_mi() or tus_bekle(0.3):
                break


# ═══════════════════════════ KOMUTLAR: OYUNLAR ═══════════════════════════
@komut("tahmin", "guess", "Oyunlar", "1-100 arası sayıyı tahmin et", "Guess the number between 1 and 100")
def k_tahmin(arg):
    hedef, deneme = random.randint(1, 100), 0
    soyle(tr_en("🎯 1 ile 100 arasında bir sayı tuttum. Bil bakalım! (çıkmak için q)",
                "🎯 I'm thinking of a number between 1 and 100. Can you guess it? (q to quit)"))
    while True:
        cevap = sor(tr_en("Tahminin: ", "Your guess: "))
        if sadelestir(cevap) in ("q", "cikis", "exit", "quit"):
            soyle(tr_en(f"Pes mi ediyorsun? Sayı {hedef} idi. 🐼", f"Giving up? The number was {hedef}. 🐼"), GRI)
            return
        try:
            tahmin = int(cevap)
        except ValueError:
            hata(tr_en("Sayı yazmalısın.", "You need to type a number."))
            continue
        deneme += 1
        fark = abs(tahmin - hedef)
        if fark == 0:
            soyle(tr_en(f"🎉 BİLDİN! {deneme} denemede buldun.",
                        f"🎉 YOU GOT IT! Found it in {deneme} {'try' if deneme == 1 else 'tries'}."), YESIL + KALIN)
            if rekor_kontrol("tahmin", deneme, buyuk_iyi=False):
                soyle(tr_en("🏆 YENİ REKOR!", "🏆 NEW RECORD!"), SARI)
            return
        yon = tr_en("⬆ Daha BÜYÜK", "⬆ HIGHER") if tahmin < hedef else tr_en("⬇ Daha KÜÇÜK", "⬇ LOWER")
        isi = (tr_en("🔥 çok sıcak!", "🔥 very hot!") if fark <= 3 else
               tr_en("♨ sıcak", "♨ warm") if fark <= 10 else tr_en("❄ soğuk", "❄ cold"))
        soyle(f"{yon}  {GRI}({isi})")


ADAM_KELIMELERI = {"tr": ["python", "panda", "bambu", "klavye", "terminal", "algoritma", "degisken", "fonksiyon",
                          "dongu", "derleyici", "sunucu", "piksel", "yazilim", "donanim", "internet", "sifre",
                          "veritabani", "kutuphane", "modul", "sozluk", "liste", "ekran", "islemci", "bellek",
                          "robot", "yapayzeka", "kodlama", "bilgisayar", "tarayici", "uygulama"],
                   "en": ["python", "panda", "bamboo", "keyboard", "terminal", "algorithm", "variable", "function",
                          "loop", "compiler", "server", "pixel", "software", "hardware", "internet", "password",
                          "database", "library", "module", "dictionary", "list", "screen", "processor", "memory",
                          "robot", "keyword", "coding", "computer", "browser", "application"]}


def adam_ciz(yanlis):
    parca = lambda n, c: c if yanlis >= n else " "
    return [f"  {BEYAZ}┌───┐",
            f"  │   {parca(1, 'O')}",
            f"  │  {parca(3, '/')}{parca(2, '|')}{parca(4, chr(92))}",
            f"  │  {parca(5, '/')} {parca(6, chr(92))}",
            f" ─┴─{RESET}"]


@komut("adamasmaca", "hangman", "Oyunlar", "Kodlama kelimeleriyle adam asmaca", "Hangman with coding words")
def k_adamasmaca(arg):
    kelime = random.choice(ADAM_KELIMELERI[dil()])
    bilinen, yanlislar = set(), []
    while True:
        for satir in adam_ciz(len(yanlislar)):
            print(satir)
        gorunen = " ".join(h if h in bilinen else "_" for h in kelime)
        yanlis = " ".join(yanlislar) or "-"
        soyle(tr_en(f"Kelime: {BEYAZ}{KALIN}{gorunen}{RESET}   {GRI}Yanlışlar: {yanlis}",
                    f"Word: {BEYAZ}{KALIN}{gorunen}{RESET}   {GRI}Misses: {yanlis}"))
        if all(h in bilinen for h in kelime):
            soyle(tr_en(f"🎉 KAZANDIN! Kelime: {kelime}", f"🎉 YOU WIN! The word was: {kelime}"), YESIL + KALIN)
            return
        if len(yanlislar) >= 6:
            soyle(tr_en(f"💀 Adam asıldı! Kelime: {kelime}", f"💀 You've been hanged! The word was: {kelime}"), KIRMIZI + KALIN)
            return
        tahmin = sadelestir(sor(tr_en("Harf (ya da kelimenin tamamı, çıkmak için 0): ",
                                      "Letter (or the whole word, 0 to quit): ")))
        if tahmin == "0":
            soyle(tr_en(f"Kelime '{kelime}' idi.", f"The word was '{kelime}'."), GRI)
            return
        if len(tahmin) > 1:
            if tahmin == kelime:
                bilinen.update(kelime)
            else:
                yanlislar.append(tahmin)
        elif tahmin and tahmin.isalpha():
            if tahmin in bilinen or tahmin in yanlislar:
                hata(tr_en("Bunu zaten denedin.", "You already tried that."))
            elif tahmin in kelime:
                bilinen.add(tahmin)
            else:
                yanlislar.append(tahmin)
        print()


XOX_HATLARI = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def xox_kazanan(tahta):
    for a, b, c in XOX_HATLARI:
        if tahta[a] != " " and tahta[a] == tahta[b] == tahta[c]:
            return tahta[a]
    return "berabere" if " " not in tahta else None


def xox_minimax(tahta, sira):
    """Bilgisayar (O) için en iyi hamleyi bulur: her ihtimali sonuna kadar dener."""
    kazanan = xox_kazanan(tahta)
    if kazanan:
        return {"O": 1, "X": -1, "berabere": 0}[kazanan], None
    en_iyi = (-2, None) if sira == "O" else (2, None)
    for i in range(9):
        if tahta[i] == " ":
            tahta[i] = sira
            puan, _ = xox_minimax(tahta, "X" if sira == "O" else "O")
            tahta[i] = " "
            if (sira == "O" and puan > en_iyi[0]) or (sira == "X" and puan < en_iyi[0]):
                en_iyi = (puan, i)
    return en_iyi


def xox_ciz(tahta):
    renk = {"X": T.ANA + KALIN, "O": KIRMIZI + KALIN}
    for satir in range(3):
        hucreler = [renk[tahta[i]] + tahta[i] + RESET if tahta[i] != " " else GRI + str(i + 1) + RESET
                    for i in range(satir * 3, satir * 3 + 3)]
        print(f"     {hucreler[0]} │ {hucreler[1]} │ {hucreler[2]}")
        if satir < 2:
            print("    ───┼───┼───")


@komut("xox", "tictactoe", "Oyunlar", "Pandaya karşı XOX (tic-tac-toe)", "Tic-tac-toe against the panda")
def k_xox(arg):
    tahta = [" "] * 9
    soyle(tr_en("❌ Sen X'sin, panda O. Kutu numarasını yaz (1-9), çıkmak için q.",
                "❌ You're X, the panda is O. Type a square's number (1-9), q to quit."))
    while True:
        print()
        xox_ciz(tahta)
        kazanan = xox_kazanan(tahta)
        if kazanan:
            mesaj = {"X": (tr_en("🎉 KAZANDIN! Pandayı yendin!", "🎉 YOU WIN! You beat the panda!"), YESIL),
                     "O": (tr_en("🐼 Panda kazandı! Bir daha dene.", "🐼 The panda wins! Try again."), KIRMIZI),
                     "berabere": (tr_en("🤝 Berabere!", "🤝 It's a draw!"), SARI)}[kazanan]
            soyle(*mesaj)
            return
        cevap = sor(tr_en("Hamlen: ", "Your move: "))
        if sadelestir(cevap) == "q":
            return
        if not (cevap.isdigit() and 1 <= int(cevap) <= 9 and tahta[int(cevap) - 1] == " "):
            hata(tr_en("Boş bir kutunun numarasını yaz (1-9).", "Type the number of an empty square (1-9)."))
            continue
        tahta[int(cevap) - 1] = "X"
        if xox_kazanan(tahta) or " " not in tahta:
            continue
        if random.random() < 0.2:  # panda bazen dalgın, yenilebilsin :)
            hamle = random.choice([i for i in range(9) if tahta[i] == " "])
        else:
            hamle = xox_minimax(tahta, "O")[1]
        tahta[hamle] = "O"
        soyle(tr_en(f"🐼 Panda {hamle + 1} numaraya oynadı.", f"🐼 The panda played square {hamle + 1}."), GRI)


TKM_SKOR = {"sen": 0, "panda": 0}


@komut("tkm taskagitmakas", "rps", "Oyunlar", "Taş-kâğıt-makas", "Rock-paper-scissors",
       "<tas|kagit|makas>", "<rock|paper|scissors>")
def k_tkm(arg):
    secimler = {"tas": tr_en("🪨 Taş", "🪨 Rock"), "kagit": tr_en("📄 Kâğıt", "📄 Paper"),
                "makas": tr_en("✂️  Makas", "✂️  Scissors")}
    yener = {"tas": "makas", "kagit": "tas", "makas": "kagit"}
    ingilizce = {"rock": "tas", "paper": "kagit", "scissors": "makas"}
    anla = lambda metin: ingilizce.get(sadelestir(metin), sadelestir(metin))  # 'rock' → 'tas'
    senin = anla(arg)
    if senin not in secimler:
        senin = anla(sor(tr_en("Taş, kâğıt, makas? ", "Rock, paper, scissors? ")))
        if senin not in secimler:
            kullanim("tkm")
            return
    pandanin = random.choice(list(secimler))
    for kelime in tr_en(("Taş...", "Kâğıt...", "Makas!"), ("Rock...", "Paper...", "Scissors!")):
        sys.stdout.write(f"  {SARI}{kelime}{RESET}")
        sys.stdout.flush()
        time.sleep(0.35)
    print()
    soyle(tr_en(f"Sen: {secimler[senin]}   Panda: {secimler[pandanin]}",
                f"You: {secimler[senin]}   Panda: {secimler[pandanin]}"), BEYAZ)
    if senin == pandanin:
        soyle(tr_en("🤝 Berabere!", "🤝 It's a draw!"), SARI)
    elif yener[senin] == pandanin:
        TKM_SKOR["sen"] += 1
        soyle(tr_en("🎉 Kazandın!", "🎉 You win!"), YESIL)
    else:
        TKM_SKOR["panda"] += 1
        soyle(tr_en("🐼 Panda kazandı!", "🐼 The panda wins!"), KIRMIZI)
    soyle(tr_en(f"Skor → Sen {TKM_SKOR['sen']} - {TKM_SKOR['panda']} Panda",
                f"Score → You {TKM_SKOR['sen']} - {TKM_SKOR['panda']} Panda"), GRI)


@komut("yilan", "snake", "Oyunlar", "Klasik yılan oyunu: oklarla bambuları topla",
       "Classic snake: collect bamboo with the arrow keys")
def k_yilan(arg):
    if not ekran_gerekli():
        return
    en, boy = min(genislik() - 4, 60), min(yukseklik() - 5, 20)
    if en < 20 or boy < 8:
        hata(tr_en("Pencere çok küçük, biraz büyüt.", "The window is too small, make it a bit bigger."))
        return
    yonler = {"YUKARI": (0, -1), "ASAGI": (0, 1), "SOL": (-1, 0), "SAG": (1, 0),
              "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
    yilan = [(en // 2 - i, boy // 2) for i in range(3)]
    yon, puan = (1, 0), 0
    hucre = lambda x, y, metin: sys.stdout.write(git(y + 3, x + 2) + metin)

    def yeni_yem():
        while True:
            yer = (random.randrange(en), random.randrange(boy))
            if yer not in yilan:
                return yer

    yem = yeni_yem()
    rekor = VERI["rekorlar"].get("yilan", 0)
    with Sahne(tam_ekran=True):
        sys.stdout.write(git(2, 1) + T.KOYU + "┌" + "─" * en + "┐")
        for y in range(boy):
            sys.stdout.write(git(y + 3, 1) + "│" + git(y + 3, en + 2) + "│")
        sys.stdout.write(git(boy + 3, 1) + "└" + "─" * en + "┘" + RESET)
        for x, y in yilan:
            hucre(x, y, T.ANA + "o")
        hucre(*yem, YESIL + KALIN + "Ψ")
        while True:
            sys.stdout.write(git(1, 1) + f"{T.ANA}{KALIN}🐍 {tr_en('YILAN', 'SNAKE')}{RESET}  "
                                         f"{tr_en('Puan', 'Score')}: {BEYAZ}{puan}{RESET}  "
                                         f"{tr_en('Rekor', 'Best')}: {SARI}{max(rekor, puan)}{RESET}  "
                                         f"{GRI}{tr_en('oklar/WASD • q çık', 'arrows/WASD • q quit')}{RESET}\033[K")
            sys.stdout.flush()
            yeni_yon = yon
            bitis = time.time() + max(0.05, 0.14 - puan * 0.004)
            while time.time() < bitis:
                if tus_var():
                    tus = tus_oku()
                    if tus in ("q", "Q", "ESC"):
                        return
                    aday = yonler.get(tus.lower() if len(tus) == 1 else tus)
                    if aday and (aday[0] != -yon[0] or aday[1] != -yon[1]):
                        yeni_yon = aday
                time.sleep(0.005)
            yon = yeni_yon
            bas = (yilan[0][0] + yon[0], yilan[0][1] + yon[1])
            yiyor = bas == yem
            govde = yilan if yiyor else yilan[:-1]
            if not (0 <= bas[0] < en and 0 <= bas[1] < boy) or bas in govde:
                break
            yilan.insert(0, bas)
            hucre(*yilan[1], T.ANA + "o")
            hucre(*bas, BEYAZ + KALIN + "@")
            if yiyor:
                puan += 1
                yem = yeni_yem()
                hucre(*yem, YESIL + KALIN + "Ψ")
            else:
                hucre(*yilan.pop(), " ")
        yeni_rekor = puan > 0 and rekor_kontrol("yilan", puan)
        rekor_yazisi = tr_en("🏆 YENİ REKOR!", "🏆 NEW RECORD!") if yeni_rekor else ""
        mesaj = f" {tr_en('OYUN BİTTİ! Puan', 'GAME OVER! Score')}: {puan} {rekor_yazisi} "
        sys.stdout.write(git(boy // 2 + 3, max(2, en // 2 - len(mesaj) // 2)) + TERS + KIRMIZI + KALIN + mesaj + RESET)
        sys.stdout.write(git(boy // 2 + 4, max(2, en // 2 - 10)) + GRI
                         + tr_en("(devam için bir tuşa bas)", "(press any key to continue)") + RESET)
        sys.stdout.flush()
        time.sleep(0.6)
        tuslari_bosalt()
        tus_oku()


YAZI_CUMLELERI = {"tr": [
    "Panda bambu yerken kod yazmayı da ihmal etmez.",
    "Bugün küçük bir adım at, yarın büyük bir program yaz.",
    "Klavyede hızlı olmak için önce doğru yazmayı öğren.",
    "Python öğrenmek eğlenceli ve çok faydalıdır.",
    "Her hata seni daha iyi bir programcı yapar.",
    "Terminal ekranı siyah olabilir ama fikirlerin renkli olsun.",
    "Döngüler, koşullar ve fonksiyonlar programlamanın temelidir.",
], "en": [
    "A panda never forgets to write code while eating bamboo.",
    "Take a small step today and write a big program tomorrow.",
    "To type fast, first learn to type correctly.",
    "Learning Python is fun and very useful.",
    "Every mistake makes you a better programmer.",
    "The terminal screen may be black, but your ideas can be colorful.",
    "Loops, conditions and functions are the basics of programming.",
]}


@komut("yazhizi", "typing wpm", "Oyunlar", "Klavye hız testi: dakikada kaç kelime yazıyorsun?",
       "Typing test: how many words per minute can you type?")
def k_yazhizi(arg):
    cumle = random.choice(YAZI_CUMLELERI[dil()])
    soyle(tr_en("Aşağıdaki cümleyi olabildiğince hızlı ve doğru yaz:",
                "Type the sentence below as fast and as accurately as you can:"), GRI)
    print(f"\n  {BEYAZ}{KALIN}{cumle}{RESET}\n")
    sor(tr_en("Hazır olunca Enter'a bas...", "Press Enter when you're ready..."))
    baslangic = time.time()
    yazilan = input(f"  {T.ANA}> {RESET}")
    sure = max(time.time() - baslangic, 0.1)
    dogruluk = difflib.SequenceMatcher(None, cumle, yazilan).ratio() * 100
    kelime_dakika = len(yazilan) / 5 / (sure / 60) * dogruluk / 100
    karsilastirma = "".join((YESIL if i < len(cumle) and h == cumle[i] else KIRMIZI) + h
                            for i, h in enumerate(yazilan))
    print(f"  {GRI}{tr_en('Sen:', 'You:')}{RESET} {karsilastirma}{RESET}")
    soyle(tr_en(f"⏱  {sure:.1f} sn  •  🎯 %{dogruluk:.0f} doğruluk  •  ⚡ {BEYAZ}{KALIN}{kelime_dakika:.0f} kelime/dk",
                f"⏱  {sure:.1f} s  •  🎯 {dogruluk:.0f}% accuracy  •  ⚡ {BEYAZ}{KALIN}{kelime_dakika:.0f} WPM"))
    if dogruluk < 70:
        soyle(tr_en("Doğruluk çok düşük, bu tur sayılmadı. Önce doğru, sonra hızlı! 🐢",
                    "Accuracy is too low, this round doesn't count. Accurate first, fast later! 🐢"), KIRMIZI)
        return
    seviye = ((tr_en("🐢 Kaplumbağa", "🐢 Turtle"), 20), ("🐼 Panda", 35), (tr_en("🐇 Tavşan", "🐇 Rabbit"), 50),
              (tr_en("🐆 Çita", "🐆 Cheetah"), 70), (tr_en("🚀 Roket", "🚀 Rocket"), 9999))
    soyle(tr_en("Seviyen: ", "Your level: ") + next(ad for ad, sinir in seviye if kelime_dakika < sinir), SARI)
    if rekor_kontrol("yazhizi", round(kelime_dakika)):
        soyle(tr_en("🏆 YENİ REKOR!", "🏆 NEW RECORD!"), SARI)


@komut("islem", "mathquiz", "Oyunlar", "Hızlı zihinden matematik yarışı (10 soru)", "A quick mental math race (10 questions)")
def k_islem(arg):
    dogru, baslangic = 0, time.time()
    soyle(tr_en("🧮 10 soru geliyor, hızlı ol! (çıkmak için q)", "🧮 10 questions coming up, be quick! (q to quit)"))
    for no in range(1, 11):
        islem = random.choice("+-×")
        if islem == "×":
            a, b = random.randint(2, 12), random.randint(2, 12)
            cevap = a * b
        else:
            a, b = random.randint(5, 99), random.randint(2, 50)
            cevap = a + b if islem == "+" else a - b
        yanit = sor(f"{no:>2}) {a} {islem} {b} = ")
        if sadelestir(yanit) == "q":
            return
        if yanit.lstrip("-").isdigit() and int(yanit) == cevap:
            dogru += 1
            soyle("✓", YESIL)
        else:
            soyle(tr_en(f"✗ doğrusu {cevap}", f"✗ the answer is {cevap}"), KIRMIZI)
    sure = time.time() - baslangic
    soyle(tr_en(f"🏁 {dogru}/10 doğru, {sure:.1f} saniyede.", f"🏁 {dogru}/10 correct in {sure:.1f} seconds."), BEYAZ + KALIN)
    if dogru == 10 and rekor_kontrol("islem_sure", round(sure, 1), buyuk_iyi=False):
        soyle(tr_en("🏆 YENİ REKOR! (10/10 en hızlı)", "🏆 NEW RECORD! (fastest 10/10)"), SARI)


@komut("hafiza", "memory", "Oyunlar", "Ekranda beliren sayıyı ezberle, her tur uzar",
       "Memorize the number on the screen; it gets longer every round")
def k_hafiza(arg):
    uzunluk = 3
    soyle(tr_en("🧠 Sayı kısa süre görünecek, sonra kaybolacak. Aynen yaz!",
                "🧠 A number will show up for a moment, then vanish. Type it back exactly!"))
    time.sleep(1)
    while True:
        dizi = "".join(random.choice(string.digits) for _ in range(uzunluk))
        print(f"  {SARI}{tr_en('Ezberle:', 'Memorize:')}{RESET} {BEYAZ}{KALIN}{dizi}{RESET}")
        time.sleep(1 + uzunluk * 0.35)
        sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
        tuslari_bosalt()
        cevap = sor(tr_en("Sayı neydi? ", "What was the number? "))
        if cevap != dizi:
            soyle(tr_en(f"✗ Yanlış! Doğrusu {dizi} idi. Ulaştığın seviye: {uzunluk - 1} basamak",
                        f"✗ Wrong! It was {dizi}. You made it to {uzunluk - 1} digits"), KIRMIZI)
            if uzunluk > 3 and rekor_kontrol("hafiza", uzunluk - 1):
                soyle(tr_en("🏆 YENİ REKOR!", "🏆 NEW RECORD!"), SARI)
            return
        soyle(tr_en(f"✓ Doğru! Şimdi {uzunluk + 1} basamak...", f"✓ Correct! Now {uzunluk + 1} digits..."), YESIL)
        uzunluk += 1


BILMECELER = {"tr": [
    ("Tuşları var ama kilit açmaz, boşluğu var ama oda değil. Nedir?", ["klavye"]),
    ("Ağzı var konuşmaz, yatağı var uyumaz. Nedir?", ["nehir", "irmak", "dere"]),
    ("Ne kadar çok kurularsa o kadar ıslanır. Nedir?", ["havlu"]),
    ("Senindir ama başkaları senden çok kullanır. Nedir?", ["isim", "ad", "adin", "ismin"]),
    ("Kullanmadan önce kırman gerekir. Nedir?", ["yumurta"]),
    ("Faresi var ama kedisi yok. Nedir?", ["bilgisayar", "pc"]),
    ("Elleri var ama alkışlayamaz. Nedir?", ["saat"]),
    ("Pencereleri var ama bir evi yok. Nedir? (ipucu: işletim sistemi)", ["windows"]),
    ("Siyah beyazdır, bambu yer, bu terminalin şefidir. Kimdir?", ["panda"]),
    ("Sadece 0 ve 1 bilir ama her şeyi anlatır. Nedir?", ["ikili", "binary", "ikilik", "ikili sistem"]),
    ("Ne kadar çok alırsan arkanda o kadar çok bırakırsın. Nedir?", ["adim", "ayak izi", "iz", "adimlar"]),
    ("Hep önündedir ama asla göremezsin. Nedir?", ["gelecek", "yarin"]),
], "en": [
    ("It has keys but opens no locks, and a space but no room. What is it?", ["keyboard", "a keyboard"]),
    ("It has a mouth but never talks, and a bed but never sleeps. What is it?", ["river", "a river", "stream"]),
    ("The more it dries, the wetter it gets. What is it?", ["towel", "a towel"]),
    ("It belongs to you, but other people use it more than you do. What is it?", ["name", "your name", "my name"]),
    ("You have to break it before you can use it. What is it?", ["egg", "an egg"]),
    ("It has a mouse but no cat. What is it?", ["computer", "a computer", "pc"]),
    ("It has hands but can't clap. What is it?", ["clock", "a clock", "watch"]),
    ("It has windows but no house. What is it? (hint: an operating system)", ["windows"]),
    ("It's black and white, eats bamboo and runs this terminal. Who is it?", ["panda", "a panda", "the panda"]),
    ("It only knows 0 and 1, yet it can say anything. What is it?", ["binary", "binary code"]),
    ("The more you take, the more you leave behind. What are they?", ["footsteps", "steps", "footprints"]),
    ("It's always in front of you, but you can never see it. What is it?", ["future", "the future", "tomorrow"]),
]}


@komut("bilmece", "riddle", "Oyunlar", "Bilmece sorar, bil bakalım", "Asks you a riddle; can you solve it?")
def k_bilmece(arg):
    soru, cevaplar = random.choice(BILMECELER[dil()])
    yaz(f"  ❓ {soru}", BEYAZ, 0.02)
    for hak in (2, 1, 0):
        cevap = sadelestir(sor(tr_en("Cevabın: ", "Your answer: ")))
        if cevap in cevaplar:
            soyle(tr_en("🎉 Bildin!", "🎉 You got it!"), YESIL + KALIN)
            return
        if hak:
            soyle(tr_en(f"✗ Olmadı, {hak} hakkın kaldı.", f"✗ Nope, {hak} {'try' if hak == 1 else 'tries'} left."), KIRMIZI)
    soyle(tr_en(f"Cevap: {cevaplar[0]}", f"Answer: {cevaplar[0]}"), SARI)


@komut("rekorlar skorlar", "scores", "Oyunlar", "Oyunlardaki en iyi skorlarını gösterir", "Shows your best game scores")
def k_rekorlar(arg):
    adlar = {"yilan": tr_en("Yılan (puan)", "Snake (score)"), "tahmin": tr_en("Tahmin (en az deneme)", "Guess (fewest tries)"),
             "yazhizi": tr_en("Yazma hızı (kelime/dk)", "Typing speed (WPM)"),
             "hafiza": tr_en("Hafıza (basamak)", "Memory (digits)"), "islem_sure": tr_en("İşlem 10/10 (saniye)", "Math 10/10 (seconds)")}
    if not VERI["rekorlar"]:
        soyle(tr_en("Henüz rekor yok. Hadi bir oyun oyna! 🎮", "No records yet. Go play a game! 🎮"), GRI)
        return
    kutu([f"{T.ANA}{adlar.get(ad, ad):<24}{RESET} {BEYAZ}{KALIN}{deger}{RESET}"
          for ad, deger in VERI["rekorlar"].items()], tr_en("🏆 REKORLAR", "🏆 HIGH SCORES"))


# ═══════════════════════════ KOMUTLAR: ÖĞREN ═══════════════════════════
def renklendir(kod):
    """Python kodunu basitçe renklendirir."""
    desen = (r"(#.*$)|(\"[^\"]*\"|'[^']*')|"
             r"\b(def|return|if|elif|else|for|while|in|import|from|class|try|except|finally|with|as|and|or|"
             r"not|True|False|None|break|continue|pass|lambda|self)\b|"
             r"\b(print|input|len|range|int|str|float|list|dict|open|type|append|upper|split)\b|\b(\d+(?:\.\d+)?)\b")

    def boya(m):
        for grup, renk in zip(m.groups(), (GRI, SARI, MOR, CAMGOBEGI, MAVI)):
            if grup:
                return renk + grup + BEYAZ
        return m.group(0)

    return BEYAZ + re.sub(desen, boya, kod) + RESET


DERSLER = {"tr": {  # Türkçe ve İngilizce dersler aynı sırada olmalı (konu_bul sırayla eşleştirir)
    "degisken": ("Değişkenler", "Değişken, bir değeri saklayan etiketli kutudur.", [
        "isim = \"Panda\"      # metin (str)",
        "yas = 5             # tam sayı (int)",
        "boy = 1.2           # ondalıklı (float)",
        "ac_mi = True        # doğru/yanlış (bool)",
        "print(isim, yas)    # Panda 5"]),
    "metin": ("Metinler (str)", "Tırnak içindeki her şey metindir. Toplanabilir, çarpılabilir, dilimlenebilir.", [
        "ad = \"Bambu\"",
        "print(ad + \" yiyorum\")   # birleştirme",
        "print(ad * 3)             # BambuBambuBambu",
        "print(ad[0], ad[-1])      # B u",
        "print(f\"{ad} lezzetli\")   # f-string",
        "print(ad.upper(), len(ad))"]),
    "kosul": ("Koşullar (if)", "Program karar verir: koşul doğruysa o blok çalışır.", [
        "not_ = int(input(\"Notun: \"))",
        "if not_ >= 85:",
        "    print(\"Pekiyi!\")",
        "elif not_ >= 50:",
        "    print(\"Geçtin\")",
        "else:",
        "    print(\"Tekrar çalış\")"]),
    "dongu": ("Döngüler (for / while)", "Aynı işi tekrar tekrar yaptırmanın yolu.", [
        "for i in range(5):          # 0,1,2,3,4",
        "    print(i)",
        "",
        "sayac = 3",
        "while sayac > 0:            # koşul doğru oldukça döner",
        "    print(sayac)",
        "    sayac -= 1"]),
    "liste": ("Listeler", "Birden çok değeri sıralı tutar. Köşeli parantez [] ile yazılır.", [
        "meyveler = [\"elma\", \"muz\", \"kiraz\"]",
        "meyveler.append(\"bambu\")   # sona ekle",
        "print(meyveler[0])          # elma",
        "print(len(meyveler))        # 4",
        "for m in meyveler:",
        "    print(m)"]),
    "sozluk": ("Sözlükler (dict)", "Anahtar → değer eşleşmesi tutar. Süslü parantez {} ile yazılır.", [
        "panda = {\"ad\": \"Po\", \"yas\": 5}",
        "print(panda[\"ad\"])          # Po",
        "panda[\"yemek\"] = \"bambu\"    # yeni anahtar ekle",
        "for anahtar, deger in panda.items():",
        "    print(anahtar, deger)"]),
    "fonksiyon": ("Fonksiyonlar", "Tekrar kullanılabilen kod parçası. 'def' ile tanımlanır.", [
        "def selamla(isim):",
        "    return \"Merhaba \" + isim",
        "",
        "print(selamla(\"Panda\"))    # Merhaba Panda",
        "",
        "def topla(a, b=10):         # b'nin varsayılan değeri var",
        "    return a + b"]),
    "sinif": ("Sınıflar (class)", "Kendi veri tipini yaratırsın: özellikler + davranışlar.", [
        "class Panda:",
        "    def __init__(self, ad):",
        "        self.ad = ad",
        "",
        "    def ye(self):",
        "        print(self.ad + \" bambu yiyor\")",
        "",
        "po = Panda(\"Po\")",
        "po.ye()"]),
    "hata": ("Hata yakalama (try)", "Program çökmesin diye hataları yakalarsın.", [
        "try:",
        "    sayi = int(input(\"Sayı: \"))",
        "    print(10 / sayi)",
        "except ValueError:",
        "    print(\"Sayı yazmadın!\")",
        "except ZeroDivisionError:",
        "    print(\"Sıfıra bölünmez!\")"]),
    "dosya": ("Dosyalar", "'with open' ile dosya okur/yazarsın; iş bitince dosya otomatik kapanır.", [
        "with open(\"not.txt\", \"w\", encoding=\"utf-8\") as d:",
        "    d.write(\"Bambu al\\n\")",
        "",
        "with open(\"not.txt\", encoding=\"utf-8\") as d:",
        "    print(d.read())"]),
    "modul": ("Modüller (import)", "Başkalarının yazdığı hazır kodları kullanırsın.", [
        "import random",
        "print(random.randint(1, 6))     # zar at",
        "",
        "from math import sqrt",
        "print(sqrt(16))                 # 4.0",
        "",
        "import time",
        "time.sleep(1)                   # 1 saniye bekle"]),
    "girdi": ("Kullanıcıdan girdi (input)", "input() her zaman METİN döndürür; sayıya çevirmeyi unutma!", [
        "ad = input(\"Adın ne? \")",
        "yas = int(input(\"Kaç yaşındasın? \"))",
        "print(f\"{ad}, 10 yıl sonra {yas + 10} yaşında olacaksın\")"]),
}, "en": {
    "variables": ("Variables", "A variable is a labeled box that stores a value.", [
        "name = \"Panda\"      # text (str)",
        "age = 5             # whole number (int)",
        "height = 1.2        # decimal number (float)",
        "is_hungry = True    # true/false (bool)",
        "print(name, age)    # Panda 5"]),
    "strings": ("Strings (str)", "Anything inside quotes is a string. You can add, multiply and slice strings.", [
        "food = \"Bamboo\"",
        "print(food + \" is tasty\")   # joining",
        "print(food * 3)             # BambooBambooBamboo",
        "print(food[0], food[-1])    # B o",
        "print(f\"{food} is yummy\")   # f-string",
        "print(food.upper(), len(food))"]),
    "if": ("Conditions (if)", "The program makes a decision: if the condition is true, that block runs.", [
        "score = int(input(\"Your score: \"))",
        "if score >= 85:",
        "    print(\"Excellent!\")",
        "elif score >= 50:",
        "    print(\"You passed\")",
        "else:",
        "    print(\"Study a bit more\")"]),
    "loops": ("Loops (for / while)", "The way to make the computer do the same job again and again.", [
        "for i in range(5):          # 0,1,2,3,4",
        "    print(i)",
        "",
        "count = 3",
        "while count > 0:            # repeats while the condition is true",
        "    print(count)",
        "    count -= 1"]),
    "lists": ("Lists", "Keeps several values in order. Written with square brackets [].", [
        "fruits = [\"apple\", \"banana\", \"cherry\"]",
        "fruits.append(\"bamboo\")     # add to the end",
        "print(fruits[0])            # apple",
        "print(len(fruits))          # 4",
        "for f in fruits:",
        "    print(f)"]),
    "dicts": ("Dictionaries (dict)", "Stores key → value pairs. Written with curly braces {}.", [
        "panda = {\"name\": \"Po\", \"age\": 5}",
        "print(panda[\"name\"])         # Po",
        "panda[\"food\"] = \"bamboo\"     # add a new key",
        "for key, value in panda.items():",
        "    print(key, value)"]),
    "functions": ("Functions", "A reusable piece of code. You define one with 'def'.", [
        "def greet(name):",
        "    return \"Hello \" + name",
        "",
        "print(greet(\"Panda\"))       # Hello Panda",
        "",
        "def add(a, b=10):           # b has a default value",
        "    return a + b"]),
    "classes": ("Classes (class)", "Create your own data type: attributes + behaviors.", [
        "class Panda:",
        "    def __init__(self, name):",
        "        self.name = name",
        "",
        "    def eat(self):",
        "        print(self.name + \" is eating bamboo\")",
        "",
        "po = Panda(\"Po\")",
        "po.eat()"]),
    "errors": ("Catching errors (try)", "Catch errors so your program doesn't crash.", [
        "try:",
        "    number = int(input(\"Number: \"))",
        "    print(10 / number)",
        "except ValueError:",
        "    print(\"That's not a number!\")",
        "except ZeroDivisionError:",
        "    print(\"You can't divide by zero!\")"]),
    "files": ("Files", "Read and write files with 'with open'; the file closes by itself when you're done.", [
        "with open(\"note.txt\", \"w\", encoding=\"utf-8\") as f:",
        "    f.write(\"Buy bamboo\\n\")",
        "",
        "with open(\"note.txt\", encoding=\"utf-8\") as f:",
        "    print(f.read())"]),
    "modules": ("Modules (import)", "Use ready-made code that other people wrote.", [
        "import random",
        "print(random.randint(1, 6))     # roll a die",
        "",
        "from math import sqrt",
        "print(sqrt(16))                 # 4.0",
        "",
        "import time",
        "time.sleep(1)                   # wait 1 second"]),
    "input": ("Getting input (input)", "input() ALWAYS returns text; don't forget to turn it into a number!", [
        "name = input(\"What's your name? \")",
        "age = int(input(\"How old are you? \"))",
        "print(f\"{name}, in 10 years you'll be {age + 10}\")"]),
}}


def konu_bul(tablo, arg):
    """Konuyu iki dilde de tanır, aktif dildeki adını döndürür: 'dongu' da 'loops' da İngilizcede 'loops' olur."""
    aranan = sadelestir(arg)
    for anahtarlar in (list(tablo["tr"]), list(tablo["en"])):
        if aranan in anahtarlar:
            return list(tablo[dil()])[anahtarlar.index(aranan)]
    return None


@komut("ogren ders", "learn", "Öğren", "Mini Python dersleri (örnek kodlu)", "Mini Python lessons (with example code)",
       "[konu]", "[topic]")
def k_ogren(arg):
    konu = konu_bul(DERSLER, arg)
    if not konu:
        if arg:
            hata(tr_en(f"'{arg}' diye bir ders yok.", f"There's no lesson called '{arg}'."))
        soyle(tr_en("📚 Dersler: ", "📚 Lessons: ") + ", ".join(DERSLER[dil()]), BEYAZ)
        soyle(tr_en("Örnek: ogren dongu", "Example: learn loops"), GRI)
        return
    baslik, aciklama, kod = DERSLER[dil()][konu]
    print(f"\n  {T.ANA}{KALIN}📘 {baslik}{RESET}")
    soyle(aciklama, BEYAZ)
    kutu([renklendir(satir) for satir in kod], tr_en("örnek kod", "example code"), GRI)
    soyle(tr_en("Deneme: bu kodu bir .py dosyasına yazıp çalıştır!", "Try it: put this code in a .py file and run it!"), GRI)


IPUCLARI = {"tr": [  # `ters tırnak` içindeki kısımlar kod olarak renklendirilir
    "`print(*liste)` listeyi köşeli parantezsiz yazdırır.",
    "`a, b = b, a` ile iki değişkenin değerini tek satırda değiştirebilirsin.",
    "f-string: `print(f\"{ad} {yas} yaşında\")` en okunaklı metin biçimidir.",
    "`len()` ile metnin, listenin, sözlüğün uzunluğunu öğrenirsin.",
    "`range(1, 11)` 1'den 10'a kadar sayar; 11 dahil değildir!",
    "`liste[::-1]` listeyi (ya da metni) ters çevirir.",
    "`enumerate(liste)` ile döngüde hem sırayı hem değeri alırsın.",
    "Sözlükte olmayan anahtar için hata almamak için `sozluk.get(\"anahtar\", varsayilan)` kullan.",
    "`input()` hep metin verir. Sayı lazımsa `int(input())` yaz.",
    "Değişken adlarında Türkçe karakter kullanabilirsin ama İngilizce klavye alışkanlığı işini kolaylaştırır.",
    "Hata mesajının EN ALT satırını oku; asıl sorun oradadır.",
    "Girinti (4 boşluk) Python'da süs değil, kuraldır!",
    "`in` ile üyelik kontrolü: `if \"a\" in \"panda\": ...`",
    "`sum(liste)`, `max(liste)`, `min(liste)` hazır fonksiyonlardır.",
    "Liste üreteci: `kareler = [x*x for x in range(10)]`",
    "`if __name__ == \"__main__\":` dosya doğrudan çalıştırıldığında çalışacak kodu ayırır.",
    "`help(print)` yazarsan Python sana print'in nasıl kullanıldığını anlatır.",
    "`type(x)` ile bir değişkenin tipini öğrenebilirsin.",
    "`round(3.14159, 2)` → `3.14`",
    "Kodunu küçük parçalar halinde yaz ve her parçayı çalıştırıp dene.",
], "en": [
    "`print(*my_list)` prints a list without the square brackets.",
    "`a, b = b, a` swaps the values of two variables in a single line.",
    "f-strings are the most readable way to build text: `print(f\"{name} is {age}\")`",
    "`len()` gives you the length of a string, a list or a dictionary.",
    "`range(1, 11)` counts from 1 to 10; 11 is not included!",
    "`my_list[::-1]` reverses a list (or a string).",
    "`enumerate(my_list)` gives you both the position and the value in a loop.",
    "To avoid an error when a key is missing, use `my_dict.get(\"key\", default)`.",
    "`input()` always returns text. If you need a number, write `int(input())`.",
    "Python names use snake_case: `user_name`, not `userName`.",
    "Read the LAST line of an error message first; that's where the real problem is.",
    "Indentation (4 spaces) isn't decoration in Python, it's the rule!",
    "Check membership with `in`: `if \"a\" in \"panda\": ...`",
    "`sum(my_list)`, `max(my_list)` and `min(my_list)` are built in.",
    "List comprehension: `squares = [x*x for x in range(10)]`",
    "`if __name__ == \"__main__\":` marks code that should run only when the file is run directly.",
    "Type `help(print)` and Python will explain how print works.",
    "`type(x)` tells you the type of a variable.",
    "`round(3.14159, 2)` → `3.14`",
    "Write your code in small pieces, and run each piece to test it.",
]}


@komut("ipucu", "tip", "Öğren", "Rastgele bir Python ipucu verir", "Gives a random Python tip")
def k_ipucu(arg):
    parcalar = random.choice(IPUCLARI[dil()]).split("`")  # tek sıradakiler ters tırnak içindeki koddur
    soyle("💡 " + "".join(renklendir(p) if i % 2 else BEYAZ + p for i, p in enumerate(parcalar)))


KOPYALAR = {"tr": {  # Türkçe ve İngilizce konular aynı sırada olmalı (konu_bul sırayla eşleştirir)
    "git": [("git init", "Klasörü git deposu yap"), ("git status", "Neler değişti?"),
            ("git add .", "Tüm değişiklikleri hazırla"), ("git commit -m \"mesaj\"", "Kaydet (commit)"),
            ("git log --oneline", "Geçmişi kısa göster"), ("git branch yeni", "Yeni dal aç"),
            ("git switch yeni", "Dala geç"), ("git merge yeni", "Dalı birleştir"),
            ("git clone <url>", "Depoyu indir"), ("git pull", "Uzaktaki değişiklikleri çek"),
            ("git push", "Değişiklikleri gönder"), ("git diff", "Satır satır farkları gör")],
    "python": [("python dosya.py", "Dosyayı çalıştır"), ("python", "Etkileşimli Python'u aç"),
               ("pip install paket", "Paket kur"), ("pip list", "Kurulu paketleri listele"),
               ("python -m venv venv", "Sanal ortam oluştur"), ("venv\\Scripts\\activate", "Sanal ortamı aç (Windows)"),
               ("python -m http.server", "Bulunduğun klasörü web sunucusu yap"),
               ("python -c \"print(1+1)\"", "Tek satır kod çalıştır")],
    "terminal": [("cd klasor", "Klasöre gir"), ("cd ..", "Bir üst klasöre çık"), ("dir / ls", "Dosyaları listele"),
                 ("mkdir ad", "Klasör oluştur"), ("cls / clear", "Ekranı temizle"),
                 ("type / cat dosya", "Dosyayı ekrana yaz"), ("copy / cp a b", "Dosya kopyala"),
                 ("move / mv a b", "Dosya taşı / adını değiştir"), ("↑ tuşu", "Önceki komutu getir"),
                 ("Tab tuşu", "Dosya adını otomatik tamamla"), ("Ctrl + C", "Çalışan programı durdur")],
    "klavye": [("Ctrl + C / V / X", "Kopyala / yapıştır / kes"), ("Ctrl + Z / Y", "Geri al / yinele"),
               ("Ctrl + S", "Kaydet"), ("Ctrl + F", "Bul"), ("Alt + Tab", "Pencereler arası geç"),
               ("Win + D", "Masaüstünü göster"), ("Win + Shift + S", "Ekran görüntüsü al"),
               ("Win + V", "Pano geçmişi"), ("Win + .", "Emoji paneli 🐼"), ("Ctrl + Shift + Esc", "Görev yöneticisi"),
               ("Ctrl + /", "(Kod editöründe) satırı yorum yap")],
}, "en": {
    "git": [("git init", "Turn the folder into a git repo"), ("git status", "What changed?"),
            ("git add .", "Stage all your changes"), ("git commit -m \"message\"", "Save a snapshot (commit)"),
            ("git log --oneline", "Show a short history"), ("git branch new", "Create a new branch"),
            ("git switch new", "Switch to that branch"), ("git merge new", "Merge the branch in"),
            ("git clone <url>", "Download a repo"), ("git pull", "Get the changes from the remote"),
            ("git push", "Send your changes"), ("git diff", "See the changes line by line")],
    "python": [("python file.py", "Run a file"), ("python", "Open interactive Python"),
               ("pip install package", "Install a package"), ("pip list", "List installed packages"),
               ("python -m venv venv", "Create a virtual environment"),
               ("venv\\Scripts\\activate", "Activate the virtual environment (Windows)"),
               ("python -m http.server", "Serve the current folder as a website"),
               ("python -c \"print(1+1)\"", "Run a single line of code")],
    "terminal": [("cd folder", "Go into a folder"), ("cd ..", "Go up one folder"), ("dir / ls", "List files"),
                 ("mkdir name", "Create a folder"), ("cls / clear", "Clear the screen"),
                 ("type / cat file", "Print a file"), ("copy / cp a b", "Copy a file"),
                 ("move / mv a b", "Move / rename a file"), ("↑ key", "Bring back the previous command"),
                 ("Tab key", "Autocomplete file names"), ("Ctrl + C", "Stop the running program")],
    "keyboard": [("Ctrl + C / V / X", "Copy / paste / cut"), ("Ctrl + Z / Y", "Undo / redo"),
                 ("Ctrl + S", "Save"), ("Ctrl + F", "Find"), ("Alt + Tab", "Switch between windows"),
                 ("Win + D", "Show the desktop"), ("Win + Shift + S", "Take a screenshot"),
                 ("Win + V", "Clipboard history"), ("Win + .", "Emoji panel 🐼"), ("Ctrl + Shift + Esc", "Task Manager"),
                 ("Ctrl + /", "Comment out a line (in code editors)")],
}}


@komut("kopya kisayol", "cheatsheet", "Öğren", "Kopya kâğıdı: git, python, terminal, klavye kısayolları",
       "Cheat sheets: git, python, terminal and keyboard shortcuts", "<konu>", "<topic>")
def k_kopya(arg):
    konu = konu_bul(KOPYALAR, arg)
    if not konu:
        soyle(tr_en("📋 Kopya kâğıtları: ", "📋 Cheat sheets: ") + ", ".join(KOPYALAR[dil()]), BEYAZ)
        soyle(tr_en("Örnek: kopya git", "Example: cheatsheet git"), GRI)
        return
    satirlar = KOPYALAR[dil()][konu]
    en = max(len(k) for k, _ in satirlar)
    kutu([f"{T.ANA}{k:<{en}}{RESET}  {a}" for k, a in satirlar], tr_en("KOPYA: ", "CHEAT SHEET: ") + buyuk_harf(konu))


HTTP_KODLARI = {  # (Türkçe, İngilizce)
    100: ("Continue — devam et", "Continue — keep going"),
    200: ("OK — her şey yolunda ✅", "OK — all good ✅"),
    201: ("Created — oluşturuldu", "Created — it was created"),
    204: ("No Content — tamam ama gösterecek içerik yok", "No Content — fine, but there's nothing to show"),
    301: ("Moved Permanently — kalıcı olarak taşındı", "Moved Permanently — it moved for good"),
    302: ("Found — geçici olarak başka yerde", "Found — it's somewhere else for now"),
    304: ("Not Modified — değişmedi, önbellekteki kullan", "Not Modified — nothing changed, use your cached copy"),
    400: ("Bad Request — isteğin bozuk", "Bad Request — your request is broken"),
    401: ("Unauthorized — önce giriş yapmalısın", "Unauthorized — you need to log in first"),
    403: ("Forbidden — yasak, iznin yok 🚫", "Forbidden — you're not allowed 🚫"),
    404: ("Not Found — bulunamadı 🔍", "Not Found — nothing here 🔍"),
    405: ("Method Not Allowed — bu yöntem kullanılamaz", "Method Not Allowed — you can't use that method here"),
    408: ("Request Timeout — istek zaman aşımına uğradı", "Request Timeout — the request took too long"),
    418: ("I'm a teapot — ben bir çaydanlığım ☕ (şaka olarak eklenmiş gerçek bir kod)",
          "I'm a teapot — a real code that was added as a joke ☕"),
    429: ("Too Many Requests — çok fazla istek, yavaş ol", "Too Many Requests — slow down"),
    500: ("Internal Server Error — sunucu patladı 💥", "Internal Server Error — the server blew up 💥"),
    502: ("Bad Gateway — aradaki sunucu kötü cevap verdi", "Bad Gateway — a server in between gave a bad answer"),
    503: ("Service Unavailable — hizmet şu an yok / bakımda", "Service Unavailable — down or under maintenance"),
    504: ("Gateway Timeout — aradaki sunucu zamanında cevap alamadı",
          "Gateway Timeout — a server in between didn't answer in time"),
}


@komut("http", "http", "Öğren", "HTTP durum kodunun anlamını söyler (404, 500...)",
       "Explains what an HTTP status code means (404, 500...)", "[kod]", "[code]")
def k_http(arg):
    if arg.strip().isdigit() and int(arg) in HTTP_KODLARI:
        soyle(f"🌐 {BEYAZ}{KALIN}{arg}{RESET}{T.ANA} → {tr_en(*HTTP_KODLARI[int(arg)])}")
        return
    if arg:
        hata(tr_en(f"'{arg}' kodunu bilmiyorum. Bildiklerim:", f"I don't know the code '{arg}'. Here are the ones I know:"))
    for kod, anlam in HTTP_KODLARI.items():
        renk = YESIL if kod < 300 else CAMGOBEGI if kod < 400 else SARI if kod < 500 else KIRMIZI
        print(f"  {renk}{kod}{RESET}  {tr_en(*anlam)}")


PORTLAR = {  # (Türkçe, İngilizce)
    20: ("FTP (veri)", "FTP (data)"),
    21: ("FTP (kontrol) — dosya aktarımı", "FTP (control) — file transfer"),
    22: ("SSH — güvenli uzak bağlantı", "SSH — secure remote login"),
    23: ("Telnet — eski, şifresiz uzak bağlantı", "Telnet — old, unencrypted remote login"),
    25: ("SMTP — e-posta gönderme", "SMTP — sending email"),
    53: ("DNS — alan adı çözme", "DNS — looking up domain names"),
    80: ("HTTP — web", "HTTP — the web"),
    110: ("POP3 — e-posta alma", "POP3 — receiving email"),
    143: ("IMAP — e-posta alma", "IMAP — receiving email"),
    443: ("HTTPS — güvenli web 🔒", "HTTPS — the secure web 🔒"),
    3306: ("MySQL veritabanı", "MySQL database"),
    3389: ("RDP — Windows uzak masaüstü", "RDP — Windows Remote Desktop"),
    5432: ("PostgreSQL veritabanı", "PostgreSQL database"),
    6379: ("Redis", "Redis"),
    8080: ("HTTP (alternatif / geliştirme)", "HTTP (alternative / development)"),
    25565: ("Minecraft sunucusu ⛏", "Minecraft server ⛏"),
    27017: ("MongoDB veritabanı", "MongoDB database"),
    5000: ("Flask geliştirme sunucusu", "Flask development server"),
    3000: ("Node / React geliştirme sunucusu", "Node / React development server"),
}


@komut("port", "port", "Öğren", "Ağ port numarasının ne işe yaradığını söyler", "Tells what a network port number is used for",
       "[numara]", "[number]")
def k_port(arg):
    if arg.strip().isdigit() and int(arg) in PORTLAR:
        soyle(f"🔌 Port {BEYAZ}{KALIN}{arg}{RESET}{T.ANA} → {tr_en(*PORTLAR[int(arg)])}")
        return
    if arg:
        hata(tr_en(f"{arg} numaralı portu tanımıyorum. Bildiklerim:", f"I don't know port {arg}. Here are the ones I know:"))
    for no, anlam in sorted(PORTLAR.items()):
        print(f"  {T.ANA}{no:>6}{RESET}  {tr_en(*anlam)}")


PY_SORULARI = {"tr": [
    ("print(type(3 / 2)) ne yazar?", ["<class 'int'>", "<class 'float'>", "<class 'str'>", "Hata verir"], 1),
    ("len(\"panda\") kaçtır?", ["4", "5", "6", "Hata verir"], 1),
    ("[1, 2, 3][-1] nedir?", ["1", "3", "-1", "Hata verir"], 1),
    ("\"ab\" * 3 nedir?", ["\"ab3\"", "\"ababab\"", "\"aaabbb\"", "Hata verir"], 1),
    ("7 // 2 kaçtır?", ["3.5", "3", "4", "1"], 1),
    ("7 % 3 kaçtır?", ["1", "2", "2.33", "0"], 0),
    ("bool(\"\") nedir?", ["True", "False", "None", "\"\""], 1),
    ("list(range(3)) nedir?", ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[3]"], 1),
    ("Hangisi değiştirilemez (immutable)?", ["list", "dict", "tuple", "set"], 2),
    ("\"Merhaba\"[0:3] nedir?", ["\"Mer\"", "\"Merh\"", "\"erh\"", "\"M\""], 0),
    ("2 ** 3 kaçtır?", ["6", "8", "9", "5"], 1),
    ("Fonksiyon tanımlamak için hangi kelime kullanılır?", ["func", "function", "def", "fn"], 2),
    ("\"3\" + \"4\" nedir?", ["7", "\"34\"", "\"7\"", "Hata verir"], 1),
    ("Sözlük (dict) hangi parantezle yazılır?", ["[ ]", "( )", "{ }", "< >"], 2),
    ("int(\"12\") + 1 kaçtır?", ["\"121\"", "13", "12.1", "Hata verir"], 1),
], "en": [
    ("What does print(type(3 / 2)) print?", ["<class 'int'>", "<class 'float'>", "<class 'str'>", "An error"], 1),
    ("What is len(\"panda\")?", ["4", "5", "6", "An error"], 1),
    ("What is [1, 2, 3][-1]?", ["1", "3", "-1", "An error"], 1),
    ("What is \"ab\" * 3?", ["\"ab3\"", "\"ababab\"", "\"aaabbb\"", "An error"], 1),
    ("What is 7 // 2?", ["3.5", "3", "4", "1"], 1),
    ("What is 7 % 3?", ["1", "2", "2.33", "0"], 0),
    ("What is bool(\"\")?", ["True", "False", "None", "\"\""], 1),
    ("What is list(range(3))?", ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[3]"], 1),
    ("Which of these can't be changed (immutable)?", ["list", "dict", "tuple", "set"], 2),
    ("What is \"Hello\"[0:3]?", ["\"Hel\"", "\"Hell\"", "\"ell\"", "\"H\""], 0),
    ("What is 2 ** 3?", ["6", "8", "9", "5"], 1),
    ("Which keyword defines a function?", ["func", "function", "def", "fn"], 2),
    ("What is \"3\" + \"4\"?", ["7", "\"34\"", "\"7\"", "An error"], 1),
    ("Which brackets does a dict use?", ["[ ]", "( )", "{ }", "< >"], 2),
    ("What is int(\"12\") + 1?", ["\"121\"", "13", "12.1", "An error"], 1),
]}


@komut("pyquiz sinav", "pyquiz quiz", "Öğren", "5 soruluk Python bilgi yarışması", "A 5-question Python quiz")
def k_pyquiz(arg):
    sorular = random.sample(PY_SORULARI[dil()], 5)
    puan = 0
    soyle(tr_en("🐍 Python Quiz! Her soruda a, b, c ya da d yaz.", "🐍 Python Quiz! Answer each question with a, b, c or d."))
    for no, (soru, secenekler, dogru) in enumerate(sorular, 1):
        print(f"\n  {BEYAZ}{KALIN}{no}. {renklendir(soru)}{RESET}")
        for harf, secenek in zip("abcd", secenekler):
            print(f"     {T.ANA}{harf}){RESET} {secenek}")
        cevap = sadelestir(sor(tr_en("Cevabın: ", "Your answer: ")))
        if cevap == "abcd"[dogru]:
            puan += 1
            soyle(tr_en("✓ Doğru!", "✓ Correct!"), YESIL)
        else:
            soyle(tr_en("✗ Doğrusu: ", "✗ The answer is ") + f"{'abcd'[dogru]}) {secenekler[dogru]}", KIRMIZI)
    yorum = (tr_en("Python ustası! 🏆", "Python master! 🏆") if puan == 5 else
             tr_en("Çok iyi! 👏", "Very good! 👏") if puan >= 3 else
             tr_en("Biraz daha 'ogren' komutuna bak 📚", "Spend some more time with the 'learn' command 📚"))
    soyle(tr_en(f"\n  Sonuç: {puan}/5 — {yorum}", f"\n  Result: {puan}/5 — {yorum}"), BEYAZ + KALIN)


# ═══════════════════════════ AÇILIŞ, VEDA VE ANA DÖNGÜ ═══════════════════════════
def acilis():
    ekrani_temizle()
    matrix_yagmuru(1.2)
    ekrani_temizle()
    panda_ciz()
    print()
    for satir in buyuk_yazi("PANDACODE"):
        print("  " + T.ANA + KALIN + satir)
        time.sleep(0.04)
    print(T.KOYU + "  " + "═" * 57 + RESET)
    yaz(tr_en(f"  >> PANDACODE v{SURUM} // kodlardan yapılmış bir panda", f"  >> PANDACODE v{SURUM} // a panda made of code"),
        BEYAZ)
    soyle(tr_en(f"{len(KOMUTLAR)} komut yüklendi. 'yardim' yaz → ok tuşlarıyla gez.",
                f"{len(KOMUTLAR)} commands loaded. Type 'help' → browse with the arrow keys."), SARI)
    soyle(tr_en("For English, type 'lang'.", "Türkçe için 'dil' yaz.") + "\n", GRI)  # öbür dile geçiş, o dilde yazılır


def veda():
    print(RESET)
    imlec(True)
    yaz(tr_en("  Görüşürüz! Panda bambusunu alıp uyumaya gidiyor... 🐼💤",
              "  See you! The panda grabs its bamboo and heads off to sleep... 🐼💤"), T.ANA, 0.02)


def istem():
    return f"{T.ANA}{KALIN}{VERI['isim']}@pandacode{RESET}{BEYAZ}:~$ {RESET}"


def calistir(satir):
    parcalar = satir.split(maxsplit=1)
    yazilan = parcalar[0]
    ad = komut_coz(yazilan)
    arg = parcalar[1].strip() if len(parcalar) > 1 else ""
    if ad not in KOMUTLAR:
        oneri = difflib.get_close_matches(ad, list(KOMUTLAR) + list(TAKMA_ADLAR), n=1, cutoff=0.6)
        hata(tr_en(f"'{yazilan}' diye bir komut yok aga.", f"There's no '{yazilan}' command, buddy."))
        if oneri:
            soyle(tr_en("Bunu mu demek istedin: ", "Did you mean: ")
                  + f"{BEYAZ}{KALIN}{komut_adi(TAKMA_ADLAR.get(oneri[0], oneri[0]))}{RESET}{SARI} ?", SARI)
        else:
            soyle(tr_en("Tüm komutları görmek için 'yardim' yaz.", "Type 'help' to see every command."), SARI)
        return
    if ad != "tekrar":
        GECMIS.append(yazilan if ad == "sifreguc" else satir)  # şifreler geçmişe yazılmasın
    try:
        KOMUTLAR[ad]["fonksiyon"](arg)
    except KeyboardInterrupt:
        print(RESET)
        soyle(tr_en("⏹  İptal edildi.", "⏹  Cancelled."), SARI)
    except Cikis:
        raise
    except Exception as e:  # bir komut bozulsa bile terminal çökmesin
        print(RESET)
        hata(tr_en(f"Bir şeyler ters gitti: {e}", f"Something went wrong: {e}"))


def main():
    veri_yukle()
    acilis()
    while True:
        try:
            satir = input(istem()).strip()
        except EOFError:
            raise Cikis
        if satir:
            calistir(satir)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, Cikis):
        veda()
