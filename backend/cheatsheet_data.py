"""
Master Cheatsheet & Statistical Reference Data for SPSS & Excel
Author: BieM363 (https://github.com/BieM363)
Detailed step-by-step guides, decision criteria, and syntax for 12 SPSS tests & 16 Excel formulas.
"""

SPSS_NAV_MENUS = [
    {
        "id": "spss_explore",
        "analysis": "Statistika Deskriptif Lengkap",
        "category": "Deskriptif & Eksplorasi",
        "menu_path": "Analyze > Descriptive Statistics > Explore...",
        "output_key": "Mean, Median, 5% Trimmed, Std Dev, Variance, IQR, Skewness, Kurtosis, Boxplot",
        "purpose": "Menghitung ringkasan statistik pemusatan, penyebaran, bentuk distribusi, serta mendeteksi pencilan (outlier) secara visual.",
        "assumptions": "Variabel berskala numerik (interval / rasio).",
        "detailed_steps": [
            "Buka dataset di IBM SPSS (Data View).",
            "Klik menu utama: Analyze ➔ Descriptive Statistics ➔ Explore...",
            "Pindahkan variabel kontinu target ke kotak Dependent List.",
            "(Opsional) Pindahkan variabel kategori ke Factor List jika ingin membagi hasil per kelompok wilayah/grup.",
            "Pada bagian Display, pastikan memilih opsi 'Both' (Statistics & Plots).",
            "Klik tombol 'Statistics...' ➔ Centang Descriptives (Confidence Interval 95%) dan Outliers ➔ Klik Continue.",
            "Klik tombol 'Plots...' ➔ Centang Factor levels together dan Stem-and-leaf ➔ Klik Continue.",
            "Klik tombol 'OK' untuk menjalankan analisis."
        ],
        "decision_rule": "Outlier ditandai lingkaran (o) jika berjarak 1.5 - 3x IQR dari kuartil, atau bintang (*) jika > 3x IQR. Nilai Skewness antara -0.5 sampai +0.5 mengindikasikan distribusi simetris.",
        "example_case": "Mengevaluasi distribusi pengeluaran per kapita sebulan dan mendeteksi rumah tangga dengan pengeluaran ekstrem.",
        "spss_syntax": "EXAMINE VARIABLES=pengeluaran_perkapita /PLOT BOXPLOT STEMLEAF /STATISTICS DESCRIPTIVES /CINTERVAL 95 /MISSING LISTWISE."
    },
    {
        "id": "spss_freq",
        "analysis": "Tabel Frekuensi & Modus",
        "category": "Statistika Deskriptif",
        "menu_path": "Analyze > Descriptive Statistics > Frequencies...",
        "output_key": "Mode (Modus), Frekuensi, Persentase Valid, Persentase Kumulatif, Bar Chart / Histogram",
        "purpose": "Menghitung sebaran frekuensi data kategorik atau diskrit, menentukan nilai modus, persentil, dan membuat grafik distribusi.",
        "assumptions": "Dapat digunakan untuk semua skala data (nominal, ordinal, interval, rasio).",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Descriptive Statistics ➔ Frequencies...",
            "Pilih satu atau beberapa variabel target ➔ Klik tombol panah ke kotak Variable(s).",
            "Klik tombol 'Statistics...' ➔ Centang Mode, Median, Mean, Quartiles sesuai kebutuhan ➔ Klik Continue.",
            "Klik tombol 'Charts...' ➔ Pilih 'Bar charts' untuk data nominal/ordinal atau 'Histograms with normal curve' untuk numerik ➔ Klik Continue.",
            "Pastikan opsi 'Display frequency tables' dicentang ➔ Klik 'OK'."
        ],
        "decision_rule": "Modus adalah kategori dengan frekuensi tertinggi. 'Valid Percent' dihitung terhadap jumlah data yang tidak kosong (mengabaikan missing values).",
        "example_case": "Mengetahui proporsi status kemiskinan (Miskin vs Tidak Miskin) atau sektor pekerjaan responden.",
        "spss_syntax": "FREQUENCIES VARIABLES=status_miskin /STATISTICS=MODE /BARCHART /ORDER=ANALYSIS."
    },
    {
        "id": "spss_normality",
        "analysis": "Uji Normalitas (K-S & Shapiro-Wilk)",
        "category": "Uji Asumsi Klasik",
        "menu_path": "Analyze > Descriptive Statistics > Explore... (Plots > Normality plots with tests)",
        "output_key": "Tabel Tests of Normality (Kolmogorov-Smirnov & Shapiro-Wilk Statistic, df, Sig.)",
        "purpose": "Menguji apakah sebaran data sampel terdistribusi normal sebagai syarat utama penggunaan uji parametrik.",
        "assumptions": "Data numerik (interval / rasio) berasal dari sampel acak.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Descriptive Statistics ➔ Explore...",
            "Masukkan variabel target ke kotak Dependent List.",
            "Klik tombol 'Plots...'.",
            "Centang kotak 'Normality plots with tests'.",
            "Pada bagian Boxplots, pilih 'None' atau 'Factor levels together' ➔ Klik Continue.",
            "Klik 'OK' untuk menjalankan pengujian."
        ],
        "decision_rule": "• Jika N ≤ 50: Gunakan nilai Sig. pada uji Shapiro-Wilk.\\n• Jika N > 50: Gunakan nilai Sig. pada uji Kolmogorov-Smirnov (Lilliefors).\\n• Jika Sig. (p-value) > 0.05 ➔ Data berdistribusi NORMAL (H0 diterima).\\n• Jika Sig. (p-value) ≤ 0.05 ➔ Data TIDAK berdistribusi normal (H0 ditolak, disarankan transformasi data atau uji non-parametrik).",
        "example_case": "Memeriksa kenormalan data pendapatan sebelum dilakukan Uji t atau Analisis Regresi.",
        "spss_syntax": "EXAMINE VARIABLES=pendapatan /PLOT NPPLOT /STATISTICS NONE /MISSING LISTWISE."
    },
    {
        "id": "spss_ttest_1samp",
        "analysis": "Uji t Satu Sampel",
        "category": "Uji Komparatif Parametrik",
        "menu_path": "Analyze > Compare Means > One-Sample T Test... (Isi Test Value)",
        "output_key": "t-statistic, df, Sig. (2-tailed), Mean Difference, 95% Confidence Interval",
        "purpose": "Menguji apakah rata-rata (mean) dari satu populasi sama dengan nilai konstanta/standar hipotesis acuan (μ0).",
        "assumptions": "Data berskala interval/rasio, sampel acak independen, data berdistribusi normal.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Compare Means ➔ One-Sample T Test...",
            "Pindahkan variabel kontinu ke kotak Test Variable(s).",
            "Ketikkan nilai acuan hipotesis pada kotak 'Test Value' (misal: 50 atau nilai target nasional).",
            "Klik tombol 'Options...' untuk memastikan Confidence Interval = 95% ➔ Klik Continue.",
            "Klik 'OK'."
        ],
        "decision_rule": "• Jika Sig. (2-tailed) < 0.05 ➔ Tolak H0 (Rata-rata sampel BERBEDA signifikan dari nilai Test Value).\\n• Jika Sig. (2-tailed) ≥ 0.05 ➔ Gagal tolak H0 (Tidak ada perbedaan signifikan antara rata-rata sampel dengan Test Value).",
        "example_case": "Menguji apakah rata-rata jam kerja mingguan karyawan berbeda secara nyata dari standar 40 jam.",
        "spss_syntax": "T-TEST /TESTVAL=40 /MISSING=ANALYSIS /VARIABLES=jam_kerja /CRITERIA=CI(.95)."
    },
    {
        "id": "spss_ttest_ind",
        "analysis": "Uji t Dua Sampel Independen",
        "category": "Uji Komparatif Parametrik",
        "menu_path": "Analyze > Compare Means > Independent-Samples T Test...",
        "output_key": "Levene's Test (F & Sig.), t-statistic, df, Sig. (2-tailed), Mean Difference, Std. Error",
        "purpose": "Membandingkan rata-rata antara 2 kelompok sampel yang saling bebas (tidak berhubungan).",
        "assumptions": "Data numerik berdistribusi normal pada kedua kelompok, subjek saling independen.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Compare Means ➔ Independent-Samples T Test...",
            "Pindahkan variabel terikat numerik ke kotak Test Variable(s).",
            "Pindahkan variabel pembeda kelompok ke kotak Grouping Variable.",
            "Klik tombol 'Define Groups...' ➔ Masukkan kode grup (misal: Group 1 = 1, Group 2 = 2) ➔ Klik Continue.",
            "Klik 'OK'."
        ],
        "decision_rule": "1. Periksa Levene's Test for Equality of Variances:\\n   - Jika Sig. Levene > 0.05 ➔ Varians Homogen, baca baris 'Equal variances assumed'.\\n   - Jika Sig. Levene ≤ 0.05 ➔ Varians Tidak Homogen, baca baris 'Equal variances not assumed'.\\n2. Periksa Sig. (2-tailed):\\n   - Jika Sig. < 0.05 ➔ Tolak H0 (Ada perbedaan rata-rata yang signifikan antara kedua kelompok).\\n   - Jika Sig. ≥ 0.05 ➔ Gagal tolak H0 (Tidak ada perbedaan rata-rata yang signifikan).",
        "example_case": "Menguji perbedaan rata-rata pengeluaran pangan antara rumah tangga di Perkotaan vs Perdesaan.",
        "spss_syntax": "T-TEST GROUPS=wilayah(1 2) /VARIABLES=pengeluaran /CRITERIA=CI(.95)."
    },
    {
        "id": "spss_ttest_paired",
        "analysis": "Uji t Sampel Berpasangan",
        "category": "Uji Komparatif Parametrik",
        "menu_path": "Analyze > Compare Means > Paired-Samples T Test...",
        "output_key": "Paired Differences (Mean, Std. Dev, Std. Error), t, df, Sig. (2-tailed)",
        "purpose": "Menguji signifikansi perbedaan rata-rata pada 2 kondisi pengukuran berbeda pada subjek yang sama (Before vs After).",
        "assumptions": "Sampel berpasangan, selisih (d = Before - After) berdistribusi normal.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Compare Means ➔ Paired-Samples T Test...",
            "Pilih variabel kondisi 1 (Before) dan variabel kondisi 2 (After) bersamaan, lalu klik panah ke kotak Paired Variables (muncul Pair 1: Var1 - Var2).",
            "Klik tombol 'Options...' jika ingin menyesuaikan tingkat kepercayaan (default 95%).",
            "Klik 'OK'."
        ],
        "decision_rule": "• Jika Sig. (2-tailed) < 0.05 ➔ Tolak H0 (Terdapat perbedaan rata-rata yang signifikan antara sebelum dan sesudah intervensi).\\n• Jika Sig. (2-tailed) ≥ 0.05 ➔ Gagal tolak H0 (Tidak ada perbedaan yang signifikan).",
        "example_case": "Evaluasi dampak pelatihan terhadap produktivitas kerja petani sebelum vs sesudah program.",
        "spss_syntax": "T-TEST PAIRS=produktivitas_pre WITH produktivitas_post (PAIRED) /CRITERIA=CI(.95) /MISSING=ANALYSIS."
    },
    {
        "id": "spss_anova",
        "analysis": "One-Way ANOVA",
        "category": "Uji Komparatif Parametrik (> 2 Kelompok)",
        "menu_path": "Analyze > Compare Means > One-Way ANOVA... (Post Hoc > Tukey)",
        "output_key": "ANOVA Table (Sum of Squares, df, Mean Square, F, Sig.), Test of Homogeneity, Post Hoc",
        "purpose": "Menguji apakah terdapat perbedaan rata-rata antara 3 kelompok atau lebih.",
        "assumptions": "Data numerik berdistribusi normal di tiap kelompok, varians antarkelompok homogen, observasi independen.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Compare Means ➔ One-Way ANOVA...",
            "Pindahkan variabel dependen numerik ke Dependent List.",
            "Pindahkan variabel faktor (> 2 kelompok) ke Factor.",
            "Klik tombol 'Post Hoc...' ➔ Centang 'Tukey' (jika varians homogen) atau 'Games-Howell' (jika tidak homogen) ➔ Klik Continue.",
            "Klik tombol 'Options...' ➔ Centang 'Descriptive' dan 'Homogeneity of variance test' ➔ Klik Continue.",
            "Klik 'OK'."
        ],
        "decision_rule": "• Jika Sig. ANOVA < 0.05 ➔ Tolak H0 (Minimal ada satu pasang kelompok yang berbeda signifikan). Lanjut baca tabel Multiple Comparisons (Post Hoc) untuk melihat pasangan mana yang berbeda (tanda *).\\n• Jika Sig. ANOVA ≥ 0.05 ➔ Gagal tolak H0 (Semua kelompok memiliki rata-rata yang sama).",
        "example_case": "Membandingkan hasil panen padi per hektar antar 4 jenis pupuk yang berbeda.",
        "spss_syntax": "ONEWAY hasil_panen BY jenis_pupuk /STATISTICS DESCRIPTIVES HOMOGENEITY /POSTHOC=TUKEY ALPHA(0.05)."
    },
    {
        "id": "spss_correlation",
        "analysis": "Korelasi Bivariat (Pearson & Spearman)",
        "category": "Uji Hubungan / Asosiatif",
        "menu_path": "Analyze > Correlate > Bivariate...",
        "output_key": "Pearson r / Spearman rho, Sig. (2-tailed), N, Flagged Correlations (**)",
        "purpose": "Mengukur kekuatan (derajat asosiasi) dan arah hubungan linier/monotonik antara dua variabel numerik.",
        "assumptions": "Pearson: data interval/rasio normal linier. Spearman: data ordinal atau numerik non-normal.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Correlate ➔ Bivariate...",
            "Pindahkan kedua variabel ke kotak Variables.",
            "Pada Correlation Coefficients, centang 'Pearson' atau 'Spearman'.",
            "Pada Test of Significance, pilih 'Two-tailed' dan centang 'Flag significant correlations'.",
            "Klik tombol 'Options...' jika ingin menampilkan Means & Standard deviations ➔ Klik Continue.",
            "Klik 'OK'."
        ],
        "decision_rule": "1. Kekuatan Hubungan (|r|):\\n   • 0.00 - 0.19: Sangat Lemah | 0.20 - 0.39: Lemah | 0.40 - 0.59: Sedang | 0.60 - 0.79: Kuat | 0.80 - 1.00: Sangat Kuat.\\n2. Arah Hubungan: (+) Searah, (-) Berlawanan arah.\\n3. Signifikansi: Jika Sig. (2-tailed) < 0.05 ➔ Hubungan korelasi signifikan secara statistik.",
        "example_case": "Menganalisis hubungan antara lama pendidikan kepala keluarga dengan total pendapatan keluarga.",
        "spss_syntax": "CORRELATIONS /VARIABLES=pendidikan pendapatan /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE."
    },
    {
        "id": "spss_chisq",
        "analysis": "Tabel Kontingensi & Uji Chi-Square",
        "category": "Uji Hubungan Non-Parametrik",
        "menu_path": "Analyze > Descriptive Statistics > Crosstabs... (Statistics > Chi-Square, Phi/Cramer)",
        "output_key": "Pearson Chi-Square Value, df, Asymp. Sig. (2-sided), Expected Counts, Cramer's V",
        "purpose": "Menguji hubungan/independensi antara dua variabel kategorik (nominal atau ordinal).",
        "assumptions": "Data frekuensi/kategori, tidak boleh ada sel dengan Expected Count < 5 melebihi 20% dari total sel.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Descriptive Statistics ➔ Crosstabs...",
            "Pindahkan variabel kategori 1 ke Row(s) dan variabel kategori 2 ke Column(s).",
            "Klik tombol 'Statistics...' ➔ Centang 'Chi-square' dan 'Phi and Cramer\\'s V' ➔ Klik Continue.",
            "Klik tombol 'Cells...' ➔ Centang 'Observed', 'Expected', dan 'Row / Column Percentages' ➔ Klik Continue.",
            "Klik 'OK'."
        ],
        "decision_rule": "• Periksa catatan di bawah tabel Chi-Square: Pastikan sel dengan expected count < 5 tidak lebih dari 20%.\\n• Jika Asymp. Sig. (2-sided) < 0.05 ➔ Tolak H0 (Ada hubungan signifikan antara kedua variabel kategorik).\\n• Jika Asymp. Sig. ≥ 0.05 ➔ Gagal tolak H0 (Kedua variabel independen / tidak berhubungan).",
        "example_case": "Menguji apakah ada hubungan antara klasifikasi daerah (Kota/Desa) dengan partisipasi program BPJS.",
        "spss_syntax": "CROSSTABS /TABLES=klasifikasi_daerah BY ikut_bpjs /STATISTICS=CHISQ PHI /CELLS=COUNT EXPECTED ROW."
    },
    {
        "id": "spss_regression",
        "analysis": "Regresi Linear & Asumsi Klasik",
        "category": "Analisis Pengaruh & Prediksi",
        "menu_path": "Analyze > Regression > Linear... (Statistics > Collinearity, Durbin-Watson)",
        "output_key": "Model Summary (R, R², Adjusted R²), ANOVA Table (F, Sig.), Coefficients (Unstandardized B, t, Sig., VIF)",
        "purpose": "Menentukan persamaan regresi Y = a + bX, mengukur persentase pengaruh X terhadap Y (R²), dan memprediksi nilai Y.",
        "assumptions": "Hubungan linier, data berdistribusi normal, tidak terjadi multikolinearitas (VIF < 10), tidak ada autokorelasi (Durbin-Watson ~ 2), homoskedastisitas.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Regression ➔ Linear...",
            "Pindahkan variabel terikat (Y) ke kotak Dependent.",
            "Pindahkan satu atau lebih variabel bebas (X) ke kotak Independent(s).",
            "Klik tombol 'Statistics...' ➔ Centang 'Estimates', 'Model fit', 'R squared change', 'Collinearity diagnostics', dan 'Durbin-Watson' ➔ Klik Continue.",
            "Klik tombol 'Plots...' ➔ Masukkan *ZRESID ke Y dan *ZPRED ke X untuk memeriksa heteroskedastisitas ➔ Klik Continue.",
            "Klik 'OK'."
        ],
        "decision_rule": "1. Uji Simultan (F): Jika Sig. F pada tabel ANOVA < 0.05 ➔ Model regresi valid/signifikan secara simultan.\\n2. Uji Parsial (t): Jika Sig. t pada tabel Coefficients < 0.05 ➔ Variabel X berpengaruh signifikan terhadap Y.\\n3. Koefisien Determinasi (R²): Menunjukkan berapa % variasi Y yang dapat dijelaskan oleh X.",
        "example_case": "Menganalisis pengaruh luas lahan dan biaya pupuk terhadap hasil produksi padi.",
        "spss_syntax": "REGRESSION /MISSING LISTWISE /STATISTICS COEFF OUTS R ANOVA COLLIN TOL /DEPENDENT produksi /METHOD=ENTER luas_lahan pupuk."
    },
    {
        "id": "spss_mann_whitney",
        "analysis": "Uji Mann-Whitney U",
        "category": "Uji Komparatif Non-Parametrik (2 Kelompok)",
        "menu_path": "Analyze > Nonparametric Tests > Legacy Dialogs > 2 Independent Samples...",
        "output_key": "Mann-Whitney U Statistic, Wilcoxon W, Z-score, Asymp. Sig. (2-tailed), Mean Rank",
        "purpose": "Alternatif Uji t 2 Sampel Independen jika data berskala ordinal atau data kontinu tidak berdistribusi normal.",
        "assumptions": "Dua kelompok saling independen, data berskala minimal ordinal.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Nonparametric Tests ➔ Legacy Dialogs ➔ 2 Independent Samples...",
            "Pindahkan variabel uji ke Test Variable List.",
            "Pindahkan variabel kategori ke Grouping Variable ➔ Klik 'Define Groups...' (isi 1 dan 2) ➔ Klik Continue.",
            "Pada bagian Test Type, centang 'Mann-Whitney U'.",
            "Klik 'OK'."
        ],
        "decision_rule": "• Jika Asymp. Sig. (2-tailed) < 0.05 ➔ Tolak H0 (Terdapat perbedaan peringkat/distribusi yang signifikan antara kedua kelompok).\\n• Jika Asymp. Sig. ≥ 0.05 ➔ Gagal tolak H0 (Tidak ada perbedaan signifikan).",
        "example_case": "Membandingkan skor kepuasan pelayanan publik (skala Likert 1-5) antara warga pria dan wanita.",
        "spss_syntax": "NPAR TESTS /M-W= skor_kepuasan BY gender(1 2) /MISSING ANALYSIS."
    },
    {
        "id": "spss_kruskal_wallis",
        "analysis": "Uji Kruskal-Wallis H",
        "category": "Uji Komparatif Non-Parametrik (> 2 Kelompok)",
        "menu_path": "Analyze > Nonparametric Tests > Legacy Dialogs > K Independent Samples...",
        "output_key": "Kruskal-Wallis H (Chi-Square Statistic), df, Asymp. Sig., Mean Rank",
        "purpose": "Alternatif One-Way ANOVA untuk membandingkan > 2 kelompok independen jika data berskala ordinal atau tidak memenuhi asumsi normalitas.",
        "assumptions": "Data berpasangan/berkelompok > 2, skala data minimal ordinal, observasi independen.",
        "detailed_steps": [
            "Klik menu: Analyze ➔ Nonparametric Tests ➔ Legacy Dialogs ➔ K Independent Samples...",
            "Pindahkan variabel uji ke Test Variable List.",
            "Pindahkan variabel kelompok ke Grouping Variable ➔ Klik 'Define Range...' (masukkan rentang minimum 1 dan maksimum k) ➔ Klik Continue.",
            "Centang 'Kruskal-Wallis H'.",
            "Klik 'OK'."
        ],
        "decision_rule": "• Jika Asymp. Sig. < 0.05 ➔ Tolak H0 (Terdapat perbedaan peringkat yang signifikan antara kelompok-kelompok tersebut).\\n• Jika Asymp. Sig. ≥ 0.05 ➔ Gagal tolak H0 (Tidak ada perbedaan peringkat yang signifikan).",
        "example_case": "Membandingkan tingkat kepuasan pelanggan terhadap 3 operator telekomunikasi yang berbeda.",
        "spss_syntax": "NPAR TESTS /K-W=skor_layanan BY provider(1 3) /MISSING ANALYSIS."
    }
]

EXCEL_FORMULAS = [
    {
        "id": "excel_average",
        "category": "Tendensi Sentral",
        "name": "Mean / Rata-rata",
        "formula": "=AVERAGE(range)",
        "note": "Mengabaikan cell kosong & teks",
        "purpose": "Menghitung rata-rata aritmatika dari sekumpulan nilai numerik.",
        "syntax": "=AVERAGE(number1, [number2], ...)",
        "example": "=AVERAGE(C2:C51) menghasilkan nilai rata-rata dari kolom C baris 2 hingga 51.",
        "tips": "Jika cell bernilai angka 0, tetap dihitung dalam pembagi. Jika cell benar-benar kosong atau teks, cell dilewati secara otomatis."
    },
    {
        "id": "excel_median",
        "category": "Tendensi Sentral",
        "name": "Median / Nilai Tengah",
        "formula": "=MEDIAN(range)",
        "note": "Membagi data urut 50-50",
        "purpose": "Mencari nilai tengah dari sekumpulan data numerik yang telah diurutkan.",
        "syntax": "=MEDIAN(number1, [number2], ...)",
        "example": "=MEDIAN(C2:C51) membagi separuh data di bawah median dan separuh di atasnya.",
        "tips": "Sangat tangguh terhadap outlier (pencilan ekstrem) dibandingkan nilai rata-rata (Mean)."
    },
    {
        "id": "excel_mode",
        "category": "Tendensi Sentral",
        "name": "Modus",
        "formula": "=MODE.SNGL(range)",
        "note": "Nilai paling sering muncul",
        "purpose": "Menemukan nilai yang paling sering/banyak muncul dalam suatu kumpulan data.",
        "syntax": "=MODE.SNGL(number1, [number2], ...)",
        "example": "=MODE.SNGL(C2:C51)",
        "tips": "Jika tidak ada angka yang berulang sama sekali, formula akan menghasilkan error #N/A."
    },
    {
        "id": "excel_stdev",
        "category": "Dispersi",
        "name": "Standar Deviasi Sampel",
        "formula": "=STDEV.S(range)",
        "note": "Pembagi n - 1 (Bessel Correction)",
        "purpose": "Mengukur seberapa jauh sebaran titik data dari nilai rata-ratanya pada sampel.",
        "syntax": "=STDEV.S(number1, [number2], ...)",
        "example": "=STDEV.S(C2:C51)",
        "tips": "Gunakan STDEV.S untuk data sampel (pembagi n-1). Jika menghitung seluruh populasi, gunakan STDEV.P (pembagi N)."
    },
    {
        "id": "excel_var",
        "category": "Dispersi",
        "name": "Varians Sampel",
        "formula": "=VAR.S(range)",
        "note": "s kuadrat (akar dari deviasi)",
        "purpose": "Mengukur kuadrat dari simpangan rata-rata sampel.",
        "syntax": "=VAR.S(number1, [number2], ...)",
        "example": "=VAR.S(C2:C51)",
        "tips": "Nilai varians adalah kuadrat dari standar deviasi: VAR.S = (STDEV.S)^2."
    },
    {
        "id": "excel_q1",
        "category": "Dispersi",
        "name": "Kuartil 1 (Q1)",
        "formula": "=QUARTILE.INC(range, 1)",
        "note": "Percentile 25 (Batas 25% terbawah)",
        "purpose": "Menghitung batas nilai yang memisahkan 25% data terendah.",
        "syntax": "=QUARTILE.INC(array, quart)",
        "example": "=QUARTILE.INC(C2:C51, 1)",
        "tips": "Argumen quart: 0 = Min, 1 = Q1 (25%), 2 = Median (50%), 3 = Q3 (75%), 4 = Max."
    },
    {
        "id": "excel_q3",
        "category": "Dispersi",
        "name": "Kuartil 3 (Q3)",
        "formula": "=QUARTILE.INC(range, 3)",
        "note": "Percentile 75 (Batas 75% data)",
        "purpose": "Menghitung batas nilai yang memisahkan 75% data terendah (atau 25% data teratas).",
        "syntax": "=QUARTILE.INC(array, 3)",
        "example": "=QUARTILE.INC(C2:C51, 3)",
        "tips": "Jarak antara Q3 dan Q1 adalah Interquartile Range (IQR)."
    },
    {
        "id": "excel_iqr",
        "category": "Dispersi",
        "name": "Jangkauan Antarkuartil (IQR)",
        "formula": "=QUARTILE.INC(range,3) - QUARTILE.INC(range,1)",
        "note": "Ukuran penyebaran 50% data tengah",
        "purpose": "Mengukur rentang penyebaran 50% data di bagian tengah, bebas dari pengaruh data ekstrem.",
        "syntax": "=QUARTILE.INC(range, 3) - QUARTILE.INC(range, 1)",
        "example": "=QUARTILE.INC(C2:C51, 3) - QUARTILE.INC(C2:C51, 1)",
        "tips": "IQR dipakai untuk menentukan batas outlier: Batas Bawah = Q1 - 1.5*IQR, Batas Atas = Q3 + 1.5*IQR."
    },
    {
        "id": "excel_ttest_ind",
        "category": "Uji Parametrik",
        "name": "Uji t Dua Sampel",
        "formula": "=T.TEST(array1, array2, 2, 2)",
        "note": "Two-tailed, Equal Variance",
        "purpose": "Menghitung p-value uji beda rata-rata antara 2 kelompok independen.",
        "syntax": "=T.TEST(array1, array2, tails, type)",
        "example": "=T.TEST(C2:C25, C26:C50, 2, 2)",
        "tips": "Argumen type: 1 = Paired, 2 = Two-sample equal variance (Homoscedastic), 3 = Two-sample unequal variance (Heteroscedastic)."
    },
    {
        "id": "excel_ttest_paired",
        "category": "Uji Parametrik",
        "name": "Uji t Berpasangan",
        "formula": "=T.TEST(array_pre, array_post, 2, 1)",
        "note": "Two-tailed, Paired",
        "purpose": "Menghitung p-value uji beda berpasangan sebelum vs sesudah intervensi.",
        "syntax": "=T.TEST(array1, array2, 2, 1)",
        "example": "=T.TEST(C2:C50, D2:D50, 2, 1)",
        "tips": "Kedua array harus memiliki jumlah observasi (panjang baris) yang persis sama."
    },
    {
        "id": "excel_correl",
        "category": "Korelasi & Regresi",
        "name": "Korelasi Pearson",
        "formula": "=CORREL(array1, array2)",
        "note": "Rentang nilai -1.0 sd +1.0",
        "purpose": "Menghitung koefisien korelasi linier Pearson (r) antara dua variabel kontinu.",
        "syntax": "=CORREL(array1, array2)",
        "example": "=CORREL(C2:C51, D2:D51)",
        "tips": "Nilai mendekati +1 berarti hubungan positif kuat, mendekati -1 berarti negatif kuat, dan 0 berarti tidak ada hubungan linier."
    },
    {
        "id": "excel_slope",
        "category": "Korelasi & Regresi",
        "name": "Slope Regresi (b)",
        "formula": "=SLOPE(known_y's, known_x's)",
        "note": "Kemiringan garis regresi",
        "purpose": "Menghitung koefisien arah (slope) dari persamaan garis regresi linier y = a + bx.",
        "syntax": "=SLOPE(known_y's, known_x's)",
        "example": "=SLOPE(D2:D51, C2:C51)",
        "tips": "Pastikan urutan argumen adalah Y (variabel dependen) terlebih dahulu, baru kemudian X (variabel independen)."
    },
    {
        "id": "excel_intercept",
        "category": "Korelasi & Regresi",
        "name": "Intercept Regresi (a)",
        "formula": "=INTERCEPT(known_y's, known_x's)",
        "note": "Titik potong sumbu Y",
        "purpose": "Menghitung konstanta titik potong sumbu Y saat nilai X bernilai 0.",
        "syntax": "=INTERCEPT(known_y's, known_x's)",
        "example": "=INTERCEPT(D2:D51, C2:C51)",
        "tips": "Persamaan garis lengkap: Y_hat = INTERCEPT(...) + SLOPE(...) * X."
    },
    {
        "id": "excel_rsq",
        "category": "Korelasi & Regresi",
        "name": "R-Square (R²)",
        "formula": "=RSQ(known_y's, known_x's)",
        "note": "Koefisien determinasi (proporsi varians)",
        "purpose": "Menghitung proporsi variansi variabel dependen Y yang dapat diterangkan oleh variabel independen X.",
        "syntax": "=RSQ(known_y's, known_x's)",
        "example": "=RSQ(D2:D51, C2:C51)",
        "tips": "Nilai R² berada dalam rentang 0.0 sampai 1.0 (misal: R² = 0.64 berarti 64% variasi Y dijelaskan oleh X)."
    },
    {
        "id": "excel_forecast",
        "category": "Korelasi & Regresi",
        "name": "Prediksi Nilai Y Linier",
        "formula": "=FORECAST.LINEAR(x, known_y's, known_x's)",
        "note": "Estimasi Y_hat untuk nilai X tertentu",
        "purpose": "Menghitung nilai ramalan/prediksi Y berdasarkan tren linier masa lalu untuk suatu input nilai x.",
        "syntax": "=FORECAST.LINEAR(x, known_y's, known_x's)",
        "example": "=FORECAST.LINEAR(25, D2:D51, C2:C51)",
        "tips": "Sangat praktis untuk memproyeksikan target tanpa perlu menyusun persamaan regresi secara manual terlebih dahulu."
    },
    {
        "id": "excel_chisq",
        "category": "Chi-Square",
        "name": "Uji Independensi Chi-Square",
        "formula": "=CHISQ.TEST(actual_range, expected_range)",
        "note": "Menghasilkan p-value uji asosiasi",
        "purpose": "Menghitung p-value dari uji Chi-Square untuk tabel kontingensi baris x kolom.",
        "syntax": "=CHISQ.TEST(actual_range, expected_range)",
        "example": "=CHISQ.TEST(B2:C3, E2:F3)",
        "tips": "actual_range adalah tabel observasi riil, sedangkan expected_range adalah tabel frekuensi harapan yang dihitung dari (Total Baris * Total Kolom / Total Keseluruhan)."
    }
]
