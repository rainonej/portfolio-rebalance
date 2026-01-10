from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "relative_path",
    [
        "paper/main.tex",
        "paper/macros.tex",
        "paper/refs.bib",
        "paper/sections/01_introduction.tex",
        "paper/sections/02_related_work.tex",
        "paper/sections/03_method.tex",
        "paper/sections/04_experiments.tex",
        "paper/sections/05_results.tex",
        "paper/sections/06_conclusion.tex",
    ],
)
def test_paper_files_exist(relative_path: str) -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / relative_path
    assert target.exists(), f"Missing expected paper file: {relative_path}"


def test_main_includes_sections() -> None:
    root = Path(__file__).resolve().parents[1]
    main_tex = (root / "paper/main.tex").read_text(encoding="utf-8")
    for section in [
        "sections/01_introduction",
        "sections/02_related_work",
        "sections/03_method",
        "sections/04_experiments",
        "sections/05_results",
        "sections/06_conclusion",
    ]:
        assert f"\\input{{{section}}}" in main_tex
