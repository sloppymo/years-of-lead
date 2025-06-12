"""
Years of Lead - Enhanced Mission Execution System

Phase 2: Mission Outcome Enhancement
Adds multi-step consequences, agent emotional states affecting outcomes,
and multi-agent mission collaboration mechanics.
"""

import random
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class EnhancedExecutionOutcome(Enum):
    """Expanded mission execution outcomes"""

    PERFECT_SUCCESS = "perfect_success"
    SUCCESS_WITH_COMPLICATIONS = "success_with_complications"
    PARTIAL_SUCCESS = "partial_success"
    PARTIAL_SUCCESS_WITH_CONSEQUENCES = "partial_success_with_consequences"
    FAILURE_WITH_INTEL = "failure_with_intel"
    FAILURE_WITH_EXPOSURE = "failure_with_exposure"
    COMPLETE_FAILURE = "complete_failure"
    CATASTROPHIC_FAILURE = "catastrophic_failure"
    TRAGIC_SUCCESS = "tragic_success"  # Success but at great cost
    PYRRHIC_VICTORY = "pyrrhic_victory"  # Success undermines future operations
    BENEFICIAL_FAILURE = (
        "beneficial_failure"  # Failure that provides unexpected benefits
    )
    SABOTAGED_MISSION = "sabotaged_mission"  # Internal sabotage caused failure
    BETRAYAL_REVEALED = "betrayal_revealed"  # Mission reveals agent betrayal
    UNINTENDED_CONSEQUENCES = (
        "unintended_consequences"  # Success causes unexpected problems
    )


@dataclass
class MissionCollaboration:
    """Multi-agent collaboration effects"""

    agents: List[str]
    trust_synergy: float = 0.0  # Bonus from trusted agents
    skill_complementarity: float = 0.0  # Bonus from complementary skills
    communication_efficiency: float = 0.0  # How well agents coordinate
    leadership_effectiveness: float = 0.0  # Quality of mission leadership
    emotional_contagion: Dict[str, float] = field(default_factory=dict)
    relationship_strain: float = 0.0  # Stress on relationships
    group_cohesion: float = 0.0  # Overall team unity


@dataclass
class EnhancedConsequence:
    """Enhanced consequence with emotional and relationship impacts"""

    type: str
    description: str
    immediate_effects: Dict[str, Any] = field(default_factory=dict)
    delayed_effects: Dict[str, Any] = field(default_factory=dict)
    emotional_impact: Dict[str, Dict[str, float]] = field(
        default_factory=dict
    )  # Per agent
    relationship_changes: Dict[Tuple[str, str], Dict[str, float]] = field(
        default_factory=dict
    )
    narrative_hooks: List[str] = field(default_factory=list)
    escalation_potential: float = 0.0
    recovery_time: int = 0  # Turns for effects to fade


class EnhancedMissionExecutor:
    """Enhanced mission execution with emotional and collaboration mechanics"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.mission_history: List[Dict[str, Any]] = []
        self.consequence_tracker: Dict[str, List[EnhancedConsequence]] = {}

    def execute_enhanced_mission(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        location: Dict[str, Any],
        resources: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute mission with enhanced outcome and collaboration mechanics"""

        # Analyze agent collaboration
        collaboration = self._analyze_agent_collaboration(agents)

        # Calculate base success with emotional modifiers
        base_success = self._calculate_emotional_success_probability(
            mission, agents, collaboration
        )

        # Apply collaboration bonuses/penalties
        modified_success = self._apply_collaboration_effects(
            base_success, collaboration
        )

        # Determine enhanced outcome
        outcome = self._determine_enhanced_outcome(
            modified_success, agents, collaboration
        )

        # Generate multi-layered consequences
        consequences = self._generate_enhanced_consequences(
            mission, agents, outcome, collaboration
        )

        # Apply emotional impacts to all agents
        emotional_impacts = self._calculate_mission_emotional_impacts(
            outcome, agents, consequences
        )

        # Update relationships based on mission experience
        relationship_changes = self._update_mission_relationships(
            agents, outcome, collaboration
        )

        # Generate enhanced narrative
        narrative = self._generate_enhanced_narrative(
            mission, agents, outcome, consequences
        )

        result = {
            "outcome": outcome,
            "original_success_probability": base_success,
            "collaboration_modified_success": modified_success,
            "collaboration_analysis": collaboration,
            "consequences": consequences,
            "emotional_impacts": emotional_impacts,
            "relationship_changes": relationship_changes,
            "narrative": narrative,
            "mission_id": mission.get("id", "unknown"),
            "agents_involved": [a["id"] for a in agents],
        }

        self.mission_history.append(result)
        return result

    def _analyze_agent_collaboration(
        self, agents: List[Dict[str, Any]]
    ) -> MissionCollaboration:
        """Analyze how well agents collaborate on the mission"""

        if len(agents) <= 1:
            return MissionCollaboration(agents=[a["id"] for a in agents])

        agent_ids = [a["id"] for a in agents]
        collaboration = MissionCollaboration(agents=agent_ids)

        # Calculate trust synergy
        total_trust = 0.0
        trust_pairs = 0

        for i, agent_a in enumerate(agents):
            for j, agent_b in enumerate(agents[i + 1 :], i + 1):
                # Get relationship if exists
                agent_a_obj = self.game_state.agents.get(agent_a["id"])
                if agent_a_obj and hasattr(agent_a_obj, "relationships"):
                    rel = agent_a_obj.relationships.get(agent_b["id"])
                    if rel:
                        total_trust += rel.trust
                        trust_pairs += 1

        if trust_pairs > 0:
            collaboration.trust_synergy = total_trust / trust_pairs

        # Calculate skill complementarity
        skill_coverage = set()
        for agent in agents:
            if "skills" in agent:
                skill_coverage.update(agent["skills"].keys())

        max_possible_skills = 6  # Assuming 6 skill types
        collaboration.skill_complementarity = len(skill_coverage) / max_possible_skills

        # Communication efficiency based on group size and relationships
        group_size_penalty = max(
            0.0, (len(agents) - 3) * 0.1
        )  # Penalty for large groups
        collaboration.communication_efficiency = max(
            0.0, 0.8 + collaboration.trust_synergy * 0.2 - group_size_penalty
        )

        # Leadership effectiveness (highest leadership skill in group)
        max_leadership = 0.0
        for agent in agents:
            leadership_skill = agent.get("skills", {}).get("leadership", {"level": 1})
            leadership_level = (
                leadership_skill.get("level", 1)
                if isinstance(leadership_skill, dict)
                else 1
            )
            max_leadership = max(max_leadership, leadership_level / 5.0)

        collaboration.leadership_effectiveness = max_leadership

        # Emotional contagion analysis
        collaboration.emotional_contagion = self._analyze_emotional_contagion(agents)

        # Group cohesion
        collaboration.group_cohesion = (
            collaboration.trust_synergy * 0.4
            + collaboration.communication_efficiency * 0.3
            + collaboration.leadership_effectiveness * 0.3
        )

        return collaboration

    def _analyze_emotional_contagion(
        self, agents: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Analyze how emotions spread through the agent group"""

        emotional_summary = {
            "fear": 0.0,
            "anger": 0.0,
            "sadness": 0.0,
            "joy": 0.0,
            "trust": 0.0,
            "anticipation": 0.0,
            "dominant_emotion": "neutral",
        }

        if not agents:
            return emotional_summary

        # Collect emotional states
        emotions_count = {
            "fear": 0,
            "anger": 0,
            "sadness": 0,
            "joy": 0,
            "trust": 0,
            "anticipation": 0,
        }
        total_agents = 0

        for agent in agents:
            emotional_state = agent.get("emotional_state", {})
            if emotional_state:
                for emotion in emotions_count.keys():
                    value = emotional_state.get(emotion, 0.0)
                    emotions_count[emotion] += value
                total_agents += 1

        if total_agents > 0:
            # Calculate average emotions
            for emotion in emotions_count:
                emotional_summary[emotion] = emotions_count[emotion] / total_agents

            # Find dominant emotion
            dominant = max(
                emotional_summary.items(),
                key=lambda x: x[1] if x[0] != "dominant_emotion" else -1,
            )
            emotional_summary["dominant_emotion"] = dominant[0]

        return emotional_summary

    def _calculate_emotional_success_probability(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        collaboration: MissionCollaboration,
    ) -> float:
        """Calculate mission success probability with emotional state modifiers"""

        # Base success calculation
        base_success = 0.6  # Default

        # Mission difficulty modifier
        difficulty = mission.get("difficulty", "medium")
        difficulty_modifiers = {
            "easy": 0.2,
            "medium": 0.0,
            "hard": -0.2,
            "extreme": -0.4,
        }
        base_success += difficulty_modifiers.get(difficulty, 0.0)

        # Agent skill modifiers
        total_skill_bonus = 0.0
        for agent in agents:
            skills = agent.get("skills", {})
            relevant_skill = self._get_relevant_skill(mission, skills)
            if relevant_skill:
                skill_level = (
                    relevant_skill.get("level", 1)
                    if isinstance(relevant_skill, dict)
                    else 1
                )
                total_skill_bonus += (
                    skill_level - 2
                ) * 0.05  # Skill levels 1-5, average 2-3

        base_success += total_skill_bonus / len(agents) if agents else 0

        # Emotional state impacts
        emotional_modifier = 0.0

        for agent in agents:
            emotional_state = agent.get("emotional_state", {})
            if not emotional_state:
                continue

            # Mission type specific emotional impacts
            mission_type = mission.get("type", "propaganda")

            if mission_type in ["assassination", "sabotage", "rescue"]:
                # Combat/high-risk missions
                fear_penalty = emotional_state.get("fear", 0.0) * 0.15
                anger_bonus = max(0, emotional_state.get("anger", 0.0)) * 0.08
                emotional_modifier += anger_bonus - fear_penalty

            elif mission_type in ["recruitment", "propaganda", "intelligence"]:
                # Social/subtle missions
                trust_bonus = max(0, emotional_state.get("trust", 0.0)) * 0.12
                joy_bonus = max(0, emotional_state.get("joy", 0.0)) * 0.08
                sadness_penalty = emotional_state.get("sadness", 0.0) * 0.1
                emotional_modifier += trust_bonus + joy_bonus - sadness_penalty

            # Trauma always reduces effectiveness
            trauma_level = emotional_state.get("trauma_level", 0.0)
            emotional_modifier -= trauma_level * 0.2

        # Average emotional impact across agents
        emotional_modifier /= len(agents) if agents else 1

        return max(0.05, min(0.95, base_success + emotional_modifier))

    def _get_relevant_skill(
        self, mission: Dict[str, Any], skills: Dict[str, Any]
    ) -> Optional[Any]:
        """Get the most relevant skill for the mission type"""
        mission_type = mission.get("type", "propaganda")

        skill_mapping = {
            "propaganda": "social",
            "intelligence": "stealth",
            "sabotage": "technical",
            "recruitment": "social",
            "assassination": "combat",
            "rescue": "combat",
        }

        relevant_skill_name = skill_mapping.get(mission_type, "social")
        return skills.get(relevant_skill_name)

    def _apply_collaboration_effects(
        self, base_success: float, collaboration: MissionCollaboration
    ) -> float:
        """Apply collaboration bonuses and penalties to success probability"""

        if len(collaboration.agents) <= 1:
            return base_success

        # Positive collaboration effects
        trust_bonus = collaboration.trust_synergy * 0.15
        skill_bonus = collaboration.skill_complementarity * 0.1
        leadership_bonus = collaboration.leadership_effectiveness * 0.1
        cohesion_bonus = collaboration.group_cohesion * 0.12

        # Communication inefficiency penalty
        communication_penalty = (1.0 - collaboration.communication_efficiency) * 0.08

        # Emotional contagion effects
        dominant_emotion = collaboration.emotional_contagion.get(
            "dominant_emotion", "neutral"
        )
        emotion_intensity = collaboration.emotional_contagion.get(dominant_emotion, 0.0)

        emotional_modifier = 0.0
        if dominant_emotion == "fear" and emotion_intensity > 0.5:
            emotional_modifier = -emotion_intensity * 0.12
        elif dominant_emotion == "anger" and emotion_intensity > 0.3:
            emotional_modifier = emotion_intensity * 0.08
        elif dominant_emotion == "joy" and emotion_intensity > 0.3:
            emotional_modifier = emotion_intensity * 0.06

        total_modifier = (
            trust_bonus
            + skill_bonus
            + leadership_bonus
            + cohesion_bonus
            + emotional_modifier
            - communication_penalty
        )

        return max(0.05, min(0.95, base_success + total_modifier))

    def _determine_enhanced_outcome(
        self,
        success_probability: float,
        agents: List[Dict[str, Any]],
        collaboration: MissionCollaboration,
    ) -> EnhancedExecutionOutcome:
        """Determine enhanced mission outcome"""

        roll = random.random()

        # Base outcome determination
        if roll <= success_probability * 0.3:
            base_outcome = EnhancedExecutionOutcome.PERFECT_SUCCESS
        elif roll <= success_probability * 0.7:
            base_outcome = EnhancedExecutionOutcome.SUCCESS_WITH_COMPLICATIONS
        elif roll <= success_probability:
            base_outcome = EnhancedExecutionOutcome.PARTIAL_SUCCESS
        elif roll <= success_probability + 0.15:
            base_outcome = EnhancedExecutionOutcome.FAILURE_WITH_INTEL
        elif roll <= success_probability + 0.3:
            base_outcome = EnhancedExecutionOutcome.COMPLETE_FAILURE
        else:
            base_outcome = EnhancedExecutionOutcome.CATASTROPHIC_FAILURE

        # Apply special outcome modifiers
        return self._apply_special_outcome_modifiers(
            base_outcome, agents, collaboration
        )

    def _apply_special_outcome_modifiers(
        self,
        base_outcome: EnhancedExecutionOutcome,
        agents: List[Dict[str, Any]],
        collaboration: MissionCollaboration,
    ) -> EnhancedExecutionOutcome:
        """Apply special outcome modifiers based on agent states and relationships"""

        # Check for betrayal potential
        betrayal_risk = self._calculate_betrayal_risk(agents)
        if betrayal_risk > 0.7 and random.random() < 0.3:
            return EnhancedExecutionOutcome.BETRAYAL_REVEALED

        # Check for sabotage
        if collaboration.group_cohesion < 0.3 and random.random() < 0.2:
            return EnhancedExecutionOutcome.SABOTAGED_MISSION

        # Tragic success - high emotional cost
        if base_outcome in [
            EnhancedExecutionOutcome.PERFECT_SUCCESS,
            EnhancedExecutionOutcome.SUCCESS_WITH_COMPLICATIONS,
        ] and self._has_high_emotional_cost(agents):
            return EnhancedExecutionOutcome.TRAGIC_SUCCESS

        # Pyrrhic victory - success that undermines future
        if (
            base_outcome == EnhancedExecutionOutcome.PERFECT_SUCCESS
            and collaboration.trust_synergy < 0.3
            and random.random() < 0.15
        ):
            return EnhancedExecutionOutcome.PYRRHIC_VICTORY

        # Beneficial failure - failure that provides unexpected benefits
        if (
            base_outcome
            in [
                EnhancedExecutionOutcome.COMPLETE_FAILURE,
                EnhancedExecutionOutcome.CATASTROPHIC_FAILURE,
            ]
            and random.random() < 0.1
        ):
            return EnhancedExecutionOutcome.BENEFICIAL_FAILURE

        return base_outcome

    def _calculate_betrayal_risk(self, agents: List[Dict[str, Any]]) -> float:
        """Calculate risk of betrayal among mission agents"""

        if len(agents) <= 1:
            return 0.0

        max_betrayal_risk = 0.0

        for agent in agents:
            agent_obj = self.game_state.agents.get(agent["id"])
            if not agent_obj:
                continue

            # Check loyalty level
            loyalty_risk = max(0.0, (50 - agent_obj.loyalty) / 50.0)

            # Check for planned betrayal
            if hasattr(agent_obj, "planned_betrayal") and agent_obj.planned_betrayal:
                loyalty_risk += 0.4

            # Check stress level
            stress_risk = (
                agent_obj.stress / 200.0
            )  # Stress contributes to betrayal risk

            # Check emotional state
            emotional_risk = 0.0
            if hasattr(agent_obj, "emotional_state"):
                emotional_state = agent_obj.emotional_state
                # Anger and fear increase betrayal risk
                emotional_risk = (
                    getattr(emotional_state, "anger", 0.0) * 0.2
                    + getattr(emotional_state, "fear", 0.0) * 0.3
                )

            total_risk = loyalty_risk + stress_risk + emotional_risk
            max_betrayal_risk = max(max_betrayal_risk, total_risk)

        return min(1.0, max_betrayal_risk)

    def _has_high_emotional_cost(self, agents: List[Dict[str, Any]]) -> bool:
        """Check if mission has high emotional cost for agents"""

        high_trauma_agents = 0
        high_stress_agents = 0

        for agent in agents:
            emotional_state = agent.get("emotional_state", {})
            trauma_level = emotional_state.get("trauma_level", 0.0)

            if trauma_level > 0.6:
                high_trauma_agents += 1

            # Check stress from agent data
            agent_obj = self.game_state.agents.get(agent["id"])
            if agent_obj and agent_obj.stress > 70:
                high_stress_agents += 1

        # High emotional cost if majority of agents are traumatized/stressed
        return (high_trauma_agents + high_stress_agents) > len(agents) / 2

    def _generate_enhanced_consequences(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        outcome: EnhancedExecutionOutcome,
        collaboration: MissionCollaboration,
    ) -> List[EnhancedConsequence]:
        """Generate enhanced consequences with emotional and relationship impacts"""

        consequences = []

        # Outcome-specific consequences
        if outcome == EnhancedExecutionOutcome.PERFECT_SUCCESS:
            consequences.extend(
                self._generate_perfect_success_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.SUCCESS_WITH_COMPLICATIONS:
            consequences.extend(
                self._generate_success_with_complications_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.PARTIAL_SUCCESS:
            consequences.extend(
                self._generate_partial_success_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.PARTIAL_SUCCESS_WITH_CONSEQUENCES:
            consequences.extend(
                self._generate_partial_success_with_consequences_consequences(
                    mission, agents
                )
            )
        elif outcome == EnhancedExecutionOutcome.FAILURE_WITH_INTEL:
            consequences.extend(
                self._generate_failure_with_intel_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.FAILURE_WITH_EXPOSURE:
            consequences.extend(
                self._generate_failure_with_exposure_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.COMPLETE_FAILURE:
            consequences.extend(
                self._generate_complete_failure_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.TRAGIC_SUCCESS:
            consequences.extend(
                self._generate_tragic_success_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.PYRRHIC_VICTORY:
            consequences.extend(
                self._generate_pyrrhic_victory_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.BENEFICIAL_FAILURE:
            consequences.extend(
                self._generate_beneficial_failure_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.SABOTAGED_MISSION:
            consequences.extend(
                self._generate_sabotaged_mission_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.BETRAYAL_REVEALED:
            consequences.extend(self._generate_betrayal_consequences(mission, agents))
        elif outcome == EnhancedExecutionOutcome.UNINTENDED_CONSEQUENCES:
            consequences.extend(
                self._generate_unintended_consequences_consequences(mission, agents)
            )
        elif outcome == EnhancedExecutionOutcome.CATASTROPHIC_FAILURE:
            consequences.extend(
                self._generate_catastrophic_failure_consequences(mission, agents)
            )

        # Collaboration-based consequences
        if collaboration.group_cohesion > 0.8:
            consequences.extend(self._generate_high_cohesion_consequences(agents))
        elif collaboration.group_cohesion < 0.3:
            consequences.extend(self._generate_low_cohesion_consequences(agents))

        return consequences

    def _generate_perfect_success_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for perfect mission success"""

        consequences = []

        # Positive morale boost
        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "joy": 0.3,
                "trust": 0.2,
                "anticipation": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="morale_boost",
                description="Perfect mission execution boosts team morale and confidence",
                immediate_effects={"morale": 20, "reputation": 15},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Team celebrates successful operation",
                    "Confidence in future missions increases",
                ],
            )
        )

        return consequences

    def _generate_success_with_complications_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for successful mission with complications"""

        consequences = []

        # Positive morale boost
        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "joy": 0.2,
                "trust": 0.1,
                "anticipation": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="success_with_complications",
                description="Mission succeeds with complications, boosting team morale",
                immediate_effects={"morale": 15, "reputation": 10},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Mission succeeds with challenges",
                    "Team morale remains high",
                ],
            )
        )

        return consequences

    def _generate_partial_success_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for partial mission success"""

        consequences = []

        # Positive morale boost
        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "joy": 0.2,
                "trust": 0.1,
                "anticipation": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="partial_success",
                description="Mission succeeds partially, boosting team morale",
                immediate_effects={"morale": 10, "reputation": 5},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Mission succeeds with limitations",
                    "Team morale remains positive",
                ],
            )
        )

        return consequences

    def _generate_partial_success_with_consequences_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for partial mission success with consequences"""

        consequences = []

        # Positive morale boost
        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "joy": 0.2,
                "trust": 0.1,
                "anticipation": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="partial_success_with_consequences",
                description="Mission succeeds partially with consequences, boosting team morale",
                immediate_effects={"morale": 10, "reputation": 5},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Mission succeeds with limitations",
                    "Team morale remains positive",
                ],
            )
        )

        return consequences

    def _generate_failure_with_intel_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for failure with unexpected intelligence"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "surprise": 0.3,
                "anticipation": 0.2,
                "trust": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="failure_with_intel",
                description="Mission failure unexpectedly provides valuable intelligence",
                immediate_effects={"mission_failure": True, "intelligence_gained": 25},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Failure reveals enemy weakness",
                    "Setback provides new opportunities",
                ],
            )
        )

        return consequences

    def _generate_failure_with_exposure_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for failure with network exposure"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "fear": 0.4,
                "anger": 0.3,
                "trauma_increase": 0.3,
            }

        consequences.append(
            EnhancedConsequence(
                type="failure_with_exposure",
                description="Mission failure exposes the network",
                immediate_effects={"network_exposure": 0.6, "heat_level": 30},
                emotional_impact=emotional_impact,
                narrative_hooks=["Operation blown", "Authorities launch investigation"],
                escalation_potential=0.7,
                recovery_time=3,
            )
        )

        return consequences

    def _generate_complete_failure_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for complete mission failure"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "sadness": 0.5,
                "fear": 0.4,
                "anger": 0.3,
                "trauma_increase": 0.4,
            }

        consequences.append(
            EnhancedConsequence(
                type="complete_failure",
                description="Mission fails completely, exposing the network",
                immediate_effects={"network_exposure": 0.8, "heat_level": 40},
                delayed_effects={"government_crackdown": True},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Operation blown",
                    "Authorities launch massive investigation",
                ],
                escalation_potential=0.9,
                recovery_time=4,
            )
        )

        return consequences

    def _generate_tragic_success_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for tragic success"""

        consequences = []

        # Success but with high emotional cost
        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "sadness": 0.4,
                "joy": 0.2,
                "trauma_increase": 0.3,
            }

        consequences.append(
            EnhancedConsequence(
                type="tragic_success",
                description="Mission succeeds but at great emotional cost to the team",
                immediate_effects={"mission_success": True, "team_trauma": 30},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Victory feels hollow",
                    "Team questions if success was worth the cost",
                ],
                recovery_time=3,
            )
        )

        return consequences

    def _generate_pyrrhic_victory_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for pyrrhic victory"""

        consequences = []

        # Success that undermines future
        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "joy": 0.2,
                "trust": -0.2,
                "trauma_increase": 0.3,
            }

        consequences.append(
            EnhancedConsequence(
                type="pyrrhic_victory",
                description="Mission succeeds but undermines future operations",
                immediate_effects={"mission_success": True, "team_trauma": 20},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Victory feels hollow",
                    "Team questions if success was worth the cost",
                ],
                recovery_time=3,
            )
        )

        return consequences

    def _generate_beneficial_failure_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for beneficial failure"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "surprise": 0.3,
                "anticipation": 0.2,
                "trust": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="beneficial_failure",
                description="Mission failure unexpectedly provides valuable intelligence",
                immediate_effects={"mission_failure": True, "intelligence_gained": 25},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Failure reveals enemy weakness",
                    "Setback provides new opportunities",
                ],
            )
        )

        return consequences

    def _generate_sabotaged_mission_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for sabotaged mission"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "anger": 0.5,
                "trust": -0.4,
                "sadness": 0.3,
            }

        consequences.append(
            EnhancedConsequence(
                type="sabotaged_mission",
                description="Mission sabotaged, shattering team trust",
                immediate_effects={"mission_failure": True, "network_compromise": 0.6},
                emotional_impact=emotional_impact,
                narrative_hooks=["Team discovers sabotage", "Trust network collapses"],
                escalation_potential=0.8,
                recovery_time=5,
            )
        )

        return consequences

    def _generate_betrayal_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for betrayal revelation"""

        consequences = []

        # Identify potential betrayer
        betrayer_id = self._identify_most_likely_betrayer(agents)

        emotional_impact = {}
        relationship_changes = {}

        for agent in agents:
            if agent["id"] != betrayer_id:
                emotional_impact[agent["id"]] = {
                    "anger": 0.5,
                    "trust": -0.4,
                    "sadness": 0.3,
                }
                # Relationship damage with betrayer
                relationship_changes[(agent["id"], betrayer_id)] = {
                    "trust": -0.8,
                    "affinity": -50,
                    "loyalty": -0.6,
                }

        consequences.append(
            EnhancedConsequence(
                type="betrayal_revealed",
                description="Mission reveals betrayal, shattering team trust",
                immediate_effects={"mission_failure": True, "network_compromise": 0.6},
                emotional_impact=emotional_impact,
                relationship_changes=relationship_changes,
                narrative_hooks=[
                    "Team discovers the betrayer",
                    "Trust network collapses",
                ],
                escalation_potential=0.8,
                recovery_time=5,
            )
        )

        return consequences

    def _identify_most_likely_betrayer(self, agents: List[Dict[str, Any]]) -> str:
        """Identify the agent most likely to be a betrayer"""

        if not agents:
            return ""

        min_loyalty = float("inf")
        betrayer_id = agents[0]["id"]

        for agent in agents:
            agent_obj = self.game_state.agents.get(agent["id"])
            if agent_obj and agent_obj.loyalty < min_loyalty:
                min_loyalty = agent_obj.loyalty
                betrayer_id = agent["id"]

        return betrayer_id

    def _generate_unintended_consequences_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for unintended consequences"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "surprise": 0.3,
                "anticipation": 0.2,
                "trust": 0.1,
            }

        consequences.append(
            EnhancedConsequence(
                type="unintended_consequences",
                description="Mission success causes unexpected problems",
                immediate_effects={"mission_success": True, "problem_gained": 20},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Success reveals enemy weakness",
                    "Setback provides new challenges",
                ],
            )
        )

        return consequences

    def _generate_catastrophic_failure_consequences(
        self, mission: Dict[str, Any], agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for catastrophic failure"""

        consequences = []

        emotional_impact = {}
        for agent in agents:
            emotional_impact[agent["id"]] = {
                "sadness": 0.5,
                "fear": 0.4,
                "anger": 0.3,
                "trauma_increase": 0.4,
            }

        consequences.append(
            EnhancedConsequence(
                type="catastrophic_failure",
                description="Mission fails catastrophically, exposing the network",
                immediate_effects={"network_exposure": 0.8, "heat_level": 40},
                delayed_effects={"government_crackdown": True},
                emotional_impact=emotional_impact,
                narrative_hooks=[
                    "Operation blown",
                    "Authorities launch massive investigation",
                ],
                escalation_potential=0.9,
                recovery_time=4,
            )
        )

        return consequences

    def _generate_high_cohesion_consequences(
        self, agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for high team cohesion"""

        consequences = []

        relationship_changes = {}
        emotional_impact = {}

        # Improve relationships between all agents
        for i, agent_a in enumerate(agents):
            emotional_impact[agent_a["id"]] = {"trust": 0.1, "joy": 0.1}
            for agent_b in agents[i + 1 :]:
                relationship_changes[(agent_a["id"], agent_b["id"])] = {
                    "trust": 0.2,
                    "affinity": 10,
                    "loyalty": 0.1,
                }

        consequences.append(
            EnhancedConsequence(
                type="team_bonding",
                description="High team cohesion strengthens bonds between agents",
                immediate_effects={"team_cohesion": 15},
                emotional_impact=emotional_impact,
                relationship_changes=relationship_changes,
                narrative_hooks=[
                    "Team works perfectly together",
                    "Bonds of trust strengthen",
                ],
            )
        )

        return consequences

    def _generate_low_cohesion_consequences(
        self, agents: List[Dict[str, Any]]
    ) -> List[EnhancedConsequence]:
        """Generate consequences for low team cohesion"""

        consequences = []

        relationship_changes = {}
        emotional_impact = {}

        # Strain relationships between agents
        for i, agent_a in enumerate(agents):
            emotional_impact[agent_a["id"]] = {"anger": 0.2, "trust": -0.1}
            for agent_b in agents[i + 1 :]:
                relationship_changes[(agent_a["id"], agent_b["id"])] = {
                    "trust": -0.1,
                    "affinity": -5,
                }

        consequences.append(
            EnhancedConsequence(
                type="team_friction",
                description="Poor team cohesion creates friction and mistrust",
                immediate_effects={"team_friction": 10},
                emotional_impact=emotional_impact,
                relationship_changes=relationship_changes,
                narrative_hooks=[
                    "Team struggles to coordinate",
                    "Tensions rise between agents",
                ],
                recovery_time=2,
            )
        )

        return consequences

    def _calculate_mission_emotional_impacts(
        self,
        outcome: EnhancedExecutionOutcome,
        agents: List[Dict[str, Any]],
        consequences: List[EnhancedConsequence],
    ) -> Dict[str, Dict[str, float]]:
        """Calculate and apply emotional impacts from mission"""

        total_impacts = {}

        # Initialize impact tracking
        for agent in agents:
            total_impacts[agent["id"]] = {}

        # Collect impacts from consequences
        for consequence in consequences:
            for agent_id, impacts in consequence.emotional_impact.items():
                if agent_id not in total_impacts:
                    total_impacts[agent_id] = {}

                for emotion, value in impacts.items():
                    total_impacts[agent_id][emotion] = (
                        total_impacts[agent_id].get(emotion, 0.0) + value
                    )

        # Apply to actual agent emotional states
        for agent_id, impacts in total_impacts.items():
            agent_obj = self.game_state.agents.get(agent_id)
            if agent_obj and hasattr(agent_obj, "emotional_state"):
                for emotion, value in impacts.items():
                    if emotion == "trauma_increase":
                        agent_obj.emotional_state.trauma_level = min(
                            1.0, agent_obj.emotional_state.trauma_level + value
                        )
                    elif hasattr(agent_obj.emotional_state, emotion):
                        current_value = getattr(agent_obj.emotional_state, emotion)
                        new_value = max(-1.0, min(1.0, current_value + value))
                        setattr(agent_obj.emotional_state, emotion, new_value)

        return total_impacts

    def _update_mission_relationships(
        self,
        agents: List[Dict[str, Any]],
        outcome: EnhancedExecutionOutcome,
        collaboration: MissionCollaboration,
    ) -> Dict[Tuple[str, str], Dict[str, float]]:
        """Update relationships based on mission experience"""

        relationship_changes = {}

        if len(agents) <= 1:
            return relationship_changes

        # Base relationship changes from shared experience
        for i, agent_a in enumerate(agents):
            for agent_b in agents[i + 1 :]:
                agent_a_obj = self.game_state.agents.get(agent_a["id"])

                if not agent_a_obj or not hasattr(agent_a_obj, "relationships"):
                    continue

                # Calculate relationship change based on mission outcome
                affinity_change = 0
                trust_change = 0.0
                loyalty_change = 0.0

                if outcome in [
                    EnhancedExecutionOutcome.PERFECT_SUCCESS,
                    EnhancedExecutionOutcome.SUCCESS_WITH_COMPLICATIONS,
                ]:
                    affinity_change = random.randint(5, 15)
                    trust_change = 0.1
                    loyalty_change = 0.05
                elif outcome in [
                    EnhancedExecutionOutcome.CATASTROPHIC_FAILURE,
                    EnhancedExecutionOutcome.BETRAYAL_REVEALED,
                ]:
                    affinity_change = random.randint(-20, -5)
                    trust_change = -0.2
                    loyalty_change = -0.1

                # Apply collaboration modifiers
                if collaboration.group_cohesion > 0.7:
                    affinity_change += 5
                    trust_change += 0.05
                elif collaboration.group_cohesion < 0.3:
                    affinity_change -= 5
                    trust_change -= 0.05

                relationship_changes[(agent_a["id"], agent_b["id"])] = {
                    "affinity": affinity_change,
                    "trust": trust_change,
                    "loyalty": loyalty_change,
                }

        # Apply changes to actual relationships
        for (agent_a_id, agent_b_id), changes in relationship_changes.items():
            agent_a_obj = self.game_state.agents.get(agent_a_id)
            self.game_state.agents.get(agent_b_id)

            if agent_a_obj and hasattr(agent_a_obj, "relationships"):
                if agent_b_id not in agent_a_obj.relationships:
                    # Create new relationship - simplified for demonstration
                    class SimpleRelationship:
                        def __init__(self, agent_a_id, agent_b_id):
                            self.agent_a_id = agent_a_id
                            self.agent_b_id = agent_b_id
                            self.affinity = 0
                            self.trust = 0.0
                            self.loyalty = 0.0

                    agent_a_obj.relationships[agent_b_id] = SimpleRelationship(
                        agent_a_id, agent_b_id
                    )

                rel = agent_a_obj.relationships[agent_b_id]
                rel.affinity = max(-100, min(100, rel.affinity + changes["affinity"]))
                rel.trust = max(0.0, min(1.0, rel.trust + changes["trust"]))
                rel.loyalty = max(0.0, min(1.0, rel.loyalty + changes["loyalty"]))

        return relationship_changes

    def _generate_enhanced_narrative(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        outcome: EnhancedExecutionOutcome,
        consequences: List[EnhancedConsequence],
    ) -> str:
        """Generate enhanced narrative for mission outcome"""

        agent_names = [a.get("name", f"Agent {a['id']}") for a in agents]

        base_narratives = {
            EnhancedExecutionOutcome.PERFECT_SUCCESS: f"{', '.join(agent_names)} execute the mission flawlessly",
            EnhancedExecutionOutcome.TRAGIC_SUCCESS: f"{', '.join(agent_names)} succeed but at great personal cost",
            EnhancedExecutionOutcome.BETRAYAL_REVEALED: f"The mission exposes betrayal within {', '.join(agent_names)}",
            EnhancedExecutionOutcome.CATASTROPHIC_FAILURE: f"{', '.join(agent_names)} face devastating failure",
            EnhancedExecutionOutcome.BENEFICIAL_FAILURE: f"Despite failure, {', '.join(agent_names)} gain unexpected advantages",
        }

        narrative = base_narratives.get(
            outcome, f"{', '.join(agent_names)} complete their mission"
        )

        # Add consequence narratives
        if consequences:
            narrative += ". " + ". ".join([c.description for c in consequences[:2]])

        return narrative


# Integration with existing mission system
def integrate_enhanced_mission_system(game_state):
    """Create an integrated mission executor that works with both systems"""

    enhanced_executor = EnhancedMissionExecutor(game_state)

    def enhanced_mission_wrapper(
        mission_obj, agents_list, location_obj, resources_dict
    ):
        """Wrapper to execute missions with enhanced outcomes"""

        # Convert existing mission system objects to enhanced system format
        mission_dict = convert_mission_to_dict(mission_obj)
        agents_dict_list = convert_agents_to_dict_list(agents_list)
        location_dict = convert_location_to_dict(location_obj)

        # Execute with enhanced system
        result = enhanced_executor.execute_enhanced_mission(
            mission_dict, agents_dict_list, location_dict, resources_dict
        )

        # Convert back to existing system format and apply results
        apply_enhanced_results_to_mission(mission_obj, result, game_state)

        return result

    return enhanced_mission_wrapper


def convert_mission_to_dict(mission_obj) -> Dict[str, Any]:
    """Convert existing Mission object to dictionary format"""

    if hasattr(mission_obj, "__dict__"):
        mission_dict = {
            "id": getattr(mission_obj, "id", "unknown"),
            "type": getattr(mission_obj, "mission_type", "propaganda").value
            if hasattr(getattr(mission_obj, "mission_type", None), "value")
            else str(getattr(mission_obj, "mission_type", "propaganda")),
            "difficulty": "medium",  # Default
            "target_location": getattr(mission_obj, "target_location_id", "unknown"),
        }

        # Add complexity if available
        if hasattr(mission_obj, "complexity"):
            complexity = mission_obj.complexity
            difficulty_level = (
                complexity.calculate_difficulty()
                if hasattr(complexity, "calculate_difficulty")
                else 0.5
            )

            if difficulty_level < 0.3:
                mission_dict["difficulty"] = "easy"
            elif difficulty_level < 0.6:
                mission_dict["difficulty"] = "medium"
            elif difficulty_level < 0.8:
                mission_dict["difficulty"] = "hard"
            else:
                mission_dict["difficulty"] = "extreme"

        return mission_dict

    # Fallback for dict-like objects
    return {
        "id": mission_obj.get("id", "unknown"),
        "type": mission_obj.get("type", "propaganda"),
        "difficulty": mission_obj.get("difficulty", "medium"),
        "target_location": mission_obj.get("target_location", "unknown"),
    }


def convert_agents_to_dict_list(agents_list) -> List[Dict[str, Any]]:
    """Convert list of Agent objects to dictionary format"""

    agents_dict_list = []

    for agent in agents_list:
        if hasattr(agent, "__dict__"):
            # Convert Agent object
            agent_dict = {
                "id": getattr(agent, "id", "unknown"),
                "name": getattr(agent, "name", "Unknown Agent"),
                "skills": {},
                "emotional_state": {},
            }

            # Convert skills
            if hasattr(agent, "skills"):
                for skill_name, skill_obj in agent.skills.items():
                    if hasattr(skill_obj, "level"):
                        agent_dict["skills"][skill_name] = {"level": skill_obj.level}
                    else:
                        agent_dict["skills"][skill_name] = {"level": skill_obj}

            # Convert emotional state
            if hasattr(agent, "emotional_state"):
                emotional_state = agent.emotional_state
                if hasattr(emotional_state, "__dict__"):
                    agent_dict["emotional_state"] = {
                        "fear": getattr(emotional_state, "fear", 0.0),
                        "anger": getattr(emotional_state, "anger", 0.0),
                        "sadness": getattr(emotional_state, "sadness", 0.0),
                        "joy": getattr(emotional_state, "joy", 0.0),
                        "trust": getattr(emotional_state, "trust", 0.0),
                        "anticipation": getattr(emotional_state, "anticipation", 0.0),
                        "trauma_level": getattr(emotional_state, "trauma_level", 0.0),
                    }
                else:
                    agent_dict["emotional_state"] = emotional_state or {}

            agents_dict_list.append(agent_dict)
        else:
            # Fallback for dict-like objects
            agents_dict_list.append(agent)

    return agents_dict_list


def convert_location_to_dict(location_obj) -> Dict[str, Any]:
    """Convert Location object to dictionary format"""

    if hasattr(location_obj, "__dict__"):
        return {
            "id": getattr(location_obj, "id", "unknown"),
            "name": getattr(location_obj, "name", "Unknown Location"),
            "security_level": getattr(location_obj, "security_level", 5),
            "type": getattr(location_obj, "location_type", "urban"),
        }

    # Fallback for dict-like objects
    return {
        "id": location_obj.get("id", "unknown"),
        "name": location_obj.get("name", "Unknown Location"),
        "security_level": location_obj.get("security_level", 5),
        "type": location_obj.get("type", "urban"),
    }


def apply_enhanced_results_to_mission(
    mission_obj, enhanced_result: Dict[str, Any], game_state
):
    """Apply enhanced mission results back to existing mission system"""

    outcome = enhanced_result["outcome"]

    # Determine if mission was successful
    success_outcomes = [
        EnhancedExecutionOutcome.PERFECT_SUCCESS,
        EnhancedExecutionOutcome.SUCCESS_WITH_COMPLICATIONS,
        EnhancedExecutionOutcome.PARTIAL_SUCCESS,
        EnhancedExecutionOutcome.PARTIAL_SUCCESS_WITH_CONSEQUENCES,
        EnhancedExecutionOutcome.TRAGIC_SUCCESS,
        EnhancedExecutionOutcome.PYRRHIC_VICTORY,
        EnhancedExecutionOutcome.BENEFICIAL_FAILURE,  # Still provides value
    ]

    mission_success = outcome in success_outcomes

    # Update mission object
    if hasattr(mission_obj, "complete_mission"):
        turn_number = getattr(game_state, "turn_number", 0)
        mission_obj.complete_mission(mission_success, turn_number)

    # Apply consequences to game state
    consequences = enhanced_result.get("consequences", [])
    for consequence in consequences:
        apply_consequence_to_game_state(consequence, game_state)

    # Apply emotional impacts
    emotional_impacts = enhanced_result.get("emotional_impacts", {})
    for agent_id, impacts in emotional_impacts.items():
        apply_emotional_impact_to_agent(agent_id, impacts, game_state)

    # Apply relationship changes
    relationship_changes = enhanced_result.get("relationship_changes", {})
    for (agent_a_id, agent_b_id), changes in relationship_changes.items():
        apply_relationship_changes_to_agents(
            agent_a_id, agent_b_id, changes, game_state
        )


def apply_consequence_to_game_state(consequence: EnhancedConsequence, game_state):
    """Apply a single consequence to the game state"""

    # Apply immediate effects
    for effect_type, value in consequence.immediate_effects.items():
        if effect_type == "morale" and hasattr(game_state, "faction_morale"):
            current_morale = getattr(game_state, "faction_morale", 50)
            game_state.faction_morale = min(100, max(0, current_morale + value))

        elif effect_type == "reputation" and hasattr(game_state, "reputation"):
            current_reputation = getattr(game_state, "reputation", 50)
            game_state.reputation = min(100, max(0, current_reputation + value))

        elif effect_type == "network_exposure" and hasattr(game_state, "network_heat"):
            current_heat = getattr(game_state, "network_heat", 0.0)
            game_state.network_heat = min(1.0, max(0.0, current_heat + value))

    # Store delayed effects for later processing
    if consequence.delayed_effects and hasattr(game_state, "delayed_consequences"):
        if not hasattr(game_state, "delayed_consequences"):
            game_state.delayed_consequences = []

        game_state.delayed_consequences.append(
            {
                "effects": consequence.delayed_effects,
                "turn_delay": consequence.recovery_time,
                "scheduled_turn": getattr(game_state, "turn_number", 0)
                + consequence.recovery_time,
            }
        )


def apply_emotional_impact_to_agent(
    agent_id: str, impacts: Dict[str, float], game_state
):
    """Apply emotional impacts to a specific agent"""

    if not hasattr(game_state, "agents"):
        return

    agent = game_state.agents.get(agent_id)
    if not agent or not hasattr(agent, "emotional_state"):
        return

    emotional_state = agent.emotional_state

    for emotion, change in impacts.items():
        if emotion == "trauma_increase":
            if hasattr(emotional_state, "trauma_level"):
                emotional_state.trauma_level = min(
                    1.0, emotional_state.trauma_level + change
                )
        elif hasattr(emotional_state, emotion):
            current_value = getattr(emotional_state, emotion)
            new_value = max(-1.0, min(1.0, current_value + change))
            setattr(emotional_state, emotion, new_value)


def apply_relationship_changes_to_agents(
    agent_a_id: str, agent_b_id: str, changes: Dict[str, float], game_state
):
    """Apply relationship changes between two agents"""

    if not hasattr(game_state, "agents"):
        return

    agent_a = game_state.agents.get(agent_a_id)
    agent_b = game_state.agents.get(agent_b_id)

    if not agent_a or not agent_b:
        return

    # Apply changes to agent A's relationships
    if hasattr(agent_a, "relationships"):
        if agent_b_id in agent_a.relationships:
            rel = agent_a.relationships[agent_b_id]

            for change_type, value in changes.items():
                if hasattr(rel, change_type):
                    current_value = getattr(rel, change_type)
                    if change_type == "affinity":
                        new_value = max(-100, min(100, current_value + value))
                    else:  # trust, loyalty
                        new_value = max(0.0, min(1.0, current_value + value))
                    setattr(rel, change_type, new_value)

    # Apply changes to agent B's relationships (symmetric)
    if hasattr(agent_b, "relationships"):
        if agent_a_id in agent_b.relationships:
            rel = agent_b.relationships[agent_a_id]

            for change_type, value in changes.items():
                if hasattr(rel, change_type):
                    current_value = getattr(rel, change_type)
                    if change_type == "affinity":
                        new_value = max(-100, min(100, current_value + value))
                    else:  # trust, loyalty
                        new_value = max(0.0, min(1.0, current_value + value))
                    setattr(rel, change_type, new_value)
