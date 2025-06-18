"""
Years of Lead - Advanced Mission Execution Engine

Comprehensive mission execution with nuanced success/failure mechanics,
resource management, and meaningful narrative consequences.
"""

import random
import logging
from enum import Enum
from typing import Dict, List, Any
from dataclasses import dataclass

# Import equipment integration
from .equipment_integration import EquipmentIntegrationManager, AgentLoadout, LoadoutSlot
from .equipment_enhanced import EnhancedEquipmentProfile, EquipmentDurability

logger = logging.getLogger(__name__)


class ExecutionOutcome(Enum):
    """Detailed execution outcomes"""

    PERFECT_SUCCESS = "perfect_success"
    SUCCESS_WITH_COMPLICATIONS = "success_with_complications"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE_WITH_INTEL = "failure_with_intel"
    COMPLETE_FAILURE = "complete_failure"
    CATASTROPHIC_FAILURE = "catastrophic_failure"


class ConsequenceType(Enum):
    """Types of mission consequences"""

    POLITICAL = "political"
    SOCIAL = "social"
    RESOURCE = "resource"
    PERSONNEL = "personnel"
    INTELLIGENCE = "intelligence"
    REPUTATION = "reputation"
    TACTICAL = "tactical"
    EMOTIONAL = "emotional"
    EQUIPMENT = "equipment"  # New consequence type for equipment


@dataclass
class MissionConsequence:
    """Detailed mission consequence"""

    type: ConsequenceType
    description: str
    immediate_effects: Dict[str, Any]
    long_term_effects: Dict[str, Any]
    emotional_impact: Dict[str, float]
    narrative_text: str
    severity: float  # 0.0 to 1.0


@dataclass
class ResourceCost:
    """Resource costs for mission execution"""

    money: int = 0
    equipment: int = 0
    agent_time_hours: int = 0
    network_exposure: float = 0.0  # 0.0-1.0 risk of network compromise
    safe_house_risk: float = 0.0  # Risk to safe house security
    equipment_repair_costs: float = 0.0  # New: equipment repair costs

    def __post_init__(self):
        self.network_exposure = max(0.0, min(1.0, self.network_exposure))
        self.safe_house_risk = max(0.0, min(1.0, self.safe_house_risk))


@dataclass
class ExecutionResult:
    """Complete mission execution result"""

    outcome: ExecutionOutcome
    success_score: float  # 0.0 to 1.0
    consequences: List[MissionConsequence]
    resources_consumed: ResourceCost
    intelligence_gained: List[Dict[str, Any]]
    agent_effects: Dict[str, Dict[str, Any]]  # agent_id -> effects
    narrative_summary: str
    political_impact: float
    reputation_changes: Dict[str, float]
    equipment_effects: Dict[str, Any]  # New: equipment effects and degradation


class MissionExecutionEngine:
    """Enhanced mission execution engine with spy network integration"""

    def __init__(self, game_state, equipment_manager):
        self.game_state = game_state
        self.execution_history = []
        self.network_compromise_tracker = {}
        self.equipment_manager = equipment_manager

    def execute_mission(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        resources: Dict[str, Any],
        agent_loadouts: Dict[str, AgentLoadout] = None,  # New parameter
    ) -> Dict[str, Any]:
        """Execute a mission with comprehensive outcome tracking and equipment integration"""

        # Initialize equipment integration
        if agent_loadouts is None:
            agent_loadouts = {}
            for agent in agents:
                agent_id = agent.get("id")
                if agent_id:
                    loadout = self.equipment_manager.create_agent_loadout(agent_id)
                    agent_loadouts[agent_id] = loadout

        # Apply equipment effects to mission
        equipment_effects = self.equipment_manager.apply_equipment_effects_to_mission(
            mission, agents, agent_loadouts
        )

        # Calculate base success probability with equipment modifiers
        base_success = self._calculate_base_success_with_equipment(
            mission, agents, location, equipment_effects
        )

        # Apply execution modifiers (emotional state, trauma, equipment)
        modified_success = self._apply_execution_modifiers_with_equipment(
            base_success, mission, agents, location, equipment_effects
        )

        # Determine outcome
        outcome = self._determine_outcome(modified_success)

        # Calculate resource costs including equipment
        resource_costs = self._calculate_resource_costs_with_equipment(
            mission, agents, outcome, equipment_effects
        )

        # Generate consequences including equipment consequences
        consequences = self._generate_mission_consequences_with_equipment(
            mission, agents, location, outcome, equipment_effects
        )

        # Apply network effects
        network_effects = self._apply_network_effects(mission, agents, outcome)

        # Generate narrative with equipment elements
        narrative = self._generate_mission_narrative_with_equipment(
            mission, agents, location, outcome, equipment_effects
        )

        # Track execution for patterns
        self._track_execution_patterns(mission, outcome, consequences)

        # Update agent loadouts with equipment degradation
        self._update_agent_loadouts(agent_loadouts, equipment_effects)

        return {
            "outcome": outcome,
            "success_probability": modified_success,
            "resource_costs": resource_costs,
            "consequences": consequences,
            "network_effects": network_effects,
            "narrative": narrative,
            "agents_affected": len(agents),
            "mission_type": mission.get("type", "unknown"),
            "equipment_effects": equipment_effects,  # New: equipment effects
            "agent_loadouts": agent_loadouts,  # New: updated loadouts
        }

    def _calculate_base_success_with_equipment(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        equipment_effects: Dict[str, Any],
    ) -> float:
        """Calculate base mission success probability with equipment integration"""

        # Get base success without equipment
        base_success = self._calculate_base_success(mission, agents, location)

        # Apply equipment success modifier
        equipment_success_modifier = equipment_effects.get("success_modifier", 0.0)
        base_success += equipment_success_modifier

        # Apply skill bonuses from equipment
        skill_bonuses = equipment_effects.get("skill_bonuses", {})
        for skill, bonus in skill_bonuses.items():
            # Convert skill bonus to success probability boost
            skill_boost = bonus * 0.1  # 10% of skill bonus becomes success boost
            base_success += skill_boost

        # Apply concealment effects for stealth missions
        mission_type = mission.get("type", "propaganda")
        if mission_type in ["intelligence", "sabotage"]:
            concealment_rating = equipment_effects.get("concealment_rating", 0.0)
            concealment_boost = concealment_rating * 0.15  # 15% boost from good concealment
            base_success += concealment_boost

        # Apply legal risk penalty
        legal_risk = equipment_effects.get("legal_risk", 0.0)
        legal_penalty = legal_risk * 0.1  # 10% penalty from high legal risk
        base_success -= legal_penalty

        return max(0.05, min(0.95, base_success))

    def _apply_execution_modifiers_with_equipment(
        self,
        base_success: float,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        equipment_effects: Dict[str, Any],
    ) -> float:
        """Apply situational modifiers including equipment effects"""

        modified_success = base_success

        # Emotional state modifiers
        for agent in agents:
            emotional_state = agent.get("emotional_state", {})
            trauma_level = emotional_state.get("trauma_level", 0.0)

            # Trauma reduces effectiveness
            trauma_penalty = trauma_level * 0.15
            modified_success -= trauma_penalty

            # Apply equipment emotional effects
            emotional_effects = equipment_effects.get("emotional_effects", {})
            for emotion, effect in emotional_effects.items():
                if emotion == "confidence" and effect > 0:
                    modified_success += effect * 0.05  # Confidence boosts success
                elif emotion == "fear" and effect > 0:
                    modified_success -= effect * 0.03  # Fear reduces success

        # Equipment degradation effects
        equipment_degradation = equipment_effects.get("equipment_degradation", {})
        for agent_id, degradation in equipment_degradation.items():
            for slot, result in degradation.items():
                if result.get("broken", False):
                    modified_success -= 0.1  # Broken equipment penalty
                elif result.get("maintenance_required", False):
                    modified_success -= 0.05  # Maintenance required penalty

        return max(0.05, min(0.95, modified_success))

    def _calculate_resource_costs_with_equipment(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        outcome: ExecutionOutcome,
        equipment_effects: Dict[str, Any],
    ) -> ResourceCost:
        """Calculate resource costs including equipment repair costs"""

        # Get base resource costs
        base_costs = self._calculate_resource_costs(mission, agents, outcome)

        # Add equipment repair costs
        equipment_repair_costs = 0.0
        equipment_degradation = equipment_effects.get("equipment_degradation", {})
        
        for agent_id, degradation in equipment_degradation.items():
            for slot, result in degradation.items():
                if result.get("broken", False) or result.get("maintenance_required", False):
                    # Estimate repair costs based on equipment value
                    equipment_repair_costs += result.get("repair_cost", 100)

        # Create enhanced resource cost
        enhanced_costs = ResourceCost(
            money=base_costs.money + int(equipment_repair_costs),
            equipment=base_costs.equipment,
            agent_time_hours=base_costs.agent_time_hours,
            network_exposure=base_costs.network_exposure,
            safe_house_risk=base_costs.safe_house_risk,
            equipment_repair_costs=equipment_repair_costs
        )

        return enhanced_costs

    def _generate_mission_consequences_with_equipment(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        outcome: ExecutionOutcome,
        equipment_effects: Dict[str, Any],
    ) -> List[MissionConsequence]:
        """Generate mission consequences including equipment-related consequences"""

        # Get base consequences
        consequences = self._generate_mission_consequences(mission, agents, location, outcome)

        # Add equipment-specific consequences
        equipment_consequences = self._generate_equipment_consequences(
            mission, agents, outcome, equipment_effects
        )
        consequences.extend(equipment_consequences)

        return consequences

    def _generate_equipment_consequences(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        outcome: ExecutionOutcome,
        equipment_effects: Dict[str, Any],
    ) -> List[MissionConsequence]:
        """Generate equipment-specific consequences"""

        consequences = []
        equipment_degradation = equipment_effects.get("equipment_degradation", {})
        
        # Check for broken equipment
        broken_equipment_count = 0
        for agent_id, degradation in equipment_degradation.items():
            for slot, result in degradation.items():
                if result.get("broken", False):
                    broken_equipment_count += 1

        if broken_equipment_count > 0:
            consequence = MissionConsequence(
                type=ConsequenceType.EQUIPMENT,
                description=f"{broken_equipment_count} pieces of equipment were destroyed",
                immediate_effects={
                    "equipment_loss": broken_equipment_count,
                    "repair_costs": equipment_effects.get("equipment_repair_costs", 0)
                },
                long_term_effects={
                    "equipment_shortage": broken_equipment_count * 0.1,
                    "maintenance_backlog": broken_equipment_count * 0.2
                },
                emotional_impact={
                    "frustration": 0.3,
                    "anxiety": 0.2
                },
                narrative_text=f"Critical equipment failure during the mission resulted in the loss of {broken_equipment_count} items.",
                severity=min(0.8, broken_equipment_count * 0.2)
            )
            consequences.append(consequence)

        # Check for maintenance requirements
        maintenance_required_count = 0
        for agent_id, degradation in equipment_degradation.items():
            for slot, result in degradation.items():
                if result.get("maintenance_required", False) and not result.get("broken", False):
                    maintenance_required_count += 1

        if maintenance_required_count > 0:
            consequence = MissionConsequence(
                type=ConsequenceType.EQUIPMENT,
                description=f"{maintenance_required_count} pieces of equipment need maintenance",
                immediate_effects={
                    "maintenance_required": maintenance_required_count,
                    "reduced_effectiveness": maintenance_required_count * 0.1
                },
                long_term_effects={
                    "maintenance_costs": maintenance_required_count * 50,
                    "equipment_reliability": -maintenance_required_count * 0.05
                },
                emotional_impact={
                    "concern": 0.2
                },
                narrative_text=f"Several pieces of equipment require immediate maintenance after the mission.",
                severity=min(0.5, maintenance_required_count * 0.1)
            )
            consequences.append(consequence)

        return consequences

    def _generate_mission_narrative_with_equipment(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        outcome: ExecutionOutcome,
        equipment_effects: Dict[str, Any],
    ) -> str:
        """Generate mission narrative including equipment elements"""

        # Get base narrative
        base_narrative = self._generate_mission_narrative(mission, agents, location, outcome)

        # Add equipment narrative elements
        equipment_narrative = equipment_effects.get("narrative_elements", [])
        
        if equipment_narrative:
            equipment_text = " Equipment-wise, " + ". ".join(equipment_narrative) + "."
            base_narrative += equipment_text

        # Add equipment effectiveness narrative
        success_modifier = equipment_effects.get("success_modifier", 0.0)
        if success_modifier > 0.1:
            base_narrative += " The team's equipment proved highly effective."
        elif success_modifier < -0.1:
            base_narrative += " Equipment issues hampered the team's effectiveness."

        return base_narrative

    def _update_agent_loadouts(
        self,
        agent_loadouts: Dict[str, AgentLoadout],
        equipment_effects: Dict[str, Any]
    ):
        """Update agent loadouts with equipment degradation results"""
        
        equipment_degradation = equipment_effects.get("equipment_degradation", {})
        
        for agent_id, degradation in equipment_degradation.items():
            loadout = agent_loadouts.get(agent_id)
            if loadout:
                # Loadout is already updated by the equipment manager
                # This method can be used for additional post-mission processing
                pass

    def get_equipment_analysis_for_mission(
        self,
        mission: Dict[str, Any],
        available_equipment: List[EnhancedEquipmentProfile]
    ) -> Dict[str, Any]:
        """Get equipment analysis and recommendations for a mission"""
        
        return self.equipment_manager.analyze_mission_equipment(mission, available_equipment)

    def get_equipment_maintenance_status(self) -> Dict[str, Any]:
        """Get current equipment maintenance status"""
        
        return self.equipment_manager.get_equipment_maintenance_report()

    def _calculate_base_success(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
    ) -> float:
        """Calculate base mission success probability"""

        # Agent skill assessment
        agent_competency = self._assess_agent_competency(mission, agents)

        # Location difficulty
        location_difficulty = self._assess_location_difficulty(mission, location)

        # Mission complexity
        complexity_modifier = self._get_complexity_modifier(mission)

        # Mission type base modifiers - REDUCED SABOTAGE DIFFICULTY
        mission_type = mission.get("type", "propaganda")
        type_base_modifiers = {
            "propaganda": 0.0,      # No modifier
            "intelligence": -0.05,   # Slightly harder
            "sabotage": -0.15,       # REDUCED from -0.25 to -0.15
            "recruitment": -0.05,    # Slightly harder
            "rescue": -0.20,         # Hard
            "assassination": -0.30,  # Very hard
        }
        
        type_modifier = type_base_modifiers.get(mission_type, 0.0)

        # Base success calculation with improved balance
        base_success = (
            (agent_competency * 0.6)
            + ((1.0 - location_difficulty) * 0.3)
            + (complexity_modifier * 0.1)
            + type_modifier  # Add mission type modifier
        )

        return max(0.05, min(0.95, base_success))

    def _apply_execution_modifiers(
        self,
        base_success: float,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
    ) -> float:
        """Apply situational modifiers to success probability"""

        modified_success = base_success

        # Emotional state modifiers
        for agent in agents:
            emotional_state = agent.get("emotional_state", {})
            trauma_level = emotional_state.get("trauma_level", 0.0)

            # Trauma reduces effectiveness
            trauma_penalty = trauma_level * 0.15
            modified_success -= trauma_penalty

            # Specific emotional impacts
            mission_type = mission.get("type", "propaganda")
            if mission_type in ["assassination", "sabotage"]:
                # Combat-related missions affected by fear
                fear_penalty = max(0, emotional_state.get("fear", 0)) * 0.1
                modified_success -= fear_penalty

                # But anger can help
                anger_bonus = max(0, emotional_state.get("anger", 0)) * 0.05
                modified_success += anger_bonus

            elif mission_type in ["recruitment", "propaganda"]:
                # Social missions affected by trust and joy
                trust_bonus = max(0, emotional_state.get("trust", 0)) * 0.08
                joy_bonus = max(0, emotional_state.get("joy", 0)) * 0.06
                modified_success += trust_bonus + joy_bonus

        # Mission type specific modifiers
        if mission.get("type") == "intelligence":
            # Intel missions benefit from patience and observation
            modified_success += 0.1 if len(agents) <= 2 else -0.05

        elif mission.get("type") == "sabotage":
            # SABOTAGE BALANCE: Reduced penalties and added bonuses
            # Smaller teams get coordination bonus
            if len(agents) <= 2:
                modified_success += 0.08  # REDUCED from 0.05
            # Equipment quality matters more for sabotage
            equipment_bonus = 0.0
            for agent in agents:
                if agent.get("equipment", {}).get("quality", 0) > 5:
                    equipment_bonus += 0.05
            modified_success += min(equipment_bonus, 0.15)  # Cap equipment bonus

        elif mission.get("type") == "rescue":
            # Rescue missions need speed and coordination
            if len(agents) >= 3:
                modified_success += 0.15
            else:
                modified_success -= 0.2

        # Environmental modifiers
        security_level = location.get("security_level", 5)
        if security_level > 7:
            modified_success -= 0.2
        elif security_level < 3:
            modified_success += 0.1

        return max(0.05, min(0.95, modified_success))

    def _determine_outcome(self, success_probability: float) -> ExecutionOutcome:
        """Determine mission outcome based on probability"""

        roll = random.random()

        if roll <= success_probability * 0.3:
            return ExecutionOutcome.PERFECT_SUCCESS
        elif roll <= success_probability * 0.7:
            return ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS
        elif roll <= success_probability:
            return ExecutionOutcome.PARTIAL_SUCCESS
        elif roll <= success_probability + 0.2:
            return ExecutionOutcome.FAILURE_WITH_INTEL
        elif roll <= success_probability + 0.4:
            return ExecutionOutcome.COMPLETE_FAILURE
        else:
            return ExecutionOutcome.CATASTROPHIC_FAILURE

    def _calculate_resource_costs(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        outcome: ExecutionOutcome,
    ) -> ResourceCost:
        """Calculate resources consumed during mission"""

        mission_type = mission.get("type", "propaganda")
        base_costs = {
            "propaganda": ResourceCost(
                money=500, equipment=1, agent_time_hours=8
            ),
            "sabotage": ResourceCost(
                money=2000, equipment=3, agent_time_hours=12
            ),
            "intelligence": ResourceCost(
                money=300, equipment=1, agent_time_hours=16
            ),
            "recruitment": ResourceCost(
                money=800, equipment=1, agent_time_hours=10
            ),
            "rescue": ResourceCost(
                money=3000, equipment=3, agent_time_hours=6
            ),
            "assassination": ResourceCost(
                money=5000, equipment=4, agent_time_hours=4
            ),
        }

        base_cost = base_costs.get(
            mission_type, ResourceCost(money=1000, agent_time_hours=8)
        )

        # Scale by number of agents
        multiplier = len(agents) * 0.7 + 0.3

        # Outcome modifiers
        outcome_modifiers = {
            ExecutionOutcome.PERFECT_SUCCESS: 0.8,  # Efficient execution
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS: 1.2,  # Extra resources needed
            ExecutionOutcome.PARTIAL_SUCCESS: 1.1,
            ExecutionOutcome.FAILURE_WITH_INTEL: 1.3,  # Wasted resources
            ExecutionOutcome.COMPLETE_FAILURE: 1.5,
            ExecutionOutcome.CATASTROPHIC_FAILURE: 2.0,
        }

        modifier = outcome_modifiers.get(outcome, 1.0)

        return ResourceCost(
            money=int(base_cost.money * multiplier * modifier),
            equipment=int(base_cost.equipment * multiplier * modifier),
            agent_time_hours=int(base_cost.agent_time_hours * multiplier * modifier),
            network_exposure=self._calculate_network_exposure(mission, outcome),
            safe_house_risk=self._calculate_safe_house_risk(mission, outcome),
        )

    def _calculate_network_exposure(
        self, mission: Dict[str, Any], outcome: ExecutionOutcome
    ) -> float:
        """Calculate how much the mission exposes the broader network"""
        mission_type = mission.get("type", "propaganda")
        base_exposure = {
            "propaganda": 0.1,
            "intelligence": 0.2,
            "sabotage": 0.4,
            "recruitment": 0.3,
            "rescue": 0.6,
            "assassination": 0.8,
        }.get(mission_type, 0.3)

        outcome_multipliers = {
            ExecutionOutcome.PERFECT_SUCCESS: 0.3,
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS: 0.7,
            ExecutionOutcome.PARTIAL_SUCCESS: 1.0,
            ExecutionOutcome.FAILURE_WITH_INTEL: 1.2,
            ExecutionOutcome.COMPLETE_FAILURE: 1.8,
            ExecutionOutcome.CATASTROPHIC_FAILURE: 3.0,
        }

        return base_exposure * outcome_multipliers.get(outcome, 1.0)

    def _calculate_safe_house_risk(
        self, mission: Dict[str, Any], outcome: ExecutionOutcome
    ) -> float:
        """Calculate risk to safe houses from mission"""
        mission_type = mission.get("type", "propaganda")
        base_risk = {
            "propaganda": 0.1,
            "sabotage": 0.3,
            "intelligence": 0.2,
            "recruitment": 0.15,
            "rescue": 0.4,
            "assassination": 0.6,
        }.get(mission_type, 0.3)

        outcome_multipliers = {
            ExecutionOutcome.PERFECT_SUCCESS: 0.5,
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS: 0.8,
            ExecutionOutcome.PARTIAL_SUCCESS: 1.0,
            ExecutionOutcome.COMPLETE_FAILURE: 1.5,
            ExecutionOutcome.CATASTROPHIC_FAILURE: 2.0,
        }

        return base_risk * outcome_multipliers.get(outcome, 1.0)

    def _generate_mission_consequences(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        outcome: ExecutionOutcome,
    ) -> List[MissionConsequence]:
        """Generate detailed mission consequences"""

        consequences = []
        mission_type = mission.get("type", "propaganda")

        # Mission type specific consequences
        if mission_type == "propaganda":
            consequences.extend(
                self._generate_propaganda_consequences(outcome, location)
            )
        elif mission_type == "sabotage":
            consequences.extend(self._generate_sabotage_consequences(outcome, location))
        elif mission_type == "assassination":
            consequences.extend(
                self._generate_assassination_consequences(outcome, location)
            )
        elif mission_type == "rescue":
            consequences.extend(self._generate_rescue_consequences(outcome, agents))
        elif mission_type == "intelligence":
            consequences.extend(
                self._generate_intelligence_consequences(outcome, location)
            )
        elif mission_type == "recruitment":
            consequences.extend(
                self._generate_recruitment_consequences(outcome, location)
            )

        # Universal consequences based on outcome
        consequences.extend(
            self._generate_universal_consequences(
                outcome,
                agents,
                self._calculate_resource_costs(mission, agents, outcome),
            )
        )

        return consequences

    def _generate_propaganda_consequences(
        self, outcome: ExecutionOutcome, location: Dict[str, Any]
    ) -> List[MissionConsequence]:
        """Generate propaganda mission consequences"""
        consequences = []

        if outcome in [
            ExecutionOutcome.PERFECT_SUCCESS,
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS,
        ]:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.SOCIAL,
                    description="Propaganda successfully distributed, public opinion shifts in favor",
                    immediate_effects={"public_support": 15, "recruitment_bonus": 10},
                    long_term_effects={"faction_reputation": 5},
                    emotional_impact={"joy": 0.3, "anticipation": 0.2},
                    narrative_text="The propaganda campaign resonates with the people. Support for the cause grows visibly in the streets.",
                    severity=0.6,
                )
            )

            # Possible government counter-response
            if outcome == ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS:
                consequences.append(
                    MissionConsequence(
                        type=ConsequenceType.POLITICAL,
                        description="Government launches counter-propaganda campaign",
                        immediate_effects={"government_attention": 10},
                        long_term_effects={"propaganda_difficulty": 5},
                        emotional_impact={"anger": 0.2},
                        narrative_text="The authorities respond with their own propaganda offensive, making future operations more challenging.",
                        severity=0.4,
                    )
                )

        elif outcome == ExecutionOutcome.PARTIAL_SUCCESS:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.SOCIAL,
                    description="Propaganda partially distributed, mixed public response",
                    immediate_effects={"public_support": 5, "confusion": 5},
                    long_term_effects={},
                    emotional_impact={"trust": -0.1, "anticipation": 0.1},
                    narrative_text="The message reaches some people, but the impact is limited. Mixed reactions from the public.",
                    severity=0.3,
                )
            )

        elif outcome in [
            ExecutionOutcome.COMPLETE_FAILURE,
            ExecutionOutcome.CATASTROPHIC_FAILURE,
        ]:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.REPUTATION,
                    description="Propaganda effort backfires, damages faction reputation",
                    immediate_effects={"public_support": -10, "faction_reputation": -8},
                    long_term_effects={"recruitment_difficulty": 10},
                    emotional_impact={"sadness": 0.4, "anger": 0.3},
                    narrative_text="The propaganda effort is exposed and ridiculed. Public opinion turns against the faction.",
                    severity=0.7,
                )
            )

        return consequences

    def _generate_sabotage_consequences(
        self, outcome: ExecutionOutcome, location: Dict[str, Any]
    ) -> List[MissionConsequence]:
        """Generate sabotage mission consequences"""
        consequences = []

        if outcome == ExecutionOutcome.PERFECT_SUCCESS:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.TACTICAL,
                    description="Target completely destroyed, no trace left behind",
                    immediate_effects={
                        "infrastructure_damage": 20,
                        "government_resources": -15,
                    },
                    long_term_effects={"strategic_advantage": 10},
                    emotional_impact={"joy": 0.4, "trust": 0.2},
                    narrative_text="The target is completely destroyed in a perfectly executed operation. No evidence points back to the faction.",
                    severity=0.8,
                )
            )

        elif outcome == ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.TACTICAL,
                    description="Target damaged but evidence left behind",
                    immediate_effects={"infrastructure_damage": 15, "heat_level": 10},
                    long_term_effects={"security_response": 8},
                    emotional_impact={"joy": 0.3, "fear": 0.2},
                    narrative_text="The sabotage succeeds but leaves traces. Authorities launch investigation.",
                    severity=0.6,
                )
            )

        elif outcome == ExecutionOutcome.CATASTROPHIC_FAILURE:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.PERSONNEL,
                    description="Saboteurs captured, major security crackdown initiated",
                    immediate_effects={
                        "agents_captured": 1,
                        "heat_level": 25,
                        "safe_houses_compromised": 2,
                    },
                    long_term_effects={
                        "operation_difficulty": 15,
                        "recruitment_difficulty": 20,
                    },
                    emotional_impact={"fear": 0.6, "anger": 0.4, "sadness": 0.3},
                    narrative_text="The sabotage fails catastrophically. Agents are captured and the authorities launch a massive crackdown.",
                    severity=1.0,
                )
            )

        return consequences

    def _generate_assassination_consequences(
        self, outcome: ExecutionOutcome, location: Dict[str, Any]
    ) -> List[MissionConsequence]:
        """Generate assassination mission consequences"""
        consequences = []

        if outcome == ExecutionOutcome.PERFECT_SUCCESS:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.POLITICAL,
                    description="Target eliminated, creates power vacuum and confusion",
                    immediate_effects={
                        "political_chaos": 20,
                        "government_effectiveness": -15,
                    },
                    long_term_effects={
                        "strategic_advantage": 15,
                        "faction_reputation": 10,
                    },
                    emotional_impact={"joy": 0.3, "fear": 0.2, "anticipation": 0.4},
                    narrative_text="The assassination creates chaos in government ranks. The faction gains significant strategic advantage.",
                    severity=0.9,
                )
            )

            # But also increases heat significantly
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.TACTICAL,
                    description="Massive manhunt launched for assassins",
                    immediate_effects={"heat_level": 30, "security_presence": 20},
                    long_term_effects={"operation_difficulty": 25},
                    emotional_impact={"fear": 0.4},
                    narrative_text="The successful assassination triggers an unprecedented manhunt. All operations become more dangerous.",
                    severity=0.8,
                )
            )

        elif outcome in [
            ExecutionOutcome.COMPLETE_FAILURE,
            ExecutionOutcome.CATASTROPHIC_FAILURE,
        ]:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.POLITICAL,
                    description="Failed assassination attempt backfires dramatically",
                    immediate_effects={
                        "government_support": 15,
                        "public_support": -20,
                        "heat_level": 35,
                    },
                    long_term_effects={
                        "faction_reputation": -25,
                        "recruitment_difficulty": 30,
                    },
                    emotional_impact={"anger": 0.5, "sadness": 0.4, "fear": 0.3},
                    narrative_text="The failed assassination attempt rallies support for the government and turns public opinion against the faction.",
                    severity=1.0,
                )
            )

        return consequences

    def _generate_intelligence_consequences(
        self, outcome: ExecutionOutcome, location: Dict[str, Any]
    ) -> List[MissionConsequence]:
        """Generate intelligence mission consequences"""
        consequences = []

        if outcome == ExecutionOutcome.PERFECT_SUCCESS:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.INTELLIGENCE,
                    description="Valuable intelligence gathered successfully",
                    immediate_effects={"intelligence_value": 20},
                    long_term_effects={"strategic_knowledge": 10},
                    emotional_impact={"joy": 0.3, "anticipation": 0.2},
                    narrative_text="High-value intelligence is successfully extracted without detection.",
                    severity=0.5,
                )
            )

        return consequences

    def _generate_recruitment_consequences(
        self, outcome: ExecutionOutcome, location: Dict[str, Any]
    ) -> List[MissionConsequence]:
        """Generate recruitment mission consequences"""
        consequences = []

        if outcome in [
            ExecutionOutcome.PERFECT_SUCCESS,
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS,
        ]:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.PERSONNEL,
                    description="New recruits successfully recruited to the cause",
                    immediate_effects={
                        "new_recruits": 3
                        if outcome == ExecutionOutcome.PERFECT_SUCCESS
                        else 1
                    },
                    long_term_effects={"operational_capacity": 5},
                    emotional_impact={"joy": 0.2, "trust": 0.1},
                    narrative_text="New members join the faction, increasing operational capacity.",
                    severity=0.4,
                )
            )

        return consequences

    def _generate_universal_consequences(
        self,
        outcome: ExecutionOutcome,
        agents: List[Dict[str, Any]],
        resources: ResourceCost,
    ) -> List[MissionConsequence]:
        """Generate consequences that apply to all mission types"""
        consequences = []

        if outcome == ExecutionOutcome.CATASTROPHIC_FAILURE:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.RESOURCE,
                    description="Significant resources lost due to mission failure",
                    immediate_effects={"resource_loss": resources.money},
                    long_term_effects={"operational_capacity": -5},
                    emotional_impact={"sadness": 0.3, "anger": 0.2},
                    narrative_text="The failed mission results in significant resource losses.",
                    severity=0.6,
                )
            )

        return consequences

    def _apply_network_effects(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        outcome: ExecutionOutcome,
    ) -> Dict[str, Any]:
        """Apply spy network effects and coordination bonuses"""

        effects = {
            "network_exposure": 0.0,
            "intelligence_gathered": [],
            "network_coordination_bonus": 0.0,
            "counter_intelligence_triggered": False,
            "safe_house_compromise_risk": 0.0,
        }

        # Calculate network coordination effects
        if len(agents) > 1:
            # Multi-agent missions benefit from network coordination
            coordination_bonus = min(0.3, len(agents) * 0.1)
            effects["network_coordination_bonus"] = coordination_bonus

        # Spy network intelligence gathering during missions
        mission_type = mission.get("type", "unknown")
        if mission_type in ["intelligence", "reconnaissance"]:
            # Intelligence missions can gather additional intel
            intel_gathered = []

            if outcome in [
                ExecutionOutcome.PERFECT_SUCCESS,
                ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS,
            ]:
                # Successful intel missions provide multiple intelligence types
                intel_types = [
                    "security_patterns",
                    "personnel_movements",
                    "communication_intercepts",
                ]
                for intel_type in intel_types:
                    if random.random() < 0.6:  # 60% chance per type
                        intel_gathered.append(
                            {
                                "type": intel_type,
                                "reliability": 0.8
                                if outcome == ExecutionOutcome.PERFECT_SUCCESS
                                else 0.6,
                                "urgency": random.randint(3, 8),
                                "actionable": random.random() < 0.7,
                            }
                        )

            effects["intelligence_gathered"] = intel_gathered

        # Network exposure calculations
        base_exposure = self._calculate_network_exposure(mission, outcome)

        # Spy network operational security modifiers
        if hasattr(self.game_state, "spy_network_system"):
            # If spy network system exists, use its OPSEC calculations
            try:
                spy_system = self.game_state.spy_network_system
                if hasattr(spy_system, "calculate_opsec_risk"):
                    opsec_risk = spy_system.calculate_opsec_risk(mission, agents)
                    base_exposure *= 1.0 + opsec_risk
            except Exception:
                pass  # Fallback to base calculation

        effects["network_exposure"] = base_exposure

        # Counter-intelligence triggering
        if base_exposure > 0.6 and outcome in [
            ExecutionOutcome.COMPLETE_FAILURE,
            ExecutionOutcome.CATASTROPHIC_FAILURE,
        ]:
            effects["counter_intelligence_triggered"] = True
            effects["safe_house_compromise_risk"] = base_exposure * 0.8

        # Network resilience effects
        if outcome == ExecutionOutcome.CATASTROPHIC_FAILURE:
            # Catastrophic failures can compromise multiple network elements
            effects["network_cascade_risk"] = base_exposure * 1.5
            effects["communication_compromise"] = random.random() < base_exposure
            effects["asset_exposure"] = random.random() < (base_exposure * 0.7)

        return effects

    def _track_execution_patterns(
        self,
        mission: Dict[str, Any],
        outcome: ExecutionOutcome,
        consequences: List[MissionConsequence],
    ) -> None:
        """Track mission execution patterns for AI learning"""

        execution_record = {
            "mission_type": mission.get("type"),
            "outcome": outcome.value,
            "turn": self.game_state.turn_number
            if hasattr(self.game_state, "turn_number")
            else 0,
            "consequences_count": len(consequences),
            "severity_total": sum(c.severity for c in consequences),
            "location_id": mission.get("location_id"),
            "agent_count": len(mission.get("participants", [])),
        }

        self.execution_history.append(execution_record)

        # Keep only recent history (last 50 missions)
        if len(self.execution_history) > 50:
            self.execution_history = self.execution_history[-50:]

    def get_mission_success_patterns(self, mission_type: str = None) -> Dict[str, Any]:
        """Analyze historical mission success patterns"""

        relevant_missions = self.execution_history
        if mission_type:
            relevant_missions = [
                m for m in self.execution_history if m["mission_type"] == mission_type
            ]

        if not relevant_missions:
            return {"total_missions": 0, "success_rate": 0.0, "average_severity": 0.0}

        successful_outcomes = [
            "PERFECT_SUCCESS",
            "SUCCESS_WITH_COMPLICATIONS",
            "PARTIAL_SUCCESS",
        ]
        successes = sum(
            1 for m in relevant_missions if m["outcome"] in successful_outcomes
        )

        return {
            "total_missions": len(relevant_missions),
            "success_rate": successes / len(relevant_missions),
            "average_severity": sum(m["severity_total"] for m in relevant_missions)
            / len(relevant_missions),
            "most_common_outcome": max(
                set(m["outcome"] for m in relevant_missions),
                key=lambda x: sum(1 for m in relevant_missions if m["outcome"] == x),
            ),
        }

    # Helper methods
    def _assess_agent_competency(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> float:
        """Assess agent competency for mission type"""
        if not agents:
            return 0.1

        total_competency = 0
        for agent in agents:
            skills = agent.get("skills", {})
            mission_type = mission.get("type", "propaganda")

            # Map mission types to relevant skills
            relevant_skills = {
                "propaganda": ["social", "intelligence"],
                "sabotage": ["technical", "stealth"],
                "assassination": ["combat", "stealth"],
                "rescue": ["combat", "medical"],
                "intelligence": ["intelligence", "stealth"],
                "recruitment": ["social", "intelligence"],
            }.get(mission_type, ["intelligence"])

            agent_competency = 0
            for skill in relevant_skills:
                # Handle both float and dict skill formats
                skill_value = skills.get(skill, 0.0)
                if isinstance(skill_value, dict):
                    # Dict format: {"level": 0.7, "experience": 100}
                    skill_level = skill_value.get("level", 0.0)
                else:
                    # Float format: 0.7
                    skill_level = float(skill_value)
                
                agent_competency += skill_level / 5.0  # Normalize to 0-1

            total_competency += agent_competency / len(relevant_skills)

        return total_competency / len(agents)

    def _assess_location_difficulty(
        self, mission: Dict[str, Any], location: Dict[str, Any]
    ) -> float:
        """Assess location-based mission difficulty"""
        security_level = location.get("security_level", 5)
        surveillance_level = location.get("surveillance_level", 5)

        # Normalize to 0-1 scale where 1 is most difficult
        difficulty = (security_level + surveillance_level) / 20.0
        return min(1.0, max(0.0, difficulty))

    def _get_complexity_modifier(self, mission: Dict[str, Any]) -> float:
        """Get mission complexity modifier"""
        complexity = mission.get("complexity", 5)
        # Normalize to 0-1 scale where 1 is optimal complexity
        return 1.0 - abs(complexity - 5) / 5.0

    def _generate_mission_narrative(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        outcome: ExecutionOutcome,
    ) -> str:
        """Generate comprehensive narrative summary"""

        agent_names = [agent.get("name", "Unknown") for agent in agents]
        mission_name = mission.get("type", "operation").replace("_", " ").title()

        outcome_intros = {
            ExecutionOutcome.PERFECT_SUCCESS: f"The {mission_name} by {', '.join(agent_names)} exceeded all expectations.",
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS: f"The {mission_name} succeeded, though not without complications.",
            ExecutionOutcome.PARTIAL_SUCCESS: f"The {mission_name} achieved some of its objectives.",
            ExecutionOutcome.FAILURE_WITH_INTEL: f"While the {mission_name} failed, valuable intelligence was gathered.",
            ExecutionOutcome.COMPLETE_FAILURE: f"The {mission_name} failed to achieve its objectives.",
            ExecutionOutcome.CATASTROPHIC_FAILURE: f"The {mission_name} ended in disaster.",
        }

        intro = outcome_intros.get(outcome, f"The {mission_name} concluded.")

        # Add consequence narratives
        consequence_texts = [
            c.narrative_text
            for c in self._generate_mission_consequences(
                mission, agents, location, outcome
            )
            if c.narrative_text
        ]

        if consequence_texts:
            full_narrative = intro + " " + " ".join(consequence_texts)
        else:
            full_narrative = intro

        return full_narrative

    def _calculate_political_impact(
        self,
        mission: Dict[str, Any],
        consequences: List[MissionConsequence],
        outcome: ExecutionOutcome,
    ) -> float:
        """Calculate political impact of mission"""
        base_impact = {
            ExecutionOutcome.PERFECT_SUCCESS: 0.3,
            ExecutionOutcome.SUCCESS_WITH_COMPLICATIONS: 0.2,
            ExecutionOutcome.PARTIAL_SUCCESS: 0.1,
            ExecutionOutcome.FAILURE_WITH_INTEL: -0.1,
            ExecutionOutcome.COMPLETE_FAILURE: -0.2,
            ExecutionOutcome.CATASTROPHIC_FAILURE: -0.4,
        }.get(outcome, 0.0)

        # Mission type modifiers
        mission_type = mission.get("type", "propaganda")
        type_modifiers = {
            "assassination": 2.0,
            "sabotage": 1.5,
            "propaganda": 1.2,
            "rescue": 1.1,
            "intelligence": 0.8,
            "recruitment": 0.9,
        }

        modifier = type_modifiers.get(mission_type, 1.0)
        return base_impact * modifier

    def _calculate_reputation_changes(
        self,
        mission: Dict[str, Any],
        consequences: List[MissionConsequence],
        outcome: ExecutionOutcome,
    ) -> Dict[str, float]:
        """Calculate reputation changes from mission"""
        changes = {"faction": 0.0, "public": 0.0, "government": 0.0}

        for consequence in consequences:
            for effect, value in consequence.immediate_effects.items():
                if "reputation" in effect:
                    changes["faction"] += value / 10.0
                elif "public_support" in effect:
                    changes["public"] += value / 10.0
                elif "government" in effect:
                    changes["government"] += value / 10.0

        return changes

    def _generate_rescue_consequences(
        self, outcome: ExecutionOutcome, agents: List[Dict[str, Any]]
    ) -> List[MissionConsequence]:
        """Generate rescue mission consequences"""
        consequences = []

        if outcome == ExecutionOutcome.PERFECT_SUCCESS:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.PERSONNEL,
                    description="Rescue successful, valuable operative saved",
                    immediate_effects={"operative_rescued": 1, "morale_boost": 15},
                    long_term_effects={"faction_loyalty": 10},
                    emotional_impact={"joy": 0.5, "trust": 0.3},
                    narrative_text="The rescue operation succeeds flawlessly, saving a valuable member and boosting faction morale.",
                    severity=0.7,
                )
            )

        elif outcome == ExecutionOutcome.CATASTROPHIC_FAILURE:
            consequences.append(
                MissionConsequence(
                    type=ConsequenceType.PERSONNEL,
                    description="Rescue fails, additional operatives captured",
                    immediate_effects={"operatives_lost": 2, "morale_damage": -20},
                    long_term_effects={
                        "faction_loyalty": -15,
                        "recruitment_difficulty": 15,
                    },
                    emotional_impact={"sadness": 0.6, "anger": 0.4, "fear": 0.3},
                    narrative_text="The rescue attempt fails catastrophically, resulting in additional losses and damaged morale.",
                    severity=1.0,
                )
            )

        return consequences
