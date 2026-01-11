from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--long",
        action="store_true",
        default=False,
        help="Run long tests that hit external data providers.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "long: external provider tests")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--long"):
        return
    skip_long = pytest.mark.skip(reason="need --long option to run")
    for item in items:
        if "long" in item.keywords:
            item.add_marker(skip_long)
