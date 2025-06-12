#!/usr/bin/env python3
"""
Years of Lead - Main Game Entry Point
"""

import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Now import after path setup
from main import main

if __name__ == "__main__":
    main()
