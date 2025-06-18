"""
Years of Lead - Enhanced Player Decision Interface

Interactive CLI interface for mission planning and agent management with support for
multiple missions per turn.
"""

import os
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .entities import Agent, Mission, MissionType
from .core import GameState
from .relationships import evaluate_team_dynamics


class TacticalApproach(Enum):
    """Available tactical approaches for missions"""

    STEALTH = "stealth"
    AGGRESSIVE = "aggressive"
    SOCIAL = "social"
    TECHNICAL = "technical"


@dataclass
class MissionPacket:
    """Complete mission specification from player planning"""

    agents: List[Agent]
    location_id: str
    mission_type: MissionType
    approach: TacticalApproach
    equipment_assignments: Dict[str, List[str]]  # agent_id -> equipment_list
    special_instructions: str = ""
    estimated_duration: int = 4  # hours
    risk_acknowledgment: bool = False


class PlayerInterface:
    """Enhanced CLI interface for player decision-making and mission planning"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.selected_agents: List[Agent] = []
        self.current_mission_packet: Optional[MissionPacket] = None
        self.warnings_acknowledged = False

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("clear" if os.name == "posix" else "cls")

    def display_header(self):
        """Display game header with current turn and phase info"""
        self.clear_screen()
        print("=" * 80)
        print("🎯 YEARS OF LEAD - MISSION COMMAND")
        print("=" * 80)
        print(
            f"Turn: {self.game_state.turn_number} | Phase: {self.game_state.current_phase.value.upper()}"
        )
        print(f"Date: {self.game_state.get_current_date_string()}")
        print("-" * 80)

    def display_faction_status(self):
        """Show critical faction information"""
        total_agents = len(self.game_state.agents)
        available_agents = len(
            [a for a in self.game_state.agents.values() if a.status == "available"]
        )
        broken_agents = len(
            [
                a
                for a in self.game_state.agents.values()
                if hasattr(a, "psychological_state")
                and a.psychological_state == "broken"
            ]
        )

        print("\n📊 FACTION STATUS:")
        print(f"   Resources: {getattr(self.game_state, 'resources', 'N/A')}")
        print(f"   Agents: {available_agents}/{total_agents} available")

        if hasattr(self.game_state, "faction_cohesion"):
            print(f"   Cohesion: {self.game_state.faction_cohesion.unity_score:.0f}%")

        if broken_agents > 0:
            print(f"   ⚠️  {broken_agents} agents need psychological support")

        if (
            hasattr(self.game_state, "faction_cohesion")
            and self.game_state.faction_cohesion.unity_score < 60
        ):
            print("   🚨 FACTION INSTABILITY - Risk of fracture!")

    def display_agent_status(self, agent: Agent, detailed: bool = False) -> str:
        """Display agent status with emotional indicators"""
        # Get dominant emotion for display
        dominant_emotion = max(agent.emotion_state.items(), key=lambda x: x[1])
        emotion_icon = self._get_emotion_icon(dominant_emotion[0])

        # Basic status line
        status_line = f"[{agent.id}] {agent.name} {emotion_icon}"
        status_line += f" | Stress: {getattr(agent, 'stress', 0)}% | Loyalty: {getattr(agent, 'loyalty', 50)}%"

        if detailed:
            status_line += f"\n    Location: {getattr(agent, 'location_id', 'Unknown')}"
            status_line += f" | Background: {getattr(agent, 'background', 'Unknown')}"
            status_line += f"\n    Skills: {', '.join(f'{k}:{v}' for k, v in getattr(agent, 'skills', {}).items() if v > 50)}"
            status_line += f"\n    Status: {getattr(agent, 'status', 'Unknown')}"

            # Show psychological warnings
            warnings = self.get_agent_warnings(agent)
            if warnings:
                status_line += "\n    ⚠️  " + "; ".join(warnings)

        return status_line

    def _get_emotion_icon(self, emotion: str) -> str:
        """Get icon for emotional state"""
        emotion_icons = {
            "hope": "🌟",
            "fear": "😨",
            "anger": "😠",
            "despair": "😔",
            "determination": "💪",
        }
        return emotion_icons.get(emotion, "😐")

    def get_agent_warnings(self, agent: Agent) -> List[str]:
        """Generate psychological and relationship warnings for agent"""
        warnings = []

        # High stress warning
        if getattr(agent, "stress", 0) > 70:
            warnings.append("High stress")

        # Low loyalty warning
        if getattr(agent, "loyalty", 50) < 30:
            warnings.append("Low loyalty")

        # Psychological state warnings
        if hasattr(agent, "psychological_state"):
            if agent.psychological_state == "broken":
                warnings.append("BROKEN - needs recovery")
            elif agent.psychological_state == "unstable":
                warnings.append("Unstable - high risk")

        return warnings

    def display_current_mission_plan(self, missions: List[Tuple[Mission, List[Agent]]]):
        """Display the current mission plan with all planned missions"""
        if not missions:
            print("\n📋 CURRENT MISSION PLAN: No missions planned yet")
            return

        print("\n📋 CURRENT MISSION PLAN:")
        print("-" * 40)
        for i, (mission, agents) in enumerate(missions, 1):
            agent_names = ", ".join(agent.name for agent in agents)
            print(f"{i}. {mission.mission_type.value.upper()}")
            print(f"   Agents: {agent_names}")
            print(f"   Location: {getattr(mission, 'target_location_id', 'Unknown')}")
            print("-" * 40)

    def mission_planning_interface(
        self, current_missions_count: int = 0
    ) -> Optional[Tuple[Mission, List[Agent]]]:
        """
        Enhanced mission planning with relationship awareness and multi-mission support

        Args:
            current_missions_count: Number of missions already planned this turn

        Returns:
            Tuple of (Mission, List[Agent]) if a mission was planned, None otherwise
        """
        self.clear_screen()
        self.display_header()

        # Show current mission plan if any
        if (
            hasattr(self.game_state, "planned_missions")
            and self.game_state.planned_missions
        ):
            self.display_current_mission_plan(self.game_state.planned_missions)

        print("\n🎯 PLAN NEW MISSION")
        print("=" * 40)

        # Show available agents (filter out those already on missions)
        available_agents = [
            agent
            for agent in self.game_state.agents.values()
            if agent.status.value == "active" and not hasattr(agent, "current_mission")
        ]

        if not available_agents:
            print("❌ No agents available for new missions!")
            input("Press Enter to continue...")
            return None

        print("\n📋 AVAILABLE AGENTS (not on missions):")
        for i, agent in enumerate(available_agents):
            print(f"{i+1}. {self.display_agent_status(agent)}")

        # Mission type selection
        print("\n🎯 MISSION TYPES:")
        mission_types = list(MissionType)
        for i, mission_type in enumerate(mission_types):
            print(f"{i+1}. {mission_type.value.upper()}")

        try:
            # Get mission type choice
            mission_choice = input(
                "\nSelect mission type (1-{}, or 'c' to cancel): ".format(
                    len(mission_types)
                )
            )
            if mission_choice.lower() == "c":
                return None

            mission_type = mission_types[int(mission_choice) - 1]

            # Get agent selection
            while True:
                agent_selection = input(
                    "Select agents (comma-separated numbers, e.g., '1,3,5'): "
                )
                try:
                    agent_indices = [
                        int(x.strip()) - 1 for x in agent_selection.split(",")
                    ]
                    selected_agents = [available_agents[i] for i in agent_indices]
                    if not selected_agents:
                        print("❌ Please select at least one agent")
                        continue
                    break
                except (ValueError, IndexError):
                    print(
                        "❌ Invalid selection. Please enter numbers separated by commas."
                    )

            # Check if any selected agent is already on a mission
            busy_agents = [
                agent.name
                for agent in selected_agents
                if hasattr(agent, "current_mission") and agent.current_mission
            ]
            if busy_agents:
                print(f"❌ Error: {', '.join(busy_agents)} are already on a mission!")
                input("Press Enter to continue...")
                return None

            # Team compatibility check
            if len(selected_agents) > 1:
                print(f"\nAnalyzing team of {len(selected_agents)} agents...")

                if not self.display_team_analysis(selected_agents):
                    print(
                        "Mission planning cancelled due to team compatibility issues."
                    )
                    input("Press Enter to continue...")
                    return None

            # Create mission
            mission = Mission(
                id=f"mission_{self.game_state.turn_number}_{mission_type.value}_{current_missions_count}",
                mission_type=mission_type,
                faction_id="resistance",  # Default faction
                target_location_id="university",  # Default location for now
                participants=[agent.id for agent in selected_agents],
                status="planned",
            )

            print(f"\n✅ Mission planned: {mission_type.value.upper()}")
            print(
                f"Assigned agents: {', '.join(agent.name for agent in selected_agents)}"
            )

            confirm = input("\nAdd this mission to the plan? (y/n): ").lower()
            if confirm == "y":
                # Mark agents as assigned to this mission
                for agent in selected_agents:
                    agent.current_mission = mission.id
                return mission, selected_agents

            print("Mission not added to plan.")
            return None

        except (ValueError, IndexError) as e:
            print(f"❌ Invalid selection: {str(e)}. Mission planning cancelled.")
            input("Press Enter to continue...")
            return None
        except KeyboardInterrupt:
            print("\n❌ Mission planning cancelled.")
            return None

    def display_team_analysis(self, agents: List[Agent]) -> bool:
        """Display team analysis and get confirmation"""
        print("\n🔍 TEAM ANALYSIS:")
        print("-" * 40)

        # Calculate team compatibility
        team_dynamics = evaluate_team_dynamics(agents)

        # Display compatibility score
        compat_score = team_dynamics.team_compatibility
        compat_status = (
            "🟢 GOOD"
            if compat_score >= 70
            else "🟡 FAIR"
            if compat_score >= 40
            else "🔴 POOR"
        )
        print(f"Team Compatibility: {compat_status} ({compat_score}/100)")

        # Display relationship warnings
        if team_dynamics.relationship_warnings:
            print("\n⚠️  RELATIONSHIP WARNINGS:")
            for warning in team_dynamics.relationship_warnings:
                print(f" • {warning}")

        # Display skill coverage
        print("\n🎯 SKILL COVERAGE:")
        for skill, coverage in team_dynamics.skill_coverage.items():
            print(f" • {skill}: {coverage:.0f}%")

        # Get confirmation
        print("\n" + "=" * 40)
        if team_dynamics.relationship_warnings:
            confirm = input(
                "\n⚠️  WARNING: This team has compatibility issues. Proceed anyway? (y/n): "
            )
        else:
            confirm = input("\nProceed with this team? (y/n): ")

        return confirm.lower() == "y"

    def display_mission_outcome(
        self, mission: Mission, agents: List[Agent], outcome: Dict
    ):
        """Display mission outcome with relationship-driven narrative"""
        self.clear_screen()
        self.display_header()

        print("📋 MISSION OUTCOME REPORT")
        print("=" * 40)

        # Basic outcome
        success_icon = "✅" if outcome.get("success", False) else "❌"
        print(f"{success_icon} Mission: {mission.mission_type.value.upper()}")
        print(f"Result: {'SUCCESS' if outcome.get('success', False) else 'FAILURE'}")
        print(f"Description: {outcome.get('description', 'No description')}")

        # Casualties and consequences
        if outcome.get("casualties", 0) > 0:
            print(f"💀 Casualties: {outcome['casualties']}")

        # Phase 2: Relationship-driven narrative
        from .relationships import generate_relationship_narrative

        relationship_narratives = generate_relationship_narrative(
            {
                "agents": agents,
                "mission_type": mission.mission_type.value,
                "outcome": outcome,
            }
        )

        if relationship_narratives:
            print("\n🎭 TEAM DYNAMICS:")
            for narrative in relationship_narratives:
                print(f"   • {narrative}")

        # Show emotional impacts
        if "emotional_impacts" in outcome:
            print("\n🎭 EMOTIONAL IMPACTS:")
            for agent_id, changes in outcome["emotional_impacts"].items():
                agent = self.game_state.agents[agent_id]
                print(f"   {agent.name}: {changes}")

        input("\nPress Enter to continue...")

    def end_turn_summary(self):
        """Display end of turn summary"""
        print("\n" + "=" * 50)
        print("📊 TURN SUMMARY")
        print("=" * 50)

        # Show agent status
        print("Agent Status:")
        for agent in self.game_state.agents.values():
            print(f"  {self.display_agent_status(agent)}")

        # Show faction resources
        for faction in self.game_state.factions.values():
            print(f"\nFaction: {faction.name}")
            for resource, amount in faction.resources.items():
                print(f"  {resource.capitalize()}: {amount}")

        input("\nPress Enter to continue to next turn...")

    def _get_mood_description(self, emotion: str, intensity: float) -> str:
        """Get descriptive text for agent mood"""
        if intensity > 0.7:
            intensity_word = "Very"
        elif intensity > 0.5:
            intensity_word = "Quite"
        elif intensity > 0.3:
            intensity_word = "Somewhat"
        else:
            intensity_word = "Slightly"

        emotion_descriptions = {
            "hope": f"{intensity_word} optimistic",
            "fear": f"{intensity_word} anxious",
            "anger": f"{intensity_word} frustrated",
            "despair": f"{intensity_word} dejected",
            "determination": f"{intensity_word} focused",
        }

        return emotion_descriptions.get(emotion, f"{intensity_word} {emotion}")


class EmotionalStateManager:
    """Manages basic emotional states and their impacts on agent behavior"""

    def __init__(self):
        self.base_emotions = ["hope", "fear", "anger", "despair", "determination"]

    def update_agent_emotions(
        self, agent: Agent, mission_outcome: Dict[str, any]
    ) -> Dict[str, float]:
        """Update agent emotions based on mission outcome"""
        emotional_changes = {}

        success = mission_outcome.get("success", False)
        mission_type = mission_outcome.get("mission_type")
        casualties = mission_outcome.get("casualties", 0)

        if success:
            # Successful missions boost hope and determination
            emotional_changes["hope"] = 0.2
            emotional_changes["determination"] = 0.1
            emotional_changes["fear"] = -0.1
            emotional_changes["despair"] = -0.1
        else:
            # Failed missions increase fear and despair
            emotional_changes["fear"] = 0.15
            emotional_changes["despair"] = 0.1
            emotional_changes["hope"] = -0.1
            emotional_changes["anger"] = 0.05

        # High casualties increase trauma
        if casualties > 0:
            emotional_changes["fear"] = (
                emotional_changes.get("fear", 0) + 0.1 * casualties
            )
            emotional_changes["anger"] = (
                emotional_changes.get("anger", 0) + 0.05 * casualties
            )

        # Apply emotional changes
        for emotion, change in emotional_changes.items():
            if emotion in agent.emotion_state:
                new_value = max(0.0, min(1.0, agent.emotion_state[emotion] + change))
                agent.emotion_state[emotion] = new_value

        return emotional_changes

    def get_emotional_mission_modifiers(self, agent: Agent) -> Dict[str, float]:
        """Get mission success modifiers based on emotional state"""
        modifiers = {}

        # Hope increases success chance
        if agent.emotion_state.get("hope", 0) > 0.6:
            modifiers["success_bonus"] = 0.1

        # Fear decreases success chance
        if agent.emotion_state.get("fear", 0) > 0.6:
            modifiers["success_penalty"] = -0.15

        # Anger can help with sabotage but hurt with recruitment
        if agent.emotion_state.get("anger", 0) > 0.6:
            modifiers["sabotage_bonus"] = 0.1
            modifiers["recruitment_penalty"] = -0.1

        # Despair significantly hurts all missions
        if agent.emotion_state.get("despair", 0) > 0.7:
            modifiers["major_penalty"] = -0.2

        return modifiers
