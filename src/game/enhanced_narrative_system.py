"""
Years of Lead - Enhanced Dynamic Narrative Generation System

Phase 4: Dynamic Narrative Generation Enhancement
Implements contextual narrative generation based on agent interactions,
emotional states, and factional dynamics with emergent plotlines.
"""

import random
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


class NarrativeArcType(Enum):
    """Types of narrative arcs"""

    BETRAYAL = "betrayal"
    REDEMPTION = "redemption"
    DESCENT = "descent"
    ASCENSION = "ascension"
    CONFLICT = "conflict"
    RECONCILIATION = "reconciliation"
    ISOLATION = "isolation"
    INTEGRATION = "integration"
    SECRET_REVELATION = "secret_revelation"
    IDENTITY_CRISIS = "identity_crisis"
    LOYALTY_TEST = "loyalty_test"
    SACRIFICE = "sacrifice"
    REVENGE = "revenge"
    FORGIVENESS = "forgiveness"


class NarrativeTrigger(Enum):
    """Triggers for narrative events"""

    EMOTIONAL_BREAKDOWN = "emotional_breakdown"
    TRAUMA_ACCUMULATION = "trauma_accumulation"
    BETRAYAL_DISCOVERY = "betrayal_discovery"
    LOYALTY_CRISIS = "loyalty_crisis"
    RELATIONSHIP_STRAIN = "relationship_strain"
    FACTION_CONFLICT = "faction_conflict"
    MISSION_FAILURE = "mission_failure"
    MISSION_SUCCESS = "mission_success"
    SECRET_EXPOSURE = "secret_exposure"
    IDENTITY_REVELATION = "identity_revelation"


@dataclass
class NarrativeArc:
    """A narrative arc spanning multiple events"""

    id: str
    arc_type: NarrativeArcType
    agents_involved: List[str]
    trigger: NarrativeTrigger
    start_turn: int
    current_stage: int = 0
    total_stages: int = 3
    emotional_tone: str = "neutral"
    complexity: int = 1
    active: bool = True
    completed: bool = False
    story_elements: List[Dict[str, Any]] = field(default_factory=list)
    consequences: List[Dict[str, Any]] = field(default_factory=list)

    def advance_stage(self):
        """Advance the narrative arc to the next stage"""
        if self.current_stage < self.total_stages - 1:
            self.current_stage += 1
        else:
            self.completed = True
            self.active = False

    def add_story_element(self, element: Dict[str, Any]):
        """Add a story element to the arc"""
        self.story_elements.append(element)

    def add_consequence(self, consequence: Dict[str, Any]):
        """Add a consequence to the arc"""
        self.consequences.append(consequence)


@dataclass
class EmergentPlotline:
    """An emergent plotline that develops from agent interactions"""

    id: str
    plotline_type: str
    description: str
    agents_involved: List[str]
    locations_involved: List[str]
    factions_involved: List[str]
    start_turn: int
    current_turn: int
    active: bool = True
    resolution_conditions: List[Dict[str, Any]] = field(default_factory=list)
    story_events: List[Dict[str, Any]] = field(default_factory=list)
    branching_paths: List[Dict[str, Any]] = field(default_factory=list)

    def add_story_event(self, event: Dict[str, Any]):
        """Add a story event to the plotline"""
        self.story_events.append(event)

    def add_branching_path(self, path: Dict[str, Any]):
        """Add a branching path to the plotline"""
        self.branching_paths.append(path)

    def check_resolution(self, game_state) -> bool:
        """Check if plotline resolution conditions are met"""
        for condition in self.resolution_conditions:
            if not self._evaluate_condition(condition, game_state):
                return False
        return True

    def _evaluate_condition(self, condition: Dict[str, Any], game_state) -> bool:
        """Evaluate a resolution condition"""
        condition_type = condition.get("type")

        if condition_type == "agent_state":
            agent_id = condition.get("agent_id")
            required_state = condition.get("state")
            agent = game_state.agents.get(agent_id)
            return agent and agent.status == required_state

        elif condition_type == "relationship_state":
            agent_a = condition.get("agent_a")
            agent_b = condition.get("agent_b")
            min_affinity = condition.get("min_affinity", -100)
            agent_a_obj = game_state.agents.get(agent_a)
            if agent_a_obj and hasattr(agent_a_obj, "relationships"):
                rel = agent_a_obj.relationships.get(agent_b)
                return rel and rel.affinity >= min_affinity

        elif condition_type == "faction_state":
            faction_id = condition.get("faction_id")
            required_state = condition.get("state")
            faction = game_state.factions.get(faction_id)
            return faction and faction.status == required_state

        return False


@dataclass
class ContextualNarrativeHook:
    """A narrative hook based on specific context"""

    id: str
    hook_type: str
    description: str
    context_requirements: Dict[str, Any]
    narrative_template: str
    emotional_impact: Dict[str, float]
    relationship_changes: Dict[Tuple[str, str], Dict[str, float]]
    prerequisites: List[str] = field(default_factory=list)
    cooldown_turns: int = 5
    last_used: Optional[int] = None

    def can_trigger(self, game_state, current_turn: int) -> bool:
        """Check if hook can be triggered"""
        if self.last_used and current_turn - self.last_used < self.cooldown_turns:
            return False

        return self._check_context_requirements(game_state)

    def _check_context_requirements(self, game_state) -> bool:
        """Check if context requirements are met"""
        for requirement, value in self.context_requirements.items():
            if not self._evaluate_requirement(requirement, value, game_state):
                return False
        return True

    def _evaluate_requirement(self, requirement: str, value: Any, game_state) -> bool:
        """Evaluate a context requirement"""
        if requirement == "min_traumatized_agents":
            traumatized_count = sum(
                1
                for agent in game_state.agents.values()
                if hasattr(agent, "emotional_state")
                and agent.emotional_state.trauma_level > 0.6
            )
            return traumatized_count >= value

        elif requirement == "max_faction_loyalty":
            faction_id = value.get("faction_id")
            max_loyalty = value.get("max_loyalty", 100)
            faction_agents = [
                a for a in game_state.agents.values() if a.faction_id == faction_id
            ]
            return all(agent.loyalty <= max_loyalty for agent in faction_agents)

        elif requirement == "relationship_conflict":
            agent_a = value.get("agent_a")
            agent_b = value.get("agent_b")
            min_conflict = value.get("min_conflict", -50)
            agent_a_obj = game_state.agents.get(agent_a)
            if agent_a_obj and hasattr(agent_a_obj, "relationships"):
                rel = agent_a_obj.relationships.get(agent_b)
                return rel and rel.affinity <= min_conflict

        return True


class EnhancedDynamicNarrativeSystem:
    """Enhanced dynamic narrative generation system"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.narrative_arcs: List[NarrativeArc] = []
        self.emergent_plotlines: List[EmergentPlotline] = []
        self.contextual_hooks: List[ContextualNarrativeHook] = []
        self.story_history: List[Dict[str, Any]] = []

        # System parameters
        self.max_active_arcs = 5
        self.max_plotlines = 3
        self.narrative_frequency = 0.3  # 30% chance per turn
        self.arc_completion_threshold = 0.8

        # Tracking
        self.used_hooks: Set[str] = set()
        self.agent_story_participation: Dict[str, int] = defaultdict(int)
        self.faction_story_involvement: Dict[str, int] = defaultdict(int)

        self._initialize_contextual_hooks()

    def _initialize_contextual_hooks(self):
        """Initialize contextual narrative hooks"""

        # Trauma-based hooks
        self.contextual_hooks.append(
            ContextualNarrativeHook(
                id="collective_trauma",
                hook_type="trauma",
                description="Multiple agents share traumatic experiences, creating a collective psychological crisis",
                context_requirements={"min_traumatized_agents": 3},
                narrative_template="The shared trauma of {agent_names} creates a collective psychological crisis. Their experiences bond them in unexpected ways, but also threaten to overwhelm the entire network.",
                emotional_impact={"trauma": 0.3, "fear": 0.2, "sadness": 0.2},
                relationship_changes={},
                cooldown_turns=8,
            )
        )

        # Betrayal hooks
        self.contextual_hooks.append(
            ContextualNarrativeHook(
                id="betrayal_ripple",
                hook_type="betrayal",
                description="A betrayal creates ripples of suspicion throughout the network",
                context_requirements={
                    "relationship_conflict": {
                        "agent_a": "any",
                        "agent_b": "any",
                        "min_conflict": -30,
                    }
                },
                narrative_template="The betrayal between {agent_a} and {agent_b} sends ripples of suspicion through the network. Trust becomes a scarce commodity as agents question their closest allies.",
                emotional_impact={"anger": 0.4, "fear": 0.3, "trust": -0.5},
                relationship_changes={},
                cooldown_turns=6,
            )
        )

        # Faction conflict hooks
        self.contextual_hooks.append(
            ContextualNarrativeHook(
                id="faction_ideological_split",
                hook_type="faction_conflict",
                description="Ideological differences create a faction split",
                context_requirements={
                    "max_faction_loyalty": {"faction_id": "any", "max_loyalty": 60}
                },
                narrative_template="Ideological differences within {faction_name} reach a breaking point. The faction faces an internal crisis as members question their fundamental beliefs.",
                emotional_impact={"anger": 0.3, "sadness": 0.2, "confusion": 0.3},
                relationship_changes={},
                cooldown_turns=10,
            )
        )

    def process_dynamic_narrative(self) -> Dict[str, Any]:
        """Process dynamic narrative generation for the current turn"""
        results = {
            "new_arcs": [],
            "arc_advancements": [],
            "new_plotlines": [],
            "plotline_developments": [],
            "triggered_hooks": [],
            "story_events": [],
            "narrative_consequences": [],
        }

        current_turn = getattr(self.game_state, "turn_number", 1)

        # Check for new narrative triggers
        if random.random() < self.narrative_frequency:
            new_arcs = self._check_for_narrative_triggers(current_turn)
            results["new_arcs"] = new_arcs

        # Advance existing narrative arcs
        arc_advancements = self._advance_narrative_arcs(current_turn)
        results["arc_advancements"] = arc_advancements

        # Check for emergent plotlines
        new_plotlines = self._check_for_emergent_plotlines(current_turn)
        results["new_plotlines"] = new_plotlines

        # Develop existing plotlines
        plotline_developments = self._develop_plotlines(current_turn)
        results["plotline_developments"] = plotline_developments

        # Trigger contextual hooks
        triggered_hooks = self._trigger_contextual_hooks(current_turn)
        results["triggered_hooks"] = triggered_hooks

        # Generate story events
        story_events = self._generate_story_events(results)
        results["story_events"] = story_events

        # Apply narrative consequences
        consequences = self._apply_narrative_consequences(results)
        results["narrative_consequences"] = consequences

        return results

    def _check_for_narrative_triggers(self, current_turn: int) -> List[NarrativeArc]:
        """Check for new narrative triggers and create arcs"""
        new_arcs = []

        # Check agent emotional states for triggers
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, "emotional_state"):
                continue

            emotional_state = agent.emotional_state

            # Trauma accumulation trigger
            if emotional_state.trauma_level > 0.7:
                arc = self._create_trauma_arc(agent_id, current_turn)
                if arc:
                    new_arcs.append(arc)

            # Emotional breakdown trigger
            dominant_emotion, intensity = emotional_state.get_dominant_emotion()
            if intensity > 0.8 and dominant_emotion in ["fear", "anger", "sadness"]:
                arc = self._create_emotional_breakdown_arc(
                    agent_id, dominant_emotion, current_turn
                )
                if arc:
                    new_arcs.append(arc)

        # Check relationships for triggers
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, "relationships"):
                continue

            for other_id, relationship in agent.relationships.items():
                # Betrayal discovery trigger
                if relationship.affinity < -40 and relationship.trust < 0.2:
                    arc = self._create_betrayal_arc(agent_id, other_id, current_turn)
                    if arc:
                        new_arcs.append(arc)

                # Loyalty crisis trigger
                if relationship.loyalty < 0.3 and relationship.affinity > 20:
                    arc = self._create_loyalty_crisis_arc(
                        agent_id, other_id, current_turn
                    )
                    if arc:
                        new_arcs.append(arc)

        # Limit new arcs
        if len(new_arcs) + len(self.narrative_arcs) > self.max_active_arcs:
            new_arcs = new_arcs[: self.max_active_arcs - len(self.narrative_arcs)]

        # Add to active arcs
        self.narrative_arcs.extend(new_arcs)

        return new_arcs

    def _create_trauma_arc(
        self, agent_id: str, current_turn: int
    ) -> Optional[NarrativeArc]:
        """Create a trauma-based narrative arc"""
        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return None

        arc = NarrativeArc(
            id=f"trauma_arc_{agent_id}_{current_turn}",
            arc_type=NarrativeArcType.DESCENT,
            agents_involved=[agent_id],
            trigger=NarrativeTrigger.TRAUMA_ACCUMULATION,
            start_turn=current_turn,
            total_stages=4,
            emotional_tone="tragic",
            complexity=3,
        )

        # Add initial story element
        arc.add_story_element(
            {
                "stage": 0,
                "description": f"{agent.name} begins to show signs of psychological trauma",
                "emotional_impact": {"trauma": 0.2, "fear": 0.1},
            }
        )

        return arc

    def _create_emotional_breakdown_arc(
        self, agent_id: str, emotion: str, current_turn: int
    ) -> Optional[NarrativeArc]:
        """Create an emotional breakdown narrative arc"""
        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return None

        arc = NarrativeArc(
            id=f"breakdown_arc_{agent_id}_{current_turn}",
            arc_type=NarrativeArcType.DESCENT,
            agents_involved=[agent_id],
            trigger=NarrativeTrigger.EMOTIONAL_BREAKDOWN,
            start_turn=current_turn,
            total_stages=3,
            emotional_tone="desperate",
            complexity=2,
        )

        # Add initial story element
        arc.add_story_element(
            {
                "stage": 0,
                "description": f"{agent.name} experiences an emotional breakdown due to overwhelming {emotion}",
                "emotional_impact": {emotion: 0.3, "trauma": 0.1},
            }
        )

        return arc

    def _create_betrayal_arc(
        self, agent_a_id: str, agent_b_id: str, current_turn: int
    ) -> Optional[NarrativeArc]:
        """Create a betrayal narrative arc"""
        agent_a = self.game_state.agents.get(agent_a_id)
        agent_b = self.game_state.agents.get(agent_b_id)
        if not agent_a or not agent_b:
            return None

        arc = NarrativeArc(
            id=f"betrayal_arc_{agent_a_id}_{agent_b_id}_{current_turn}",
            arc_type=NarrativeArcType.BETRAYAL,
            agents_involved=[agent_a_id, agent_b_id],
            trigger=NarrativeTrigger.BETRAYAL_DISCOVERY,
            start_turn=current_turn,
            total_stages=4,
            emotional_tone="devastating",
            complexity=4,
        )

        # Add initial story element
        arc.add_story_element(
            {
                "stage": 0,
                "description": f"{agent_a.name} discovers evidence of betrayal by {agent_b.name}",
                "emotional_impact": {"anger": 0.4, "sadness": 0.3, "trust": -0.5},
            }
        )

        return arc

    def _create_loyalty_crisis_arc(
        self, agent_a_id: str, agent_b_id: str, current_turn: int
    ) -> Optional[NarrativeArc]:
        """Create a loyalty crisis narrative arc"""
        agent_a = self.game_state.agents.get(agent_a_id)
        agent_b = self.game_state.agents.get(agent_b_id)
        if not agent_a or not agent_b:
            return None

        arc = NarrativeArc(
            id=f"loyalty_arc_{agent_a_id}_{agent_b_id}_{current_turn}",
            arc_type=NarrativeArcType.LOYALTY_TEST,
            agents_involved=[agent_a_id, agent_b_id],
            trigger=NarrativeTrigger.LOYALTY_CRISIS,
            start_turn=current_turn,
            total_stages=3,
            emotional_tone="conflicted",
            complexity=3,
        )

        # Add initial story element
        arc.add_story_element(
            {
                "stage": 0,
                "description": f"{agent_a.name} faces a loyalty crisis regarding {agent_b.name}",
                "emotional_impact": {"confusion": 0.3, "sadness": 0.2},
            }
        )

        return arc

    def _advance_narrative_arcs(self, current_turn: int) -> List[Dict[str, Any]]:
        """Advance existing narrative arcs"""
        advancements = []

        for arc in self.narrative_arcs:
            if not arc.active:
                continue

            # Check if arc should advance
            advancement_chance = self._calculate_arc_advancement_chance(arc)
            if random.random() < advancement_chance:
                # Advance the arc
                old_stage = arc.current_stage
                arc.advance_stage()

                # Generate story element for new stage
                story_element = self._generate_arc_story_element(arc)
                arc.add_story_element(story_element)

                advancements.append(
                    {
                        "arc_id": arc.id,
                        "old_stage": old_stage,
                        "new_stage": arc.current_stage,
                        "story_element": story_element,
                        "completed": arc.completed,
                    }
                )

                # Track agent participation
                for agent_id in arc.agents_involved:
                    self.agent_story_participation[agent_id] += 1

        return advancements

    def _calculate_arc_advancement_chance(self, arc: NarrativeArc) -> float:
        """Calculate chance of arc advancement"""
        base_chance = 0.3

        # Complexity affects advancement speed
        complexity_modifier = (6 - arc.complexity) * 0.1  # Higher complexity = slower

        # Emotional intensity affects advancement
        emotional_modifier = 0.0
        for agent_id in arc.agents_involved:
            agent = self.game_state.agents.get(agent_id)
            if agent and hasattr(agent, "emotional_state"):
                (
                    dominant_emotion,
                    intensity,
                ) = agent.emotional_state.get_dominant_emotion()
                emotional_modifier += intensity * 0.2

        # Arc type affects advancement
        type_modifiers = {
            NarrativeArcType.BETRAYAL: 0.2,
            NarrativeArcType.DESCENT: 0.15,
            NarrativeArcType.LOYALTY_TEST: 0.1,
            NarrativeArcType.REDEMPTION: 0.05,
        }
        type_modifier = type_modifiers.get(arc.arc_type, 0.0)

        return min(
            0.8, base_chance + complexity_modifier + emotional_modifier + type_modifier
        )

    def _generate_arc_story_element(self, arc: NarrativeArc) -> Dict[str, Any]:
        """Generate a story element for an arc stage"""
        agent_names = [
            self.game_state.agents.get(
                aid, type("obj", (), {"name": f"Agent_{aid}"})
            ).name
            for aid in arc.agents_involved
        ]

        story_templates = {
            NarrativeArcType.DESCENT: [
                f"The psychological pressure on {agent_names[0]} continues to mount",
                f"{agent_names[0]} begins to isolate themselves from the network",
                f"The trauma takes its toll on {agent_names[0]}'s decision-making",
            ],
            NarrativeArcType.BETRAYAL: [
                f"The betrayal between {agent_names[0]} and {agent_names[1]} deepens",
                "Other agents begin to take sides in the conflict",
                "The network fractures along lines of loyalty",
            ],
            NarrativeArcType.LOYALTY_TEST: [
                f"{agent_names[0]} must choose between conflicting loyalties",
                f"The crisis forces {agent_names[0]} to question their values",
                "Both agents struggle with their commitments",
            ],
        }

        templates = story_templates.get(
            arc.arc_type, [f"The story continues for {', '.join(agent_names)}"]
        )
        description = random.choice(templates)

        return {
            "stage": arc.current_stage,
            "description": description,
            "emotional_impact": self._calculate_stage_emotional_impact(arc),
        }

    def _calculate_stage_emotional_impact(self, arc: NarrativeArc) -> Dict[str, float]:
        """Calculate emotional impact for arc stage"""
        base_impact = {"trauma": 0.1, "sadness": 0.1, "anger": 0.1}

        # Modify based on arc type and stage
        if arc.arc_type == NarrativeArcType.DESCENT:
            base_impact["trauma"] += 0.2
            base_impact["fear"] = 0.15
        elif arc.arc_type == NarrativeArcType.BETRAYAL:
            base_impact["anger"] += 0.2
            base_impact["trust"] = -0.2
        elif arc.arc_type == NarrativeArcType.LOYALTY_TEST:
            base_impact["confusion"] = 0.2
            base_impact["sadness"] += 0.1

        # Later stages have stronger impact
        if arc.current_stage > 1:
            for emotion in base_impact:
                if base_impact[emotion] > 0:
                    base_impact[emotion] *= 1.5
                elif base_impact[emotion] < 0:
                    base_impact[emotion] *= 1.5

        return base_impact

    def _check_for_emergent_plotlines(
        self, current_turn: int
    ) -> List[EmergentPlotline]:
        """Check for emergent plotlines from agent interactions"""
        new_plotlines = []

        # Check for faction conflicts
        faction_conflicts = self._detect_faction_conflicts()
        for conflict in faction_conflicts:
            plotline = self._create_faction_conflict_plotline(conflict, current_turn)
            if plotline:
                new_plotlines.append(plotline)

        # Check for network-wide patterns
        network_patterns = self._detect_network_patterns()
        for pattern in network_patterns:
            plotline = self._create_network_pattern_plotline(pattern, current_turn)
            if plotline:
                new_plotlines.append(plotline)

        # Limit new plotlines
        if len(new_plotlines) + len(self.emergent_plotlines) > self.max_plotlines:
            new_plotlines = new_plotlines[
                : self.max_plotlines - len(self.emergent_plotlines)
            ]

        # Add to active plotlines
        self.emergent_plotlines.extend(new_plotlines)

        return new_plotlines

    def _detect_faction_conflicts(self) -> List[Dict[str, Any]]:
        """Detect conflicts between factions"""
        conflicts = []

        faction_agents = defaultdict(list)
        for agent_id, agent in self.game_state.agents.items():
            faction_agents[agent.faction_id].append(agent_id)

        # Check for inter-faction relationship conflicts
        for faction_a_id, agents_a in faction_agents.items():
            for faction_b_id, agents_b in faction_agents.items():
                if faction_a_id >= faction_b_id:
                    continue

                conflict_score = 0
                for agent_a_id in agents_a:
                    agent_a = self.game_state.agents.get(agent_a_id)
                    if not agent_a or not hasattr(agent_a, "relationships"):
                        continue

                    for agent_b_id in agents_b:
                        rel = agent_a.relationships.get(agent_b_id)
                        if rel and rel.affinity < -20:
                            conflict_score += abs(rel.affinity)

                if conflict_score > 100:  # Threshold for faction conflict
                    conflicts.append(
                        {
                            "faction_a": faction_a_id,
                            "faction_b": faction_b_id,
                            "conflict_score": conflict_score,
                            "agents_involved": agents_a + agents_b,
                        }
                    )

        return conflicts

    def _create_faction_conflict_plotline(
        self, conflict: Dict[str, Any], current_turn: int
    ) -> Optional[EmergentPlotline]:
        """Create a faction conflict plotline"""
        plotline = EmergentPlotline(
            id=f"faction_conflict_{conflict['faction_a']}_{conflict['faction_b']}_{current_turn}",
            plotline_type="faction_conflict",
            description=f"Growing conflict between factions {conflict['faction_a']} and {conflict['faction_b']} threatens network stability",
            agents_involved=conflict["agents_involved"],
            locations_involved=[],
            factions_involved=[conflict["faction_a"], conflict["faction_b"]],
            start_turn=current_turn,
            current_turn=current_turn,
        )

        # Add resolution conditions
        plotline.resolution_conditions = [
            {
                "type": "faction_state",
                "faction_id": conflict["faction_a"],
                "state": "reconciled",
            },
            {
                "type": "faction_state",
                "faction_id": conflict["faction_b"],
                "state": "reconciled",
            },
        ]

        # Add initial story event
        plotline.add_story_event(
            {
                "turn": current_turn,
                "description": f"Tensions between factions {conflict['faction_a']} and {conflict['faction_b']} reach a breaking point",
                "impact": "network_instability",
            }
        )

        return plotline

    def _detect_network_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns across the agent network"""
        patterns = []

        # Check for isolation patterns
        isolated_agents = []
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, "relationships"):
                continue

            positive_relationships = sum(
                1 for rel in agent.relationships.values() if rel.affinity > 10
            )
            if positive_relationships < 2:
                isolated_agents.append(agent_id)

        if len(isolated_agents) >= 3:
            patterns.append(
                {
                    "type": "isolation",
                    "description": "Multiple agents becoming isolated from the network",
                    "agents_involved": isolated_agents,
                    "severity": len(isolated_agents),
                }
            )

        # Check for trauma clusters
        traumatized_agents = []
        for agent_id, agent in self.game_state.agents.items():
            if (
                hasattr(agent, "emotional_state")
                and agent.emotional_state.trauma_level > 0.6
            ):
                traumatized_agents.append(agent_id)

        if len(traumatized_agents) >= 3:
            patterns.append(
                {
                    "type": "trauma_cluster",
                    "description": "Trauma spreading through multiple agents",
                    "agents_involved": traumatized_agents,
                    "severity": len(traumatized_agents),
                }
            )

        return patterns

    def _create_network_pattern_plotline(
        self, pattern: Dict[str, Any], current_turn: int
    ) -> Optional[EmergentPlotline]:
        """Create a network pattern plotline"""
        plotline = EmergentPlotline(
            id=f"network_pattern_{pattern['type']}_{current_turn}",
            plotline_type=pattern["type"],
            description=pattern["description"],
            agents_involved=pattern["agents_involved"],
            locations_involved=[],
            factions_involved=[],
            start_turn=current_turn,
            current_turn=current_turn,
        )

        # Add resolution conditions based on pattern type
        if pattern["type"] == "isolation":
            plotline.resolution_conditions = [
                {"type": "agent_state", "agent_id": aid, "state": "connected"}
                for aid in pattern["agents_involved"][
                    :2
                ]  # Require 2 agents to reconnect
            ]
        elif pattern["type"] == "trauma_cluster":
            plotline.resolution_conditions = [
                {"type": "agent_state", "agent_id": aid, "state": "recovered"}
                for aid in pattern["agents_involved"][:2]  # Require 2 agents to recover
            ]

        # Add initial story event
        plotline.add_story_event(
            {
                "turn": current_turn,
                "description": pattern["description"],
                "impact": pattern["type"],
            }
        )

        return plotline

    def _develop_plotlines(self, current_turn: int) -> List[Dict[str, Any]]:
        """Develop existing plotlines"""
        developments = []

        for plotline in self.emergent_plotlines:
            if not plotline.active:
                continue

            plotline.current_turn = current_turn

            # Check for resolution
            if plotline.check_resolution(self.game_state):
                plotline.active = False
                developments.append(
                    {
                        "plotline_id": plotline.id,
                        "type": "resolved",
                        "description": f"Plotline '{plotline.description}' has been resolved",
                    }
                )
                continue

            # Generate development event
            development_chance = 0.4  # 40% chance per turn
            if random.random() < development_chance:
                event = self._generate_plotline_development(plotline, current_turn)
                plotline.add_story_event(event)

                developments.append(
                    {"plotline_id": plotline.id, "type": "developed", "event": event}
                )

        return developments

    def _generate_plotline_development(
        self, plotline: EmergentPlotline, current_turn: int
    ) -> Dict[str, Any]:
        """Generate a development event for a plotline"""
        development_templates = {
            "faction_conflict": [
                "The conflict escalates as more agents take sides",
                "Attempts at mediation fail to resolve the tensions",
                "The factions begin competing for resources and influence",
            ],
            "isolation": [
                "Isolated agents begin to form their own sub-networks",
                "The isolation spreads as other agents become wary",
                "Communication breakdowns threaten network cohesion",
            ],
            "trauma_cluster": [
                "The trauma begins to affect mission effectiveness",
                "Agents start avoiding high-risk operations",
                "The psychological strain creates new conflicts",
            ],
        }

        templates = development_templates.get(
            plotline.plotline_type, ["The situation continues to develop"]
        )
        description = random.choice(templates)

        return {
            "turn": current_turn,
            "description": description,
            "impact": plotline.plotline_type,
        }

    def _trigger_contextual_hooks(self, current_turn: int) -> List[Dict[str, Any]]:
        """Trigger contextual narrative hooks"""
        triggered_hooks = []

        for hook in self.contextual_hooks:
            if hook.can_trigger(self.game_state, current_turn):
                # Generate narrative from hook
                narrative = self._generate_hook_narrative(hook)

                # Apply emotional and relationship impacts
                self._apply_hook_impacts(hook)

                # Mark as used
                hook.last_used = current_turn
                self.used_hooks.add(hook.id)

                triggered_hooks.append(
                    {
                        "hook_id": hook.id,
                        "hook_type": hook.hook_type,
                        "narrative": narrative,
                        "impacts": {
                            "emotional": hook.emotional_impact,
                            "relationships": hook.relationship_changes,
                        },
                    }
                )

        return triggered_hooks

    def _generate_hook_narrative(self, hook: ContextualNarrativeHook) -> str:
        """Generate narrative from a contextual hook"""
        narrative = hook.narrative_template

        # Fill in agent names
        if "{agent_names}" in narrative:
            agent_names = [
                self.game_state.agents.get(
                    aid, type("obj", (), {"name": f"Agent_{aid}"})
                ).name
                for aid in self.game_state.agents.keys()
            ]
            narrative = narrative.replace("{agent_names}", ", ".join(agent_names[:3]))

        # Fill in faction names
        if "{faction_name}" in narrative:
            faction_names = list(self.game_state.factions.keys())
            if faction_names:
                narrative = narrative.replace("{faction_name}", faction_names[0])

        return narrative

    def _apply_hook_impacts(self, hook: ContextualNarrativeHook):
        """Apply hook impacts to agents and relationships"""

        # Apply emotional impacts to all agents
        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "emotional_state"):
                for emotion, value in hook.emotional_impact.items():
                    if hasattr(agent.emotional_state, emotion):
                        current_value = getattr(agent.emotional_state, emotion)
                        new_value = max(-1.0, min(1.0, current_value + value))
                        setattr(agent.emotional_state, emotion, new_value)

        # Apply relationship changes
        for (agent_a_id, agent_b_id), changes in hook.relationship_changes.items():
            agent_a = self.game_state.agents.get(agent_a_id)
            if agent_a and hasattr(agent_a, "relationships"):
                if agent_b_id not in agent_a.relationships:
                    # Create new relationship
                    from .relationships import Relationship, BondType

                    agent_a.relationships[agent_b_id] = Relationship(
                        agent_a_id=agent_a_id,
                        agent_b_id=agent_b_id,
                        bond_type=BondType.NEUTRAL,
                        affinity=0,
                        trust=0.0,
                        loyalty=0.0,
                    )

                rel = agent_a.relationships[agent_b_id]
                for attr, value in changes.items():
                    if hasattr(rel, attr):
                        current_value = getattr(rel, attr)
                        if attr == "affinity":
                            new_value = max(-100, min(100, current_value + value))
                        else:
                            new_value = max(0.0, min(1.0, current_value + value))
                        setattr(rel, attr, new_value)

    def _generate_story_events(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate story events from narrative results"""
        story_events = []

        # Convert arc advancements to story events
        for advancement in results["arc_advancements"]:
            story_events.append(
                {
                    "type": "arc_advancement",
                    "arc_id": advancement["arc_id"],
                    "description": advancement["story_element"]["description"],
                    "emotional_impact": advancement["story_element"][
                        "emotional_impact"
                    ],
                }
            )

        # Convert plotline developments to story events
        for development in results["plotline_developments"]:
            if development["type"] == "developed":
                story_events.append(
                    {
                        "type": "plotline_development",
                        "plotline_id": development["plotline_id"],
                        "description": development["event"]["description"],
                        "impact": development["event"]["impact"],
                    }
                )

        # Convert triggered hooks to story events
        for hook in results["triggered_hooks"]:
            story_events.append(
                {
                    "type": "contextual_hook",
                    "hook_type": hook["hook_type"],
                    "description": hook["narrative"],
                    "impacts": hook["impacts"],
                }
            )

        return story_events

    def _apply_narrative_consequences(
        self, results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply narrative consequences to the game state"""
        consequences = []

        # Apply story event consequences
        for event in results["story_events"]:
            consequence = self._apply_story_event_consequence(event)
            if consequence:
                consequences.append(consequence)

        return consequences

    def _apply_story_event_consequence(
        self, event: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Apply consequence for a single story event"""

        if event["type"] == "arc_advancement":
            # Apply emotional impacts to involved agents
            arc = next(
                (a for a in self.narrative_arcs if a.id == event["arc_id"]), None
            )
            if arc:
                for agent_id in arc.agents_involved:
                    agent = self.game_state.agents.get(agent_id)
                    if agent and hasattr(agent, "emotional_state"):
                        for emotion, value in event["emotional_impact"].items():
                            if hasattr(agent.emotional_state, emotion):
                                current_value = getattr(agent.emotional_state, emotion)
                                new_value = max(-1.0, min(1.0, current_value + value))
                                setattr(agent.emotional_state, emotion, new_value)

                return {
                    "type": "emotional_impact",
                    "agents": arc.agents_involved,
                    "impacts": event["emotional_impact"],
                }

        elif event["type"] == "contextual_hook":
            # Hook impacts already applied, just return summary
            return {
                "type": "hook_consequence",
                "hook_type": event["hook_type"],
                "description": "Contextual hook consequences applied",
            }

        return None

    def get_narrative_summary(self) -> Dict[str, Any]:
        """Get comprehensive narrative system summary"""

        active_arcs = [arc for arc in self.narrative_arcs if arc.active]
        active_plotlines = [
            plotline for plotline in self.emergent_plotlines if plotline.active
        ]

        return {
            "active_narrative_arcs": len(active_arcs),
            "active_plotlines": len(active_plotlines),
            "total_story_events": len(self.story_history),
            "used_hooks": len(self.used_hooks),
            "agent_participation": dict(self.agent_story_participation),
            "faction_involvement": dict(self.faction_story_involvement),
            "arc_types": self._get_arc_type_breakdown(),
            "plotline_types": self._get_plotline_type_breakdown(),
            "system_efficiency": self._calculate_narrative_efficiency(),
        }

    def _get_arc_type_breakdown(self) -> Dict[str, int]:
        """Get breakdown of narrative arc types"""
        breakdown = defaultdict(int)
        for arc in self.narrative_arcs:
            breakdown[arc.arc_type.value] += 1
        return dict(breakdown)

    def _get_plotline_type_breakdown(self) -> Dict[str, int]:
        """Get breakdown of plotline types"""
        breakdown = defaultdict(int)
        for plotline in self.emergent_plotlines:
            breakdown[plotline.plotline_type] += 1
        return dict(breakdown)

    def _calculate_narrative_efficiency(self) -> float:
        """Calculate narrative system efficiency"""

        if not self.narrative_arcs and not self.emergent_plotlines:
            return 0.0

        # Efficiency based on story generation and resolution
        total_arcs = len(self.narrative_arcs)
        completed_arcs = sum(1 for arc in self.narrative_arcs if arc.completed)
        completion_rate = completed_arcs / total_arcs if total_arcs > 0 else 0.0

        # Agent participation diversity
        participation_scores = list(self.agent_story_participation.values())
        participation_variance = 0.0
        if participation_scores:
            mean_participation = sum(participation_scores) / len(participation_scores)
            participation_variance = sum(
                (score - mean_participation) ** 2 for score in participation_scores
            ) / len(participation_scores)

        # Hook utilization
        hook_utilization = (
            len(self.used_hooks) / len(self.contextual_hooks)
            if self.contextual_hooks
            else 0.0
        )

        overall_efficiency = (
            completion_rate * 0.4
            + min(1.0, 1.0 - (participation_variance / 100)) * 0.3
            + hook_utilization * 0.3
        )

        return min(1.0, overall_efficiency)
