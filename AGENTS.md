# Agent Guidelines

This repository emphasizes configuration-driven experiments, contract-style tests, and documented assumptions.

Before making changes:
- Read `README.md` for project overview and repository structure.
- Follow design and testing guidance in `CONTRIBUTING.md`.
- Review testing expectations in `tests/README.md`.
- Use `EXTRA_CONTEXT.md` for the ticket roadmap and dependencies.

When adding tests:
- Prefer contract/invariant or end-to-end checks over tests that encode internal structure.
- Parameterize tests across registry implementations when multiple entries share an interface.

Paper build:
- The LaTeX sources live in `paper/`. Build instructions are in `paper/README.md`.
