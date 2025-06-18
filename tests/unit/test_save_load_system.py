import os
import sys
import unittest
import json
import shutil
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.main import GameCLI
from src.game.save_manager import SaveManager


class TestSaveLoadSystem(unittest.TestCase):
    """Tests for the save/load system features"""

    def setUp(self):
        """Set up test environment"""
        self.cli = GameCLI()
        self.save_manager = SaveManager()

        # Create test directory for saves
        self.test_save_dir = os.path.join(os.path.dirname(__file__), "test_saves")
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

    def test_save_game_with_metadata(self):
        """Test saving a game with metadata"""
        # Mock game state
        game_state = {
            "turn": 5,
            "date": "1975-03-15",
            "agents": [{"name": "Agent1"}, {"name": "Agent2"}],
            "public_support": 45,
            "resources": 100,
            "locations": [{"name": "Milan", "controlled": True}],
            "factions": [{"name": "Red Brigades", "strength": 30}],
        }

        # Mock the game object
        self.cli.game = MagicMock()
        self.cli.game.to_dict.return_value = game_state

        with patch("builtins.open", mock_open()) as mock_file:
            with patch("json.dump") as mock_json_dump:
                # Call save_game method
                filename = self.save_manager.save_game(self.cli.game, "test_save")

                # Check that file was opened for writing
                mock_file.assert_called_once()

                # Check that json.dump was called with the game state and metadata
                args, _ = mock_json_dump.call_args
                saved_data = args[0]

                # Verify metadata was included
                self.assertIn("metadata", saved_data)
                metadata = saved_data["metadata"]
                self.assertEqual(metadata["turn"], 5)
                self.assertEqual(metadata["date"], "1975-03-15")
                self.assertEqual(metadata["agent_count"], 2)
                self.assertEqual(metadata["public_support"], 45)
                self.assertEqual(metadata["controlled_locations"], 1)

                # Verify game state was included
                self.assertIn("game_state", saved_data)
                self.assertEqual(saved_data["game_state"], game_state)

    def test_load_game(self):
        """Test loading a game"""
        # Create a test save file
        save_data = {
            "metadata": {
                "turn": 5,
                "date": "1975-03-15",
                "agent_count": 2,
                "public_support": 45,
                "controlled_locations": 1,
                "save_type": "manual",
                "timestamp": datetime.now().isoformat(),
            },
            "game_state": {
                "turn": 5,
                "date": "1975-03-15",
                "agents": [{"name": "Agent1"}, {"name": "Agent2"}],
            },
        }

        # Mock the game object
        self.cli.game = MagicMock()

        # Mock open and json.load
        with patch("builtins.open", mock_open(read_data=json.dumps(save_data))):
            with patch("json.load", return_value=save_data):
                # Call load_game method
                self.save_manager.load_game(self.cli, "test_save.json")

                # Check that from_dict was called with the game state
                self.cli.game.from_dict.assert_called_once_with(save_data["game_state"])

    def test_autosave(self):
        """Test autosave functionality"""
        # Mock game state
        game_state = {"turn": 5, "date": "1975-03-15", "agents": [{"name": "Agent1"}]}

        # Mock the game object
        self.cli.game = MagicMock()
        self.cli.game.to_dict.return_value = game_state

        with patch.object(self.save_manager, "save_game") as mock_save:
            # Call autosave method
            self.save_manager.autosave(self.cli.game)

            # Check that save_game was called with autosave prefix
            mock_save.assert_called_once()
            args, _ = mock_save.call_args
            self.assertEqual(args[0], self.cli.game)
            self.assertTrue(args[1].startswith("autosave_"))

    def test_special_save_victory(self):
        """Test special save for victory condition"""
        # Mock game state
        game_state = {"turn": 20, "date": "1976-05-10", "agents": [{"name": "Agent1"}]}

        # Mock the game object
        self.cli.game = MagicMock()
        self.cli.game.to_dict.return_value = game_state

        with patch.object(self.save_manager, "save_game") as mock_save:
            # Call victory_save method
            self.save_manager.victory_save(self.cli.game, "high_support")

            # Check that save_game was called with victory prefix
            mock_save.assert_called_once()
            args, kwargs = mock_save.call_args
            self.assertEqual(args[0], self.cli.game)
            self.assertTrue(args[1].startswith("victory_high_support_"))
            self.assertEqual(kwargs["save_type"], "victory")

    def test_special_save_defeat(self):
        """Test special save for defeat condition"""
        # Mock game state
        game_state = {"turn": 15, "date": "1976-01-20", "agents": []}

        # Mock the game object
        self.cli.game = MagicMock()
        self.cli.game.to_dict.return_value = game_state

        with patch.object(self.save_manager, "save_game") as mock_save:
            # Call defeat_save method
            self.save_manager.defeat_save(self.cli.game, "no_agents")

            # Check that save_game was called with defeat prefix
            mock_save.assert_called_once()
            args, kwargs = mock_save.call_args
            self.assertEqual(args[0], self.cli.game)
            self.assertTrue(args[1].startswith("defeat_no_agents_"))
            self.assertEqual(kwargs["save_type"], "defeat")

    def test_list_saves(self):
        """Test listing save files"""
        # Create test save files
        save_files = [
            "manual_save_20250615.json",
            "autosave_turn10_20250615.json",
            "victory_high_support_20250615.json",
            "defeat_no_agents_20250615.json",
        ]

        # Mock os.listdir
        with patch("os.listdir", return_value=save_files):
            # Call list_saves method
            saves = self.save_manager.list_saves()

            # Check that all save files were returned
            self.assertEqual(len(saves), 4)
            self.assertIn("manual_save_20250615.json", saves)
            self.assertIn("autosave_turn10_20250615.json", saves)
            self.assertIn("victory_high_support_20250615.json", saves)
            self.assertIn("defeat_no_agents_20250615.json", saves)

    def test_get_save_metadata(self):
        """Test retrieving save metadata"""
        # Create a test save file
        save_data = {
            "metadata": {
                "turn": 5,
                "date": "1975-03-15",
                "agent_count": 2,
                "public_support": 45,
                "controlled_locations": 1,
                "save_type": "manual",
                "timestamp": datetime.now().isoformat(),
            },
            "game_state": {
                "turn": 5,
                "date": "1975-03-15",
                "agents": [{"name": "Agent1"}, {"name": "Agent2"}],
            },
        }

        # Mock open and json.load
        with patch("builtins.open", mock_open(read_data=json.dumps(save_data))):
            with patch("json.load", return_value=save_data):
                # Call get_save_metadata method
                metadata = self.save_manager.get_save_metadata("test_save.json")

                # Check that metadata was returned correctly
                self.assertEqual(metadata["turn"], 5)
                self.assertEqual(metadata["date"], "1975-03-15")
                self.assertEqual(metadata["agent_count"], 2)
                self.assertEqual(metadata["public_support"], 45)
                self.assertEqual(metadata["controlled_locations"], 1)
                self.assertEqual(metadata["save_type"], "manual")

    def test_display_save_browser(self):
        """Test displaying save browser"""
        # Create test save files with metadata
        save_files = [
            "manual_save_20250615.json",
            "autosave_turn10_20250615.json",
            "victory_high_support_20250615.json",
            "defeat_no_agents_20250615.json",
        ]

        save_metadata = {
            "manual_save_20250615.json": {
                "turn": 5,
                "date": "1975-03-15",
                "agent_count": 2,
                "public_support": 45,
                "controlled_locations": 1,
                "save_type": "manual",
                "timestamp": "2025-06-15T10:30:00",
            },
            "autosave_turn10_20250615.json": {
                "turn": 10,
                "date": "1975-05-20",
                "agent_count": 3,
                "public_support": 50,
                "controlled_locations": 2,
                "save_type": "autosave",
                "timestamp": "2025-06-15T11:15:00",
            },
            "victory_high_support_20250615.json": {
                "turn": 20,
                "date": "1976-01-10",
                "agent_count": 4,
                "public_support": 75,
                "controlled_locations": 3,
                "save_type": "victory",
                "timestamp": "2025-06-15T14:45:00",
            },
            "defeat_no_agents_20250615.json": {
                "turn": 15,
                "date": "1975-10-05",
                "agent_count": 0,
                "public_support": 30,
                "controlled_locations": 1,
                "save_type": "defeat",
                "timestamp": "2025-06-15T13:20:00",
            },
        }

        # Mock os.listdir and get_save_metadata
        with patch("os.listdir", return_value=save_files):
            with patch.object(
                self.save_manager,
                "get_save_metadata",
                side_effect=lambda x: save_metadata[x],
            ):
                with patch("builtins.print") as mock_print:
                    # Call display_save_browser method
                    self.save_manager.display_save_browser()

                    # Check that print was called for each save file
                    self.assertEqual(
                        mock_print.call_count, len(save_files) + 2
                    )  # +2 for header and footer


if __name__ == "__main__":
    unittest.main()
