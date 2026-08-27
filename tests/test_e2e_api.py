"""
End-to-End API Integration Test for Generator Tugas Random SPSS & Excel
"""

import json
import urllib.request
import unittest


class TestE2EApi(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8000"

    def test_01_index_html(self):
        html = urllib.request.urlopen(f"{self.BASE_URL}/").read().decode("utf-8")
        self.assertIn("StatTask AutoGen", html)
        self.assertIn("Mode Kuis", html)

    def test_02_themes_and_categories(self):
        res = json.loads(urllib.request.urlopen(f"{self.BASE_URL}/api/themes").read())
        self.assertEqual(len(res["themes"]), 5)
        self.assertEqual(len(res["categories"]), 10)

    def test_03_generate_100_questions_quiz(self):
        data = json.dumps({"count": 100}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/quiz/generate",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        res = json.loads(urllib.request.urlopen(req).read())
        self.assertEqual(res["quiz_count"], 100)
        self.assertEqual(len(res["questions"]), 100)

        # Verify first question structure
        q1 = res["questions"][0]
        self.assertIn("id", q1)
        self.assertIn("title", q1)
        self.assertIn("task_text", q1)
        self.assertIn("expected_value", q1)
        self.assertIn("excel_guide", q1)
        self.assertIn("spss_guide", q1)

    def test_04_check_answer_and_steps(self):
        # Generate 1 question
        data = json.dumps({"count": 1}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/quiz/generate",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        res = json.loads(urllib.request.urlopen(req).read())
        q = res["questions"][0]

        # Submit exact correct answer
        check_payload = json.dumps({
            "question_id": q["id"],
            "user_answer": str(q["expected_value"]),
            "expected_value": q["expected_value"],
            "tolerance": q["tolerance"],
            "ground_truth_details": q["ground_truth_details"],
        }).encode("utf-8")

        check_req = urllib.request.Request(
            f"{self.BASE_URL}/api/quiz/check",
            data=check_payload,
            headers={"Content-Type": "application/json"},
        )
        check_res = json.loads(urllib.request.urlopen(check_req).read())
        self.assertTrue(check_res["is_correct"])
        self.assertIn("feedback_message", check_res)

    def test_05_universal_calculator(self):
        calc_payload = json.dumps({
            "analysis_type": "dispersion",
            "data_x": [10, 20, 30, 40, 50],
        }).encode("utf-8")
        calc_req = urllib.request.Request(
            f"{self.BASE_URL}/api/validator/calculate",
            data=calc_payload,
            headers={"Content-Type": "application/json"},
        )
        calc_res = json.loads(urllib.request.urlopen(calc_req).read())
        self.assertEqual(calc_res["range"], 40.0)
        self.assertEqual(calc_res["variance_sample"], 250.0)

    def test_06_cheatsheet(self):
        res = json.loads(urllib.request.urlopen(f"{self.BASE_URL}/api/cheatsheet").read())
        self.assertTrue(len(res["excel_formulas"]) > 10)
        self.assertTrue(len(res["spss_nav_menus"]) > 10)


if __name__ == "__main__":
    unittest.main()
