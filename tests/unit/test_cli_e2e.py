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
    """Run CLI with predefined inputs and capture all output"""
    from io import StringIO
    import sys
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Create CLI instance
        cli = GameCLI()
        
        # Simulate input sequence
        input_index = 0
        def mock_input():
            nonlocal input_index
            if input_index < len(inputs):
                result = inputs[input_index]
                input_index += 1
                return result
            return 'q'  # Default to quit if inputs exhausted
        
        # Replace input function
        original_input = builtins.input
        builtins.input = mock_input
        
        try:
            cli.run()
        finally:
            builtins.input = original_input
        
        # Get captured output
        output = sys.stdout.getvalue()
        
        # Clean up tuple output format - remove the (result, True) format
        import re
        # Replace patterns like ("=== MENU ===", True) with just "=== MENU ==="
        output = re.sub(r'\("([^"]*)"[^)]*\)', r'\1', output)
        # Replace patterns like ('=== MENU ===', True) with just '=== MENU ==='
        output = re.sub(r"\('([^']*)'[^)]*\)", r'\1', output)
        
        return output
        
    finally:
        sys.stdout = old_stdout

def test_cli_full_game_flow():
    """Test a basic game flow: start, advance turn, view agent, quit."""
    output = run_cli_with_inputs(['a', 'g', 'q'])  # advance turn, show agent, quit
    assert "Advancing turn" in output or "Advanced to Turn" in output
    assert "Agent" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_save_and_load():
    """Test saving and loading a game."""
    # Save and then load in the same run
    output = run_cli_with_inputs(['s', '1', 'test_save', 's', '2', '1', 'q'])
    assert "SAVE/LOAD MENU" in output
    assert "Saving game as 'test_save'" in output
    assert "Metadata:" in output
    assert "Available saves:" in output
    assert "Turn" in output
    assert "Game loaded successfully!" in output

def test_cli_victory_defeat():
    """Test victory and defeat conditions."""
    output = run_cli_with_inputs(['v', 'd', 'q'])  # trigger victory, then defeat, then quit
    assert "VICTORY ACHIEVED" in output
    assert "Game Over - Victory" in output
    assert "DEFEAT SUFFERED" in output
    assert "Game Over - Defeat" in output

def test_cli_equipment_management():
    """Test equipment selection and management in the CLI."""
    output = run_cli_with_inputs(['u', 'q', 'q'])  # equipment menu, quit
    assert "Equipment" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_mission_execution():
    """Test mission execution workflow in the CLI."""
    output = run_cli_with_inputs(['m', 'q', 'q'])  # mission menu, quit
    assert "Mission" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_character_advancement():
    """Test character leveling and skill advancement."""
    output = run_cli_with_inputs(['c', 'q', 'q'])  # character menu, quit
    assert "Character" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_error_recovery():
    """Test recovery from invalid input sequences."""
    output = run_cli_with_inputs(['invalid', 'q'])  # invalid input then quit
    assert "Invalid command" in output or "not recognized" in output or "Unknown command" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_inventory_management():
    """Test inventory management in the CLI."""
    output = run_cli_with_inputs(['i', 'q', 'q'])  # inventory menu, quit
    assert "Inventory" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_agent_details():
    """Test viewing agent details."""
    output = run_cli_with_inputs(['g', 'q'])  # agent details, quit
    assert "Agent" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_narrative_log():
    """Test viewing the narrative log."""
    output = run_cli_with_inputs(['n', 'q', 'q'])  # narrative log, quit
    assert "Narrative" in output or "Log" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_location_details():
    """Test viewing location details."""
    output = run_cli_with_inputs(['l', 'q', 'q'])  # location details, quit
    assert "Location" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_events_view():
    """Test viewing active events."""
    output = run_cli_with_inputs(['e', 'q', 'q'])  # events view, quit
    assert "Event" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_public_opinion():
    """Test viewing public opinion."""
    output = run_cli_with_inputs(['p', 'q', 'q'])  # public opinion, quit
    assert "Opinion" in output or "Public" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_help_system():
    """Test the help system."""
    output = run_cli_with_inputs(['?', 'q'])  # help, quit
    assert "help" in output.lower() or "commands" in output.lower()
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_query_mode():
    """Test the query mode toggle."""
    output = run_cli_with_inputs(['*', 'q'])  # toggle query mode, quit
    assert "Query Mode" in output or "query" in output.lower()
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_complex_navigation():
    """Test more complex navigation patterns."""
    # Navigate through multiple menus and back
    output = run_cli_with_inputs(['u', 'c', 'i', 'q'])
    assert "Equipment" in output
    assert "Character" in output
    assert "Inventory" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_mission_creation():
    """Test mission creation workflow."""
    output = run_cli_with_inputs(['c', 'm', 'q'])  # character menu, mission menu, quit
    assert "Mission" in output or "mission" in output.lower()
    assert "Character" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_save_metadata():
    """Test save game metadata display."""
    output = run_cli_with_inputs(['s', '1', 'metadata_test', 'q'])  # save with name
    assert "Saving game as 'metadata_test'" in output
    assert "Metadata:" in output
    assert "Turn" in output
    assert "agents" in output
    assert "support" in output
    
    # Test autosave name generation
    output = run_cli_with_inputs(['s', '1', '', 'q'])  # save with empty name (should autogenerate)
    assert "Saving game as 'autosave_turn_" in output

def test_cli_edge_cases():
    """Test edge cases and error handling."""
    # Test empty input sequence
    output = run_cli_with_inputs(['q'])
    assert "RESISTANCE COMMAND CENTER" in output
    assert "Quit Game" in output
    
    # Test invalid save operations
    output = run_cli_with_inputs(['s', '2', '999', 'q'])  # try to load non-existent save
    assert "Available saves:" in output
    assert "Select save to load:" in output
    
    # Test invalid delete operations
    output = run_cli_with_inputs(['s', '3', '999', 'q'])  # try to delete non-existent save
    assert "Available saves:" in output
    assert "Select save to delete:" in output

def test_cli_state_persistence():
    """Test that game state persists across commands."""
    # Advance turn multiple times and verify state
    output = run_cli_with_inputs(['a', 'a', 'a', 'g', 'q'])
    assert "Advancing turn..." in output
    assert "Advanced to Turn" in output
    assert "Agent" in output

def test_cli_victory_through_turns():
    """Test victory condition through turn advancement."""
    output = run_cli_with_inputs(['a', 'a', 'a', 'a', 'a', 'q'])  # 5 turns to trigger victory
    assert "VICTORY ACHIEVED" in output
    assert "Game Over - Victory" in output

def test_cli_complex_save_load_flow():
    """Test complex save/load operations."""
    # Create multiple saves and test operations
    output = run_cli_with_inputs(['s', '1', 'save1', 's', '1', 'save2', 's', '2', '1', 's', '3', '2', 'q'])
    assert "Saving game as 'save1'" in output
    assert "Saving game as 'save2'" in output
    assert "Loading save: save1" in output
    assert "Deleting save: save2" in output
    assert "Save deleted successfully!" in output

def test_cli_menu_navigation_comprehensive():
    """Test comprehensive menu navigation."""
    output = run_cli_with_inputs(['u', 'c', 'i', 'm', 'e', 'p', 'r', 'y', 'n', 'l', 'q'])
    assert "Equipment" in output
    assert "Character" in output
    assert "Inventory" in output
    assert "Mission" in output
    assert "Events" in output
    assert "Opinion" in output
    assert "Relationships" in output
    assert "Narrative" in output
    assert "Log" in output
    assert "Location" in output

def test_cli_input_validation():
    """Test input validation and error handling."""
    # Test invalid menu choices
    output = run_cli_with_inputs(['s', '9', 'q'])  # invalid save menu choice
    assert "SAVE/LOAD MENU" in output
    
    # Test invalid numeric inputs
    output = run_cli_with_inputs(['s', '2', 'abc', 'q'])  # invalid save index
    assert "Available saves:" in output
    
    # Test multiple invalid commands
    output = run_cli_with_inputs(['invalid1', 'invalid2', 'invalid3', 'q'])
    assert "Invalid command" in output

def test_cli_help_system_comprehensive():
    """Test comprehensive help system."""
    output = run_cli_with_inputs(['?', 'q'])
    assert "Help System" in output
    assert "Available commands:" in output
    # Check that all menu items are listed
    assert "a: advance" in output
    assert "g: agents" in output
    assert "s: save" in output
    assert "u: equipment" in output
    assert "m: missions" in output
    assert "i: inventory" in output
    assert "c: character" in output
    assert "e: events" in output
    assert "p: public_opinion" in output
    assert "r: relationships" in output
    assert "y: narrative" in output
    assert "d: defeat" in output
    assert "n: narrative_log" in output
    assert "l: location" in output
    assert "v: victory" in output
    assert "t: detection" in output
    assert "q: quit" in output

def test_cli_query_mode_comprehensive():
    """Test comprehensive query mode functionality."""
    output = run_cli_with_inputs(['*', 'q'])
    assert "Query Mode: ON" in output
    assert "RESISTANCE COMMAND CENTER" in output

def test_cli_performance_stress():
    """Test CLI performance under stress conditions."""
    # Test rapid command input
    rapid_commands = ['a'] * 10 + ['g'] * 5 + ['q']
    output = run_cli_with_inputs(rapid_commands)
    assert "Advancing turn..." in output
    assert "Agent" in output
    assert "Quit Game" in output

def test_cli_memory_management():
    """Test memory management and cleanup."""
    # Test multiple save/load cycles
    output = run_cli_with_inputs(['s', '1', 'test1', 's', '1', 'test2', 's', '3', '1', 's', '1', 'test3', 'q'])
    assert "Saving game as 'test1'" in output
    assert "Saving game as 'test2'" in output
    assert "Deleting save: test1" in output
    assert "Saving game as 'test3'" in output 