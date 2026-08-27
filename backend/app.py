"""
FastAPI Server for Generator Tugas Random SPSS & Excel
Author: Antigravity
Main application exposing statistical calculation, dataset generation,
dynamic 100-question quiz, answer validation, and file export endpoints.
"""

import os
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd

from backend.dataset_generator import DatasetGenerator
from backend.question_bank_100 import QUESTION_BANK, CATEGORIES
from backend.question_engine import QuestionEngine, to_serializable
from backend.statistical_solver import StatisticalSolver
from backend.export_service import ExportService
from backend.cheatsheet_data import SPSS_NAV_MENUS, EXCEL_FORMULAS

app = FastAPI(
    title="Generator Tugas Random SPSS & Excel API",
    description="Otomasi Dataset Statistik & 100 Bank Soal Latihan Praktik SPSS & Excel",
    version="1.0.0",
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for active dataset
ACTIVE_DATASET_STORE: Dict[str, Any] = {}


# Initial default dataset bootstrap
def _init_default_dataset():
    data = DatasetGenerator.generate_dataset(theme_id="susenas_rt", n_rows=50, seed=42)
    ACTIVE_DATASET_STORE["current"] = data
    ACTIVE_DATASET_STORE["df"] = pd.DataFrame(data["all_data"])


_init_default_dataset()


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class GenerateDatasetRequest(BaseModel):
    theme_id: str = "susenas_rt"
    n_rows: int = 50
    seed: Optional[int] = None


class GenerateQuizRequest(BaseModel):
    count: int = 10
    category_ids: Optional[List[str]] = None
    difficulties: Optional[List[str]] = None
    seed: Optional[int] = None


class CheckAnswerRequest(BaseModel):
    question_id: str
    user_answer: Any
    expected_value: Any
    tolerance: float = 0.05
    ground_truth_details: Optional[Dict[str, Any]] = None


class UniversalCalculationRequest(BaseModel):
    analysis_type: str  # 'mean', 'ttest_1samp', 'ttest_ind', 'anova', 'correlation', 'regression', 'chisq', 'bps_poverty'
    data_x: Optional[List[float]] = None
    data_y: Optional[List[float]] = None
    group_data: Optional[Dict[str, List[float]]] = None
    contingency_table: Optional[List[List[int]]] = None
    parameter_mu0: Optional[float] = 0.0
    parameter_poverty_line: Optional[float] = 580000.0


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/api/themes")
def get_themes():
    return {
        "themes": list(DatasetGenerator.AVAILABLE_THEMES.values()),
        "categories": CATEGORIES,
    }


@app.post("/api/dataset/generate")
def generate_dataset(req: GenerateDatasetRequest):
    data = DatasetGenerator.generate_dataset(theme_id=req.theme_id, n_rows=req.n_rows, seed=req.seed)
    ACTIVE_DATASET_STORE["current"] = data
    ACTIVE_DATASET_STORE["df"] = pd.DataFrame(data["all_data"])
    return {
        "status": "success",
        "message": f"Dataset '{data['theme_name']}' ({data['total_rows']} baris) berhasil di-generate.",
        "dataset_summary": {
            "theme_id": data["theme_id"],
            "theme_name": data["theme_name"],
            "total_rows": data["total_rows"],
            "columns": data["columns"],
            "column_summaries": data["column_summaries"],
            "sample_data": data["sample_data"],
            "dictionary": data["dictionary"],
            "seed": data["seed"],
        },
    }


@app.get("/api/dataset/current")
def get_current_dataset():
    if "current" not in ACTIVE_DATASET_STORE:
        _init_default_dataset()
    data = ACTIVE_DATASET_STORE["current"]
    return {
        "theme_id": data["theme_id"],
        "theme_name": data["theme_name"],
        "total_rows": data["total_rows"],
        "columns": data["columns"],
        "column_summaries": data["column_summaries"],
        "sample_data": data["sample_data"],
        "dictionary": data["dictionary"],
        "seed": data["seed"],
    }


@app.get("/api/dataset/export/{export_format}")
def export_dataset(export_format: str):
    if "df" not in ACTIVE_DATASET_STORE:
        _init_default_dataset()

    df = ACTIVE_DATASET_STORE["df"]
    meta = ACTIVE_DATASET_STORE["current"]
    theme_id = meta.get("theme_id", "dataset")

    if export_format == "excel" or export_format == "xlsx":
        buffer = ExportService.export_to_excel(df, meta)
        filename = f"{theme_id}_latihan_spss_excel.xlsx"
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    elif export_format == "csv":
        csv_str = ExportService.export_to_csv(df)
        filename = f"{theme_id}_dataset.csv"
        return Response(
            content=csv_str,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    elif export_format == "spss" or export_format == "sps":
        sps_code = ExportService.export_to_spss_syntax(df, meta, filename_hint=f"{theme_id}_dataset.csv")
        filename = f"{theme_id}_spss_syntax.sps"
        return Response(
            content=sps_code,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    else:
        raise HTTPException(status_code=400, detail="Format tidak didukung. Pilih: excel, csv, atau spss.")


@app.get("/api/questions/categories")
def get_categories():
    return {"categories": CATEGORIES}


@app.get("/api/questions/bank")
def get_question_bank(
    category_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
):
    results = QUESTION_BANK.copy()
    if category_id:
        results = [q for q in results if q["cat_id"] == category_id]
    if difficulty:
        results = [q for q in results if q["difficulty"] == difficulty]
    if search:
        s = search.lower()
        results = [q for q in results if s in q["title"].lower() or s in q["task_text"].lower() or s in q["id"].lower()]

    return {
        "total_available": len(QUESTION_BANK),
        "filtered_count": len(results),
        "questions": results,
    }


@app.post("/api/quiz/generate")
def generate_quiz(req: GenerateQuizRequest):
    if "df" not in ACTIVE_DATASET_STORE:
        _init_default_dataset()

    df = ACTIVE_DATASET_STORE["df"]
    theme_id = ACTIVE_DATASET_STORE["current"]["theme_id"]

    engine = QuestionEngine(df=df, theme_id=theme_id)
    questions = engine.generate_quiz(
        count=req.count,
        category_ids=req.category_ids,
        difficulties=req.difficulties,
        seed=req.seed,
    )

    return {
        "quiz_count": len(questions),
        "theme_id": theme_id,
        "questions": questions,
    }


@app.post("/api/quiz/check")
def check_quiz_answer(req: CheckAnswerRequest):
    eval_result = QuestionEngine.verify_answer(
        user_input=req.user_answer,
        expected_value=req.expected_value,
        tolerance=req.tolerance,
    )

    return to_serializable({
        "question_id": req.question_id,
        "is_correct": eval_result["is_correct"],
        "user_answer": eval_result["user_answer"],
        "expected_answer": eval_result["expected_answer"],
        "tolerance": eval_result["tolerance_allowed"],
        "feedback_message": eval_result["message"],
        "solution_details": req.ground_truth_details,
    })


@app.post("/api/validator/calculate")
def universal_calculator(req: UniversalCalculationRequest):
    """
    Universal internal calculator for custom manual data.
    """
    atype = req.analysis_type
    try:
        if atype == "mean" and req.data_x:
            res = StatisticalSolver.calculate_mean(req.data_x)
        elif atype == "median" and req.data_x:
            res = StatisticalSolver.calculate_median(req.data_x)
        elif atype == "dispersion" and req.data_x:
            res = StatisticalSolver.calculate_dispersion_all(req.data_x)
        elif atype == "ttest_1samp" and req.data_x:
            res = StatisticalSolver.one_sample_ttest(req.data_x, req.parameter_mu0 or 0.0)
        elif atype == "ttest_ind" and req.data_x and req.data_y:
            res = StatisticalSolver.independent_ttest(req.data_x, req.data_y)
        elif atype == "ttest_paired" and req.data_x and req.data_y:
            res = StatisticalSolver.paired_ttest(req.data_x, req.data_y)
        elif atype == "correlation" and req.data_x and req.data_y:
            res = StatisticalSolver.calculate_correlation(req.data_x, req.data_y)
        elif atype == "regression" and req.data_x and req.data_y:
            res = StatisticalSolver.linear_regression(req.data_x, req.data_y)
        elif atype == "chisq" and req.contingency_table:
            res = StatisticalSolver.chi_square_independence(req.contingency_table)
        elif atype == "anova" and req.group_data:
            groups = list(req.group_data.values())
            names = list(req.group_data.keys())
            res = StatisticalSolver.one_way_anova(groups, group_names=names)
        elif atype == "bps_poverty" and req.data_x:
            res = StatisticalSolver.calculate_fgt_poverty_indices(req.data_x, req.parameter_poverty_line or 580000.0)
        else:
            raise HTTPException(status_code=400, detail="Data atau parameter tidak lengkap untuk analisis ini.")
        return to_serializable(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan komputasi: {str(e)}")


@app.get("/api/cheatsheet")
def get_cheatsheet():
    return {
        "excel_formulas": EXCEL_FORMULAS,
        "spss_nav_menus": SPSS_NAV_MENUS,
    }


# Static frontend mounting & favicon
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    ico_path = os.path.join(FRONTEND_DIR, "favicon.ico")
    if os.path.exists(ico_path):
        return FileResponse(ico_path, media_type="image/x-icon")
    svg_path = os.path.join(FRONTEND_DIR, "favicon.svg")
    if os.path.exists(svg_path):
        return FileResponse(svg_path, media_type="image/svg+xml")
    return Response(status_code=404)

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

