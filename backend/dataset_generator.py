"""
Dataset Generator Engine for Generator Tugas Random SPSS & Excel
Author: Antigravity
Generates realistic, customizable statistical datasets with BPS & Academic contexts.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class DatasetGenerator:
    AVAILABLE_THEMES = {
        "susenas_rt": {
            "id": "susenas_rt",
            "name": "Survei Sosial Ekonomi Nasional (Susenas BPS)",
            "description": "Dataset tingkat rumah tangga berisi pengeluaran, pendapatan, karakteristik demografi, dan perumahan.",
            "category": "Sosial & Ekonomi",
            "default_rows": 60,
        },
        "sakernas_kerja": {
            "id": "sakernas_kerja",
            "name": "Survei Angkatan Kerja Nasional (Sakernas BPS)",
            "description": "Dataset ketenagakerjaan berisi status bekerja, jam kerja, upah bulanan, tingkat pendidikan, dan sektor usaha.",
            "category": "Ketenagakerjaan",
            "default_rows": 60,
        },
        "sensus_pertanian": {
            "id": "sensus_pertanian",
            "name": "Sensus Pertanian BPS (Usaha Tani & Agrikultur)",
            "description": "Dataset produktivitas pertanian, luas lahan, biaya saprodi (pupuk/pestisida), dan hasil panen.",
            "category": "Pertanian",
            "default_rows": 50,
        },
        "pelayanan_publik": {
            "id": "pelayanan_publik",
            "name": "Survei Kepuasan Masyarakat (SKM / Pelayanan PST)",
            "description": "Dataset evaluasi pelayanan publik, skor kepuasan Likert, waktu tunggu, dan loyalitas pengguna data.",
            "category": "Pelayanan Publik",
            "default_rows": 50,
        },
        "evaluasi_diklat": {
            "id": "evaluasi_diklat",
            "name": "Evaluasi Diklat Statistik & Komputasi SPSS",
            "description": "Dataset hasil pelatihan pegawai/mahasiswa meliputi nilai pre-test, post-test, skor SPSS, dan metode belajar.",
            "category": "Pendidikan & Diklat",
            "default_rows": 45,
        },
    }

    @staticmethod
    def generate_dataset(
        theme_id: str = "susenas_rt",
        n_rows: int = 50,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        if seed is not None:
            np.random.seed(seed)
        else:
            seed = int(np.random.randint(1000, 999999))
            np.random.seed(seed)

        if theme_id == "susenas_rt":
            df, meta = DatasetGenerator._gen_susenas(n_rows)
        elif theme_id == "sakernas_kerja":
            df, meta = DatasetGenerator._gen_sakernas(n_rows)
        elif theme_id == "sensus_pertanian":
            df, meta = DatasetGenerator._gen_pertanian(n_rows)
        elif theme_id == "pelayanan_publik":
            df, meta = DatasetGenerator._gen_pelayanan(n_rows)
        elif theme_id == "evaluasi_diklat":
            df, meta = DatasetGenerator._gen_diklat(n_rows)
        else:
            df, meta = DatasetGenerator._gen_susenas(n_rows)
            theme_id = "susenas_rt"

        # Summary metadata
        theme_info = DatasetGenerator.AVAILABLE_THEMES.get(theme_id, {})
        records = df.to_dict(orient="records")

        # Column statistics summary for UI preview
        col_summaries = {}
        for col in df.columns:
            s = df[col]
            if pd.api.types.is_numeric_dtype(s):
                col_summaries[col] = {
                    "type": "numeric",
                    "min": float(s.min()),
                    "max": float(s.max()),
                    "mean": round(float(s.mean()), 2),
                    "median": round(float(s.median()), 2),
                    "std": round(float(s.std()), 2),
                }
            else:
                top_vals = s.value_counts().head(3).to_dict()
                col_summaries[col] = {
                    "type": "categorical",
                    "unique_count": int(s.nunique()),
                    "top_values": {str(k): int(v) for k, v in top_vals.items()},
                }

        return {
            "theme_id": theme_id,
            "theme_name": theme_info.get("name", "Dataset Statistik"),
            "description": theme_info.get("description", ""),
            "seed": seed,
            "total_rows": len(df),
            "columns": list(df.columns),
            "dictionary": meta["dictionary"],
            "column_summaries": col_summaries,
            "sample_data": records[:15],
            "all_data": records,
        }

    # =========================================================================
    # THEME 1: SUSENAS RUMAH TANGGA
    # =========================================================================
    @staticmethod
    def _gen_susenas(n: int) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        id_rt = [f"RT_{1001 + i}" for i in range(n)]
        wilayah_choices = ["Jawa Barat", "Jawa Tengah", "Jawa Timur", "Sumatera Utara", "Sulawesi Selatan"]
        wilayah = np.random.choice(wilayah_choices, size=n, p=[0.25, 0.25, 0.25, 0.15, 0.10])
        tipe_daerah = np.random.choice(["Perkotaan", "Perdesaan"], size=n, p=[0.55, 0.45])
        art = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], size=n, p=[0.05, 0.15, 0.30, 0.25, 0.15, 0.05, 0.03, 0.02])

        # Expenditure generation correlated with ART & Tipe Daerah
        base_exp = np.random.lognormal(mean=14.5, sigma=0.45, size=n)
        factor_urban = np.where(tipe_daerah == "Perkotaan", 1.35, 0.95)
        factor_art = 0.6 + 0.12 * art

        pendapatan = np.round(base_exp * factor_urban * factor_art, -4)  # Round to nearest 10,000
        pengeluaran_total = np.round(pendapatan * np.random.uniform(0.65, 0.92, size=n), -4)
        prop_makanan = np.random.uniform(0.40, 0.68, size=n)
        pengeluaran_makanan = np.round(pengeluaran_total * prop_makanan, -4)
        pengeluaran_non_makanan = pengeluaran_total - pengeluaran_makanan

        luas_lantai = np.round(np.clip(art * 15 + np.random.normal(25, 12, size=n), 18, 250), 1)
        status_rumah = np.random.choice(["Milik Sendiri", "Sewa/Kontrak", "Bebas Sewa/Menumpang"], size=n, p=[0.75, 0.18, 0.07])

        # Poverty Line threshold simulation (Rp 580,000 per kapita per bulan)
        garis_kemiskinan_perkapita = 580000
        pengeluaran_perkapita = pengeluaran_total / art
        status_miskin = np.where(pengeluaran_perkapita < garis_kemiskinan_perkapita, "Miskin", "Tidak Miskin")

        df = pd.DataFrame({
            "ID_RT": id_rt,
            "Wilayah": wilayah,
            "Tipe_Daerah": tipe_daerah,
            "Jumlah_ART": art,
            "Pendapatan_Bulanan": pendapatan.astype(int),
            "Pengeluaran_Makanan": pengeluaran_makanan.astype(int),
            "Pengeluaran_NonMakanan": pengeluaran_non_makanan.astype(int),
            "Total_Pengeluaran": pengeluaran_total.astype(int),
            "Pengeluaran_Perkapita": np.round(pengeluaran_perkapita, 0).astype(int),
            "Luas_Lantai_m2": luas_lantai,
            "Status_Rumah": status_rumah,
            "Status_Kemiskinan": status_miskin,
        })

        dictionary = {
            "ID_RT": "Nomor Pengenal Rumah Tangga Sampel",
            "Wilayah": "Provinsi lokasi sampel rumah tangga",
            "Tipe_Daerah": "Klasifikasi wilayah sensus (Perkotaan / Perdesaan)",
            "Jumlah_ART": "Banyaknya Anggota Rumah Tangga yang tinggal",
            "Pendapatan_Bulanan": "Total pendapatan seluruh ART per bulan (Rupiah)",
            "Pengeluaran_Makanan": "Pengeluaran konsumsi makanan sebulan (Rupiah)",
            "Pengeluaran_NonMakanan": "Pengeluaran komoditas non-makanan sebulan (Rupiah)",
            "Total_Pengeluaran": "Total pengeluaran konsumsi rumah tangga per bulan (Rupiah)",
            "Pengeluaran_Perkapita": "Total pengeluaran dibagi jumlah ART (Rupiah)",
            "Luas_Lantai_m2": "Luas lantai bangunan tempat tinggal (m²)",
            "Status_Rumah": "Status kepemilikan bangunan tempat tinggal",
            "Status_Kemiskinan": "Kategori kemiskinan berbasis garis kemiskinan perkapita",
        }

        return df, {"dictionary": dictionary}

    # =========================================================================
    # THEME 2: SAKERNAS KETENAGAKERJAAN
    # =========================================================================
    @staticmethod
    def _gen_sakernas(n: int) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        id_ind = [f"IND_{2001 + i}" for i in range(n)]
        jk = np.random.choice(["Laki-laki", "Perempuan"], size=n, p=[0.52, 0.48])
        usia = np.clip(np.random.normal(36, 11, size=n).astype(int), 17, 65)
        pendidikan = np.random.choice(["SD", "SMP", "SMA/SMK", "Diploma/Sarjana"], size=n, p=[0.18, 0.22, 0.42, 0.18])

        # Status bekerja
        status_bekerja = np.random.choice(["Bekerja", "Pengangguran", "Sekolah", "Mengurus Rumah Tangga"], size=n, p=[0.68, 0.08, 0.10, 0.14])

        sektor = []
        jam_kerja = []
        upah = []
        masa_kerja = []

        for i in range(n):
            if status_bekerja[i] == "Bekerja":
                sek = np.random.choice(["Pertanian", "Industri Pengolahan", "Perdagangan & Jasa"], p=[0.28, 0.32, 0.40])
                sektor.append(sek)
                jk_val = int(np.clip(np.random.normal(42, 8), 15, 60))
                jam_kerja.append(jk_val)

                # Base wage influenced by education & experience
                exp_years = max(1, min(usia[i] - 18, int(np.random.normal(8, 5))))
                masa_kerja.append(exp_years)

                edu_multiplier = {"SD": 1.0, "SMP": 1.25, "SMA/SMK": 1.65, "Diploma/Sarjana": 2.6}[pendidikan[i]]
                base_w = (2200000 + exp_years * 90000) * edu_multiplier * np.random.uniform(0.85, 1.2)
                upah.append(int(round(base_w, -4)))
            else:
                sektor.append("Tidak Bekerja")
                jam_kerja.append(0)
                masa_kerja.append(0)
                upah.append(0)

        df = pd.DataFrame({
            "ID_Individu": id_ind,
            "Jenis_Kelamin": jk,
            "Usia": usia,
            "Pendidikan": pendidikan,
            "Status_Bekerja": status_bekerja,
            "Sektor_Pekerjaan": sektor,
            "Masa_Kerja_Tahun": masa_kerja,
            "Jam_Kerja_Mingguan": jam_kerja,
            "Upah_Bulanan_Rp": upah,
        })

        dictionary = {
            "ID_Individu": "Nomor Registrasi Responden Sakernas",
            "Jenis_Kelamin": "Jenis kelamin responden",
            "Usia": "Usia responden (tahun)",
            "Pendidikan": "Tingkat pendidikan formal tertinggi yang ditamatkan",
            "Status_Bekerja": "Status kegiatan utama seminggu yang lalu",
            "Sektor_Pekerjaan": "Lapangan usaha / sektor pekerjaan responden",
            "Masa_Kerja_Tahun": "Lama pengalaman bekerja di bidang terkait (tahun)",
            "Jam_Kerja_Mingguan": "Jumlah jam kerja selama seminggu yang lalu",
            "Upah_Bulanan_Rp": "Pendapatan bersih / gaji sebulan (Rupiah)",
        }

        return df, {"dictionary": dictionary}

    # =========================================================================
    # THEME 3: SENSUS PERTANIAN (USAHA TANI)
    # =========================================================================
    @staticmethod
    def _gen_pertanian(n: int) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        id_petani = [f"PTN_{3001 + i}" for i in range(n)]
        komoditas = np.random.choice(["Padi Sawah", "Jagung Hibrida", "Kelapa Sawit", "Cabai Merah"], size=n, p=[0.40, 0.25, 0.20, 0.15])
        irigasi = np.random.choice(["Irigasi Teknis", "Irigasi Semi-Teknis", "Tadah Hujan"], size=n, p=[0.45, 0.35, 0.20])

        luas_lahan = np.round(np.clip(np.random.lognormal(mean=0.2, sigma=0.5, size=n), 0.2, 5.0), 2)
        tenaga_kerja = np.clip(np.round(luas_lahan * 2.5 + np.random.normal(1.5, 0.8, size=n)).astype(int), 1, 15)

        biaya_pupuk = np.round(luas_lahan * np.random.normal(2800000, 400000, size=n), -4)
        biaya_pestisida = np.round(luas_lahan * np.random.normal(1200000, 250000, size=n), -4)

        # Yield (Ton) correlated with fertilizer & irrigation
        irigasi_mult = np.where(irigasi == "Irigasi Teknis", 1.25, np.where(irigasi == "Irigasi Semi-Teknis", 1.05, 0.85))
        yield_per_ha = np.random.normal(5.8, 0.9, size=n) * irigasi_mult
        hasil_panen_ton = np.round(luas_lahan * yield_per_ha, 2)

        # Revenue
        harga_per_ton = np.where(komoditas == "Padi Sawah", 6200000, np.where(komoditas == "Jagung Hibrida", 5100000, np.where(komoditas == "Kelapa Sawit", 2800000, 18500000)))
        pendapatan_kotor = np.round(hasil_panen_ton * harga_per_ton, -4)
        keuntungan_bersih = pendapatan_kotor - biaya_pupuk - biaya_pestisida - (tenaga_kerja * 850000)

        df = pd.DataFrame({
            "ID_Petani": id_petani,
            "Komoditas": komoditas,
            "Jenis_Irigasi": irigasi,
            "Luas_Lahan_Ha": luas_lahan,
            "Tenaga_Kerja_Orang": tenaga_kerja,
            "Biaya_Pupuk_Rp": biaya_pupuk.astype(int),
            "Biaya_Pestisida_Rp": biaya_pestisida.astype(int),
            "Hasil_Panen_Ton": hasil_panen_ton,
            "Pendapatan_Kotor_Rp": pendapatan_kotor.astype(int),
            "Keuntungan_Bersih_Rp": keuntungan_bersih.astype(int),
        })

        dictionary = {
            "ID_Petani": "Nomor Registrasi Petani / Usaha Tani Sampel",
            "Komoditas": "Komoditas pangan / perkebunan utama yang diusahakan",
            "Jenis_Irigasi": "Kategori saluran pengairan sawah/lahan",
            "Luas_Lahan_Ha": "Luas lahan garapan yang dikelola (Hektar)",
            "Tenaga_Kerja_Orang": "Jumlah tenaga kerja yang terlibat selama masa tanam",
            "Biaya_Pupuk_Rp": "Total pengeluaran pupuk organik & anorganik (Rupiah)",
            "Biaya_Pestisida_Rp": "Total pengeluaran obat-obatan/pestisida (Rupiah)",
            "Hasil_Panen_Ton": "Total volume produksi hasil panen (Ton)",
            "Pendapatan_Kotor_Rp": "Total nilai penjualan hasil panen (Rupiah)",
            "Keuntungan_Bersih_Rp": "Pendapatan kotor dikurangi seluruh biaya produksi (Rupiah)",
        }

        return df, {"dictionary": dictionary}

    # =========================================================================
    # THEME 4: SURVEI KEPUASAN MASYARAKAT (SKM / PELAYANAN BPS)
    # =========================================================================
    @staticmethod
    def _gen_pelayanan(n: int) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        id_resp = [f"SKM_{4001 + i}" for i in range(n)]
        jk = np.random.choice(["Laki-laki", "Perempuan"], size=n, p=[0.55, 0.45])
        usia = np.clip(np.random.normal(32, 9, size=n).astype(int), 19, 60)
        jenis_layanan = np.random.choice(
            ["Pelayanan Statistik Terpadu (PST)", "Konsultasi Data Mikro", "Rekomendasi Kegiatan Statistik", "Pembelian Publikasi"],
            size=n,
            p=[0.45, 0.25, 0.20, 0.10],
        )

        waktu_tunggu = np.clip(np.round(np.random.exponential(scale=18, size=n) + 5).astype(int), 3, 60)

        # Likert scores (1-5)
        skor_fasilitas = np.clip(np.round(np.random.normal(4.1, 0.7, size=n)).astype(int), 1, 5)
        skor_kecepatan = np.clip(np.round(5.5 - (waktu_tunggu / 18.0) + np.random.normal(0, 0.4, size=n)).astype(int), 1, 5)
        skor_keramahan = np.clip(np.round(np.random.normal(4.3, 0.6, size=n)).astype(int), 1, 5)
        skor_kualitas_data = np.clip(np.round(np.random.normal(4.4, 0.6, size=n)).astype(int), 1, 5)

        # Index total (0 - 100)
        ikm_skor = np.round(((skor_fasilitas + skor_kecepatan + skor_keramahan + skor_kualitas_data) / 20.0) * 100, 1)
        loyalitas = np.where(ikm_skor >= 80, "Sangat Puas", np.where(ikm_skor >= 65, "Puas", "Kurang Puas"))

        df = pd.DataFrame({
            "ID_Responden": id_resp,
            "Jenis_Kelamin": jk,
            "Usia": usia,
            "Jenis_Layanan": jenis_layanan,
            "Waktu_Tunggu_Menit": waktu_tunggu,
            "Skor_Fasilitas": skor_fasilitas,
            "Skor_Kecepatan": skor_kecepatan,
            "Skor_Keramahan": skor_keramahan,
            "Skor_Kualitas_Data": skor_kualitas_data,
            "Indeks_Kepuasan_IKM": ikm_skor,
            "Kategori_Kepuasan": loyalitas,
        })

        dictionary = {
            "ID_Responden": "Nomor Registrasi Pengunjung / Responden",
            "Jenis_Kelamin": "Jenis kelamin responden",
            "Usia": "Usia responden (tahun)",
            "Jenis_Layanan": "Kategori layanan BPS yang diakses",
            "Waktu_Tunggu_Menit": "Durasi waktu menunggu hingga dilayani (menit)",
            "Skor_Fasilitas": "Penilaian sarana dan prasarana (Skala Likert 1-5)",
            "Skor_Kecepatan": "Penilaian kecepatan respon petugas (Skala Likert 1-5)",
            "Skor_Keramahan": "Penilaian kesopanan dan keramahan petugas (Skala Likert 1-5)",
            "Skor_Kualitas_Data": "Penilaian keakuratan dan kelengkapan data (Skala Likert 1-5)",
            "Indeks_Kepuasan_IKM": "Indeks Kepuasan Masyarakat terstandarisasi (Skala 0-100)",
            "Kategori_Kepuasan": "Klasifikasi tingkat kepuasan akhir responden",
        }

        return df, {"dictionary": dictionary}

    # =========================================================================
    # THEME 5: EVALUASI DIKLAT STATISTIK
    # =========================================================================
    @staticmethod
    def _gen_diklat(n: int) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        id_peserta = [f"DKT_{5001 + i}" for i in range(n)]
        divisi = np.random.choice(["Statistik Sosial", "Statistik Produksi", "Statistik Distribusi", "IPDS / IT", "Neraca & Analisis"], size=n)
        metode = np.random.choice(["Tatap Muka (Offline)", "Daring (Online Zoom)", "Hybrid"], size=n, p=[0.40, 0.35, 0.25])

        pre_test = np.clip(np.round(np.random.normal(54, 12, size=n)).astype(int), 25, 85)
        jam_belajar = np.clip(np.round(np.random.normal(24, 7, size=n)).astype(int), 8, 45)

        # Post test improves with learning hours & pre-test
        gain = jam_belajar * 0.75 + np.random.normal(18, 6, size=n)
        post_test = np.clip(np.round(pre_test + gain).astype(int), 45, 100)

        skor_praktek_spss = np.clip(np.round(0.4 * pre_test + 0.6 * post_test + np.random.normal(0, 4, size=n)).astype(int), 40, 100)
        kehadiran_pct = np.clip(np.round(np.random.normal(92, 7, size=n)).astype(int), 70, 100)
        kelulusan = np.where(post_test >= 70, "Lulus", "Tidak Lulus")

        df = pd.DataFrame({
            "ID_Peserta": id_peserta,
            "Divisi": divisi,
            "Metode_Pembelajaran": metode,
            "Jam_Belajar_Mandiri": jam_belajar,
            "Nilai_PreTest": pre_test,
            "Nilai_PostTest": post_test,
            "Nilai_Praktek_SPSS": skor_praktek_spss,
            "Kehadiran_Persen": kehadiran_pct,
            "Status_Kelulusan": kelulusan,
        })

        dictionary = {
            "ID_Peserta": "Nomor Induk Peserta Diklat",
            "Divisi": "Unit kerja asal peserta pelatihan",
            "Metode_Pembelajaran": "Metode penyampaian materi pelatihan",
            "Jam_Belajar_Mandiri": "Alokasi jam belajar mandiri dan latihan soal (jam)",
            "Nilai_PreTest": "Nilai tes kompetensi awal sebelum pelatihan (0-100)",
            "Nilai_PostTest": "Nilai tes evaluasi akhir setelah pelatihan (0-100)",
            "Nilai_Praktek_SPSS": "Nilai ujian praktik olah data software SPSS & Excel (0-100)",
            "Kehadiran_Persen": "Tingkat persentase presensi kehadiran sesi kelas (%)",
            "Status_Kelulusan": "Status penetapan kelulusan peserta diklat",
        }

        return df, {"dictionary": dictionary}
