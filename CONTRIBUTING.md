# Contributing Guide

Welcome! This repository is designed to be both a research project and a professional-grade codebase. To maintain clarity and flexibility, please adhere to the following principles when contributing.

## Design Principles

### 1) Config-first
Anything that changes experiment behavior must be controlled via configuration files under `configs/`. Code must not hardcode experiment parameters. Examples include:
- Asset universe and subset size (N)
- Date ranges and frequencies
- Rolling window lengths for statistics and covariance estimation
- Rebalance cadence and horizon
- Choice of constraint and utility functions with parameters
- Model architecture selection (e.g., MLP vs Set Transformer)

### 2) Single source of truth for hard-coded values
Any hard-coded constant must exist in exactly one location:
- `src/pf/constants.py` for runtime constants and fixed paths (non-secret)
- `src/pf/config/defaults.py` for config defaults

This eliminates “magic numbers” spread through the codebase. When a constant matters, name it and centralize it.

### 3) Strict modularity boundaries
These components must be swappable without refactoring other code:
- Providers (`src/pf/data/providers/*`) — abstract data sources (Stooq, yfinance, Finnhub, Schwab, etc.)
- Feature modules (`src/pf/features/*`) — rolling stats, factor exposures, covariance computations
- Constraints (`src/pf/modeling/constraints/*`) — long-only simplex, long/short, etc.
- Utilities (`src/pf/modeling/utilities/*`) — semivariance, CVaR, drawdown, etc.
- Policies (`src/pf/modeling/policies/*`) — MLP baseline, Set Transformer, etc.

### 4) Python 3.12 + typing
Use Python 3.12 exclusively.
Add type hints for all public functions and methods.
Use pyright for type checking and treat type errors as warnings to be fixed.

### 5) Lint + format
Code formatting and linting are enforced by Ruff. Run `ruff format .` to apply formatting and `ruff check .` to catch lints.
Pre-commit hooks run these automatically; install them with `pre-commit install`.

### 6) Meaningful docstrings
Use Google- or NumPy-style docstrings for public functions.
If a function has input restrictions that cannot be enforced by the type system or linter, document them explicitly. Then either validate inputs in code or ensure that data flows in the repository satisfy them. For stored data that flows into such functions, add tests under `tests/data_assumptions/`.

## Testing Philosophy
This repository uses contract tests and invariant checks rather than unit tests of internal behaviors. Tests live under `tests/`.

Integration/contract tests (in `tests/integration/`) verify that:
- Provider output conforms to canonical schema and can be stored/loaded losslessly.
- Feature pipeline accepts provider data and yields tensors with correct shapes and semantics.
- Rollout simulator accepts feature tensors and returns differentiable scalar losses.
- Training loops can run small experiments end-to-end.

Dataset assumption tests (in `tests/data_assumptions/`) ensure that repository-stored data and configs satisfy all documented preconditions not enforced by the type system. For example, ensure there are no NaNs in a stored returns dataset or that date indices are strictly increasing.

We do not write tests that assert specific numerical outputs of algorithms or the behaviour of internal functions. Performance evaluation and algorithmic results belong in experiment scripts and the paper, not in tests. Avoid tests that encode internal structure choices (for example, asserting a particular LaTeX file hierarchy) when a higher-level contract (such as a successful LaTeX build) can be tested instead.

### Parameterized coverage across registries
When a registry contains multiple implementations that share the same interface (e.g., policies, providers, utilities), prefer parameterized tests to validate each implementation against the same contract. When unit tests are appropriate (boundary/edge behavior is documented and consistent across the registry), parameterize those unit tests across all registered implementations to ensure new entries comply with stated assumptions and restrictions.

## Development Workflow
- Create a feature or bug-fix branch: `feat/<name>` or `fix/<name>`.
- Write code adhering to the design principles.
- Update or add configuration files rather than changing code where possible.
- Run linting (`ruff format`, `ruff check`), type checking (`pyright`), and tests (`pytest`) locally.
- Open a pull request; CI will run the same checks and build the LaTeX paper.

## Pre-commit Hooks
Install and run pre-commit hooks to ensure a clean commit history:
```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

## Questions?
For design, architectural, or scientific questions, please consult the open issues or open a discussion thread. For any missing context about the research questions or experiment setup, see `EXTRA_CONTEXT.md`.
