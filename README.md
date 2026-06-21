# NutriWise AI 🍏🧠

NutriWise AI adalah Sistem Pendukung Keputusan (SPK) cerdas berbasis **Logika Fuzzy Sugeno** yang dirancang untuk membantu pengguna menentukan target kalori dan kebutuhan makronutrisi harian secara akurat. Aplikasi ini dilengkapi dengan antarmuka yang sangat modern (Glassmorphism), *Explainable AI (XAI)*, dan sistem manajemen riwayat makanan.

## ✨ Fitur Utama
1. **Kalkulator Nutrisi Fuzzy (Sugeno Order-0):** Menghitung BMR dan TDEE, lalu mengaplikasikan logika fuzzy berdasarkan 3 variabel: Usia, Status BMI, dan Tingkat Aktivitas untuk menghasilkan kalori target harian yang dinamis secara komputasi ringan dan akurat.
2. **Explainable AI (XAI) Log:** Pengguna dapat melihat transparansi logika AI secara rinci (Fuzzifikasi, Evaluasi Aturan MIN, hingga perhitungan *Weighted Average* Defuzzifikasi).
3. **Dashboard & Time-Travel:** Melacak konsumsi kalori harian dan makronutrisi (Donut Chart) dengan kemampuan melihat riwayat kalender di hari-hari sebelumnya. Termasuk grafik analitik tren kalori mingguan.
4. **Smart Food Recommendation:** Menyarankan menu makan pagi, siang, malam, dan camilan beserta alokasi kalorinya.
5. **Autentikasi & Manajemen Profil:** Sistem pendaftaran, login, dan pembaruan profil yang aman (terenkripsi *Bcrypt*).

---

## 🛠️ Persyaratan Sistem
Pastikan laptop/PC Anda telah terinstal:
- **Python 3.8** atau versi yang lebih baru.
- **Pip** (Python Package Installer).
- **Git** (Opsional, untuk *clone* repositori).

---

## 🚀 Panduan Instalasi (Step-by-Step)

Anda hanya perlu mengikuti langkah-langkah di bawah ini untuk menjalankan NutriWise AI di perangkat Anda:

### 1. Unduh / Clone Repositori
Buka terminal/Command Prompt dan arahkan ke folder yang Anda inginkan, lalu jalankan:
```bash
git clone <url-repositori-ini>
cd nutriwise_ai
```
*(Jika Anda mengunduh berformat .zip, cukup ekstrak dan buka terminal di dalam folder tersebut).*

### 2. Buat Virtual Environment (Sangat Direkomendasikan)
Untuk mencegah konflik modul Python, buatlah *virtual environment*:
```bash
python -m venv venv
```
Aktifkan *virtual environment*:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalasi Dependensi (Requirements)
Instal semua modul/library yang dibutuhkan aplikasi (Flask, SQLAlchemy, Scikit-Fuzzy, dll) dengan perintah:
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Database (Otomatis!)
Anda **TIDAK PERLU** melakukan setup *database* secara manual. Aplikasi ini telah diprogram menggunakan SQLite dan akan **membangun database serta seluruh tabelnya secara otomatis** (`nutriwise.db`) saat Anda menjalankan server untuk pertama kalinya.

### 5. Jalankan Aplikasi
Jalankan server Flask dengan perintah:
```bash
python run.py
```

### 6. Buka di Browser
Aplikasi sekarang sudah berjalan secara lokal! Buka peramban (*browser*) Anda seperti Google Chrome atau Edge, dan akses alamat berikut:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📂 Struktur Direktori Singkat
- `app/` : Folder utama yang berisi konfigurasi Flask (*Routes, Models, Forms, Templates, dll*).
- `app/fuzzy/` : Berisi mesin utama Logika Fuzzy Mamdani (`engine.py`).
- `instance/` : (Akan muncul otomatis) Tempat *database* SQLite `nutriwise.db` tersimpan.
- `run.py` : Skrip utama untuk menyalakan server aplikasi.

## 🤝 Kontribusi & Dukungan
Sistem ini dibangun khusus untuk proyek implementasi Sistem Pendukung Keputusan (SPK) Logika Fuzzy. Jika Anda ingin melakukan *debugging* perhitungan, seluruh log perhitungan akan dicetak juga di terminal (*console*) saat Anda melakukan "Hitung Nutrisi" di aplikasi.

Selamat mengeksplorasi NutriWise AI! 🚀
