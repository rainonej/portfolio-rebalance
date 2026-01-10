# Paper

This directory contains the LaTeX source for the accompanying research paper.

## Building the Paper
From the `paper/` directory, run the following command to compile the PDF with citations:
```bash
latexmk -pdf -bibtex -interaction=nonstopmode -halt-on-error main.tex
```

This will create `main.pdf` in the current directory. Note that the generated PDF is ignored by git; CI will build the PDF on every push and upload it as an artifact.

## Directory Structure
- `main.tex` — Top-level LaTeX file that includes section files and the bibliography.
- `macros.tex` — Custom macros and preamble settings (packages, commands).
- `sections/` — Individual section files split by logical topic.
- `refs.bib` — BibTeX database for citations.
- `figures/` and `tables/` — Placeholders for generated figures and tables (the code under `src/pf/` should write results to `artifacts/reports/` and scripts may copy them into these directories).

## Compilation in CI
The GitHub Actions workflow defined in `.github/workflows/ci.yml` automatically runs latexmk with bibtex to build the paper and uploads it as an artifact. If the build fails, ensure that all referenced files exist and compile locally before pushing.
