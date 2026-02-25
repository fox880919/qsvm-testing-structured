import os
import sys
import subprocess
import re
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# @ = project root (path of this file's parent's parent)
ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = ROOT  # alias

STEP1_CSV = ROOT / "saved_data" / "my_data_frame_Jan_all.csv"
STEP2_CSV = ROOT / "results_v41_kernel_test.csv"

# Progress report: env var (supports @/ = project root), or first existing candidate
def _resolve_path(p: str, base: Path) -> Path:
    """Resolve path; @ or @/ means project root (e.g. @/progress report)."""
    p = p.strip()
    if p == "@":
        return base
    if p.startswith("@/"):
        return (base / p[2:].lstrip("/")).resolve()
    if p.startswith("@"):
        return (base / p[1:].lstrip("/")).resolve()
    return Path(p).resolve()

_progress_dir = os.environ.get("PROGRESS_REPORT_DIR")
if _progress_dir:
    PROGRESS_REPORT_DIR = _resolve_path(_progress_dir, ROOT)
else:
    _candidates = [
        ROOT / "progress report",
        Path.cwd() / "progress report",
    ]
    PROGRESS_REPORT_DIR = next((p for p in _candidates if p.exists()), ROOT / "progress report")

job_state = {
    "status": "idle",
    "phase": "",
    "phase_detail": "",
    "log": [],
    "returncode": None,
    "step1_exists": False,
    "step2_exists": False,
}
_running_proc = None

app = FastAPI(
    title="QSVM Structure Testing API",
    description="Run mutation and metamorphic testing for QSVM",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    dataset: int = 0
    kfold: int = 5
    experiment: str = "all"  # "all" | "1" | "2" | "3"


class VisualizationRequest(BaseModel):
    dataset: int = 0
    feature_map_type: int = 0  # 0=amplitude, 1=angle


class ExecuteRequest(BaseModel):
    code: str


class LatexUpdateRequest(BaseModel):
    content: str


class RunResponse(BaseModel):
    status: str
    job_id: str = "default"


class StatusResponse(BaseModel):
    status: str
    phase: str
    phase_detail: str
    log: list[str]
    returncode: int | None
    step1_exists: bool
    step2_exists: bool


def infer_phase(log_text: str) -> tuple[str, str]:
    if "Experiment 3: Kernel Testing" in log_text or "Kernel Testing" in log_text:
        return "step3", "Kernel Testing (14 MRs, 3 feature maps)"
    if "Experiment 2: Statistical Testing" in log_text or "Statistical Testing" in log_text:
        mr_match = re.search(r"mr number:\s*(\d+)", log_text, re.IGNORECASE)
        if mr_match:
            mr = int(mr_match.group(1))
            return "step2", f"Statistical Testing (MR {mr}/12)"
        return "step2", "Statistical Testing (12 MRs, angle + amplitude)"
    if "Experiment 1: Baseline" in log_text or "MR#1 (scaling)" in log_text or "MR#2 (rotation)" in log_text:
        return "step1", "Baseline (MR#1 scaling, MR#2 rotation)"
    if "originalScore" in log_text or "runScript" in log_text:
        return "step2", "Statistical Testing (12 MRs, angle + amplitude)"
    return "config", "Configuration loaded"


def run_tests_thread(dataset: int, kfold: int, experiment: str = "all"):
    global job_state, _running_proc
    job_state["status"] = "running"
    job_state["phase"] = "config"
    job_state["phase_detail"] = f"Dataset {dataset}, K-fold {kfold}, Experiment: {experiment}"
    job_state["log"] = []
    job_state["returncode"] = None

    os.makedirs(PROJECT_ROOT / "saved_data", exist_ok=True)
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "main.py"),
        "--dataset", str(dataset),
        "--kfold", str(kfold),
        "--experiment", experiment,
    ]
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    proc = subprocess.Popen(
        cmd,
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )
    _running_proc = proc

    def read_output():
        for line in iter(proc.stdout.readline, ""):
            job_state["log"].append(line.rstrip())
            phase, detail = infer_phase("\n".join(job_state["log"]))
            job_state["phase"] = phase
            job_state["phase_detail"] = detail

    t = threading.Thread(target=read_output)
    t.start()
    proc.wait()
    t.join()
    _running_proc = None

    job_state["returncode"] = proc.returncode
    job_state["step1_exists"] = STEP1_CSV.exists()
    job_state["step2_exists"] = STEP2_CSV.exists()
    if job_state["status"] == "cancelled":
        # Keep phase as-is (where we were when cancelled), don't set to "done"
        job_state["phase_detail"] = "Cancelled by user"
    else:
        job_state["status"] = "completed" if proc.returncode == 0 else "failed"
        job_state["phase"] = "done"
        job_state["phase_detail"] = "All tests completed" if proc.returncode == 0 else "Tests failed"


@app.post("/api/cancel")
def cancel_run():
    global _running_proc
    if job_state["status"] != "running":
        raise HTTPException(409, "No test run in progress")
    if _running_proc is None:
        raise HTTPException(409, "Process not available")
    job_state["status"] = "cancelled"
    _running_proc.terminate()
    return {"status": "cancelled"}


@app.api_route("/api/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok", "python": sys.version}


@app.post("/api/run", response_model=RunResponse)
def run_tests(req: RunRequest):
    if req.dataset not in (0, 1, 2, 3):
        raise HTTPException(400, "dataset must be 0, 1, 2, or 3")
    if req.kfold < 2 or req.kfold > 20:
        raise HTTPException(400, "kfold must be between 2 and 20")
    if req.experiment not in ("all", "1", "2", "3"):
        raise HTTPException(400, "experiment must be 'all', '1', '2', or '3'")
    if job_state["status"] == "running":
        raise HTTPException(409, "A test run is already in progress")

    t = threading.Thread(target=run_tests_thread, args=(req.dataset, req.kfold, req.experiment))
    t.start()
    return RunResponse(status="started", job_id="default")


@app.get("/api/status", response_model=StatusResponse)
def get_status():
    return StatusResponse(
        status=job_state["status"],
        phase=job_state["phase"],
        phase_detail=job_state["phase_detail"],
        log=job_state["log"][-200:],
        returncode=job_state["returncode"],
        step1_exists=job_state["step1_exists"],
        step2_exists=job_state["step2_exists"],
    )


@app.post("/api/notebook/execute")
def execute_code(req: ExecuteRequest):
    import subprocess as sp
    if not req.code or not req.code.strip():
        return {"stdout": "", "stderr": "", "error": "Empty code"}
    try:
        result = sp.run(
            [sys.executable, "-c", req.code],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )
        return {
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
            "error": None if result.returncode == 0 else f"Exit code {result.returncode}",
        }
    except sp.TimeoutExpired:
        return {"stdout": "", "stderr": "", "error": "Execution timed out (60s)"}
    except Exception as e:
        return {"stdout": "", "stderr": "", "error": str(e)}


@app.post("/api/visualization")
def get_qsvm_visualization(req: VisualizationRequest):
    """Generate QSVM decision boundary plot (2D PCA projection). Returns base64 PNG."""
    if req.dataset != 0:
        raise HTTPException(400, "Visualization only supports Wine dataset (0)")
    if req.feature_map_type not in (0, 1):
        raise HTTPException(400, "feature_map_type must be 0 (amplitude) or 1 (angle)")
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from qsvm_visualization import generate_qsvm_visualization
        img_b64 = generate_qsvm_visualization(
            dataset=req.dataset,
            feature_map_type=req.feature_map_type,
        )
        if img_b64 is None:
            raise HTTPException(500, "Failed to generate visualization")
        return {"image": img_b64, "feature_map_type": req.feature_map_type}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/pipeline/summary")
def get_pipeline_summary(dataset: int = 0):
    """Get data extraction and PCA summary for the experiment pipeline."""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from pipeline_visualization import get_pipeline_summary as _get
        return _get(dataset)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/pipeline/circuits/{feature_map_type}")
def get_circuit_diagram(feature_map_type: int):
    """Get circuit diagram for amplitude (0) or angle (1) embedding. Returns base64 PNG."""
    if feature_map_type not in (0, 1):
        raise HTTPException(400, "feature_map_type must be 0 (amplitude) or 1 (angle)")
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from pipeline_visualization import get_circuit_diagram as _get
        img = _get(feature_map_type)
        if img is None:
            raise HTTPException(500, "Failed to generate circuit diagram")
        return {"image": img, "feature_map_type": feature_map_type}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/pipeline/step1")
def get_step1_analysis():
    """Get Step 1 mutation analysis (equivalent, killed, survived, crashed) for charts."""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from pipeline_visualization import get_step1_analysis as _get
        result = _get(STEP1_CSV)
        if result is None:
            return {"equivalent": 0, "killed": 0, "survived": 0, "crashed": 0, "total": 0, "rows": []}
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/pipeline/step2")
def get_step2_analysis():
    """Get Step 2 golden matrix and kernel testing results."""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from pipeline_visualization import get_step2_analysis as _get
        result = _get(STEP2_CSV)
        if result is None:
            return {"modes": [], "defect_combos": [], "caught_rates": [], "rows": []}
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/results/step1")
def download_step1():
    if not STEP1_CSV.exists():
        raise HTTPException(404, "Step 1 results not found. Run tests first.")
    return FileResponse(STEP1_CSV, filename="my_data_frame_Jan_all.csv", media_type="text/csv")


@app.get("/api/results/step2")
def download_step2():
    if not STEP2_CSV.exists():
        raise HTTPException(404, "Step 2 results not found. Run tests first.")
    return FileResponse(STEP2_CSV, filename="results_v41_kernel_test.csv", media_type="text/csv")


# --- Experiment Figures (for report charts) ---

FIGURES_DIR = PROGRESS_REPORT_DIR / "figures"
FIGURES2_DIR = PROGRESS_REPORT_DIR / "figures2"

FIGURE_PATHS = {
    "experiment2_heatmap": FIGURES_DIR / "mutant_outcome_fully_hierarchical_heatmap_sequential_labels_fixed_data.png",
    "experiment2_pie": FIGURES_DIR / "mutant_detection_coverage_pie_chart.png",
    "experiment3_detection": FIGURES2_DIR / "chart_v41_detection_omni_2.png",
    "experiment3_heatmap": FIGURES2_DIR / "chart_v41_heatmap_omni_2.png",
}


# Specific figure routes (must be defined before /api/figures/{figure_id})
@app.get("/api/figures/experiment2/heatmap")
def get_exp2_heatmap():
    path = FIGURE_PATHS["experiment2_heatmap"]
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "Run chart generation after Statistical Testing.")
    return FileResponse(path, media_type="image/png")


@app.get("/api/figures/experiment2/pie")
def get_exp2_pie():
    path = FIGURE_PATHS["experiment2_pie"]
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "Run chart generation after Statistical Testing.")
    return FileResponse(path, media_type="image/png")


@app.get("/api/figures/experiment3/detection")
def get_exp3_detection():
    path = FIGURE_PATHS["experiment3_detection"]
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "Run chart generation after Kernel Testing.")
    return FileResponse(path, media_type="image/png")


@app.get("/api/figures/experiment3/heatmap")
def get_exp3_heatmap():
    path = FIGURE_PATHS["experiment3_heatmap"]
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "Run chart generation after Kernel Testing.")
    return FileResponse(path, media_type="image/png")


@app.get("/api/figures/{figure_id}")
def get_experiment_figure(figure_id: str):
    """Serve experiment figure by ID (e.g. experiment2_heatmap). 404 if not found."""
    if figure_id not in FIGURE_PATHS:
        raise HTTPException(400, f"Unknown figure: {figure_id}")
    path = FIGURE_PATHS[figure_id]
    if not path.exists() or not path.is_file():
        raise HTTPException(404, f"Figure not found. Run chart generation after experiments.")
    return FileResponse(path, media_type="image/png")


@app.get("/api/figures/available")
def list_available_figures():
    """Return which experiment figures exist."""
    return {
        "experiment2_heatmap": FIGURE_PATHS["experiment2_heatmap"].exists(),
        "experiment2_pie": FIGURE_PATHS["experiment2_pie"].exists(),
        "experiment3_detection": FIGURE_PATHS["experiment3_detection"].exists(),
        "experiment3_heatmap": FIGURE_PATHS["experiment3_heatmap"].exists(),
    }


@app.post("/api/figures/generate")
def generate_figures():
    """Run chart generation scripts. Requires Statistical Testing and/or Kernel Testing CSV data."""
    if job_state["status"] == "running":
        raise HTTPException(409, "Cannot generate charts while tests are running.")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "charts.run_all_charts"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise HTTPException(500, result.stderr or result.stdout or "Chart generation failed")
        return {"success": True}
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "Chart generation timed out")
    except Exception as e:
        raise HTTPException(500, str(e))


# --- Progress Report (LaTeX) ---

@app.get("/api/report/latex/files")
def list_latex_files():
    """List available .tex files in the progress report folder."""
    if not PROGRESS_REPORT_DIR.exists():
        return {"files": []}
    files = sorted(
        f.stem for f in PROGRESS_REPORT_DIR.glob("*.tex")
        if not f.name.startswith(".") and f.stem not in ("quantikz", "sample")
    )
    return {"files": files}


def _get_latest_pdf_path():
    """Return path to latest PDF: prefer highest progress_report_N, else most recent by mtime."""
    if not PROGRESS_REPORT_DIR.exists():
        return None
    pdfs = list(PROGRESS_REPORT_DIR.glob("*.pdf"))
    if not pdfs:
        return None

    def sort_key(p):
        stem = p.stem
        if stem.startswith("progress_report_"):
            try:
                n = int(stem.split("_")[-1])
                return (1, n)
            except ValueError:
                pass
        return (0, p.stat().st_mtime)

    return max(pdfs, key=sort_key)


@app.get("/api/report/pdf/latest")
def get_latest_pdf():
    """Serve the latest PDF (highest progress_report_N, else most recent by mtime)."""
    path = _get_latest_pdf_path()
    if path is None:
        raise HTTPException(404, "No PDF found. Compile your LaTeX to generate a PDF.")
    return FileResponse(path, filename=path.name, media_type="application/pdf")


@app.get("/api/report/pdf/{filename}")
def get_pdf_by_name(filename: str):
    """Serve a specific PDF by name (e.g. progress_report_6)."""
    if not PROGRESS_REPORT_DIR.exists():
        raise HTTPException(404, "Progress report folder not found")
    safe = "".join(c for c in filename if c.isalnum() or c in "_-.")
    if safe != filename:
        raise HTTPException(400, "Invalid filename")
    name = filename if filename.endswith(".pdf") else f"{filename}.pdf"
    path = PROGRESS_REPORT_DIR / name
    if not path.exists() or not path.is_file():
        raise HTTPException(404, f"PDF {path.name} not found")
    return FileResponse(path, filename=path.name, media_type="application/pdf")


@app.get("/api/report/latex/{filename}/pdf")
def get_pdf_via_latex_path(filename: str):
    """Serve PDF using same path structure as LaTeX (avoids /api/report/pdf/ routing issues)."""
    if not PROGRESS_REPORT_DIR.exists():
        raise HTTPException(404, "Progress report folder not found")
    safe = "".join(c for c in filename if c.isalnum() or c in "_-")
    if safe != filename:
        raise HTTPException(400, "Invalid filename")
    path = PROGRESS_REPORT_DIR / f"{filename}.pdf"
    if not path.exists() or not path.is_file():
        raise HTTPException(404, f"PDF {path.name} not found")
    return FileResponse(
        path,
        filename=path.name,
        media_type="application/pdf",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"},
    )


@app.get("/api/report/latex/{filename}")
def get_latex_content(filename: str):
    """Get the raw content of a .tex file from the progress report folder."""
    if not PROGRESS_REPORT_DIR.exists():
        raise HTTPException(404, "Progress report folder not found")
    # Sanitize: only allow alphanumeric, underscore, hyphen
    safe = "".join(c for c in filename if c.isalnum() or c in "_-")
    if safe != filename:
        raise HTTPException(400, "Invalid filename")
    path = PROGRESS_REPORT_DIR / f"{filename}.tex"
    if not path.exists() or not path.is_file():
        raise HTTPException(404, f"File {filename}.tex not found")
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        return {"filename": f"{filename}.tex", "content": content}
    except OSError as e:
        raise HTTPException(500, f"Could not read file: {e}")


def _validate_latex_filename(filename: str) -> Path:
    """Validate filename and return path to .tex file."""
    if not PROGRESS_REPORT_DIR.exists():
        raise HTTPException(404, "Progress report folder not found")
    safe = "".join(c for c in filename if c.isalnum() or c in "_-")
    if safe != filename:
        raise HTTPException(400, "Invalid filename")
    return PROGRESS_REPORT_DIR / f"{filename}.tex"


@app.put("/api/report/latex/{filename}")
@app.post("/api/report/latex/{filename}")
def update_latex_content(filename: str, req: LatexUpdateRequest):
    """Save LaTeX content to file."""
    path = _validate_latex_filename(filename)
    try:
        path.write_text(req.content, encoding="utf-8")
        return {"filename": f"{filename}.tex", "saved": True}
    except OSError as e:
        raise HTTPException(500, f"Could not write file: {e}")


@app.post("/api/report/latex/{filename}/compile")
def compile_latex_to_pdf(filename: str):
    """Compile .tex to .pdf using pdflatex (runs twice for references)."""
    path = _validate_latex_filename(filename)
    if not path.exists():
        raise HTTPException(404, f"File {filename}.tex not found")
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", path.name],
            cwd=str(PROGRESS_REPORT_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr or result.stdout or f"pdflatex exited with {result.returncode}",
            }
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", path.name],
            cwd=str(PROGRESS_REPORT_DIR),
            capture_output=True,
            timeout=120,
        )
        pdf_path = PROGRESS_REPORT_DIR / f"{filename}.pdf"
        return {"success": pdf_path.exists(), "pdf": pdf_path.name}
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "LaTeX compilation timed out")
    except FileNotFoundError:
        raise HTTPException(503, "pdflatex not found. Install TeX Live or MiKTeX.")


# Serve built frontend for Electron (must be last)
FRONTEND_DIST = ROOT / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
