"""
Runs tests via pytest. Invoke using `python -m potluck.tests`.

tests/__main__.py
"""

import sys

import pytest

sys.exit(pytest.main(["--pyargs", "potluck.tests"]))
