"""
Mock SaveManager class for testing purposes.
"""
import os
from datetime import datetime


class MockSaveManager:
    """Mock version of SaveManager for testing"""

    def __init__(self):
        """Initialize the mock save manager"""
        self.save_directory = os.path.join(os.path.dirname(__file__), "test_saves")
        self.saves = {}  # Dictionary to store "saved" games
        self.metadata = {}  # Dictionary to store save metadata

    def save_game(self, game, filename, save_type="manual"):
        """Mock saving a game"""
        # Create a unique filename if one is not provided
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        # Extract metadata from game state
        game_state = game.to_dict() if hasattr(game, "to_dict") else {}
        metadata = {
            "turn": game_state.get("turn", 0),
            "date": game_state.get("date", "1975-01-01"),
            "agent_count": len(game_state.get("agents", [])),
            "public_support": game_state.get("public_support", 0),
            "controlled_locations": sum(
                1
                for loc in game_state.get("locations", [])
                if loc.get("controlled", False)
            ),
            "save_type": save_type,
            "timestamp": datetime.now().isoformat(),
        }

        # Store the save data
        self.saves[filename] = {"metadata": metadata, "game_state": game_state}
        self.metadata[filename] = metadata

        return filename

    def load_game(self, cli, filename):
        """Mock loading a game"""
        if filename in self.saves:
            game_state = self.saves[filename]["game_state"]
            if hasattr(cli.game, "from_dict"):
                cli.game.from_dict(game_state)
            return True
        return False

    def autosave(self, game):
        """Mock autosave functionality"""
        turn = game.turn if hasattr(game, "turn") else 0
        filename = f"autosave_turn{turn}_{datetime.now().strftime('%Y%m%d')}.json"
        return self.save_game(game, filename, save_type="autosave")

    def victory_save(self, game, victory_type):
        """Mock victory save functionality"""
        filename = f"victory_{victory_type}_{datetime.now().strftime('%Y%m%d')}.json"
        return self.save_game(game, filename, save_type="victory")

    def defeat_save(self, game, defeat_type):
        """Mock defeat save functionality"""
        filename = f"defeat_{defeat_type}_{datetime.now().strftime('%Y%m%d')}.json"
        return self.save_game(game, filename, save_type="defeat")

    def list_saves(self):
        """Mock listing save files"""
        return list(self.saves.keys())

    def get_save_metadata(self, filename):
        """Mock retrieving save metadata"""
        if filename in self.metadata:
            return self.metadata[filename]
        return None

    def display_save_browser(self):
        """Mock displaying save browser"""
        print("=== Save Browser ===")
        for i, filename in enumerate(self.list_saves(), 1):
            metadata = self.get_save_metadata(filename)
            if metadata:
                save_type = metadata.get("save_type", "unknown")
                turn = metadata.get("turn", 0)
                date = metadata.get("date", "unknown")
                public_support = metadata.get("public_support", 0)
                print(
                    f"{i}. [{save_type.upper()}] Turn {turn} ({date}) - Support: {public_support}% - {filename}"
                )
        print("===================")
        return self.list_saves()
