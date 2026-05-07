# 🍅 Pomodoro App

Aplikasi timer Pomodoro untuk Android, dibangun dengan **Python + Flet**. Ringan, efisien, dan siap di-build menjadi APK via **GitHub Actions**.

---

## 📁 Struktur Folder

```
pomodoro-app/
├── src/
│   ├── components/
│   │   ├── circular_timer.py     # Widget timer lingkaran (Canvas arc)
│   │   ├── control_buttons.py    # Tombol Start / Pause / Reset
│   │   ├── mode_selector.py      # Toggle: Pomodoro / Short Break / Long Break
│   │   └── stats_card.py         # Kartu statistik sesi harian
│   ├── utils/
│   │   ├── storage.py            # Simpan & baca statistik (page.client_storage)
│   │   ├── notifications.py      # Notifikasi & alarm (flet Audio + vibrate)
│   │   └── timer_logic.py        # State mesin timer (countdown, mode cycling)
│   └── constants/
│       ├── theme.py              # Warna, ukuran font, border radius
│       └── timer.py              # Durasi default (pomodoro=25, short=5, long=15 menit)
├── assets/
│   └── alarm.mp3                 # File suara alarm, disarankan < 50 KB
├── main.py                       # Entry point — flet.app(target=main)
├── requirements.txt
├── pyproject.toml                # Metadata build Flet (app_id, versi, ikon, dsb.)
└── .github/
    └── workflows/
        └── build-apk.yml         # GitHub Actions: flet build android → upload APK artifact
```

---

## ⚙️ Install (Lokal / Dev)

```bash
# 1. Buat & aktifkan virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

**requirements.txt** (isi minimal):
```
flet>=0.24.0
```

---

## 🚀 Run (Development — Desktop Preview)

```bash
flet run main.py
```

> Untuk preview tampilan mobile langsung di HP, gunakan: `flet run main.py --android` (membutuhkan Flet app terinstal di HP).

---

## 📦 Build APK (GitHub Actions)

APK di-build otomatis oleh GitHub Actions setiap push ke branch `main`.

### Cara pakai:
1. Push project ke repository GitHub.
2. GitHub Actions menjalankan workflow `.github/workflows/build-apk.yml`.
3. APK hasil build tersedia di tab **Actions → Artifacts** pada repository.

### Isi `.github/workflows/build-apk.yml`:
```yaml
name: Build Android APK

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Flet CLI
        run: pip install flet

      - name: Set up Java (diperlukan Android SDK)
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Set up Android SDK
        uses: android-actions/setup-android@v3

      - name: Build APK
        run: flet build android --no-rich-output

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: pomodoro-apk
          path: build/android/outputs/**/*.apk
          retention-days: 7
```

---

## 📐 Panduan Implementasi untuk AI

Instruksi ini untuk memandu AI IDE (Cursor, Copilot, dsb.) saat menulis kode.

### Prinsip Utama
- **Minimal dependency**: hanya gunakan library bawaan Python + `flet`. Jangan tambah dependency eksternal kecuali benar-benar diperlukan.
- **Single responsibility**: setiap file hanya mengekspor satu class atau fungsi utama.
- **State terpusat**: semua logika dan state timer ada di `timer_logic.py`. Komponen UI hanya menerima nilai dan callback — tidak boleh menyimpan state sendiri.
- **APK sekecil mungkin**: hindari import library besar. Gunakan `ft.Canvas` untuk menggambar timer lingkaran secara native — jangan gunakan gambar atau SVG eksternal.

### Desain UI
- Gunakan `ft.Theme` dengan satu `color_scheme_seed` (misal merah tomat `#E05A4E`) agar palet warna konsisten.
- Layout utama: `ft.Column` terpusat dengan `horizontal_alignment=ft.CrossAxisAlignment.CENTER`.
- Gunakan `ft.Container` dengan `border_radius` dan `shadow` tipis untuk tampilan kartu.
- Timer lingkaran: gambar dengan `ft.Canvas` + `ft.Paint(style=PaintingStyle.STROKE)` — **bukan** gambar atau library chart.
- Responsif: gunakan `expand=True` dan persentase lebar (`width=page.width * 0.8`), hindari nilai piksel hardcode.
- Font: gunakan font bawaan sistem — tidak perlu load font eksternal agar APK tetap kecil.

### Notifikasi & Alarm
- Gunakan `ft.Audio` untuk memutar suara dari `assets/alarm.mp3`.
- Fallback jika audio gagal: panggil `page.show_snack_bar()` dan aktifkan getar via `ft.HapticFeedback`.
- Simpan preferensi volume ke `page.client_storage`.

### Penyimpanan Statistik
- Gunakan `page.client_storage` (built-in Flet) — **tidak perlu** database atau file eksternal.
- Format key: `stats_{YYYY-MM-DD}` → value: jumlah sesi selesai (integer).
- Reset otomatis: saat app dibuka, bandingkan tanggal hari ini dengan key terakhir. Jika berbeda hari, reset counter ke 0.

### `pyproject.toml` (metadata build)
```toml
[tool.flet]
app_id = "com.yourname.pomodoroapp"
product_name = "Pomodoro"
description = "Pomodoro timer app"
version = "1.0.0"
build_number = 1

[tool.flet.android]
permissions = ["VIBRATE", "RECEIVE_BOOT_COMPLETED"]
```

---

## 📝 Catatan

- **Alarm**: simpan file audio di `assets/` agar di-bundle ke APK. Format `.mp3`, ukuran disarankan < 50 KB.
- **Notifikasi**: gunakan `ft.Audio` + `page.show_snack_bar()` sebagai fallback jika izin notifikasi sistem tidak diberikan.
- **Statistik**: tersimpan lokal via `page.client_storage`. Data hilang jika app di-uninstall — ini perilaku yang diharapkan.
- **Build time**: proses build APK di GitHub Actions ±10–20 menit, lebih cepat jika cache Android SDK sudah tersimpan dari run sebelumnya.
