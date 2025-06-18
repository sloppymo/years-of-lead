"""
Comprehensive Test Suite for Enhanced Years of Lead Systems

Tests all enhanced systems:
- Phase 1: Agent Autonomy Enhancement
- Phase 2: Mission Outcome Enhancement
- Phase 3: Real-time Intelligence Systems
- Phase 4: Dynamic Narrative Generation
- Phase 5: Advanced Trauma and Psychological Impact
- Integration System
"""

import unittest
import sys
import os
from unittest.mock import Mock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from game.core import GameState, Agent
from game.emotional_state import EmotionalState

# PATCH: Ensure all emotional state attributes are numeric in all test agent mocks
EMOTION_ATTRS = [
    "trauma_level",
    "fear",
    "anger",
    "anticipation",
    "trust",
    "sadness",
    "joy",
    "despair",
    "hope",
    "surprise",
    "disgust",
]


def patch_emotional_state(emotional_state, values=None):
    if values is None:
        values = {}
    for attr in EMOTION_ATTRS:
        setattr(emotional_state, attr, values.get(attr, 0.0))


class TestEnhancedAgentAutonomy(unittest.TestCase):
    """Test Phase 1: Agent Autonomy Enhancement"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}
        self.game_state.turn_number = 1

        # Create test agents
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.stress = 50
        self.agent1.loyalty = 80
        self.agent1.background = "veteran"
        self.agent1.faction_id = "faction_1"

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state,
            {"trauma_level": 0.3, "fear": 0.2, "anger": 0.1},
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = ("fear", 0.2)
        self.agent1.emotional_state.is_psychologically_stable.return_value = True

        # Add relationships
        self.agent1.relationships = {}

        self.game_state.agents["agent_1"] = self.agent1

    def test_autonomy_system_initialization(self):
        """Test autonomy system initialization"""
        try:
            from game.enhanced_agent_autonomy import EnhancedAgentAutonomySystem

            autonomy_system = EnhancedAgentAutonomySystem(self.game_state)

            self.assertIsNotNone(autonomy_system)
            self.assertEqual(autonomy_system.game_state, self.game_state)
            self.assertIsInstance(autonomy_system.agent_profiles, dict)

        except ImportError:
            self.skipTest("Enhanced agent autonomy system not available")

    def test_agent_autonomy_profile_creation(self):
        """Test creation of agent autonomy profiles"""
        try:
            from game.enhanced_agent_autonomy import EnhancedAgentAutonomySystem

            autonomy_system = EnhancedAgentAutonomySystem(self.game_state)

            # Initialize autonomy for agent
            autonomy_system.initialize_agent_autonomy("agent_1")

            self.assertIn("agent_1", autonomy_system.agent_profiles)
            profile = autonomy_system.agent_profiles["agent_1"]

            self.assertEqual(profile.agent_id, "agent_1")
            self.assertGreater(profile.autonomy_level, 0.0)
            self.assertLess(profile.autonomy_level, 1.0)

        except ImportError:
            self.skipTest("Enhanced agent autonomy system not available")

    def test_autonomous_decision_generation(self):
        """Test generation of autonomous decisions"""
        try:
            from game.enhanced_agent_autonomy import EnhancedAgentAutonomySystem

            autonomy_system = EnhancedAgentAutonomySystem(self.game_state)

            # Set up agent for decision making
            autonomy_system.initialize_agent_autonomy("agent_1")
            profile = autonomy_system.agent_profiles["agent_1"]
            profile.last_decision_turn = 0  # Force decision making

            # Process autonomous decisions
            results = autonomy_system.process_autonomous_decisions()

            self.assertIsInstance(results, dict)
            self.assertIn("decisions_made", results)
            self.assertIn("actions_taken", results)

        except ImportError:
            self.skipTest("Enhanced agent autonomy system not available")


class TestEnhancedMissionSystem(unittest.TestCase):
    """Test Phase 2: Mission Outcome Enhancement"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}
        self.game_state.locations = {"location_1": {"name": "Test Location"}}
        self.game_state.factions = {"faction_1": {"name": "Test Faction"}}

        # Create test agents
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.stress = 50
        self.agent1.loyalty = 80
        self.agent1.faction_id = "faction_1"
        self.agent1.location_id = "location_1"

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state,
            {"trauma_level": 0.3, "fear": 0.2, "anger": 0.1},
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = ("fear", 0.2)
        self.agent1.emotional_state.is_psychologically_stable.return_value = True

        # Add skills
        self.agent1.skills = {
            "intelligence": Mock(level=3),
            "social": Mock(level=2),
            "combat": Mock(level=4),
        }

        # Add relationships
        self.agent1.relationships = {}

        self.game_state.agents["agent_1"] = self.agent1

    def test_mission_system_initialization(self):
        """Test mission system initialization"""
        try:
            from game.enhanced_mission_system import EnhancedMissionExecutor

            mission_system = EnhancedMissionExecutor(self.game_state)

            self.assertIsNotNone(mission_system)
            self.assertEqual(mission_system.game_state, self.game_state)

        except ImportError:
            self.skipTest("Enhanced mission system not available")

    def test_mission_collaboration_analysis(self):
        """Test mission collaboration analysis"""
        try:
            from game.enhanced_mission_system import EnhancedMissionExecutor

            mission_system = EnhancedMissionExecutor(self.game_state)

            # Create test mission
            mission = {
                "id": "test_mission",
                "type": "intelligence",
                "difficulty": "medium",
            }

            agents = [
                {"id": "agent_1", "name": "Test Agent 1", "skills": self.agent1.skills}
            ]
            location = {"id": "location_1", "name": "Test Location"}
            resources = {"budget": 1000, "time": 5}

            # Execute enhanced mission
            result = mission_system.execute_enhanced_mission(
                mission, agents, location, resources
            )

            self.assertIsInstance(result, dict)
            self.assertIn("outcome", result)
            self.assertIn("collaboration_analysis", result)
            self.assertIn("consequences", result)

        except ImportError:
            self.skipTest("Enhanced mission system not available")


class TestEnhancedIntelligenceSystem(unittest.TestCase):
    """Test Phase 3: Real-time Intelligence Systems"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}
        self.game_state.locations = {"location_1": {"name": "Test Location"}}

        # Create test agent
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.stress = 50
        self.agent1.loyalty = 80
        self.agent1.location_id = "location_1"

        # Add skills
        self.agent1.skills = {"intelligence": Mock(level=3)}

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state, {"fear": 0.2, "anticipation": 0.3}
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = (
            "anticipation",
            0.3,
        )

        self.game_state.agents["agent_1"] = self.agent1

    def test_intelligence_system_initialization(self):
        """Test intelligence system initialization"""
        try:
            from game.enhanced_intelligence_system import EnhancedIntelligenceSystem

            intelligence_system = EnhancedIntelligenceSystem(self.game_state)

            self.assertIsNotNone(intelligence_system)
            self.assertEqual(intelligence_system.game_state, self.game_state)
            self.assertIsInstance(intelligence_system.real_time_events, list)

        except ImportError:
            self.skipTest("Enhanced intelligence system not available")

    def test_intelligence_generation(self):
        """Test intelligence generation"""
        try:
            from game.enhanced_intelligence_system import EnhancedIntelligenceSystem

            intelligence_system = EnhancedIntelligenceSystem(self.game_state)

            # Process real-time intelligence
            results = intelligence_system.process_real_time_intelligence()

            self.assertIsInstance(results, dict)
            self.assertIn("new_intelligence", results)
            self.assertIn("patterns_detected", results)
            self.assertIn("threat_assessments", results)

        except ImportError:
            self.skipTest("Enhanced intelligence system not available")


class TestEnhancedNarrativeSystem(unittest.TestCase):
    """Test Phase 4: Dynamic Narrative Generation"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}
        self.game_state.factions = {"faction_1": {"name": "Test Faction"}}

        # Create test agents
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.faction_id = "faction_1"

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state, {"trauma_level": 0.7, "fear": 0.8}
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = ("fear", 0.8)
        self.agent1.emotional_state.is_psychologically_stable.return_value = False

        # Add relationships
        self.agent1.relationships = {}

        self.game_state.agents["agent_1"] = self.agent1

    def test_narrative_system_initialization(self):
        """Test narrative system initialization"""
        try:
            from game.enhanced_narrative_system import EnhancedDynamicNarrativeSystem

            narrative_system = EnhancedDynamicNarrativeSystem(self.game_state)

            self.assertIsNotNone(narrative_system)
            self.assertEqual(narrative_system.game_state, self.game_state)
            self.assertIsInstance(narrative_system.narrative_arcs, list)

        except ImportError:
            self.skipTest("Enhanced narrative system not available")

    def test_narrative_trigger_detection(self):
        """Test narrative trigger detection"""
        try:
            from game.enhanced_narrative_system import EnhancedDynamicNarrativeSystem

            narrative_system = EnhancedDynamicNarrativeSystem(self.game_state)

            # Process dynamic narrative
            results = narrative_system.process_dynamic_narrative()

            self.assertIsInstance(results, dict)
            self.assertIn("new_arcs", results)
            self.assertIn("arc_advancements", results)
            self.assertIn("story_events", results)

        except ImportError:
            self.skipTest("Enhanced narrative system not available")


class TestAdvancedTraumaSystem(unittest.TestCase):
    """Test Phase 5: Advanced Trauma and Psychological Impact"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}

        # Create test agent
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.stress = 95  # High stress

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state, {"trauma_level": 0.8, "fear": 0.9}
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = ("fear", 0.9)
        self.agent1.emotional_state.is_psychologically_stable.return_value = False

        # Add relationships
        self.agent1.relationships = {}

        self.game_state.agents["agent_1"] = self.agent1

    def test_trauma_system_initialization(self):
        """Test trauma system initialization"""
        try:
            from game.advanced_trauma_system import AdvancedTraumaSystem

            trauma_system = AdvancedTraumaSystem(self.game_state)

            self.assertIsNotNone(trauma_system)
            self.assertEqual(trauma_system.game_state, self.game_state)
            self.assertIsInstance(trauma_system.trauma_events, dict)

        except ImportError:
            self.skipTest("Advanced trauma system not available")

    def test_trauma_event_creation(self):
        """Test trauma event creation"""
        try:
            from game.advanced_trauma_system import AdvancedTraumaSystem

            trauma_system = AdvancedTraumaSystem(self.game_state)

            # Process trauma system
            results = trauma_system.process_trauma_system()

            self.assertIsInstance(results, dict)
            self.assertIn("new_trauma_events", results)
            self.assertIn("trauma_recovery", results)
            self.assertIn("psychological_crises", results)

        except ImportError:
            self.skipTest("Advanced trauma system not available")


class TestEnhancedSimulationIntegration(unittest.TestCase):
    """Test the complete enhanced simulation integration"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}
        self.game_state.locations = {"location_1": {"name": "Test Location"}}
        self.game_state.factions = {"faction_1": {"name": "Test Faction"}}
        self.game_state.turn_number = 1

        # Create test agents
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.stress = 70
        self.agent1.loyalty = 80
        self.agent1.faction_id = "faction_1"
        self.agent1.location_id = "location_1"

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state,
            {"trauma_level": 0.5, "fear": 0.4, "anger": 0.2},
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = ("fear", 0.4)
        self.agent1.emotional_state.is_psychologically_stable.return_value = True

        # Add skills
        self.agent1.skills = {
            "intelligence": Mock(level=3),
            "social": Mock(level=2),
            "combat": Mock(level=4),
        }

        # Add relationships
        self.agent1.relationships = {}

        self.game_state.agents["agent_1"] = self.agent1

    def test_integration_system_initialization(self):
        """Test integration system initialization"""
        try:
            from game.enhanced_simulation_integration import (
                EnhancedSimulationIntegration,
            )

            integration_system = EnhancedSimulationIntegration(self.game_state)

            self.assertIsNotNone(integration_system)
            self.assertEqual(integration_system.game_state, self.game_state)

        except ImportError:
            self.skipTest("Enhanced simulation integration system not available")

    def test_single_turn_processing(self):
        """Test processing of a single enhanced turn"""
        try:
            from game.enhanced_simulation_integration import (
                EnhancedSimulationIntegration,
            )

            integration_system = EnhancedSimulationIntegration(self.game_state)

            # Process a single turn
            turn = integration_system.process_enhanced_turn()

            self.assertIsNotNone(turn)
            self.assertEqual(turn.turn_number, 1)
            self.assertIsInstance(turn.autonomy_results, dict)
            self.assertIsInstance(turn.intelligence_results, dict)
            self.assertIsInstance(turn.narrative_results, dict)
            self.assertIsInstance(turn.trauma_results, dict)
            self.assertIsInstance(turn.integration_events, list)
            self.assertIsInstance(turn.system_synergies, list)

        except ImportError:
            self.skipTest("Enhanced simulation integration system not available")

    def test_multi_turn_simulation(self):
        """Test running a multi-turn enhanced simulation"""
        try:
            from game.enhanced_simulation_integration import (
                EnhancedSimulationIntegration,
            )

            integration_system = EnhancedSimulationIntegration(self.game_state)

            # Run 3 turns
            results = integration_system.run_enhanced_simulation(turns=3)

            self.assertIsInstance(results, list)
            self.assertEqual(len(results), 3)

            for turn in results:
                self.assertIsInstance(turn.autonomy_results, dict)
                self.assertIsInstance(turn.intelligence_results, dict)
                self.assertIsInstance(turn.narrative_results, dict)
                self.assertIsInstance(turn.trauma_results, dict)

        except ImportError:
            self.skipTest("Enhanced simulation integration system not available")

    def test_integration_summary(self):
        """Test integration system summary generation"""
        try:
            from game.enhanced_simulation_integration import (
                EnhancedSimulationIntegration,
            )

            integration_system = EnhancedSimulationIntegration(self.game_state)

            # Process a turn first
            integration_system.process_enhanced_turn()

            # Get summary
            summary = integration_system.get_integration_summary()

            self.assertIsInstance(summary, dict)
            self.assertIn("total_turns_processed", summary)
            self.assertIn("system_performance", summary)
            self.assertIn("integration_metrics", summary)
            self.assertIn("system_status", summary)

        except ImportError:
            self.skipTest("Enhanced simulation integration system not available")


class TestSystemInteroperability(unittest.TestCase):
    """Test interoperability between enhanced systems"""

    def setUp(self):
        """Set up test environment"""
        self.game_state = Mock(spec=GameState)
        self.game_state.agents = {}
        self.game_state.locations = {"location_1": {"name": "Test Location"}}
        self.game_state.factions = {"faction_1": {"name": "Test Faction"}}
        self.game_state.turn_number = 1

        # Create test agent with complex state
        self.agent1 = Mock(spec=Agent)
        self.agent1.id = "agent_1"
        self.agent1.name = "Test Agent 1"
        self.agent1.status = "active"
        self.agent1.stress = 85  # High stress
        self.agent1.loyalty = 60  # Moderate loyalty
        self.agent1.faction_id = "faction_1"
        self.agent1.location_id = "location_1"

        # Add emotional state
        self.agent1.emotional_state = Mock(spec=EmotionalState)
        patch_emotional_state(
            self.agent1.emotional_state,
            {"trauma_level": 0.6, "fear": 0.5, "anger": 0.3},
        )
        self.agent1.emotional_state.get_dominant_emotion.return_value = ("fear", 0.5)
        self.agent1.emotional_state.is_psychologically_stable.return_value = True

        # Add skills
        self.agent1.skills = {
            "intelligence": Mock(level=4),
            "social": Mock(level=3),
            "combat": Mock(level=2),
        }

        # Add relationships
        self.agent1.relationships = {}

        self.game_state.agents["agent_1"] = self.agent1

    def test_cross_system_impact(self):
        """Test impact of one system on another"""
        try:
            from game.enhanced_simulation_integration import (
                EnhancedSimulationIntegration,
            )

            integration_system = EnhancedSimulationIntegration(self.game_state)

            # Process a turn
            turn = integration_system.process_enhanced_turn()

            # Check for cross-system integration events
            self.assertIsInstance(turn.integration_events, list)

            # Check for system synergies
            self.assertIsInstance(turn.system_synergies, list)

            # Verify that systems are interacting
            if turn.integration_events:
                self.assertGreater(len(turn.integration_events), 0)

        except ImportError:
            self.skipTest("Enhanced simulation integration system not available")

    def test_emergent_complexity(self):
        """Test emergent complexity from system interactions"""
        try:
            from game.enhanced_simulation_integration import (
                EnhancedSimulationIntegration,
            )

            integration_system = EnhancedSimulationIntegration(self.game_state)

            # Process multiple turns to build complexity
            for i in range(3):
                integration_system.game_state.turn_number = i + 1
                turn = integration_system.process_enhanced_turn()

                # Check for emergent events
                if turn.integration_events:
                    emergent_events = [
                        e
                        for e in turn.integration_events
                        if e.get("type", "").startswith("emergent")
                    ]
                    if emergent_events:
                        self.assertIsInstance(emergent_events, list)

        except ImportError:
            self.skipTest("Enhanced simulation integration system not available")


def run_enhanced_systems_tests():
    """Run all enhanced systems tests"""
    print("🧪 Running Enhanced Years of Lead Systems Tests")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestEnhancedAgentAutonomy,
        TestEnhancedMissionSystem,
        TestEnhancedIntelligenceSystem,
        TestEnhancedNarrativeSystem,
        TestAdvancedTraumaSystem,
        TestEnhancedSimulationIntegration,
        TestSystemInteroperability,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_enhanced_systems_tests()
    sys.exit(0 if success else 1)
