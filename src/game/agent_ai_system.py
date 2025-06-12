"""
Years of Lead - Advanced Agent AI System

Autonomous decision-making for agents based on emotional state,
relationships, faction goals, and environmental factors.
"""

import random
import logging
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class DecisionPriority(Enum):
    """Priority levels for agent decisions"""

    CRITICAL = "critical"  # Life-threatening, immediate action required
    HIGH = "high"  # Important faction goals, time-sensitive
    MEDIUM = "medium"  # Regular operations, relationship maintenance
    LOW = "low"  # Personal goals, skill development


class AgentGoal(Enum):
    """Types of goals agents can pursue"""

    SURVIVAL = "survival"
    FACTION_ADVANCEMENT = "faction_advancement"
    PERSONAL_RELATIONSHIP = "personal_relationship"
    SKILL_DEVELOPMENT = "skill_development"
    REVENGE = "revenge"
    IDEOLOGICAL_COMMITMENT = "ideological_commitment"
    FINANCIAL_SECURITY = "financial_security"
    INFORMATION_GATHERING = "information_gathering"


@dataclass
class Decision:
    """A decision an agent can make"""

    action_type: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = None
    priority: DecisionPriority = DecisionPriority.MEDIUM
    emotional_motivation: Dict[str, float] = None
    expected_outcome: str = ""
    risk_level: float = 0.0

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.emotional_motivation is None:
            self.emotional_motivation = {}


class AgentAI:
    """Advanced AI decision-making system for individual agents"""

    def __init__(self, agent_id: str, game_state):
        self.agent_id = agent_id
        self.game_state = game_state
        self.current_goals: List[AgentGoal] = []
        self.decision_history: List[Decision] = []
        self.stress_threshold = 0.8
        self.relationship_threshold = 0.6

    def make_decision(self) -> Optional[Decision]:
        """Make an autonomous decision based on current state"""

        agent = self.game_state.agents.get(self.agent_id)
        if not agent:
            return None

        # Assess current situation
        situation = self._assess_situation(agent)

        # Generate possible decisions
        possible_decisions = self._generate_possible_decisions(agent, situation)

        # Evaluate and rank decisions
        ranked_decisions = self._evaluate_decisions(
            agent, possible_decisions, situation
        )

        # Select best decision
        if ranked_decisions:
            best_decision = ranked_decisions[0]
            self.decision_history.append(best_decision)

            # Keep only recent history
            if len(self.decision_history) > 20:
                self.decision_history = self.decision_history[-20:]

            return best_decision

        return None

    def _assess_situation(self, agent) -> Dict[str, Any]:
        """Assess the agent's current situation"""

        situation = {
            "emotional_state": self._analyze_emotional_state(agent),
            "relationships": self._analyze_relationships(agent),
            "faction_status": self._analyze_faction_status(agent),
            "environmental_threats": self._assess_threats(agent),
            "opportunities": self._identify_opportunities(agent),
            "resource_status": self._assess_resources(agent),
        }

        return situation

    def _analyze_emotional_state(self, agent) -> Dict[str, Any]:
        """Analyze agent's current emotional state"""

        emotional_state = getattr(agent, "emotional_state", None)
        if not emotional_state:
            return {
                "dominant_emotion": "neutral",
                "stability": "stable",
                "stress_level": 0.0,
            }

        # Find dominant emotion
        emotions = {
            "fear": getattr(emotional_state, "fear", 0.0),
            "anger": getattr(emotional_state, "anger", 0.0),
            "sadness": getattr(emotional_state, "sadness", 0.0),
            "joy": getattr(emotional_state, "joy", 0.0),
            "trust": getattr(emotional_state, "trust", 0.0),
            "anticipation": getattr(emotional_state, "anticipation", 0.0),
        }

        dominant_emotion = max(emotions.keys(), key=lambda k: emotions[k])
        trauma_level = getattr(emotional_state, "trauma_level", 0.0)

        # Determine stability
        max_emotion = max(emotions.values())
        stability = "unstable" if max_emotion > 0.8 or trauma_level > 0.7 else "stable"

        return {
            "dominant_emotion": dominant_emotion,
            "emotion_intensity": max_emotion,
            "stability": stability,
            "trauma_level": trauma_level,
            "stress_level": trauma_level * 0.5 + max_emotion * 0.3,
        }

    def _analyze_relationships(self, agent) -> Dict[str, Any]:
        """Analyze agent's relationship network"""

        relationships = getattr(agent, "relationships", {})

        if hasattr(self.game_state, "get_social_circle"):
            self.game_state.get_social_circle(agent.id)

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
            "network_size": len(relationships),
        }

    def _analyze_faction_status(self, agent) -> Dict[str, Any]:
        """Analyze agent's standing within their faction"""

        faction = self.game_state.factions.get(agent.faction_id)
        if not faction:
            return {"status": "unknown", "influence": 0.0}

        # Calculate agent's influence within faction
        faction_agents = [
            a
            for a in self.game_state.agents.values()
            if a.faction_id == agent.faction_id
        ]
        agent_rank = 0.5  # Default middle rank

        if hasattr(agent, "reputation") or hasattr(agent, "influence"):
            # Compare with other faction members
            agent_influence = getattr(agent, "influence", 0.5)
            other_influences = [
                getattr(a, "influence", 0.5) for a in faction_agents if a.id != agent.id
            ]

            if other_influences:
                agent_rank = sum(
                    1 for inf in other_influences if agent_influence > inf
                ) / len(other_influences)

        return {
            "faction_name": faction.name,
            "faction_resources": getattr(faction, "resources", {}),
            "agent_rank": agent_rank,
            "faction_size": len(faction_agents),
            "faction_status": getattr(faction, "status", "active"),
        }

    def _assess_threats(self, agent) -> List[Dict[str, Any]]:
        """Assess environmental and personal threats"""

        threats = []

        # Location-based threats
        location = self.game_state.locations.get(agent.location_id)
        if location:
            security_level = getattr(location, "security_level", 5)
            if security_level > 7:
                threats.append(
                    {
                        "type": "high_security",
                        "severity": (security_level - 5) / 5.0,
                        "source": "location_security",
                        "description": f"High security presence in {location.name}",
                    }
                )

        # Relationship-based threats
        emotional_state = self._analyze_emotional_state(agent)
        if emotional_state["trauma_level"] > 0.6:
            threats.append(
                {
                    "type": "psychological_breakdown",
                    "severity": emotional_state["trauma_level"],
                    "source": "internal",
                    "description": "High trauma levels threatening mental stability",
                }
            )

        return threats

    def _identify_opportunities(self, agent) -> List[Dict[str, Any]]:
        """Identify current opportunities for the agent"""

        opportunities = []

        # Skill development opportunities
        if hasattr(agent, "skills"):
            for skill_name, skill_level in agent.skills.__dict__.items():
                if skill_level < 8:  # Room for improvement
                    opportunities.append(
                        {
                            "type": "skill_development",
                            "target": skill_name,
                            "potential": (10 - skill_level) / 10.0,
                            "description": f"Improve {skill_name} skill",
                        }
                    )

        # Relationship opportunities
        relationships_analysis = self._analyze_relationships(agent)
        if len(relationships_analysis["strong_allies"]) < 3:
            opportunities.append(
                {
                    "type": "relationship_building",
                    "target": "new_allies",
                    "potential": 0.7,
                    "description": "Build stronger alliances",
                }
            )

        return opportunities

    def _assess_resources(self, agent) -> Dict[str, Any]:
        """Assess agent's available resources"""

        return {
            "financial": getattr(agent, "money", 0),
            "equipment": getattr(agent, "equipment", {}),
            "contacts": len(getattr(agent, "relationships", {})),
            "skills_total": sum(
                getattr(agent.skills, attr, 0)
                for attr in dir(agent.skills)
                if not attr.startswith("_")
            )
            if hasattr(agent, "skills")
            else 0,
        }

    def _generate_possible_decisions(self, agent, situation) -> List[Decision]:
        """Generate all possible decisions for the current situation"""

        decisions = []

        # Critical decisions (survival, urgent threats)
        for threat in situation["threats"]:
            if threat["severity"] > 0.7:
                decisions.append(
                    Decision(
                        action_type="avoid_threat",
                        target=threat["source"],
                        priority=DecisionPriority.CRITICAL,
                        risk_level=threat["severity"],
                        expected_outcome="threat_mitigation",
                    )
                )

        # Emotional-driven decisions
        emotional_state = situation["emotional_state"]
        dominant_emotion = emotional_state["dominant_emotion"]

        if dominant_emotion == "fear" and emotional_state["emotion_intensity"] > 0.6:
            decisions.append(
                Decision(
                    action_type="seek_safety",
                    priority=DecisionPriority.HIGH,
                    emotional_motivation={"fear": emotional_state["emotion_intensity"]},
                    expected_outcome="reduced_fear",
                )
            )

        elif dominant_emotion == "anger" and emotional_state["emotion_intensity"] > 0.6:
            # Look for revenge or confrontation opportunities
            for threat_agent in situation["relationships"]["potential_threats"]:
                decisions.append(
                    Decision(
                        action_type="confront",
                        target=threat_agent,
                        priority=DecisionPriority.HIGH,
                        emotional_motivation={
                            "anger": emotional_state["emotion_intensity"]
                        },
                        risk_level=0.6,
                        expected_outcome="emotional_release",
                    )
                )

        elif (
            dominant_emotion == "sadness" and emotional_state["emotion_intensity"] > 0.5
        ):
            decisions.append(
                Decision(
                    action_type="seek_comfort",
                    target=random.choice(situation["relationships"]["strong_allies"])
                    if situation["relationships"]["strong_allies"]
                    else None,
                    priority=DecisionPriority.MEDIUM,
                    emotional_motivation={
                        "sadness": emotional_state["emotion_intensity"]
                    },
                    expected_outcome="emotional_support",
                )
            )

        # Relationship-driven decisions
        if situation["relationships"]["social_isolation"]:
            decisions.append(
                Decision(
                    action_type="build_relationship",
                    priority=DecisionPriority.MEDIUM,
                    expected_outcome="expanded_network",
                    risk_level=0.2,
                )
            )

        # Opportunity-driven decisions
        for opportunity in situation["opportunities"]:
            if opportunity["potential"] > 0.5:
                decisions.append(
                    Decision(
                        action_type=opportunity["type"],
                        target=opportunity.get("target"),
                        priority=DecisionPriority.MEDIUM,
                        expected_outcome="self_improvement",
                        risk_level=0.1,
                    )
                )

        # Faction-driven decisions
        faction_status = situation["faction_status"]
        if faction_status["agent_rank"] < 0.3:  # Low rank, try to improve
            decisions.append(
                Decision(
                    action_type="faction_mission",
                    priority=DecisionPriority.HIGH,
                    expected_outcome="increased_reputation",
                    risk_level=0.4,
                )
            )

        return decisions

    def _evaluate_decisions(
        self, agent, decisions: List[Decision], situation: Dict[str, Any]
    ) -> List[Decision]:
        """Evaluate and rank decisions by utility"""

        scored_decisions = []

        for decision in decisions:
            score = self._calculate_decision_score(agent, decision, situation)
            scored_decisions.append((score, decision))

        # Sort by score (highest first)
        scored_decisions.sort(key=lambda x: x[0], reverse=True)

        return [decision for score, decision in scored_decisions]

    def _calculate_decision_score(
        self, agent, decision: Decision, situation: Dict[str, Any]
    ) -> float:
        """Calculate utility score for a decision"""

        score = 0.0

        # Priority weight
        priority_weights = {
            DecisionPriority.CRITICAL: 100.0,
            DecisionPriority.HIGH: 50.0,
            DecisionPriority.MEDIUM: 20.0,
            DecisionPriority.LOW: 5.0,
        }
        score += priority_weights.get(decision.priority, 10.0)

        # Risk penalty
        risk_penalty = decision.risk_level * 30.0
        score -= risk_penalty

        # Emotional alignment bonus
        emotional_state = situation["emotional_state"]
        if decision.emotional_motivation:
            for emotion, intensity in decision.emotional_motivation.items():
                if emotion == emotional_state["dominant_emotion"]:
                    score += intensity * 25.0  # Bonus for addressing dominant emotion

        # Personality-based modifiers
        if hasattr(agent, "traits"):
            traits = agent.traits
            if hasattr(traits, "primary_trait"):
                trait = traits.primary_trait

                # Adjust score based on personality
                if (
                    str(trait).lower() in ["reckless", "aggressive"]
                    and decision.risk_level < 0.3
                ):
                    score -= 10.0  # Reckless agents prefer higher risk
                elif (
                    str(trait).lower() in ["cautious", "careful"]
                    and decision.risk_level > 0.5
                ):
                    score -= 20.0  # Cautious agents avoid high risk

        # Resource consideration
        resources = situation["resource_status"]
        if (
            decision.action_type in ["faction_mission", "build_relationship"]
            and resources["financial"] < 100
        ):
            score -= 15.0  # Financial constraints

        return score


class AgentAIDirector:
    """Manages AI for all agents in the game"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.agent_ais: Dict[str, AgentAI] = {}

    def process_agent_ai_turn(self) -> Dict[str, Any]:
        """Process AI decisions for all agents"""

        results = {
            "decisions_made": [],
            "agent_status_changes": [],
            "relationship_changes": [],
            "narrative_events": [],
        }

        # Process each active agent
        for agent_id, agent in self.game_state.agents.items():
            if agent.status != "active":
                continue

            # Get or create AI for this agent
            if agent_id not in self.agent_ais:
                self.agent_ais[agent_id] = AgentAI(agent_id, self.game_state)

            agent_ai = self.agent_ais[agent_id]

            # Make decision
            decision = agent_ai.make_decision()
            if decision:
                # Execute decision
                execution_result = self._execute_decision(agent, decision)

                results["decisions_made"].append(
                    {
                        "agent_id": agent_id,
                        "agent_name": agent.name,
                        "action": decision.action_type,
                        "target": decision.target,
                        "result": execution_result,
                    }
                )

                # Generate narrative
                narrative = self._generate_decision_narrative(
                    agent, decision, execution_result
                )
                if narrative:
                    results["narrative_events"].append(narrative)

        return results

    def _execute_decision(self, agent, decision: Decision) -> Dict[str, Any]:
        """Execute an agent's decision"""

        result = {"success": False, "effects": {}}

        try:
            if decision.action_type == "seek_safety":
                # Move to safer location or increase caution
                if hasattr(agent, "stress"):
                    agent.stress = max(0, agent.stress - 10)
                result = {"success": True, "effects": {"stress_reduction": 10}}

            elif decision.action_type == "build_relationship":
                # Attempt to improve a relationship
                if hasattr(self.game_state, "social_network"):
                    # Find a suitable target for relationship building
                    potential_targets = [
                        a.id
                        for a in self.game_state.agents.values()
                        if a.id != agent.id and a.faction_id == agent.faction_id
                    ]
                    if potential_targets:
                        target_id = random.choice(potential_targets)
                        self.game_state.update_relationship(
                            agent.id, target_id, delta_affinity=5, delta_trust=0.1
                        )
                        result = {
                            "success": True,
                            "effects": {"relationship_improved": target_id},
                        }

            elif decision.action_type == "skill_development":
                # Improve a skill
                if hasattr(agent, "skills") and decision.target:
                    skill_attr = decision.target
                    if hasattr(agent.skills, skill_attr):
                        current_value = getattr(agent.skills, skill_attr)
                        setattr(agent.skills, skill_attr, min(10, current_value + 1))
                        result = {
                            "success": True,
                            "effects": {"skill_improved": skill_attr},
                        }

            elif decision.action_type == "faction_mission":
                # Volunteer for faction activities
                if hasattr(agent, "loyalty"):
                    agent.loyalty = min(100, agent.loyalty + 5)
                result = {"success": True, "effects": {"loyalty_increased": 5}}

        except Exception as e:
            logger.error(f"Error executing decision for agent {agent.id}: {e}")
            result = {"success": False, "error": str(e)}

        return result

    def _generate_decision_narrative(
        self, agent, decision: Decision, result: Dict[str, Any]
    ) -> Optional[str]:
        """Generate narrative text for an agent's decision"""

        if not result.get("success"):
            return None

        narratives = {
            "seek_safety": f"{agent.name} takes measures to improve their security and reduce stress.",
            "build_relationship": f"{agent.name} reaches out to strengthen bonds with their allies.",
            "skill_development": f"{agent.name} dedicates time to improving their {decision.target} abilities.",
            "faction_mission": f"{agent.name} volunteers for additional faction duties, demonstrating loyalty.",
            "seek_comfort": f"{agent.name} seeks emotional support from trusted allies.",
            "avoid_threat": f"{agent.name} takes evasive action to avoid a perceived threat.",
        }

        return narratives.get(
            decision.action_type, f"{agent.name} takes autonomous action."
        )


# Integration function
def integrate_agent_ai_with_game_state(game_state):
    """Integrate the AI system with the main game state"""

    # Create AI director
    ai_director = AgentAIDirector(game_state)

    # Add AI processing to the game's advance_turn method
    original_advance_turn = game_state.advance_turn

    def enhanced_advance_turn():
        # Run original turn processing
        original_advance_turn()

        # Process AI decisions
        ai_results = ai_director.process_agent_ai_turn()

        # Add AI narratives to game narrative
        for narrative in ai_results["narrative_events"]:
            game_state.recent_narrative.append(narrative)

        return ai_results

    game_state.advance_turn = enhanced_advance_turn
    game_state.ai_director = ai_director

    return ai_director
