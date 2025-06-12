"""
Years of Lead - Spy Network System

Advanced spy network management with agent recruitment, loyalty tracking,
and operational security mechanics that integrate with existing systems.
"""

import random
import uuid
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Types of spy agents in the network"""

    ASSET = "asset"  # Recruited civilian with access
    INFORMANT = "informant"  # Paid information source
    DOUBLE_AGENT = "double_agent"  # Working for multiple sides
    SLEEPER_AGENT = "sleeper_agent"  # Deep cover, inactive until needed
    HANDLER = "handler"  # Manages other agents
    COURIER = "courier"  # Moves information/materials
    SABOTEUR = "saboteur"  # Specialist in disruption
    INFILTRATOR = "infiltrator"  # Deep cover in target organizations


class LoyaltyState(Enum):
    """Agent loyalty levels"""

    LOYAL = "loyal"  # Completely trusted
    WAVERING = "wavering"  # Loyalty in question
    COMPROMISED = "compromised"  # Known to authorities
    TURNED = "turned"  # Working for the other side
    BURNED = "burned"  # Exposed and unusable


class RecruitmentMethod(Enum):
    """Methods for recruiting new agents"""

    IDEOLOGICAL = "ideological"  # Shared beliefs
    FINANCIAL = "financial"  # Money motivation
    BLACKMAIL = "blackmail"  # Coercion
    ROMANTIC = "romantic"  # Personal relationships
    FAMILY = "family"  # Family connections
    PROFESSIONAL = "professional"  # Career advancement


@dataclass
class SpyAgent:
    """Individual spy agent in the network"""

    id: str
    code_name: str
    real_name: str
    agent_type: AgentType
    loyalty_state: LoyaltyState

    # Skills and capabilities
    access_level: int = 1  # 1-10, what they can access
    reliability: float = 0.7  # 0.0-1.0, how dependable
    stealth_rating: float = 0.5  # 0.0-1.0, how well they avoid detection
    stress_level: float = 0.3  # 0.0-1.0, current psychological pressure

    # Operational details
    cover_identity: str = ""  # Their cover story/job
    location: str = ""  # Where they operate
    handler_id: Optional[str] = None  # Who manages them
    recruitment_method: Optional[RecruitmentMethod] = None
    recruitment_turn: int = 0  # When they were recruited

    # Risk factors
    exposure_risk: float = 0.1  # 0.0-1.0, chance of being discovered
    burn_risk: float = 0.05  # 0.0-1.0, chance of being exposed

    # Network connections
    contacts: Set[str] = field(default_factory=set)  # Other agent IDs they know
    assets: Dict[str, Any] = field(default_factory=dict)  # Resources they control

    # Performance tracking
    missions_completed: int = 0
    intelligence_gathered: int = 0
    operations_compromised: int = 0

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.code_name:
            self.code_name = f"Asset-{random.randint(1000, 9999)}"

    def get_effectiveness(self) -> float:
        """Calculate overall agent effectiveness"""
        base_effectiveness = (self.reliability + self.stealth_rating) / 2

        # Loyalty affects effectiveness
        loyalty_modifiers = {
            LoyaltyState.LOYAL: 1.0,
            LoyaltyState.WAVERING: 0.7,
            LoyaltyState.COMPROMISED: 0.3,
            LoyaltyState.TURNED: 0.0,
            LoyaltyState.BURNED: 0.0,
        }

        loyalty_modifier = loyalty_modifiers.get(self.loyalty_state, 0.5)

        # Stress reduces effectiveness
        stress_penalty = self.stress_level * 0.3

        return max(0.0, base_effectiveness * loyalty_modifier - stress_penalty)

    def apply_stress(self, stress_amount: float, source: str = "general"):
        """Apply stress to the agent"""
        self.stress_level = min(1.0, self.stress_level + stress_amount)

        # High stress can affect loyalty
        if self.stress_level > 0.8:
            if random.random() < 0.1:  # 10% chance per stress application
                if self.loyalty_state == LoyaltyState.LOYAL:
                    self.loyalty_state = LoyaltyState.WAVERING
                elif self.loyalty_state == LoyaltyState.WAVERING:
                    self.loyalty_state = LoyaltyState.COMPROMISED

    def recover_stress(self, recovery_amount: float = 0.1):
        """Natural stress recovery over time"""
        self.stress_level = max(0.0, self.stress_level - recovery_amount)

    def check_loyalty_shift(self) -> Optional[LoyaltyState]:
        """Check if agent loyalty changes"""
        old_state = self.loyalty_state

        # Various factors that can affect loyalty
        factors = {
            "stress": self.stress_level > 0.7,
            "exposure": self.exposure_risk > 0.6,
            "missions_failed": self.operations_compromised > 2,
            "long_service": (self.missions_completed - self.recruitment_turn) > 20,
        }

        risk_factors = sum(factors.values())

        if risk_factors >= 2 and random.random() < 0.15:
            # Loyalty degradation
            if self.loyalty_state == LoyaltyState.LOYAL:
                self.loyalty_state = LoyaltyState.WAVERING
            elif self.loyalty_state == LoyaltyState.WAVERING:
                self.loyalty_state = LoyaltyState.COMPROMISED

        return self.loyalty_state if self.loyalty_state != old_state else None


@dataclass
class NetworkCell:
    """Organizational unit within the spy network"""

    id: str
    name: str
    location: str
    agents: Set[str] = field(default_factory=set)
    security_level: int = 5  # 1-10
    communication_methods: List[str] = field(default_factory=list)
    safe_houses: List[str] = field(default_factory=list)
    operational_status: str = "active"  # active, dormant, compromised
    last_contact: int = 0  # Turn number of last communication


@dataclass
class NetworkStatus:
    """Overall network health and security status"""

    operational_security: float = 0.8  # 0.0-1.0
    communication_security: float = 0.7
    counter_intelligence_threat: float = 0.3
    network_coverage: float = 0.6  # How much of the target area is covered
    active_agents: int = 0
    compromised_agents: int = 0
    burned_agents: int = 0


class SpyNetworkSystem:
    """Advanced spy network management system"""

    def __init__(self, game_state=None):
        self.game_state = game_state
        self.agents: Dict[str, SpyAgent] = {}
        self.cells: Dict[str, NetworkCell] = {}
        self.network_status = NetworkStatus()
        self.recruitment_queue: List[Dict[str, Any]] = []
        self.active_operations: List[Dict[str, Any]] = []
        self.burn_list: Set[str] = set()  # Agents that need to be extracted

        # Network configuration
        self.max_cell_size = 7  # Maximum agents per cell for security
        self.stress_recovery_rate = 0.05  # Per turn stress recovery
        self.loyalty_check_frequency = 5  # Turns between loyalty checks

    def recruit_agent(
        self,
        target_profile: Dict[str, Any],
        method: RecruitmentMethod,
        recruiter_id: Optional[str] = None,
    ) -> Optional[SpyAgent]:
        """Recruit a new agent to the network"""

        # Calculate recruitment success chance
        base_success = 0.6

        # Method affects success rate
        method_modifiers = {
            RecruitmentMethod.IDEOLOGICAL: 0.8,
            RecruitmentMethod.FINANCIAL: 0.7,
            RecruitmentMethod.BLACKMAIL: 0.9,
            RecruitmentMethod.ROMANTIC: 0.6,
            RecruitmentMethod.FAMILY: 0.85,
            RecruitmentMethod.PROFESSIONAL: 0.65,
        }

        success_chance = base_success * method_modifiers.get(method, 0.6)

        # Recruiter skill affects success
        if recruiter_id and recruiter_id in self.agents:
            recruiter = self.agents[recruiter_id]
            success_chance *= 1.0 + recruiter.get_effectiveness() * 0.3

        # Network security affects recruitment difficulty
        if self.network_status.counter_intelligence_threat > 0.5:
            success_chance *= 0.7

        if random.random() > success_chance:
            logger.info("Agent recruitment failed")
            return None

        # Create new agent
        agent = SpyAgent(
            id=str(uuid.uuid4()),
            code_name=self._generate_code_name(),
            real_name=target_profile.get("name", "Unknown"),
            agent_type=target_profile.get("type", AgentType.ASSET),
            loyalty_state=LoyaltyState.LOYAL,
            access_level=target_profile.get("access_level", 2),
            reliability=random.uniform(0.5, 0.9),
            stealth_rating=random.uniform(0.4, 0.8),
            cover_identity=target_profile.get("cover", "Civilian"),
            location=target_profile.get("location", "unknown"),
            handler_id=recruiter_id,
            recruitment_method=method,
            recruitment_turn=getattr(self.game_state, "turn_number", 0),
        )

        self.agents[agent.id] = agent
        self._assign_to_cell(agent)
        self._update_network_status()

        logger.info(
            f"Successfully recruited agent {agent.code_name} via {method.value}"
        )
        return agent

    def assign_mission(
        self, agent_id: str, mission_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assign a mission to a specific agent"""

        if agent_id not in self.agents:
            return {"success": False, "reason": "Agent not found"}

        agent = self.agents[agent_id]

        # Check if agent is capable of the mission
        if agent.loyalty_state in [LoyaltyState.TURNED, LoyaltyState.BURNED]:
            return {"success": False, "reason": "Agent is compromised"}

        if agent.stress_level > 0.9:
            return {"success": False, "reason": "Agent is too stressed"}

        mission_type = mission_details.get("type", "intelligence")
        mission_risk = mission_details.get("risk", 0.3)

        # Calculate mission success probability
        success_chance = agent.get_effectiveness()

        # Mission type modifiers
        type_modifiers = {
            "intelligence": 1.0,
            "sabotage": 0.8,
            "infiltration": 0.9,
            "courier": 1.1,
            "surveillance": 1.0,
        }

        success_chance *= type_modifiers.get(mission_type, 1.0)

        # Execute mission
        mission_success = random.random() < success_chance

        if mission_success:
            agent.missions_completed += 1
            if mission_type == "intelligence":
                agent.intelligence_gathered += 1

            # Stress from successful mission
            agent.apply_stress(mission_risk * 0.3, "mission_success")

            return {
                "success": True,
                "outcome": "success",
                "intelligence": mission_details.get("intelligence_value", 10),
                "exposure_increase": mission_risk * 0.1,
            }
        else:
            agent.operations_compromised += 1
            agent.apply_stress(mission_risk * 0.7, "mission_failure")

            # Check for exposure
            if random.random() < mission_risk * 0.4:
                agent.exposure_risk = min(1.0, agent.exposure_risk + 0.2)
                if agent.exposure_risk > 0.8:
                    agent.loyalty_state = LoyaltyState.COMPROMISED
                    self.burn_list.add(agent_id)

            return {
                "success": False,
                "outcome": "failure",
                "exposure_increase": mission_risk * 0.3,
                "stress_increase": mission_risk * 0.7,
            }

    def process_turn(self) -> Dict[str, Any]:
        """Process spy network events for a game turn"""
        turn_results = {
            "agent_updates": [],
            "loyalty_changes": [],
            "burned_agents": [],
            "network_events": [],
            "intelligence_gathered": 0,
        }

        # Process each agent
        for agent_id, agent in self.agents.items():
            # Natural stress recovery
            agent.recover_stress(self.stress_recovery_rate)

            # Check for loyalty shifts
            if (
                getattr(self.game_state, "turn_number", 0)
                % self.loyalty_check_frequency
                == 0
            ):
                loyalty_change = agent.check_loyalty_shift()
                if loyalty_change:
                    turn_results["loyalty_changes"].append(
                        {
                            "agent_id": agent_id,
                            "code_name": agent.code_name,
                            "old_loyalty": agent.loyalty_state.value,
                            "new_loyalty": loyalty_change.value,
                        }
                    )

            # Check if agent needs to be burned
            if agent.exposure_risk > 0.9 or agent.loyalty_state == LoyaltyState.BURNED:
                if agent_id not in self.burn_list:
                    self.burn_list.add(agent_id)
                    turn_results["burned_agents"].append(
                        {
                            "agent_id": agent_id,
                            "code_name": agent.code_name,
                            "reason": "high_exposure"
                            if agent.exposure_risk > 0.9
                            else "loyalty_compromised",
                        }
                    )

        # Process burned agents
        for agent_id in list(self.burn_list):
            self._burn_agent(agent_id)
            turn_results["network_events"].append(
                f"Agent {self.agents.get(agent_id, {}).get('code_name', 'Unknown')} has been burned and extracted"
            )

        # Update network status
        self._update_network_status()

        # Generate intelligence from active agents
        intelligence = self._generate_passive_intelligence()
        turn_results["intelligence_gathered"] = intelligence

        return turn_results

    def get_network_analysis(self) -> Dict[str, Any]:
        """Get comprehensive network analysis"""

        agent_breakdown = {
            "total": len(self.agents),
            "by_type": {},
            "by_loyalty": {},
            "by_location": {},
            "average_effectiveness": 0.0,
            "high_risk_agents": 0,
        }

        effectiveness_sum = 0

        for agent in self.agents.values():
            # By type
            agent_type = agent.agent_type.value
            agent_breakdown["by_type"][agent_type] = (
                agent_breakdown["by_type"].get(agent_type, 0) + 1
            )

            # By loyalty
            loyalty = agent.loyalty_state.value
            agent_breakdown["by_loyalty"][loyalty] = (
                agent_breakdown["by_loyalty"].get(loyalty, 0) + 1
            )

            # By location
            location = agent.location or "unknown"
            agent_breakdown["by_location"][location] = (
                agent_breakdown["by_location"].get(location, 0) + 1
            )

            # Effectiveness
            effectiveness_sum += agent.get_effectiveness()

            # High risk
            if agent.exposure_risk > 0.6 or agent.stress_level > 0.8:
                agent_breakdown["high_risk_agents"] += 1

        if len(self.agents) > 0:
            agent_breakdown["average_effectiveness"] = effectiveness_sum / len(
                self.agents
            )

        return {
            "network_status": {
                "operational_security": self.network_status.operational_security,
                "counter_intelligence_threat": self.network_status.counter_intelligence_threat,
                "network_coverage": self.network_status.network_coverage,
            },
            "agents": agent_breakdown,
            "cells": {
                "total": len(self.cells),
                "active": len(
                    [c for c in self.cells.values() if c.operational_status == "active"]
                ),
                "compromised": len(
                    [
                        c
                        for c in self.cells.values()
                        if c.operational_status == "compromised"
                    ]
                ),
            },
        }

    def _generate_code_name(self) -> str:
        """Generate a code name for a new agent"""
        adjectives = [
            "Swift",
            "Silent",
            "Deep",
            "Sharp",
            "Quick",
            "Ghost",
            "Shadow",
            "Steel",
        ]
        nouns = ["Eagle", "Wolf", "Fox", "Raven", "Hawk", "Lion", "Bear", "Tiger"]

        return f"{random.choice(adjectives)}{random.choice(nouns)}"

    def _assign_to_cell(self, agent: SpyAgent):
        """Assign agent to appropriate cell"""

        # Find a cell in the same location with space
        for cell in self.cells.values():
            if (
                cell.location == agent.location
                and len(cell.agents) < self.max_cell_size
                and cell.operational_status == "active"
            ):
                cell.agents.add(agent.id)
                return

        # Create new cell if needed
        cell_id = f"cell_{len(self.cells) + 1}"
        new_cell = NetworkCell(
            id=cell_id,
            name=f"Cell {len(self.cells) + 1}",
            location=agent.location,
            agents={agent.id},
            communication_methods=["dead_drop", "coded_message"],
            last_contact=getattr(self.game_state, "turn_number", 0),
        )

        self.cells[cell_id] = new_cell

    def _burn_agent(self, agent_id: str):
        """Remove an agent from the network (burned/compromised)"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.loyalty_state = LoyaltyState.BURNED

            # Remove from cells
            for cell in self.cells.values():
                if agent_id in cell.agents:
                    cell.agents.remove(agent_id)

            # Remove from burn list
            self.burn_list.discard(agent_id)

            logger.info(f"Agent {agent.code_name} has been burned")

    def _update_network_status(self):
        """Update overall network status"""
        if not self.agents:
            return

        # Calculate operational security
        loyal_agents = sum(
            1 for a in self.agents.values() if a.loyalty_state == LoyaltyState.LOYAL
        )
        compromised_agents = sum(
            1
            for a in self.agents.values()
            if a.loyalty_state in [LoyaltyState.COMPROMISED, LoyaltyState.TURNED]
        )

        self.network_status.active_agents = loyal_agents
        self.network_status.compromised_agents = compromised_agents

        if len(self.agents) > 0:
            self.network_status.operational_security = loyal_agents / len(self.agents)

        # Calculate counter-intelligence threat
        avg_exposure = sum(a.exposure_risk for a in self.agents.values()) / len(
            self.agents
        )
        self.network_status.counter_intelligence_threat = min(1.0, avg_exposure * 1.2)

        # Calculate coverage
        covered_locations = len(
            set(
                a.location
                for a in self.agents.values()
                if a.loyalty_state == LoyaltyState.LOYAL
            )
        )
        total_locations = len(set(a.location for a in self.agents.values())) or 1
        self.network_status.network_coverage = covered_locations / total_locations

    def _generate_passive_intelligence(self) -> int:
        """Generate intelligence from routine agent operations"""
        intelligence_value = 0

        for agent in self.agents.values():
            if (
                agent.loyalty_state == LoyaltyState.LOYAL
                and agent.stress_level < 0.7
                and random.random() < agent.get_effectiveness() * 0.3
            ):
                # Generate intelligence based on agent access level
                intelligence_value += agent.access_level * random.randint(1, 3)

        return intelligence_value


# Integration functions for the main game
def integrate_with_mission_system(
    spy_network: SpyNetworkSystem, mission_execution_engine
):
    """Integrate spy network with existing mission execution system"""

    def enhanced_mission_execution(mission, agents, location, resources):
        """Enhanced mission execution with spy network support"""

        # Check if we have spy assets in the target location
        local_agents = [
            a
            for a in spy_network.agents.values()
            if a.location == location.get("name", "")
            and a.loyalty_state == LoyaltyState.LOYAL
        ]

        # Spy network can provide intelligence bonus
        intelligence_bonus = 0
        for spy_agent in local_agents:
            if spy_agent.agent_type == AgentType.INFORMANT:
                intelligence_bonus += spy_agent.access_level * 0.1

        # Execute mission with original system
        result = mission_execution_engine.execute_mission(
            mission, agents, location, resources
        )

        # Add spy network effects
        if intelligence_bonus > 0:
            result["intelligence_bonus"] = intelligence_bonus
            result["success_probability"] = min(
                0.95, result.get("success_probability", 0.5) + intelligence_bonus
            )

        # Apply stress to local spy agents based on mission heat
        mission_heat = result.get("network_effects", {}).get("network_compromise", 0.0)
        for spy_agent in local_agents:
            spy_agent.apply_stress(mission_heat * 0.5, "mission_proximity")

        return result

    return enhanced_mission_execution
