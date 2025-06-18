"""
Core game engine for Years of Lead
Implements the turn-based game loop and event system
"""

import uuid
import time
import json
from typing import Dict, Any
from enum import Enum
from loguru import logger
from pathlib import Path

from game.state import GameState
from game.events import EventManager
from game.factions import FactionManager


class GameStatus(Enum):
    """Game status enum"""

    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class GameEngine:
    """
    Core game engine for Years of Lead
    Manages the turn-based loop, game state, and event processing
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize game engine with optional configuration"""
        self.game_id = str(uuid.uuid4())
        self.status = GameStatus.INITIALIZING
        self.current_turn = 0
        self.max_turns = config.get("max_turns", 100) if config else 100
        self.start_time = time.time()

        # Initialize core components
        self.state = GameState(game_id=self.game_id)
        self.event_manager = EventManager()
        self.faction_manager = FactionManager()

        logger.info(f"Game engine initialized with ID: {self.game_id}")

    async def initialize_game(
        self, scenario_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Initialize a new game with the given scenario configuration"""
        logger.info(f"Initializing new game with scenario: {scenario_config}")

        # Set up initial world state
        await self.state.initialize(scenario_config)

        # Initialize factions
        await self.faction_manager.initialize(self.state, scenario_config)

        # Register core event listeners
        self._register_event_listeners()

        # Set game to running state
        self.status = GameStatus.RUNNING

        # Trigger game start event
        self.event_manager.trigger(
            "game.started",
            {
                "game_id": self.game_id,
                "start_time": self.start_time,
                "scenario": scenario_config,
            },
        )

        return self.get_game_info()

    def _register_event_listeners(self):
        """Register core event listeners"""
        # Register turn-related events
        self.event_manager.register("turn.start", self._on_turn_start)
        self.event_manager.register("turn.end", self._on_turn_end)

        # Register faction-related events
        self.event_manager.register("faction.action", self._on_faction_action)

        # Register game state events
        self.event_manager.register("game.paused", self._on_game_paused)
        self.event_manager.register("game.resumed", self._on_game_resumed)

    async def process_turn(self) -> Dict[str, Any]:
        """Process a single game turn"""
        if self.status != GameStatus.RUNNING:
            logger.warning(f"Cannot process turn, game is in {self.status} state")
            return {"error": f"Game is in {self.status} state"}

        # Increment turn counter
        self.current_turn += 1
        logger.info(f"Processing turn {self.current_turn}/{self.max_turns}")

        # Trigger turn start event
        turn_data = {
            "game_id": self.game_id,
            "turn": self.current_turn,
            "max_turns": self.max_turns,
        }
        self.event_manager.trigger("turn.start", turn_data)

        # Process faction actions
        faction_results = await self.faction_manager.process_turn(
            self.state, self.current_turn
        )

        # Update game state based on actions
        await self.state.update(faction_results)

        # Trigger turn end event
        self.event_manager.trigger("turn.end", turn_data)

        # Check for game end conditions
        if self.current_turn >= self.max_turns:
            logger.info("Maximum turns reached, ending game")
            await self.end_game("maximum_turns_reached")
        elif await self.state.check_victory_conditions():
            logger.info("Victory conditions met, ending game")
            await self.end_game("victory_conditions_met")

        return {
            "turn": self.current_turn,
            "faction_results": faction_results,
            "state_summary": self.state.get_summary(),
        }

    async def end_game(self, reason: str) -> Dict[str, Any]:
        """End the current game with the specified reason"""
        logger.info(f"Ending game {self.game_id}, reason: {reason}")

        # Set game status to completed
        self.status = GameStatus.COMPLETED

        # Calculate game duration
        duration = time.time() - self.start_time

        # Trigger game end event
        end_data = {
            "game_id": self.game_id,
            "reason": reason,
            "duration": duration,
            "turns": self.current_turn,
            "state_summary": self.state.get_summary(),
        }
        self.event_manager.trigger("game.ended", end_data)

        return end_data

    async def pause_game(self) -> Dict[str, Any]:
        """Pause the current game"""
        if self.status == GameStatus.RUNNING:
            self.status = GameStatus.PAUSED
            logger.info(f"Game {self.game_id} paused")
            self.event_manager.trigger("game.paused", {"game_id": self.game_id})

        return self.get_game_info()

    async def resume_game(self) -> Dict[str, Any]:
        """Resume the current game"""
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.RUNNING
            logger.info(f"Game {self.game_id} resumed")
            self.event_manager.trigger("game.resumed", {"game_id": self.game_id})

        return self.get_game_info()

    async def perform_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a player action in the game"""
        # Validate action
        if not self._validate_action(action_data):
            return {"error": "Invalid action data"}

        # Process the action in the game state
        result = await self.state.process_action(action_data)

        # Trigger action event
        self.event_manager.trigger(
            "player.action",
            {
                "game_id": self.game_id,
                "turn": self.current_turn,
                "action": action_data,
                "result": result,
            },
        )

        return result

    def _validate_action(self, action_data: Dict[str, Any]) -> bool:
        """Validate a player action"""
        if not action_data or not isinstance(action_data, dict):
            return False
            
        # Check required fields
        required_fields = ["type"]
        for field in required_fields:
            if field not in action_data:
                logger.warning(f"Action validation failed: missing required field '{field}'")
                return False
        
        # Validate action type
        valid_action_types = [
            "move_agent", "assign_mission", "equip_item", "unequip_item",
            "recruit_agent", "train_agent", "research_technology", "build_facility",
            "negotiate", "attack", "defend", "gather_intelligence", "propaganda"
        ]
        
        action_type = action_data.get("type")
        if action_type not in valid_action_types:
            logger.warning(f"Action validation failed: invalid action type '{action_type}'")
            return False
        
        # Validate action-specific requirements
        if action_type == "move_agent":
            if "agent_id" not in action_data or "target_location" not in action_data:
                logger.warning("Move agent action missing agent_id or target_location")
                return False
        elif action_type == "assign_mission":
            if "mission_id" not in action_data or "agent_ids" not in action_data:
                logger.warning("Assign mission action missing mission_id or agent_ids")
                return False
        elif action_type in ["equip_item", "unequip_item"]:
            if "agent_id" not in action_data or "item_id" not in action_data:
                logger.warning("Equipment action missing agent_id or item_id")
                return False
        
        return True

    def get_game_info(self) -> Dict[str, Any]:
        """Get current game information"""
        return {
            "game_id": self.game_id,
            "status": self.status.value,
            "current_turn": self.current_turn,
            "max_turns": self.max_turns,
            "start_time": self.start_time,
            "state_summary": self.state.get_summary() if self.state else {},
        }

    async def save_game(self) -> Dict[str, Any]:
        """Save the current game state"""
        try:
            logger.info(f"Saving game {self.game_id}")
            
            # Create save data
            save_data = {
                "game_id": self.game_id,
                "status": self.status.value,
                "current_turn": self.current_turn,
                "max_turns": self.max_turns,
                "start_time": self.start_time,
                "save_timestamp": time.time(),
                "state": await self.state.serialize() if self.state else {},
                "faction_data": await self.faction_manager.serialize() if self.faction_manager else {},
                "event_history": self.event_manager.get_history() if self.event_manager else []
            }
            
            # Save to file system (temporary implementation)
            save_dir = Path("saves")
            save_dir.mkdir(exist_ok=True)
            
            save_file = save_dir / f"{self.game_id}_turn_{self.current_turn}.json"
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2, default=str)
            
            logger.info(f"Game saved to {save_file}")
            return {
                "success": True,
                "save_file": str(save_file),
                "message": f"Game saved successfully to {save_file}"
            }
            
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to save game"
            }

    async def load_game(self, game_id: str) -> Dict[str, Any]:
        """Load a saved game state"""
        try:
            logger.info(f"Loading game {game_id}")
            
            # Find save file
            save_dir = Path("saves")
            if not save_dir.exists():
                return {
                    "success": False,
                    "error": "No saves directory found",
                    "message": "No saved games available"
                }
            
            # Look for save files matching the game_id
            save_files = list(save_dir.glob(f"{game_id}_*.json"))
            if not save_files:
                return {
                    "success": False,
                    "error": "No save files found for game_id",
                    "message": f"No save files found for game {game_id}"
                }
            
            # Load the most recent save
            latest_save = max(save_files, key=lambda f: f.stat().st_mtime)
            
            with open(latest_save, 'r') as f:
                save_data = json.load(f)
            
            # Restore game state
            self.game_id = save_data["game_id"]
            self.status = GameStatus(save_data["status"])
            self.current_turn = save_data["current_turn"]
            self.max_turns = save_data["max_turns"]
            self.start_time = save_data["start_time"]
            
            # Restore state and faction data
            if self.state and "state" in save_data:
                await self.state.deserialize(save_data["state"])
            
            if self.faction_manager and "faction_data" in save_data:
                await self.faction_manager.deserialize(save_data["faction_data"])
            
            # Restore event history
            if self.event_manager and "event_history" in save_data:
                self.event_manager.restore_history(save_data["event_history"])
            
            logger.info(f"Game loaded from {latest_save}")
            return {
                "success": True,
                "save_file": str(latest_save),
                "message": f"Game loaded successfully from {latest_save}",
                "game_info": self.get_game_info()
            }
            
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to load game"
            }

    # Event handlers
    def _on_turn_start(self, data: Dict[str, Any]):
        """Handle turn start event"""
        logger.debug(f"Turn {data['turn']} started")

    def _on_turn_end(self, data: Dict[str, Any]):
        """Handle turn end event"""
        logger.debug(f"Turn {data['turn']} ended")

    def _on_faction_action(self, data: Dict[str, Any]):
        """Handle faction action event"""
        logger.debug(
            f"Faction {data.get('faction_id')} performed action: {data.get('action_type')}"
        )

    def _on_game_paused(self, data: Dict[str, Any]):
        """Handle game paused event"""
        logger.debug(f"Game {data['game_id']} paused")

    def _on_game_resumed(self, data: Dict[str, Any]):
        """Handle game resumed event"""
        logger.debug(f"Game {data['game_id']} resumed")
