from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.mark.skipif(shutil.which("latexmk") is None, reason="latexmk not installed")
def test_paper_builds_pdf() -> None:
    root = Path(__file__).resolve().parents[1]
    paper_dir = root / "paper"
    main_tex = paper_dir / "main.tex"
    assert main_tex.exists(), "paper/main.tex is required to build the PDF"

    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)
        command = [
            "latexmk",
            "-pdf",
            "-bibtex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={output_dir}",
            f"-auxdir={output_dir}",
            "main.tex",
        ]
        subprocess.run(command, cwd=paper_dir, check=True, capture_output=True, text=True)
        assert (output_dir / "main.pdf").exists(), "PDF output was not generated"
