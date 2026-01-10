# Tests

## Purpose
Tests in this repository serve to validate contracts between modules and invariant properties of stored data and configurations. They are not intended to verify implementation details or numerical results of algorithms.

## Why this philosophy?
The goal is to keep the codebase modular and flexible. Tests should ensure that modules can interact correctly and that assumptions documented in docstrings are satisfied by the data flowing through the system. They should not lock in specific behaviors, allowing researchers to experiment with alternative algorithms and architectures without rewriting tests.

## Test Categories

### 1) Integration / Contract Tests (`tests/integration/`)
These tests confirm that independent modules can communicate using the prescribed interfaces and schemas. Examples:
- Provider → Schema → Store Roundtrip: Fetch data from a provider, validate against the canonical schema, store to parquet, and read back without loss.
- Feature Pipeline Compatibility: Ensure that the feature pipeline accepts stored returns and produces valid token tables with appropriate shapes and no leakage (past-only).
- Rollout Simulator Contract: Confirm that the simulator accepts the token tables and returns differentiable scalar losses.
- Training Loop Smoke Test: Run a tiny training loop using toy data and a simple model to ensure the entire pipeline executes without error.

### 2) Data Assumption Tests (`tests/data_assumptions/`)
When a function’s docstring imposes input restrictions that are not statically enforced (e.g., “dates must be strictly increasing” or “returns must be finite”), and data is stored in this repo that flows into that function, we add a test to ensure the stored data satisfies those assumptions.

These tests automatically guard against silent breakage if a future contributor introduces a dataset that violates documented assumptions.

## Test Design Guidance
- Prefer tests that validate externally observable behavior (contracts, invariants, or successful end-to-end execution).
- Avoid tests that encode internal structure choices (for example, asserting a particular LaTeX file hierarchy). For the paper, prefer a compile check rather than checking for specific inputs.

## Running Tests
To execute the test suite, run:
```bash
pytest
```

Optional flags such as `-n auto` can be passed to run tests in parallel if `pytest-xdist` is installed.

## Adding Tests
When adding new data files, configurations, or modules, consider the following:
- Does the new data respect the documented assumptions of functions it feeds into? If not, update the assumptions, enforce them in code, or add a test.
- Do new module interfaces need a contract test? Write a minimal integration test to exercise the happy path.
- Avoid writing tests that assert exact numerical outputs or algorithmic outcomes. Those belong in experiments and should be documented in reports and the paper.
