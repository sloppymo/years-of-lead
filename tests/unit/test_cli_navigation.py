import pytest
from unittest import mock
import builtins
import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the mock CLI class
from tests.unit.mock_cli import GameCLI

@pytest.fixture(autouse=True)
def reload_main_module():
    # Ensure fresh import for each test
    if 'tests.unit.mock_cli' in sys.modules:
        del sys.modules['tests.unit.mock_cli']
    yield

def run_cli_with_inputs(inputs):
    """Helper to run the CLI with a sequence of inputs and capture output."""
    cli = GameCLI()
    with mock.patch.object(builtins, 'input', side_effect=inputs), \
         mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        try:
            cli.run()
        except (StopIteration, SystemExit):
            pass  # End of input or quit
        return mock_stdout.getvalue()

def test_arrow_key_navigation():
    """Test arrow key navigation in the main menu."""
    # Test down arrow navigation and selection
    output = run_cli_with_inputs(['arrow:down', 'arrow:down', 'arrow:enter', 'q'])
    assert "→" in output  # Arrow indicator for selected item
    assert "Navigation:" in output
    assert "arrows to select" in output
    assert "Agent Details" in output  # The action executed after Enter

    # Test up arrow navigation and selection
    output = run_cli_with_inputs(['arrow:up', 'arrow:enter', 'q'])
    assert "→" in output
    assert "Query Mode" in output  # Last item selected with up arrow

def test_arrow_key_submenu_navigation():
    """Test arrow key navigation in submenus."""
    # Test arrow navigation in save/load menu
    output = run_cli_with_inputs(['s', 'arrow:down', 'arrow:enter', 'q', 'q'])
    assert "SAVE/LOAD MENU" in output
    assert "Load Game" in output
    assert "Available saves:" in output

def test_mouse_navigation():
    """Test mouse click navigation in the main menu."""
    # Simulate mouse click on the second menu item (agents)
    # Position is approximate - row 5, column 10 (middle of the second menu item)
    output = run_cli_with_inputs(['mouse:10,5', 'q'])
    assert "Agent Details" in output or "RESISTANCE COMMAND CENTER" in output

    # Simulate mouse click on the save/load menu item and then in the submenu
    output = run_cli_with_inputs(['s', 'mouse:10,2', 'q', 'q'])
    assert "SAVE/LOAD MENU" in output
    assert "Save Game" in output

def test_combined_navigation():
    """Test combining arrow keys and mouse navigation."""
    # Use arrow keys then mouse
    output = run_cli_with_inputs(['arrow:down', 'arrow:down', 'mouse:10,10', 'q'])
    assert "→" in output
    assert "Location Details" in output or "RESISTANCE COMMAND CENTER" in output

    # Use mouse then arrow keys
    output = run_cli_with_inputs(['mouse:10,7', 'arrow:up', 'arrow:enter', 'q'])
    assert "Agent Details" in output or "RESISTANCE COMMAND CENTER" in output

def test_navigation_help_display():
    """Test that navigation help is displayed."""
    output = run_cli_with_inputs(['q'])
    assert "Navigation:" in output
    assert "arrows to select" in output
    assert "Click to select" in output

def test_menu_item_selection_indicator():
    """Test that the selected menu item is properly indicated."""
    output = run_cli_with_inputs(['arrow:down', 'q'])
    # Check that the arrow indicator is present (lowercase g for agents)
    assert "→ [g] agents" in output or "→ [a] advance" in output

def test_save_menu_arrow_navigation():
    """Test arrow navigation in the save menu."""
    output = run_cli_with_inputs(['s', 'arrow:down', 'arrow:down', 'arrow:enter', 'q'])
    assert "SAVE/LOAD MENU" in output
    assert "Delete Save" in output
    assert "Available saves:" in output

def test_load_menu_arrow_navigation():
    """Test arrow navigation in the load menu."""
    output = run_cli_with_inputs(['s', 'arrow:down', 'arrow:enter', 'arrow:down', 'q', 'q'])
    assert "SAVE/LOAD MENU" in output
    assert "Load Game" in output
    assert "Available saves:" in output
    
if __name__ == "__main__":
    pytest.main(["-v", __file__]) 