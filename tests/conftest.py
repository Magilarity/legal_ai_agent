import os
import sys

# Додаємо корінь проєкту в sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest

import app.document_loader as document_loader_module
import app.text_splitter as text_splitter_module


@pytest.fixture(scope="session")
def loader_module():
    return document_loader_module


@pytest.fixture(scope="session")
def splitter_module():
    return text_splitter_module
