import os, sys, pathlib

# ITERATION_028: Ensure test discovery can import the 'game' package from src/
SRC_DIR = pathlib.Path(__file__).resolve().parents[1] / 'src'
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))