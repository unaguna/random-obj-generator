import os
from pathlib import Path

import pytest


@pytest.fixture
def resources():
    return Path(os.path.dirname(__file__), "tests/resources")
