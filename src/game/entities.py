"""
Years of Lead - Core Entity Definitions

This module contains the core entity types, enums, and base classes to avoid circular imports.
All shared types that multiple modules depend on are defined here.
"""

from enum import Enum
from typing import Dict, List, Any, Set
from dataclasses import dataclass, field
import random


class GamePhase(Enum):
    """Game turn phases"""

    PLANNING = "planning"
    ACTION = "action"
    RESOLUTION = "resolution"


class AgentStatus(Enum):
    """Agent status types"""

    ACTIVE = "active"
    ON_MISSION = "on_mission"
    INJURED = "injured"
    ARRESTED = "arrested"
    DEAD = "dead"


class SkillType(Enum):
    """Agent skill types"""

    COMBAT = "combat"
    STEALTH = "stealth"
    HACKING = "hacking"
    PERSUASION = "persuasion"
    INTELLIGENCE = "intelligence"
    DEMOLITIONS = "demolitions"


class MissionType(Enum):
    """Mission types"""

    PROPAGANDA = "propaganda"
    SABOTAGE = "sabotage"
    RECRUITMENT = "recruitment"
    INTELLIGENCE = "intelligence"
    FINANCING = "financing"


@dataclass
class Skill:
    """Agent skill with level"""

    level: int = 1
    experience: int = 0


@dataclass
class Equipment:
    """Equipment item"""

    name: str
    type: str
    effectiveness: int = 1


@dataclass
class Agent:
    """Game agent/operative - Base definition without complex dependencies"""

    id: str
    name: str
    faction_id: str
    location_id: str
    status: AgentStatus = AgentStatus.ACTIVE
    background: str = "civilian"
    loyalty: int = 50
    stress: int = 0
    skills: Dict[SkillType, Skill] = field(default_factory=dict)
    equipment: List[Equipment] = field(default_factory=list)

    # These will be populated by the main core module
    emotional_state: Any = None
    relationships: Dict[str, Any] = field(default_factory=dict)
    social_tags: Set[str] = field(default_factory=set)

    # Advanced relationship mechanics
    secrets: List[Any] = field(default_factory=list)
    memory_journal: List[Any] = field(default_factory=list)
    memory_forks: List[Any] = field(
        default_factory=list
    )  # Emotional memory forking system
    masked_relationships: Dict[str, Any] = field(default_factory=dict)
    ideology_vector: Dict[str, float] = field(
        default_factory=lambda: {
            "radical": 0.5,
            "pacifist": 0.5,
            "individualist": 0.5,
            "nationalist": 0.5,
        }
    )

    # Emotional state tracking
    emotion_state: Dict[str, float] = field(
        default_factory=lambda: {
            "hope": 0.5,
            "fear": 0.3,
            "anger": 0.2,
            "despair": 0.1,
            "determination": 0.6,
        }
    )

    # Current turn number (for advanced mechanics)
    _current_turn: int = 1

    def add_secret(self, secret):
        """Add a secret to this agent"""
        self.secrets.append(secret)

    def get_secret_count(self) -> int:
        """Get number of secrets this agent has"""
        return len(self.secrets)
    
    def get_relationship_with(self, other_agent_id: str):
        """Get relationship state with another agent (Phase 2)"""
        # Import here to avoid circular import
        from .relationships import RelationshipState
        
        if other_agent_id not in self.relationships:
            self.relationships[other_agent_id] = RelationshipState()
        
        # Convert dict to RelationshipState if needed
        rel_data = self.relationships[other_agent_id]
        if isinstance(rel_data, dict):
            self.relationships[other_agent_id] = RelationshipState.from_dict(rel_data)
        elif not hasattr(rel_data, 'trust'):
            # Create new RelationshipState if the data isn't properly structured
            self.relationships[other_agent_id] = RelationshipState()
            
        return self.relationships[other_agent_id]

    def __post_init__(self):
        """Initialize default skills"""
        if not self.skills:
            for skill_type in SkillType:
                self.skills[skill_type] = Skill(level=random.randint(1, 3))


@dataclass
class Faction:
    """Political faction"""

    id: str
    name: str
    current_goal: str = "recruitment"
    resources: Dict[str, int] = field(
        default_factory=lambda: {"money": 100, "influence": 10, "personnel": 5}
    )


@dataclass
class Location:
    """Game location"""

    id: str
    name: str
    security_level: int = 5
    unrest_level: int = 3
    active_events: List[str] = field(default_factory=list)


@dataclass
class Mission:
    """Active mission"""

    id: str
    mission_type: MissionType
    faction_id: str
    target_location_id: str
    name: str = ""  # Name of the mission
    participants: List[str] = field(default_factory=list)
    progress: int = 0


class GameState:
    """Main game state manager - Base definition without complex dependencies"""

    def __init__(self):
        self.turn_number = 1
        self.current_phase = GamePhase.PLANNING
        self.agents: Dict[str, Agent] = {}
        self.factions: Dict[str, Faction] = {}
        self.locations: Dict[str, Location] = {}
        self.missions: Dict[str, Mission] = {}
        self.recent_narrative: List[str] = []

        # These will be populated by the main core module
        self.social_network = None
        self.advanced_relationships = None
