# 🦠 InfoKesehatan - Aplikasi Informasi Penyakit dan Kesehatan

Aplikasi berbasis Flask untuk menampilkan data penyakit menular di Indonesia, dengan fitur visualisasi data, multilingual support, dan analisis clustering K-Means.

## 🚀 Fitur

- 🌐 Dukungan multi-bahasa (Bahasa Indonesia dan Inggris)
- 📊 Visualisasi data penyakit per tahun dan wilayah
- 🔍 Heatmap korelasi penyakit
- 🔎 Clustering K-Means berdasarkan jumlah kasus
- 🧾 Halaman statis informatif (tentang kami, kontak, bantuan, dll)
- 📁 Modular folder structure

## 📁 Struktur Proyek

```bash
├── app.py # Entry point aplikasi Flask
├── data/ # Folder data CSV
│ ├── Data_TBC.csv
│ └── extended_data_tbc.csv
├── static/ # File statis
│ ├── images/ # Gambar untuk slide dan favicon
│ ├── plots/ # Output plot visualisasi
│ ├── js/ # JavaScript (jika diperlukan)
│ └── style/ # CSS (style.css & variables.css)
├── templates/ # HTML templates Jinja2
├── translations/ # File terjemahan JSON (id.json, en.json)
├── .env # Variabel environment
├── .gitignore # File ignore Git
├── requirements.txt # Daftar dependensi Python
└── README.md # Dokumentasi proyek
```

## 📦 Instalasi

1. **Clone repositori**

   ```bash
   git clone https://github.com/yourusername/infokesehatan.git
   cd infokesehatan
   ```

2. **Buat dan aktifkan virtual environment**

```bash
   python -m venv venv
   source venv/bin/activate # (Linux/macOS)
   venv\Scripts\activate # (Windows)
```

3. **Instal dependensi**

```bash
   pip install -r requirements.txt
```

4. **Atur file .env**

```text
   SECRET_KEY=your-secret-key
   FLASK_ENV=development
   CSV_FILE=data/extended_data_tbc.csv
   STATIC_PLOTS=static/plots
```

5. **Jalankan server**

```bash
   python app.py
```

## 🖼️ Visualisasi

- Bar chart jumlah kasus per penyakit

- Heatmap korelasi antar penyakit

- Heatmap jumlah kasus per tahun dan penyakit

- Scatter plot clustering K-Means

## 📚 Dependensi Utama

- Flask

- Pandas

- Seaborn & Matplotlib

- scikit-learn

- python-dotenv

## 🤝 Kontribusi

Pull request terbuka untuk perbaikan fitur atau UI. Jangan lupa sertakan deskripsi perubahanmu.
