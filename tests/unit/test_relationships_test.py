"""
Unit tests for the dynamic relationships and social network system
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from game.relationships import Relationship, BondType, EventType, SocialNetwork
from game.core import Agent, GameState
from game.narrative_engine import NarrativeEngine, NarrativeTemplate


class TestRelationship(unittest.TestCase):
    """Test the Relationship class"""

    def setUp(self):
        """Set up test fixtures"""
        self.relationship = Relationship(
            agent_id="agent_b",
            bond_type=BondType.NEUTRAL,  # Use neutral to avoid random initialization
            affinity=50.0,
            trust=0.8,
            loyalty=0.9,
        )

    def test_relationship_initialization(self):
        """Test relationship initialization with different bond types"""
        # Test ally relationship
        ally_rel = Relationship(agent_id="test", bond_type=BondType.ALLY)
        self.assertGreater(ally_rel.affinity, 0)
        self.assertGreater(ally_rel.trust, 0.5)
        self.assertGreater(ally_rel.loyalty, 0.5)

        # Test rival relationship
        rival_rel = Relationship(agent_id="test", bond_type=BondType.RIVAL)
        self.assertLess(rival_rel.affinity, 0)
        self.assertLess(rival_rel.trust, 0.5)
        self.assertLess(rival_rel.loyalty, 0.5)

        # Test mentor relationship
        mentor_rel = Relationship(agent_id="test", bond_type=BondType.MENTOR)
        self.assertGreater(mentor_rel.affinity, 20)
        self.assertGreater(mentor_rel.trust, 0.6)
        self.assertGreater(mentor_rel.loyalty, 0.7)

    def test_update_from_event(self):
        """Test relationship updates from events"""
        initial_affinity = self.relationship.affinity
        initial_trust = self.relationship.trust

        # Test positive event
        self.relationship.update_from_event(EventType.SHARED_RISK, magnitude=1.0)
        self.assertGreater(self.relationship.affinity, initial_affinity)
        self.assertGreater(self.relationship.trust, initial_trust)

        # Test negative event
        self.relationship.update_from_event(EventType.BETRAYAL, magnitude=1.0)
        self.assertLess(self.relationship.affinity, initial_affinity + 10)
        self.assertLess(self.relationship.trust, initial_trust + 0.05)

    def test_apply_decay(self):
        """Test relationship decay over time"""
        initial_affinity = self.relationship.affinity
        initial_trust = self.relationship.trust

        self.relationship.apply_decay()

        # Affinity should decay towards neutral
        if initial_affinity > 0:
            self.assertLess(self.relationship.affinity, initial_affinity)

        # Trust should decay slightly
        self.assertLess(self.relationship.trust, initial_trust)

    def test_get_strength(self):
        """Test relationship strength calculation"""
        strength = self.relationship.get_strength()

        # Strength should be between 0 and 1
        self.assertGreaterEqual(strength, 0.0)
        self.assertLessEqual(strength, 1.0)

        # Strong relationships should have higher strength
        strong_rel = Relationship(agent_id="test", bond_type=BondType.FAMILY)
        weak_rel = Relationship(agent_id="test", bond_type=BondType.ENEMY)

        self.assertGreater(strong_rel.get_strength(), weak_rel.get_strength())

    def test_is_positive_negative(self):
        """Test positive/negative relationship detection"""
        # Test positive relationship
        positive_rel = Relationship(agent_id="test", bond_type=BondType.ALLY)
        self.assertTrue(positive_rel.is_positive())
        self.assertFalse(positive_rel.is_negative())

        # Test negative relationship
        negative_rel = Relationship(agent_id="test", bond_type=BondType.ENEMY)
        self.assertFalse(negative_rel.is_positive())
        self.assertTrue(negative_rel.is_negative())

        # Test neutral relationship
        neutral_rel = Relationship(agent_id="test", bond_type=BondType.NEUTRAL)
        self.assertFalse(neutral_rel.is_positive())
        self.assertFalse(neutral_rel.is_negative())

    def test_serialization(self):
        """Test relationship serialization and deserialization"""
        # Serialize
        data = self.relationship.as_dict()

        # Check all fields are present
        self.assertIn("agent_id", data)
        self.assertIn("bond_type", data)
        self.assertIn("affinity", data)
        self.assertIn("trust", data)
        self.assertIn("loyalty", data)

        # Deserialize
        restored_rel = Relationship.from_dict(data)

        # Check values match (using approximate equality for floating point)
        self.assertEqual(restored_rel.agent_id, self.relationship.agent_id)
        self.assertEqual(restored_rel.bond_type, self.relationship.bond_type)
        self.assertAlmostEqual(
            restored_rel.affinity, self.relationship.affinity, places=5
        )
        self.assertAlmostEqual(restored_rel.trust, self.relationship.trust, places=5)
        self.assertAlmostEqual(
            restored_rel.loyalty, self.relationship.loyalty, places=5
        )


class TestSocialNetwork(unittest.TestCase):
    """Test the SocialNetwork class"""

    def setUp(self):
        """Set up test fixtures"""
        self.network = SocialNetwork()

        # Create test relationships
        self.rel1 = Relationship(
            agent_id="agent_b", bond_type=BondType.ALLY, affinity=50
        )
        self.rel2 = Relationship(
            agent_id="agent_c", bond_type=BondType.RIVAL, affinity=-30
        )

    def test_add_relationship(self):
        """Test adding relationships to the network"""
        self.network.add_relationship("agent_a", "agent_b", self.rel1)

        # Check relationship was added
        self.assertIn("agent_a", self.network.relationships)
        self.assertIn("agent_b", self.network.relationships["agent_a"])

        # Check reverse relationship was created
        self.assertIn("agent_b", self.network.relationships)
        self.assertIn("agent_a", self.network.relationships["agent_b"])

    def test_get_relationship(self):
        """Test retrieving relationships"""
        self.network.add_relationship("agent_a", "agent_b", self.rel1)

        # Get relationship
        rel = self.network.get_relationship("agent_a", "agent_b")
        self.assertIsNotNone(rel)
        self.assertEqual(rel.agent_id, "agent_b")

        # Get non-existent relationship
        rel = self.network.get_relationship("agent_a", "agent_c")
        self.assertIsNone(rel)

    def test_update_relationship(self):
        """Test updating existing relationships"""
        self.network.add_relationship("agent_a", "agent_b", self.rel1)

        # Get initial values
        initial_rel = self.network.get_relationship("agent_a", "agent_b")
        initial_affinity = initial_rel.affinity
        initial_trust = initial_rel.trust

        # Update relationship
        self.network.update_relationship(
            "agent_a", "agent_b", delta_affinity=10, delta_trust=0.1
        )

        # Check updates were applied
        rel = self.network.get_relationship("agent_a", "agent_b")
        self.assertAlmostEqual(rel.affinity, initial_affinity + 10, places=5)
        self.assertAlmostEqual(rel.trust, initial_trust + 0.1, places=5)

    def test_get_social_circle(self):
        """Test getting an agent's social circle"""
        self.network.add_relationship("agent_a", "agent_b", self.rel1)
        self.network.add_relationship("agent_a", "agent_c", self.rel2)

        # Get all relationships
        circle = self.network.get_social_circle("agent_a")
        self.assertEqual(len(circle), 2)

        # Get only positive relationships
        positive_circle = self.network.get_social_circle("agent_a", min_affinity=0)
        self.assertEqual(len(positive_circle), 1)
        self.assertEqual(positive_circle[0][0], "agent_b")

        # Get only allies
        ally_circle = self.network.get_social_circle(
            "agent_a", bond_filter=BondType.ALLY
        )
        self.assertEqual(len(ally_circle), 1)
        self.assertEqual(ally_circle[0][0], "agent_b")

    def test_get_most_influential(self):
        """Test finding most influential agents"""
        # Create a more complex network
        self.network.add_relationship("agent_a", "agent_b", self.rel1)
        self.network.add_relationship("agent_b", "agent_c", self.rel1)
        self.network.add_relationship("agent_c", "agent_d", self.rel1)

        # Get influential agents within radius 2
        influential = self.network.get_most_influential("agent_a", radius=2)

        # Should find agents within radius
        self.assertGreater(len(influential), 0)

        # Check all returned agents are within radius
        for agent_id, influence in influential:
            self.assertIn(agent_id, ["agent_b", "agent_c"])

    def test_propagate_morale_effect(self):
        """Test morale effect propagation through network"""
        # Create a chain of positive relationships
        self.network.add_relationship("agent_a", "agent_b", self.rel1)
        self.network.add_relationship("agent_b", "agent_c", self.rel1)

        # Get initial values
        initial_rel_ab = self.network.get_relationship("agent_a", "agent_b")
        initial_rel_bc = self.network.get_relationship("agent_b", "agent_c")
        initial_affinity_ab = initial_rel_ab.affinity
        initial_affinity_bc = initial_rel_bc.affinity

        # Propagate morale effect
        self.network.propagate_morale_effect("agent_a", 10.0, max_propagation=2)

        # Check that relationships were affected
        rel_ab = self.network.get_relationship("agent_a", "agent_b")
        rel_bc = self.network.get_relationship("agent_b", "agent_c")

        # Effects should be positive for positive relationships
        self.assertGreater(rel_ab.affinity, initial_affinity_ab)
        self.assertGreater(rel_bc.affinity, initial_affinity_bc)

    def test_decay_all_relationships(self):
        """Test relationship decay across the network"""
        self.network.add_relationship("agent_a", "agent_b", self.rel1)

        initial_affinity = self.rel1.affinity
        initial_trust = self.rel1.trust

        # Apply decay
        self.network.decay_all_relationships()

        # Check relationships decayed
        rel = self.network.get_relationship("agent_a", "agent_b")
        self.assertLess(rel.affinity, initial_affinity)
        self.assertLess(rel.trust, initial_trust)

    def test_get_social_clusters(self):
        """Test social cluster identification"""
        # Create two separate clusters
        self.network.add_relationship("agent_a", "agent_b", self.rel1)
        self.network.add_relationship("agent_b", "agent_c", self.rel1)

        # Separate cluster
        rel3 = Relationship(agent_id="agent_e", bond_type=BondType.ALLY, affinity=40)
        self.network.add_relationship("agent_d", "agent_e", rel3)

        clusters = self.network.get_social_clusters()

        # Should find clusters
        self.assertGreater(len(clusters), 0)

        # Check cluster sizes
        for cluster_id, cluster in clusters.items():
            self.assertGreater(len(cluster), 1)  # No singleton clusters

    def test_get_faction_cohesion_index(self):
        """Test faction cohesion calculation"""
        # Create faction with strong internal relationships
        self.network.add_relationship("agent_a", "agent_b", self.rel1)
        self.network.add_relationship("agent_b", "agent_c", self.rel1)

        faction_agents = ["agent_a", "agent_b", "agent_c"]
        cohesion = self.network.get_faction_cohesion_index(faction_agents)

        # Cohesion should be positive for positive relationships
        self.assertGreater(cohesion, 0.0)
        self.assertLessEqual(cohesion, 1.0)

        # Empty faction should have zero cohesion
        empty_cohesion = self.network.get_faction_cohesion_index([])
        self.assertEqual(empty_cohesion, 0.0)

    def test_serialization(self):
        """Test social network serialization and deserialization"""
        # Add some relationships
        self.network.add_relationship("agent_a", "agent_b", self.rel1)

        # Serialize
        data = self.network.serialize()

        # Check data structure
        self.assertIn("relationships", data)
        self.assertIn("social_clusters", data)
        self.assertIn("influence_cache", data)

        # Deserialize
        restored_network = SocialNetwork.deserialize(data)

        # Check relationships were restored
        rel = restored_network.get_relationship("agent_a", "agent_b")
        self.assertIsNotNone(rel)
        self.assertEqual(rel.agent_id, "agent_b")


class TestAgentRelationships(unittest.TestCase):
    """Test Agent class relationship functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.agent = Agent(
            id="agent_a",
            name="Test Agent",
            faction_id="resistance",
            location_id="safehouse",
            background="veteran",
        )

        self.other_agent = Agent(
            id="agent_b",
            name="Other Agent",
            faction_id="resistance",
            location_id="safehouse",
            background="student",
        )

    def test_agent_initialization_with_relationships(self):
        """Test agent initialization includes relationships and social tags"""
        self.assertIsInstance(self.agent.relationships, dict)
        self.assertIsInstance(self.agent.social_tags, set)

        # Check social tags were initialized based on background
        self.assertIn("experienced", self.agent.social_tags)
        self.assertIn("disciplined", self.agent.social_tags)
        self.assertIn("trauma", self.agent.social_tags)
        self.assertIn("military", self.agent.social_tags)

    def test_relationship_management(self):
        """Test agent relationship management methods"""
        relationship = Relationship(agent_id="agent_b", bond_type=BondType.ALLY)

        # Update relationship
        self.agent.update_relationship("agent_b", relationship)

        # Get relationship
        retrieved_rel = self.agent.get_relationship("agent_b")
        self.assertIsNotNone(retrieved_rel)
        self.assertEqual(retrieved_rel.agent_id, "agent_b")

    def test_get_closest_allies(self):
        """Test finding closest allies"""
        # Add some relationships
        ally_rel = Relationship(
            agent_id="agent_b", bond_type=BondType.ALLY, affinity=50
        )
        enemy_rel = Relationship(
            agent_id="agent_c", bond_type=BondType.ENEMY, affinity=-30
        )

        self.agent.update_relationship("agent_b", ally_rel)
        self.agent.update_relationship("agent_c", enemy_rel)

        # Get allies
        allies = self.agent.get_closest_allies(min_affinity=20)

        # Should only find positive relationships above threshold
        self.assertEqual(len(allies), 1)
        self.assertEqual(allies[0][0], "agent_b")

    def test_get_enemies(self):
        """Test finding enemies"""
        # Add some relationships
        ally_rel = Relationship(
            agent_id="agent_b", bond_type=BondType.ALLY, affinity=50
        )
        enemy_rel = Relationship(
            agent_id="agent_c", bond_type=BondType.ENEMY, affinity=-30
        )

        self.agent.update_relationship("agent_b", ally_rel)
        self.agent.update_relationship("agent_c", enemy_rel)

        # Get enemies
        enemies = self.agent.get_enemies(max_affinity=-20)

        # Should find negative relationships
        self.assertEqual(len(enemies), 1)
        self.assertEqual(enemies[0][0], "agent_c")

    def test_agent_serialization_with_relationships(self):
        """Test agent serialization includes relationships"""
        relationship = Relationship(agent_id="agent_b", bond_type=BondType.ALLY)
        self.agent.update_relationship("agent_b", relationship)

        # Serialize
        data = self.agent.serialize()

        # Check relationships are included
        self.assertIn("relationships", data)
        self.assertIn("social_tags", data)

        # Deserialize
        restored_agent = Agent.deserialize(data)

        # Check relationships were restored
        self.assertIn("agent_b", restored_agent.relationships)
        self.assertEqual(restored_agent.relationships["agent_b"].agent_id, "agent_b")


class TestGameStateRelationships(unittest.TestCase):
    """Test GameState relationship integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.game_state = GameState()
        self.game_state.initialize_game()

    def test_game_state_initialization_with_relationships(self):
        """Test game state includes social network"""
        self.assertIsNotNone(self.game_state.social_network)
        self.assertIsInstance(self.game_state.social_network, SocialNetwork)

    def test_relationship_initialization(self):
        """Test initial relationships are created"""
        # Check that some relationships exist
        self.assertGreater(len(self.game_state.social_network.relationships), 0)

        # Check specific relationships were created
        maria_sofia = self.game_state.social_network.get_relationship(
            "agent_maria", "agent_sofia"
        )
        self.assertIsNotNone(maria_sofia)
        self.assertEqual(maria_sofia.bond_type, BondType.ALLY)

    def test_relationship_updates(self):
        """Test relationship updates through game state"""
        # Get initial relationship values
        initial_rel = self.game_state.social_network.get_relationship(
            "agent_maria", "agent_sofia"
        )
        initial_affinity = initial_rel.affinity
        initial_trust = initial_rel.trust

        # Update relationship
        self.game_state.update_relationship(
            "agent_maria", "agent_sofia", delta_affinity=10, delta_trust=0.1
        )

        # Check update was applied
        rel = self.game_state.social_network.get_relationship(
            "agent_maria", "agent_sofia"
        )
        self.assertAlmostEqual(rel.affinity, initial_affinity + 10, places=5)
        self.assertAlmostEqual(rel.trust, initial_trust + 0.1, places=5)

    def test_social_circle_queries(self):
        """Test social circle queries"""
        # Get Maria's social circle
        circle = self.game_state.get_social_circle("agent_maria")
        self.assertGreater(len(circle), 0)

        # Get only allies
        allies = self.game_state.get_social_circle(
            "agent_maria", bond_filter=BondType.ALLY
        )
        for agent_id, rel in allies:
            self.assertEqual(rel.bond_type, BondType.ALLY)

    def test_faction_cohesion(self):
        """Test faction cohesion calculation"""
        # Get cohesion for a faction
        cohesion = self.game_state.get_faction_cohesion("resistance")

        # Cohesion should be a valid value
        self.assertGreaterEqual(cohesion, 0.0)
        self.assertLessEqual(cohesion, 1.0)

    def test_relationship_events_during_turn(self):
        """Test relationship events are processed during game turns"""
        initial_narrative_length = len(self.game_state.recent_narrative)

        # Advance turn to trigger relationship events
        self.game_state.advance_turn()

        # Should have new narrative entries
        self.assertGreater(
            len(self.game_state.recent_narrative), initial_narrative_length
        )

    def test_relationship_decay_during_turn(self):
        """Test relationships decay during resolution phase"""
        # Get initial relationship values
        rel = self.game_state.social_network.get_relationship(
            "agent_maria", "agent_sofia"
        )
        initial_affinity = rel.affinity
        initial_trust = rel.trust

        # Complete a full turn cycle to trigger decay
        self.game_state.advance_turn()  # Planning -> Action
        self.game_state.advance_turn()  # Action -> Resolution (decay happens)

        # Check relationship values changed (either through decay or other events)
        rel = self.game_state.social_network.get_relationship(
            "agent_maria", "agent_sofia"
        )
        # Values should have changed due to game events, even if decay is small
        self.assertTrue(
            abs(rel.affinity - initial_affinity) > 0.001
            or abs(rel.trust - initial_trust) > 0.001,
            "Relationship values should change during game turns",
        )


class TestNarrativeEngine(unittest.TestCase):
    """Test the narrative engine integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.game_state = GameState()
        self.game_state.initialize_game()
        self.narrative_engine = NarrativeEngine(self.game_state)

    def test_narrative_engine_initialization(self):
        """Test narrative engine initialization"""
        self.assertIsNotNone(self.narrative_engine.templates)
        self.assertGreater(len(self.narrative_engine.templates), 0)

    def test_template_matching(self):
        """Test template matching logic"""
        agent_a = self.game_state.agents["agent_maria"]
        agent_b = self.game_state.agents["agent_sofia"]
        relationship = self.game_state.social_network.get_relationship(
            "agent_maria", "agent_sofia"
        )

        # Find matching template
        template = self.narrative_engine._find_matching_template(
            agent_a, agent_b, relationship, {}
        )

        # Should find a template for ally relationship
        self.assertIsNotNone(template)

    def test_relationship_narrative_generation(self):
        """Test relationship narrative generation"""
        agent_a = self.game_state.agents["agent_maria"]
        agent_b = self.game_state.agents["agent_sofia"]

        # Generate narrative
        narrative = self.narrative_engine.apply_relationship_effects(
            agent_a, agent_b, {"type": "cooperation"}
        )

        # Should generate narrative
        self.assertIsInstance(narrative, str)
        self.assertGreater(len(narrative), 0)

    def test_template_statistics(self):
        """Test template statistics"""
        stats = self.narrative_engine.get_template_statistics()

        # Check statistics structure
        self.assertIn("total_templates", stats)
        self.assertIn("templates_by_complexity", stats)
        self.assertIn("templates_by_emotional_tone", stats)
        self.assertIn("templates_by_bond_type", stats)

        # Check values are reasonable
        self.assertGreater(stats["total_templates"], 0)
        self.assertGreater(len(stats["templates_by_complexity"]), 0)

    def test_custom_template_addition(self):
        """Test adding custom templates"""
        initial_count = len(self.narrative_engine.templates)

        # Add custom template
        custom_template = NarrativeTemplate(
            id="custom_test",
            title="Custom Test",
            template="Custom narrative for {agent_a.name} and {agent_b.name}",
            emotional_tone="test",
        )

        self.narrative_engine.add_custom_template(custom_template)

        # Check template was added
        self.assertEqual(len(self.narrative_engine.templates), initial_count + 1)

        # Check template can be found
        templates = self.narrative_engine.generate_relationship_templates(
            emotional_tone="test"
        )
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].id, "custom_test")


if __name__ == "__main__":
    # Run the tests
    unittest.main()
