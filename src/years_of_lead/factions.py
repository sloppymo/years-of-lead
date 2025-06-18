"""
Faction management system for Years of Lead
Handles faction behaviors, relationships, and AI decision making
"""

from typing import Dict, Any, Optional
import random
from loguru import logger
import time


class FactionManager:
    """
    Faction manager for Years of Lead

    Manages all factions in the game, their relationships,
    and their AI-driven decision making processes.
    """

    def __init__(self):
        """Initialize faction manager"""
        self.factions = {}
        self.relationships = {}

    async def initialize(
        self, game_state, scenario_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize factions based on scenario configuration

        Args:
            game_state: Current game state
            scenario_config: Scenario configuration
        """
        # Default factions if no scenario provided
        default_factions = [
            {
                "id": "anarchists",
                "name": "Radical Anarchists",
                "description": "Decentralized cells focused on direct action and sabotage",
                "strength": 50,
                "ideology": "radical_left",
                "resources": {"money": 500, "influence": 200, "personnel": 30},
                "specialties": ["direct_action", "underground_networks", "sabotage"],
            },
            {
                "id": "thinktanks",
                "name": "Centrist Think Tanks",
                "description": "Policy influencers with media connections",
                "strength": 70,
                "ideology": "centrist",
                "resources": {"money": 2000, "influence": 1000, "personnel": 15},
                "specialties": ["media_influence", "policy_shaping", "research"],
            },
            {
                "id": "corporations",
                "name": "Corporate Lobbies",
                "description": "Financial power brokers with regulatory capture capabilities",
                "strength": 85,
                "ideology": "corporatist",
                "resources": {"money": 5000, "influence": 800, "personnel": 20},
                "specialties": [
                    "financial_pressure",
                    "regulatory_capture",
                    "market_manipulation",
                ],
            },
            {
                "id": "religious",
                "name": "Religious Militias",
                "description": "Ideologically motivated community organizers",
                "strength": 60,
                "ideology": "religious_right",
                "resources": {"money": 1200, "influence": 500, "personnel": 40},
                "specialties": [
                    "recruitment",
                    "community_organizing",
                    "morality_policing",
                ],
            },
            {
                "id": "separatists",
                "name": "Separatist Syndicates",
                "description": "Territorial control focused on independence movements",
                "strength": 65,
                "ideology": "regionalist",
                "resources": {"money": 1500, "influence": 400, "personnel": 35},
                "specialties": [
                    "territorial_control",
                    "resource_extraction",
                    "autonomous_governance",
                ],
            },
        ]

        factions_config = (
            scenario_config.get("factions", default_factions)
            if scenario_config
            else default_factions
        )

        # Initialize faction data
        for faction_data in factions_config:
            faction_id = faction_data["id"]
            self.factions[faction_id] = faction_data

        # Initialize relationships between factions
        await self._initialize_relationships()

        logger.info(f"Initialized {len(self.factions)} factions")

    async def _initialize_relationships(self) -> None:
        """Initialize relationships between factions"""
        faction_ids = list(self.factions.keys())

        # Create empty relationship matrix
        for faction_id in faction_ids:
            self.relationships[faction_id] = {}

        # Generate initial relationships
        for i, faction_id in enumerate(faction_ids):
            for other_id in faction_ids:
                if faction_id == other_id:
                    continue

                # Skip if relationship is already defined in the opposite direction
                if (
                    other_id in self.relationships
                    and faction_id in self.relationships[other_id]
                ):
                    self.relationships[faction_id][other_id] = self.relationships[
                        other_id
                    ][faction_id]
                    continue

                # Generate relationship value between -100 (enemies) to 100 (allies)
                # Based on ideological differences and other factors
                faction_ideology = self.factions[faction_id].get("ideology", "")
                other_ideology = self.factions[other_id].get("ideology", "")

                # Basic ideological compatibility
                base_value = self._calculate_ideological_compatibility(
                    faction_ideology, other_ideology
                )

                # Add some randomness
                random_factor = random.randint(-20, 20)

                relationship_value = base_value + random_factor
                relationship_value = max(
                    -100, min(100, relationship_value)
                )  # Clamp to -100 to 100

                self.relationships[faction_id][other_id] = relationship_value

        logger.debug(f"Initialized faction relationships: {self.relationships}")

    def _calculate_ideological_compatibility(
        self, ideology1: str, ideology2: str
    ) -> int:
        """
        Calculate base compatibility between two ideologies

        Returns value from -80 (opposed) to 80 (aligned)
        """
        # Ideology compatibility matrix (simplified)
        compatibility = {
            "radical_left": {
                "radical_left": 80,
                "centrist": -40,
                "corporatist": -80,
                "religious_right": -60,
                "regionalist": 20,
            },
            "centrist": {
                "radical_left": -40,
                "centrist": 80,
                "corporatist": 40,
                "religious_right": 0,
                "regionalist": -20,
            },
            "corporatist": {
                "radical_left": -80,
                "centrist": 40,
                "corporatist": 80,
                "religious_right": 20,
                "regionalist": -40,
            },
            "religious_right": {
                "radical_left": -60,
                "centrist": 0,
                "corporatist": 20,
                "religious_right": 80,
                "regionalist": 0,
            },
            "regionalist": {
                "radical_left": 20,
                "centrist": -20,
                "corporatist": -40,
                "religious_right": 0,
                "regionalist": 80,
            },
        }

        # Default to neutral if ideologies aren't found
        if ideology1 not in compatibility or ideology2 not in compatibility.get(
            ideology1, {}
        ):
            return 0

        return compatibility[ideology1][ideology2]

    async def process_turn(self, game_state, current_turn: int) -> Dict[str, Any]:
        """
        Process faction actions for the current turn

        Args:
            game_state: Current game state
            current_turn: Current turn number

        Returns:
            Dictionary of faction action results
        """
        results = {
            "turn": current_turn,
            "faction_actions": {},
        }

        # For each faction, determine and execute actions
        for faction_id, faction_data in self.factions.items():
            faction_results = await self._process_faction_turn(
                faction_id, faction_data, game_state, current_turn
            )
            results["faction_actions"][faction_id] = faction_results

        logger.info(f"Processed turn {current_turn} for {len(self.factions)} factions")
        return results

    async def _process_faction_turn(
        self,
        faction_id: str,
        faction_data: Dict[str, Any],
        game_state,
        current_turn: int,
    ) -> Dict[str, Any]:
        """
        Process a single faction's turn

        Args:
            faction_id: ID of the faction
            faction_data: Faction data
            game_state: Current game state
            current_turn: Current turn number

        Returns:
            Dictionary of action results
        """
        # Get faction AI strategy based on faction type
        strategy = self._get_faction_strategy(faction_id, faction_data)

        # Determine goals for this turn
        goals = strategy.determine_goals(game_state)

        # Generate possible actions
        possible_actions = strategy.generate_actions(goals, game_state)

        # Evaluate and select actions
        selected_actions = strategy.select_actions(possible_actions, game_state)

        # Execute actions and get results
        action_results = []
        for action in selected_actions:
            result = await self._execute_faction_action(
                faction_id, faction_data, action, game_state
            )
            action_results.append(result)

        logger.debug(
            f"Faction {faction_id} completed {len(action_results)} actions on turn {current_turn}"
        )

        return {
            "faction_id": faction_id,
            "actions_taken": len(action_results),
            "results": action_results,
            # Include summaries of changes
            "faction_updates": {},  # Changes to faction data
            "district_changes": {},  # Changes to districts
            "heat_changes": {},  # Changes to heat levels
            "events": [],  # Events generated
        }

    def _get_faction_strategy(
        self, faction_id: str, faction_data: Dict[str, Any]
    ) -> Any:
        """
        Get the AI strategy object for a faction
        """
        # Create strategy based on faction type and current state
        faction_type = faction_data.get("type", "neutral")

        if faction_type == "government":
            return GovernmentStrategy(faction_id, faction_data)
        elif faction_type == "resistance":
            return ResistanceStrategy(faction_id, faction_data)
        elif faction_type == "criminal":
            return CriminalStrategy(faction_id, faction_data)
        elif faction_type == "corporate":
            return CorporateStrategy(faction_id, faction_data)
        else:
            return NeutralStrategy(faction_id, faction_data)

    async def _execute_faction_action(
        self,
        faction_id: str,
        faction_data: Dict[str, Any],
        action: Dict[str, Any],
        game_state,
    ) -> Dict[str, Any]:
        """
        Execute a faction action and determine results

        Args:
            faction_id: ID of the faction
            faction_data: Faction data
            action: Action to execute
            game_state: Current game state

        Returns:
            Action result
        """
        action_type = action.get("type", "unknown")
        target = action.get("target", {})

        try:
            # Get faction strategy
            strategy = self._get_faction_strategy(faction_id, faction_data)

            # Execute action based on type
            if action_type == "expand_influence":
                result = await self._execute_expand_influence(
                    faction_id, target, game_state
                )
            elif action_type == "gather_resources":
                result = await self._execute_gather_resources(
                    faction_id, target, game_state
                )
            elif action_type == "recruit_agents":
                result = await self._execute_recruit_agents(
                    faction_id, target, game_state
                )
            elif action_type == "conduct_mission":
                result = await self._execute_conduct_mission(
                    faction_id, target, game_state
                )
            elif action_type == "negotiate":
                result = await self._execute_negotiate(faction_id, target, game_state)
            elif action_type == "attack":
                result = await self._execute_attack(faction_id, target, game_state)
            else:
                result = {
                    "success": False,
                    "message": f"Unknown action type: {action_type}",
                }

            # Add faction-specific modifiers
            result = strategy.modify_action_result(result, action, game_state)

            return result

        except Exception as e:
            logger.error(f"Error executing faction action: {e}")
            return {"success": False, "message": f"Error executing action: {str(e)}"}

    async def _execute_expand_influence(
        self, faction_id: str, target: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Execute influence expansion action"""
        target_district = target.get("district")
        if not target_district:
            return {"success": False, "message": "No target district specified"}

        # Calculate success probability
        base_success = 0.6
        current_control = (
            game_state.districts.get(target_district, {})
            .get("control", {})
            .get(faction_id, 0)
        )
        security_level = game_state.districts.get(target_district, {}).get(
            "security_level", 5
        )

        # Adjust success based on current control and security
        success_chance = (
            base_success - (current_control * 0.3) - (security_level * 0.05)
        )
        success_chance = max(0.1, min(0.9, success_chance))

        # Determine success
        import random

        success = random.random() < success_chance

        if success:
            # Increase control in target district
            if target_district not in game_state.districts:
                game_state.districts[target_district] = {"control": {}}

            current_control = game_state.districts[target_district].get("control", {})
            current_control[faction_id] = current_control.get(faction_id, 0) + 0.1
            game_state.districts[target_district]["control"] = current_control

            return {
                "success": True,
                "message": f"Successfully expanded influence in {target_district}",
                "district_changes": {target_district: {"control": current_control}},
            }
        else:
            return {
                "success": False,
                "message": f"Failed to expand influence in {target_district}",
            }

    async def _execute_gather_resources(
        self, faction_id: str, target: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Execute resource gathering action"""
        resource_type = target.get("resource_type", "money")
        amount = target.get("amount", 100)

        # Calculate success probability
        base_success = 0.7
        success_chance = base_success

        # Determine success
        import random

        success = random.random() < success_chance

        if success:
            # Add resources to faction
            if faction_id not in game_state.factions:
                game_state.factions[faction_id] = {"resources": {}}

            current_resources = game_state.factions[faction_id].get("resources", {})
            current_resources[resource_type] = (
                current_resources.get(resource_type, 0) + amount
            )
            game_state.factions[faction_id]["resources"] = current_resources

            return {
                "success": True,
                "message": f"Successfully gathered {amount} {resource_type}",
                "faction_updates": {"resources": current_resources},
            }
        else:
            return {"success": False, "message": f"Failed to gather {resource_type}"}

    async def _execute_recruit_agents(
        self, faction_id: str, target: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Execute agent recruitment action"""
        agent_count = target.get("count", 1)

        # Calculate success probability
        base_success = 0.5
        current_agents = len(
            [p for p in game_state.players.values() if p.get("faction") == faction_id]
        )
        success_chance = base_success - (
            current_agents * 0.02
        )  # Harder to recruit more agents
        success_chance = max(0.1, success_chance)

        # Determine success
        import random

        success = random.random() < success_chance

        if success:
            recruited_agents = []
            for i in range(agent_count):
                agent_id = f"agent_{faction_id}_{len(game_state.players) + i}"
                game_state.players[agent_id] = {
                    "id": agent_id,
                    "name": f"Agent {agent_id}",
                    "faction": faction_id,
                    "location": "downtown",
                    "skills": {},
                    "status": "active",
                }
                recruited_agents.append(agent_id)

            return {
                "success": True,
                "message": f"Successfully recruited {len(recruited_agents)} agents",
                "recruited_agents": recruited_agents,
            }
        else:
            return {"success": False, "message": "Failed to recruit agents"}

    async def _execute_conduct_mission(
        self, faction_id: str, target: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Execute mission action"""
        mission_type = target.get("mission_type", "intelligence")
        target_location = target.get("location", "downtown")

        # Calculate success probability
        base_success = 0.6
        security_level = game_state.districts.get(target_location, {}).get(
            "security_level", 5
        )
        success_chance = base_success - (security_level * 0.05)
        success_chance = max(0.1, success_chance)

        # Determine success
        import random

        success = random.random() < success_chance

        if success:
            # Add mission success event
            game_state.events.append(
                {
                    "type": "mission_success",
                    "faction": faction_id,
                    "mission_type": mission_type,
                    "location": target_location,
                    "timestamp": int(time.time()),
                }
            )

            return {
                "success": True,
                "message": f"Mission {mission_type} at {target_location} successful",
                "events": [
                    {
                        "type": "mission_success",
                        "faction": faction_id,
                        "mission_type": mission_type,
                        "location": target_location,
                    }
                ],
            }
        else:
            # Add mission failure event
            game_state.events.append(
                {
                    "type": "mission_failure",
                    "faction": faction_id,
                    "mission_type": mission_type,
                    "location": target_location,
                    "timestamp": int(time.time()),
                }
            )

            return {
                "success": False,
                "message": f"Mission {mission_type} at {target_location} failed",
                "events": [
                    {
                        "type": "mission_failure",
                        "faction": faction_id,
                        "mission_type": mission_type,
                        "location": target_location,
                    }
                ],
            }

    async def _execute_negotiate(
        self, faction_id: str, target: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Execute negotiation action"""
        target_faction = target.get("target_faction")
        negotiation_type = target.get("type", "alliance")

        if not target_faction:
            return {"success": False, "message": "No target faction specified"}

        # Calculate success probability
        base_success = 0.4
        current_relationship = self.get_relationship(faction_id, target_faction)
        success_chance = base_success + (current_relationship * 0.01)
        success_chance = max(0.1, min(0.8, success_chance))

        # Determine success
        import random

        success = random.random() < success_chance

        if success:
            # Improve relationship
            self.relationships[faction_id][target_faction] = current_relationship + 10
            self.relationships[target_faction][faction_id] = current_relationship + 10

            return {
                "success": True,
                "message": f"Successfully negotiated {negotiation_type} with {target_faction}",
                "relationship_change": 10,
            }
        else:
            # Worsen relationship
            self.relationships[faction_id][target_faction] = current_relationship - 5
            self.relationships[target_faction][faction_id] = current_relationship - 5

            return {
                "success": False,
                "message": f"Failed to negotiate {negotiation_type} with {target_faction}",
                "relationship_change": -5,
            }

    async def _execute_attack(
        self, faction_id: str, target: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Execute attack action"""
        target_faction = target.get("target_faction")
        target_location = target.get("location", "downtown")

        if not target_faction:
            return {"success": False, "message": "No target faction specified"}

        # Calculate success probability
        base_success = 0.3
        attacker_strength = game_state.factions.get(faction_id, {}).get("strength", 50)
        defender_strength = game_state.factions.get(target_faction, {}).get(
            "strength", 50
        )

        success_chance = base_success + (attacker_strength - defender_strength) * 0.01
        success_chance = max(0.1, min(0.8, success_chance))

        # Determine success
        import random

        success = random.random() < success_chance

        if success:
            # Reduce target faction strength
            if target_faction in game_state.factions:
                game_state.factions[target_faction]["strength"] = max(
                    0, defender_strength - 10
                )

            # Worsen relationship
            current_relationship = self.get_relationship(faction_id, target_faction)
            self.relationships[faction_id][target_faction] = current_relationship - 20
            self.relationships[target_faction][faction_id] = current_relationship - 20

            return {
                "success": True,
                "message": f"Successfully attacked {target_faction} at {target_location}",
                "faction_updates": {
                    target_faction: {"strength": max(0, defender_strength - 10)}
                },
                "relationship_change": -20,
            }
        else:
            # Reduce attacker strength
            if faction_id in game_state.factions:
                game_state.factions[faction_id]["strength"] = max(
                    0, attacker_strength - 5
                )

            return {
                "success": False,
                "message": f"Failed to attack {target_faction} at {target_location}",
                "faction_updates": {
                    faction_id: {"strength": max(0, attacker_strength - 5)}
                },
            }

    async def serialize(self) -> Dict[str, Any]:
        """Serialize faction manager state"""
        return {
            "factions": self.factions,
            "relationships": self.relationships,
            "strategies": {
                fid: str(type(self._get_faction_strategy(fid, fdata)))
                for fid, fdata in self.factions.items()
            },
        }

    async def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize faction manager state"""
        self.factions = data.get("factions", {})
        self.relationships = data.get("relationships", {})


# Strategy classes for different faction types
class FactionStrategy:
    """Base class for faction strategies"""

    def __init__(self, faction_id: str, faction_data: Dict[str, Any]):
        self.faction_id = faction_id
        self.faction_data = faction_data

    def modify_action_result(
        self, result: Dict[str, Any], action: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        """Modify action result based on faction strategy"""
        return result


class GovernmentStrategy(FactionStrategy):
    """Strategy for government factions"""

    def modify_action_result(
        self, result: Dict[str, Any], action: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        # Government actions are more likely to succeed in high-security areas
        if result.get("success") and action.get("type") in [
            "expand_influence",
            "conduct_mission",
        ]:
            target_location = action.get("target", {}).get("location", "downtown")
            security_level = game_state.districts.get(target_location, {}).get(
                "security_level", 5
            )
            if security_level >= 7:
                result["message"] += " (Government advantage in high-security area)"
        return result


class ResistanceStrategy(FactionStrategy):
    """Strategy for resistance factions"""

    def modify_action_result(
        self, result: Dict[str, Any], action: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        # Resistance actions are more likely to succeed in low-security areas
        if result.get("success") and action.get("type") in [
            "expand_influence",
            "conduct_mission",
        ]:
            target_location = action.get("target", {}).get("location", "downtown")
            security_level = game_state.districts.get(target_location, {}).get(
                "security_level", 5
            )
            if security_level <= 4:
                result["message"] += " (Resistance advantage in low-security area)"
        return result


class CriminalStrategy(FactionStrategy):
    """Strategy for criminal factions"""

    def modify_action_result(
        self, result: Dict[str, Any], action: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        # Criminal actions are more likely to succeed in industrial areas
        if result.get("success") and action.get("type") in [
            "gather_resources",
            "conduct_mission",
        ]:
            target_location = action.get("target", {}).get("location", "downtown")
            if target_location == "industrial":
                result["message"] += " (Criminal advantage in industrial area)"
        return result


class CorporateStrategy(FactionStrategy):
    """Strategy for corporate factions"""

    def modify_action_result(
        self, result: Dict[str, Any], action: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        # Corporate actions are more likely to succeed in downtown areas
        if result.get("success") and action.get("type") in [
            "negotiate",
            "gather_resources",
        ]:
            target_location = action.get("target", {}).get("location", "downtown")
            if target_location == "downtown":
                result["message"] += " (Corporate advantage in downtown area)"
        return result


class NeutralStrategy(FactionStrategy):
    """Strategy for neutral factions"""

    def modify_action_result(
        self, result: Dict[str, Any], action: Dict[str, Any], game_state
    ) -> Dict[str, Any]:
        # Neutral factions have no special advantages
        return result

    def get_faction(self, faction_id: str) -> Optional[Dict[str, Any]]:
        """Get faction data by ID"""
        return self.factions.get(faction_id)

    def get_relationship(self, faction_id: str, other_id: str) -> int:
        """Get relationship value between two factions"""
        if (
            faction_id not in self.relationships
            or other_id not in self.relationships[faction_id]
        ):
            return 0
        return self.relationships[faction_id][other_id]

    def set_relationship(self, faction_id: str, other_id: str, value: int) -> None:
        """Set relationship value between two factions"""
        if faction_id not in self.relationships:
            self.relationships[faction_id] = {}

        # Clamp value between -100 and 100
        value = max(-100, min(100, value))
        self.relationships[faction_id][other_id] = value
        logger.debug(
            f"Updated relationship between {faction_id} and {other_id} to {value}"
        )
