"""
Game state management for Years of Lead
Handles the core state of the game world, districts, and factions
"""

from typing import Dict, Any, Optional
from loguru import logger


class GameState:
    """
    Game state manager for Years of Lead
    Maintains the current state of the game world, including
    districts, factions, resources, and other game elements
    """

    def __init__(self, game_id: str):
        """Initialize game state with game ID"""
        self.game_id = game_id
        self.world_data = {}
        self.factions = {}
        self.districts = {}
        self.players = {}
        self.resources = {}
        self.heat_levels = {}
        self.turn_history = []
        self.events = []

        logger.info(f"Game state initialized for game {game_id}")

    async def initialize(
        self, scenario_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize game state with scenario configuration"""
        scenario_name = (
            scenario_config.get("name", "default") if scenario_config else "default"
        )
        logger.info(f"Initializing game state with scenario: {scenario_name}")

        # Initialize districts
        await self._initialize_districts(scenario_config)

        # Initialize resources
        await self._initialize_resources(scenario_config)

        # Initialize heat levels
        await self._initialize_heat_levels()

        # Save initial state to history
        self._save_state_to_history(0, "game_initialized")

    async def _initialize_districts(
        self, scenario_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize game districts"""
        # Default districts if no scenario provided
        default_districts = [
            {
                "id": "downtown",
                "name": "Downtown",
                "population": 250000,
                "security_level": 8,
            },
            {
                "id": "industrial",
                "name": "Industrial Zone",
                "population": 120000,
                "security_level": 5,
            },
            {
                "id": "suburbs",
                "name": "Suburbs",
                "population": 350000,
                "security_level": 6,
            },
            {
                "id": "university",
                "name": "University District",
                "population": 80000,
                "security_level": 4,
            },
            {
                "id": "government",
                "name": "Government Quarter",
                "population": 40000,
                "security_level": 10,
            },
        ]

        districts_config = (
            scenario_config.get("districts", default_districts)
            if scenario_config
            else default_districts
        )

        for district in districts_config:
            district_id = district["id"]
            self.districts[district_id] = {
                "id": district_id,
                "name": district.get("name", district_id),
                "population": district.get("population", 100000),
                "security_level": district.get("security_level", 5),
                "control": {},  # Faction control percentages
                "facilities": district.get("facilities", []),
                "events": [],
            }

        logger.info(f"Initialized {len(self.districts)} districts")

    async def _initialize_resources(
        self, scenario_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize game resources"""
        default_resources = {"money": 1000, "influence": 500, "personnel": 10}

        resources_config = (
            scenario_config.get("initial_resources", default_resources)
            if scenario_config
            else default_resources
        )
        self.resources = resources_config

        logger.info(f"Initialized resources: {self.resources}")

    async def _initialize_heat_levels(self) -> None:
        """Initialize heat levels for districts and factions"""
        # Initialize district heat levels
        for district_id in self.districts:
            self.heat_levels[district_id] = 0

        logger.info(f"Initialized heat levels for {len(self.heat_levels)} districts")

    async def update(self, faction_results: Dict[str, Any]) -> None:
        """Update game state based on faction action results"""
        # Process faction results and update state
        for faction_id, results in faction_results.items():
            if faction_id in self.factions:
                # Update faction state
                for key, value in results.get("faction_updates", {}).items():
                    self.factions[faction_id][key] = value

                # Process district changes
                for district_id, changes in results.get("district_changes", {}).items():
                    if district_id in self.districts:
                        for key, value in changes.items():
                            self.districts[district_id][key] = value

                # Update heat levels
                for district_id, heat_change in results.get("heat_changes", {}).items():
                    if district_id in self.heat_levels:
                        self.heat_levels[district_id] += heat_change

                # Add events
                for event in results.get("events", []):
                    self.events.append(event)

        # Save updated state to history
        turn = faction_results.get("turn", len(self.turn_history))
        self._save_state_to_history(turn, "turn_processed")

    async def process_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a player action and update state accordingly"""
        action_type = action_data.get("type", "unknown")
        logger.info(f"Processing action of type: {action_type}")

        try:
            result = {"success": False, "action_type": action_type, "message": ""}
            
            if action_type == "move_agent":
                result = await self._process_move_agent(action_data)
            elif action_type == "assign_mission":
                result = await self._process_assign_mission(action_data)
            elif action_type == "equip_item":
                result = await self._process_equip_item(action_data)
            elif action_type == "unequip_item":
                result = await self._process_unequip_item(action_data)
            elif action_type == "recruit_agent":
                result = await self._process_recruit_agent(action_data)
            elif action_type == "gather_intelligence":
                result = await self._process_gather_intelligence(action_data)
            elif action_type == "propaganda":
                result = await self._process_propaganda(action_data)
            else:
                result["message"] = f"Unknown action type: {action_type}"
                logger.warning(f"Unknown action type: {action_type}")

            # Add action to events
            self.events.append({
                "type": "player_action",
                "action_type": action_type,
                "data": action_data,
                "result": result,
                "timestamp": self._get_timestamp(),
            })

            return result

        except Exception as e:
            logger.error(f"Error processing action {action_type}: {e}")
            return {
                "success": False,
                "action_type": action_type,
                "message": f"Error processing action: {str(e)}"
            }

    async def _process_move_agent(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent movement action"""
        agent_id = action_data.get("agent_id")
        target_location = action_data.get("target_location")
        
        if not agent_id or not target_location:
            return {
                "success": False,
                "message": "Missing agent_id or target_location"
            }
        
        # Check if agent exists
        if agent_id not in self.players:
            return {
                "success": False,
                "message": f"Agent {agent_id} not found"
            }
        
        # Check if location exists
        if target_location not in self.districts:
            return {
                "success": False,
                "message": f"Location {target_location} not found"
            }
        
        # Update agent location
        self.players[agent_id]["location"] = target_location
        
        return {
            "success": True,
            "message": f"Agent {agent_id} moved to {target_location}"
        }

    async def _process_assign_mission(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process mission assignment action"""
        mission_id = action_data.get("mission_id")
        agent_ids = action_data.get("agent_ids", [])
        
        if not mission_id or not agent_ids:
            return {
                "success": False,
                "message": "Missing mission_id or agent_ids"
            }
        
        # Validate agents exist
        for agent_id in agent_ids:
            if agent_id not in self.players:
                return {
                    "success": False,
                    "message": f"Agent {agent_id} not found"
                }
        
        # Add mission assignment to events
        self.events.append({
            "type": "mission_assigned",
            "mission_id": mission_id,
            "agent_ids": agent_ids,
            "timestamp": self._get_timestamp(),
        })
        
        return {
            "success": True,
            "message": f"Mission {mission_id} assigned to {len(agent_ids)} agents"
        }

    async def _process_equip_item(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process equipment assignment action"""
        agent_id = action_data.get("agent_id")
        item_id = action_data.get("item_id")
        
        if not agent_id or not item_id:
            return {
                "success": False,
                "message": "Missing agent_id or item_id"
            }
        
        # Check if agent exists
        if agent_id not in self.players:
            return {
                "success": False,
                "message": f"Agent {agent_id} not found"
            }
        
        return {
            "success": True,
            "message": f"Item {item_id} equipped to agent {agent_id}"
        }

    async def _process_unequip_item(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process equipment removal action"""
        agent_id = action_data.get("agent_id")
        item_id = action_data.get("item_id")
        
        if not agent_id or not item_id:
            return {
                "success": False,
                "message": "Missing agent_id or item_id"
            }
        
        # Check if agent exists
        if agent_id not in self.players:
            return {
                "success": False,
                "message": f"Agent {agent_id} not found"
            }
        
        return {
            "success": True,
            "message": f"Item {item_id} unequipped from agent {agent_id}"
        }

    async def _process_recruit_agent(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent recruitment action"""
        agent_data = action_data.get("agent_data", {})
        
        if not agent_data:
            return {
                "success": False,
                "message": "Missing agent_data"
            }
        
        # Generate new agent ID
        agent_id = f"agent_{len(self.players) + 1}"
        
        # Add agent to players
        self.players[agent_id] = {
            "id": agent_id,
            "name": agent_data.get("name", f"Agent {agent_id}"),
            "location": agent_data.get("location", "downtown"),
            "skills": agent_data.get("skills", {}),
            "equipment": agent_data.get("equipment", []),
            "status": "active"
        }
        
        return {
            "success": True,
            "message": f"Agent {agent_id} recruited successfully"
        }

    async def _process_gather_intelligence(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process intelligence gathering action"""
        location = action_data.get("location", "downtown")
        
        # Simulate intelligence gathering
        intelligence_quality = 0.7  # Base quality
        if location in self.districts:
            security_level = self.districts[location].get("security_level", 5)
            intelligence_quality = max(0.1, intelligence_quality - (security_level * 0.05))
        
        # Add intelligence event
        self.events.append({
            "type": "intelligence_gathered",
            "location": location,
            "quality": intelligence_quality,
            "timestamp": self._get_timestamp(),
        })
        
        return {
            "success": True,
            "message": f"Intelligence gathered at {location} (quality: {intelligence_quality:.2f})"
        }

    async def _process_propaganda(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process propaganda action"""
        target_district = action_data.get("target_district", "downtown")
        message = action_data.get("message", "General propaganda")
        
        # Simulate propaganda effect
        effect_strength = 0.3  # Base effect
        if target_district in self.districts:
            population = self.districts[target_district].get("population", 100000)
            effect_strength = min(1.0, effect_strength * (population / 100000))
        
        # Add propaganda event
        self.events.append({
            "type": "propaganda_campaign",
            "target_district": target_district,
            "message": message,
            "effect_strength": effect_strength,
            "timestamp": self._get_timestamp(),
        })
        
        return {
            "success": True,
            "message": f"Propaganda campaign in {target_district} (effect: {effect_strength:.2f})"
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the current game state"""
        return {
            "game_id": self.game_id,
            "districts_count": len(self.districts),
            "factions_count": len(self.factions),
            "players_count": len(self.players),
            "event_count": len(self.events),
            "resources": self.resources,
            "latest_events": self.events[-5:] if self.events else [],
        }

    def _save_state_to_history(self, turn: int, reason: str) -> None:
        """Save current state snapshot to history"""
        # Create a deep copy of essential state data
        state_snapshot = {
            "turn": turn,
            "reason": reason,
            "timestamp": self._get_timestamp(),
            "resources": dict(self.resources),
            "heat_levels": dict(self.heat_levels),
            # Only save summaries of large data structures
            "districts_summary": {
                d_id: {"name": d["name"], "control": d.get("control", {})}
                for d_id, d in self.districts.items()
            },
            "factions_summary": {
                f_id: {"name": f.get("name", f_id), "strength": f.get("strength", 0)}
                for f_id, f in self.factions.items()
            },
        }

        self.turn_history.append(state_snapshot)
        logger.debug(f"Saved state snapshot for turn {turn}, reason: {reason}")

    async def check_victory_conditions(self) -> bool:
        """Check if any victory conditions have been met"""
        # Check for victory conditions
        victory_conditions = [
            self._check_public_support_victory(),
            self._check_territory_control_victory(),
            self._check_enemy_weakening_victory(),
            self._check_mission_completion_victory()
        ]
        
        return any(victory_conditions)

    def _check_public_support_victory(self) -> bool:
        """Check if public support victory condition is met"""
        # Calculate total public support across all districts
        total_population = sum(d.get("population", 0) for d in self.districts.values())
        if total_population == 0:
            return False
        
        # Simulate public support calculation
        support_percentage = 0.5  # Base 50% support
        for event in self.events[-10:]:  # Look at recent events
            if event.get("type") == "propaganda_campaign":
                support_percentage += event.get("effect_strength", 0) * 0.1
            elif event.get("type") == "mission_success":
                support_percentage += 0.05
            elif event.get("type") == "mission_failure":
                support_percentage -= 0.03
        
        return support_percentage >= 0.75  # 75% support needed for victory

    def _check_territory_control_victory(self) -> bool:
        """Check if territory control victory condition is met"""
        controlled_districts = 0
        for district_id, district in self.districts.items():
            # Check if player faction has majority control
            control = district.get("control", {})
            player_control = control.get("player", 0)
            if player_control > 0.5:  # More than 50% control
                controlled_districts += 1
        
        return controlled_districts >= 3  # Need 3+ districts under control

    def _check_enemy_weakening_victory(self) -> bool:
        """Check if enemy weakening victory condition is met"""
        # Simulate enemy strength calculation
        enemy_strength = 1.0  # Base enemy strength
        
        # Reduce enemy strength based on successful operations
        for event in self.events[-20:]:  # Look at recent events
            if event.get("type") == "mission_success":
                enemy_strength -= 0.02
            elif event.get("type") == "intelligence_gathered"):
                enemy_strength -= 0.01
        
        return enemy_strength <= 0.25  # Enemy strength below 25%

    def _check_mission_completion_victory(self) -> bool:
        """Check if mission completion victory condition is met"""
        completed_missions = sum(1 for event in self.events 
                               if event.get("type") == "mission_success")
        
        return completed_missions >= 10  # Complete 10+ missions for victory

    async def serialize(self) -> Dict[str, Any]:
        """Serialize the game state for saving"""
        return {
            "game_id": self.game_id,
            "districts": self.districts,
            "factions": self.factions,
            "players": self.players,
            "resources": self.resources,
            "heat_levels": self.heat_levels,
            "events": self.events,
            "turn_history": self.turn_history
        }

    async def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the game state from saved data"""
        self.game_id = data.get("game_id", self.game_id)
        self.districts = data.get("districts", {})
        self.factions = data.get("factions", {})
        self.players = data.get("players", {})
        self.resources = data.get("resources", {})
        self.heat_levels = data.get("heat_levels", {})
        self.events = data.get("events", [])
        self.turn_history = data.get("turn_history", [])

    def _get_timestamp(self) -> int:
        """Get current timestamp"""
        import time

        return int(time.time())
