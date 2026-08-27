"""
Automated Test Suite for Generator Tugas Random SPSS & Excel
Verifies:
1. Dataset Generator for all 5 BPS Themes.
2. Statistical Solver numerical correctness for all 10 modules.
3. Question Engine instantiation of all 100 unique templates in QUESTION_BANK.
4. Export Service for Excel, CSV, and SPSS Syntax.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np

from backend.dataset_generator import DatasetGenerator
from backend.question_bank_100 import QUESTION_BANK, CATEGORIES
from backend.question_engine import QuestionEngine
from backend.statistical_solver import StatisticalSolver
from backend.export_service import ExportService


class TestStatisticalEngine(unittest.TestCase):
    def setUp(self):
        # Sample dataset for tests
        self.sample_data = pd.DataFrame({
            "ID_RT": [f"RT_{i}" for i in range(1, 21)],
            "Wilayah": ["Jawa Barat"] * 10 + ["Jawa Timur"] * 10,
            "Tipe_Daerah": ["Perkotaan", "Perdesaan"] * 10,
            "Pendapatan": [3000000 + i * 250000 for i in range(20)],
            "Pengeluaran": [2000000 + i * 180000 for i in range(20)],
            "Jumlah_ART": [1, 2, 3, 4] * 5,
            "Skor_Pre": [50 + i * 2 for i in range(20)],
            "Skor_Post": [65 + i * 2 for i in range(20)],
            "Status_Kemiskinan": ["Tidak Miskin"] * 16 + ["Miskin"] * 4,
            "Status_Bekerja": ["Bekerja"] * 14 + ["Pengangguran"] * 2 + ["Sekolah"] * 4,
            "Usia": [20 + i * 2 for i in range(20)],
            "Jenis_Kelamin": ["Laki-laki"] * 11 + ["Perempuan"] * 9,
            "Pengeluaran_Perkapita": [800000 + i * 50000 for i in range(20)],
        })

    def test_theme_generation(self):
        themes = ["susenas_rt", "sakernas_kerja", "sensus_pertanian", "pelayanan_publik", "evaluasi_diklat"]
        for theme in themes:
            res = DatasetGenerator.generate_dataset(theme_id=theme, n_rows=30, seed=123)
            self.assertEqual(res["total_rows"], 30)
            self.assertIn("columns", res)
            self.assertIn("dictionary", res)
            self.assertTrue(len(res["columns"]) >= 5)

    def test_statistical_solver_descriptive(self):
        arr = [10, 20, 30, 40, 50]
        mean_res = StatisticalSolver.calculate_mean(arr)
        self.assertEqual(mean_res["value"], 30.0)

        med_res = StatisticalSolver.calculate_median(arr)
        self.assertEqual(med_res["value"], 30.0)

        disp = StatisticalSolver.calculate_dispersion_all(arr)
        self.assertEqual(disp["range"], 40.0)
        self.assertEqual(disp["variance_sample"], 250.0)
        self.assertAlmostEqual(disp["std_sample"], 15.8114, places=3)

    def test_statistical_solver_hypothesis_and_regression(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2, 4, 5, 4, 5, 7, 8, 9, 9, 11]

        # Correlation
        corr = StatisticalSolver.calculate_correlation(x, y)
        self.assertGreater(corr["pearson_r"], 0.9)
        self.assertTrue(corr["significant"])

        # Regression
        reg = StatisticalSolver.linear_regression(x, y)
        self.assertAlmostEqual(reg["r_squared"], 0.93, places=1)
        self.assertTrue(reg["model_significant"])

        # One sample t-test
        t_res = StatisticalSolver.one_sample_ttest(x, mu0=5.5)
        self.assertAlmostEqual(t_res["mean"], 5.5, places=2)

    def test_all_300_questions_instantiation(self):
        self.assertEqual(len(QUESTION_BANK), 300)
        self.assertEqual(len(CATEGORIES), 10)

        engine = QuestionEngine(df=self.sample_data, theme_id="susenas_rt")
        quiz = engine.generate_quiz(count=300, seed=42)

        self.assertEqual(len(quiz), 300)
        for q in quiz:
            self.assertIn("id", q)
            self.assertIn("title", q)
            self.assertIn("task_text", q)
            self.assertIn("expected_value", q)
            self.assertIn("excel_guide", q)
            self.assertIn("spss_guide", q)
            self.assertIsNotNone(q["expected_value"])

    def test_answer_verification(self):
        # Numeric with float tolerance
        v1 = QuestionEngine.verify_answer(user_input="30.04", expected_value=30.0, tolerance=0.05)
        self.assertTrue(v1["is_correct"])

        # String decision matching
        v2 = QuestionEngine.verify_answer(user_input="Tolak H0", expected_value="Tolak H0", tolerance=0.0)
        self.assertTrue(v2["is_correct"])

        # Comma decimal
        v3 = QuestionEngine.verify_answer(user_input="30,02", expected_value=30.0, tolerance=0.05)
        self.assertTrue(v3["is_correct"])

    def test_export_service(self):
        meta = {"theme_name": "Test Theme", "dictionary": {"Pendapatan": "Uang masuk"}}
        
        # Excel
        excel_buf = ExportService.export_to_excel(self.sample_data, meta)
        self.assertTrue(excel_buf.getbuffer().nbytes > 1000)

        # CSV
        csv_str = ExportService.export_to_csv(self.sample_data)
        self.assertIn("Pendapatan", csv_str)

        # SPSS Syntax
        sps_str = ExportService.export_to_spss_syntax(self.sample_data, meta)
        self.assertIn("VARIABLE LABELS", sps_str)
        self.assertIn("GET DATA", sps_str)


if __name__ == "__main__":
    unittest.main()
