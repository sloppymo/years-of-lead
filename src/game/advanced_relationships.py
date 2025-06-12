"""
Advanced Relationship Mechanics for Years of Lead

This module extends the core relationship system with psychological complexity,
social deception, emotional contagion, factional instability, and ideological drift.
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
import random
import math
from datetime import datetime
from .relationships import Relationship, BondType, EventType, SocialNetwork
from .entities import Agent, GameState


class SecretType(Enum):
    """Types of secrets agents can hold"""
    PERSONAL = "personal"           # Personal vulnerabilities
    OPERATIONAL = "operational"     # Mission details, safe houses
    POLITICAL = "political"         # Faction secrets, betrayals
    CRIMINAL = "criminal"           # Illegal activities
    EMOTIONAL = "emotional"         # Hidden feelings, trauma
    STRATEGIC = "strategic"         # Long-term plans, alliances


class IdeologyType(Enum):
    """Ideological dimensions for agents"""
    RADICAL = "radical"             # Radical vs moderate
    PACIFIST = "pacifist"           # Peaceful vs violent
    INDIVIDUALIST = "individualist" # Individual vs collective
    TRADITIONAL = "traditional"     # Traditional vs progressive
    NATIONALIST = "nationalist"     # National vs international
    MATERIALIST = "materialist"     # Material vs idealistic


@dataclass
class Secret:
    """Represents a secret that an agent holds"""
    id: str
    description: str
    secret_type: SecretType
    impact: float  # trust/loyalty modifier when revealed
    known_by: Set[str] = field(default_factory=set)
    weaponized: bool = False
    created_turn: int = 0
    discovered_turn: Optional[int] = None
    emotional_weight: float = 1.0  # How emotionally charged this secret is

    def can_be_weaponized(self) -> bool:
        """Check if secret can be used for blackmail"""
        return self.impact < -0.2 and not self.weaponized

    def get_blackmail_potential(self) -> float:
        """Calculate blackmail potential"""
        if not self.can_be_weaponized():
            return 0.0
        return abs(self.impact) * self.emotional_weight

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'description': self.description,
            'secret_type': self.secret_type.value,
            'impact': self.impact,
            'known_by': list(self.known_by),
            'weaponized': self.weaponized,
            'created_turn': self.created_turn,
            'discovered_turn': self.discovered_turn,
            'emotional_weight': self.emotional_weight
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Secret':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            description=data['description'],
            secret_type=SecretType(data['secret_type']),
            impact=data['impact'],
            known_by=set(data.get('known_by', [])),
            weaponized=data.get('weaponized', False),
            created_turn=data.get('created_turn', 0),
            discovered_turn=data.get('discovered_turn'),
            emotional_weight=data.get('emotional_weight', 1.0)
        )


@dataclass
class MemoryEntry:
    """Represents a memory entry in an agent's journal"""
    id: str
    summary: str
    emotional_tone: str
    agent_involved: Optional[str] = None
    impact_score: float = 0.0
    created_turn: int = 0
    relationship_context: Optional[Dict[str, Any]] = None
    symbolic_elements: List[str] = field(default_factory=list)

    def get_age(self, current_turn: int) -> int:
        """Get age of memory in turns"""
        return current_turn - self.created_turn

    def get_fading_impact(self, current_turn: int, decay_rate: float = 0.1) -> float:
        """Calculate impact with time-based decay"""
        age = self.get_age(current_turn)
        return self.impact_score * math.exp(-decay_rate * age)

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'summary': self.summary,
            'emotional_tone': self.emotional_tone,
            'agent_involved': self.agent_involved,
            'impact_score': self.impact_score,
            'created_turn': self.created_turn,
            'relationship_context': self.relationship_context,
            'symbolic_elements': self.symbolic_elements
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            summary=data['summary'],
            emotional_tone=data['emotional_tone'],
            agent_involved=data.get('agent_involved'),
            impact_score=data.get('impact_score', 0.0),
            created_turn=data.get('created_turn', 0),
            relationship_context=data.get('relationship_context'),
            symbolic_elements=data.get('symbolic_elements', [])
        )


@dataclass
class BetrayalPlan:
    """Represents a planned betrayal by an agent"""
    target_agent: str
    trigger_conditions: Dict[str, Any]
    preferred_timing: str  # "immediate", "during_mission", "after_success", etc.
    potential_co_conspirators: List[str] = field(default_factory=list)
    plan_confidence: float = 0.5
    created_turn: int = 0
    activation_threshold: float = 0.7

    def should_activate(self, current_conditions: Dict[str, Any]) -> bool:
        """Check if betrayal plan should be activated"""
        # Check if conditions are met
        conditions_met = 0
        total_conditions = len(self.trigger_conditions)

        for condition, value in self.trigger_conditions.items():
            if current_conditions.get(condition, 0) >= value:
                conditions_met += 1

        activation_score = conditions_met / total_conditions
        return activation_score >= self.activation_threshold

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'target_agent': self.target_agent,
            'trigger_conditions': self.trigger_conditions,
            'preferred_timing': self.preferred_timing,
            'potential_co_conspirators': self.potential_co_conspirators,
            'plan_confidence': self.plan_confidence,
            'created_turn': self.created_turn,
            'activation_threshold': self.activation_threshold
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BetrayalPlan':
        """Create from dictionary"""
        return cls(
            target_agent=data['target_agent'],
            trigger_conditions=data['trigger_conditions'],
            preferred_timing=data['preferred_timing'],
            potential_co_conspirators=data.get('potential_co_conspirators', []),
            plan_confidence=data.get('plan_confidence', 0.5),
            created_turn=data.get('created_turn', 0),
            activation_threshold=data.get('activation_threshold', 0.7)
        )


class AdvancedRelationshipManager:
    """Manages advanced relationship mechanics"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.secret_templates = self._initialize_secret_templates()
        self.memory_templates = self._initialize_memory_templates()
        self.emotion_propagation_rate = 0.1
        self.ideology_drift_rate = 0.05
        self.faction_fracture_threshold = 0.3

    def _initialize_secret_templates(self) -> List[Dict[str, Any]]:
        """Initialize secret templates"""
        return [
            {
                "type": SecretType.PERSONAL,
                "templates": [
                    "Has a family member working for the government",
                    "Suffers from severe PTSD from past operations",
                    "Is secretly in love with a rival faction member",
                    "Has a gambling addiction that's causing financial problems",
                    "Was once arrested and has a criminal record"
                ],
                "impact_range": (-0.4, -0.1),
                "emotional_weight_range": (0.7, 1.0)
            },
            {
                "type": SecretType.OPERATIONAL,
                "templates": [
                    "Knows the location of a major weapons cache",
                    "Has access to government intelligence sources",
                    "Knows about an upcoming major operation",
                    "Has compromised a high-ranking government official",
                    "Knows the identity of a deep-cover agent"
                ],
                "impact_range": (-0.6, -0.2),
                "emotional_weight_range": (0.5, 0.8)
            },
            {
                "type": SecretType.POLITICAL,
                "templates": [
                    "Disagrees with faction leadership on key issues",
                    "Has been secretly meeting with rival factions",
                    "Plans to defect to another faction",
                    "Has been spreading dissent among faction members",
                    "Knows about faction corruption or betrayal"
                ],
                "impact_range": (-0.8, -0.3),
                "emotional_weight_range": (0.8, 1.0)
            },
            {
                "type": SecretType.CRIMINAL,
                "templates": [
                    "Has committed murder during a mission",
                    "Has been embezzling funds from the faction",
                    "Is involved in illegal drug trafficking",
                    "Has been running a black market operation",
                    "Has committed war crimes during operations"
                ],
                "impact_range": (-0.9, -0.5),
                "emotional_weight_range": (0.8, 1.0)
            },
            {
                "type": SecretType.EMOTIONAL,
                "templates": [
                    "Is secretly terrified of continuing the fight",
                    "Has lost faith in the cause",
                    "Is experiencing severe depression",
                    "Feels guilty about civilian casualties",
                    "Is questioning their own morality"
                ],
                "impact_range": (-0.3, -0.1),
                "emotional_weight_range": (0.9, 1.0)
            },
            {
                "type": SecretType.STRATEGIC,
                "templates": [
                    "Has knowledge of a planned major government operation",
                    "Knows about a mole in high government positions",
                    "Has intel on enemy faction strategic plans",
                    "Knows the location of a critical government facility",
                    "Has information about upcoming faction alliances"
                ],
                "impact_range": (-0.7, -0.3),
                "emotional_weight_range": (0.6, 0.9)
            }
        ]

    def _initialize_memory_templates(self) -> List[Dict[str, Any]]:
        """Initialize memory entry templates"""
        return [
            {
                "event_type": "rescue",
                "templates": [
                    "{agent_name} saved my life during the {location} operation",
                    "I owe {agent_name} everything after they pulled me from that ambush",
                    "Without {agent_name}, I would have died in that safe house raid"
                ],
                "emotional_tone": "grateful",
                "impact_range": (0.3, 0.6)
            },
            {
                "event_type": "betrayal",
                "templates": [
                    "{agent_name} betrayed us to the authorities",
                    "I can never trust {agent_name} again after what they did",
                    "{agent_name} sold us out for money/power"
                ],
                "emotional_tone": "bitter",
                "impact_range": (-0.6, -0.3)
            },
            {
                "event_type": "loss",
                "templates": [
                    "I watched {agent_name} die in that operation",
                    "We lost {agent_name} because of my mistake",
                    "I couldn't save {agent_name} when they needed me"
                ],
                "emotional_tone": "grieving",
                "impact_range": (-0.5, -0.2)
            },
            {
                "event_type": "victory",
                "templates": [
                    "We achieved something incredible with {agent_name}",
                    "That operation with {agent_name} changed everything",
                    "I'll never forget the look on {agent_name}'s face when we succeeded"
                ],
                "emotional_tone": "proud",
                "impact_range": (0.2, 0.5)
            }
        ]

    def generate_secret_for_agent(self, agent: Agent, secret_type: Optional[SecretType] = None) -> Secret:
        """Generate a secret for an agent"""
        if secret_type is None:
            secret_type = random.choice(list(SecretType))

        # Find appropriate template
        template_group = next(t for t in self.secret_templates if t["type"] == secret_type)
        template = random.choice(template_group["templates"])

        # Generate impact and emotional weight
        impact = random.uniform(*template_group["impact_range"])
        emotional_weight = random.uniform(*template_group["emotional_weight_range"])

        # Create secret
        secret = Secret(
            id=f"secret_{agent.id}_{random.randint(1000, 9999)}",
            description=template,
            secret_type=secret_type,
            impact=impact,
            emotional_weight=emotional_weight,
            created_turn=self.game_state.turn_number
        )

        return secret

    def spread_rumor(self, secret: Secret, source_agent: str, target_agent: str,
                    success_chance: float = 0.3) -> bool:
        """Attempt to spread a rumor about a secret"""
        if random.random() > success_chance:
            return False

        # Add target to known_by set
        secret.known_by.add(target_agent)

        # Generate narrative
        narrative = f"{self.game_state.agents[source_agent].name} spreads a rumor about {secret.description}"
        self.game_state.recent_narrative.append(narrative)

        return True

    def use_blackmail(self, blackmailer: str, target: str, secret: Secret) -> Dict[str, Any]:
        """Use a secret for blackmail"""
        if not secret.can_be_weaponized():
            return {"success": False, "reason": "Secret cannot be weaponized"}

        # Calculate blackmail effectiveness
        effectiveness = secret.get_blackmail_potential()
        resistance = self.game_state.agents[target].loyalty / 100.0

        if random.random() < effectiveness * (1 - resistance):
            # Blackmail successful
            secret.weaponized = True

            # Apply relationship effects
            self.game_state.update_relationship(
                blackmailer, target,
                delta_affinity=-20,
                delta_trust=-0.3,
                event_type=EventType.BETRAYAL
            )

            return {
                "success": True,
                "effectiveness": effectiveness,
                "narrative": f"{self.game_state.agents[blackmailer].name} successfully blackmails {self.game_state.agents[target].name}"
            }
        else:
            # Blackmail failed
            return {
                "success": False,
                "reason": "Target resisted blackmail",
                "narrative": f"{self.game_state.agents[target].name} resists {self.game_state.agents[blackmailer].name}'s blackmail attempt"
            }

    def create_memory_entry(self, agent: Agent, event_type: str, other_agent: Optional[str] = None,
                           custom_summary: Optional[str] = None) -> MemoryEntry:
        """Create a memory entry for an agent"""
        # Find appropriate template
        template_group = next((t for t in self.memory_templates if t["event_type"] == event_type), None)

        if template_group:
            template = random.choice(template_group["templates"])
            emotional_tone = template_group["emotional_tone"]
            impact = random.uniform(*template_group["impact_range"])

            if other_agent:
                other_agent_name = self.game_state.agents[other_agent].name
                summary = template.format(agent_name=other_agent_name)
            else:
                summary = template
        else:
            summary = custom_summary or f"Significant event: {event_type}"
            emotional_tone = "neutral"
            impact = 0.0

        memory = MemoryEntry(
            id=f"memory_{agent.id}_{random.randint(1000, 9999)}",
            summary=summary,
            emotional_tone=emotional_tone,
            agent_involved=other_agent,
            impact_score=impact,
            created_turn=self.game_state.turn_number
        )

        return memory

    def propagate_emotions(self):
        """Propagate emotions through the social network"""
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'emotion_state'):
                agent.emotion_state = {"hope": 0.5, "fear": 0.3, "anger": 0.2, "despair": 0.1}

            # Get social circle
            social_circle = self.game_state.get_social_circle(agent_id)

            for other_id, relationship in social_circle:
                if other_id not in self.game_state.agents:
                    continue

                other_agent = self.game_state.agents[other_id]
                if not hasattr(other_agent, 'emotion_state'):
                    other_agent.emotion_state = {"hope": 0.5, "fear": 0.3, "anger": 0.2, "despair": 0.1}

                # Calculate emotional drift
                influence = relationship.get_strength() * self.emotion_propagation_rate

                for emotion in agent.emotion_state:
                    if emotion in other_agent.emotion_state:
                        drift = (agent.emotion_state[emotion] - other_agent.emotion_state[emotion]) * influence
                        other_agent.emotion_state[emotion] = max(0.0, min(1.0,
                            other_agent.emotion_state[emotion] + drift))

    def check_faction_fractures(self):
        """Check for faction fractures due to low cohesion"""
        for faction_id, faction in list(self.game_state.factions.items()):
            cohesion = self.game_state.get_faction_cohesion(faction_id)

            if cohesion < self.faction_fracture_threshold:
                self._trigger_faction_fracture(faction_id, faction)

    def _trigger_faction_fracture(self, faction_id: str, faction):
        """Trigger a faction fracture event"""
        # Get faction agents
        faction_agents = [a for a in self.game_state.agents.items() if a[1].faction_id == faction_id]

        if len(faction_agents) < 2:
            return

        # Find potential defectors (agents with low loyalty to faction)
        defectors = []
        loyalists = []

        for agent_id, agent in faction_agents:
            # Calculate loyalty to faction based on relationships
            faction_loyalty = self._calculate_faction_loyalty(agent, [a[1] for a in faction_agents])

            if faction_loyalty < 0.4:
                defectors.append(agent)
            else:
                loyalists.append(agent)

        if len(defectors) > 0:
            # Create new faction
            new_faction_id = f"{faction_id}_splinter_{random.randint(1000, 9999)}"
            new_faction_name = f"{faction.name} Splinter Group"

            # Create new faction object
            from .core import Faction
            new_faction = Faction(
                id=new_faction_id,
                name=new_faction_name,
                current_goal="survival",
                resources={"money": faction.resources["money"] // 3,
                          "influence": faction.resources["influence"] // 3,
                          "personnel": len(defectors)}
            )

            # Add to game state
            self.game_state.factions[new_faction_id] = new_faction

            # Migrate defectors
            for agent in defectors:
                agent.faction_id = new_faction_id

                # Update social tags
                agent.social_tags.add("defector")
                agent.social_tags.add("splinter")

            # Generate narrative
            defector_names = [a.name for a in defectors]
            narrative = f"Faction fracture: {', '.join(defector_names)} defect from {faction.name}, forming {new_faction_name}"
            self.game_state.recent_narrative.append(narrative)

    def _calculate_faction_loyalty(self, agent: Agent, faction_agents: List[Agent]) -> float:
        """Calculate an agent's loyalty to their faction"""
        if not faction_agents:
            return 0.0

        total_loyalty = 0.0
        relationship_count = 0

        for other_agent in faction_agents:
            if other_agent.id != agent.id:
                relationship = agent.get_relationship(other_agent.id)
                if relationship:
                    total_loyalty += relationship.loyalty
                    relationship_count += 1

        if relationship_count == 0:
            return agent.loyalty / 100.0  # Fallback to base loyalty

        return total_loyalty / relationship_count

    def update_ideologies(self):
        """Update agent ideologies based on relationships and events"""
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'ideology_vector'):
                agent.ideology_vector = {
                    "radical": 0.5,
                    "pacifist": 0.5,
                    "individualist": 0.5,
                    "traditional": 0.5,
                    "nationalist": 0.5,
                    "materialist": 0.5
                }

            # Get influential agents in social circle
            social_circle = self.game_state.get_social_circle(agent_id)

            for other_id, relationship in social_circle:
                if other_id not in self.game_state.agents:
                    continue

                other_agent = self.game_state.agents[other_id]
                if not hasattr(other_agent, 'ideology_vector'):
                    other_agent.ideology_vector = {
                        "radical": 0.5,
                        "pacifist": 0.5,
                        "individualist": 0.5,
                        "traditional": 0.5,
                        "nationalist": 0.5,
                        "materialist": 0.5
                    }

                # Calculate ideological drift
                if relationship.is_positive():
                    influence = relationship.get_strength() * self.ideology_drift_rate

                    for ideology in agent.ideology_vector:
                        if ideology in other_agent.ideology_vector:
                            drift = (other_agent.ideology_vector[ideology] - agent.ideology_vector[ideology]) * influence
                            agent.ideology_vector[ideology] = max(0.0, min(1.0,
                                agent.ideology_vector[ideology] + drift))

    def check_defection_risk(self, agent: Agent) -> float:
        """Calculate agent's risk of defecting from their faction"""
        if not hasattr(agent, 'ideology_vector'):
            return 0.0

        # Get faction ideology (average of faction members)
        faction_agents = [a for a in self.game_state.agents.values() if a.faction_id == agent.faction_id]

        if len(faction_agents) < 2:
            return 0.0

        faction_ideology = {}
        for ideology in agent.ideology_vector:
            faction_ideology[ideology] = sum(
                a.ideology_vector.get(ideology, 0.5) for a in faction_agents
            ) / len(faction_agents)

        # Calculate ideological distance
        total_distance = 0.0
        for ideology in agent.ideology_vector:
            distance = abs(agent.ideology_vector[ideology] - faction_ideology[ideology])
            total_distance += distance

        avg_distance = total_distance / len(agent.ideology_vector)

        # Factor in relationship strength with faction
        faction_loyalty = self._calculate_faction_loyalty(agent, faction_agents)

        # Calculate defection risk
        defection_risk = avg_distance * (1 - faction_loyalty) * 0.5

        return min(1.0, defection_risk)

    def create_betrayal_plan(self, agent: Agent, target_agent: Agent) -> BetrayalPlan:
        """Create a betrayal plan for an agent"""
        # Define trigger conditions
        trigger_conditions = {
            "low_trust": 0.3,
            "high_stress": 0.7,
            "ideological_distance": 0.6,
            "faction_loyalty": 0.4
        }

        # Find potential co-conspirators
        co_conspirators = []
        social_circle = self.game_state.get_social_circle(agent.id)

        for other_id, relationship in social_circle:
            if relationship.is_negative() or relationship.trust < 0.4:
                co_conspirators.append(other_id)

        plan = BetrayalPlan(
            target_agent=target_agent.id,
            trigger_conditions=trigger_conditions,
            preferred_timing=random.choice(["immediate", "during_mission", "after_success"]),
            potential_co_conspirators=co_conspirators[:3],  # Limit to 3
            plan_confidence=random.uniform(0.3, 0.8),
            created_turn=self.game_state.turn_number
        )

        return plan

    def check_betrayal_activation(self, agent: Agent) -> Optional[Dict[str, Any]]:
        """Check if an agent's betrayal plan should be activated"""
        if not hasattr(agent, 'planned_betrayal') or agent.planned_betrayal is None:
            return None

        plan = agent.planned_betrayal

        # Check current conditions
        current_conditions = {
            "low_trust": 1.0 - agent.get_relationship(plan.target_agent).trust if agent.get_relationship(plan.target_agent) else 0.5,
            "high_stress": agent.stress / 100.0,
            "ideological_distance": self._calculate_ideological_distance(agent, self.game_state.agents[plan.target_agent]),
            "faction_loyalty": self._calculate_faction_loyalty(agent, [a for a in self.game_state.agents.values() if a.faction_id == agent.faction_id])
        }

        if plan.should_activate(current_conditions):
            return {
                "activated": True,
                "plan": plan,
                "conditions": current_conditions,
                "narrative": f"{agent.name} decides to betray {self.game_state.agents[plan.target_agent].name}"
            }

        return None

    def _calculate_ideological_distance(self, agent_a: Agent, agent_b: Agent) -> float:
        """Calculate ideological distance between two agents"""
        if not hasattr(agent_a, 'ideology_vector') or not hasattr(agent_b, 'ideology_vector'):
            return 0.5

        total_distance = 0.0
        for ideology in agent_a.ideology_vector:
            if ideology in agent_b.ideology_vector:
                distance = abs(agent_a.ideology_vector[ideology] - agent_b.ideology_vector[ideology])
                total_distance += distance

        return total_distance / len(agent_a.ideology_vector)

    def process_turn(self):
        """Process all advanced relationship mechanics for a turn"""
        # Propagate emotions
        self.propagate_emotions()

        # Update ideologies
        self.update_ideologies()

        # Check for faction fractures
        self.check_faction_fractures()

        # Check for betrayal activations
        for agent_id, agent in self.game_state.agents.items():
            betrayal_result = self.check_betrayal_activation(agent)
            if betrayal_result and betrayal_result["activated"]:
                self.game_state.recent_narrative.append(betrayal_result["narrative"])

        # Check defection risks
        for agent_id, agent in self.game_state.agents.items():
            defection_risk = self.check_defection_risk(agent)
            if defection_risk > 0.7:
                narrative = f"{agent.name} shows signs of ideological drift from their faction"
                self.game_state.recent_narrative.append(narrative)