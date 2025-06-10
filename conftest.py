import sys, pathlib, os

# ITERATION_028: Add ./src to Python path for all tests
ROOT_DIR = pathlib.Path(__file__).resolve().parent
# Support both monorepo root and when tests are run from subdirectories
SRC_DIR = ROOT_DIR / 'src'
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
    # Verify import works during test collection
    try:
        import importlib
        importlib.import_module('game')
    except ModuleNotFoundError:
        # Fallback: also add absolute path one level up (for unusual layouts)
        ALT = ROOT_DIR.parent / 'src'
        if ALT.exists() and str(ALT) not in sys.path:
            sys.path.insert(0, str(ALT))