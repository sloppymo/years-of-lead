import sys, pathlib, os

# ITERATION_028: Add ./src to Python path for all tests
ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / 'src'
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))