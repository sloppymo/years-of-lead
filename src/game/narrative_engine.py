"""
Narrative Engine Integration for Years of Lead

This module provides integration between the relationship system and SYLVA/WREN
for enhanced narrative generation and emotional storytelling.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import random
import json
from .relationships import Relationship, BondType, EventType, SocialNetwork
from .core import Agent, GameState
from .advanced_relationships import Secret, MemoryEntry, BetrayalPlan, SecretType
from .dynamic_narrative_tone import (
    DynamicNarrativeToneEngine, VoiceConfiguration, EmotionalTone,
    SymbolicElement, NarrativeStyle, VoiceCommandHandler
)


@dataclass
class NarrativeTemplate:
    """Template for generating relationship-based narratives"""
    id: str
    title: str
    template: str
    required_bond_type: Optional[BondType] = None
    min_affinity: Optional[float] = None
    max_affinity: Optional[float] = None
    min_trust: Optional[float] = None
    max_trust: Optional[float] = None
    min_loyalty: Optional[float] = None
    max_loyalty: Optional[float] = None
    required_tags: List[str] = field(default_factory=list)
    excluded_tags: List[str] = field(default_factory=list)
    emotional_tone: str = "neutral"
    complexity: int = 1  # 1-5 scale
    rarity: float = 1.0  # 0.0-1.0 scale
    # Advanced relationship fields
    requires_secret: bool = False
    requires_memory: bool = False
    requires_persona: bool = False
    requires_ideology_conflict: bool = False
    secret_type: Optional[SecretType] = None
    memory_tone: Optional[str] = None


class NarrativeEngine:
    """Manages narrative generation with relationship and SYLVA/WREN integration"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.templates = self._initialize_templates()
        self.recently_used = []
        self.max_recent = 10

        # SYLVA/WREN integration placeholders
        self.sylva_enabled = False
        self.wren_enabled = False

        # Dynamic Narrative Tone System integration
        self.tone_engine = DynamicNarrativeToneEngine()
        self.voice_handler = self.tone_engine.create_voice_command_handler()

    def _initialize_templates(self) -> List[NarrativeTemplate]:
        """Initialize relationship-based narrative templates"""
        templates = [
            # Advanced relationship templates - Secrets & Blackmail
            NarrativeTemplate(
                id="secret_discovery_shock",
                title="Secret Discovery Shock",
                template="{agent_a.name} discovers {agent_b.name}'s secret: {secret_description}. The revelation shakes their trust to the core.",
                requires_secret=True,
                min_trust=0.4,
                emotional_tone="shocked",
                complexity=4,
                rarity=0.3
            ),

            NarrativeTemplate(
                id="blackmail_attempt",
                title="Blackmail Attempt",
                template="{agent_a.name} attempts to blackmail {agent_b.name} using their knowledge of {secret_description}, creating a tense power dynamic.",
                requires_secret=True,
                secret_type=SecretType.PERSONAL,
                emotional_tone="tense",
                complexity=4,
                rarity=0.2
            ),

            NarrativeTemplate(
                id="rumor_spread",
                title="Rumor Spread",
                template="Rumors about {agent_b.name}'s {secret_description} begin circulating through the network, causing paranoia and suspicion.",
                requires_secret=True,
                emotional_tone="paranoid",
                complexity=3,
                rarity=0.4
            ),

            # Memory Journal templates
            NarrativeTemplate(
                id="memory_haunts_present",
                title="Memory Haunts Present",
                template="{agent_a.name} is haunted by memories of {agent_b.name} from {memory_summary}, affecting their current interactions.",
                requires_memory=True,
                emotional_tone="haunted",
                complexity=3,
                rarity=0.4
            ),

            NarrativeTemplate(
                id="shared_trauma_bond",
                title="Shared Trauma Bond",
                template="{agent_a.name} and {agent_b.name} share a traumatic memory: {memory_summary}. This shared experience creates an unbreakable bond.",
                requires_memory=True,
                memory_tone="traumatic",
                emotional_tone="bonded",
                complexity=4,
                rarity=0.3
            ),

            # Persona Mask templates
            NarrativeTemplate(
                id="mask_slippage",
                title="Mask Slippage",
                template="{agent_a.name} notices inconsistencies in {agent_b.name}'s behavior, suspecting they're hiding their true feelings.",
                requires_persona=True,
                emotional_tone="suspicious",
                complexity=3,
                rarity=0.4
            ),

            NarrativeTemplate(
                id="mask_revealed",
                title="Mask Revealed",
                template="{agent_a.name} finally sees through {agent_b.name}'s carefully constructed persona, revealing their true nature.",
                requires_persona=True,
                emotional_tone="betrayed",
                complexity=4,
                rarity=0.2
            ),

            # Ideological Conflict templates
            NarrativeTemplate(
                id="ideological_break",
                title="Ideological Break",
                template="{agent_a.name} and {agent_b.name} clash over fundamental ideological differences, {agent_a.name} being more {ideology_a} while {agent_b.name} leans {ideology_b}.",
                requires_ideology_conflict=True,
                emotional_tone="conflicted",
                complexity=3,
                rarity=0.5
            ),

            NarrativeTemplate(
                id="ideological_conversion",
                title="Ideological Conversion",
                template="{agent_a.name} begins to question their beliefs after discussions with {agent_b.name}, whose {dominant_ideology} perspective proves compelling.",
                requires_ideology_conflict=True,
                emotional_tone="questioning",
                complexity=4,
                rarity=0.3
            ),

            # Betrayal Planning templates
            NarrativeTemplate(
                id="betrayal_planning",
                title="Betrayal Planning",
                template="{agent_a.name} secretly begins planning to betray {agent_b.name}, carefully considering timing and potential co-conspirators.",
                emotional_tone="calculating",
                complexity=4,
                rarity=0.2
            ),

            NarrativeTemplate(
                id="betrayal_executed",
                title="Betrayal Executed",
                template="{agent_a.name} executes their planned betrayal of {agent_b.name}, the carefully orchestrated deception finally revealed.",
                emotional_tone="devastating",
                complexity=5,
                rarity=0.1
            ),

            # Emotion Propagation templates
            NarrativeTemplate(
                id="emotional_contagion",
                title="Emotional Contagion",
                template="{agent_a.name}'s {dominant_emotion_a} begins to affect {agent_b.name}, who starts feeling {dominant_emotion_b} as well.",
                emotional_tone="contagious",
                complexity=2,
                rarity=0.6
            ),

            # Faction Fracture templates
            NarrativeTemplate(
                id="faction_fracture",
                title="Faction Fracture",
                template="The ideological rift between {agent_a.name} and {agent_b.name} leads to a faction fracture, with {defector_names} forming a splinter group.",
                emotional_tone="divisive",
                complexity=4,
                rarity=0.2
            ),

            # Legacy templates (keeping existing ones)
            NarrativeTemplate(
                id="sibling_betrayal",
                title="Sibling Betrayal",
                template="{agent_a.name} discovers that {agent_b.name} has been working with the authorities, shattering their bond of trust.",
                required_bond_type=BondType.FAMILY,
                min_affinity=30,
                min_trust=0.6,
                emotional_tone="devastating",
                complexity=4,
                rarity=0.3
            ),

            NarrativeTemplate(
                id="ex_lover_sabotage",
                title="Ex-Lover Sabotage",
                template="{agent_a.name} learns that {agent_b.name} has been sabotaging their operations, driven by old resentments.",
                required_bond_type=BondType.EX_LOVER,
                max_affinity=-10,
                emotional_tone="bitter",
                complexity=3,
                rarity=0.4
            ),

            # Mentorship narratives
            NarrativeTemplate(
                id="mentor_disillusionment",
                title="Mentor Disillusionment",
                template="{agent_a.name} realizes that {agent_b.name} has lost faith in the cause, causing deep disappointment.",
                required_bond_type=BondType.MENTOR,
                min_affinity=20,
                min_trust=0.5,
                emotional_tone="disappointed",
                complexity=3,
                rarity=0.5
            ),

            NarrativeTemplate(
                id="student_exceeds_mentor",
                title="Student Exceeds Mentor",
                template="{agent_b.name} has surpassed {agent_a.name}'s expectations, creating both pride and insecurity.",
                required_bond_type=BondType.MENTOR,
                min_affinity=30,
                min_trust=0.6,
                emotional_tone="proud",
                complexity=2,
                rarity=0.6
            ),

            # Rescue narratives
            NarrativeTemplate(
                id="unexpected_ally_rescue",
                title="Unexpected Ally Rescue",
                template="{agent_b.name} unexpectedly comes to {agent_a.name}'s aid during a dangerous mission.",
                min_affinity=-20,
                max_affinity=10,
                min_trust=0.3,
                emotional_tone="surprised",
                complexity=2,
                rarity=0.7
            ),

            # Grief narratives
            NarrativeTemplate(
                id="grief_spiral_friend_arrest",
                title="Grief Spiral from Friend's Arrest",
                template="{agent_a.name} spirals into grief after {agent_b.name} is arrested, questioning their own safety.",
                required_bond_type=BondType.FRIEND,
                min_affinity=20,
                min_trust=0.5,
                emotional_tone="grieving",
                complexity=4,
                rarity=0.4
            ),

            # Loyalty narratives
            NarrativeTemplate(
                id="loyalty_proven_under_fire",
                title="Loyalty Proven Under Fire",
                template="{agent_b.name} proves their loyalty to {agent_a.name} during a critical moment of danger.",
                min_affinity=10,
                min_trust=0.4,
                emotional_tone="grateful",
                complexity=2,
                rarity=0.8
            ),

            # Conflict narratives
            NarrativeTemplate(
                id="ideological_conflict",
                title="Ideological Conflict",
                template="{agent_a.name} and {agent_b.name} clash over fundamental differences in their approach to the resistance.",
                required_tags=["idealistic", "practical"],
                emotional_tone="tense",
                complexity=3,
                rarity=0.6
            ),

            # Cooperation narratives
            NarrativeTemplate(
                id="unlikely_cooperation",
                title="Unlikely Cooperation",
                template="{agent_a.name} and {agent_b.name} put aside their differences to achieve a common goal.",
                max_affinity=0,
                emotional_tone="hopeful",
                complexity=2,
                rarity=0.7
            ),

            # Sacrifice narratives
            NarrativeTemplate(
                id="sacrifice_for_comrade",
                title="Sacrifice for Comrade",
                template="{agent_a.name} makes a significant sacrifice to protect {agent_b.name}, deepening their bond.",
                required_bond_type=BondType.COMRADE,
                min_affinity=20,
                emotional_tone="heroic",
                complexity=4,
                rarity=0.3
            ),

            # Daily life narratives
            NarrativeTemplate(
                id="shared_moment_of_normalcy",
                title="Shared Moment of Normalcy",
                template="{agent_a.name} and {agent_b.name} share a rare moment of normalcy, reminding them of life before the resistance.",
                min_affinity=10,
                emotional_tone="nostalgic",
                complexity=1,
                rarity=0.9
            ),

            NarrativeTemplate(
                id="stress_relief_together",
                title="Stress Relief Together",
                template="{agent_a.name} and {agent_b.name} find ways to relieve stress together, strengthening their friendship.",
                required_bond_type=BondType.FRIEND,
                min_affinity=15,
                emotional_tone="relaxed",
                complexity=1,
                rarity=0.8
            ),

            # Professional narratives
            NarrativeTemplate(
                id="professional_respect_grows",
                title="Professional Respect Grows",
                template="{agent_a.name} gains new respect for {agent_b.name}'s skills and dedication to the cause.",
                min_affinity=5,
                emotional_tone="respectful",
                complexity=1,
                rarity=0.8
            ),
        ]

        return templates

    def apply_relationship_effects(self, agent_a: Agent, agent_b: Agent, event_context: Dict[str, Any]) -> str:
        """Apply relationship effects and generate narrative"""
        from .relationships import EventType

        # Determine event type from context
        event_type = self._determine_event_type(event_context)

        # Apply relationship updates
        if event_type:
            self.game_state.update_relationship(
                agent_a.id, agent_b.id, event_type=event_type
            )

        # Generate narrative
        narrative = self._generate_relationship_narrative(agent_a, agent_b, event_context)

        # Integrate with SYLVA/WREN if available
        if self.sylva_enabled or self.wren_enabled:
            narrative = self._enhance_with_sylva_wren(narrative, agent_a, agent_b, event_context)

        return narrative

    def _determine_event_type(self, context: Dict[str, Any]) -> Optional[EventType]:
        """Determine event type from context"""
        context_type = context.get('type', '').lower()

        event_mapping = {
            'shared_risk': EventType.SHARED_RISK,
            'abandonment': EventType.ABANDONMENT,
            'betrayal': EventType.BETRAYAL,
            'rescue': EventType.RESCUE,
            'mentorship': EventType.MENTORSHIP,
            'conflict': EventType.CONFLICT,
            'sacrifice': EventType.SACRIFICE,
            'cooperation': EventType.COOPERATION,
            'competition': EventType.COMPETITION,
            'loyalty_test': EventType.LOYALTY_TEST
        }

        return event_mapping.get(context_type)

    def _generate_relationship_narrative(self, agent_a: Agent, agent_b: Agent,
                                       context: Dict[str, Any]) -> str:
        """Generate narrative for relationship interaction"""

        # Get relationship between agents
        relationship = self.game_state.social_network.get_relationship(agent_a.id, agent_b.id)

        if not relationship:
            # Create basic narrative for agents without relationship
            return f"{agent_a.name} and {agent_b.name} interact for the first time."

        # Find appropriate template
        template = self._find_matching_template(agent_a, agent_b, relationship, context)

        if template:
            # Apply template
            narrative = template.template.format(
                agent_a=agent_a,
                agent_b=agent_b,
                relationship=relationship,
                context=context
            )

            # Track usage
            self._track_template_usage(template.id)

            return narrative
        else:
            # Fallback narrative
            return self._generate_fallback_narrative(agent_a, agent_b, relationship, context)

    def _find_matching_template(self, agent_a: Agent, agent_b: Agent,
                               relationship: Relationship, context: Dict[str, Any]) -> Optional[NarrativeTemplate]:
        """Find a template that matches the current situation"""

        # Filter templates by basic criteria
        candidates = []

        for template in self.templates:
            # Skip recently used templates
            if template.id in self.recently_used:
                continue

            # Check bond type requirement
            if template.required_bond_type and relationship.bond_type != template.required_bond_type:
                continue

            # Check affinity requirements
            if template.min_affinity is not None and relationship.affinity < template.min_affinity:
                continue
            if template.max_affinity is not None and relationship.affinity > template.max_affinity:
                continue

            # Check trust requirements
            if template.min_trust is not None and relationship.trust < template.min_trust:
                continue
            if template.max_trust is not None and relationship.trust > template.max_trust:
                continue

            # Check loyalty requirements
            if template.min_loyalty is not None and relationship.loyalty < template.min_loyalty:
                continue
            if template.max_loyalty is not None and relationship.loyalty > template.max_loyalty:
                continue

            # Check tag requirements
            if template.required_tags:
                agent_tags = agent_a.social_tags.union(agent_b.social_tags)
                if not any(tag in agent_tags for tag in template.required_tags):
                    continue

            if template.excluded_tags:
                agent_tags = agent_a.social_tags.union(agent_b.social_tags)
                if any(tag in agent_tags for tag in template.excluded_tags):
                    continue

            candidates.append(template)

        if not candidates:
            return None

        # Weight by rarity and complexity
        weighted_candidates = []
        for template in candidates:
            weight = template.rarity * (6 - template.complexity)  # Higher complexity = lower weight
            weighted_candidates.extend([template] * int(weight * 10))

        if weighted_candidates:
            return random.choice(weighted_candidates)

        return None

    def _generate_fallback_narrative(self, agent_a: Agent, agent_b: Agent,
                                   relationship: Relationship, context: Dict[str, Any]) -> str:
        """Generate fallback narrative when no template matches"""

        # Simple narratives based on relationship type
        fallback_narratives = {
            BondType.ALLY: f"{agent_a.name} and {agent_b.name} work together as allies.",
            BondType.RIVAL: f"{agent_a.name} and {agent_b.name} continue their rivalry.",
            BondType.MENTOR: f"{agent_a.name} provides guidance to {agent_b.name}.",
            BondType.STUDENT: f"{agent_b.name} learns from {agent_a.name}.",
            BondType.FRIEND: f"{agent_a.name} and {agent_b.name} spend time together as friends.",
            BondType.ENEMY: f"{agent_a.name} and {agent_b.name} maintain their enmity.",
            BondType.FAMILY: f"{agent_a.name} and {agent_b.name} support each other as family.",
            BondType.COMRADE: f"{agent_a.name} and {agent_b.name} fight together as comrades.",
            BondType.TRAITOR: f"{agent_a.name} and {agent_b.name} deal with betrayal.",
            BondType.NEUTRAL: f"{agent_a.name} and {agent_b.name} interact neutrally."
        }

        return fallback_narratives.get(relationship.bond_type,
                                     f"{agent_a.name} and {agent_b.name} interact.")

    def _track_template_usage(self, template_id: str):
        """Track recently used templates to avoid repetition"""
        self.recently_used.append(template_id)

        if len(self.recently_used) > self.max_recent:
            self.recently_used = self.recently_used[-self.max_recent:]

    def _enhance_with_sylva_wren(self, base_narrative: str, agent_a: Agent, agent_b: Agent,
                                context: Dict[str, Any]) -> str:
        """Enhance narrative with SYLVA/WREN integration"""

        # Prepare data for SYLVA/WREN
        relationship = self.game_state.social_network.get_relationship(agent_a.id, agent_b.id)

        sylva_data = {
            "agent_a": {
                "name": agent_a.name,
                "background": agent_a.background,
                "faction": agent_a.faction_id,
                "emotional_state": agent_a.emotional_state.serialize(),
                "social_tags": list(agent_a.social_tags)
            },
            "agent_b": {
                "name": agent_b.name,
                "background": agent_b.background,
                "faction": agent_b.faction_id,
                "emotional_state": agent_b.emotional_state.serialize(),
                "social_tags": list(agent_b.social_tags)
            },
            "relationship_context": relationship.as_dict() if relationship else {},
            "event_context": context,
            "base_narrative": base_narrative
        }

        # SYLVA integration (placeholder)
        if self.sylva_enabled:
            sylva_enhancement = self._call_sylva_api(sylva_data)
            if sylva_enhancement:
                base_narrative += f" {sylva_enhancement}"

        # WREN integration (placeholder)
        if self.wren_enabled:
            wren_enhancement = self._call_wren_api(sylva_data)
            if wren_enhancement:
                base_narrative += f" {wren_enhancement}"

        return base_narrative

    def _call_sylva_api(self, data: Dict[str, Any]) -> Optional[str]:
        """Call SYLVA API for emotional analysis (placeholder)"""
        # This would integrate with the actual SYLVA API
        # For now, return None to indicate no enhancement
        return None

    def _call_wren_api(self, data: Dict[str, Any]) -> Optional[str]:
        """Call WREN API for narrative enhancement (placeholder)"""
        # This would integrate with the actual WREN API
        # For now, return None to indicate no enhancement
        return None

    def generate_relationship_templates(self, bond_type: Optional[BondType] = None,
                                      emotional_tone: Optional[str] = None) -> List[NarrativeTemplate]:
        """Generate relationship-based narrative templates"""
        templates = []

        for template in self.templates:
            if bond_type and template.required_bond_type != bond_type:
                continue
            if emotional_tone and template.emotional_tone != emotional_tone:
                continue

            templates.append(template)

        return templates

    def add_custom_template(self, template: NarrativeTemplate):
        """Add a custom narrative template"""
        self.templates.append(template)

    def get_template_statistics(self) -> Dict[str, Any]:
        """Get statistics about template usage"""
        return {
            "total_templates": len(self.templates),
            "recently_used": len(self.recently_used),
            "templates_by_complexity": self._count_by_complexity(),
            "templates_by_emotional_tone": self._count_by_emotional_tone(),
            "templates_by_bond_type": self._count_by_bond_type()
        }

    def _count_by_complexity(self) -> Dict[int, int]:
        """Count templates by complexity level"""
        counts = {}
        for template in self.templates:
            counts[template.complexity] = counts.get(template.complexity, 0) + 1
        return counts

    def _count_by_emotional_tone(self) -> Dict[str, int]:
        """Count templates by emotional tone"""
        counts = {}
        for template in self.templates:
            counts[template.emotional_tone] = counts.get(template.emotional_tone, 0) + 1
        return counts

    def _count_by_bond_type(self) -> Dict[str, int]:
        """Count templates by required bond type"""
        counts = {}
        for template in self.templates:
            bond_type = template.required_bond_type.value if template.required_bond_type else "any"
            counts[bond_type] = counts.get(bond_type, 0) + 1
        return counts

    def generate_advanced_narrative(self, agent_a: Agent, agent_b: Agent,
                                  context: Dict[str, Any] = None) -> str:
        """Generate narrative using advanced relationship mechanics"""
        if context is None:
            context = {}

        # Check for advanced relationship conditions
        template = self._find_advanced_template(agent_a, agent_b, context)

        if template:
            return self._fill_advanced_template(template, agent_a, agent_b, context)

        # Fallback to regular narrative generation
        return self._generate_relationship_narrative(agent_a, agent_b, context)

    def _find_advanced_template(self, agent_a: Agent, agent_b: Agent,
                              context: Dict[str, Any]) -> Optional[NarrativeTemplate]:
        """Find template matching advanced relationship conditions"""
        relationship = agent_a.get_relationship(agent_b.id)
        if not relationship:
            return None

        # Filter templates by advanced requirements
        candidates = []

        for template in self.templates:
            if template.id in self.recently_used:
                continue

            # Check basic requirements
            if not self._check_basic_requirements(template, agent_a, agent_b, relationship):
                continue

            # Check advanced requirements
            if template.requires_secret and not self._check_secret_requirement(template, agent_a, agent_b):
                continue

            if template.requires_memory and not self._check_memory_requirement(template, agent_a, agent_b):
                continue

            if template.requires_persona and not self._check_persona_requirement(agent_a, agent_b):
                continue

            if template.requires_ideology_conflict and not self._check_ideology_conflict(agent_a, agent_b):
                continue

            candidates.append(template)

        if not candidates:
            return None

        # Weight by rarity and complexity
        weighted_candidates = []
        for template in candidates:
            weight = template.rarity * (6 - template.complexity)  # Higher complexity = lower weight
            weighted_candidates.extend([template] * int(weight * 10))

        if not weighted_candidates:
            return random.choice(candidates)

        return random.choice(weighted_candidates)

    def _check_secret_requirement(self, template: NarrativeTemplate, agent_a: Agent, agent_b: Agent) -> bool:
        """Check if secret requirement is met"""
        # Check if either agent has secrets
        secrets_a = [s for s in agent_a.secrets if not template.secret_type or s.secret_type == template.secret_type]
        secrets_b = [s for s in agent_b.secrets if not template.secret_type or s.secret_type == template.secret_type]

        return len(secrets_a) > 0 or len(secrets_b) > 0

    def _check_memory_requirement(self, template: NarrativeTemplate, agent_a: Agent, agent_b: Agent) -> bool:
        """Check if memory requirement is met"""
        memories_a = agent_a.get_memories_by_agent(agent_b.id)
        memories_b = agent_b.get_memories_by_agent(agent_a.id)

        if template.memory_tone:
            memories_a = [m for m in memories_a if m.emotional_tone == template.memory_tone]
            memories_b = [m for m in memories_b if m.emotional_tone == template.memory_tone]

        return len(memories_a) > 0 or len(memories_b) > 0

    def _check_persona_requirement(self, agent_a: Agent, agent_b: Agent) -> bool:
        """Check if persona mask requirement is met"""
        return agent_a.persona_active or agent_b.persona_active

    def _check_ideology_conflict(self, agent_a: Agent, agent_b: Agent) -> bool:
        """Check if ideological conflict requirement is met"""
        if not hasattr(agent_a, 'ideology_vector') or not hasattr(agent_b, 'ideology_vector'):
            return False

        # Calculate ideological distance
        total_distance = 0.0
        for ideology in agent_a.ideology_vector:
            if ideology in agent_b.ideology_vector:
                distance = abs(agent_a.ideology_vector[ideology] - agent_b.ideology_vector[ideology])
                total_distance += distance

        avg_distance = total_distance / len(agent_a.ideology_vector)
        return avg_distance > 0.3  # Significant ideological difference

    def _fill_advanced_template(self, template: NarrativeTemplate, agent_a: Agent, agent_b: Agent,
                              context: Dict[str, Any]) -> str:
        """Fill an advanced template with dynamic content"""
        narrative = template.template

        # Basic substitutions
        narrative = narrative.replace("{agent_a.name}", agent_a.name)
        narrative = narrative.replace("{agent_b.name}", agent_b.name)

        # Advanced substitutions
        if "{secret_description}" in narrative:
            secret = self._get_relevant_secret(agent_a, agent_b, template.secret_type)
            if secret:
                narrative = narrative.replace("{secret_description}", secret.description)

        if "{memory_summary}" in narrative:
            memory = self._get_relevant_memory(agent_a, agent_b, template.memory_tone)
            if memory:
                narrative = narrative.replace("{memory_summary}", memory.summary)

        if "{ideology_a}" in narrative and "{ideology_b}" in narrative:
            ideology_a, _ = agent_a.get_dominant_ideology()
            ideology_b, _ = agent_b.get_dominant_ideology()
            narrative = narrative.replace("{ideology_a}", ideology_a)
            narrative = narrative.replace("{ideology_b}", ideology_b)

        if "{dominant_ideology}" in narrative:
            ideology, _ = agent_b.get_dominant_ideology()
            narrative = narrative.replace("{dominant_ideology}", ideology)

        if "{dominant_emotion_a}" in narrative and "{dominant_emotion_b}" in narrative:
            emotion_a, _ = agent_a.get_dominant_emotion()
            emotion_b, _ = agent_b.get_dominant_emotion()
            narrative = narrative.replace("{dominant_emotion_a}", emotion_a)
            narrative = narrative.replace("{dominant_emotion_b}", emotion_b)

        if "{defector_names}" in narrative:
            # Get faction defectors
            faction_id = agent_a.faction_id
            defectors = [a.name for a in self.game_state.agents.values()
                        if a.faction_id == faction_id and "defector" in a.social_tags]
            if defectors:
                narrative = narrative.replace("{defector_names}", ", ".join(defectors[:3]))
            else:
                narrative = narrative.replace("{defector_names}", "several members")

        # Track usage
        self._track_template_usage(template.id)

        return narrative

    def _get_relevant_secret(self, agent_a: Agent, agent_b: Agent, secret_type: Optional[SecretType]) -> Optional[Secret]:
        """Get a relevant secret for narrative generation"""
        secrets_a = [s for s in agent_a.secrets if not secret_type or s.secret_type == secret_type]
        secrets_b = [s for s in agent_b.secrets if not secret_type or s.secret_type == secret_type]

        all_secrets = secrets_a + secrets_b
        if not all_secrets:
            return None

        # Prefer weaponized secrets for dramatic effect
        weaponized = [s for s in all_secrets if s.weaponized]
        if weaponized:
            return random.choice(weaponized)

        return random.choice(all_secrets)

    def _get_relevant_memory(self, agent_a: Agent, agent_b: Agent, memory_tone: Optional[str]) -> Optional[MemoryEntry]:
        """Get a relevant memory for narrative generation"""
        memories_a = agent_a.get_memories_by_agent(agent_b.id)
        memories_b = agent_b.get_memories_by_agent(agent_a.id)

        if memory_tone:
            memories_a = [m for m in memories_a if m.emotional_tone == memory_tone]
            memories_b = [m for m in memories_b if m.emotional_tone == memory_tone]

        all_memories = memories_a + memories_b
        if not all_memories:
            return None

        # Prefer recent memories
        recent_memories = [m for m in all_memories if m.get_age(self.game_state.turn_number) <= 5]
        if recent_memories:
            return random.choice(recent_memories)

        return random.choice(all_memories)

    def register_character_voice(self, character_id: str, voice_config: VoiceConfiguration):
        """Register a character's voice configuration with the tone engine"""
        self.tone_engine.register_voice_configuration(voice_config)

    def handle_voice_command(self, character_id: str, command_text: str) -> str:
        """Handle player voice configuration commands"""
        # Parse command
        parts = command_text.split()
        if not parts:
            return self.voice_handler._get_help_text()

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        return self.voice_handler.handle_voice_config_command(character_id, command, args)

    def generate_enhanced_narrative(self, character_id: str, base_event: str,
                                  context: Dict[str, Any] = None) -> str:
        """Generate narrative enhanced with character voice configuration"""
        if context is None:
            context = {}

        # First apply relationship-based narrative generation
        enhanced_narrative = base_event

        # If we have character relationships, enhance with relationship context
        if 'target_character_id' in context:
            target_id = context['target_character_id']
            relationship_narrative = self._generate_relationship_narrative_context(
                character_id, target_id, context
            )
            if relationship_narrative:
                enhanced_narrative = relationship_narrative

        # Apply dynamic tone filtering based on character voice
        tone_enhanced = self.tone_engine.generate_narrative_with_voice(
            character_id, enhanced_narrative, context
        )

        # Apply SYLVA/WREN enhancements if enabled
        if self.sylva_enabled or self.wren_enabled:
            tone_enhanced = self._enhance_with_sylva_wren_extended(
                tone_enhanced, character_id, context
            )

        return tone_enhanced

    def _generate_relationship_narrative_context(self, character_a_id: str,
                                               character_b_id: str,
                                               context: Dict[str, Any]) -> Optional[str]:
        """Generate narrative based on relationship context between characters"""
        if not hasattr(self.game_state, 'social_network'):
            return None

        relationship = self.game_state.social_network.get_relationship(character_a_id, character_b_id)
        if not relationship:
            return None

        # Find appropriate narrative template based on relationship
        template = self._find_relationship_template_for_context(relationship, context)
        if template:
            # Create mock agents for template filling
            agent_a = self._create_agent_proxy(character_a_id)
            agent_b = self._create_agent_proxy(character_b_id)

            if agent_a and agent_b:
                return self._fill_narrative_template(template, agent_a, agent_b, relationship, context)

        return None

    def _create_agent_proxy(self, character_id: str) -> Optional[Any]:
        """Create an agent proxy for narrative generation"""
        # In a full implementation, this would get the actual character/agent
        # For now, create a simple proxy with the character ID
        class AgentProxy:
            def __init__(self, character_id: str):
                self.id = character_id
                self.name = f"Character_{character_id}"

        return AgentProxy(character_id)

    def _find_relationship_template_for_context(self, relationship: Relationship,
                                              context: Dict[str, Any]) -> Optional[Any]:
        """Find a narrative template that matches the relationship and context"""
        # Filter templates based on context
        event_type = context.get('event_type', 'general')
        emotional_context = context.get('emotional_context', 'neutral')

        suitable_templates = []

        for template in self.templates:
            # Check if template matches the relationship type
            if (template.required_bond_type and
                template.required_bond_type != relationship.bond_type):
                continue

            # Check affinity ranges
            if (template.min_affinity and relationship.affinity < template.min_affinity):
                continue
            if (template.max_affinity and relationship.affinity > template.max_affinity):
                continue

            # Check trust ranges
            if (template.min_trust and relationship.trust < template.min_trust):
                continue
            if (template.max_trust and relationship.trust > template.max_trust):
                continue

            # Check emotional tone match
            if emotional_context != 'neutral' and template.emotional_tone != emotional_context:
                continue

            suitable_templates.append(template)

        if suitable_templates:
            # Prefer templates that haven't been used recently
            unused_templates = [t for t in suitable_templates if t.id not in self.recently_used]
            if unused_templates:
                return random.choice(unused_templates)
            else:
                return random.choice(suitable_templates)

        return None

    def _enhance_with_sylva_wren_extended(self, base_narrative: str, character_id: str,
                                        context: Dict[str, Any]) -> str:
        """Extended SYLVA/WREN enhancement that includes voice configuration"""

        # Get character voice configuration
        voice_config = self.tone_engine.get_voice_configuration(character_id)

        # Prepare enhanced data for SYLVA/WREN
        sylva_data = {
            "character_id": character_id,
            "base_narrative": base_narrative,
            "context": context,
            "voice_configuration": voice_config.to_dict() if voice_config else None,
        }

        enhanced_narrative = base_narrative

        # SYLVA integration with voice awareness
        if self.sylva_enabled:
            sylva_enhancement = self._call_sylva_api_extended(sylva_data)
            if sylva_enhancement:
                enhanced_narrative += f" {sylva_enhancement}"

        # WREN integration with voice awareness
        if self.wren_enabled:
            wren_enhancement = self._call_wren_api_extended(sylva_data)
            if wren_enhancement:
                enhanced_narrative += f" {wren_enhancement}"

        return enhanced_narrative

    def _call_sylva_api_extended(self, data: Dict[str, Any]) -> Optional[str]:
        """Extended SYLVA API call that includes voice configuration data"""
        # This would integrate with the actual SYLVA API, sending voice config data
        # For now, simulate some voice-aware emotional analysis

        voice_config = data.get('voice_configuration')
        if voice_config and voice_config.get('emotional_tones'):
            # Simulate SYLVA enhancing based on emotional tones
            dominant_tone = voice_config['emotional_tones'][0] if voice_config['emotional_tones'] else None

            if dominant_tone == 'wry':
                return "The irony wasn't lost on them."
            elif dominant_tone == 'melancholic':
                return "The memory lingered like morning fog."
            elif dominant_tone == 'rebellious':
                return "Defiance burned in their chest."

        return None

    def _call_wren_api_extended(self, data: Dict[str, Any]) -> Optional[str]:
        """Extended WREN API call that includes voice configuration data"""
        # This would integrate with the actual WREN API, sending voice config data
        # For now, simulate some voice-aware narrative enhancement

        voice_config = data.get('voice_configuration')
        if voice_config and voice_config.get('symbolic_preferences'):
            # Simulate WREN adding symbolic elements
            symbols = voice_config['symbolic_preferences']

            if 'cigarettes' in symbols:
                return "Smoke curled upward, carrying unspoken thoughts."
            elif 'coffee' in symbols:
                return "The aroma brought fleeting comfort in uncertain times."
            elif 'broken_glass' in symbols:
                return "Fragments caught the light, beautiful in their destruction."

        return None

    def get_character_voice_summary(self, character_id: str) -> str:
        """Get a summary of a character's voice configuration"""
        voice_config = self.tone_engine.get_voice_configuration(character_id)
        if not voice_config:
            return f"No voice configuration found for character {character_id}"

        return self.voice_handler._format_voice_config(voice_config)

    def export_voice_configurations(self) -> Dict[str, Dict[str, Any]]:
        """Export all voice configurations for save/load"""
        export_data = {}
        for char_id, config in self.tone_engine.voice_configurations.items():
            export_data[char_id] = config.to_dict()
        return export_data

    def import_voice_configurations(self, import_data: Dict[str, Dict[str, Any]]):
        """Import voice configurations from save data"""
        for char_id, config_data in import_data.items():
            config = VoiceConfiguration.from_dict(config_data)
            self.tone_engine.register_voice_configuration(config)