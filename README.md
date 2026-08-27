# Generator Tugas Random SPSS & Excel (300 Bank Soal Dinamis & Otomasi Dataset Statistik)

Aplikasi pintar berbasis web untuk **otomasi pembuatan dataset statistik realistis** (berbasis survei riil BPS seperti Susenas, Sakernas, Sensus Pertanian, dan Pelayanan Publik) dan **300 Bank Soal Latihan Praktik SPSS & Excel** dengan sistem koreksi / pemeriksa jawaban otomatis (*Automatic Answer Checker & Step-by-Step Solver*).

Sangat cocok untuk mahasiswa statistika, dosen, praktisi data, serta persiapan ujian kompetensi statistik BPS / instansi pemerintah.

---

## 🌟 Fitur Unggulan

### 1. Bank 300 Template Soal Statistik Terstruktur (Anti-Mengulang)
Tersedia 300 variasi soal (30 soal per modul) yang dikelompokkan ke dalam **10 Modul Statistik**:
1. **Statistika Deskriptif & Tendensi Sentral** (Mean, Median, Modus, Geometric Mean, Harmonic Mean, Weighted Mean, Trimmed Mean, Sum, Count, Mean vs Median, Winsorized Mean, Desil D1/D5/D9, Persentil P10/P90/P95/P99, Mid-Range, Midhinge, Trimean, RMS, dll).
2. **Ukuran Dispersi & Bentuk Distribusi** (Range, Varians Sampel/Populasi, Standar Deviasi, Koefisien Variasi CV%, Q1, Q3, IQR, QD, Skewness, Kurtosis, Tukey Outlier Upper/Lower/Extreme Fences, MAD, Z-Score, Sarle's Bimodality, dll).
3. **Uji Hipotesis 1 & 2 Sampel (Parametrik)** (One-Sample t-Test, Independent t-Test Equal/Unequal Var, Welch's t-Test, Paired t-Test, SE Mean/Diff, 90%/95%/99% Confidence Intervals, Margin of Error, Cohen's d, Hedges' g effect size, dll).
4. **Analisis Varians (ANOVA)** (One-Way ANOVA SS/MS Between & Within, SS/df Total, F-hitung, p-value, df, Eta-Squared, Partial Eta², Omega², Levene Homogeneity, Welch/Brown-Forsythe ANOVA, Tukey HSD, Bonferroni Alpha, Cohen's f, dll).
5. **Analisis Korelasi & Kovarians** (Korelasi Pearson r, R-Squared, % R², Uji t Korelasi, p-value Pearson, Spearman rho, Kendall's Tau, Sample/Pop Covariance, Fisher's z transform, Point-Biserial, Partial & Semipartial Correlation, SE r, dll).
6. **Uji Chi-Square & Asosiasi Kategorik** (Pearson Chi-Square, p-value Asymp. Sig, df Kontingensi, Cramer's V, Koefisien Kontingensi C, Phi, Expected Counts, Yates Correction, Likelihood Ratio, Std Residuals, Odds Ratio, Relative Risk, Gamma, McNemar, Kappa, dll).
7. **Analisis Regresi Linear** (Slope b, Intercept a, R-Square, Adjusted R-Square, Uji F ANOVA Regresi, p-value F, Uji t Parsial Slope/Intercept, Standard Error of Estimate, Prediksi Titik Y_hat, CI Parameter, MAE, RMSE, dll).
8. **Uji Asumsi Klasik / Ekonometrika** (Uji Normalitas Kolmogorov-Smirnov & Shapiro-Wilk, Jarque-Bera, Durbin-Watson Autokorelasi, Multikolinearitas VIF & Tolerance, Condition Index, Breusch-Pagan, Glejser, White, Cook's Distance, Leverage, Runs Test, dll).
9. **Statistika Non-Parametrik** (Mann-Whitney U Test, Wilcoxon Signed-Rank, Kruskal-Wallis H, Median Test, Sign Test, Friedman Two-Way ANOVA by Ranks, Kendall's W, Cochran's Q, Jonckheere-Terpstra, Rank Biserial Correlation, dll).
10. **Indikator Spesial BPS & Sosial Ekonomi** (Tingkat Pengangguran Terbuka [TPT %], TPAK %, Tingkat Kesempatan Kerja [TKK %], Garis Kemiskinan FGT P0, P1, P2, Sex Ratio, Dependency Ratio [Total/Muda/Lansia], IHK Laspeyres/Paasche/Fisher, Laju Inflasi %, Engel Food Share Ratio %, Gini Ratio, Rasio Palma, Kriteria Bank Dunia 40%, dll).

---

### 2. Random Dataset Generator Engine (Konteks Riil BPS)
Mendukung 5 skenario survei statistik:
- **Susenas Rumah Tangga (BPS)**: Pengeluaran makanan/non-makanan, pendapatan, ART, tipe daerah perdesaan/perkotaan, status kemiskinan.
- **Sakernas Ketenagakerjaan (BPS)**: Usia, pendidikan, status bekerja, jam kerja mingguan, upah bulanan, sektor usaha.
- **Sensus Pertanian (BPS)**: Luas lahan, komoditas, biaya pupuk/pestisida, hasil panen ton, jenis irigasi.
- **Survei Kepuasan Masyarakat (SKM Pelayanan PST)**: Waktu tunggu, skor Likert fasilitas/keramahan/kecepatan, indeks kepuasan IKM.
- **Evaluasi Diklat Statistik**: Nilai Pre-Test, Post-Test, Nilai Praktik SPSS, jam belajar mandiri, status kelulusan.

### 3. Ekspor Data Multi-Format
- **Excel (.xlsx)**: Dilengkapi format styling profesional, sheet Kamus Data, dan sheet Panduan Rumus Excel.
- **CSV (.csv)**: Format tabel standar untuk olah data Python / R / Stata.
- **Sintaks IBM SPSS (.sps)**: Sintaks siap eksekusi di SPSS (`GET DATA`, `VARIABLE LABELS`, `DESCRIPTIVES`, `ONEWAY`, `REGRESSION`, dll).

### 4. Automatic Answer Checker & Pembahasan Langkah Demi Langkah
- Menilai jawaban pengguna dengan **toleransi pembulatan desimal** ($\pm 0.05$ atau 1%).
- Menampilkan perbandingan jawaban pengguna vs nilai eksak komputasi.
- Memaparkan **rumus matematika**, **formula Microsoft Excel**, **menu navigasi IBM SPSS**, serta **interpretasi keputusan statistik**.

---

## 💻 Cara Menjalankan

### Persyaratan:
- Python 3.10+
- Dependencies: `fastapi`, `uvicorn`, `pandas`, `numpy`, `scipy`, `statsmodels`, `openpyxl`

### Instalasi & Menjalankan:
```bash
# 1. Install dependensi
pip install -r requirements.txt

# 2. Jalankan aplikasi
python run.py
```
Buka browser pada alamat: **`http://localhost:8000`**

### Menjalankan Unit Test Otomatis:
```bash
python -m unittest tests/test_stats_and_questions.py
```

---

## 📁 Struktur Direktori
```
15. Generator Tugas Random SPSS & Excel/
├── backend/
│   ├── app.py                      # FastAPI Web Server & API Endpoints
│   ├── dataset_generator.py        # Mesin pembuat dataset realistis BPS & Akademik
│   ├── question_bank_100.py        # Definisi 300 Template Soal Terstruktur
│   ├── question_engine.py          # Mesin instansiasi soal dinamis berbasis dataset aktif
│   ├── statistical_solver.py       # Mesin kalkulasi ilmiah (SciPy/Statsmodels/Pandas) & solver
│   └── export_service.py           # Layanan export data ke .xlsx, .csv, dan .sps
├── frontend/
│   ├── index.html                  # Halaman aplikasi web modern
│   ├── css/
│   │   └── style.css               # Styling Glassmorphism, animasi mikro, dan tema warna
│   └── js/
│       ├── app.js                  # Logika UI, state data, API fetcher, quiz runner
│       ├── question_renderer.js    # Komponen render kartu soal, validator input, kalkulator
│       └── charts.js               # Visualisasi grafik distribusi data & korelasi
├── tests/
│   └── test_stats_and_questions.py # Unit test untuk 300 soal dan keakuratan kalkulasi solver
├── requirements.txt                # Dependensi Python
├── run.py                          # Skrip peluncur server lokal satu klik
└── README.md                       # Dokumentasi lengkap proyek
```
