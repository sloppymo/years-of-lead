"""
SaveManager module for handling game saves and loads.
"""
import os
import json
from datetime import datetime


class SaveManager:
    """Handles saving and loading game states"""

    def __init__(self):
        """Initialize the save manager"""
        # Create saves directory if it doesn't exist
        self.save_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "saves"
        )
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def save_game(self, game, filename, save_type="manual"):
        """Save the game state to a file

        Args:
            game: The game object to save
            filename: The name of the save file (without extension)
            save_type: The type of save (manual, autosave, victory, defeat)

        Returns:
            The full filename of the saved game
        """
        # Create a unique filename if one is not provided
        if not filename.endswith(".json"):
            filename = f"{filename}.json"

        # Get the full path to the save file
        save_path = os.path.join(self.save_directory, filename)

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

        # Prepare the save data
        save_data = {"metadata": metadata, "game_state": game_state}

        # Save the data to the file
        with open(save_path, "w") as f:
            json.dump(save_data, f, indent=2)

        return filename

    def load_game(self, cli, filename):
        """Load a game state from a file

        Args:
            cli: The CLI object that contains the game
            filename: The name of the save file

        Returns:
            True if the load was successful, False otherwise
        """
        # Get the full path to the save file
        save_path = os.path.join(self.save_directory, filename)

        # Check if the file exists
        if not os.path.exists(save_path):
            print(f"Save file {filename} not found!")
            return False

        # Load the data from the file
        try:
            with open(save_path, "r") as f:
                save_data = json.load(f)

            # Extract the game state
            game_state = save_data.get("game_state", {})

            # Load the game state
            if hasattr(cli.game, "from_dict"):
                cli.game.from_dict(game_state)

            return True
        except Exception as e:
            print(f"Error loading save file: {e}")
            return False

    def autosave(self, game):
        """Create an autosave

        Args:
            game: The game object to save

        Returns:
            The filename of the autosave
        """
        # Get the current turn
        turn = game.turn if hasattr(game, "turn") else 0

        # Create a filename with the turn number and current date
        filename = f"autosave_turn{turn}_{datetime.now().strftime('%Y%m%d')}"

        # Save the game
        return self.save_game(game, filename, save_type="autosave")

    def victory_save(self, game, victory_type):
        """Create a victory save

        Args:
            game: The game object to save
            victory_type: The type of victory (e.g., "high_public_support")

        Returns:
            The filename of the victory save
        """
        # Create a filename with the victory type and current date
        filename = f"victory_{victory_type}_{datetime.now().strftime('%Y%m%d')}"

        # Save the game
        return self.save_game(game, filename, save_type="victory")

    def defeat_save(self, game, defeat_type):
        """Create a defeat save

        Args:
            game: The game object to save
            defeat_type: The type of defeat (e.g., "low_public_support")

        Returns:
            The filename of the defeat save
        """
        # Create a filename with the defeat type and current date
        filename = f"defeat_{defeat_type}_{datetime.now().strftime('%Y%m%d')}"

        # Save the game
        return self.save_game(game, filename, save_type="defeat")

    def list_saves(self):
        """List all save files

        Returns:
            A list of save filenames
        """
        # Get all files in the save directory
        files = os.listdir(self.save_directory)

        # Filter for JSON files
        save_files = [f for f in files if f.endswith(".json")]

        return save_files

    def get_save_metadata(self, filename):
        """Get metadata for a save file

        Args:
            filename: The name of the save file

        Returns:
            The metadata dictionary, or None if the file doesn't exist
        """
        # Get the full path to the save file
        save_path = os.path.join(self.save_directory, filename)

        # Check if the file exists
        if not os.path.exists(save_path):
            return None

        # Load the data from the file
        try:
            with open(save_path, "r") as f:
                save_data = json.load(f)

            # Extract the metadata
            return save_data.get("metadata", {})
        except Exception as e:
            print(f"Error reading save metadata: {e}")
            return None

    def display_save_browser(self):
        """Display a browser for save files

        Returns:
            A list of save filenames
        """
        # Get all save files
        save_files = self.list_saves()

        # If there are no save files, return an empty list
        if not save_files:
            print("No save files found!")
            return []

        # Display the save files
        print("=== Save Browser ===")
        for i, filename in enumerate(save_files, 1):
            # Get metadata for the save file
            metadata = self.get_save_metadata(filename)

            if metadata:
                # Extract metadata fields
                save_type = metadata.get("save_type", "unknown")
                turn = metadata.get("turn", 0)
                date = metadata.get("date", "unknown")
                agent_count = metadata.get("agent_count", 0)
                public_support = metadata.get("public_support", 0)
                controlled_locations = metadata.get("controlled_locations", 0)
                timestamp = metadata.get("timestamp", "unknown")

                # Format the timestamp
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass

                # Display the save file with metadata
                print(
                    f"{i}. [{save_type.upper()}] Turn {turn} ({date}) - Agents: {agent_count}, Support: {public_support}%, "
                    f"Locations: {controlled_locations} - {timestamp} - {filename}"
                )
            else:
                # Display the save file without metadata
                print(f"{i}. {filename}")

        print("===================")
        return save_files
