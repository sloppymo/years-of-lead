"""
Pytest configuration file for Years of Lead tests

This file sets up the Python path so that tests can import from the src directory.
"""

import sys
from pathlib import Path
import pytest

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from game.core import GameState

# ---------------------------------------------------------------------------
# Reusable fixtures for game tests
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def game_state() -> GameState:
    """Return a fully initialised GameState instance for use in tests."""
    gs = GameState()
    gs.initialize_game()
    return gs


@pytest.fixture()
def two_agents(game_state):
    """Return a tuple with two distinct agent IDs from the initialised game state."""
    agent_ids = list(game_state.agents.keys())
    if len(agent_ids) < 2:
        pytest.skip("Not enough agents initialised for relationship tests")
    return agent_ids[0], agent_ids[1]
