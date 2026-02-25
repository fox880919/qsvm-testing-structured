# QSVM Structure Testing

Mutation testing project for Quantum Support Vector Machines (QSVM), extracted from the September mutation testing project.

## New device / one-command run

From a fresh clone, install system prerequisites, then run:

```bash
# Prerequisites (install once): Python 3, Node 20+ (or nvm)
./scripts/start.sh
```

`start.sh` will automatically:
- Use Node from `.nvmrc` if nvm is installed (or install it via `nvm install`)
- Create Python venv and install pip dependencies if `venv` is missing
- Install root and frontend npm dependencies if `node_modules` are missing
- Start backend and frontend

## Setup

### Python (virtual environment, Python 3)

```bash
./scripts/setup_venv.sh
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r api/requirements.txt
```

### Web Interface (React + TypeScript + Tailwind)

- **Node.js 20+ required** (Vite 7 and Tailwind v4 need Node 20.19+ or 22.12+). If you see "Cannot find native binding" or "Vite requires Node.js version 20.19+", upgrade Node:
  - With nvm: `nvm install 20 && nvm use 20` (or `nvm use` if `.nvmrc` exists)
  - With Homebrew: `brew install node@20`
- **King's branding**: Uses King's College London theme (red/white). To use the official logo, add `kings-logo.png` to `frontend/public/` (the app will prefer it over the built-in SVG).

```bash
cd frontend && npm install
```

## Run

### Command line

```bash
source venv/bin/activate
python main.py --dataset 0 --kfold 5
```

### Web Interface (React + FastAPI)

1. **Start backend** (from project root, with venv activated):

   ```bash
   source venv/bin/activate
   uvicorn api.server:app --reload --port 8000
   ```

   Or use the script:

   ```bash
   ./scripts/run_backend.sh
   ```

2. **Start frontend** (new terminal):

   ```bash
   cd frontend && npm run dev
   ```

   Or: `./scripts/run_frontend.sh`

3. Open **http://localhost:5173** in your browser.

**One command** (from project root, after `./scripts/setup_venv.sh`):

```bash
./scripts/run_all.sh
```

Or: `npm start`

The test runs in two steps:
1. **Step 1** (September-style): Mutant testing with MRs 13–16 over mutants 1–30
2. **Step 2** (February main41): Kernel testing with defect injection and 14 MRs; outputs `results_v41_kernel_test.csv`

## Structure

| Path | Purpose |
|------|---------|
| `main.py` | Entry point; runs mutants through metamorphic relation tests |
| `main_class.py` | QSVM execution logic |
| `main_statistical_class.py` | Statistical testing (t-tests, k-fold) |
| `quantum/` | Feature maps (`feature_map.py`, `feature_map_m*.py`) and kernels |
| `classes/` | Parameters, configuration, dataframe helpers |
| `data/` | Dataset loaders (Wine, load_digits, etc.) |
| `metamorphic/` | Metamorphic relations for test oracles |

## Mutant Order (1–30 sequential)

Mutants 1–30 map to different subsystems (see `default_parameters.py`):

| Subsystem | Mutant IDs | Files |
|-----------|------------|-------|
| Feature map | 1–6, 11–13, 16, 20, 22–30 | `quantum/feature_map_m{N}.py` |
| Q kernel | 7–10 | `quantum/q_kernel_m{N}.py` |
| Main class | 14, 17 | `main_class_m{N}.py` |
| Main statistical class | 18, 21 | `main_statistical_class_m{N}.py` |
| Data | 15 | `data/wine_data_m{N}.py` |
| Metamorphic | 19 | `metamorphic/my_metamorphic_relations_m19.py` |

- **Angle embedding**: mutants 1–6 (feature maps)
- **Amplitude embedding**: mutants 1–30 (all types)
