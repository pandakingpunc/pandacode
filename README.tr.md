# 🐼 PandaCode

[English](README.md) | **Türkçe**

**[oh-my-pi (omp)](https://github.com/can1357/oh-my-pi) üstüne kurulmuş, sade ve Türkçe bir terminal kodlama ajanı.**

omp, yüzden fazla komutu olan güçlü bir kodlama ajanı. PandaCode onun motoruna dokunmadan etrafındaki deneyimi değiştiriyor: terminalde çalışan ama masaüstü uygulaması kadar kolay kullanılan bir araç. Günlük komutları görürsün, lazım olan tuşlar yazı alanının hemen altında durur, arayüz Türkçe konuşur.

> **Durum:** erken aşama. PandaCode, geliştiricisi tarafından Windows'ta yapılıp deneniyor. Pürüzler ve hâlâ İngilizce kalmış yerler olabilir.

## PandaCode neler ekliyor

| | |
|---|---|
| **Sade mod** | `/` listesinde tüm komutlar yerine 16 günlük komut görünür. Hiçbir şey silinmedi: omp'nin bütün komutları yazınca yine çalışır; `/gelismis` (ya da `/advanced`) tam listeyi açıp kapatır. |
| **Komut paleti** | Yazı alanı boşken <kbd>Ctrl</kbd>+<kbd>K</kbd>, komutları açıklamalarıyla birlikte aranabilir bir listede açar. Yazı alanında metin varken <kbd>Ctrl</kbd>+<kbd>K</kbd> eskisi gibi satır sonuna kadar siler. |
| **Kısayol çubuğu** | Yazı alanının altındaki sönük satır o an işine yarayan tuşları gösterir: boştayken komutlar, model, düşünme seviyesi, geçmiş ve çıkış; ajan çalışırken durdurma ve ayrıntı. |
| **Türkçe arayüz** | Komut açıklamaları, ipuçları, kısayol çubuğu, seçiciler ve kurulum başlıkları varsayılan olarak Türkçe. `/settings` → PandaCode → *Arayüz Dili* ile Türkçe/İngilizce arasında geçebilirsin. |
| **3 adımlı kurulum** | İlk açılışta yalnız giriş, model ve tema sorulur. |
| **`pandacode` komutu** | Bu klasörü her yerden çalıştıran bir başlatıcı. Kurulu bir `omp` varsa ona dokunmaz. |
| **Panda** | Açılış ve kurulum ekranlarında panda logosu ve PandaCode adı. |

Bu ayarların hepsi `/settings` içinde **PandaCode** grubunda.

## Kaynaktan kurulum

[Bun](https://bun.sh) ve Git gerekli.

```bash
git clone https://github.com/pandakingpunc/pandacode.git
cd pandacode
bun install
```

PandaCode, omp'nin repoda bulunmayan native eklentisine (`pi_natives`) ihtiyaç duyar. İki yoldan biriyle edinebilirsin:

- **Derle:** `bun run build:native`. Bunun için `rust-toolchain.toml` içinde sabitlenmiş Rust sürümü ve işletim sisteminin C/C++ derleme araçları gerekir.
- **Aynı sürümde (18.12.6) kurulu bir omp'den kopyala:** `~/.omp/natives/18.12.6/pi_natives.<platform>.node` dosyasını `packages/natives/native/` içine kopyala.

Sonra başlatıcıyı kurup aç:

```bash
bun run install:pandacode
pandacode
```

`install:pandacode`, Bun'ın global bin klasörüne `pandacode` (Windows'ta ayrıca `pandacode.cmd`) yazar. Kendi yazmadığı bir dosyanın üstüne asla yazmaz; `bun run install:pandacode --uninstall` bunları kaldırır.

## Bilmekte fayda var

- PandaCode'un içinde hâlâ omp 18.12.6 çalışıyor. Ayarlar, oturumlar ve girişler `~/.omp` içinde durur; mevcut bir omp kurulumun aynen geçer. `pandacode --version` de `omp/…` yazar.
- Türkçe arayüz şimdilik kısmi. Ayarlar panelinin içi, kurulum adımlarının gövde metinleri ve çoğu durum mesajı hâlâ İngilizce.
- omp'nin kendi özellikleri (araçlar, sağlayıcılar, alt ajanlar, LSP, hata ayıklayıcı ve daha fazlası) için [oh-my-pi README'sine](https://github.com/can1357/oh-my-pi#readme) bak.

## Emek ve lisans

PandaCode, Can Bölük ve Stencil Labs'in [oh-my-pi](https://github.com/can1357/oh-my-pi) projesinin fork'udur; omp de Mario Zechner'in pi'si üstüne kurulu. Ağır işi onlar yaptı.

PandaCode değişiklikleri: [Mustafa Karatum](https://github.com/pandakingpunc).

omp gibi [MIT Lisansı](LICENSE) ile yayınlanır. Özgün telif bildirimleri [LICENSE](LICENSE) dosyasında korunuyor.
