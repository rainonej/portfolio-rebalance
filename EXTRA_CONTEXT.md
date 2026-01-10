# Extra Context: Roadmap, Tickets, Dependencies, and Notes

This file contains planning material not suited for the main documentation. It outlines the ticket breakdown, their dependencies, and design notes for the project.

## Ticket list (with dependencies)

### Epic 0 — Scaffold + CI + Paper
- **T0.1**: Create monorepo structure and Python package skeleton (`src/pf`).
- **T0.2**: Add `pyproject.toml` with Ruff/Pyright/Pytest config.
- **T0.3**: Add CI workflows (Python checks + LaTeX build with BibTeX).
- **T0.4**: Add `CONTRIBUTING.md` and tests philosophy docs.
- **T0.5**: Add LaTeX paper skeleton and bibliography.

Depends: none

### Epic 1 — Data pipeline v0 (Stooq only)
- **T1.1**: Canonical schemas and parquet store utilities (`src/pf/data/schemas.py`, `store.py`).
- **T1.2**: Implement `StooqProvider` (prices only) in `src/pf/data/providers/stooq.py`.
- **T1.3**: Implement CLI command `pf data fetch` with config parsing.
- **T1.4**: Integration tests:
  - provider output conforms to schema
  - parquet roundtrip and no data loss
  - dataset invariants: monotonic dates, finite returns, no duplicates

Depends: Epic 0

### Epic 2 — Feature pipeline v0
- **T2.1**: Implement returns computation and rolling statistics features.
- **T2.2**: Implement PCA factor exposures + residual risk (rolling).
- **T2.3**: Implement rolling covariance and covariance-row feature for subset size N.
- **T2.4**: Assemble tokens and validate feature tables.
- **T2.5**: Integration tests:
  - features are computed with past-only data (no leakage)
  - token shapes and types are correct

Depends: Epic 1

### Epic 3 — Modeling and training v0
- **T3.1**: Build differentiable rollout simulator (zero transaction cost).
- **T3.2**: Implement constraint interface and simplex projection.
- **T3.3**: Implement utility interface and semivariance utility.
- **T3.4**: Implement baseline MLP policy supporting optional identity embeddings.
- **T3.5**: Implement foundation trainer (subset sampling) with checkpointing.
- **T3.6**: Implement fine-tune trainer (fixed subset) with optional trainable identity embeddings.
- **T3.7**: Implement evaluation harness, metrics, and plots (saving artifacts for the paper).
- **T3.8**: Add an end-to-end smoke test: run a tiny training session on toy data.

Depends: Epic 2

### Epic 4 — Experiments and paper v0
- **T4.1**: Implement holdout protocols for time and asset generalization.
- **T4.2**: Write the Method section aligned to code modules.
- **T4.3**: Write the Experiments section describing setups and baselines.
- **T4.4**: Produce Results and Ablations section:
  - Covariance-row ablation
  - Scratch vs pretrained fine-tune
  - Identity embedding ablation (optional)

Depends: Epic 3

### Epic 5 — Model upgrade v1 (future)
- **T5.1**: Implement Set Transformer policy (permutation-equivariant).
- **T5.2**: Run ablation: compare MLP vs Set Transformer.
- **T5.3**: Update the paper with architecture and scaling discussion.

Depends: Epic 3

## Notes

### Why covariance-row features
Correlation structure is central to diversification. Including a covariance-row per asset within the subset provides explicit cross-asset context beyond what per-asset rolling statistics can carry. The ablation experiment will test whether this improves risk control and generalization.

### Why identity embeddings are optional
Identity embeddings allow the model to learn persistent asset-specific patterns but risk overfitting and reduce generalization to unseen assets. Our experimental design explicitly compares policies trained without identity to those fine-tuned with identity.

## Future extensions (not in v0)
- Use Set Transformer architecture to better handle unordered asset sets.
- Incorporate CVaR and drawdown penalties in the utility function.
- Add transaction costs and turnover penalties (with smoothing to maintain differentiability).
- Extend provider support to additional sources (yfinance, Schwab, Finnhub, CoinGecko).
- Test more robust covariance estimation methods (shrinkage, factor models).
