"""
Years of Lead - Enhanced Agent Autonomy System

Advanced autonomous decision-making for agents based on emotional state,
faction loyalty, trust, and mission priorities. Agents make independent
decisions that affect the game world dynamically.
"""

import random
import logging
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


logger = logging.getLogger(__name__)


class AutonousActionType(Enum):
    """Types of autonomous actions agents can take"""

    SEEK_SAFETY = "seek_safety"
    GATHER_INTELLIGENCE = "gather_intelligence"
    BUILD_RELATIONSHIP = "build_relationship"
    AVOID_THREAT = "avoid_threat"
    SEEK_MEDICAL_HELP = "seek_medical_help"
    RECRUIT_CONTACT = "recruit_contact"
    ABANDON_MISSION = "abandon_mission"
    REQUEST_BACKUP = "request_backup"
    CHANGE_LOCATION = "change_location"
    CONFIDE_SECRET = "confide_secret"
    BETRAY_TARGET = "betray_target"
    SELF_SACRIFICE = "self_sacrifice"
    EMOTIONAL_BREAKDOWN = "emotional_breakdown"
    SEEK_REVENGE = "seek_revenge"
    DESERT_FACTION = "desert_faction"


class RiskAssessment(Enum):
    """Risk levels for autonomous decisions"""

    MINIMAL = "minimal"  # 0.0-0.2
    LOW = "low"  # 0.2-0.4
    MODERATE = "moderate"  # 0.4-0.6
    HIGH = "high"  # 0.6-0.8
    EXTREME = "extreme"  # 0.8-1.0


@dataclass
class AutonomousDecision:
    """An autonomous decision made by an agent"""

    agent_id: str
    action_type: AutonousActionType
    target_agent_id: Optional[str] = None
    target_location_id: Optional[str] = None
    risk_level: float = 0.0
    emotional_driver: str = "none"
    confidence: float = 0.5
    expected_outcome: str = ""
    reasoning: str = ""
    prerequisites_met: bool = True
    execution_time: int = 1  # Turns to execute
    success_probability: float = 0.5

    # Emotional factors
    fear_factor: float = 0.0
    anger_factor: float = 0.0
    trust_factor: float = 0.0
    loyalty_factor: float = 0.0

    # Additional context
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentAutonomyProfile:
    """Profile defining an agent's autonomy characteristics"""

    agent_id: str
    autonomy_level: float = 0.7  # How likely to make autonomous decisions
    risk_tolerance: float = 0.5  # Willingness to take risks
    emotional_stability: float = 0.6  # Resistance to emotional decisions
    faction_loyalty: float = 0.8  # Loyalty to faction
    decision_frequency: int = 3  # Turns between autonomous decisions
    last_decision_turn: int = 0

    # Personality modifiers
    impulsiveness: float = 0.3
    cautious_nature: float = 0.5
    social_dependency: float = 0.4
    independence: float = 0.6

    # Learning from past decisions
    successful_decisions: int = 0
    failed_decisions: int = 0

    def get_decision_success_rate(self) -> float:
        """Calculate historical decision success rate"""
        total = self.successful_decisions + self.failed_decisions
        if total == 0:
            return 0.5
        return self.successful_decisions / total


class EnhancedAgentAutonomySystem:
    """Enhanced system for agent autonomous decision-making"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.agent_profiles: Dict[str, AgentAutonomyProfile] = {}
        self.pending_decisions: List[AutonomousDecision] = []
        self.decision_history: List[AutonomousDecision] = []
        self.decision_outcomes: Dict[str, Dict[str, Any]] = {}

        # System parameters
        self.max_decisions_per_turn = 5
        self.stress_decision_threshold = 0.7
        self.trauma_decision_threshold = 0.6
        self.loyalty_crisis_threshold = 0.3

    def initialize_agent_autonomy(self, agent_id: str, **kwargs):
        """Initialize autonomy profile for an agent"""
        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return

        # Create autonomy profile based on agent characteristics
        profile = AgentAutonomyProfile(
            agent_id=agent_id,
            autonomy_level=kwargs.get(
                "autonomy_level", self._calculate_base_autonomy(agent)
            ),
            risk_tolerance=kwargs.get(
                "risk_tolerance", self._calculate_risk_tolerance(agent)
            ),
            emotional_stability=kwargs.get(
                "emotional_stability", self._calculate_emotional_stability(agent)
            ),
            faction_loyalty=kwargs.get("faction_loyalty", agent.loyalty / 100.0),
        )

        # Adjust based on personality traits if available
        self._adjust_profile_for_traits(profile, agent)

        self.agent_profiles[agent_id] = profile
        logger.info(f"Initialized autonomy for agent {agent.name}")

    def process_autonomous_decisions(self) -> Dict[str, Any]:
        """Process autonomous decisions for all agents"""
        results = {
            "decisions_made": [],
            "actions_taken": [],
            "narrative_events": [],
            "faction_impacts": {},
            "relationship_changes": [],
        }

        decisions_this_turn = 0

        for agent_id, agent in self.game_state.agents.items():
            if agent.status != "active":
                continue

            if agent_id not in self.agent_profiles:
                self.initialize_agent_autonomy(agent_id)

            profile = self.agent_profiles[agent_id]

            # Check if agent should make an autonomous decision
            if self._should_make_decision(agent, profile):
                decision = self._generate_autonomous_decision(agent, profile)
                if decision and decisions_this_turn < self.max_decisions_per_turn:
                    outcome = self._execute_autonomous_decision(decision)
                    results["decisions_made"].append(decision)
                    results["actions_taken"].append(outcome)

                    # Generate narrative
                    narrative = self._generate_decision_narrative(decision, outcome)
                    if narrative:
                        results["narrative_events"].append(narrative)

                    # Update profile based on outcome
                    self._update_profile_from_outcome(profile, decision, outcome)

                    decisions_this_turn += 1
                    profile.last_decision_turn = self.game_state.turn_number

        # Process pending decisions from previous turns
        self._process_pending_decisions(results)

        return results

    def _should_make_decision(self, agent, profile: AgentAutonomyProfile) -> bool:
        """Determine if agent should make an autonomous decision"""

        # Check decision frequency
        turns_since_last = self.game_state.turn_number - profile.last_decision_turn
        if turns_since_last < profile.decision_frequency:
            return False

        # Base probability from autonomy level
        base_prob = profile.autonomy_level

        # Emotional state modifiers
        emotional_state = getattr(agent, "emotional_state", None)
        if emotional_state:
            # High stress/trauma increases likelihood of autonomous action
            stress_modifier = emotional_state.trauma_level * 0.3
            if emotional_state.trauma_level > self.trauma_decision_threshold:
                stress_modifier += 0.4

            # Extreme emotions trigger autonomous decisions
            dominant_emotion, intensity = emotional_state.get_dominant_emotion()
            if intensity > 0.8:
                stress_modifier += 0.3

            base_prob = min(1.0, base_prob + stress_modifier)

        # Loyalty crisis modifier
        if agent.loyalty < (self.loyalty_crisis_threshold * 100):
            base_prob += 0.4

        # Physical stress modifier
        if agent.stress > (self.stress_decision_threshold * 100):
            base_prob += 0.3

        return random.random() < base_prob

    def _generate_autonomous_decision(
        self, agent, profile: AgentAutonomyProfile
    ) -> Optional[AutonomousDecision]:
        """Generate an autonomous decision for an agent"""

        # Analyze agent's current state
        state_analysis = self._analyze_agent_state(agent)

        # Generate possible decisions based on state
        possible_decisions = self._generate_decision_options(agent, state_analysis)

        if not possible_decisions:
            return None

        # Evaluate and rank decisions
        best_decision = self._evaluate_decisions(agent, possible_decisions, profile)

        if best_decision:
            # Perform risk assessment
            risk_assessment = self._assess_decision_risk(
                best_decision, agent, state_analysis
            )
            best_decision.risk_level = risk_assessment["risk_level"]
            best_decision.success_probability = risk_assessment["success_probability"]

            # Check if agent will proceed with risky decision
            if not self._will_proceed_with_risk(profile, best_decision):
                logger.info(
                    f"Agent {agent.name} decided against risky action: {best_decision.action_type}"
                )
                return None

        return best_decision

    def _analyze_agent_state(self, agent) -> Dict[str, Any]:
        """Analyze agent's current state comprehensively"""

        emotional_state = getattr(agent, "emotional_state", None)
        analysis = {
            "stress_level": agent.stress / 100.0,
            "loyalty_level": agent.loyalty / 100.0,
            "is_traumatized": False,
            "dominant_emotion": "neutral",
            "emotion_intensity": 0.0,
            "psychological_stability": True,
            "social_isolation": False,
            "threat_level": 0.0,
            "needs_help": False,
            "faction_crisis": False,
        }

        if emotional_state:
            analysis["is_traumatized"] = (
                emotional_state.trauma_level > self.trauma_decision_threshold
            )
            (
                analysis["dominant_emotion"],
                analysis["emotion_intensity"],
            ) = emotional_state.get_dominant_emotion()
            analysis[
                "psychological_stability"
            ] = emotional_state.is_psychologically_stable()

            # Determine if agent needs help
            if (
                emotional_state.trauma_level > 0.7
                or not analysis["psychological_stability"]
                or agent.stress > 80
            ):
                analysis["needs_help"] = True

        # Analyze social connections
        if hasattr(agent, "relationships"):
            positive_relationships = sum(
                1 for rel in agent.relationships.values() if rel.affinity > 10
            )
            analysis["social_isolation"] = positive_relationships < 2

        # Faction analysis
        analysis["faction_crisis"] = agent.loyalty < 30

        return analysis

    def _generate_decision_options(
        self, agent, state_analysis: Dict[str, Any]
    ) -> List[AutonomousDecision]:
        """Generate possible autonomous decisions based on agent state"""

        decisions = []

        # Emotional state-driven decisions
        if state_analysis["is_traumatized"]:
            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.SEEK_MEDICAL_HELP,
                    emotional_driver="trauma",
                    reasoning="High trauma level requires medical attention",
                    expected_outcome="Reduced trauma and stress",
                )
            )

            if state_analysis["emotion_intensity"] > 0.8:
                decisions.append(
                    AutonomousDecision(
                        agent_id=agent.id,
                        action_type=AutonousActionType.EMOTIONAL_BREAKDOWN,
                        emotional_driver=state_analysis["dominant_emotion"],
                        reasoning="Overwhelming emotional state",
                        expected_outcome="Emotional release but potential exposure",
                    )
                )

        # Fear-driven decisions
        if (
            state_analysis["dominant_emotion"] == "fear"
            and state_analysis["emotion_intensity"] > 0.6
        ):
            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.SEEK_SAFETY,
                    emotional_driver="fear",
                    reasoning="Fear overwhelming, seeking safety",
                    expected_outcome="Reduced fear, potential mission abandonment",
                )
            )

            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.CHANGE_LOCATION,
                    emotional_driver="fear",
                    reasoning="Current location feels unsafe",
                    expected_outcome="Temporary safety, disrupted operations",
                )
            )

        # Anger-driven decisions
        if (
            state_analysis["dominant_emotion"] == "anger"
            and state_analysis["emotion_intensity"] > 0.7
        ):
            # Look for revenge targets
            if hasattr(agent, "relationships"):
                enemies = [
                    aid
                    for aid, rel in agent.relationships.items()
                    if rel.affinity < -20
                ]
                if enemies:
                    target = random.choice(enemies)
                    decisions.append(
                        AutonomousDecision(
                            agent_id=agent.id,
                            action_type=AutonousActionType.SEEK_REVENGE,
                            target_agent_id=target,
                            emotional_driver="anger",
                            reasoning="Anger demands retribution",
                            expected_outcome="Emotional satisfaction, potential escalation",
                        )
                    )

        # Loyalty crisis decisions
        if state_analysis["faction_crisis"]:
            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.DESERT_FACTION,
                    emotional_driver="disillusionment",
                    reasoning="Lost faith in faction cause",
                    expected_outcome="Freedom from faction, loss of support network",
                )
            )

        # Social isolation decisions
        if state_analysis["social_isolation"]:
            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.BUILD_RELATIONSHIP,
                    emotional_driver="loneliness",
                    reasoning="Need for social connection",
                    expected_outcome="New relationship, reduced isolation",
                )
            )

        # Stress-driven decisions
        if state_analysis["stress_level"] > self.stress_decision_threshold:
            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.ABANDON_MISSION,
                    emotional_driver="stress",
                    reasoning="Stress level too high to continue",
                    expected_outcome="Stress reduction, mission failure",
                )
            )

            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.REQUEST_BACKUP,
                    emotional_driver="stress",
                    reasoning="Need support to handle pressure",
                    expected_outcome="Shared burden, potential security risk",
                )
            )

        # Proactive decisions for stable agents
        if (
            state_analysis["psychological_stability"]
            and state_analysis["stress_level"] < 0.5
            and not state_analysis["is_traumatized"]
        ):
            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.GATHER_INTELLIGENCE,
                    emotional_driver="initiative",
                    reasoning="Stable state allows proactive intelligence gathering",
                    expected_outcome="Valuable intelligence, slight exposure risk",
                )
            )

            decisions.append(
                AutonomousDecision(
                    agent_id=agent.id,
                    action_type=AutonousActionType.RECRUIT_CONTACT,
                    emotional_driver="initiative",
                    reasoning="Expand network while stable",
                    expected_outcome="New contact, increased network size",
                )
            )

        return decisions

    def _evaluate_decisions(
        self, agent, decisions: List[AutonomousDecision], profile: AgentAutonomyProfile
    ) -> Optional[AutonomousDecision]:
        """Evaluate and select the best decision"""

        if not decisions:
            return None

        scored_decisions = []

        for decision in decisions:
            score = self._score_decision(decision, agent, profile)
            scored_decisions.append((score, decision))

        # Sort by score (highest first)
        scored_decisions.sort(key=lambda x: x[0], reverse=True)

        # Add some randomness but prefer higher-scored decisions
        if len(scored_decisions) > 1:
            # 70% chance to pick best, 20% second best, 10% others
            rand = random.random()
            if rand < 0.7:
                return scored_decisions[0][1]
            elif rand < 0.9 and len(scored_decisions) > 1:
                return scored_decisions[1][1]
            else:
                return random.choice(scored_decisions)[1]

        return scored_decisions[0][1] if scored_decisions else None

    def _score_decision(
        self, decision: AutonomousDecision, agent, profile: AgentAutonomyProfile
    ) -> float:
        """Score a decision based on multiple factors"""

        base_score = 50.0

        # Emotional alignment bonus
        emotional_state = getattr(agent, "emotional_state", None)
        if emotional_state:
            dominant_emotion, intensity = emotional_state.get_dominant_emotion()
            if decision.emotional_driver == dominant_emotion:
                base_score += intensity * 30.0

        # Personality alignment
        if decision.action_type in [
            AutonousActionType.SEEK_SAFETY,
            AutonousActionType.AVOID_THREAT,
        ]:
            base_score += profile.cautious_nature * 20.0
        elif decision.action_type in [
            AutonousActionType.SEEK_REVENGE,
            AutonousActionType.BETRAY_TARGET,
        ]:
            base_score += profile.impulsiveness * 25.0
        elif decision.action_type in [
            AutonousActionType.BUILD_RELATIONSHIP,
            AutonousActionType.CONFIDE_SECRET,
        ]:
            base_score += profile.social_dependency * 15.0
        elif decision.action_type in [
            AutonousActionType.DESERT_FACTION,
            AutonousActionType.CHANGE_LOCATION,
        ]:
            base_score += profile.independence * 20.0

        # Risk tolerance adjustment
        estimated_risk = self._estimate_decision_risk(decision, agent)
        if estimated_risk > profile.risk_tolerance:
            base_score -= (estimated_risk - profile.risk_tolerance) * 40.0

        # Success rate consideration
        historical_success = profile.get_decision_success_rate()
        if decision.action_type == AutonousActionType.GATHER_INTELLIGENCE:
            base_score += historical_success * 15.0

        # Loyalty factor
        if decision.action_type == AutonousActionType.DESERT_FACTION:
            base_score -= profile.faction_loyalty * 50.0

        return max(0.0, base_score)

    def _estimate_decision_risk(self, decision: AutonomousDecision, agent) -> float:
        """Estimate the risk level of a decision"""

        base_risk = {
            AutonousActionType.SEEK_SAFETY: 0.1,
            AutonousActionType.GATHER_INTELLIGENCE: 0.4,
            AutonousActionType.BUILD_RELATIONSHIP: 0.2,
            AutonousActionType.AVOID_THREAT: 0.2,
            AutonousActionType.SEEK_MEDICAL_HELP: 0.3,
            AutonousActionType.RECRUIT_CONTACT: 0.5,
            AutonousActionType.ABANDON_MISSION: 0.6,
            AutonousActionType.REQUEST_BACKUP: 0.3,
            AutonousActionType.CHANGE_LOCATION: 0.4,
            AutonousActionType.CONFIDE_SECRET: 0.7,
            AutonousActionType.BETRAY_TARGET: 0.9,
            AutonousActionType.SELF_SACRIFICE: 1.0,
            AutonousActionType.EMOTIONAL_BREAKDOWN: 0.8,
            AutonousActionType.SEEK_REVENGE: 0.8,
            AutonousActionType.DESERT_FACTION: 0.7,
        }.get(decision.action_type, 0.5)

        # Adjust based on agent state
        if agent.stress > 70:
            base_risk += 0.2

        if (
            hasattr(agent, "emotional_state")
            and agent.emotional_state.trauma_level > 0.6
        ):
            base_risk += 0.1

        return min(1.0, base_risk)

    def _assess_decision_risk(
        self, decision: AutonomousDecision, agent, state_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Comprehensive risk assessment for a decision"""

        base_risk = self._estimate_decision_risk(decision, agent)

        # Emotional state risk modifiers
        if state_analysis["is_traumatized"]:
            base_risk += 0.2

        if not state_analysis["psychological_stability"]:
            base_risk += 0.3

        # Success probability calculation
        success_prob = 1.0 - base_risk

        # Agent skill modifiers (if available)
        if hasattr(agent, "skills"):
            relevant_skill_level = 1.0  # Default
            if decision.action_type in [AutonousActionType.GATHER_INTELLIGENCE]:
                intel_skill = agent.skills.get(
                    "intelligence", type("obj", (), {"level": 1})
                )
                relevant_skill_level = intel_skill.level / 5.0
            elif decision.action_type in [AutonousActionType.BUILD_RELATIONSHIP]:
                social_skill = agent.skills.get("social", type("obj", (), {"level": 1}))
                relevant_skill_level = social_skill.level / 5.0

            success_prob = min(0.95, success_prob + (relevant_skill_level - 0.5) * 0.3)

        return {
            "risk_level": base_risk,
            "success_probability": max(0.05, success_prob),
            "risk_category": self._categorize_risk(base_risk),
        }

    def _categorize_risk(self, risk_level: float) -> RiskAssessment:
        """Categorize risk level"""
        if risk_level <= 0.2:
            return RiskAssessment.MINIMAL
        elif risk_level <= 0.4:
            return RiskAssessment.LOW
        elif risk_level <= 0.6:
            return RiskAssessment.MODERATE
        elif risk_level <= 0.8:
            return RiskAssessment.HIGH
        else:
            return RiskAssessment.EXTREME

    def _will_proceed_with_risk(
        self, profile: AgentAutonomyProfile, decision: AutonomousDecision
    ) -> bool:
        """Determine if agent will proceed with a risky decision"""

        # Compare decision risk with agent's risk tolerance
        risk_differential = decision.risk_level - profile.risk_tolerance

        if risk_differential <= 0:
            return True  # Within risk tolerance

        # Emotional decisions may override risk assessment
        if decision.emotional_driver in ["fear", "anger", "trauma"]:
            # High emotional intensity can override caution
            proceed_chance = 0.7 - (risk_differential * 0.5)
        else:
            # Rational decisions respect risk tolerance more
            proceed_chance = 0.3 - (risk_differential * 0.8)

        # Impulsive agents are more likely to proceed despite risk
        proceed_chance += profile.impulsiveness * 0.3

        return random.random() < max(0.0, proceed_chance)

    def _execute_autonomous_decision(
        self, decision: AutonomousDecision
    ) -> Dict[str, Any]:
        """Execute an autonomous decision and return results"""

        outcome = {
            "decision_id": f"auto_{decision.agent_id}_{self.game_state.turn_number}",
            "success": False,
            "effects": {},
            "narrative": "",
            "consequences": [],
            "emotional_impact": {},
            "relationship_changes": {},
        }

        agent = self.game_state.agents.get(decision.agent_id)
        if not agent:
            outcome["effects"]["error"] = "Agent not found"
            return outcome

        # Roll for success
        success_roll = random.random()
        outcome["success"] = success_roll <= decision.success_probability

        # Execute specific action
        if decision.action_type == AutonousActionType.SEEK_SAFETY:
            outcome = self._execute_seek_safety(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.GATHER_INTELLIGENCE:
            outcome = self._execute_gather_intelligence(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.BUILD_RELATIONSHIP:
            outcome = self._execute_build_relationship(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.SEEK_MEDICAL_HELP:
            outcome = self._execute_seek_medical_help(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.EMOTIONAL_BREAKDOWN:
            outcome = self._execute_emotional_breakdown(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.DESERT_FACTION:
            outcome = self._execute_desert_faction(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.ABANDON_MISSION:
            outcome = self._execute_abandon_mission(decision, agent, outcome)
        elif decision.action_type == AutonousActionType.SEEK_REVENGE:
            outcome = self._execute_seek_revenge(decision, agent, outcome)
        else:
            # Generic execution
            outcome = self._execute_generic_action(decision, agent, outcome)

        # Store decision outcome
        self.decision_outcomes[outcome["decision_id"]] = outcome
        self.decision_history.append(decision)

        return outcome

    def _execute_seek_safety(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute seek safety action"""
        if outcome["success"]:
            # Reduce stress and fear
            agent.stress = max(0, agent.stress - 20)
            if hasattr(agent, "emotional_state"):
                agent.emotional_state.fear = max(-1.0, agent.emotional_state.fear - 0.3)

            outcome["effects"]["stress_reduction"] = 20
            outcome["emotional_impact"]["fear"] = -0.3
            outcome[
                "narrative"
            ] = f"{agent.name} finds a safe place to recover and calm down"
        else:
            # Failed to find safety, increased stress
            agent.stress = min(100, agent.stress + 10)
            outcome["effects"]["stress_increase"] = 10
            outcome[
                "narrative"
            ] = f"{agent.name} attempts to find safety but fails, feeling more anxious"

        return outcome

    def _execute_gather_intelligence(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute intelligence gathering action"""
        if outcome["success"]:
            # Generate intelligence value
            intel_value = random.randint(5, 15)
            outcome["effects"]["intelligence_gathered"] = intel_value
            outcome[
                "narrative"
            ] = f"{agent.name} autonomously gathers valuable intelligence"

            # Small stress increase from operation
            agent.stress = min(100, agent.stress + 5)
        else:
            # Failed operation, potential exposure
            agent.stress = min(100, agent.stress + 15)
            outcome["effects"]["stress_increase"] = 15
            outcome["effects"]["exposure_risk"] = 0.2
            outcome[
                "narrative"
            ] = f"{agent.name}'s intelligence gathering attempt fails and raises suspicion"

        return outcome

    def _execute_build_relationship(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute relationship building action"""
        # Find a suitable target for relationship building
        other_agents = [
            a
            for a_id, a in self.game_state.agents.items()
            if a_id != agent.id and a.status == "active"
        ]

        if not other_agents:
            outcome["effects"]["no_targets"] = True
            outcome[
                "narrative"
            ] = f"{agent.name} wants to build relationships but finds no one available"
            return outcome

        target_agent = random.choice(other_agents)

        if outcome["success"]:
            # Improve relationship
            if hasattr(agent, "relationships"):
                if target_agent.id not in agent.relationships:
                    # Create new relationship
                    from .relationships import Relationship, BondType

                    new_rel = Relationship(
                        agent_a_id=agent.id,
                        agent_b_id=target_agent.id,
                        bond_type=BondType.ACQUAINTANCE,
                        affinity=random.randint(5, 15),
                        trust=0.1,
                        loyalty=0.0,
                    )
                    agent.relationships[target_agent.id] = new_rel
                else:
                    # Improve existing relationship
                    rel = agent.relationships[target_agent.id]
                    rel.affinity = min(100, rel.affinity + random.randint(5, 10))
                    rel.trust = min(1.0, rel.trust + 0.1)

            outcome["effects"]["relationship_improved"] = target_agent.id
            outcome[
                "narrative"
            ] = f"{agent.name} successfully builds rapport with {target_agent.name}"

            # Reduce stress from social connection
            agent.stress = max(0, agent.stress - 10)
        else:
            # Relationship attempt failed, potential awkwardness
            outcome["effects"]["relationship_strain"] = target_agent.id
            outcome[
                "narrative"
            ] = f"{agent.name}'s attempt to connect with {target_agent.name} creates awkwardness"

        return outcome

    def _execute_seek_medical_help(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute seeking medical help action"""
        if outcome["success"]:
            # Reduce trauma and stress
            if hasattr(agent, "emotional_state"):
                agent.emotional_state.trauma_level = max(
                    0.0, agent.emotional_state.trauma_level - 0.2
                )
            agent.stress = max(0, agent.stress - 25)

            outcome["effects"]["trauma_reduction"] = 0.2
            outcome["effects"]["stress_reduction"] = 25
            outcome[
                "narrative"
            ] = f"{agent.name} successfully receives medical and psychological help"
        else:
            # Help not available or ineffective
            outcome["effects"]["help_unavailable"] = True
            outcome[
                "narrative"
            ] = f"{agent.name} seeks help but cannot find adequate medical support"

        return outcome

    def _execute_emotional_breakdown(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute emotional breakdown action"""
        # Emotional breakdown always "succeeds" but has consequences
        outcome["success"] = True

        # Temporary stress relief but increased vulnerability
        agent.stress = max(0, agent.stress - 30)

        if hasattr(agent, "emotional_state"):
            # Reduce dominant emotion intensity
            dominant_emotion, intensity = agent.emotional_state.get_dominant_emotion()
            setattr(
                agent.emotional_state,
                dominant_emotion,
                max(-1.0, getattr(agent.emotional_state, dominant_emotion) - 0.4),
            )

        outcome["effects"]["stress_reduction"] = 30
        outcome["effects"]["exposure_risk"] = 0.4  # High exposure risk from breakdown
        outcome["effects"]["reputation_damage"] = 10
        outcome[
            "narrative"
        ] = f"{agent.name} has an emotional breakdown, releasing pent-up stress but attracting attention"

        return outcome

    def _execute_desert_faction(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute faction desertion action"""
        if outcome["success"]:
            # Remove from faction
            agent.loyalty = 0
            agent.status = "deserter"

            # Stress relief from freedom
            agent.stress = max(0, agent.stress - 40)

            outcome["effects"]["faction_left"] = agent.faction_id
            outcome["effects"]["stress_reduction"] = 40
            outcome["effects"]["support_network_lost"] = True
            outcome[
                "narrative"
            ] = f"{agent.name} deserts the faction, seeking freedom from the cause"
        else:
            # Failed desertion attempt, potential consequences
            agent.loyalty = max(0, agent.loyalty - 20)
            outcome["effects"]["loyalty_damage"] = 20
            outcome["effects"]["suspicion_raised"] = True
            outcome[
                "narrative"
            ] = f"{agent.name} considers desertion but cannot go through with it"

        return outcome

    def _execute_abandon_mission(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute mission abandonment action"""
        # This always "succeeds" as it's an internal decision
        outcome["success"] = True

        # Immediate stress relief
        agent.stress = max(0, agent.stress - 20)

        # But loyalty and reputation consequences
        agent.loyalty = max(0, agent.loyalty - 15)

        outcome["effects"]["stress_reduction"] = 20
        outcome["effects"]["loyalty_damage"] = 15
        outcome["effects"]["mission_abandoned"] = True
        outcome[
            "narrative"
        ] = f"{agent.name} abandons their current mission due to overwhelming stress"

        return outcome

    def _execute_seek_revenge(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute revenge-seeking action"""
        target_id = decision.target_agent_id
        if not target_id:
            outcome["effects"]["no_target"] = True
            return outcome

        target_agent = self.game_state.agents.get(target_id)
        if not target_agent:
            outcome["effects"]["target_not_found"] = True
            return outcome

        if outcome["success"]:
            # Successful revenge action
            if hasattr(agent, "emotional_state"):
                agent.emotional_state.anger = max(
                    -1.0, agent.emotional_state.anger - 0.5
                )

            # Damage relationship
            if hasattr(agent, "relationships") and target_id in agent.relationships:
                rel = agent.relationships[target_id]
                rel.affinity = max(-100, rel.affinity - 30)
                rel.trust = max(0.0, rel.trust - 0.5)

            outcome["effects"]["revenge_taken"] = target_id
            outcome["effects"]["relationship_damaged"] = target_id
            outcome[
                "narrative"
            ] = f"{agent.name} takes revenge against {target_agent.name}"
        else:
            # Failed revenge attempt
            outcome["effects"]["revenge_failed"] = target_id
            outcome["effects"]["escalation_risk"] = 0.6
            outcome[
                "narrative"
            ] = f"{agent.name}'s revenge attempt against {target_agent.name} fails and escalates tensions"

        return outcome

    def _execute_generic_action(
        self, decision: AutonomousDecision, agent, outcome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a generic autonomous action"""
        if outcome["success"]:
            outcome[
                "narrative"
            ] = f"{agent.name} successfully executes autonomous action: {decision.action_type.value}"
        else:
            outcome[
                "narrative"
            ] = f"{agent.name} fails in autonomous action: {decision.action_type.value}"

        return outcome

    def _process_pending_decisions(self, results: Dict[str, Any]):
        """Process decisions that take multiple turns to execute"""
        completed = []

        for decision in self.pending_decisions:
            decision.execution_time -= 1
            if decision.execution_time <= 0:
                # Execute the decision
                outcome = self._execute_autonomous_decision(decision)
                results["actions_taken"].append(outcome)
                completed.append(decision)

        # Remove completed decisions
        for decision in completed:
            self.pending_decisions.remove(decision)

    def _generate_decision_narrative(
        self, decision: AutonomousDecision, outcome: Dict[str, Any]
    ) -> str:
        """Generate narrative text for an autonomous decision"""
        return outcome.get(
            "narrative", f"Agent {decision.agent_id} made an autonomous decision"
        )

    def _update_profile_from_outcome(
        self,
        profile: AgentAutonomyProfile,
        decision: AutonomousDecision,
        outcome: Dict[str, Any],
    ):
        """Update agent profile based on decision outcome"""
        if outcome["success"]:
            profile.successful_decisions += 1
        else:
            profile.failed_decisions += 1

        # Adjust autonomy based on success rate
        success_rate = profile.get_decision_success_rate()
        if success_rate > 0.7:
            profile.autonomy_level = min(1.0, profile.autonomy_level + 0.05)
        elif success_rate < 0.3:
            profile.autonomy_level = max(0.2, profile.autonomy_level - 0.05)

    def _calculate_base_autonomy(self, agent) -> float:
        """Calculate base autonomy level for an agent"""
        base = 0.5

        # Adjust based on background
        background_modifiers = {
            "veteran": 0.2,
            "organizer": 0.15,
            "student": -0.1,
            "insider": -0.15,
        }
        base += background_modifiers.get(agent.background, 0.0)

        # Adjust based on stress and loyalty
        stress_modifier = (100 - agent.stress) / 200.0  # Higher stress = less autonomy
        loyalty_modifier = agent.loyalty / 200.0  # Higher loyalty = less autonomy

        return max(0.1, min(1.0, base + stress_modifier - loyalty_modifier))

    def _calculate_risk_tolerance(self, agent) -> float:
        """Calculate risk tolerance for an agent"""
        base = 0.5

        # Adjust based on emotional state
        if hasattr(agent, "emotional_state"):
            # Fear reduces risk tolerance, anger increases it
            fear_penalty = getattr(agent.emotional_state, "fear", 0) * 0.3
            anger_bonus = getattr(agent.emotional_state, "anger", 0) * 0.2
            base = base - fear_penalty + anger_bonus

        return max(0.0, min(1.0, base))

    def _calculate_emotional_stability(self, agent) -> float:
        """Calculate emotional stability for an agent"""
        if hasattr(agent, "emotional_state"):
            return agent.emotional_state.get_emotional_stability()
        return 0.6

    def _adjust_profile_for_traits(self, profile: AgentAutonomyProfile, agent):
        """Adjust profile based on agent personality traits"""
        # This would integrate with a trait system if available
        # For now, make random adjustments based on background
        background_traits = {
            "veteran": {"cautious_nature": 0.2, "independence": 0.15},
            "student": {"impulsiveness": 0.15, "social_dependency": 0.1},
            "organizer": {"social_dependency": -0.1, "independence": -0.1},
            "journalist": {"independence": 0.1, "cautious_nature": -0.1},
        }

        traits = background_traits.get(agent.background, {})
        for trait, modifier in traits.items():
            current_value = getattr(profile, trait, 0.5)
            setattr(profile, trait, max(0.0, min(1.0, current_value + modifier)))

    def get_autonomy_summary(self) -> Dict[str, Any]:
        """Get summary of autonomous decision-making activity"""
        return {
            "total_profiles": len(self.agent_profiles),
            "total_decisions": len(self.decision_history),
            "pending_decisions": len(self.pending_decisions),
            "success_rate": self._calculate_overall_success_rate(),
            "decision_types": self._get_decision_type_breakdown(),
            "most_autonomous_agents": self._get_most_autonomous_agents(),
        }

    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall success rate of autonomous decisions"""
        if not self.decision_outcomes:
            return 0.0

        successes = sum(
            1
            for outcome in self.decision_outcomes.values()
            if outcome.get("success", False)
        )
        return successes / len(self.decision_outcomes)

    def _get_decision_type_breakdown(self) -> Dict[str, int]:
        """Get breakdown of decision types"""
        breakdown = defaultdict(int)
        for decision in self.decision_history:
            breakdown[decision.action_type.value] += 1
        return dict(breakdown)

    def _get_most_autonomous_agents(self) -> List[Tuple[str, float]]:
        """Get agents with highest autonomy levels"""
        autonomous_agents = [
            (agent_id, profile.autonomy_level)
            for agent_id, profile in self.agent_profiles.items()
        ]
        autonomous_agents.sort(key=lambda x: x[1], reverse=True)
        return autonomous_agents[:5]
