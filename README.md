# Portfolio Foundation: Context-Only Policy Pretraining + Asset Fine-Tuning

This monorepo contains:
- A reproducible research codebase for training portfolio rebalancing policies using distributional (risk-aware) objectives.
- A LaTeX paper living in the same repository (code + paper monorepo).
- A strict engineering philosophy: configuration-driven experiments, typed interfaces, contract-style tests, and centralized constants.

**Latest paper PDF (GitHub Pages):** `https://<your-github-username>.github.io/portfolio-rebalance/paper/main.pdf`

## Core Idea
We train two models:

### 1) Foundation Model (generalizable)
A portfolio policy is trained on many assets using non-identifying context only:
- Rolling return statistics (mean/vol/downside/drawdown)
- Factor exposures (PCA-based betas to start)
- Residual risk
- Liquidity proxies (if data includes volume)
- Sector one-hot etc. (when available)
- Covariance-row feature for each asset within the chosen subset

Identity embedding exists in the architecture but is set to all zeros during foundation training/evaluation. This encourages learning transferable structure rather than memorizing ticker identities.

### 2) Fine-Tuned Model (asset-specific)
We fix a subset of assets of size N (configurable; e.g., 2, 3, 10, 15) and fine-tune:
- Initialize weights from the foundation model
- Optionally enable identity embeddings only for the fixed subset
- Observe convergence speed and possible overfitting/generalization loss

## Objectives
v0 utility: semivariance rebalanced returns under long-only constraint.
All constraints and utilities are pluggable modules (no refactoring required to change them).

## Repository Layout (high level)
- `src/pf/` — Python package containing data ingestion, feature engineering, modeling, training, and evaluation code.
- `configs/` — YAML configs for data fetching, feature computation, training, and evaluation.
- `artifacts/` — Generated outputs (parquet, checkpoints, figures). This directory is gitignored.
- `paper/` — LaTeX paper source and bibliography.
- `tests/` — Contract & invariant tests (not unit tests of internal behavior).

## Repository Structure
```
.
├── .github/             # CI workflows
├── configs/             # Data/feature/train/eval configuration
├── paper/               # LaTeX source for the paper
├── tests/               # Contract/invariant tests
├── CONTRIBUTING.md      # Engineering and testing guidance
├── EXTRA_CONTEXT.md     # Roadmap and tickets
├── pyproject.toml       # Tooling and dependency config
└── README.md            # Project overview
```

## Quickstart

### 1) Create a virtual environment (Python 3.12) and install
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

### 2) Run checks locally
```bash
ruff format .
ruff check .
pyright
pytest
```

### 3) Build the paper locally
```bash
cd paper
latexmk -pdf -bibtex -interaction=nonstopmode -halt-on-error main.tex
```

## CLI (planned)
This repo is structured around a CLI with these commands:
```
pf data fetch --config configs/data/stooq_daily.yaml
pf features build --config configs/features/features_v0.yaml
pf train foundation --config configs/train/foundation_v0.yaml
pf train finetune --config configs/train/finetune_v0.yaml
pf eval foundation --config configs/eval/eval_foundation.yaml
pf eval finetune --config configs/eval/eval_finetune.yaml
```

Implementation will follow the ticket list in `EXTRA_CONTEXT.md`.

## Testing philosophy
We use tests to verify:
- Schema compatibility between modules (provider → store → feature pipeline → rollout → training)
- Dataset/config invariants required by docstrings and assumptions
- End-to-end executability (tiny runs)

We do not write tests that assert internal algorithmic behavior.
See `tests/README.md` and `CONTRIBUTING.md` for more details.
