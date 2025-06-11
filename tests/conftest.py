"""
Pytest configuration file for Years of Lead tests

This file sets up the Python path so that tests can import from the src directory.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))