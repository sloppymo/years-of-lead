"""
Years of Lead - Core Game State and Logic

This module provides the main GameState class and core game mechanics
for the Years of Lead insurgency simulator.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
import random
from .entities import (
    GamePhase, AgentStatus, SkillType, MissionType,
    Skill, Equipment, Agent, Faction, Location, Mission, GameState
)
from .emotional_state import EmotionalState
from .relationships import Relationship, BondType, SocialNetwork, EventType
from .advanced_relationships import Secret, MemoryEntry, BetrayalPlan, AdvancedRelationshipManager


# Extend the base Agent class with complex functionality by adding methods
def _initialize_social_tags(self):
    """Initialize social tags based on background and faction"""
    # Background-based tags
    background_tags = {
        "student": {"academic", "young", "idealistic"},
        "veteran": {"experienced", "disciplined", "trauma"},
        "journalist": {"informed", "curious", "networked"},
        "worker": {"labor", "practical", "solidarity"},
        "organizer": {"charismatic", "networked", "influential"},
        "insider": {"connected", "informed", "risky"}
    }

    self.social_tags.update(background_tags.get(self.background, set()))

    # Add faction-based tags
    faction_tags = {
        "resistance": {"military", "organized", "loyal"},
        "urban_liberation": {"urban", "radical", "youth"},
        "underground": {"secretive", "intelligent", "cautious"}
    }

    self.social_tags.update(faction_tags.get(self.faction_id, set()))

def _initialize_ideology(self):
    """Initialize ideology vector based on background and faction"""
    # Background-based ideology adjustments
    background_ideology = {
        "student": {"radical": 0.7, "pacifist": 0.6, "individualist": 0.4},
        "veteran": {"radical": 0.4, "pacifist": 0.3, "traditional": 0.7},
        "journalist": {"individualist": 0.7, "materialist": 0.6},
        "worker": {"materialist": 0.7, "individualist": 0.3},
        "organizer": {"radical": 0.6, "individualist": 0.5},
        "insider": {"traditional": 0.6, "nationalist": 0.5}
    }

    # Apply background adjustments
    if self.background in background_ideology:
        for ideology, value in background_ideology[self.background].items():
            self.ideology_vector[ideology] = value

    # Faction-based ideology adjustments
    faction_ideology = {
        "resistance": {"traditional": 0.7, "nationalist": 0.6},
        "urban_liberation": {"radical": 0.8, "pacifist": 0.3},
        "underground": {"individualist": 0.6, "materialist": 0.5}
    }

    if self.faction_id in faction_ideology:
        for ideology, value in faction_ideology[self.faction_id].items():
            self.ideology_vector[ideology] = value

def agent_post_init(self):
    """Initialize agent after creation"""
    # Set up proper type annotations for complex fields
    if self.emotional_state is None:
        self.emotional_state = EmotionalState()
    if not self.relationships:
        self.relationships = {}
    if not self.social_tags:
        self.social_tags = set()
    if not self.secrets:
        self.secrets = []
    if not self.memory_journal:
        self.memory_journal = []
    if not self.masked_relationships:
        self.masked_relationships = {}

    # Initialize default skills if not present
    if not self.skills:
        for skill_type in SkillType:
            self.skills[skill_type] = Skill(level=random.randint(1, 3))

    # Initialize social tags and ideology
    self._initialize_social_tags()
    self._initialize_ideology()

def add_secret(self, secret: Secret):
    """Add a secret to the agent"""
    self.secrets.append(secret)

def get_secret(self, secret_id: str) -> Optional[Secret]:
    """Get a specific secret by ID"""
    for secret in self.secrets:
        if secret.id == secret_id:
            return secret
    return None

def remove_secret(self, secret_id: str) -> bool:
    """Remove a secret from the agent"""
    for i, secret in enumerate(self.secrets):
        if secret.id == secret_id:
            del self.secrets[i]
            return True
    return False

def add_memory(self, memory: MemoryEntry):
    """Add a memory entry to the journal"""
    self.memory_journal.append(memory)

    # Keep only recent memories (last 20)
    if len(self.memory_journal) > 20:
        self.memory_journal = self.memory_journal[-20:]

def get_recent_memories(self, turns_back: int = 5) -> List[MemoryEntry]:
    """Get memories from the last N turns"""
    current_turn = getattr(self, '_current_turn', 0)
    return [m for m in self.memory_journal if m.get_age(current_turn) <= turns_back]

def get_memories_by_agent(self, agent_id: str) -> List[MemoryEntry]:
    """Get all memories involving a specific agent"""
    return [m for m in self.memory_journal if m.agent_involved == agent_id]

def set_persona_mask(self, target_agent_id: str, masked_relationship: Relationship):
    """Set a persona mask for a specific relationship"""
    self.masked_relationships[target_agent_id] = masked_relationship
    self.persona_active = True

def remove_persona_mask(self, target_agent_id: str):
    """Remove persona mask for a specific relationship"""
    if target_agent_id in self.masked_relationships:
        del self.masked_relationships[target_agent_id]

    # Check if any masks remain
    if not self.masked_relationships:
        self.persona_active = False

def get_displayed_relationship(self, other_agent_id: str) -> Relationship:
    """Get the relationship as it appears to others (with persona mask if active)"""
    if self.persona_active and other_agent_id in self.masked_relationships:
        return self.masked_relationships[other_agent_id]
    return self.relationships.get(other_agent_id, Relationship())

def can_detect_mask(self, other_agent_id: str, empathy_skill: float = 0.5) -> bool:
    """Check if this agent can detect another agent's persona mask"""
    # Base chance on empathy skill and relationship strength
    relationship = self.relationships.get(other_agent_id)
    if not relationship:
        return False

    # Higher empathy and stronger relationships make detection more likely
    detection_chance = empathy_skill * relationship.get_strength()
    return random.random() < detection_chance

def update_ideology(self, ideology: str, delta: float):
    """Update an ideological value"""
    if ideology in self.ideology_vector:
        self.ideology_vector[ideology] = max(0.0, min(1.0,
            self.ideology_vector[ideology] + delta))

def get_dominant_ideology(self) -> Tuple[str, float]:
    """Get the agent's most strongly held ideology"""
    if not self.ideology_vector:
        return ("neutral", 0.5)

    dominant = max(self.ideology_vector.items(), key=lambda x: x[1])
    return dominant

def update_emotion(self, emotion: str, delta: float):
    """Update an emotional state value"""
    if emotion in self.emotion_state:
        self.emotion_state[emotion] = max(0.0, min(1.0,
            self.emotion_state[emotion] + delta))

def get_dominant_emotion(self) -> Tuple[str, float]:
    """Get the agent's most dominant emotion"""
    if not self.emotion_state:
        return ("neutral", 0.5)

    dominant = max(self.emotion_state.items(), key=lambda x: x[1])
    return dominant

def plan_betrayal(self, target_agent_id: str, trigger_conditions: Dict[str, Any],
                 preferred_timing: str = "immediate") -> BetrayalPlan:
    """Create a betrayal plan"""
    plan = BetrayalPlan(
        target_agent=target_agent_id,
        trigger_conditions=trigger_conditions,
        preferred_timing=preferred_timing,
        created_turn=getattr(self, '_current_turn', 0)
    )
    self.planned_betrayal = plan
    return plan

def cancel_betrayal_plan(self):
    """Cancel the current betrayal plan"""
    self.planned_betrayal = None

def update_emotional_state(self):
    """Update the agent's emotional state through natural drift"""
    self.emotional_state.apply_drift(time_delta=1.0)

def process_event(self, event: Dict[str, Any]):
    """Process an event and apply its emotional impact"""
    if 'emotional_impact' in event:
        self.emotional_state.apply_emotional_impact(event['emotional_impact'])

    if 'type' in event and event.get('severity', 0) > 0:
        self.emotional_state.apply_trauma(event['severity'], event['type'])

def is_state_valid(self) -> bool:
    """Check if the agent's state is valid"""
    return (
        self.status in AgentStatus and
        self.loyalty >= 0 and self.loyalty <= 100 and
        self.stress >= 0 and self.stress <= 100 and
        self.emotional_state.is_psychologically_stable()
    )

def interact_with(self, other_agent: 'Agent') -> Optional[Dict[str, Any]]:
    """Interact with another agent"""
    # Simple interaction - could be expanded
    return {
        'type': 'interaction',
        'agents': [self.id, other_agent.id],
        'location': self.location_id
    }

def add_legacy_memory(self, memory_id: str, memory_data: Dict[str, Any]):
    """Add a memory to the agent (legacy method)"""
    if not hasattr(self, 'memories'):
        self.memories = {}
    self.memories[memory_id] = memory_data

def get_relationship(self, other_agent_id: str) -> Optional[Relationship]:
    """Get relationship with another agent"""
    return self.relationships.get(other_agent_id)

def update_relationship(self, other_agent_id: str, relationship: Relationship):
    """Update relationship with another agent"""
    self.relationships[other_agent_id] = relationship

def get_closest_allies(self, min_affinity: float = 20) -> List[Tuple[str, Relationship]]:
    """Get agents with positive relationships above threshold"""
    allies = []
    for agent_id, relationship in self.relationships.items():
        if relationship.affinity >= min_affinity and relationship.is_positive():
            allies.append((agent_id, relationship))

    # Sort by relationship strength
    allies.sort(key=lambda x: x[1].get_strength(), reverse=True)
    return allies

def get_enemies(self, max_affinity: float = -20) -> List[Tuple[str, Relationship]]:
    """Get agents with negative relationships below threshold"""
    enemies = []
    for agent_id, relationship in self.relationships.items():
        if relationship.affinity <= max_affinity or relationship.is_negative():
            enemies.append((agent_id, relationship))

    # Sort by relationship strength (most negative first)
    enemies.sort(key=lambda x: x[1].get_strength())
    return enemies

def serialize(self) -> Dict[str, Any]:
    """Serialize agent to dictionary"""
    return {
        'id': self.id,
        'name': self.name,
        'faction_id': self.faction_id,
        'location_id': self.location_id,
        'status': self.status.value,
        'background': self.background,
        'loyalty': self.loyalty,
        'stress': self.stress,
        'skills': {k.value: {'level': v.level, 'experience': v.experience} for k, v in self.skills.items()},
        'equipment': [{'name': e.name, 'type': e.type, 'effectiveness': e.effectiveness} for e in self.equipment],
        'emotional_state': self.emotional_state.serialize(),
        'relationships': {k: v.as_dict() for k, v in self.relationships.items()},
        'social_tags': list(self.social_tags),
        'memories': getattr(self, 'memories', {}),
        # Advanced relationship data
        'secrets': [s.as_dict() for s in self.secrets],
        'memory_journal': [m.as_dict() for m in self.memory_journal],
        'masked_relationships': {k: v.as_dict() for k, v in self.masked_relationships.items()},
        'ideology_vector': self.ideology_vector,
        'emotion_state': self.emotion_state,
        'planned_betrayal': self.planned_betrayal.as_dict() if self.planned_betrayal else None,
        'persona_active': self.persona_active
    }

@classmethod
def deserialize(cls, data: Dict[str, Any]) -> 'Agent':
    """Create agent from serialized data"""
    agent = cls(
        id=data['id'],
        name=data['name'],
        faction_id=data['faction_id'],
        location_id=data['location_id'],
        status=AgentStatus(data['status']),
        background=data['background'],
        loyalty=data['loyalty'],
        stress=data['stress']
    )

    # Restore skills
    for skill_name, skill_data in data.get('skills', {}).items():
        skill_type = SkillType(skill_name)
        agent.skills[skill_type] = Skill(level=skill_data['level'], experience=skill_data['experience'])

    # Restore equipment
    for equip_data in data.get('equipment', []):
        agent.equipment.append(Equipment(**equip_data))

    # Restore emotional state
    agent.emotional_state = EmotionalState.deserialize(data.get('emotional_state', {}))

    # Restore relationships
    for agent_id, rel_data in data.get('relationships', {}).items():
        agent.relationships[agent_id] = Relationship.from_dict(rel_data)

    # Restore social tags
    agent.social_tags = set(data.get('social_tags', []))

    # Restore memories
    agent.memories = data.get('memories', {})

    # Restore advanced relationship data
    for secret_data in data.get('secrets', []):
        agent.secrets.append(Secret.from_dict(secret_data))

    for memory_data in data.get('memory_journal', []):
        agent.memory_journal.append(MemoryEntry.from_dict(memory_data))

    for agent_id, rel_data in data.get('masked_relationships', {}).items():
        agent.masked_relationships[agent_id] = Relationship.from_dict(rel_data)

    agent.ideology_vector = data.get('ideology_vector', agent.ideology_vector)
    agent.emotion_state = data.get('emotion_state', agent.emotion_state)

    if data.get('planned_betrayal'):
        agent.planned_betrayal = BetrayalPlan.from_dict(data['planned_betrayal'])

    agent.persona_active = data.get('persona_active', False)

    return agent


# Add all Agent methods to the Agent class
Agent._initialize_social_tags = _initialize_social_tags
Agent._initialize_ideology = _initialize_ideology
Agent.__post_init__ = agent_post_init
Agent.add_secret = add_secret
Agent.get_secret = get_secret
Agent.remove_secret = remove_secret
Agent.add_memory = add_memory
Agent.add_legacy_memory = add_legacy_memory
Agent.get_recent_memories = get_recent_memories
Agent.get_memories_by_agent = get_memories_by_agent
Agent.set_persona_mask = set_persona_mask
Agent.remove_persona_mask = remove_persona_mask
Agent.get_displayed_relationship = get_displayed_relationship
Agent.can_detect_mask = can_detect_mask
Agent.update_ideology = update_ideology
Agent.get_dominant_ideology = get_dominant_ideology
Agent.update_emotion = update_emotion
Agent.get_dominant_emotion = get_dominant_emotion
Agent.plan_betrayal = plan_betrayal
Agent.cancel_betrayal_plan = cancel_betrayal_plan
Agent.update_emotional_state = update_emotional_state
Agent.process_event = process_event
Agent.is_state_valid = is_state_valid
Agent.interact_with = interact_with
Agent.get_relationship = get_relationship
Agent.update_relationship = update_relationship
Agent.get_closest_allies = get_closest_allies
Agent.get_enemies = get_enemies
Agent.serialize = serialize
Agent.deserialize = classmethod(deserialize)


# Extend the base GameState class with complex functionality
class GameState(GameState):
    """Main game state manager"""

    def __init__(self):
        self.turn_number = 1
        self.current_phase = GamePhase.PLANNING
        self.agents: Dict[str, Agent] = {}
        self.factions: Dict[str, Faction] = {}
        self.locations: Dict[str, Location] = {}
        self.missions: Dict[str, Mission] = {}
        self.social_network = SocialNetwork()
        self.recent_narrative: List[str] = []

        # Advanced relationship manager
        from .advanced_relationships import AdvancedRelationshipManager
        self.advanced_relationships = AdvancedRelationshipManager(self)

    def initialize_game(self):
        """Initialize the game with default state"""
        self._create_default_factions()
        self._create_default_locations()
        self._create_default_agents()
        self._initialize_relationships()
        self._add_initial_narrative()

        # Initialize advanced relationship mechanics
        self._initialize_advanced_relationships()

    def _initialize_advanced_relationships(self):
        """Initialize advanced relationship mechanics"""
        # Generate initial secrets for some agents
        for agent_id, agent in self.agents.items():
            if random.random() < 0.3:  # 30% chance of having a secret
                secret = self.advanced_relationships.generate_secret_for_agent(agent)
                agent.add_secret(secret)

        # Initialize emotion states and ideology vectors
        for agent in self.agents.values():
            agent._current_turn = self.turn_number

    def advance_turn(self):
        """Advance to the next turn"""
        self.turn_number += 1

        # Update current turn for all agents
        for agent in self.agents.values():
            agent._current_turn = self.turn_number

        # Process advanced relationship mechanics
        self.advanced_relationships.process_turn()

        # Process regular turn mechanics
        self._process_planning_phase()
        self._process_action_phase()
        self._process_resolution_phase()

        # Process relationship events
        self._process_relationship_events()

        # Apply relationship decay
        self.social_network.decay_all_relationships()

        # Update faction resources
        for faction in self.factions.values():
            self._update_faction_resources(faction)

    def step(self):
        """Step the game forward one turn"""
        self.advance_turn()

    def generate_secret_for_agent(self, agent_id: str, secret_type=None) -> Optional[Secret]:
        """Generate a secret for a specific agent"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        secret = self.advanced_relationships.generate_secret_for_agent(agent, secret_type)
        agent.add_secret(secret)
        return secret

    def spread_rumor(self, secret_id: str, source_agent_id: str, target_agent_id: str,
                    success_chance: float = 0.3) -> bool:
        """Attempt to spread a rumor about a secret"""
        if source_agent_id not in self.agents or target_agent_id not in self.agents:
            return False

        source_agent = self.agents[source_agent_id]
        secret = source_agent.get_secret(secret_id)

        if not secret:
            return False

        return self.advanced_relationships.spread_rumor(secret, source_agent_id, target_agent_id, success_chance)

    def use_blackmail(self, blackmailer_id: str, target_id: str, secret_id: str) -> Dict[str, Any]:
        """Use a secret for blackmail"""
        if blackmailer_id not in self.agents or target_id not in self.agents:
            return {"success": False, "reason": "Agent not found"}

        blackmailer = self.agents[blackmailer_id]
        secret = blackmailer.get_secret(secret_id)

        if not secret:
            return {"success": False, "reason": "Secret not found"}

        result = self.advanced_relationships.use_blackmail(blackmailer_id, target_id, secret)

        if result["success"]:
            self.recent_narrative.append(result["narrative"])

        return result

    def create_memory_entry(self, agent_id: str, event_type: str, other_agent_id: str = None,
                           custom_summary: str = None) -> Optional[MemoryEntry]:
        """Create a memory entry for an agent"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        memory = self.advanced_relationships.create_memory_entry(
            agent, event_type, other_agent_id, custom_summary
        )
        agent.add_memory(memory)
        return memory

    def set_persona_mask(self, agent_id: str, target_agent_id: str,
                        masked_affinity: float, masked_trust: float, masked_loyalty: float):
        """Set a persona mask for an agent's relationship"""
        if agent_id not in self.agents or target_agent_id not in self.agents:
            return

        agent = self.agents[agent_id]
        masked_relationship = Relationship(
            affinity=masked_affinity,
            trust=masked_trust,
            loyalty=masked_loyalty,
            bond_type=BondType.ACQUAINTANCE
        )

        agent.set_persona_mask(target_agent_id, masked_relationship)

    def check_mask_detection(self, observer_id: str, target_id: str) -> bool:
        """Check if an observer can detect a target's persona mask"""
        if observer_id not in self.agents or target_id not in self.agents:
            return False

        observer = self.agents[observer_id]
        target = self.agents[target_id]

        if not target.persona_active:
            return False

        # Use persuasion skill as empathy proxy
        empathy_skill = observer.skills.get(SkillType.PERSUASION, Skill()).level / 10.0
        return observer.can_detect_mask(target_id, empathy_skill)

    def get_agent_secrets(self, agent_id: str) -> List[Secret]:
        """Get all secrets held by an agent"""
        if agent_id not in self.agents:
            return []

        return self.agents[agent_id].secrets

    def get_agent_memories(self, agent_id: str, turns_back: int = 5) -> List[MemoryEntry]:
        """Get recent memories for an agent"""
        if agent_id not in self.agents:
            return []

        return self.agents[agent_id].get_recent_memories(turns_back)

    def get_ideological_distance(self, agent_a_id: str, agent_b_id: str) -> float:
        """Calculate ideological distance between two agents"""
        if agent_a_id not in self.agents or agent_b_id not in self.agents:
            return 0.5

        return self.advanced_relationships._calculate_ideological_distance(
            self.agents[agent_a_id], self.agents[agent_b_id]
        )

    def get_defection_risk(self, agent_id: str) -> float:
        """Calculate an agent's risk of defecting from their faction"""
        if agent_id not in self.agents:
            return 0.0

        return self.advanced_relationships.check_defection_risk(self.agents[agent_id])

    def create_betrayal_plan(self, agent_id: str, target_agent_id: str,
                           trigger_conditions: Dict[str, Any], preferred_timing: str = "immediate") -> Optional[BetrayalPlan]:
        """Create a betrayal plan for an agent"""
        if agent_id not in self.agents or target_agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        target = self.agents[target_agent_id]

        plan = self.advanced_relationships.create_betrayal_plan(agent, target)
        agent.planned_betrayal = plan
        return plan

    def get_faction_ideology(self, faction_id: str) -> Dict[str, float]:
        """Get the average ideology vector for a faction"""
        faction_agents = [a for a in self.agents.values() if a.faction_id == faction_id]

        if not faction_agents:
            return {}

        faction_ideology = {}
        for ideology in ["radical", "pacifist", "individualist", "traditional", "nationalist", "materialist"]:
            avg_value = sum(a.ideology_vector.get(ideology, 0.5) for a in faction_agents) / len(faction_agents)
            faction_ideology[ideology] = avg_value

        return faction_ideology

    def get_emotion_propagation_summary(self) -> Dict[str, Any]:
        """Get a summary of emotion propagation across the social network"""
        emotion_totals = {}
        emotion_counts = {}

        for agent in self.agents.values():
            for emotion, value in agent.emotion_state.items():
                if emotion not in emotion_totals:
                    emotion_totals[emotion] = 0.0
                    emotion_counts[emotion] = 0

                emotion_totals[emotion] += value
                emotion_counts[emotion] += 1

        emotion_averages = {}
        for emotion in emotion_totals:
            if emotion_counts[emotion] > 0:
                emotion_averages[emotion] = emotion_totals[emotion] / emotion_counts[emotion]

        return {
            "emotion_averages": emotion_averages,
            "total_agents": len(self.agents),
            "dominant_emotion": max(emotion_averages.items(), key=lambda x: x[1]) if emotion_averages else ("neutral", 0.5)
        }

    def get_secret_network_summary(self) -> Dict[str, Any]:
        """Get a summary of the secret network"""
        total_secrets = 0
        weaponized_secrets = 0
        secret_types = {}

        for agent in self.agents.values():
            total_secrets += len(agent.secrets)
            for secret in agent.secrets:
                if secret.weaponized:
                    weaponized_secrets += 1

                secret_type = secret.secret_type.value
                secret_types[secret_type] = secret_types.get(secret_type, 0) + 1

        return {
            "total_secrets": total_secrets,
            "weaponized_secrets": weaponized_secrets,
            "secret_types": secret_types,
            "agents_with_secrets": sum(1 for a in self.agents.values() if a.secrets)
        }

    def get_memory_network_summary(self) -> Dict[str, Any]:
        """Get a summary of the memory network"""
        total_memories = 0
        memory_tones = {}
        recent_memories = 0

        for agent in self.agents.values():
            total_memories += len(agent.memory_journal)
            recent_memories += len(agent.get_recent_memories(5))

            for memory in agent.memory_journal:
                tone = memory.emotional_tone
                memory_tones[tone] = memory_tones.get(tone, 0) + 1

        return {
            "total_memories": total_memories,
            "recent_memories": recent_memories,
            "memory_tones": memory_tones,
            "agents_with_memories": sum(1 for a in self.agents.values() if a.memory_journal)
        }

    def _create_default_factions(self):
        """Create the default resistance factions"""
        self.factions = {
            "resistance": Faction(
                id="resistance",
                name="The Resistance",
                current_goal="military_operations",
                resources={"money": 150, "influence": 15, "personnel": 8}
            ),
            "urban_liberation": Faction(
                id="urban_liberation",
                name="Urban Liberation Front",
                current_goal="propaganda",
                resources={"money": 80, "influence": 25, "personnel": 12}
            ),
            "underground": Faction(
                id="underground",
                name="Underground Network",
                current_goal="intelligence",
                resources={"money": 200, "influence": 8, "personnel": 4}
            )
        }

    def _create_default_locations(self):
        """Create the default game locations"""
        self.locations = {
            "safehouse_alpha": Location(
                id="safehouse_alpha",
                name="Safehouse Alpha",
                security_level=2,
                unrest_level=1
            ),
            "university_district": Location(
                id="university_district",
                name="University District",
                security_level=4,
                unrest_level=6
            ),
            "industrial_zone": Location(
                id="industrial_zone",
                name="Industrial Zone",
                security_level=6,
                unrest_level=8
            ),
            "government_quarter": Location(
                id="government_quarter",
                name="Government Quarter",
                security_level=9,
                unrest_level=2
            ),
            "old_town": Location(
                id="old_town",
                name="Old Town Market",
                security_level=5,
                unrest_level=5
            )
        }

    def _create_default_agents(self):
        """Create the default operative agents"""
        agent_configs = [
            ("agent_maria", "Maria Santos", "urban_liberation", "university_district", "student"),
            ("agent_carlos", "Carlos Mendez", "resistance", "safehouse_alpha", "veteran"),
            ("agent_ana", "Ana Rodriguez", "underground", "old_town", "journalist"),
            ("agent_luis", "Luis Garcia", "resistance", "industrial_zone", "worker"),
            ("agent_sofia", "Sofia Vargas", "urban_liberation", "university_district", "organizer"),
            ("agent_miguel", "Miguel Torres", "underground", "government_quarter", "insider")
        ]

        for agent_id, name, faction_id, location_id, background in agent_configs:
            self.agents[agent_id] = Agent(
                id=agent_id,
                name=name,
                faction_id=faction_id,
                location_id=location_id,
                background=background,
                loyalty=random.randint(60, 90),
                stress=random.randint(10, 30)
            )

    def _initialize_relationships(self):
        """Initialize relationships between agents"""
        from .relationships import BondType, EventType

        # Create some initial relationships
        relationship_configs = [
            # Maria and Sofia - fellow students and organizers
            ("agent_maria", "agent_sofia", BondType.ALLY, 40, 0.8, 0.85),

            # Carlos and Luis - veterans and workers, comrades
            ("agent_carlos", "agent_luis", BondType.COMRADE, 35, 0.75, 0.8),

            # Ana and Miguel - journalists and insiders, professional respect
            ("agent_ana", "agent_miguel", BondType.FRIEND, 25, 0.7, 0.6),

            # Carlos mentors Maria (veteran mentoring student)
            ("agent_carlos", "agent_maria", BondType.MENTOR, 30, 0.8, 0.75),
            ("agent_maria", "agent_carlos", BondType.STUDENT, 30, 0.8, 0.75),

            # Sofia and Luis - potential rivalry (organizer vs worker)
            ("agent_sofia", "agent_luis", BondType.RIVAL, -15, 0.4, 0.3),
            ("agent_luis", "agent_sofia", BondType.RIVAL, -15, 0.4, 0.3),

            # Ana and Maria - journalist and student, potential friendship
            ("agent_ana", "agent_maria", BondType.FRIEND, 20, 0.6, 0.5),
            ("agent_maria", "agent_ana", BondType.FRIEND, 20, 0.6, 0.5),
        ]

        for agent_a, agent_b, bond_type, affinity, trust, loyalty in relationship_configs:
            if agent_a in self.agents and agent_b in self.agents:
                relationship = Relationship(
                    agent_id=agent_b,
                    bond_type=bond_type,
                    affinity=affinity,
                    trust=trust,
                    loyalty=loyalty
                )

                # Add to social network
                self.social_network.add_relationship(agent_a, agent_b, relationship)

                # Add to agent's relationship dict
                self.agents[agent_a].update_relationship(agent_b, relationship)
                self.agents[agent_b].update_relationship(agent_a, relationship)

    def _add_initial_narrative(self):
        """Add initial narrative events"""
        self.recent_narrative = [
            "Resistance cells established across the city",
            "Government increases security patrols in university district",
            "Underground network reports increased surveillance",
            "Worker strikes spread through industrial zones",
            "Student protests gain momentum in university district",
            "Government announces new emergency powers",
            "Resistance recruitment drives begin in safe areas",
            "Intelligence reports government infiltration attempts"
        ]

    def _process_planning_phase(self):
        """Process planning phase actions"""
        self.recent_narrative.append(f"Turn {self.turn_number}: Planning phase - Factions coordinate operations")

        # Process relationship-based events during planning
        self._process_relationship_events()

    def _process_action_phase(self):
        """Process action phase operations"""
        self.recent_narrative.append(f"Turn {self.turn_number}: Action phase - Operatives execute missions")

        # Simulate some mission results
        for faction in self.factions.values():
            if random.random() < 0.3:  # 30% chance of event
                self._generate_faction_event(faction)

    def _process_resolution_phase(self):
        """Process resolution phase outcomes"""
        self.recent_narrative.append(f"Turn {self.turn_number}: Resolution phase - Assessing operation outcomes")

        # Update faction resources
        for faction in self.factions.values():
            self._update_faction_resources(faction)

        # Apply relationship decay
        self.social_network.decay_all_relationships()

        # Update social clusters
        self.social_network.get_social_clusters()

    def _process_relationship_events(self):
        """Process events that affect relationships between agents"""
        from .relationships import EventType

        # Random relationship events
        for agent_id, agent in self.agents.items():
            if random.random() < 0.2:  # 20% chance per agent
                self._generate_relationship_event(agent)

    def _generate_relationship_event(self, agent: Agent):
        """Generate a random relationship event for an agent"""
        from .relationships import EventType

        # Get agent's social circle
        social_circle = self.social_network.get_social_circle(agent.id)

        if not social_circle:
            return

        # Pick a random agent from social circle
        other_id, relationship = random.choice(social_circle)
        other_agent = self.agents.get(other_id)

        if not other_agent:
            return

        # Generate event based on relationship type
        event_type = self._select_relationship_event_type(relationship)

        if event_type:
            # Apply event effects
            self.social_network.update_relationship(
                agent.id, other_id, event_type=event_type
            )

            # Generate narrative
            narrative = self._generate_relationship_narrative(agent, other_agent, event_type)
            self.recent_narrative.append(narrative)

    def _select_relationship_event_type(self, relationship) -> Optional[EventType]:
        """Select an appropriate event type based on relationship"""
        if relationship.is_positive():
            positive_events = [
                EventType.COOPERATION, EventType.SHARED_RISK,
                EventType.MENTORSHIP, EventType.LOYALTY_TEST
            ]
            return random.choice(positive_events)
        elif relationship.is_negative():
            negative_events = [
                EventType.CONFLICT, EventType.COMPETITION,
                EventType.ABANDONMENT
            ]
            return random.choice(negative_events)
        else:
            neutral_events = [
                EventType.COOPERATION, EventType.CONFLICT,
                EventType.COMPETITION
            ]
            return random.choice(neutral_events)

    def _generate_relationship_narrative(self, agent_a: Agent, agent_b: Agent, event_type: EventType) -> str:
        """Generate narrative for relationship events"""
        event_narratives = {
            EventType.SHARED_RISK: f"{agent_a.name} and {agent_b.name} face danger together, strengthening their bond",
            EventType.ABANDONMENT: f"{agent_a.name} feels betrayed when {agent_b.name} fails to provide backup",
            EventType.BETRAYAL: f"{agent_b.name} betrays {agent_a.name}'s trust, causing deep resentment",
            EventType.RESCUE: f"{agent_a.name} rescues {agent_b.name} from a dangerous situation",
            EventType.MENTORSHIP: f"{agent_a.name} teaches {agent_b.name} valuable skills",
            EventType.CONFLICT: f"{agent_a.name} and {agent_b.name} clash over strategy",
            EventType.SACRIFICE: f"{agent_a.name} makes a sacrifice to protect {agent_b.name}",
            EventType.COOPERATION: f"{agent_a.name} and {agent_b.name} work together successfully",
            EventType.COMPETITION: f"{agent_a.name} and {agent_b.name} compete for resources",
            EventType.LOYALTY_TEST: f"{agent_a.name} tests {agent_b.name}'s loyalty to the cause"
        }

        return event_narratives.get(event_type, f"{agent_a.name} and {agent_b.name} interact")

    def _generate_faction_event(self, faction: Faction):
        """Generate a random event for a faction"""
        events = [
            f"{faction.name} successfully recruits new operatives",
            f"{faction.name} operation encounters government resistance",
            f"{faction.name} discovers valuable intelligence",
            f"{faction.name} faces internal loyalty challenges",
            f"{faction.name} establishes new safe house location"
        ]

        event = random.choice(events)
        self.recent_narrative.append(event)

    def _update_faction_resources(self, faction: Faction):
        """Update faction resources based on activities"""
        # Small random resource changes
        money_change = random.randint(-10, 20)
        influence_change = random.randint(-2, 5)
        personnel_change = random.randint(-1, 2)

        faction.resources["money"] = max(0, faction.resources["money"] + money_change)
        faction.resources["influence"] = max(0, faction.resources["influence"] + influence_change)
        faction.resources["personnel"] = max(1, faction.resources["personnel"] + personnel_change)

    def get_status_summary(self) -> Dict[str, Any]:
        """Get current game status summary"""
        active_agents = len([a for a in self.agents.values() if a.status == AgentStatus.ACTIVE])

        faction_resources = {}
        for faction_id, faction in self.factions.items():
            faction_resources[faction_id] = faction.resources.copy()

        # Calculate faction cohesion
        faction_cohesion = {}
        for faction_id, faction in self.factions.items():
            faction_agents = [a.id for a in self.agents.values() if a.faction_id == faction_id]
            cohesion = self.social_network.get_faction_cohesion_index(faction_agents)
            faction_cohesion[faction_id] = cohesion

        return {
            "turn": self.turn_number,
            "phase": self.current_phase.value,
            "active_agents": active_agents,
            "total_agents": len(self.agents),
            "factions": faction_resources,
            "faction_cohesion": faction_cohesion,
            "recent_narrative": self.recent_narrative[-10:],  # Last 10 events
            "active_events": self.active_events
        }

    def get_agent_locations(self) -> Dict[str, List[str]]:
        """Get agents grouped by location"""
        locations = {}

        for agent in self.agents.values():
            if agent.status == AgentStatus.ACTIVE:
                if agent.location_id not in locations:
                    locations[agent.location_id] = []

                faction_name = self.factions[agent.faction_id].name
                locations[agent.location_id].append(f"{agent.name} ({faction_name})")

        return locations

    def add_agent(self, agent: Agent):
        """Add an agent to the game state"""
        self.agents[agent.id] = agent

    def update_relationship(self, agent_a: str, agent_b: str,
                          delta_affinity: float = 0, delta_trust: float = 0,
                          delta_loyalty: float = 0, event_type=None):
        """Update relationship between two agents"""
        self.social_network.update_relationship(
            agent_a, agent_b, delta_affinity, delta_trust, delta_loyalty, event_type
        )

        # Also update agent's internal relationship dict
        relationship = self.social_network.get_relationship(agent_a, agent_b)
        if relationship and agent_a in self.agents:
            self.agents[agent_a].update_relationship(agent_b, relationship)

        if agent_b in self.agents:
            reverse_relationship = self.social_network.get_relationship(agent_b, agent_a)
            if reverse_relationship:
                self.agents[agent_b].update_relationship(agent_a, reverse_relationship)

    def get_social_circle(self, agent_id: str, bond_filter=None, min_affinity=None):
        """Get an agent's social circle"""
        return self.social_network.get_social_circle(agent_id, bond_filter, min_affinity)

    def get_most_influential(self, agent_id: str, radius: int = 2):
        """Get most influential agents near an agent"""
        return self.social_network.get_most_influential(agent_id, radius)

    def get_social_clusters(self):
        """Get current social clusters"""
        return self.social_network.get_social_clusters()

    def get_faction_cohesion(self, faction_id: str) -> float:
        """Get cohesion index for a faction"""
        faction_agents = [a.id for a in self.agents.values() if a.faction_id == faction_id]
        return self.social_network.get_faction_cohesion_index(faction_agents)