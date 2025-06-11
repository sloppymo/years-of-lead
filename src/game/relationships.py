"""
Dynamic Relationships and Social Network System for Years of Lead

This module provides the core relationship system that enables emergent behaviors
like loyalty, betrayal, friendship, and rivalries between agents.
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
import random
import math
from collections import defaultdict, deque


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
    trust: float = 0.5     # 0.0 to 1.0
    loyalty: float = 0.5   # 0.0 to 1.0
    emotional_history: List[str] = field(default_factory=list)
    last_event: Optional[str] = None
    decay_rate: float = 0.02  # Rate at which relationship decays per turn
    strength: float = 1.0     # Overall relationship strength multiplier

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
            EventType.LOYALTY_TEST: {"affinity": 5, "trust": 0.02, "loyalty": 0.03}
        }

        effects = event_effects.get(event_type, {})

        # Apply effects with magnitude scaling
        if "affinity" in effects:
            self.affinity = max(-100, min(100, self.affinity + effects["affinity"] * magnitude))
        if "trust" in effects:
            self.trust = max(0.0, min(1.0, self.trust + effects["trust"] * magnitude))
        if "loyalty" in effects:
            self.loyalty = max(0.0, min(1.0, self.loyalty + effects["loyalty"] * magnitude))

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
            self.affinity *= (2.0 - decay_factor)  # Decay towards zero

        # Decay trust and loyalty slightly
        self.trust = max(0.1, self.trust * decay_factor)
        self.loyalty = max(0.1, self.loyalty * decay_factor)

    def get_strength(self) -> float:
        """Calculate overall relationship strength"""
        # Normalize affinity to 0-1 scale
        normalized_affinity = (self.affinity + 100) / 200

        # Weighted combination of factors
        strength = (
            normalized_affinity * 0.3 +
            self.trust * 0.3 +
            self.loyalty * 0.4
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
            'agent_id': self.agent_id,
            'bond_type': self.bond_type.value,
            'affinity': self.affinity,
            'trust': self.trust,
            'loyalty': self.loyalty,
            'emotional_history': self.emotional_history.copy(),
            'last_event': self.last_event,
            'decay_rate': self.decay_rate,
            'strength': self.strength
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relationship':
        """Create from dictionary"""
        return cls(
            agent_id=data['agent_id'],
            bond_type=BondType(data['bond_type']),
            affinity=data['affinity'],
            trust=data['trust'],
            loyalty=data['loyalty'],
            emotional_history=data.get('emotional_history', []),
            last_event=data.get('last_event'),
            decay_rate=data.get('decay_rate', 0.02),
            strength=data.get('strength', 1.0)
        )


class SocialNetwork:
    """Manages the social network graph of agent relationships"""

    def __init__(self):
        self.relationships: Dict[str, Dict[str, Relationship]] = {}  # agent_id -> {other_id -> relationship}
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
            strength=relationship.strength
        )
        self.relationships[agent_b][agent_a] = reverse_relationship

        # Clear influence cache
        self.influence_cache.clear()

    def get_relationship(self, agent_a: str, agent_b: str) -> Optional[Relationship]:
        """Get the relationship between two agents"""
        if agent_a in self.relationships and agent_b in self.relationships[agent_a]:
            return self.relationships[agent_a][agent_b]
        return None

    def update_relationship(self, agent_a: str, agent_b: str,
                          delta_affinity: float = 0, delta_trust: float = 0,
                          delta_loyalty: float = 0, event_type: Optional[EventType] = None):
        """Update an existing relationship"""
        relationship = self.get_relationship(agent_a, agent_b)
        if relationship:
            relationship.affinity = max(-100, min(100, relationship.affinity + delta_affinity))
            relationship.trust = max(0.0, min(1.0, relationship.trust + delta_trust))
            relationship.loyalty = max(0.0, min(1.0, relationship.loyalty + delta_loyalty))

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

    def get_social_circle(self, agent_id: str, bond_filter: Optional[BondType] = None,
                         min_affinity: Optional[float] = None) -> List[Tuple[str, Relationship]]:
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

    def get_most_influential(self, agent_id: str, radius: int = 2) -> List[Tuple[str, float]]:
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

    def propagate_morale_effect(self, source_agent: str, morale_change: float,
                               max_propagation: int = 3, falloff_rate: float = 0.5):
        """Propagate morale effects through the social network"""
        visited = set()
        queue = deque([(source_agent, morale_change, 0)])  # (agent_id, effect, distance)

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
                            propagated_effect = effect * (falloff_rate ** distance)
                            self.update_relationship(
                                current_id, other_id,
                                delta_affinity=propagated_effect * 0.5,
                                delta_trust=propagated_effect * 0.01
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
                    for other_id, relationship in self.relationships[current_id].items():
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
            'relationships': serialized_relationships,
            'social_clusters': {k: list(v) for k, v in self.social_clusters.items()},
            'influence_cache': self.influence_cache.copy()
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'SocialNetwork':
        """Deserialize the social network"""
        network = cls()

        # Restore relationships
        for agent_id, relationships in data.get('relationships', {}).items():
            network.relationships[agent_id] = {}
            for other_id, rel_data in relationships.items():
                network.relationships[agent_id][other_id] = Relationship.from_dict(rel_data)

        # Restore social clusters
        for cluster_id, agent_list in data.get('social_clusters', {}).items():
            network.social_clusters[cluster_id] = set(agent_list)

        # Restore influence cache
        network.influence_cache = data.get('influence_cache', {})

        return network