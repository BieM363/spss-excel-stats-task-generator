"""
Statistical Solver Engine for Generator Tugas Random SPSS & Excel
Author: BieM363 (https://github.com/BieM363)
Provides exact statistical computations, formula derivations,
Excel formulas, and SPSS menu instructions for all 300 question types.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor


class StatisticalSolver:
    @staticmethod
    def _clean_series(s: Union[pd.Series, List, np.ndarray]) -> np.ndarray:
        arr = np.array(s, dtype=float)
        return arr[~np.isnan(arr)]

    # =========================================================================
    # CATEGORY 1: STATISTIKA DESKRIPTIF & TENDENSI SENTRAL (Soal 1 - 10)
    # =========================================================================

    @staticmethod
    def calculate_mean(data: Union[pd.Series, List[float]]) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        n = len(arr)
        total = float(np.sum(arr))
        mean_val = float(np.mean(arr)) if n > 0 else 0.0
        return {
            "value": round(mean_val, 4),
            "n": n,
            "sum": round(total, 4),
            "excel_formula": "=AVERAGE(range)",
            "spss_menu": "Analyze > Descriptive Statistics > Frequencies... (pilih Statistics > Mean)",
            "spss_syntax": "FREQUENCIES VARIABLES=var /STATISTICS=MEAN.",
            "formula_tex": r"\bar{X} = \frac{\sum_{i=1}^n X_i}{n}",
            "steps": [
                f"Jumlahkan seluruh nilai data: Total = {total:,.2f}",
                f"Bagi dengan banyak observasi (n = {n}): {total:,.2f} / {n} = {mean_val:,.4f}",
            ],
            "conclusion": f"Rata-rata (Mean) dari data adalah {mean_val:,.4f}",
        }

    @staticmethod
    def calculate_median(data: Union[pd.Series, List[float]]) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        n = len(arr)
        med_val = float(np.median(arr)) if n > 0 else 0.0
        sorted_arr = np.sort(arr)
        return {
            "value": round(med_val, 4),
            "n": n,
            "excel_formula": "=MEDIAN(range)",
            "spss_menu": "Analyze > Descriptive Statistics > Explore... atau Frequencies...",
            "spss_syntax": "FREQUENCIES VARIABLES=var /STATISTICS=MEDIAN.",
            "formula_tex": r"Median = X_{(\frac{n+1}{2})} \text{ (jika n ganjil)} \text{ atau } \frac{X_{(n/2)} + X_{(n/2+1)}}{2}",
            "steps": [
                f"Urutkan data dari terkecil hingga terbesar (n = {n})",
                f"Nilai tengah (posisi {(n+1)/2:.1f}) diperoleh sebesar: {med_val:,.4f}",
            ],
            "conclusion": f"Median (nilai tengah data yang telah diurutkan) adalah {med_val:,.4f}",
        }

    @staticmethod
    def calculate_mode(data: Union[pd.Series, List[float]]) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        vals, counts = np.unique(arr, return_counts=True)
        max_c = np.max(counts)
        modes = vals[counts == max_c].tolist()
        primary_mode = float(modes[0]) if len(modes) > 0 else 0.0
        return {
            "value": round(primary_mode, 4),
            "all_modes": [round(m, 4) for m in modes],
            "max_frequency": int(max_c),
            "excel_formula": "=MODE.SNGL(range) atau =MODE.MULT(range)",
            "spss_menu": "Analyze > Descriptive Statistics > Frequencies... (pilih Statistics > Mode)",
            "spss_syntax": "FREQUENCIES VARIABLES=var /STATISTICS=MODE.",
            "formula_tex": r"\text{Modus} = \text{Nilai dengan frekuensi kemunculan tertinggi}",
            "steps": [
                f"Hitung frekuensi setiap angka unik",
                f"Frekuensi terbanyak adalah {max_c} kali, dimiliki oleh nilai {primary_mode:,.4f}",
            ],
            "conclusion": f"Modus data adalah {primary_mode:,.4f} dengan kemunculan sebanyak {max_c} kali.",
        }

    @staticmethod
    def calculate_trimmed_mean(
        data: Union[pd.Series, List[float]], proportioncut: float = 0.05
    ) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        tm_val = float(stats.trim_mean(arr, proportioncut))
        pct = int(proportioncut * 100)
        return {
            "value": round(tm_val, 4),
            "proportion_cut": proportioncut,
            "excel_formula": f"=TRIMMEAN(range, {proportioncut*2})",
            "spss_menu": "Analyze > Descriptive Statistics > Explore... (Otomatis menghasilkan 5% Trimmed Mean)",
            "spss_syntax": "EXAMINE VARIABLES=var /STATISTICS DESCRIPTIVES.",
            "formula_tex": r"\bar{X}_{\text{trimmed}} = \frac{\sum_{i=k+1}^{n-k} X_{(i)}}{n - 2k}",
            "steps": [
                f"Urutkan data dan potong {pct}% data terkecil dan {pct}% data terbesar",
                f"Hitung rata-rata dari data yang tersisa: {tm_val:,.4f}",
            ],
            "conclusion": f"{pct}% Trimmed Mean dari data adalah {tm_val:,.4f}",
        }

    @staticmethod
    def calculate_geometric_mean(data: Union[pd.Series, List[float]]) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        pos_arr = arr[arr > 0]
        if len(pos_arr) == 0:
            gm_val = 0.0
        else:
            gm_val = float(stats.gmean(pos_arr))
        return {
            "value": round(gm_val, 4),
            "excel_formula": "=GEOMEAN(range)",
            "spss_menu": "Transform > Compute Variable > EXP(MEAN(LN(var)))",
            "spss_syntax": "COMPUTE gmean = EXP(MEAN(LN(var))).",
            "formula_tex": r"G = \left(\prod_{i=1}^n X_i\right)^{\frac{1}{n}} = \exp\left(\frac{1}{n} \sum \ln X_i\right)",
            "steps": [
                "Hitung logaritma natural (ln) untuk setiap observasi bernilai positif",
                f"Cari rata-rata logaritma, lalu pangkatkan kembali dengan fungsi eksponensial (e^x): {gm_val:,.4f}",
            ],
            "conclusion": f"Geometric Mean (Rata-rata Geometrik) adalah {gm_val:,.4f}",
        }

    @staticmethod
    def calculate_harmonic_mean(data: Union[pd.Series, List[float]]) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        pos_arr = arr[arr > 0]
        hm_val = float(stats.hmean(pos_arr)) if len(pos_arr) > 0 else 0.0
        return {
            "value": round(hm_val, 4),
            "excel_formula": "=HARMEAN(range)",
            "spss_menu": "Transform > Compute Variable > 1 / MEAN(1/var)",
            "spss_syntax": "COMPUTE hmean = 1 / MEAN(1/var).",
            "formula_tex": r"H = \frac{n}{\sum_{i=1}^n \frac{1}{X_i}}",
            "steps": [
                "Ambil resiprokal (1/X) dari setiap nilai data",
                f"Bagi jumlah observasi (n = {len(pos_arr)}) dengan total resiprokal: {hm_val:,.4f}",
            ],
            "conclusion": f"Harmonic Mean (Rata-rata Harmonik) adalah {hm_val:,.4f}",
        }

    @staticmethod
    def calculate_weighted_mean(
        values: Union[pd.Series, List[float]], weights: Union[pd.Series, List[float]]
    ) -> Dict[str, Any]:
        v = np.array(values, dtype=float)
        w = np.array(weights, dtype=float)
        valid = (~np.isnan(v)) & (~np.isnan(w)) & (w > 0)
        v = v[valid]
        w = w[valid]
        sum_vw = float(np.sum(v * w))
        sum_w = float(np.sum(w))
        wm_val = sum_vw / sum_w if sum_w > 0 else 0.0
        return {
            "value": round(wm_val, 4),
            "sum_weights": round(sum_w, 4),
            "sum_product": round(sum_vw, 4),
            "excel_formula": "=SUMPRODUCT(values_range, weights_range) / SUM(weights_range)",
            "spss_menu": "Data > Weight Cases... (By weights_var), lalu Analyze > Descriptive Statistics > Descriptives",
            "spss_syntax": "WEIGHT BY weight_var.\nDESCRIPTIVES VARIABLES=val_var /STATISTICS=MEAN.",
            "formula_tex": r"\bar{X}_w = \frac{\sum_{i=1}^n (w_i \cdot X_i)}{\sum_{i=1}^n w_i}",
            "steps": [
                f"Hitung total perkalian nilai dan bobot: SUMPRODUCT = {sum_vw:,.2f}",
                f"Hitung total bobot: SUM(w) = {sum_w:,.2f}",
                f"Bagi hasil perkalian dengan total bobot: {sum_vw:,.2f} / {sum_w:,.2f} = {wm_val:,.4f}",
            ],
            "conclusion": f"Rata-rata Tertimbang (Weighted Mean) adalah {wm_val:,.4f}",
        }

    # =========================================================================
    # CATEGORY 2: UKURAN DISPERSI, POSISI & BENTUK (Soal 11 - 20)
    # =========================================================================

    @staticmethod
    def calculate_dispersion_all(data: Union[pd.Series, List[float]]) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        n = len(arr)
        min_v = float(np.min(arr))
        max_v = float(np.max(arr))
        range_v = max_v - min_v
        var_s = float(np.var(arr, ddof=1)) if n > 1 else 0.0
        var_p = float(np.var(arr, ddof=0))
        std_s = float(np.std(arr, ddof=1)) if n > 1 else 0.0
        std_p = float(np.std(arr, ddof=0))
        mean_v = float(np.mean(arr))
        cv = (std_s / mean_v * 100.0) if mean_v != 0 else 0.0
        q1 = float(np.percentile(arr, 25))
        q2 = float(np.percentile(arr, 50))
        q3 = float(np.percentile(arr, 75))
        iqr = q3 - q1
        skew = float(stats.skew(arr, bias=False)) if n > 2 else 0.0
        kurt = float(stats.kurtosis(arr, bias=False)) if n > 3 else 0.0
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        outliers = arr[(arr < lower_fence) | (arr > upper_fence)].tolist()

        return {
            "n": n,
            "min": round(min_v, 4),
            "max": round(max_v, 4),
            "range": round(range_v, 4),
            "variance_sample": round(var_s, 4),
            "variance_pop": round(var_p, 4),
            "std_sample": round(std_s, 4),
            "std_pop": round(std_p, 4),
            "coef_variation_pct": round(cv, 4),
            "q1": round(q1, 4),
            "median": round(q2, 4),
            "q3": round(q3, 4),
            "iqr": round(iqr, 4),
            "skewness": round(skew, 4),
            "kurtosis_excess": round(kurt, 4),
            "lower_fence": round(lower_fence, 4),
            "upper_fence": round(upper_fence, 4),
            "outliers_count": len(outliers),
            "outliers": [round(x, 4) for x in outliers],
            "excel_formulas": {
                "range": "=MAX(range) - MIN(range)",
                "variance_sample": "=VAR.S(range)",
                "std_sample": "=STDEV.S(range)",
                "q1": "=QUARTILE.EXC(range, 1) atau =QUARTILE.INC(range, 1)",
                "q3": "=QUARTILE.INC(range, 3)",
                "iqr": "=QUARTILE.INC(range, 3) - QUARTILE.INC(range, 1)",
                "skewness": "=SKEW(range)",
                "kurtosis": "=KURT(range)",
            },
            "spss_menu": "Analyze > Descriptive Statistics > Explore...",
            "spss_syntax": "EXAMINE VARIABLES=var /STATISTICS DESCRIPTIVES /PLOT BOXPLOT.",
        }

    # =========================================================================
    # CATEGORY 3: UJI HIPOTESIS 1 & 2 SAMPEL (PARAMETRIK) (Soal 21 - 30)
    # =========================================================================

    @staticmethod
    def one_sample_ttest(
        data: Union[pd.Series, List[float]],
        mu0: float,
        alpha: float = 0.05,
        alternative: str = "two-sided",
    ) -> Dict[str, Any]:
        arr = StatisticalSolver._clean_series(data)
        n = len(arr)
        mean_v = float(np.mean(arr))
        std_v = float(np.std(arr, ddof=1))
        se = std_v / np.sqrt(n)
        t_stat = (mean_v - mu0) / se if se > 0 else 0.0
        df = n - 1

        if alternative == "two-sided":
            p_val = float(2 * (1 - stats.t.cdf(np.abs(t_stat), df)))
            t_crit = float(stats.t.ppf(1 - alpha / 2, df))
            reject = p_val < alpha
        elif alternative == "greater":
            p_val = float(1 - stats.t.cdf(t_stat, df))
            t_crit = float(stats.t.ppf(1 - alpha, df))
            reject = p_val < alpha and t_stat > 0
        else:  # less
            p_val = float(stats.t.cdf(t_stat, df))
            t_crit = float(-stats.t.ppf(1 - alpha, df))
            reject = p_val < alpha and t_stat < 0

        ci_low = mean_v - stats.t.ppf(1 - alpha / 2, df) * se
        ci_high = mean_v + stats.t.ppf(1 - alpha / 2, df) * se

        return {
            "mean": round(mean_v, 4),
            "std": round(std_v, 4),
            "n": n,
            "mu0": mu0,
            "df": df,
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_val, 4),
            "alpha": alpha,
            "t_critical": round(t_crit, 4),
            "ci_95": [round(ci_low, 4), round(ci_high, 4)],
            "reject_null": reject,
            "decision": "Tolak H0" if reject else "Gagal Tolak H0 (Terima H0)",
            "excel_formula": f"=T.TEST(range, {mu0}, 2, 1) atau hitung manual t = (AVERAGE(range) - {mu0}) / (STDEV.S(range)/SQRT(COUNT(range)))",
            "spss_menu": f"Analyze > Compare Means > One-Sample T Test... (Masukkan Test Value: {mu0})",
            "spss_syntax": f"T-TEST /TESTVAL={mu0} /VARIABLES=var /CRITERIA=CI({(1-alpha)*100}).",
            "steps": [
                f"Rata-rata sampel = {mean_v:,.4f}, Std Dev = {std_v:,.4f}, n = {n}",
                f"Standard Error (SE) = {std_v:,.4f} / sqrt({n}) = {se:,.4f}",
                f"t-hitung = ({mean_v:,.4f} - {mu0}) / {se:,.4f} = {t_stat:,.4f}",
                f"Derajat Bebas (df) = {df}, Nilai p (Sig. 2-tailed) = {p_val:,.4f}",
                f"Karena p-value ({p_val:,.4f}) {'<' if reject else '>='} alpha ({alpha}), maka {'Tolak H0' if reject else 'Gagal Tolak H0'}.",
            ],
            "conclusion": (
                f"Secara signifikan (alpha = {alpha}) rata-rata populasi berbeda dari {mu0}"
                if reject
                else f"Tidak cukup bukti empiris untuk menyatakan rata-rata populasi berbeda dari {mu0}"
            ),
        }

    @staticmethod
    def independent_ttest(
        group1: Union[pd.Series, List[float]],
        group2: Union[pd.Series, List[float]],
        alpha: float = 0.05,
        equal_var: bool = True,
    ) -> Dict[str, Any]:
        g1 = StatisticalSolver._clean_series(group1)
        g2 = StatisticalSolver._clean_series(group2)
        n1, n2 = len(g1), len(g2)
        m1, m2 = float(np.mean(g1)), float(np.mean(g2))
        s1, s2 = float(np.std(g1, ddof=1)), float(np.std(g2, ddof=1))

        # Levene's test for equality of variances
        lev_stat, lev_p = stats.levene(g1, g2)

        # t-test
        t_res = stats.ttest_ind(g1, g2, equal_var=equal_var)
        t_stat = float(t_res.statistic)
        p_val = float(t_res.pvalue)
        df = float(t_res.df) if hasattr(t_res, "df") else (n1 + n2 - 2 if equal_var else 0.0)

        reject = p_val < alpha

        return {
            "mean_g1": round(m1, 4),
            "mean_g2": round(m2, 4),
            "std_g1": round(s1, 4),
            "std_g2": round(s2, 4),
            "n_g1": n1,
            "n_g2": n2,
            "mean_diff": round(m1 - m2, 4),
            "levene_stat": round(float(lev_stat), 4),
            "levene_p": round(float(lev_p), 4),
            "equal_variance_assumed": equal_var,
            "df": round(df, 2),
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_val, 4),
            "reject_null": reject,
            "decision": "Tolak H0 (Ada perbedaan signifikan)" if reject else "Gagal Tolak H0 (Tidak ada perbedaan signifikan)",
            "excel_formula": "=T.TEST(range_g1, range_g2, 2, 2)  [Type 2: Two-sample equal variance]",
            "spss_menu": "Analyze > Compare Means > Independent-Samples T Test... (Pilih Test Variable dan Grouping Variable)",
            "spss_syntax": "T-TEST GROUPS=group_var(1 2) /VARIABLES=test_var.",
            "steps": [
                f"Kelompok 1: Mean = {m1:,.4f}, SD = {s1:,.4f}, n = {n1}",
                f"Kelompok 2: Mean = {m2:,.4f}, SD = {s2:,.4f}, n = {n2}",
                f"Selisih rata-rata (Mean Difference) = {m1 - m2:,.4f}",
                f"Uji Levene Homogenitas: F = {lev_stat:,.4f}, Sig = {lev_p:,.4f}",
                f"Nilai t-hitung = {t_stat:,.4f}, df = {df:.2f}, Sig. (2-tailed) = {p_val:,.4f}",
            ],
            "conclusion": (
                f"Terdapat perbedaan rata-rata yang signifikan secara statistik antara kedua kelompok (t = {t_stat:,.4f}, p = {p_val:,.4f} < {alpha})."
                if reject
                else f"Tidak terdapat perbedaan rata-rata yang signifikan antara kedua kelompok (t = {t_stat:,.4f}, p = {p_val:,.4f} >= {alpha})."
            ),
        }

    @staticmethod
    def paired_ttest(
        pre: Union[pd.Series, List[float]],
        post: Union[pd.Series, List[float]],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        p1 = np.array(pre, dtype=float)
        p2 = np.array(post, dtype=float)
        valid = (~np.isnan(p1)) & (~np.isnan(p2))
        p1 = p1[valid]
        p2 = p2[valid]
        n = len(p1)
        diff = p2 - p1
        m_diff = float(np.mean(diff))
        s_diff = float(np.std(diff, ddof=1))
        se_diff = s_diff / np.sqrt(n) if n > 0 else 0.0
        t_stat = m_diff / se_diff if se_diff > 0 else 0.0
        df = n - 1
        p_val = float(2 * (1 - stats.t.cdf(np.abs(t_stat), df)))
        reject = p_val < alpha

        return {
            "n": n,
            "mean_pre": round(float(np.mean(p1)), 4),
            "mean_post": round(float(np.mean(p2)), 4),
            "mean_difference": round(m_diff, 4),
            "std_difference": round(s_diff, 4),
            "se_difference": round(se_diff, 4),
            "df": df,
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_val, 4),
            "reject_null": reject,
            "decision": "Tolak H0 (Terdapat perubahan signifikan)" if reject else "Gagal Tolak H0 (Tidak terdapat perubahan signifikan)",
            "excel_formula": "=T.TEST(range_pre, range_post, 2, 1)  [Type 1: Paired]",
            "spss_menu": "Analyze > Compare Means > Paired-Samples T Test... (Pilih Variable 1 dan Variable 2)",
            "spss_syntax": "T-TEST PAIRS=pre WITH post (PAIRED).",
            "steps": [
                f"Hitung selisih tiap pasangan data (d = Post - Pre)",
                f"Rata-rata selisih (d_bar) = {m_diff:,.4f}, SD selisih = {s_diff:,.4f}, n = {n}",
                f"SE selisih = {se_diff:,.4f}, t-hitung = {m_diff:,.4f} / {se_diff:,.4f} = {t_stat:,.4f}",
                f"Nilai p-value (Sig 2-tailed) = {p_val:,.4f} dengan df = {df}",
            ],
            "conclusion": (
                f"Terdapat perbedaan yang signifikan antara kondisi Sebelum (Pre) dan Sesudah (Post) dengan p = {p_val:,.4f} < {alpha}."
                if reject
                else f"Tidak terdapat perbedaan signifikan antara kondisi Sebelum dan Sesudah (p = {p_val:,.4f} >= {alpha})."
            ),
        }

    # =========================================================================
    # CATEGORY 4: ANALISIS VARIANS / ANOVA (Soal 31 - 40)
    # =========================================================================

    @staticmethod
    def one_way_anova(groups: List[Union[pd.Series, List[float]]], group_names: Optional[List[str]] = None, alpha: float = 0.05) -> Dict[str, Any]:
        cleaned_groups = [StatisticalSolver._clean_series(g) for g in groups]
        k = len(cleaned_groups)
        ns = [len(g) for g in cleaned_groups]
        total_n = sum(ns)
        means = [float(np.mean(g)) for g in cleaned_groups]
        grand_mean = float(np.mean(np.concatenate(cleaned_groups)))

        # Sum of squares
        ss_between = float(sum(ns[i] * ((means[i] - grand_mean) ** 2) for i in range(k)))
        ss_within = float(sum(sum((x - means[i]) ** 2 for x in cleaned_groups[i]) for i in range(k)))
        ss_total = ss_between + ss_within

        df_between = k - 1
        df_within = total_n - k
        df_total = total_n - 1

        ms_between = ss_between / df_between if df_between > 0 else 0.0
        ms_within = ss_within / df_within if df_within > 0 else 0.0

        f_stat = ms_between / ms_within if ms_within > 0 else 0.0
        p_val = float(1 - stats.f.cdf(f_stat, df_between, df_within))
        reject = p_val < alpha

        # Eta-squared (effect size)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0.0

        if group_names is None:
            group_names = [f"Grup {i+1}" for i in range(k)]

        group_stats = [
            {"group": group_names[i], "n": ns[i], "mean": round(means[i], 4), "std": round(float(np.std(cleaned_groups[i], ddof=1)), 4)}
            for i in range(k)
        ]

        return {
            "k_groups": k,
            "total_n": total_n,
            "grand_mean": round(grand_mean, 4),
            "group_stats": group_stats,
            "ss_between": round(ss_between, 4),
            "ss_within": round(ss_within, 4),
            "ss_total": round(ss_total, 4),
            "df_between": df_between,
            "df_within": df_within,
            "df_total": df_total,
            "ms_between": round(ms_between, 4),
            "ms_within": round(ms_within, 4),
            "f_statistic": round(f_stat, 4),
            "p_value": round(p_val, 4),
            "eta_squared": round(eta_squared, 4),
            "reject_null": reject,
            "decision": "Tolak H0 (Minimal ada 1 kelompok berbeda nyata)" if reject else "Gagal Tolak H0 (Tidak ada perbedaan signifikan)",
            "excel_formula": "Data > Data Analysis > Anova: Single Factor",
            "spss_menu": "Analyze > Compare Means > One-Way ANOVA... (Pilih Post Hoc Tukey jika diperlukan)",
            "spss_syntax": "ONEWAY test_var BY group_var /STATISTICS DESCRIPTIVES HOMOGENEITY /POSTHOC=TUKEY ALPHA(0.05).",
            "steps": [
                f"Hitung SS Between = {ss_between:,.4f} (df = {df_between}), MS Between = {ms_between:,.4f}",
                f"Hitung SS Within = {ss_within:,.4f} (df = {df_within}), MS Within = {ms_within:,.4f}",
                f"F-hitung = MS Between / MS Within = {f_stat:,.4f}",
                f"p-value (Sig) = {p_val:,.4f} terhadap alpha = {alpha}",
            ],
            "conclusion": (
                f"Terdapat perbedaan rata-rata yang signifikan antar kelompok (F({df_between}, {df_within}) = {f_stat:,.4f}, p = {p_val:,.4f} < {alpha})."
                if reject
                else f"Tidak terdapat perbedaan rata-rata yang signifikan antar kelompok (F({df_between}, {df_within}) = {f_stat:,.4f}, p = {p_val:,.4f} >= {alpha})."
            ),
        }

    # =========================================================================
    # CATEGORY 5: KORELASI & KOVARIANS (Soal 41 - 50)
    # =========================================================================

    @staticmethod
    def calculate_correlation(
        x: Union[pd.Series, List[float]],
        y: Union[pd.Series, List[float]],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        vx = np.array(x, dtype=float)
        vy = np.array(y, dtype=float)
        valid = (~np.isnan(vx)) & (~np.isnan(vy))
        vx = vx[valid]
        vy = vy[valid]
        n = len(vx)

        # Pearson
        r_pearson, p_pearson = stats.pearsonr(vx, vy)
        r2 = float(r_pearson**2)

        # Spearman
        r_spearman, p_spearman = stats.spearmanr(vx, vy)

        # Kendall Tau
        tau_val, p_tau = stats.kendalltau(vx, vy)

        # Covariance
        cov_matrix = np.cov(vx, vy)
        cov_val = float(cov_matrix[0, 1])

        # t-statistic for Pearson
        t_stat = float(r_pearson * np.sqrt((n - 2) / (1 - r2))) if (1 - r2) > 0 else 0.0

        strength = ""
        abs_r = abs(r_pearson)
        if abs_r < 0.2:
            strength = "Sangat Lemah"
        elif abs_r < 0.4:
            strength = "Lemah"
        elif abs_r < 0.6:
            strength = "Sedang"
        elif abs_r < 0.8:
            strength = "Kuat"
        else:
            strength = "Sangat Kuat"

        direction = "Positif" if r_pearson > 0 else ("Negatif" if r_pearson < 0 else "Nol")

        return {
            "n": n,
            "pearson_r": round(float(r_pearson), 4),
            "pearson_p": round(float(p_pearson), 4),
            "r_squared": round(r2, 4),
            "t_statistic": round(t_stat, 4),
            "spearman_rho": round(float(r_spearman), 4),
            "spearman_p": round(float(p_spearman), 4),
            "kendall_tau": round(float(tau_val), 4),
            "kendall_p": round(float(p_tau), 4),
            "sample_covariance": round(cov_val, 4),
            "relationship_interpretation": f"Hubungan {direction} yang {strength}",
            "significant": p_pearson < alpha,
            "excel_formulas": {
                "pearson": "=CORREL(array1, array2)",
                "covariance": "=COVARIANCE.S(array1, array2)",
                "r_squared": "=RSQ(array1, array2)",
            },
            "spss_menu": "Analyze > Correlate > Bivariate... (Centang Pearson dan Spearman)",
            "spss_syntax": "CORRELATIONS /VARIABLES=var1 var2 /PRINT=TWOTAIL NOSIG.\nNONPAR CORR /VARIABLES=var1 var2 /PRINT=SPEARMAN TWOTAIL NOSIG.",
            "steps": [
                f"Kovarians Sampel Cov(X,Y) = {cov_val:,.4f}",
                f"Koefisien Korelasi Pearson r = {r_pearson:,.4f}",
                f"Koefisien Determinasi R^2 = {r2*100:,.2f}%",
                f"Uji signifikansi korelasi t = {t_stat:,.4f}, p-value = {p_pearson:,.4f}",
            ],
            "conclusion": f"Korelasi Pearson bernilai r = {r_pearson:,.4f} ({strength} {direction}) dan {'signifikan' if p_pearson < alpha else 'tidak signifikan'} pada taraf alpha = {alpha}.",
        }

    # =========================================================================
    # CATEGORY 6: UJI CHI-SQUARE & ASOSIASI KATEGORIK (Soal 51 - 60)
    # =========================================================================

    @staticmethod
    def chi_square_independence(
        contingency_table: Union[pd.DataFrame, np.ndarray, List[List[int]]],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        table = np.array(contingency_table, dtype=float)
        chi2, p_val, dof, expected = stats.chi2_contingency(table)
        n = np.sum(table)
        r, c = table.shape
        min_dim = min(r - 1, c - 1)

        # Cramer's V
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0.0

        # Contingency Coefficient
        c_coef = np.sqrt(chi2 / (chi2 + n)) if (chi2 + n) > 0 else 0.0

        # Odds Ratio if 2x2
        odds_ratio = None
        if table.shape == (2, 2):
            if table[0, 1] * table[1, 0] != 0:
                odds_ratio = float((table[0, 0] * table[1, 1]) / (table[0, 1] * table[1, 0]))

        reject = p_val < alpha

        return {
            "chi2_statistic": round(float(chi2), 4),
            "p_value": round(float(p_val), 4),
            "df": int(dof),
            "total_observations": int(n),
            "cramers_v": round(float(cramers_v), 4),
            "contingency_coefficient": round(float(c_coef), 4),
            "odds_ratio": round(odds_ratio, 4) if odds_ratio is not None else None,
            "expected_frequencies": np.round(expected, 2).tolist(),
            "observed_frequencies": table.astype(int).tolist(),
            "reject_null": reject,
            "decision": "Tolak H0 (Ada hubungan/asosiasi yang signifikan)" if reject else "Gagal Tolak H0 (Kedua variabel independen)",
            "excel_formula": "=CHISQ.TEST(actual_range, expected_range)",
            "spss_menu": "Analyze > Descriptive Statistics > Crosstabs... (Pilih Statistics > Chi-Square, Phi and Cramer's V)",
            "spss_syntax": "CROSSTABS /TABLES=row_var BY col_var /STATISTICS=CHISQ PHI CC /CELLS=COUNT EXPECTED.",
            "steps": [
                f"Hitung tabel frekuensi harapan E_ij = (Row Total * Col Total) / Grand Total",
                f"Hitung statistik Chi-Square: chi^2 = sum((O - E)^2 / E) = {chi2:,.4f}",
                f"Derajat bebas df = ({r}-1)*({c}-1) = {dof}",
                f"Nilai p-value (Asymp. Sig) = {p_val:,.4f} terhadap alpha = {alpha}",
                f"Cramer's V = {cramers_v:,.4f}",
            ],
            "conclusion": (
                f"Terdapat asosiasi/hubungan yang signifikan antara kedua variabel kategorik (chi^2({dof}) = {chi2:,.4f}, p = {p_val:,.4f} < {alpha})."
                if reject
                else f"Tidak terdapat hubungan signifikan / kedua variabel bersifat independen (chi^2({dof}) = {chi2:,.4f}, p = {p_val:,.4f} >= {alpha})."
            ),
        }

    # =========================================================================
    # CATEGORY 7: ANALISIS REGRESI LINEAR (Soal 61 - 70)
    # =========================================================================

    @staticmethod
    def linear_regression(
        x: Union[pd.DataFrame, pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        feature_names: Optional[List[str]] = None,
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        vy = np.array(y, dtype=float)
        if isinstance(x, (pd.Series, list)) or (isinstance(x, np.ndarray) and x.ndim == 1):
            vx = np.array(x, dtype=float).reshape(-1, 1)
            f_names = feature_names if feature_names else ["X"]
        elif isinstance(x, pd.DataFrame):
            f_names = list(x.columns)
            vx = x.values
        else:
            vx = np.array(x, dtype=float)
            f_names = feature_names if feature_names else [f"X{i+1}" for i in range(vx.shape[1])]

        # Filter NaNs
        valid = ~np.isnan(vy)
        for j in range(vx.shape[1]):
            valid = valid & (~np.isnan(vx[:, j]))

        vy = vy[valid]
        vx = vx[valid]
        n = len(vy)
        p = vx.shape[1]

        # Add constant
        x_with_const = sm.add_constant(vx)
        model = sm.OLS(vy, x_with_const).fit()

        coefs = model.params.tolist()
        se_coefs = model.bse.tolist()
        t_stats = model.tvalues.tolist()
        p_vals = model.pvalues.tolist()

        intercept = float(coefs[0])
        slopes = [float(c) for c in coefs[1:]]

        r2 = float(model.rsquared)
        adj_r2 = float(model.rsquared_adj)
        f_stat = float(model.fvalue)
        f_pval = float(model.f_pvalue)
        mse_resid = float(model.mse_resid)
        std_err_est = float(np.sqrt(mse_resid))

        # Equation string
        terms = [f"{intercept:.4f}"]
        for name, slope in zip(f_names, slopes):
            sign = "+" if slope >= 0 else "-"
            terms.append(f"{sign} {abs(slope):.4f}*{name}")
        eq_str = "Y = " + " ".join(terms)

        coef_table = []
        coef_table.append({
            "variable": "Constant (Intercept)",
            "coefficient": round(intercept, 4),
            "std_error": round(float(se_coefs[0]), 4),
            "t_statistic": round(float(t_stats[0]), 4),
            "p_value": round(float(p_vals[0]), 4),
            "significant": p_vals[0] < alpha,
        })
        for i, name in enumerate(f_names):
            coef_table.append({
                "variable": name,
                "coefficient": round(slopes[i], 4),
                "std_error": round(float(se_coefs[i + 1]), 4),
                "t_statistic": round(float(t_stats[i + 1]), 4),
                "p_value": round(float(p_vals[i + 1]), 4),
                "significant": p_vals[i + 1] < alpha,
            })

        return {
            "n": n,
            "num_predictors": p,
            "features": f_names,
            "equation": eq_str,
            "intercept": round(intercept, 4),
            "slopes": [round(s, 4) for s in slopes],
            "r_squared": round(r2, 4),
            "adj_r_squared": round(adj_r2, 4),
            "f_statistic": round(f_stat, 4),
            "f_p_value": round(f_pval, 4),
            "std_error_estimate": round(std_err_est, 4),
            "coefficients_table": coef_table,
            "model_significant": f_pval < alpha,
            "excel_formulas": {
                "slope": "=SLOPE(known_y's, known_x's)",
                "intercept": "=INTERCEPT(known_y's, known_x's)",
                "r_squared": "=RSQ(known_y's, known_x's)",
                "linear_prediction": "=FORECAST.LINEAR(x, known_y's, known_x's)",
                "linest_array": "=LINEST(known_y's, known_x's, TRUE, TRUE)",
            },
            "spss_menu": "Analyze > Regression > Linear... (Masukkan Dependent & Independent variables)",
            "spss_syntax": f"REGRESSION /DEPENDENT=Y /METHOD=ENTER {' '.join(f_names)} /STATISTICS=COEFF OUTS R ANOVA.",
            "steps": [
                f"Persamaan Regresi: {eq_str}",
                f"Koefisien Determinasi R^2 = {r2*100:.2f}% (Kemampuan model menjelaskan variasi Y)",
                f"Uji F Simultan: F = {f_stat:.4f}, Sig = {f_pval:.4f} ({'Model Signifikan' if f_pval < alpha else 'Model Tidak Signifikan'})",
                f"Standard Error of the Estimate = {std_err_est:.4f}",
            ],
            "conclusion": f"Model regresi {eq_str} memiliki R^2 = {r2*100:.2f}% dan secara simultan {'berpengaruh signifikan' if f_pval < alpha else 'tidak signifikan'} terhadap Y.",
        }

    # =========================================================================
    # CATEGORY 8: UJI ASUMSI KLASIK & DIAGNOSTIK (Soal 71 - 80)
    # =========================================================================

    @staticmethod
    def classical_assumptions_diagnostics(
        x: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        feature_names: Optional[List[str]] = None,
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        vy = np.array(y, dtype=float)
        if isinstance(x, pd.DataFrame):
            f_names = list(x.columns)
            vx = x.values
        else:
            vx = np.array(x, dtype=float)
            if vx.ndim == 1:
                vx = vx.reshape(-1, 1)
            f_names = feature_names if feature_names else [f"X{i+1}" for i in range(vx.shape[1])]

        x_const = sm.add_constant(vx)
        model = sm.OLS(vy, x_const).fit()
        residuals = model.resid

        # 1. Normality of residuals (Kolmogorov-Smirnov & Shapiro-Wilk)
        std_r = np.std(residuals, ddof=1) if len(residuals) > 1 else 0.0
        if std_r > 0:
            std_resid = (residuals - np.mean(residuals)) / std_r
            ks_stat, ks_pval = stats.kstest(std_resid, "norm")
        else:
            ks_stat, ks_pval = 0.0, 1.0

        if len(residuals) >= 3 and std_r > 0 and len(residuals) <= 5000:
            try:
                shapiro_stat, shapiro_pval = stats.shapiro(residuals)
            except Exception:
                shapiro_stat, shapiro_pval = 1.0, 1.0
        else:
            shapiro_stat, shapiro_pval = 1.0, 1.0

        # 2. Autocorrelation (Durbin-Watson)
        try:
            dw_stat = float(durbin_watson(residuals))
            if np.isnan(dw_stat):
                dw_stat = 2.0
        except Exception:
            dw_stat = 2.0

        # 3. Heteroskedasticity (Breusch-Pagan)
        try:
            bp_test = het_breuschpagan(residuals, x_const)
            bp_stat, bp_pval = float(bp_test[0]), float(bp_test[1])
        except Exception:
            bp_stat, bp_pval = 0.0, 1.0

        # 4. Multicollinearity (VIF)
        vif_data = []
        if vx.shape[1] > 1:
            for i in range(vx.shape[1]):
                try:
                    vif_val = float(variance_inflation_factor(vx, i))
                    vif_data.append({
                        "variable": f_names[i],
                        "vif": round(vif_val, 4),
                        "tolerance": round(1.0 / vif_val, 4) if vif_val > 0 else 0.0,
                        "multicollinearity_detected": vif_val > 10.0,
                    })
                except Exception:
                    pass

        return {
            "normality": {
                "kolmogorov_smirnov": {"stat": round(float(ks_stat), 4), "p_value": round(float(ks_pval), 4), "is_normal": ks_pval >= alpha},
                "shapiro_wilk": {"stat": round(float(shapiro_stat), 4), "p_value": round(float(shapiro_pval), 4), "is_normal": shapiro_pval >= alpha},
            },
            "autocorrelation": {
                "durbin_watson": round(dw_stat, 4),
                "interpretation": "Tidak ada autokorelasi" if 1.5 <= dw_stat <= 2.5 else ("Korelasi positif" if dw_stat < 1.5 else "Korelasi negatif"),
            },
            "heteroskedasticity": {
                "breusch_pagan_lm": round(bp_stat, 4),
                "p_value": round(bp_pval, 4),
                "is_homoskedastic": bp_pval >= alpha,
            },
            "multicollinearity": vif_data,
            "excel_formula": "Uji residual: =NORM.DIST() atau analisis scatter residual vs predicted",
            "spss_menu": "Analyze > Regression > Linear... (Pilih Statistics > Collinearity diagnostics, Durbin-Watson; Plots > Histogram & Normal probability plot)",
            "spss_syntax": "REGRESSION /DEPENDENT=Y /METHOD=ENTER X1 X2 /STATISTICS=COLLIN DURBIN RESID /RESIDUALS=HISTOGRAM(ZRESID) NORMPROB(ZRESID).",
        }

    # =========================================================================
    # CATEGORY 9: STATISTIKA NON-PARAMETRIK (Soal 81 - 90)
    # =========================================================================

    @staticmethod
    def mann_whitney_u_test(
        g1: Union[pd.Series, List[float]],
        g2: Union[pd.Series, List[float]],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        arr1 = StatisticalSolver._clean_series(g1)
        arr2 = StatisticalSolver._clean_series(g2)
        n1, n2 = len(arr1), len(arr2)

        res = stats.mannwhitneyu(arr1, arr2, alternative="two-sided")
        u_stat = float(res.statistic)
        p_val = float(res.pvalue)

        # Calculate Z approximation for large samples
        mean_u = (n1 * n2) / 2.0
        sigma_u = np.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12.0)
        z_val = (u_stat - mean_u) / sigma_u if sigma_u > 0 else 0.0

        reject = p_val < alpha

        return {
            "n1": n1,
            "n2": n2,
            "median_g1": round(float(np.median(arr1)), 4),
            "median_g2": round(float(np.median(arr2)), 4),
            "u_statistic": round(u_stat, 4),
            "z_value": round(float(z_val), 4),
            "p_value": round(p_val, 4),
            "reject_null": reject,
            "decision": "Tolak H0 (Ada perbedaan peringkat/distribusi signifikan)" if reject else "Gagal Tolak H0 (Distribusi kedua grup identik)",
            "excel_formula": "Beri RANK.AVG pada data gabungan, lalu hitung U = R1 - (n1*(n1+1))/2",
            "spss_menu": "Analyze > Nonparametric Tests > Legacy Dialogs > 2 Independent Samples... (Pilih Mann-Whitney U)",
            "spss_syntax": "NPAR TESTS /M-W=test_var BY group_var(1 2).",
            "steps": [
                f"Kelompok 1 (n1 = {n1}, Median = {np.median(arr1):,.2f}) vs Kelompok 2 (n2 = {n2}, Median = {np.median(arr2):,.2f})",
                f"Statistik Mann-Whitney U = {u_stat:,.4f}",
                f"Nilai pendekatan Z = {z_val:,.4f}",
                f"Asymp. Sig. (2-tailed) = {p_val:,.4f}",
            ],
            "conclusion": (
                f"Terdapat perbedaan distribusi/median yang signifikan secara statistik antara kedua kelompok (U = {u_stat:,.4f}, p = {p_val:,.4f} < {alpha})."
                if reject
                else f"Tidak terdapat perbedaan signifikan antara kedua kelompok (U = {u_stat:,.4f}, p = {p_val:,.4f} >= {alpha})."
            ),
        }

    @staticmethod
    def wilcoxon_signed_rank_test(
        pre: Union[pd.Series, List[float]],
        post: Union[pd.Series, List[float]],
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        p1 = np.array(pre, dtype=float)
        p2 = np.array(post, dtype=float)
        valid = (~np.isnan(p1)) & (~np.isnan(p2))
        p1 = p1[valid]
        p2 = p2[valid]
        diff = p2 - p1
        non_zero_diff = diff[diff != 0]

        res = stats.wilcoxon(p1, p2, alternative="two-sided")
        w_stat = float(res.statistic)
        p_val = float(res.pvalue)
        reject = p_val < alpha

        return {
            "n_pairs": len(p1),
            "n_non_zero_diff": len(non_zero_diff),
            "wilcoxon_w": round(w_stat, 4),
            "p_value": round(p_val, 4),
            "reject_null": reject,
            "decision": "Tolak H0 (Ada perbedaan signifikan sebelum vs sesudah)" if reject else "Gagal Tolak H0 (Tidak ada perbedaan signifikan)",
            "excel_formula": "Beri peringkat selisih absolut |d_i|, jumlahkan rank positif (W+) dan rank negatif (W-)",
            "spss_menu": "Analyze > Nonparametric Tests > Legacy Dialogs > 2 Related Samples... (Pilih Wilcoxon)",
            "spss_syntax": "NPAR TESTS /WILCOXON=pre WITH post (PAIRED).",
            "steps": [
                f"Hitung selisih tiap pasangan (d = Post - Pre)",
                f"Beri peringkat berdasarkan nilai mutlak selisih non-nol",
                f"Statistik Wilcoxon W = {w_stat:,.4f}, Sig. (2-tailed) = {p_val:,.4f}",
            ],
            "conclusion": (
                f"Terdapat perbedaan signifikan antara sebelum dan sesudah intervensi (W = {w_stat:,.4f}, p = {p_val:,.4f} < {alpha})."
                if reject
                else f"Tidak terdapat perbedaan signifikan antara sebelum dan sesudah intervensi (W = {w_stat:,.4f}, p = {p_val:,.4f} >= {alpha})."
            ),
        }

    @staticmethod
    def kruskal_wallis_test(
        groups: List[Union[pd.Series, List[float]]],
        group_names: Optional[List[str]] = None,
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        cleaned_groups = [StatisticalSolver._clean_series(g) for g in groups]
        k = len(cleaned_groups)
        h_stat, p_val = stats.kruskal(*cleaned_groups)
        reject = p_val < alpha

        medians = [round(float(np.median(g)), 4) for g in cleaned_groups]

        return {
            "k_groups": k,
            "group_medians": medians,
            "h_statistic": round(float(h_stat), 4),
            "df": k - 1,
            "p_value": round(float(p_val), 4),
            "reject_null": reject,
            "decision": "Tolak H0 (Minimal ada 1 kelompok yang memiliki peringkat berbeda)" if reject else "Gagal Tolak H0",
            "excel_formula": "Beri peringkat seluruh data gabungan, lalu hitung H = [12/(N(N+1))] * sum(R_i^2/n_i) - 3(N+1)",
            "spss_menu": "Analyze > Nonparametric Tests > Legacy Dialogs > K Independent Samples... (Pilih Kruskal-Wallis H)",
            "spss_syntax": "NPAR TESTS /K-W=test_var BY group_var(1 k).",
            "steps": [
                f"Gabungkan seluruh sampel dan beri peringkat (Rank)",
                f"Hitung statistik Kruskal-Wallis H = {h_stat:,.4f} dengan df = {k-1}",
                f"Nilai Asymp. Sig. = {p_val:,.4f} terhadap alpha = {alpha}",
            ],
            "conclusion": (
                f"Terdapat perbedaan median/distribusi yang signifikan antar kelompok (H({k-1}) = {h_stat:,.4f}, p = {p_val:,.4f} < {alpha})."
                if reject
                else f"Tidak terdapat perbedaan signifikan antar kelompok (H({k-1}) = {h_stat:,.4f}, p = {p_val:,.4f} >= {alpha})."
            ),
        }

    # =========================================================================
    # CATEGORY 10: INDIKATOR BPS & SOSIAL EKONOMI KHUSUS (Soal 91 - 100)
    # =========================================================================

    @staticmethod
    def calculate_tpt_tpak(
        working_age_pop: int,
        employed: int,
        unemployed: int,
    ) -> Dict[str, Any]:
        """
        BPS Labor Force Indicators:
        - Angkatan Kerja (Labor Force) = Bekerja + Pengangguran
        - Bukan Angkatan Kerja (Not in Labor Force) = Usia Kerja - Angkatan Kerja
        - TPAK (Tingkat Partisipasi Angkatan Kerja) = (Angkatan Kerja / Usia Kerja) * 100%
        - TPT (Tingkat Pengangguran Terbuka) = (Pengangguran / Angkatan Kerja) * 100%
        """
        labor_force = employed + unemployed
        not_in_labor_force = working_age_pop - labor_force
        tpak = (labor_force / working_age_pop * 100.0) if working_age_pop > 0 else 0.0
        tpt = (unemployed / labor_force * 100.0) if labor_force > 0 else 0.0

        return {
            "working_age_population": working_age_pop,
            "labor_force": labor_force,
            "employed": employed,
            "unemployed": unemployed,
            "not_in_labor_force": not_in_labor_force,
            "tpak_percent": round(tpak, 2),
            "tpt_percent": round(tpt, 2),
            "excel_formula": "TPAK: =(employed + unemployed)/working_age * 100, TPT: =unemployed/(employed + unemployed) * 100",
            "spss_menu": "Transform > Compute Variable > TPAK = ((bekerja + pengangguran) / usia_kerja) * 100",
            "steps": [
                f"Angkatan Kerja = {employed:,} (Bekerja) + {unemployed:,} (Penganggur) = {labor_force:,} orang",
                f"TPAK = ({labor_force:,} / {working_age_pop:,}) * 100% = {tpak:.2f}%",
                f"TPT = ({unemployed:,} / {labor_force:,}) * 100% = {tpt:.2f}%",
            ],
            "conclusion": f"Tingkat Partisipasi Angkatan Kerja (TPAK) sebesar {tpak:.2f}% dan Tingkat Pengangguran Terbuka (TPT) sebesar {tpt:.2f}%.",
        }

    @staticmethod
    def calculate_fgt_poverty_indices(
        expenditures: Union[pd.Series, List[float]],
        poverty_line: float,
    ) -> Dict[str, Any]:
        """
        Foster-Greer-Thorbecke (FGT) Poverty Indices:
        P_alpha = (1/n) * sum( ((z - y_i) / z)^alpha ) for y_i < z
        alpha = 0 -> Headcount Index (P0, Persentase Penduduk Miskin)
        alpha = 1 -> Poverty Gap Index (P1, Indeks Kedalaman Kemiskinan)
        alpha = 2 -> Poverty Severity Index (P2, Indeks Keparahan Kemiskinan)
        """
        exp = StatisticalSolver._clean_series(expenditures)
        n = len(exp)
        poor = exp[exp < poverty_line]
        q = len(poor)

        p0 = (q / n * 100.0) if n > 0 else 0.0

        if q > 0 and poverty_line > 0:
            gaps = (poverty_line - poor) / poverty_line
            p1 = float((np.sum(gaps) / n) * 100.0)
            p2 = float((np.sum(gaps**2) / n) * 100.0)
        else:
            p1 = 0.0
            p2 = 0.0

        return {
            "total_population_n": n,
            "poor_population_q": q,
            "poverty_line_z": round(poverty_line, 2),
            "p0_headcount_ratio_pct": round(p0, 2),
            "p1_poverty_gap_pct": round(p1, 4),
            "p2_poverty_severity_pct": round(p2, 4),
            "excel_formula": "P0: =COUNTIF(range, \"<\" & poverty_line) / COUNT(range) * 100",
            "spss_menu": "Transform > Recode into Different Variables (miskin = 1 jika pengeluaran < Garis Kemiskinan, 0 lainnya), lalu Frequencies",
            "steps": [
                f"Jumlah Penduduk Miskin (Pengeluaran < {poverty_line:,.0f}) = {q:,} dari total {n:,} orang",
                f"P0 (Headcount Index) = ({q} / {n}) * 100% = {p0:.2f}%",
                f"P1 (Poverty Gap Index) = {p1:.4f}",
                f"P2 (Poverty Severity Index) = {p2:.4f}",
            ],
            "conclusion": f"Persentase Penduduk Miskin (P0) adalah {p0:.2f}%, Indeks Kedalaman (P1) adalah {p1:.4f}, dan Indeks Keparahan (P2) adalah {p2:.4f}.",
        }

    @staticmethod
    def calculate_sex_and_dependency_ratio(
        males: int,
        females: int,
        age_0_14: int,
        age_15_64: int,
        age_65_plus: int,
    ) -> Dict[str, Any]:
        """
        BPS Demographic Ratios:
        - Sex Ratio = (Jumlah Laki-laki / Jumlah Perempuan) * 100
        - Dependency Ratio = ((Usia 0-14 + Usia 65+) / Usia 15-64) * 100
        """
        sex_ratio = (males / females * 100.0) if females > 0 else 0.0
        non_productive = age_0_14 + age_65_plus
        dep_ratio = (non_productive / age_15_64 * 100.0) if age_15_64 > 0 else 0.0

        return {
            "males": males,
            "females": females,
            "sex_ratio": round(sex_ratio, 2),
            "age_0_14": age_0_14,
            "age_15_64": age_15_64,
            "age_65_plus": age_65_plus,
            "non_productive_population": non_productive,
            "dependency_ratio": round(dep_ratio, 2),
            "excel_formula": "Sex Ratio: =(males/females)*100, Dep Ratio: =((age_0_14 + age_65_plus)/age_15_64)*100",
            "spss_menu": "Transform > Compute Variable",
            "steps": [
                f"Rasio Jenis Kelamin = ({males:,} / {females:,}) * 100 = {sex_ratio:.2f}",
                f"Rasio Ketergantungan = (({age_0_14:,} + {age_65_plus:,}) / {age_15_64:,}) * 100 = {dep_ratio:.2f}",
            ],
            "conclusion": f"Rasio Jenis Kelamin = {sex_ratio:.2f} (terdapat {sex_ratio:.0f} laki-laki per 100 perempuan) dan Rasio Beban Ketergantungan = {dep_ratio:.2f} per 100 penduduk usia produktif.",
        }

    @staticmethod
    def calculate_cpi_inflation(
        base_prices: List[float],
        current_prices: List[float],
        base_quantities: List[float],
    ) -> Dict[str, Any]:
        """
        Laspeyres Consumer Price Index (IHK) & Inflation Rate:
        IHK_Laspeyres = (sum(p_t * q_0) / sum(p_0 * q_0)) * 100
        Inflation = IHK_t - 100 (jika tahun dasar = 100)
        """
        p0 = np.array(base_prices, dtype=float)
        pt = np.array(current_prices, dtype=float)
        q0 = np.array(base_quantities, dtype=float)

        sum_pt_q0 = float(np.sum(pt * q0))
        sum_p0_q0 = float(np.sum(p0 * q0))

        ihk = (sum_pt_q0 / sum_p0_q0 * 100.0) if sum_p0_q0 > 0 else 100.0
        inflation = ihk - 100.0

        return {
            "sum_pt_q0": round(sum_pt_q0, 2),
            "sum_p0_q0": round(sum_p0_q0, 2),
            "ihk_laspeyres": round(ihk, 2),
            "inflation_rate_pct": round(inflation, 2),
            "excel_formula": "=SUMPRODUCT(pt_range, q0_range) / SUMPRODUCT(p0_range, q0_range) * 100",
            "spss_menu": "Transform > Compute Variable",
            "steps": [
                f"Total Nilai Konsumsi Periode Berjalan (sum Pt*Q0) = {sum_pt_q0:,.2f}",
                f"Total Nilai Konsumsi Periode Dasar (sum P0*Q0) = {sum_p0_q0:,.2f}",
                f"IHK Laspeyres = ({sum_pt_q0:,.2f} / {sum_p0_q0:,.2f}) * 100 = {ihk:.2f}",
                f"Laju Inflasi = {ihk:.2f} - 100.00 = {inflation:+.2f}%",
            ],
            "conclusion": f"Indeks Harga Konsumen (IHK) Laspeyres adalah {ihk:.2f}, mencerminkan laju inflasi sebesar {inflation:+.2f}%.",
        }
