"""
Years of Lead - Enhanced Agent Decision System

Integrates agent AI with mission execution, intelligence system,
emotional states, and relationship dynamics for complete autonomous behavior.
"""

import random
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .mission_execution_engine import MissionExecutionEngine
from .intelligence_system import (
    IntelligenceDatabase,
    IntelligenceType,
)

logger = logging.getLogger(__name__)


@dataclass
class AgentDecision:
    """Enhanced decision structure with full system integration"""

    action_type: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = None
    priority: float = 0.5  # 0.0 to 1.0
    emotional_motivation: Dict[str, float] = None
    expected_outcome: str = ""
    risk_level: float = 0.0
    intelligence_basis: Optional[str] = None
    relationship_factor: float = 0.0
    reasoning: str = ""

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.emotional_motivation is None:
            self.emotional_motivation = {}


@dataclass
class DecisionResult:
    """Result of executing an agent decision"""

    success: bool
    effects: Dict[str, Any]
    narrative: str = ""
    relationship_changes: Dict[str, float] = None
    emotional_impact: Dict[str, float] = None

    def __post_init__(self):
        if self.relationship_changes is None:
            self.relationship_changes = {}
        if self.emotional_impact is None:
            self.emotional_impact = {}


class EnhancedAgentDecisionSystem:
    """Complete agent decision system with full game integration"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.mission_engine = MissionExecutionEngine(game_state)
        self.intelligence_db = IntelligenceDatabase()
        self.decision_history: Dict[str, List[AgentDecision]] = {}

    def make_agent_decision(self, agent_id: str) -> Optional[AgentDecision]:
        """Make a comprehensive decision for an agent using all available systems"""

        agent = self.game_state.agents.get(agent_id)
        if not agent or agent.status != "active":
            return None

        # Gather comprehensive agent context
        context = self._analyze_agent_context(agent)

        # Generate possible decisions using all systems
        possible_decisions = self._generate_comprehensive_decisions(agent, context)

        # Evaluate decisions with full context
        best_decision = self._evaluate_and_select_decision(
            agent, possible_decisions, context
        )

        if best_decision:
            # Track decision history
            if agent_id not in self.decision_history:
                self.decision_history[agent_id] = []
            self.decision_history[agent_id].append(best_decision)

            # Keep only recent decisions
            if len(self.decision_history[agent_id]) > 10:
                self.decision_history[agent_id] = self.decision_history[agent_id][-10:]

        return best_decision

    def execute_decision(
        self, agent_id: str, decision: AgentDecision
    ) -> DecisionResult:
        """Execute a decision with full system integration"""

        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return DecisionResult(success=False, effects={"error": "Agent not found"})

        try:
            if decision.action_type == "execute_mission":
                return self._execute_mission_decision(agent, decision)
            elif decision.action_type == "gather_intelligence":
                return self._execute_intelligence_decision(agent, decision)
            elif decision.action_type == "build_relationship":
                return self._execute_relationship_decision(agent, decision)
            elif decision.action_type == "manage_emotional_state":
                return self._execute_emotional_decision(agent, decision)
            elif decision.action_type == "faction_activity":
                return self._execute_faction_decision(agent, decision)
            else:
                return self._execute_general_decision(agent, decision)

        except Exception as e:
            logger.error(f"Error executing decision for {agent_id}: {e}")
            return DecisionResult(success=False, effects={"error": str(e)})

    def _analyze_agent_context(self, agent) -> Dict[str, Any]:
        """Analyze comprehensive agent context using all systems"""

        context = {
            "emotional_state": self._analyze_emotional_context(agent),
            "relationships": self._analyze_relationship_context(agent),
            "intelligence": self._analyze_intelligence_context(agent),
            "faction": self._analyze_faction_context(agent),
            "mission_readiness": self._analyze_mission_readiness(agent),
            "environmental_factors": self._analyze_environmental_context(agent),
        }

        return context

    def _analyze_emotional_context(self, agent) -> Dict[str, Any]:
        """Analyze agent's emotional state and needs"""

        emotional_state = getattr(agent, "emotional_state", None)
        if not emotional_state:
            return {"dominant_emotion": "neutral", "stability": 1.0, "needs": []}

        dominant_emotion, intensity = emotional_state.get_dominant_emotion()
        stability = emotional_state.get_emotional_stability()

        needs = []
        if emotional_state.trauma_level > 0.6:
            needs.append("trauma_recovery")
        if stability < 0.4:
            needs.append("emotional_stability")
        if emotional_state.fear > 0.7:
            needs.append("safety")
        if emotional_state.trust < -0.5:
            needs.append("trust_rebuilding")

        return {
            "dominant_emotion": dominant_emotion,
            "intensity": intensity,
            "stability": stability,
            "trauma_level": emotional_state.trauma_level,
            "combat_effectiveness": emotional_state.get_combat_effectiveness(),
            "social_effectiveness": emotional_state.get_social_effectiveness(),
            "needs": needs,
        }

    def _analyze_relationship_context(self, agent) -> Dict[str, Any]:
        """Analyze agent's relationship network and social needs"""

        relationships = getattr(agent, "relationships", {})
        strong_allies = []
        potential_threats = []
        neutral_contacts = []

        for other_id, relationship in relationships.items():
            if hasattr(relationship, "affinity") and hasattr(relationship, "trust"):
                if relationship.affinity > 60 and relationship.trust > 0.7:
                    strong_allies.append(other_id)
                elif relationship.affinity < -30 or relationship.trust < 0.3:
                    potential_threats.append(other_id)
                else:
                    neutral_contacts.append(other_id)

        return {
            "strong_allies": strong_allies,
            "potential_threats": potential_threats,
            "neutral_contacts": neutral_contacts,
            "social_isolation": len(strong_allies) == 0,
            "trust_deficit": len(potential_threats) > len(strong_allies),
            "network_size": len(relationships),
        }

    def _analyze_intelligence_context(self, agent) -> Dict[str, Any]:
        """Analyze available intelligence and information needs"""

        recent_intel = self.intelligence_db.get_recent_events(24)
        critical_intel = self.intelligence_db.get_critical_events()
        patterns = self.intelligence_db.get_patterns()

        intelligence_gaps = []
        if (
            len(
                [e for e in recent_intel if e.type == IntelligenceType.SECURITY_CHANGES]
            )
            == 0
        ):
            intelligence_gaps.append("security_status")
        if (
            len(
                [
                    e
                    for e in recent_intel
                    if e.type == IntelligenceType.GOVERNMENT_MOVEMENT
                ]
            )
            == 0
        ):
            intelligence_gaps.append("government_activity")

        return {
            "recent_events_count": len(recent_intel),
            "critical_events_count": len(critical_intel),
            "patterns_detected": len(patterns),
            "intelligence_gaps": intelligence_gaps,
            "threat_level": self.intelligence_db.threat_assessments.get(
                "overall", {}
            ).get("level", "LOW"),
        }

    def _analyze_mission_readiness(self, agent) -> Dict[str, Any]:
        """Analyze agent's readiness for different mission types"""

        emotional_context = self._analyze_emotional_context(agent)

        readiness = {
            "propaganda": max(
                0.0, min(1.0, 0.7 + emotional_context["social_effectiveness"] * 0.3)
            ),
            "intelligence": max(
                0.0, min(1.0, 0.6 + (1.0 - emotional_context["intensity"]) * 0.4)
            ),
            "sabotage": max(
                0.0, min(1.0, 0.5 + emotional_context["combat_effectiveness"] * 0.5)
            ),
            "recruitment": max(
                0.0, min(1.0, 0.6 + emotional_context["social_effectiveness"] * 0.4)
            ),
            "rescue": max(
                0.0, min(1.0, 0.4 + emotional_context["combat_effectiveness"] * 0.6)
            ),
        }

        return {
            "mission_readiness": readiness,
            "best_mission_type": max(readiness, key=readiness.get),
            "overall_readiness": sum(readiness.values()) / len(readiness),
        }

    def _analyze_faction_context(self, agent) -> Dict[str, Any]:
        """Analyze faction status and needs"""

        faction = self.game_state.factions.get(agent.faction_id)
        if not faction:
            return {"status": "unknown", "needs": []}

        faction_agents = [
            a
            for a in self.game_state.agents.values()
            if a.faction_id == agent.faction_id
        ]

        needs = []
        if getattr(faction, "resources", {}).get("money", 0) < 1000:
            needs.append("funding")
        if len(faction_agents) < 5:
            needs.append("recruitment")
        if hasattr(self.game_state, "get_faction_cohesion"):
            cohesion = self.game_state.get_faction_cohesion(agent.faction_id)
            if cohesion < 0.5:
                needs.append("unity")

        return {
            "faction_size": len(faction_agents),
            "faction_needs": needs,
            "agent_loyalty": getattr(agent, "loyalty", 50),
        }

    def _analyze_environmental_context(self, agent) -> Dict[str, Any]:
        """Analyze environmental threats and opportunities"""

        location = self.game_state.locations.get(agent.location_id)
        threats = []
        opportunities = []

        if location:
            security_level = getattr(location, "security_level", 5)
            if security_level > 7:
                threats.append("high_security")
            elif security_level < 3:
                opportunities.append("low_security_operations")

        # Check reputation system integration
        if hasattr(self.game_state, "reputation_system"):
            search_prob = (
                self.game_state.reputation_system.calculate_search_probability(
                    agent.id, agent.location_id
                )
            )
            if search_prob > 0.7:
                threats.append("high_search_probability")

        return {
            "threats": threats,
            "opportunities": opportunities,
            "location_security": getattr(location, "security_level", 5)
            if location
            else 5,
        }

    def _generate_comprehensive_decisions(
        self, agent, context: Dict[str, Any]
    ) -> List[AgentDecision]:
        """Generate all possible decisions using comprehensive context"""

        decisions = []

        # Emotional-driven decisions
        emotional_needs = context["emotional_state"]["needs"]
        if "trauma_recovery" in emotional_needs:
            decisions.append(
                AgentDecision(
                    action_type="manage_emotional_state",
                    parameters={"activity": "trauma_recovery"},
                    priority=0.9,
                    emotional_motivation={
                        "trauma": context["emotional_state"]["trauma_level"]
                    },
                    reasoning="High trauma level requires recovery time",
                )
            )

        if "safety" in emotional_needs:
            decisions.append(
                AgentDecision(
                    action_type="seek_safety",
                    priority=0.8,
                    emotional_motivation={
                        "fear": context["emotional_state"].get("fear", 0)
                    },
                    reasoning="High fear levels require safety measures",
                )
            )

        # Mission-driven decisions
        mission_readiness = context["mission_readiness"]
        if mission_readiness["overall_readiness"] > 0.6:
            best_mission = mission_readiness["best_mission_type"]
            decisions.append(
                AgentDecision(
                    action_type="execute_mission",
                    parameters={"mission_type": best_mission},
                    priority=0.7,
                    reasoning=f"Ready for {best_mission} mission (readiness: {mission_readiness['mission_readiness'][best_mission]:.2f})",
                )
            )

        # Intelligence-driven decisions
        intel_context = context["intelligence"]
        if "security_status" in intel_context["intelligence_gaps"]:
            decisions.append(
                AgentDecision(
                    action_type="gather_intelligence",
                    parameters={"intel_type": "security_changes"},
                    priority=0.6,
                    intelligence_basis="security_gap",
                    reasoning="Need intelligence on current security status",
                )
            )

        # Relationship-driven decisions
        relationship_context = context["relationships"]
        if relationship_context["social_isolation"]:
            decisions.append(
                AgentDecision(
                    action_type="build_relationship",
                    priority=0.5,
                    relationship_factor=1.0,
                    reasoning="Social isolation requires new alliances",
                )
            )

        # Faction-driven decisions
        faction_context = context["faction"]
        if "funding" in faction_context["faction_needs"]:
            decisions.append(
                AgentDecision(
                    action_type="faction_activity",
                    parameters={"activity": "fundraising"},
                    priority=0.4,
                    reasoning="Faction needs funding",
                )
            )

        return decisions

    def _evaluate_and_select_decision(
        self, agent, decisions: List[AgentDecision], context: Dict[str, Any]
    ) -> Optional[AgentDecision]:
        """Evaluate decisions with comprehensive scoring"""

        if not decisions:
            return None

        scored_decisions = []

        for decision in decisions:
            score = self._calculate_comprehensive_score(agent, decision, context)
            scored_decisions.append((score, decision))

        # Sort by score and return best
        scored_decisions.sort(key=lambda x: x[0], reverse=True)
        return scored_decisions[0][1]

    def _calculate_comprehensive_score(
        self, agent, decision: AgentDecision, context: Dict[str, Any]
    ) -> float:
        """Calculate comprehensive decision score"""

        score = decision.priority * 100  # Base priority score

        # Emotional alignment bonus
        emotional_state = context["emotional_state"]
        if decision.emotional_motivation:
            for emotion, intensity in decision.emotional_motivation.items():
                if emotion == emotional_state["dominant_emotion"]:
                    score += intensity * 50

        # Risk penalty based on current stability
        risk_penalty = decision.risk_level * emotional_state["stability"] * 30
        score -= risk_penalty

        # Relationship factor bonus
        score += decision.relationship_factor * 20

        # Mission readiness bonus
        if decision.action_type == "execute_mission":
            mission_type = decision.parameters.get("mission_type", "")
            readiness = context["mission_readiness"]["mission_readiness"].get(
                mission_type, 0.5
            )
            score += readiness * 30

        # Intelligence urgency bonus
        if (
            decision.intelligence_basis
            and context["intelligence"]["threat_level"] == "HIGH"
        ):
            score += 25

        return score

    def _execute_mission_decision(
        self, agent, decision: AgentDecision
    ) -> DecisionResult:
        """Execute a mission decision"""

        mission_type = decision.parameters.get("mission_type", "propaganda")
        location = list(self.game_state.locations.values())[0]  # Use first location

        mission = {
            "type": mission_type,
            "target_location": location.id,
            "priority": "medium",
        }

        agent_data = {
            "id": agent.id,
            "name": agent.name,
            "skills": getattr(agent, "skills", {}),
            "emotional_state": getattr(agent, "emotional_state", {}).__dict__
            if hasattr(getattr(agent, "emotional_state", {}), "__dict__")
            else {},
        }

        location_data = {
            "name": location.name,
            "security_level": getattr(location, "security_level", 5),
        }

        result = self.mission_engine.execute_mission(
            mission, [agent_data], location_data, {}
        )

        # Apply emotional impact from mission
        if hasattr(agent, "emotional_state") and result.get("consequences"):
            for consequence in result["consequences"]:
                if consequence.get("emotional_impact"):
                    agent.emotional_state.apply_emotional_impact(
                        consequence["emotional_impact"]
                    )

        return DecisionResult(
            success=result["outcome"]
            in ["perfect_success", "success_with_complications", "partial_success"],
            effects={
                "mission_outcome": result["outcome"].value
                if hasattr(result["outcome"], "value")
                else str(result["outcome"])
            },
            narrative=f"{agent.name} executed {mission_type} mission with outcome: {result['outcome']}",
        )

    def _execute_intelligence_decision(
        self, agent, decision: AgentDecision
    ) -> DecisionResult:
        """Execute an intelligence gathering decision"""

        # Apply skill check for intelligence gathering
        intelligence_success = random.random() < 0.7  # Base 70% success

        if intelligence_success:
            # Add intelligence to database (simplified)
            narrative = f"{agent.name} successfully gathered intelligence about {decision.parameters.get('intel_type', 'general situation')}"

            return DecisionResult(
                success=True,
                effects={
                    "intelligence_gained": decision.parameters.get(
                        "intel_type", "general"
                    )
                },
                narrative=narrative,
            )
        else:
            return DecisionResult(
                success=False,
                effects={"intelligence_failed": True},
                narrative=f"{agent.name} failed to gather useful intelligence",
            )

    def _execute_relationship_decision(
        self, agent, decision: AgentDecision
    ) -> DecisionResult:
        """Execute a relationship building decision"""

        # Find suitable target for relationship building
        potential_targets = [
            a
            for a in self.game_state.agents.values()
            if a.id != agent.id and a.faction_id == agent.faction_id
        ]

        if not potential_targets:
            return DecisionResult(
                success=False,
                effects={"no_targets": True},
                narrative=f"{agent.name} found no suitable targets for relationship building",
            )

        target = random.choice(potential_targets)

        # Update relationship
        if hasattr(self.game_state, "update_relationship"):
            self.game_state.update_relationship(
                agent.id, target.id, delta_affinity=10, delta_trust=0.1
            )

        return DecisionResult(
            success=True,
            effects={"relationship_improved": target.id},
            narrative=f"{agent.name} built stronger relationship with {target.name}",
            relationship_changes={target.id: 10},
        )

    def _execute_emotional_decision(
        self, agent, decision: AgentDecision
    ) -> DecisionResult:
        """Execute an emotional management decision"""

        activity = decision.parameters.get("activity", "rest")

        if hasattr(agent, "emotional_state"):
            if activity == "trauma_recovery":
                # Reduce trauma slightly
                agent.emotional_state.trauma_level = max(
                    0, agent.emotional_state.trauma_level - 0.1
                )
                narrative = f"{agent.name} takes time to process trauma and recover"

            elif activity == "stress_relief":
                # Reduce negative emotions
                agent.emotional_state.fear = max(-1.0, agent.emotional_state.fear - 0.2)
                agent.emotional_state.anger = max(
                    -1.0, agent.emotional_state.anger - 0.2
                )
                narrative = f"{agent.name} engages in stress relief activities"

            return DecisionResult(
                success=True,
                effects={"emotional_improvement": activity},
                narrative=narrative,
                emotional_impact={activity: 0.1},
            )

        return DecisionResult(
            success=False,
            effects={"no_emotional_state": True},
            narrative=f"{agent.name} attempts self-care but has no emotional tracking",
        )

    def _execute_faction_decision(
        self, agent, decision: AgentDecision
    ) -> DecisionResult:
        """Execute a faction-related decision"""

        activity = decision.parameters.get("activity", "general_support")

        if activity == "fundraising":
            # Simulate fundraising success
            success = random.random() < 0.6
            if success:
                amount = random.randint(200, 800)
                return DecisionResult(
                    success=True,
                    effects={"funds_raised": amount},
                    narrative=f"{agent.name} raised {amount} credits for the faction",
                )
            else:
                return DecisionResult(
                    success=False,
                    effects={"fundraising_failed": True},
                    narrative=f"{agent.name}'s fundraising efforts were unsuccessful",
                )

        return DecisionResult(
            success=True,
            effects={"faction_support": activity},
            narrative=f"{agent.name} contributed to faction {activity}",
        )

    def _execute_general_decision(
        self, agent, decision: AgentDecision
    ) -> DecisionResult:
        """Execute a general decision"""

        return DecisionResult(
            success=True,
            effects={"general_action": decision.action_type},
            narrative=f"{agent.name} performed {decision.action_type}",
        )


def integrate_agent_decisions(game_state):
    """Integration function to add enhanced agent decisions to game state"""

    decision_system = EnhancedAgentDecisionSystem(game_state)

    # Add decision system to game state
    game_state.agent_decision_system = decision_system

    return decision_system
