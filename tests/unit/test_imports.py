import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def test_imports():
    """Test that we can import the necessary modules."""
    from src.main import GameCLI
    assert GameCLI is not None
    
    from years_of_lead.core import GameState
    assert GameState is not None
    
if __name__ == "__main__":
    test_imports()
    print("Imports test passed successfully!") 