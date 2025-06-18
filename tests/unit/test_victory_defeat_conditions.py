import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import GameCLI
from src.game.core import GameState
from tests.unit.mock_game import MockGame
from tests.unit.mock_save_manager import MockSaveManager

class TestVictoryDefeatConditions(unittest.TestCase):
    """Tests for the victory/defeat conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_game = MockGame()
        self.mock_save_manager = MockSaveManager()
        self.cli = GameCLI()
        self.cli.game = self.mock_game
        self.cli.save_manager = self.mock_save_manager
        
    def test_victory_condition_met(self):
        """Test victory condition detection"""
        # Set up victory conditions
        self.mock_game.victory_conditions = {
            "faction_control": {"resistance": 0.8},
            "agent_survival": 0.7,
            "mission_success": 0.6
        }
        
        # Mock game state to meet victory conditions
        self.mock_game.factions = {
            "resistance": MagicMock(control_level=0.85),
            "student_movement": MagicMock(control_level=0.3)
        }
        self.mock_game.agents = [MagicMock(status="active") for _ in range(7)]
        self.mock_game.total_agents = 10
        self.mock_game.mission_success_rate = 0.65
        
        # Test victory detection
        result = self.cli.check_victory_conditions()
        self.assertTrue(result["victory_achieved"])
        self.assertEqual(result["victory_type"], "faction_control")
        
    def test_defeat_condition_met(self):
        """Test defeat condition detection"""
        # Set up defeat conditions
        self.mock_game.defeat_conditions = {
            "agent_survival": 0.3,
            "faction_control": {"resistance": 0.1},
            "time_limit": 50
        }
        
        # Mock game state to meet defeat conditions
        self.mock_game.agents = [MagicMock(status="active") for _ in range(2)]
        self.mock_game.total_agents = 10
        self.mock_game.factions = {
            "resistance": MagicMock(control_level=0.05)
        }
        self.mock_game.turn = 55
        
        # Test defeat detection
        result = self.cli.check_defeat_conditions()
        self.assertTrue(result["defeat_occurred"])
        self.assertEqual(result["defeat_type"], "agent_survival")
        
    def test_progress_tracking(self):
        """Test progress tracking for victory/defeat conditions"""
        # Set up conditions
        self.mock_game.victory_conditions = {
            "faction_control": {"resistance": 0.8},
            "agent_survival": 0.7
        }
        
        # Mock current state
        self.mock_game.factions = {
            "resistance": MagicMock(control_level=0.6)
        }
        self.mock_game.agents = [MagicMock(status="active") for _ in range(6)]
        self.mock_game.total_agents = 10
        
        # Test progress calculation
        progress = self.cli.calculate_victory_progress()
        
        self.assertIn("faction_control", progress)
        self.assertIn("agent_survival", progress)
        self.assertEqual(progress["faction_control"]["resistance"], 0.75)  # 0.6/0.8
        self.assertEqual(progress["agent_survival"], 0.857)  # 6/7
        
    def test_game_over_screen_victory(self):
        """Test victory game over screen"""
        victory_data = {
            "victory_achieved": True,
            "victory_type": "faction_control",
            "narrative": "The resistance has achieved control!"
        }
        
        with patch('builtins.print') as mock_print:
            self.cli.display_game_over_screen(victory_data)
            mock_print.assert_called()
        
    def test_game_over_screen_defeat(self):
        """Test defeat game over screen"""
        defeat_data = {
            "defeat_occurred": True,
            "defeat_type": "agent_survival",
            "narrative": "Too many agents have been lost."
        }
        
        with patch('builtins.print') as mock_print:
            self.cli.display_game_over_screen(defeat_data)
            mock_print.assert_called()
        
    def test_save_on_victory_defeat(self):
        """Test automatic save on victory/defeat"""
        victory_data = {
            "victory_achieved": True,
            "victory_type": "faction_control"
        }
        
        with patch.object(self.cli, 'save_manager') as mock_save_manager:
            self.cli.handle_game_over(victory_data)
            mock_save_manager.save_special.assert_called_once()
        
    def test_continue_after_victory_defeat(self):
        """Test option to continue after victory/defeat"""
        victory_data = {
            "victory_achieved": True,
            "victory_type": "faction_control"
        }
        
        with patch('builtins.input', return_value='y'):
            with patch.object(self.cli, 'continue_game') as mock_continue:
                self.cli.handle_game_over(victory_data)
                mock_continue.assert_called_once()

if __name__ == "__main__":
    unittest.main() 