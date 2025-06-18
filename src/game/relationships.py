"""
Dynamic Relationships and Social Network System for Years of Lead

This module provides the core relationship system that enables emergent behaviors
like loyalty, betrayal, friendship, and rivalries between agents.

Phase 2: Enhanced with team compatibility mechanics, relationship-driven mission planning,
and interpersonal dynamics that transform gameplay strategy.
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple, TYPE_CHECKING
from dataclasses import dataclass, field
import random
from collections import deque

# Import Agent for type hints only to avoid circular imports
if TYPE_CHECKING:
    from .entities import Agent  # noqa: F401


class BondType(Enum):
    """Types of relationships between agents"""

    ALLY = "ally"
    RIVAL = "rival"
    MENTOR = "mentor"
    STUDENT = "student"
    EX_LOVER = "ex-lover"
    FRIEND = "friend"
    ENEMY = "enemy"
    FAMILY = "family"
    COMRADE = "comrade"
    TRAITOR = "traitor"
    NEUTRAL = "neutral"


class EventType(Enum):
    """Types of events that can affect relationships"""

    SHARED_RISK = "shared_risk"
    ABANDONMENT = "abandonment"
    BETRAYAL = "betrayal"
    RESCUE = "rescue"
    MENTORSHIP = "mentorship"
    CONFLICT = "conflict"
    SACRIFICE = "sacrifice"
    COOPERATION = "cooperation"
    COMPETITION = "competition"
    LOYALTY_TEST = "loyalty_test"


@dataclass
class Relationship:
    """Represents a relationship between two agents"""

    agent_id: str
    bond_type: BondType = BondType.NEUTRAL
    affinity: float = 0.0  # -100 to +100
    trust: float = 0.5  # 0.0 to 1.0
    loyalty: float = 0.5  # 0.0 to 1.0
    emotional_history: List[str] = field(default_factory=list)
    last_event: Optional[str] = None
    decay_rate: float = 0.02  # Rate at which relationship decays per turn
    strength: float = 1.0  # Overall relationship strength multiplier

    def __post_init__(self):
        """Initialize relationship with bond-type specific defaults"""
        if self.bond_type == BondType.ALLY:
            self.affinity = random.uniform(20, 60)
            self.trust = random.uniform(0.6, 0.9)
            self.loyalty = random.uniform(0.7, 0.95)
        elif self.bond_type == BondType.RIVAL:
            self.affinity = random.uniform(-60, -20)
            self.trust = random.uniform(0.1, 0.4)
            self.loyalty = random.uniform(0.1, 0.3)
        elif self.bond_type == BondType.MENTOR:
            self.affinity = random.uniform(30, 70)
            self.trust = random.uniform(0.7, 0.95)
            self.loyalty = random.uniform(0.8, 0.98)
        elif self.bond_type == BondType.ENEMY:
            self.affinity = random.uniform(-80, -40)
            self.trust = random.uniform(0.0, 0.2)
            self.loyalty = random.uniform(0.0, 0.1)
        elif self.bond_type == BondType.FAMILY:
            self.affinity = random.uniform(40, 80)
            self.trust = random.uniform(0.8, 0.98)
            self.loyalty = random.uniform(0.9, 0.99)

    def update_from_event(self, event_type: EventType, magnitude: float = 1.0):
        """Update relationship based on an event"""
        event_effects = {
            EventType.SHARED_RISK: {"affinity": 10, "trust": 0.05, "loyalty": 0.03},
            EventType.ABANDONMENT: {"affinity": -30, "trust": -0.15, "loyalty": -0.2},
            EventType.BETRAYAL: {"affinity": -50, "trust": -0.4, "loyalty": -0.5},
            EventType.RESCUE: {"affinity": 25, "trust": 0.1, "loyalty": 0.15},
            EventType.MENTORSHIP: {"affinity": 15, "trust": 0.08, "loyalty": 0.05},
            EventType.CONFLICT: {"affinity": -20, "trust": -0.1, "loyalty": -0.08},
            EventType.SACRIFICE: {"affinity": 40, "trust": 0.2, "loyalty": 0.25},
            EventType.COOPERATION: {"affinity": 8, "trust": 0.04, "loyalty": 0.03},
            EventType.COMPETITION: {"affinity": -15, "trust": -0.05, "loyalty": -0.03},
            EventType.LOYALTY_TEST: {"affinity": 5, "trust": 0.02, "loyalty": 0.03},
        }

        effects = event_effects.get(event_type, {})

        # Apply effects with magnitude scaling
        if "affinity" in effects:
            self.affinity = max(
                -100, min(100, self.affinity + effects["affinity"] * magnitude)
            )
        if "trust" in effects:
            self.trust = max(0.0, min(1.0, self.trust + effects["trust"] * magnitude))
        if "loyalty" in effects:
            self.loyalty = max(
                0.0, min(1.0, self.loyalty + effects["loyalty"] * magnitude)
            )

        # Record the event
        self.last_event = event_type.value
        self.emotional_history.append(f"{event_type.value}: {magnitude:.2f}")

        # Keep only recent history
        if len(self.emotional_history) > 10:
            self.emotional_history = self.emotional_history[-10:]

    def apply_decay(self):
        """Apply natural decay to the relationship"""
        decay_factor = 1.0 - self.decay_rate

        # Decay affinity towards neutral
        if self.affinity > 0:
            self.affinity *= decay_factor
        elif self.affinity < 0:
            self.affinity *= 2.0 - decay_factor  # Decay towards zero

        # Decay trust and loyalty slightly
        self.trust = max(0.1, self.trust * decay_factor)
        self.loyalty = max(0.1, self.loyalty * decay_factor)

    def get_strength(self) -> float:
        """Calculate overall relationship strength"""
        # Normalize affinity to 0-1 scale
        normalized_affinity = (self.affinity + 100) / 200

        # Weighted combination of factors
        strength = (
            normalized_affinity * 0.3 + self.trust * 0.3 + self.loyalty * 0.4
        ) * self.strength

        return max(0.0, min(1.0, strength))

    def is_positive(self) -> bool:
        """Check if this is a positive relationship"""
        return self.affinity > 0 and self.trust > 0.5

    def is_negative(self) -> bool:
        """Check if this is a negative relationship"""
        return self.affinity < 0 or self.trust < 0.3

    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agent_id": self.agent_id,
            "bond_type": self.bond_type.value,
            "affinity": self.affinity,
            "trust": self.trust,
            "loyalty": self.loyalty,
            "emotional_history": self.emotional_history.copy(),
            "last_event": self.last_event,
            "decay_rate": self.decay_rate,
            "strength": self.strength,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Relationship":
        """Create from dictionary"""
        return cls(
            agent_id=data["agent_id"],
            bond_type=BondType(data["bond_type"]),
            affinity=data["affinity"],
            trust=data["trust"],
            loyalty=data["loyalty"],
            emotional_history=data.get("emotional_history", []),
            last_event=data.get("last_event"),
            decay_rate=data.get("decay_rate", 0.02),
            strength=data.get("strength", 1.0),
        )


# Phase 2: Enhanced Relationship State System
@dataclass
class RelationshipState:
    """Phase 2: Core relationship state between two agents"""

    trust: float = 50.0  # 0-100: Belief in competence/reliability
    loyalty: float = 50.0  # 0-100: Commitment to shared cause
    affinity: float = 50.0  # 0-100: Personal bond/friendship
    shared_history: List[str] = field(default_factory=list)  # Mission tags together

    def calculate_mission_synergy(self) -> float:
        """High trust + affinity = combat effectiveness bonus"""
        if self.trust > 75 and self.affinity > 75:
            return 0.25  # 25% bonus
        elif self.trust < 25 or self.affinity < 25:
            return -0.15  # 15% penalty
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize relationship state"""
        return {
            "trust": self.trust,
            "loyalty": self.loyalty,
            "affinity": self.affinity,
            "shared_history": self.shared_history.copy(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RelationshipState":
        """Deserialize relationship state"""
        return cls(
            trust=data.get("trust", 50.0),
            loyalty=data.get("loyalty", 50.0),
            affinity=data.get("affinity", 50.0),
            shared_history=data.get("shared_history", []).copy(),
        )


@dataclass
class TeamDynamics:
    """Phase 2: Team compatibility analysis results"""

    synergy_bonus: float = 0.0
    conflicts: List[str] = field(default_factory=list)
    refusal_risk: List[str] = field(default_factory=list)
    overall_effectiveness: float = 1.0


class SocialNetwork:
    """Manages the social network graph of agent relationships"""

    def __init__(self):
        self.relationships: Dict[
            str, Dict[str, Relationship]
        ] = {}  # agent_id -> {other_id -> relationship}
        self.social_clusters: Dict[str, Set[str]] = {}  # cluster_id -> set of agent_ids
        self.influence_cache: Dict[str, float] = {}  # agent_id -> influence_score

    def add_relationship(self, agent_a: str, agent_b: str, relationship: Relationship):
        """Add or update a relationship between two agents"""
        # Ensure both agents exist in the network
        if agent_a not in self.relationships:
            self.relationships[agent_a] = {}
        if agent_b not in self.relationships:
            self.relationships[agent_b] = {}

        # Add relationship in both directions
        self.relationships[agent_a][agent_b] = relationship

        # Create reverse relationship
        reverse_relationship = Relationship(
            agent_id=agent_a,
            bond_type=relationship.bond_type,
            affinity=relationship.affinity,
            trust=relationship.trust,
            loyalty=relationship.loyalty,
            decay_rate=relationship.decay_rate,
            strength=relationship.strength,
        )
        self.relationships[agent_b][agent_a] = reverse_relationship

        # Clear influence cache
        self.influence_cache.clear()

    def get_relationship(self, agent_a: str, agent_b: str) -> Optional[Relationship]:
        """Get the relationship between two agents"""
        if agent_a in self.relationships and agent_b in self.relationships[agent_a]:
            return self.relationships[agent_a][agent_b]
        return None

    def update_relationship(
        self,
        agent_a: str,
        agent_b: str,
        delta_affinity: float = 0,
        delta_trust: float = 0,
        delta_loyalty: float = 0,
        event_type: Optional[EventType] = None,
    ):
        """Update an existing relationship"""
        relationship = self.get_relationship(agent_a, agent_b)
        if relationship:
            relationship.affinity = max(
                -100, min(100, relationship.affinity + delta_affinity)
            )
            relationship.trust = max(0.0, min(1.0, relationship.trust + delta_trust))
            relationship.loyalty = max(
                0.0, min(1.0, relationship.loyalty + delta_loyalty)
            )

            if event_type:
                relationship.update_from_event(event_type)

            # Update reverse relationship
            reverse_rel = self.get_relationship(agent_b, agent_a)
            if reverse_rel:
                reverse_rel.affinity = relationship.affinity
                reverse_rel.trust = relationship.trust
                reverse_rel.loyalty = relationship.loyalty
                if event_type:
                    reverse_rel.update_from_event(event_type)

            # Clear influence cache
            self.influence_cache.clear()

    def get_social_circle(
        self,
        agent_id: str,
        bond_filter: Optional[BondType] = None,
        min_affinity: Optional[float] = None,
    ) -> List[Tuple[str, Relationship]]:
        """Get agents in an agent's social circle"""
        if agent_id not in self.relationships:
            return []

        circle = []
        for other_id, relationship in self.relationships[agent_id].items():
            # Apply filters
            if bond_filter and relationship.bond_type != bond_filter:
                continue
            if min_affinity is not None and relationship.affinity < min_affinity:
                continue

            circle.append((other_id, relationship))

        # Sort by relationship strength
        circle.sort(key=lambda x: x[1].get_strength(), reverse=True)
        return circle

    def get_most_influential(
        self, agent_id: str, radius: int = 2
    ) -> List[Tuple[str, float]]:
        """Find the most influential agents within a certain radius"""
        if agent_id not in self.influence_cache:
            self._calculate_influence(agent_id)

        # Get all agents within radius
        visited = set()
        queue = deque([(agent_id, 0)])  # (agent_id, distance)
        influential = []

        while queue:
            current_id, distance = queue.popleft()

            if current_id in visited or distance > radius:
                continue

            visited.add(current_id)

            if current_id != agent_id:
                influence = self.influence_cache.get(current_id, 0.0)
                influential.append((current_id, influence))

            # Add neighbors
            if current_id in self.relationships:
                for neighbor_id in self.relationships[current_id]:
                    if neighbor_id not in visited:
                        queue.append((neighbor_id, distance + 1))

        # Sort by influence
        influential.sort(key=lambda x: x[1], reverse=True)
        return influential

    def _calculate_influence(self, agent_id: str):
        """Calculate influence scores for all agents"""
        # Simple influence calculation based on relationship strength and network position
        for agent in self.relationships:
            if agent in self.influence_cache:
                continue

            influence = 0.0
            if agent in self.relationships:
                # Base influence from number of connections
                influence += len(self.relationships[agent]) * 0.1

                # Influence from strong relationships
                for other_id, rel in self.relationships[agent].items():
                    if rel.is_positive():
                        influence += rel.get_strength() * 0.2
                    else:
                        influence -= rel.get_strength() * 0.1

            self.influence_cache[agent] = max(0.0, influence)

    def propagate_morale_effect(
        self,
        source_agent: str,
        morale_change: float,
        max_propagation: int = 3,
        falloff_rate: float = 0.5,
    ):
        """Propagate morale effects through the social network"""
        visited = set()
        queue = deque(
            [(source_agent, morale_change, 0)]
        )  # (agent_id, effect, distance)

        while queue:
            current_id, effect, distance = queue.popleft()

            if current_id in visited or distance >= max_propagation:
                continue

            visited.add(current_id)

            # Apply effect to agent (this would need to be implemented in Agent class)
            # For now, we'll just update relationships

            if current_id in self.relationships:
                for other_id, relationship in self.relationships[current_id].items():
                    if other_id not in visited:
                        # Propagate effect through positive relationships
                        if relationship.is_positive():
                            propagated_effect = effect * (falloff_rate**distance)
                            self.update_relationship(
                                current_id,
                                other_id,
                                delta_affinity=propagated_effect * 0.5,
                                delta_trust=propagated_effect * 0.01,
                            )
                            queue.append((other_id, propagated_effect, distance + 1))

    def decay_all_relationships(self):
        """Apply decay to all relationships"""
        for agent_id, relationships in self.relationships.items():
            for other_id, relationship in relationships.items():
                relationship.apply_decay()

        # Clear influence cache since relationships changed
        self.influence_cache.clear()

    def get_social_clusters(self) -> Dict[str, Set[str]]:
        """Identify social clusters in the network"""
        clusters = {}
        visited = set()
        cluster_id = 0

        for agent_id in self.relationships:
            if agent_id in visited:
                continue

            # Start new cluster
            cluster = set()
            queue = deque([agent_id])

            while queue:
                current_id = queue.popleft()

                if current_id in visited:
                    continue

                visited.add(current_id)
                cluster.add(current_id)

                # Add connected agents with positive relationships
                if current_id in self.relationships:
                    for other_id, relationship in self.relationships[
                        current_id
                    ].items():
                        if other_id not in visited and relationship.is_positive():
                            queue.append(other_id)

            if len(cluster) > 1:  # Only store non-singleton clusters
                clusters[f"cluster_{cluster_id}"] = cluster
                cluster_id += 1

        self.social_clusters = clusters
        return clusters

    def get_faction_cohesion_index(self, faction_agents: List[str]) -> float:
        """Calculate faction cohesion based on internal relationships"""
        if not faction_agents:
            return 0.0

        total_strength = 0.0
        relationship_count = 0

        for agent_a in faction_agents:
            if agent_a not in self.relationships:
                continue

            for agent_b in faction_agents:
                if agent_a != agent_b and agent_b in self.relationships[agent_a]:
                    relationship = self.relationships[agent_a][agent_b]
                    if relationship.is_positive():
                        total_strength += relationship.get_strength()
                        relationship_count += 1

        if relationship_count == 0:
            return 0.0

        return total_strength / relationship_count

    def serialize(self) -> Dict[str, Any]:
        """Serialize the social network"""
        serialized_relationships = {}
        for agent_id, relationships in self.relationships.items():
            serialized_relationships[agent_id] = {
                other_id: rel.as_dict() for other_id, rel in relationships.items()
            }

        return {
            "relationships": serialized_relationships,
            "social_clusters": {k: list(v) for k, v in self.social_clusters.items()},
            "influence_cache": self.influence_cache.copy(),
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "SocialNetwork":
        """Deserialize the social network"""
        network = cls()

        # Restore relationships
        for agent_id, relationships in data.get("relationships", {}).items():
            network.relationships[agent_id] = {}
            for other_id, rel_data in relationships.items():
                network.relationships[agent_id][other_id] = Relationship.from_dict(
                    rel_data
                )

        # Restore social clusters
        for cluster_id, agent_list in data.get("social_clusters", {}).items():
            network.social_clusters[cluster_id] = set(agent_list)

        # Restore influence cache
        network.influence_cache = data.get("influence_cache", {})

        return network


# Phase 2: Team Compatibility System
def evaluate_team_dynamics(agents: List[Agent]) -> TeamDynamics:
    """Calculate how well agents work together"""

    total_synergy = 0.0
    relationship_count = 0
    potential_conflicts = []

    for i, agent_a in enumerate(agents):
        for j, agent_b in enumerate(agents[i + 1 :], i + 1):
            rel_a_to_b = agent_a.get_relationship_with(agent_b.id)
            rel_b_to_a = agent_b.get_relationship_with(agent_a.id)

            # Average their relationship scores
            mutual_trust = (rel_a_to_b.trust + rel_b_to_a.trust) / 2
            mutual_affinity = (rel_a_to_b.affinity + rel_b_to_a.affinity) / 2

            synergy = calculate_pair_synergy(mutual_trust, mutual_affinity)
            total_synergy += synergy
            relationship_count += 1

            # Flag potential conflicts
            if mutual_trust < 30 or mutual_affinity < 20:
                potential_conflicts.append(f"{agent_a.name} distrusts {agent_b.name}")

    avg_synergy = total_synergy / relationship_count if relationship_count > 0 else 0

    return TeamDynamics(
        synergy_bonus=avg_synergy,
        conflicts=potential_conflicts,
        refusal_risk=calculate_refusal_risk(agents),
        overall_effectiveness=1.0 + avg_synergy,
    )


def calculate_pair_synergy(trust: float, affinity: float) -> float:
    """Calculate synergy bonus/penalty between two agents"""
    if trust > 75 and affinity > 75:
        return 0.25  # 25% bonus
    elif trust < 25 or affinity < 25:
        return -0.15  # 15% penalty
    elif trust > 60 and affinity > 60:
        return 0.10  # 10% bonus
    elif trust < 40 or affinity < 40:
        return -0.05  # 5% penalty
    return 0.0


def calculate_refusal_risk(agents: List[Agent]) -> List[str]:
    """Check if any agent might refuse to work with teammates"""
    refusals = []

    for agent in agents:
        for other_agent in agents:
            if agent.id != other_agent.id:
                rel = agent.get_relationship_with(other_agent.id)
                if rel.loyalty < 20:
                    refusals.append(
                        f"{agent.name} may refuse to work with {other_agent.name}"
                    )
                elif rel.trust < 15:
                    refusals.append(
                        f"{agent.name} doesn't trust {other_agent.name} in combat"
                    )

    return refusals


# Phase 2: Relationship Event System
class RelationshipEvent:
    """Events that modify relationships between agents"""

    @classmethod
    def _update_relationship_history(cls, rel, event_type: str, max_events: int = 10):
        """Helper to update relationship history with deduplication"""
        if (
            event_type not in rel.shared_history[-3:]
        ):  # Don't log same event multiple times in a row
            rel.shared_history.append(event_type)
            # Keep history at reasonable length
            if len(rel.shared_history) > max_events:
                rel.shared_history = rel.shared_history[-max_events:]

    @classmethod
    def shared_success(cls, agent_a: "Agent", agent_b: "Agent", mission_type: str):
        """Agents succeed together - builds trust and affinity"""
        rel_a = agent_a.get_relationship_with(agent_b.id)
        rel_b = agent_b.get_relationship_with(agent_a.id)

        trust_gain = 8 if mission_type == "combat" else 5
        affinity_gain = 5

        rel_a.trust = min(100, rel_a.trust + trust_gain)
        rel_a.affinity = min(100, rel_a.affinity + affinity_gain)
        cls._update_relationship_history(rel_a, f"successful_{mission_type}")

        rel_b.trust = min(100, rel_b.trust + trust_gain)
        rel_b.affinity = min(100, rel_b.affinity + affinity_gain)
        cls._update_relationship_history(rel_b, f"successful_{mission_type}")

    @classmethod
    def abandonment_event(cls, abandoner: "Agent", abandoned: "Agent"):
        """One agent leaves another behind - severe relationship damage"""
        rel_abandoned = abandoned.get_relationship_with(abandoner.id)
        rel_abandoner = abandoner.get_relationship_with(abandoned.id)

        rel_abandoned.trust = max(0, rel_abandoned.trust - 40)
        rel_abandoned.affinity = max(0, rel_abandoned.affinity - 25)
        cls._update_relationship_history(rel_abandoned, "abandoned_by")

        # Abandoner feels guilt
        rel_abandoner.trust = max(0, rel_abandoner.trust - 15)
        cls._update_relationship_history(rel_abandoner, "abandoned")

    @classmethod
    def ideological_conflict(cls, agent_a: "Agent", agent_b: "Agent", severity: str):
        """Agents disagree on tactics/morality"""
        rel_a = agent_a.get_relationship_with(agent_b.id)
        rel_b = agent_b.get_relationship_with(agent_a.id)

        loyalty_damage = 20 if severity == "major" else 10

        rel_a.loyalty = max(0, rel_a.loyalty - loyalty_damage)
        rel_b.loyalty = max(0, rel_b.loyalty - loyalty_damage)

        cls._update_relationship_history(rel_a, f"{severity}_ideological_conflict")
        cls._update_relationship_history(rel_b, f"{severity}_ideological_conflict")

    @classmethod
    def mission_failure_blame(cls, blamer: "Agent", blamed: "Agent", mission_type: str):
        """One agent blames another for mission failure"""
        rel_blamer = blamer.get_relationship_with(blamed.id)
        rel_blamed = blamed.get_relationship_with(blamer.id)

        # Blamer loses trust in blamed
        rel_blamer.trust = max(0, rel_blamer.trust - 20)
        rel_blamer.affinity = max(0, rel_blamer.affinity - 10)
        cls._update_relationship_history(
            rel_blamer, f"blamed_for_{mission_type}_failure"
        )

        # Blamed may feel resentment
        rel_blamed.affinity = max(0, rel_blamed.affinity - 15)
        cls._update_relationship_history(rel_blamed, "blamed_by")

    @classmethod
    def heroic_rescue(cls, rescuer: "Agent", rescued: "Agent"):
        """One agent saves another - major relationship boost"""
        rel_rescued = rescued.get_relationship_with(rescuer.id)
        rel_rescuer = rescuer.get_relationship_with(rescued.id)

        # Rescued feels gratitude
        rel_rescued.trust = min(100, rel_rescued.trust + 25)
        rel_rescued.loyalty = min(100, rel_rescued.loyalty + 20)
        rel_rescued.affinity = min(100, rel_rescued.affinity + 30)
        cls._update_relationship_history(rel_rescued, "rescued_by")

        # Rescuer feels protective
        rel_rescuer.loyalty = min(100, rel_rescuer.loyalty + 10)
        rel_rescuer.affinity = min(100, rel_rescuer.affinity + 15)
        cls._update_relationship_history(rel_rescuer, "rescued")

    # ===== ADVANCED RELATIONSHIP EVENTS =====

    @classmethod
    def secret_revealed(
        cls, revealer: "Agent", target: "Agent", secret_gravity: str = "minor"
    ):
        """One agent reveals a secret about another, affecting relationships with all agents"""
        # Relationship between revealer and target
        rel_revealer = revealer.get_relationship_with(target.id)
        rel_target = target.get_relationship_with(revealer.id)

        # Severity of consequences
        gravity = {
            "minor": {"trust": -10, "affinity": -15, "loyalty": -5},
            "major": {"trust": -30, "affinity": -40, "loyalty": -20},
            "career_ending": {"trust": -50, "affinity": -70, "loyalty": -40},
        }.get(secret_gravity, {"trust": -20, "affinity": -25, "loyalty": -10})

        # Update revealer-target relationship
        rel_revealer.trust = max(0, rel_revealer.trust + gravity["trust"])
        rel_revealer.affinity = max(
            0, rel_revealer.affinity + gravity["affinity"] * 0.7
        )  # Less severe for revealer
        rel_target.trust = max(
            0, rel_target.trust + gravity["trust"] * 1.3
        )  # More severe for target
        rel_target.affinity = max(0, rel_target.affinity + gravity["affinity"])
        rel_target.loyalty = max(0, rel_target.loyalty + gravity["loyalty"])

        cls._update_relationship_history(
            rel_revealer, f"revealed_{secret_gravity}_secret"
        )
        cls._update_relationship_history(
            rel_target, f"betrayed_by_{secret_gravity}_revelation"
        )

        return {
            "revelation_severity": secret_gravity,
            "relationship_damage": gravity,
            "narrative": f"{revealer.name} revealed a {secret_gravity} secret about {target.name}",
        }

    @classmethod
    def romantic_entanglement(cls, agent_a: "Agent", agent_b: "Agent", outcome: str):
        """Agents develop romantic feelings - can be positive or negative"""
        rel_a = agent_a.get_relationship_with(agent_b.id)
        rel_b = agent_b.get_relationship_with(agent_a.id)

        if outcome == "mutual":
            rel_a.affinity = min(100, rel_a.affinity + 40)
            rel_b.affinity = min(100, rel_b.affinity + 40)
            rel_a.trust = min(100, rel_a.trust + 20)
            rel_b.trust = min(100, rel_b.trust + 20)
            cls._update_relationship_history(rel_a, "romantic_relationship")
            cls._update_relationship_history(rel_b, "romantic_relationship")
            return "Their relationship blossomed into romance."

        elif outcome == "unrequited":
            # Randomly decide who has unrequited feelings
            if random.random() < 0.5:
                lover, target = agent_a, agent_b
                rel_lover, rel_target = rel_a, rel_b
            else:
                lover, target = agent_b, agent_a
                rel_lover, rel_target = rel_b, rel_a

            rel_lover.affinity = min(100, rel_lover.affinity + 30)
            rel_target.affinity = max(0, rel_target.affinity - 15)
            rel_target.trust = max(0, rel_target.trust - 10)

            cls._update_relationship_history(rel_lover, "unrequited_love")
            cls._update_relationship_history(rel_target, "unwanted_attention")
            return f"{lover.name} developed feelings for {target.name}, but they weren't reciprocated."

    @classmethod
    def power_struggle(
        cls, agent_a: "Agent", agent_b: "Agent", context: str = "mission_leadership"
    ):
        """Agents compete for dominance or leadership"""
        rel_a = agent_a.get_relationship_with(agent_b.id)
        rel_b = agent_b.get_relationship_with(agent_a.id)

        # Determine winner (higher leadership skill wins)
        a_leadership = agent_a.skills.get("leadership", 0)
        b_leadership = agent_b.skills.get("leadership", 0)

        if a_leadership > b_leadership:
            winner, loser = agent_a, agent_b
            rel_winner, rel_loser = rel_a, rel_b
            winner_first = True
        else:
            winner, loser = agent_b, agent_a
            rel_winner, rel_loser = rel_b, rel_a
            winner_first = False

        # Update relationships
        rel_winner.trust = min(100, rel_winner.trust + 5)
        rel_winner.loyalty = min(100, rel_winner.loyalty + 10)
        rel_loser.trust = max(0, rel_loser.trust - 15)
        rel_loser.loyalty = max(0, rel_loser.loyalty - 10)

        cls._update_relationship_history(
            rel_winner, f"prevailed_in_power_struggle_{context}"
        )
        cls._update_relationship_history(rel_loser, f"lost_power_struggle_{context}")

        return {
            "winner": winner.id,
            "loser": loser.id,
            "context": context,
            "narrative": f"{winner.name} asserted dominance over {loser.name} in a tense power struggle over {context}.",
        }

    @classmethod
    def betrayal_of_trust(
        cls, betrayer: "Agent", betrayed: "Agent", severity: str = "moderate"
    ):
        """A significant betrayal that affects the relationship and surrounding social circle"""
        rel_betrayer = betrayer.get_relationship_with(betrayed.id)
        rel_betrayed = betrayed.get_relationship_with(betrayer.id)

        severity_levels = {
            "minor": {"trust": -30, "affinity": -20, "loyalty": -40},
            "moderate": {"trust": -60, "affinity": -50, "loyalty": -70},
            "severe": {"trust": -90, "affinity": -80, "loyalty": -90},
        }

        impact = severity_levels.get(severity, severity_levels["moderate"])

        # Apply relationship changes
        rel_betrayed.trust = max(0, rel_betrayed.trust + impact["trust"])
        rel_betrayed.affinity = max(0, rel_betrayed.affinity + impact["affinity"])
        rel_betrayed.loyalty = max(0, rel_betrayed.loyalty + impact["loyalty"])

        # Betrayer might feel guilt or justification
        rel_betrayer.trust = max(0, rel_betrayer.trust + impact["trust"] * 0.5)
        rel_betrayer.loyalty = max(0, rel_betrayer.loyalty + impact["loyalty"] * 0.7)

        cls._update_relationship_history(rel_betrayer, f"betrayed_{severity}")
        cls._update_relationship_history(rel_betrayed, f"was_betrayed_{severity}")

        # Create a long-term memory of the betrayal
        betrayed.memory_journal.append(
            {
                "event": f"betrayal_by_{betrayer.id}",
                "severity": severity,
                "turns_ago": 0,
                "forgiveness_threshold": random.uniform(
                    0.3, 0.7
                ),  # Random forgiveness threshold
            }
        )

        return {
            "betrayer": betrayer.id,
            "betrayed": betrayed.id,
            "severity": severity,
            "impact": impact,
            "narrative": f"{betrayer.name} committed a {severity} betrayal against {betrayed.name}, shaking their relationship to its core.",
        }


# Phase 2: Relationship-Driven Narrative
def generate_relationship_narrative(mission_result: Dict[str, Any]) -> List[str]:
    """Generate narrative based on agent relationships"""
    agents = mission_result.get("agents", [])
    narratives = []

    if len(agents) == 2:
        agent_a, agent_b = agents
        rel_a = agent_a.get_relationship_with(agent_b.id)
        rel_b = agent_b.get_relationship_with(agent_a.id)

        avg_trust = (rel_a.trust + rel_b.trust) / 2
        avg_affinity = (rel_a.affinity + rel_b.affinity) / 2

        if avg_trust > 80 and avg_affinity > 80:
            narratives.append(
                f"{agent_a.name} and {agent_b.name} move in perfect synchronization."
            )
        elif avg_trust < 30:
            narratives.append(
                f"{agent_a.name} keeps glancing suspiciously at {agent_b.name}."
            )
        elif avg_affinity < 25:
            narratives.append(
                f"Tension crackles between {agent_a.name} and {agent_b.name}."
            )
        elif avg_trust > 60 and avg_affinity > 60:
            narratives.append(
                f"{agent_a.name} and {agent_b.name} work well together as a team."
            )

        # Check shared history for specific narratives
        if "successful_combat" in rel_a.shared_history:
            narratives.append(
                "They've fought side by side before - it shows in their coordination."
            )
        if (
            "abandoned_by" in rel_a.shared_history
            or "abandoned_by" in rel_b.shared_history
        ):
            narratives.append(
                "Old wounds of abandonment still affect their partnership."
            )

    elif len(agents) > 2:
        # Multi-agent team dynamics
        team_dynamics = evaluate_team_dynamics(agents)
        if team_dynamics.synergy_bonus > 0.15:
            narratives.append("The team works together like a well-oiled machine.")
        elif team_dynamics.synergy_bonus < -0.1:
            narratives.append("Internal conflicts hamper the team's effectiveness.")

        if team_dynamics.conflicts:
            narratives.append("Interpersonal tensions simmer beneath the surface.")

    return narratives
