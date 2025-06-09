"""
Years of Lead - Relationship System

This module implements the relationship tracking between agents,
including admiration, fear, ideological drift, loyalty, and betrayal potential.
Integrates with the emotional state system for trauma triggers.
"""

import math
import random
import logging
from typing import Dict, Any, Optional, List, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from .emotional_state import EmotionalState


logger = logging.getLogger(__name__)


class RelationshipType(Enum):
    """Types of relationships between characters"""
    COMRADE = "comrade"           # Fellow cell member
    LEADER = "leader"             # Leadership relationship
    SUBORDINATE = "subordinate"   # Subordinate relationship
    RIVAL = "rival"               # Competitive/rival relationship
    FRIEND = "friend"             # Personal friendship
    ROMANTIC = "romantic"         # Romantic relationship
    FAMILY = "family"             # Family member
    MENTOR = "mentor"             # Mentor relationship
    STUDENT = "student"           # Student relationship
    CONTACT = "contact"           # Professional contact
    ENEMY = "enemy"               # Active enemy


class RelationshipEvent(Enum):
    """Events that can affect relationships"""
    MISSION_SUCCESS = "mission_success"
    MISSION_FAILURE = "mission_failure"
    SAVED_LIFE = "saved_life"
    ABANDONED = "abandoned"
    BETRAYAL = "betrayal"
    SHARED_TRAUMA = "shared_trauma"
    IDEOLOGICAL_DISPUTE = "ideological_dispute"
    PERSONAL_CONFLICT = "personal_conflict"
    ROMANTIC_ADVANCE = "romantic_advance"
    TRUST_BROKEN = "trust_broken"
    SACRIFICE = "sacrifice"
    CONFESSION = "confession"
    ARGUMENT = "argument"
    RECONCILIATION = "reconciliation"
    DEATH_WITNESSED = "death_witnessed"


@dataclass
class RelationshipMetrics:
    """Core metrics tracking relationship dynamics"""
    admiration: float = 0.0        # -1.0 to 1.0: How much they respect/admire
    fear: float = 0.0              # 0.0 to 1.0: How much they fear them
    trust: float = 0.0             # -1.0 to 1.0: Trust level
    ideological_proximity: float = 0.5  # 0.0 to 1.0: How aligned their beliefs are
    loyalty: float = 0.5           # 0.0 to 1.0: Personal loyalty
    
    # Betrayal tracking
    betrayal_potential: float = 0.0  # 0.0 to 1.0: Likelihood of betrayal
    last_betrayal_check: Optional[datetime] = None
    
    # Emotional bonds
    emotional_bond: float = 0.0    # -1.0 to 1.0: Emotional connection
    shared_experiences: int = 0    # Number of significant shared experiences
    
    def __post_init__(self):
        """Ensure all values are within bounds"""
        self._clamp_values()
    
    def _clamp_values(self):
        """Clamp all values to their valid ranges"""
        self.admiration = max(-1.0, min(1.0, self.admiration))
        self.fear = max(0.0, min(1.0, self.fear))
        self.trust = max(-1.0, min(1.0, self.trust))
        self.ideological_proximity = max(0.0, min(1.0, self.ideological_proximity))
        self.loyalty = max(0.0, min(1.0, self.loyalty))
        self.betrayal_potential = max(0.0, min(1.0, self.betrayal_potential))
        self.emotional_bond = max(-1.0, min(1.0, self.emotional_bond))
    
    def calculate_overall_relationship_strength(self) -> float:
        """Calculate overall relationship strength from -1.0 to 1.0"""
        # Positive factors
        positive = (
            self.admiration * 0.3 +
            self.trust * 0.3 +
            self.loyalty * 0.2 +
            self.emotional_bond * 0.2
        )
        
        # Negative factors
        negative = (
            self.fear * 0.4 +
            self.betrayal_potential * 0.3 +
            (1.0 - self.ideological_proximity) * 0.3
        )
        
        return max(-1.0, min(1.0, positive - negative))
    
    def update_betrayal_potential(self, 
                                 character_trauma: float,
                                 external_pressure: float = 0.0) -> float:
        """Update betrayal potential based on various factors"""
        # Base betrayal potential from low trust and loyalty
        base_potential = max(0.0, (1.0 - self.trust) * 0.3 + (1.0 - self.loyalty) * 0.3)
        
        # Fear increases betrayal potential
        fear_factor = self.fear * 0.3
        
        # Ideological differences increase betrayal potential
        ideology_factor = (1.0 - self.ideological_proximity) * 0.2
        
        # Trauma and external pressure
        stress_factor = (character_trauma + external_pressure) * 0.2
        
        # Emotional bonds reduce betrayal potential
        bond_reduction = max(0.0, self.emotional_bond * 0.3)
        
        self.betrayal_potential = max(0.0, min(1.0,
            base_potential + fear_factor + ideology_factor + stress_factor - bond_reduction
        ))
        
        self.last_betrayal_check = datetime.now()
        return self.betrayal_potential


@dataclass
class RelationshipHistory:
    """Tracks the history of a relationship"""
    events: List[Tuple[datetime, RelationshipEvent, Dict[str, Any]]] = field(default_factory=list)
    trust_trajectory: List[Tuple[datetime, float]] = field(default_factory=list)
    loyalty_trajectory: List[Tuple[datetime, float]] = field(default_factory=list)
    conflicts_resolved: int = 0
    conflicts_unresolved: int = 0
    times_saved_by: int = 0
    times_abandoned_by: int = 0
    shared_successes: int = 0
    shared_failures: int = 0
    
    def add_event(self, event: RelationshipEvent, details: Dict[str, Any] = None):
        """Add an event to the relationship history"""
        self.events.append((datetime.now(), event, details or {}))
        
        # Update counters based on event type
        if event == RelationshipEvent.MISSION_SUCCESS:
            self.shared_successes += 1
        elif event == RelationshipEvent.MISSION_FAILURE:
            self.shared_failures += 1
        elif event == RelationshipEvent.SAVED_LIFE:
            self.times_saved_by += 1
        elif event == RelationshipEvent.ABANDONED:
            self.times_abandoned_by += 1
        elif event == RelationshipEvent.RECONCILIATION:
            self.conflicts_resolved += 1
        elif event in [RelationshipEvent.ARGUMENT, RelationshipEvent.PERSONAL_CONFLICT]:
            self.conflicts_unresolved += 1
    
    def track_metric(self, metric_name: str, value: float):
        """Track a metric over time"""
        if metric_name == "trust":
            self.trust_trajectory.append((datetime.now(), value))
        elif metric_name == "loyalty":
            self.loyalty_trajectory.append((datetime.now(), value))
    
    def get_recent_events(self, count: int = 5) -> List[Tuple[datetime, RelationshipEvent, Dict[str, Any]]]:
        """Get the most recent events"""
        return sorted(self.events, key=lambda x: x[0], reverse=True)[:count]
    
    def has_betrayal_history(self) -> bool:
        """Check if there's a history of betrayal"""
        betrayal_events = [RelationshipEvent.BETRAYAL, RelationshipEvent.TRUST_BROKEN, 
                          RelationshipEvent.ABANDONED]
        return any(event[1] in betrayal_events for event in self.events)


@dataclass
class Relationship:
    """Complete relationship between two characters"""
    character_id: str              # ID of the character who owns this relationship
    target_id: str                 # ID of the target character
    relationship_type: RelationshipType
    metrics: RelationshipMetrics
    history: RelationshipHistory
    
    # Modifiers
    dependency_level: float = 0.0  # 0.0 to 1.0: How dependent they are
    power_dynamic: float = 0.0     # -1.0 to 1.0: Power balance (-1 = subordinate, 1 = dominant)
    
    def apply_event(self, event: RelationshipEvent, 
                   intensity: float = 1.0,
                   details: Dict[str, Any] = None) -> Dict[str, float]:
        """Apply a relationship event and return changes"""
        intensity = max(0.0, min(1.0, intensity))
        changes = {}
        
        # Record the event
        self.history.add_event(event, details)
        
        # Apply event-specific changes
        if event == RelationshipEvent.MISSION_SUCCESS:
            changes['trust'] = 0.1 * intensity
            changes['admiration'] = 0.05 * intensity
            changes['loyalty'] = 0.05 * intensity
            self.metrics.shared_experiences += 1
            
        elif event == RelationshipEvent.MISSION_FAILURE:
            changes['trust'] = -0.05 * intensity
            if details and details.get('blame_assigned'):
                changes['admiration'] = -0.1 * intensity
                changes['emotional_bond'] = -0.05 * intensity
            self.metrics.shared_experiences += 1
            
        elif event == RelationshipEvent.SAVED_LIFE:
            changes['trust'] = 0.3 * intensity
            changes['admiration'] = 0.4 * intensity
            changes['loyalty'] = 0.3 * intensity
            changes['emotional_bond'] = 0.2 * intensity
            self.metrics.fear = max(0.0, self.metrics.fear - 0.2)
            self.metrics.shared_experiences += 2
            
        elif event == RelationshipEvent.ABANDONED:
            changes['trust'] = -0.4 * intensity
            changes['loyalty'] = -0.3 * intensity
            changes['emotional_bond'] = -0.2 * intensity
            self.metrics.fear += 0.1 * intensity
            self.metrics.betrayal_potential += 0.2 * intensity
            
        elif event == RelationshipEvent.BETRAYAL:
            changes['trust'] = -0.8 * intensity
            changes['loyalty'] = -0.6 * intensity
            changes['admiration'] = -0.5 * intensity
            changes['emotional_bond'] = -0.4 * intensity
            self.metrics.fear += 0.3 * intensity
            self.metrics.betrayal_potential = min(1.0, self.metrics.betrayal_potential + 0.4)
            
        elif event == RelationshipEvent.SHARED_TRAUMA:
            changes['emotional_bond'] = 0.3 * intensity
            changes['trust'] = 0.1 * intensity
            self.metrics.shared_experiences += 1
            
        elif event == RelationshipEvent.IDEOLOGICAL_DISPUTE:
            changes['ideological_proximity'] = -0.2 * intensity
            changes['admiration'] = -0.1 * intensity
            if self.metrics.ideological_proximity < 0.3:
                changes['loyalty'] = -0.1 * intensity
                
        elif event == RelationshipEvent.ROMANTIC_ADVANCE:
            if details and details.get('accepted'):
                changes['emotional_bond'] = 0.4 * intensity
                changes['trust'] = 0.2 * intensity
                self.relationship_type = RelationshipType.ROMANTIC
            else:
                changes['emotional_bond'] = -0.1 * intensity
                # Awkwardness might temporarily reduce trust
                changes['trust'] = -0.05 * intensity
                
        elif event == RelationshipEvent.SACRIFICE:
            changes['admiration'] = 0.5 * intensity
            changes['loyalty'] = 0.4 * intensity
            changes['emotional_bond'] = 0.3 * intensity
            self.metrics.betrayal_potential = max(0.0, self.metrics.betrayal_potential - 0.3)
            
        # Apply changes
        for metric, change in changes.items():
            if hasattr(self.metrics, metric):
                current_value = getattr(self.metrics, metric)
                new_value = current_value + change
                setattr(self.metrics, metric, new_value)
        
        # Ensure values are clamped
        self.metrics._clamp_values()
        
        # Track important metrics
        self.history.track_metric("trust", self.metrics.trust)
        self.history.track_metric("loyalty", self.metrics.loyalty)
        
        return changes
    
    def apply_time_decay(self, days_passed: float = 1.0):
        """Apply natural relationship decay over time"""
        decay_rate = 0.01 * days_passed
        
        # Relationships naturally drift toward neutral without reinforcement
        if abs(self.metrics.admiration) > 0.2:
            self.metrics.admiration *= (1.0 - decay_rate)
        
        if abs(self.metrics.emotional_bond) > 0.2:
            self.metrics.emotional_bond *= (1.0 - decay_rate)
        
        # Fear naturally decreases over time
        if self.metrics.fear > 0.1:
            self.metrics.fear = max(0.0, self.metrics.fear - decay_rate * 2)
        
        # Betrayal potential slowly decreases if no negative events
        if self.metrics.betrayal_potential > 0.1:
            recent_events = self.history.get_recent_events(3)
            has_negative = any(e[1] in [RelationshipEvent.BETRAYAL, RelationshipEvent.ABANDONED, 
                                       RelationshipEvent.TRUST_BROKEN] for e in recent_events)
            if not has_negative:
                self.metrics.betrayal_potential = max(0.0, self.metrics.betrayal_potential - decay_rate)
        
        self.metrics._clamp_values()
    
    def check_for_betrayal(self, 
                          external_pressure: float = 0.0,
                          character_trauma: float = 0.0) -> Tuple[bool, float, str]:
        """
        Check if betrayal occurs based on current state
        
        Returns:
            Tuple of (betrayal_occurs, probability, reason)
        """
        # Update betrayal potential
        self.metrics.update_betrayal_potential(character_trauma, external_pressure)
        
        # Base betrayal chance
        base_chance = self.metrics.betrayal_potential
        
        # Modifiers
        if self.metrics.fear > 0.7:
            base_chance += 0.2  # High fear increases betrayal
            
        if self.metrics.loyalty > 0.8:
            base_chance *= 0.3  # High loyalty strongly reduces betrayal
            
        if self.history.has_betrayal_history():
            base_chance += 0.15  # Past betrayals make future ones more likely
            
        if self.relationship_type in [RelationshipType.FAMILY, RelationshipType.ROMANTIC]:
            base_chance *= 0.5  # Strong personal bonds reduce betrayal
        
        # Calculate final probability
        betrayal_probability = max(0.0, min(1.0, base_chance))
        
        # Determine if betrayal occurs
        betrayal_occurs = random.random() < betrayal_probability
        
        # Determine reason if betrayal occurs
        reason = ""
        if betrayal_occurs:
            if self.metrics.fear > 0.7:
                reason = "overwhelming fear"
            elif self.metrics.ideological_proximity < 0.3:
                reason = "ideological differences"
            elif external_pressure > 0.7:
                reason = "external pressure"
            elif self.metrics.trust < -0.5:
                reason = "complete loss of trust"
            else:
                reason = "accumulated grievances"
        
        return betrayal_occurs, betrayal_probability, reason
    
    def get_interaction_modifier(self) -> float:
        """Get modifier for social interactions based on relationship"""
        strength = self.metrics.calculate_overall_relationship_strength()
        
        # Adjust based on relationship type
        if self.relationship_type == RelationshipType.LEADER:
            return strength * 1.2  # Leadership relationships have more impact
        elif self.relationship_type == RelationshipType.ROMANTIC:
            return strength * 1.5  # Romantic relationships are very influential
        elif self.relationship_type == RelationshipType.ENEMY:
            return strength * 0.5  # Enemy relationships have less positive influence
        
        return strength
    
    def generate_relationship_summary(self) -> str:
        """Generate a narrative summary of the relationship"""
        strength = self.metrics.calculate_overall_relationship_strength()
        
        if strength > 0.7:
            quality = "very strong"
        elif strength > 0.3:
            quality = "positive"
        elif strength > -0.3:
            quality = "neutral"
        elif strength > -0.7:
            quality = "strained"
        else:
            quality = "hostile"
        
        summary = f"A {quality} {self.relationship_type.value} relationship. "
        
        # Add specific details
        if self.metrics.trust > 0.7:
            summary += "Built on deep trust. "
        elif self.metrics.trust < -0.5:
            summary += "Marked by deep distrust. "
        
        if self.metrics.fear > 0.5:
            summary += "Tinged with fear. "
        
        if self.metrics.betrayal_potential > 0.5:
            summary += "At high risk of betrayal. "
        
        if self.history.times_saved_by > 0:
            summary += f"They have saved each other {self.history.times_saved_by} times. "
        
        return summary
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize relationship to dictionary"""
        return {
            'character_id': self.character_id,
            'target_id': self.target_id,
            'relationship_type': self.relationship_type.value,
            'metrics': {
                'admiration': self.metrics.admiration,
                'fear': self.metrics.fear,
                'trust': self.metrics.trust,
                'ideological_proximity': self.metrics.ideological_proximity,
                'loyalty': self.metrics.loyalty,
                'betrayal_potential': self.metrics.betrayal_potential,
                'emotional_bond': self.metrics.emotional_bond,
                'shared_experiences': self.metrics.shared_experiences
            },
            'history': {
                'events': [(e[0].isoformat(), e[1].value, e[2]) for e in self.history.events],
                'conflicts_resolved': self.history.conflicts_resolved,
                'conflicts_unresolved': self.history.conflicts_unresolved,
                'times_saved_by': self.history.times_saved_by,
                'times_abandoned_by': self.history.times_abandoned_by,
                'shared_successes': self.history.shared_successes,
                'shared_failures': self.history.shared_failures
            },
            'dependency_level': self.dependency_level,
            'power_dynamic': self.power_dynamic
        }


class RelationshipManager:
    """Manages all relationships for a group of characters"""
    
    def __init__(self):
        self.relationships: Dict[str, Dict[str, Relationship]] = {}
        logger.info("RelationshipManager initialized")
    
    def create_relationship(self, 
                          character_id: str,
                          target_id: str,
                          relationship_type: RelationshipType,
                          initial_metrics: Optional[RelationshipMetrics] = None) -> Relationship:
        """Create a new relationship between two characters"""
        if character_id not in self.relationships:
            self.relationships[character_id] = {}
        
        metrics = initial_metrics or RelationshipMetrics()
        history = RelationshipHistory()
        
        relationship = Relationship(
            character_id=character_id,
            target_id=target_id,
            relationship_type=relationship_type,
            metrics=metrics,
            history=history
        )
        
        self.relationships[character_id][target_id] = relationship
        logger.info(f"Created {relationship_type.value} relationship: {character_id} -> {target_id}")
        
        return relationship
    
    def get_relationship(self, character_id: str, target_id: str) -> Optional[Relationship]:
        """Get a specific relationship"""
        if character_id in self.relationships:
            return self.relationships[character_id].get(target_id)
        return None
    
    def get_all_relationships(self, character_id: str) -> Dict[str, Relationship]:
        """Get all relationships for a character"""
        return self.relationships.get(character_id, {})
    
    def apply_group_event(self,
                         participants: List[str],
                         event: RelationshipEvent,
                         intensity: float = 1.0,
                         details: Dict[str, Any] = None):
        """Apply an event to all relationships within a group"""
        for i, char_id in enumerate(participants):
            for j, target_id in enumerate(participants):
                if i != j:  # Don't create self-relationships
                    relationship = self.get_relationship(char_id, target_id)
                    if relationship:
                        relationship.apply_event(event, intensity, details)
                        logger.debug(f"Applied {event.value} to {char_id} -> {target_id}")
    
    def check_group_cohesion(self, group_ids: List[str]) -> Dict[str, Any]:
        """Analyze the cohesion of a group"""
        total_relationships = 0
        total_strength = 0.0
        betrayal_risks = []
        conflicts = 0
        
        for char_id in group_ids:
            for target_id in group_ids:
                if char_id != target_id:
                    relationship = self.get_relationship(char_id, target_id)
                    if relationship:
                        total_relationships += 1
                        strength = relationship.metrics.calculate_overall_relationship_strength()
                        total_strength += strength
                        
                        if relationship.metrics.betrayal_potential > 0.5:
                            betrayal_risks.append((char_id, target_id, relationship.metrics.betrayal_potential))
                        
                        if relationship.history.conflicts_unresolved > relationship.history.conflicts_resolved:
                            conflicts += 1
        
        avg_strength = total_strength / total_relationships if total_relationships > 0 else 0.0
        
        return {
            'average_strength': avg_strength,
            'total_relationships': total_relationships,
            'high_betrayal_risks': betrayal_risks,
            'unresolved_conflicts': conflicts,
            'cohesion_rating': self._calculate_cohesion_rating(avg_strength, len(betrayal_risks), conflicts)
        }
    
    def _calculate_cohesion_rating(self, avg_strength: float, betrayal_risks: int, conflicts: int) -> str:
        """Calculate overall cohesion rating"""
        score = avg_strength * 100
        score -= betrayal_risks * 20
        score -= conflicts * 10
        
        if score > 80:
            return "Excellent"
        elif score > 60:
            return "Good"
        elif score > 40:
            return "Fair"
        elif score > 20:
            return "Poor"
        else:
            return "Critical"
    
    def simulate_time_passage(self, days: float = 1.0):
        """Simulate the passage of time on all relationships"""
        for char_relationships in self.relationships.values():
            for relationship in char_relationships.values():
                relationship.apply_time_decay(days)
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize all relationships"""
        return {
            char_id: {
                target_id: rel.serialize()
                for target_id, rel in relationships.items()
            }
            for char_id, relationships in self.relationships.items()
        }


def create_initial_cell_relationships(cell_members: List[str], 
                                    leader_id: Optional[str] = None) -> RelationshipManager:
    """Create initial relationships for a resistance cell"""
    manager = RelationshipManager()
    
    # Create relationships between all members
    for i, member_id in enumerate(cell_members):
        for j, target_id in enumerate(cell_members):
            if i != j:
                # Determine relationship type
                if leader_id:
                    if member_id == leader_id:
                        rel_type = RelationshipType.LEADER
                    elif target_id == leader_id:
                        rel_type = RelationshipType.SUBORDINATE
                    else:
                        rel_type = RelationshipType.COMRADE
                else:
                    rel_type = RelationshipType.COMRADE
                
                # Create initial metrics with some randomization
                metrics = RelationshipMetrics(
                    admiration=random.uniform(-0.2, 0.3),
                    fear=random.uniform(0.0, 0.2),
                    trust=random.uniform(0.1, 0.4),
                    ideological_proximity=random.uniform(0.6, 0.9),
                    loyalty=random.uniform(0.4, 0.6),
                    emotional_bond=random.uniform(-0.1, 0.2)
                )
                
                manager.create_relationship(member_id, target_id, rel_type, metrics)
    
    return manager