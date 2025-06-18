import os
import sys
import unittest
import shutil
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import GameCLI, MenuItem
from src.game.core import GameState
from src.game.save_manager import SaveManager

class TestIntegratedFeatures(unittest.TestCase):
    """Integration tests for all three features working together"""
    
    def setUp(self):
        """Set up test environment"""
        self.cli = GameCLI()
        self.game = GameState()
        self.cli.game = self.game
        self.save_manager = SaveManager()
        
        # Create test directory for saves
        self.test_save_dir = os.path.join(os.path.dirname(__file__), 'test_saves')
        if not os.path.exists(self.test_save_dir):
            os.makedirs(self.test_save_dir)
            
        # Set save directory for tests
        self.original_save_dir = self.save_manager.save_directory
        self.save_manager.save_directory = self.test_save_dir
        
    def tearDown(self):
        """Clean up after tests"""
        # Restore original save directory
        self.save_manager.save_directory = self.original_save_dir
        
        # Remove test save directory
        if os.path.exists(self.test_save_dir):
            shutil.rmtree(self.test_save_dir)
    
    def test_navigation_to_save_game(self):
        """Test navigating to and using the save game feature"""
        # Set up menu items
        self.cli.current_menu_items = [
            MenuItem("a", "advance", "Advance Turn", lambda: "advance"),
            MenuItem("s", "save", "Save Game", lambda: "save"),
            MenuItem("q", "quit", "Quit Game", lambda: "quit")
        ]
        self.cli.selected_index = 0
        self.cli.current_menu_items[0].selected = True
        
        # Mock input to navigate to save game option
        inputs = ["arrow:down", "arrow:enter", "test_save", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'save_game') as mock_save_game:
                            # Run the CLI
                            self.cli.run()
                            
                            # Check that save_game was called
                            mock_save_game.assert_called_once_with("test_save")
    
    def test_navigation_to_load_game(self):
        """Test navigating to and using the load game feature"""
        # Set up menu items
        self.cli.current_menu_items = [
            MenuItem("a", "advance", "Advance Turn", lambda: "advance"),
            MenuItem("l", "load", "Load Game", lambda: "load"),
            MenuItem("q", "quit", "Quit Game", lambda: "quit")
        ]
        self.cli.selected_index = 0
        self.cli.current_menu_items[0].selected = True
        
        # Create a test save file
        save_files = ["test_save.json"]
        
        # Mock input to navigate to load game option
        inputs = ["arrow:down", "arrow:enter", "1", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch('os.listdir', return_value=save_files):
                            with patch.object(self.cli, 'load_game') as mock_load_game:
                                # Run the CLI
                                self.cli.run()
                                
                                # Check that load_game was called
                                mock_load_game.assert_called_once_with("test_save.json")
    
    def test_mouse_navigation_to_progress_tracking(self):
        """Test using mouse navigation to view progress tracking"""
        # Set up menu items with positions
        self.cli.current_menu_items = [
            MenuItem("a", "advance", "Advance Turn", lambda: "advance"),
            MenuItem("p", "progress", "View Progress", lambda: "progress"),
            MenuItem("q", "quit", "Quit Game", lambda: "quit")
        ]
        self.cli.current_menu_items[0].position = (4, 2)
        self.cli.current_menu_items[1].position = (5, 2)
        self.cli.current_menu_items[2].position = (6, 2)
        self.cli.selected_index = 0
        self.cli.current_menu_items[0].selected = True
        
        # Mock input to use mouse click on progress option
        inputs = ["mouse:2,5", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'display_progress_tracking') as mock_progress:
                            # Run the CLI
                            self.cli.run()
                            
                            # Check that display_progress_tracking was called
                            mock_progress.assert_called_once()
    
    def test_victory_condition_with_save(self):
        """Test victory condition triggering with automatic save"""
        # Set up game state for victory
        self.game.public_support = 75  # Above threshold for victory
        
        # Mock the save manager
        self.cli.save_manager = MagicMock()
        
        # Mock input for advancing turn
        inputs = ["a", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'check_victory_conditions', return_value=True):
                            with patch.object(self.cli, 'display_victory_screen') as mock_victory:
                                # Run the CLI
                                self.cli.run()
                                
                                # Check that victory screen was displayed
                                mock_victory.assert_called_once()
                                
                                # Check that victory save was created
                                self.cli.save_manager.victory_save.assert_called_once()
    
    def test_defeat_condition_with_save(self):
        """Test defeat condition triggering with automatic save"""
        # Set up game state for defeat
        self.game.public_support = 10  # Below threshold for defeat
        
        # Mock the save manager
        self.cli.save_manager = MagicMock()
        
        # Mock input for advancing turn
        inputs = ["a", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'check_victory_conditions', return_value=False):
                            with patch.object(self.cli, 'check_defeat_conditions', return_value=True):
                                with patch.object(self.cli, 'display_defeat_screen') as mock_defeat:
                                    # Run the CLI
                                    self.cli.run()
                                    
                                    # Check that defeat screen was displayed
                                    mock_defeat.assert_called_once()
                                    
                                    # Check that defeat save was created
                                    self.cli.save_manager.defeat_save.assert_called_once()
    
    def test_autosave_after_turn_advance(self):
        """Test autosave triggering after turn advancement"""
        # Mock the save manager
        self.cli.save_manager = MagicMock()
        
        # Mock input for advancing turn
        inputs = ["a", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'check_victory_conditions', return_value=False):
                            with patch.object(self.cli, 'check_defeat_conditions', return_value=False):
                                with patch.object(self.cli, 'advance_turn'):
                                    # Run the CLI
                                    self.cli.run()
                                    
                                    # Check that autosave was called
                                    self.cli.save_manager.autosave.assert_called_once_with(self.game)
    
    def test_save_load_cycle_preserves_game_state(self):
        """Test that saving and loading preserves the game state"""
        # Set up initial game state
        self.game.turn = 5
        self.game.date = "1975-03-15"
        self.game.public_support = 45
        self.game.resources = 100
        
        # Create a save file
        save_data = {
            "metadata": {
                "turn": 5,
                "date": "1975-03-15",
                "agent_count": 2,
                "public_support": 45,
                "controlled_locations": 1,
                "save_type": "manual",
                "timestamp": datetime.now().isoformat()
            },
            "game_state": {
                "turn": 5,
                "date": "1975-03-15",
                "public_support": 45,
                "resources": 100,
                "agents": [{"name": "Agent1"}, {"name": "Agent2"}]
            }
        }
        
        # Mock save and load operations
        with patch('builtins.open', mock_open()):
            with patch('json.dump'):
                with patch('json.load', return_value=save_data):
                    # Save the game
                    self.save_manager.save_game(self.game, "test_save")
                    
                    # Modify the game state
                    self.game.turn = 6
                    self.game.public_support = 50
                    
                    # Load the game
                    self.save_manager.load_game(self.cli, "test_save.json")
                    
                    # Check that the game state was restored
                    self.assertEqual(self.game.turn, 5)
                    self.assertEqual(self.game.date, "1975-03-15")
                    self.assertEqual(self.game.public_support, 45)
                    self.assertEqual(self.game.resources, 100)

if __name__ == "__main__":
    unittest.main() 