"""
Tests for enhanced mission flows integration.
"""

import unittest
from unittest.mock import patch

# Import the game components we'll test
from src.game.core import GameState
from src.game.entities import Agent, Mission, MissionType


class TestEnhancedMissionFlows(unittest.TestCase):
    """Test cases for enhanced mission flows integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.game_state = GameState()

        # Create test agents
        self.agent1 = Agent(
            id="agent1",
            name="Test Agent 1",
            skills={"stealth": 75, "combat": 60},
            stress=30,
            faction_id="resistance",
            location_id="safehouse",
        )
        self.agent2 = Agent(
            id="agent2",
            name="Test Agent 2",
            skills={"stealth": 85, "persuasion": 70},
            stress=20,
            faction_id="resistance",
            location_id="safehouse",
        )

        # Add agents to game state
        self.game_state.agents = {
            self.agent1.id: self.agent1,
            self.agent2.id: self.agent2,
        }

        # Create test mission
        self.mission = Mission(
            id="test_mission",
            mission_type=MissionType.INTELLIGENCE,
            target_location_id="test_location",
            faction_id="resistance",
        )

        # Initialize current_missions list for agents
        if not hasattr(self.agent1, "current_missions"):
            self.agent1.current_missions = []
        if not hasattr(self.agent2, "current_missions"):
            self.agent2.current_missions = []

    def test_mission_execution_flow(self):
        """Test that mission execution flows through the enhanced system."""
        # Mock the execute_enhanced_mission function
        with patch(
            "src.game.mission_flow_integration.execute_enhanced_mission"
        ) as mock_execute:
            # Set up mock return value
            mock_execute.return_value = {
                "success": True,
                "description": "Test mission completed successfully",
                "casualties": 0,
                "stress_changes": {"agent1": -5, "agent2": -5},
            }

            # Execute the mission
            outcome = self.game_state._execute_mission_with_emotions(
                self.mission, [self.agent1, self.agent2]
            )

            # Verify the enhanced mission system was called
            mock_execute.assert_called_once_with(
                self.game_state, self.mission, [self.agent1, self.agent2]
            )

            # Verify the outcome
            self.assertTrue(outcome["success"])
            self.assertEqual(
                outcome["description"], "Test mission completed successfully"
            )

            # Verify agent states were updated
            # Note: current_missions is cleared after mission execution
            self.assertNotIn(
                self.mission.id, getattr(self.agent1, "current_missions", [])
            )
            self.assertNotIn(
                self.mission.id, getattr(self.agent2, "current_missions", [])
            )

    def test_fallback_to_basic_mission(self):
        """Test that the system falls back to basic mission resolution if enhanced flow fails."""
        # Make execute_enhanced_mission raise an exception
        with patch(
            "src.game.mission_flow_integration.execute_enhanced_mission",
            side_effect=Exception("Test error"),
        ):
            # Execute the mission
            with self.assertLogs(level="ERROR") as log:
                outcome = self.game_state._execute_mission_with_emotions(
                    self.mission, [self.agent1, self.agent2]
                )

                # Verify error was logged
                self.assertIn("Error in enhanced mission flow", log.output[0])

            # Verify we got a basic outcome
            self.assertIn("success", outcome)
            self.assertIn("description", outcome)
            self.assertIn("casualties", outcome)

    def test_mission_with_missing_outcome_fields(self):
        """Test that missing outcome fields are handled gracefully."""
        # Mock the execute_enhanced_mission function to return minimal data
        with patch(
            "src.game.mission_flow_integration.execute_enhanced_mission"
        ) as mock_execute:
            mock_execute.return_value = {"success": True}  # Missing description

            # Execute the mission
            outcome = self.game_state._execute_mission_with_emotions(
                self.mission, [self.agent1]
            )

            # Verify default values were filled in
            self.assertTrue(outcome["success"])
            self.assertIn("description", outcome)
            self.assertEqual(outcome["casualties"], 0)

            # Verify stress was updated with default values
            self.assertEqual(self.agent1.stress, 25)  # 30 - 5 for success


if __name__ == "__main__":
    unittest.main()
