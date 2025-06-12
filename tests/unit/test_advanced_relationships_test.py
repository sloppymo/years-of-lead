"""
Unit tests for advanced relationship mechanics

Tests the six advanced relationship systems:
1. Secrets, Rumors & Emotional Blackmail
2. Gossip & Emotional Drift Propagation
3. Persona Masks & Social Deception
4. Political Fracture System
5. Shared Memory Journals
6. Ideological Drift & Alignment Shifts
"""

import pytest
import sys
import os
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from game.advanced_relationships import (
    Secret,
    MemoryEntry,
    BetrayalPlan,
    AdvancedRelationshipManager,
    SecretType,
)
from game.core import Agent, GameState
from game.relationships import Relationship


class TestSecret:
    """Test the Secret class"""

    def test_secret_creation(self):
        """Test creating a secret"""
        secret = Secret(
            id="test_secret_1",
            description="Has a family member working for the government",
            secret_type=SecretType.PERSONAL,
            impact=-0.3,
            emotional_weight=0.8,
        )

        assert secret.id == "test_secret_1"
        assert secret.description == "Has a family member working for the government"
        assert secret.secret_type == SecretType.PERSONAL
        assert secret.impact == -0.3
        assert secret.emotional_weight == 0.8
        assert not secret.weaponized
        assert len(secret.known_by) == 0

    def test_can_be_weaponized(self):
        """Test weaponization logic"""
        # Secret with high negative impact can be weaponized
        weaponizable_secret = Secret(
            id="test_1",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.3,
            emotional_weight=0.8,
        )
        assert weaponizable_secret.can_be_weaponized()

        # Secret with low impact cannot be weaponized
        weak_secret = Secret(
            id="test_2",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.1,
            emotional_weight=0.8,
        )
        assert not weak_secret.can_be_weaponized()

        # Already weaponized secret cannot be weaponized again
        weaponizable_secret.weaponized = True
        assert not weaponizable_secret.can_be_weaponized()

    def test_get_blackmail_potential(self):
        """Test blackmail potential calculation"""
        secret = Secret(
            id="test_1",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.4,
            emotional_weight=0.9,
        )

        potential = secret.get_blackmail_potential()
        expected = abs(-0.4) * 0.9
        assert potential == expected

        # Non-weaponizable secret has no potential
        weak_secret = Secret(
            id="test_2",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.1,
            emotional_weight=0.8,
        )
        assert weak_secret.get_blackmail_potential() == 0.0

    def test_serialization(self):
        """Test secret serialization and deserialization"""
        secret = Secret(
            id="test_1",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.3,
            emotional_weight=0.8,
            known_by={"agent_1", "agent_2"},
            weaponized=True,
            created_turn=5,
            discovered_turn=10,
        )

        data = secret.as_dict()
        restored = Secret.from_dict(data)

        assert restored.id == secret.id
        assert restored.description == secret.description
        assert restored.secret_type == secret.secret_type
        assert restored.impact == secret.impact
        assert restored.emotional_weight == secret.emotional_weight
        assert restored.known_by == secret.known_by
        assert restored.weaponized == secret.weaponized
        assert restored.created_turn == secret.created_turn
        assert restored.discovered_turn == secret.discovered_turn


class TestMemoryEntry:
    """Test the MemoryEntry class"""

    def test_memory_creation(self):
        """Test creating a memory entry"""
        memory = MemoryEntry(
            id="test_memory_1",
            summary="Agent A saved Agent B's life",
            emotional_tone="grateful",
            agent_involved="agent_b",
            impact_score=0.5,
            created_turn=10,
        )

        assert memory.id == "test_memory_1"
        assert memory.summary == "Agent A saved Agent B's life"
        assert memory.emotional_tone == "grateful"
        assert memory.agent_involved == "agent_b"
        assert memory.impact_score == 0.5
        assert memory.created_turn == 10

    def test_get_age(self):
        """Test memory age calculation"""
        memory = MemoryEntry(
            id="test_1", summary="Test memory", emotional_tone="neutral", created_turn=5
        )

        assert memory.get_age(10) == 5
        assert memory.get_age(5) == 0
        assert memory.get_age(3) == -2

    def test_get_fading_impact(self):
        """Test memory impact decay"""
        memory = MemoryEntry(
            id="test_1",
            summary="Test memory",
            emotional_tone="neutral",
            impact_score=1.0,
            created_turn=0,
        )

        # Impact should decay over time
        impact_immediate = memory.get_fading_impact(0)
        impact_after_5_turns = memory.get_fading_impact(5)
        impact_after_10_turns = memory.get_fading_impact(10)

        assert impact_immediate == 1.0
        assert impact_after_5_turns < impact_immediate
        assert impact_after_10_turns < impact_after_5_turns

    def test_serialization(self):
        """Test memory serialization and deserialization"""
        memory = MemoryEntry(
            id="test_1",
            summary="Test memory",
            emotional_tone="grateful",
            agent_involved="agent_b",
            impact_score=0.5,
            created_turn=10,
            relationship_context={"affinity": 30, "trust": 0.7},
            symbolic_elements=["rescue", "loyalty"],
        )

        data = memory.as_dict()
        restored = MemoryEntry.from_dict(data)

        assert restored.id == memory.id
        assert restored.summary == memory.summary
        assert restored.emotional_tone == memory.emotional_tone
        assert restored.agent_involved == memory.agent_involved
        assert restored.impact_score == memory.impact_score
        assert restored.created_turn == memory.created_turn
        assert restored.relationship_context == memory.relationship_context
        assert restored.symbolic_elements == memory.symbolic_elements


class TestBetrayalPlan:
    """Test the BetrayalPlan class"""

    def test_betrayal_plan_creation(self):
        """Test creating a betrayal plan"""
        plan = BetrayalPlan(
            target_agent="agent_b",
            trigger_conditions={
                "low_trust": 0.3,
                "high_stress": 0.7,
                "ideological_distance": 0.6,
            },
            preferred_timing="during_mission",
            potential_co_conspirators=["agent_c", "agent_d"],
            plan_confidence=0.6,
            created_turn=10,
        )

        assert plan.target_agent == "agent_b"
        assert len(plan.trigger_conditions) == 3
        assert plan.preferred_timing == "during_mission"
        assert len(plan.potential_co_conspirators) == 2
        assert plan.plan_confidence == 0.6
        assert plan.created_turn == 10

    def test_should_activate(self):
        """Test betrayal plan activation logic"""
        plan = BetrayalPlan(
            target_agent="agent_b",
            trigger_conditions={
                "low_trust": 0.3,
                "high_stress": 0.7,
                "ideological_distance": 0.6,
            },
            preferred_timing="immediate",
            activation_threshold=0.7,
        )

        # All conditions met - should activate
        conditions_all_met = {
            "low_trust": 0.4,
            "high_stress": 0.8,
            "ideological_distance": 0.7,
        }
        assert plan.should_activate(conditions_all_met)

        # Only 2/3 conditions met - should not activate
        conditions_partial = {
            "low_trust": 0.4,
            "high_stress": 0.8,
            "ideological_distance": 0.5,
        }
        assert not plan.should_activate(conditions_partial)

        # No conditions met - should not activate
        conditions_none = {
            "low_trust": 0.2,
            "high_stress": 0.5,
            "ideological_distance": 0.4,
        }
        assert not plan.should_activate(conditions_none)

    def test_serialization(self):
        """Test betrayal plan serialization and deserialization"""
        plan = BetrayalPlan(
            target_agent="agent_b",
            trigger_conditions={"low_trust": 0.3, "high_stress": 0.7},
            preferred_timing="immediate",
            potential_co_conspirators=["agent_c"],
            plan_confidence=0.6,
            created_turn=10,
            activation_threshold=0.7,
        )

        data = plan.as_dict()
        restored = BetrayalPlan.from_dict(data)

        assert restored.target_agent == plan.target_agent
        assert restored.trigger_conditions == plan.trigger_conditions
        assert restored.preferred_timing == plan.preferred_timing
        assert restored.potential_co_conspirators == plan.potential_co_conspirators
        assert restored.plan_confidence == plan.plan_confidence
        assert restored.created_turn == plan.created_turn
        assert restored.activation_threshold == plan.activation_threshold


class TestAdvancedRelationshipManager:
    """Test the AdvancedRelationshipManager class"""

    @pytest.fixture
    def game_state(self):
        """Create a test game state"""
        state = GameState()
        state.turn_number = 1

        # Create test agents
        agent_a = Agent(
            id="agent_a",
            name="Agent A",
            faction_id="resistance",
            location_id="safe_house_1",
            background="veteran",
        )
        agent_b = Agent(
            id="agent_b",
            name="Agent B",
            faction_id="resistance",
            location_id="safe_house_1",
            background="student",
        )
        agent_c = Agent(
            id="agent_c",
            name="Agent C",
            faction_id="resistance",
            location_id="safe_house_1",
            background="worker",
        )

        state.agents = {"agent_a": agent_a, "agent_b": agent_b, "agent_c": agent_c}

        # Create test faction
        from game.core import Faction

        state.factions = {
            "resistance": Faction(
                id="resistance", name="Resistance", current_goal="recruitment"
            )
        }

        return state

    @pytest.fixture
    def manager(self, game_state):
        """Create an advanced relationship manager"""
        return AdvancedRelationshipManager(game_state)

    def test_generate_secret_for_agent(self, manager, game_state):
        """Test secret generation"""
        agent = game_state.agents["agent_a"]
        secret = manager.generate_secret_for_agent(agent, SecretType.PERSONAL)

        assert secret is not None
        assert secret.secret_type == SecretType.PERSONAL
        assert secret.impact < 0  # Should be negative for personal secrets
        assert secret.emotional_weight > 0
        assert secret.created_turn == game_state.turn_number

    def test_spread_rumor(self, manager, game_state):
        """Test rumor spreading"""
        agent_a = game_state.agents["agent_a"]
        game_state.agents["agent_b"]

        # Create a secret
        secret = Secret(
            id="test_secret",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.3,
            emotional_weight=0.8,
        )
        agent_a.add_secret(secret)

        # Test successful rumor spread
        with patch("random.random", return_value=0.1):  # Low random value = success
            success = manager.spread_rumor(
                secret, "agent_a", "agent_b", success_chance=0.3
            )
            assert success
            assert "agent_b" in secret.known_by

        # Test failed rumor spread
        with patch("random.random", return_value=0.5):  # High random value = failure
            success = manager.spread_rumor(
                secret, "agent_a", "agent_c", success_chance=0.3
            )
            assert not success
            assert "agent_c" not in secret.known_by

    def test_use_blackmail(self, manager, game_state):
        """Test blackmail mechanics"""
        agent_a = game_state.agents["agent_a"]
        game_state.agents["agent_b"]

        # Create a weaponizable secret
        secret = Secret(
            id="test_secret",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.4,
            emotional_weight=0.9,
        )
        agent_a.add_secret(secret)

        # Test successful blackmail
        with patch("random.random", return_value=0.1):  # Low random value = success
            result = manager.use_blackmail("agent_a", "agent_b", secret)
            assert result["success"]
            assert secret.weaponized

        # Test failed blackmail
        secret.weaponized = False
        with patch("random.random", return_value=0.9):  # High random value = failure
            result = manager.use_blackmail("agent_a", "agent_b", secret)
            assert not result["success"]
            assert not secret.weaponized

    def test_create_memory_entry(self, manager, game_state):
        """Test memory entry creation"""
        agent = game_state.agents["agent_a"]
        memory = manager.create_memory_entry(
            agent, "custom_event", "agent_b", "Custom memory summary"
        )

        assert memory is not None
        assert memory.summary == "Custom memory summary"
        assert memory.agent_involved == "agent_b"
        assert memory.emotional_tone == "neutral"  # Default for custom events
        assert memory.impact_score == 0.0  # Default for custom events

    def test_propagate_emotions(self, manager, game_state):
        """Test emotion propagation"""
        agent_a = game_state.agents["agent_a"]
        agent_b = game_state.agents["agent_b"]

        # Set different emotion states
        agent_a.emotion_state = {"hope": 0.8, "fear": 0.2, "anger": 0.1, "despair": 0.1}
        agent_b.emotion_state = {"hope": 0.3, "fear": 0.6, "anger": 0.2, "despair": 0.3}

        # Create a relationship between them
        relationship = Relationship(
            agent_id="agent_b", affinity=20, trust=0.6, loyalty=0.7
        )
        agent_a.relationships["agent_b"] = relationship

        # Propagate emotions
        manager.propagate_emotions()

        # Check that emotions have drifted toward each other
        assert (
            agent_b.emotion_state["hope"] > 0.3
        )  # Should increase toward agent_a's 0.8
        assert (
            agent_a.emotion_state["fear"] > 0.2
        )  # Should increase toward agent_b's 0.6

    def test_ideology_drift(self, manager, game_state):
        """Test ideological drift"""
        agent_a = game_state.agents["agent_a"]
        agent_b = game_state.agents["agent_b"]

        # Set different ideology vectors
        agent_a.ideology_vector = {
            "radical": 0.8,
            "pacifist": 0.2,
            "individualist": 0.5,
        }
        agent_b.ideology_vector = {
            "radical": 0.3,
            "pacifist": 0.7,
            "individualist": 0.4,
        }

        # Create a positive relationship
        relationship = Relationship(
            agent_id="agent_b", affinity=30, trust=0.7, loyalty=0.8
        )
        agent_a.relationships["agent_b"] = relationship

        # Update ideologies
        manager.update_ideologies()

        # Check that ideologies have drifted toward each other
        assert (
            agent_b.ideology_vector["radical"] > 0.3
        )  # Should increase toward agent_a's 0.8
        assert (
            agent_a.ideology_vector["pacifist"] > 0.2
        )  # Should increase toward agent_b's 0.7

    def test_defection_risk_calculation(self, manager, game_state):
        """Test defection risk calculation"""
        agent = game_state.agents["agent_a"]

        # Set ideology that differs from faction average
        agent.ideology_vector = {"radical": 0.9, "pacifist": 0.1, "individualist": 0.8}

        # Other agents in faction have different ideology
        agent_b = game_state.agents["agent_b"]
        agent_c = game_state.agents["agent_c"]
        agent_b.ideology_vector = {
            "radical": 0.3,
            "pacifist": 0.7,
            "individualist": 0.4,
        }
        agent_c.ideology_vector = {
            "radical": 0.4,
            "pacifist": 0.6,
            "individualist": 0.3,
        }

        # Create relationships (low loyalty to faction)
        relationship = Relationship(
            agent_id="agent_b", affinity=10, trust=0.3, loyalty=0.2
        )
        agent.relationships["agent_b"] = relationship
        agent.relationships["agent_c"] = relationship

        risk = manager.check_defection_risk(agent)
        assert risk > 0.5  # Should be high due to ideological distance and low loyalty

    def test_create_betrayal_plan(self, manager, game_state):
        """Test betrayal plan creation"""
        agent_a = game_state.agents["agent_a"]
        agent_b = game_state.agents["agent_b"]

        plan = manager.create_betrayal_plan(agent_a, agent_b)

        assert plan is not None
        assert plan.target_agent == "agent_b"
        assert len(plan.trigger_conditions) > 0
        assert plan.preferred_timing in ["immediate", "during_mission", "after_success"]
        assert plan.plan_confidence > 0

    def test_betrayal_activation(self, manager, game_state):
        """Test betrayal plan activation"""
        agent_a = game_state.agents["agent_a"]
        agent_b = game_state.agents["agent_b"]

        # Create a betrayal plan
        plan = BetrayalPlan(
            target_agent="agent_b",
            trigger_conditions={
                "low_trust": 0.3,
                "high_stress": 0.7,
                "ideological_distance": 0.6,
            },
            preferred_timing="immediate",
            activation_threshold=0.7,
        )
        agent_a.planned_betrayal = plan

        # Set conditions that should trigger activation
        relationship = Relationship(
            agent_id="agent_b", affinity=-10, trust=0.2, loyalty=0.3
        )
        agent_a.relationships["agent_b"] = relationship
        agent_a.stress = 80  # High stress
        agent_a.ideology_vector = {"radical": 0.9, "pacifist": 0.1}
        agent_b.ideology_vector = {"radical": 0.2, "pacifist": 0.8}

        result = manager.check_betrayal_activation(agent_a)
        assert result is not None
        assert result["activated"]
        assert result["plan"] == plan


class TestGameStateIntegration:
    """Test integration with GameState"""

    @pytest.fixture
    def game_state(self):
        """Create a test game state with advanced relationships"""
        state = GameState()
        state.initialize_game()
        return state

    def test_advanced_relationship_initialization(self, game_state):
        """Test that advanced relationships are properly initialized"""
        assert hasattr(game_state, "advanced_relationships")
        assert game_state.advanced_relationships is not None

        # Check that some agents have secrets
        agents_with_secrets = sum(
            1 for agent in game_state.agents.values() if agent.secrets
        )
        assert agents_with_secrets > 0

        # Check that all agents have emotion states and ideology vectors
        for agent in game_state.agents.values():
            assert hasattr(agent, "emotion_state")
            assert hasattr(agent, "ideology_vector")
            assert len(agent.emotion_state) > 0
            assert len(agent.ideology_vector) > 0

    def test_secret_management(self, game_state):
        """Test secret management through GameState"""
        agent_id = list(game_state.agents.keys())[0]

        # Generate a secret
        secret = game_state.generate_secret_for_agent(agent_id, SecretType.PERSONAL)
        assert secret is not None
        assert secret.secret_type == SecretType.PERSONAL

        # Get agent secrets
        secrets = game_state.get_agent_secrets(agent_id)
        assert len(secrets) > 0
        assert secret in secrets

    def test_memory_management(self, game_state):
        """Test memory management through GameState"""
        agent_id = list(game_state.agents.keys())[0]
        other_agent_id = list(game_state.agents.keys())[1]

        # Create a memory entry
        memory = game_state.create_memory_entry(agent_id, "rescue", other_agent_id)
        assert memory is not None

        # Get agent memories
        memories = game_state.get_agent_memories(agent_id)
        assert len(memories) > 0
        assert memory in memories

    def test_persona_mask_management(self, game_state):
        """Test persona mask management through GameState"""
        agent_id = list(game_state.agents.keys())[0]
        target_id = list(game_state.agents.keys())[1]

        # Set a persona mask
        game_state.set_persona_mask(agent_id, target_id, 50, 0.8, 0.9)

        agent = game_state.agents[agent_id]
        assert agent.persona_active
        assert target_id in agent.masked_relationships

        # Check mask detection
        detection = game_state.check_mask_detection(target_id, agent_id)
        assert isinstance(detection, bool)

    def test_ideological_analysis(self, game_state):
        """Test ideological analysis through GameState"""
        agent_ids = list(game_state.agents.keys())[:2]

        # Calculate ideological distance
        distance = game_state.get_ideological_distance(agent_ids[0], agent_ids[1])
        assert 0 <= distance <= 1

        # Get faction ideology
        faction_id = game_state.agents[agent_ids[0]].faction_id
        faction_ideology = game_state.get_faction_ideology(faction_id)
        assert len(faction_ideology) > 0
        assert all(0 <= value <= 1 for value in faction_ideology.values())

    def test_defection_risk_analysis(self, game_state):
        """Test defection risk analysis through GameState"""
        agent_id = list(game_state.agents.keys())[0]

        risk = game_state.get_defection_risk(agent_id)
        assert 0 <= risk <= 1

    def test_betrayal_planning(self, game_state):
        """Test betrayal planning through GameState"""
        agent_ids = list(game_state.agents.keys())[:2]

        trigger_conditions = {
            "low_trust": 0.3,
            "high_stress": 0.7,
            "ideological_distance": 0.6,
        }

        plan = game_state.create_betrayal_plan(
            agent_ids[0], agent_ids[1], trigger_conditions, "immediate"
        )
        assert plan is not None
        assert plan.target_agent == agent_ids[1]

    def test_network_summaries(self, game_state):
        """Test network summary generation"""
        # Emotion propagation summary
        emotion_summary = game_state.get_emotion_propagation_summary()
        assert "emotion_averages" in emotion_summary
        assert "total_agents" in emotion_summary
        assert "dominant_emotion" in emotion_summary

        # Secret network summary
        secret_summary = game_state.get_secret_network_summary()
        assert "total_secrets" in secret_summary
        assert "weaponized_secrets" in secret_summary
        assert "secret_types" in secret_summary

        # Memory network summary
        memory_summary = game_state.get_memory_network_summary()
        assert "total_memories" in memory_summary
        assert "recent_memories" in memory_summary
        assert "memory_tones" in memory_summary

    def test_advanced_turn_processing(self, game_state):
        """Test that advanced mechanics are processed during turn advancement"""
        initial_turn = game_state.turn_number

        # Advance turn
        game_state.advance_turn()

        assert game_state.turn_number == initial_turn + 1

        # Check that agents have updated turn numbers
        for agent in game_state.agents.values():
            assert hasattr(agent, "_current_turn")
            assert agent._current_turn == game_state.turn_number

        # Check that some narrative was generated
        assert len(game_state.recent_narrative) > 0


class TestNarrativeEngineIntegration:
    """Test integration with the narrative engine"""

    @pytest.fixture
    def game_state(self):
        """Create a test game state"""
        state = GameState()
        state.initialize_game()
        return state

    @pytest.fixture
    def narrative_engine(self, game_state):
        """Create a narrative engine"""
        from game.narrative_engine import NarrativeEngine

        return NarrativeEngine(game_state)

    def test_advanced_narrative_generation(self, narrative_engine, game_state):
        """Test advanced narrative generation"""
        agent_ids = list(game_state.agents.keys())[:2]
        agent_a = game_state.agents[agent_ids[0]]
        agent_b = game_state.agents[agent_ids[1]]

        # Add a secret to trigger secret-based narrative
        secret = Secret(
            id="test_secret",
            description="Has a family member working for the government",
            secret_type=SecretType.PERSONAL,
            impact=-0.3,
            emotional_weight=0.8,
        )
        agent_a.add_secret(secret)

        # Generate advanced narrative
        narrative = narrative_engine.generate_advanced_narrative(agent_a, agent_b)
        assert narrative is not None
        assert len(narrative) > 0
        assert agent_a.name in narrative
        assert agent_b.name in narrative

    def test_secret_requirement_checking(self, narrative_engine, game_state):
        """Test secret requirement checking in narrative templates"""
        agent_ids = list(game_state.agents.keys())[:2]
        agent_a = game_state.agents[agent_ids[0]]
        agent_b = game_state.agents[agent_ids[1]]

        # Find a template that requires secrets
        secret_template = None
        for template in narrative_engine.templates:
            if template.requires_secret:
                secret_template = template
                break

        assert secret_template is not None

        # Check without secret - should fail
        has_secret = narrative_engine._check_secret_requirement(
            secret_template, agent_a, agent_b
        )
        assert not has_secret

        # Add secret and check again - should pass
        secret = Secret(
            id="test_secret",
            description="Test secret",
            secret_type=SecretType.PERSONAL,
            impact=-0.3,
            emotional_weight=0.8,
        )
        agent_a.add_secret(secret)

        has_secret = narrative_engine._check_secret_requirement(
            secret_template, agent_a, agent_b
        )
        assert has_secret

    def test_memory_requirement_checking(self, narrative_engine, game_state):
        """Test memory requirement checking in narrative templates"""
        agent_ids = list(game_state.agents.keys())[:2]
        agent_a = game_state.agents[agent_ids[0]]
        agent_b = game_state.agents[agent_ids[1]]

        # Find a template that requires memories
        memory_template = None
        for template in narrative_engine.templates:
            if template.requires_memory:
                memory_template = template
                break

        assert memory_template is not None

        # Check without memory - should fail
        has_memory = narrative_engine._check_memory_requirement(
            memory_template, agent_a, agent_b
        )
        assert not has_memory

        # Add memory and check again - should pass
        memory = MemoryEntry(
            id="test_memory",
            summary="Test memory",
            emotional_tone="grateful",
            agent_involved=agent_b.id,
            impact_score=0.5,
        )
        agent_a.add_memory(memory)

        has_memory = narrative_engine._check_memory_requirement(
            memory_template, agent_a, agent_b
        )
        assert has_memory

    def test_persona_requirement_checking(self, narrative_engine, game_state):
        """Test persona requirement checking in narrative templates"""
        agent_ids = list(game_state.agents.keys())[:2]
        agent_a = game_state.agents[agent_ids[0]]
        agent_b = game_state.agents[agent_ids[1]]

        # Find a template that requires persona masks
        persona_template = None
        for template in narrative_engine.templates:
            if template.requires_persona:
                persona_template = template
                break

        assert persona_template is not None

        # Check without persona - should fail
        has_persona = narrative_engine._check_persona_requirement(agent_a, agent_b)
        assert not has_persona

        # Add persona mask and check again - should pass
        masked_relationship = Relationship(
            agent_id=agent_b.id, affinity=50, trust=0.8, loyalty=0.9
        )
        agent_a.set_persona_mask(agent_b.id, masked_relationship)

        has_persona = narrative_engine._check_persona_requirement(agent_a, agent_b)
        assert has_persona

    def test_ideology_conflict_checking(self, narrative_engine, game_state):
        """Test ideology conflict checking in narrative templates"""
        agent_ids = list(game_state.agents.keys())[:2]
        agent_a = game_state.agents[agent_ids[0]]
        agent_b = game_state.agents[agent_ids[1]]

        # Find a template that requires ideology conflicts
        ideology_template = None
        for template in narrative_engine.templates:
            if template.requires_ideology_conflict:
                ideology_template = template
                break

        assert ideology_template is not None

        # Set similar ideologies - should fail
        agent_a.ideology_vector = {"radical": 0.5, "pacifist": 0.5}
        agent_b.ideology_vector = {"radical": 0.6, "pacifist": 0.4}

        has_conflict = narrative_engine._check_ideology_conflict(agent_a, agent_b)
        assert not has_conflict

        # Set very different ideologies - should pass
        agent_a.ideology_vector = {"radical": 0.9, "pacifist": 0.1}
        agent_b.ideology_vector = {"radical": 0.1, "pacifist": 0.9}

        has_conflict = narrative_engine._check_ideology_conflict(agent_a, agent_b)
        assert has_conflict
