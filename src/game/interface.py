"""
Years of Lead - Player Decision Interface (Phase 1 + Phase 2)

Interactive CLI interface for mission planning and agent management.
Transforms the simulation into a playable game where player choices drive
agent psychology and mission outcomes.

Phase 2: Enhanced with relationship-driven team dynamics and compatibility warnings.
"""

import os
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from .entities import Agent, Mission, MissionType, Location
from .core import GameState


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
    """CLI interface for player decision-making and mission planning"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.selected_agents: List[Agent] = []
        self.current_mission_packet: Optional[MissionPacket] = None
        self.warnings_acknowledged = False

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system("clear" if os.name == "posix" else "cls")

    def show_message(self, message: str, pause_after: bool = True) -> None:
        """Display a message to the player

        Args:
            message: The message to display
            pause_after: If True, wait for user to press Enter
        """
        print(message)
        if pause_after:
            input("\nPress Enter to continue...")

    def confirm(self, prompt: str, default: bool = True) -> bool:
        """Get a yes/no confirmation from the player

        Args:
            prompt: The confirmation prompt to display
            default: The default value if user just presses Enter

        Returns:
            bool: True if confirmed, False otherwise
        """
        options = "[Y/n]" if default else "[y/N]"
        while True:
            response = input(f"{prompt} {options} ").strip().lower()
            if not response:
                return default
            if response in ("y", "yes"):
                return True
            if response in ("n", "no"):
                return False
            print("Please answer 'y' or 'n'.")

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
        """Display agent status with emotional indicators and detailed information"""
        # Get dominant emotion for display
        dominant_emotion = max(agent.emotion_state.items(), key=lambda x: x[1])
        emotion_icon = self._get_emotion_icon(dominant_emotion[0])

        # Basic status line with safe attribute access
        status_line = f"[{agent.id}] {agent.name} {emotion_icon}"
        status_line += f" | Stress: {getattr(agent, 'stress', 0)}% | Loyalty: {getattr(agent, 'loyalty', 50)}%"

        if detailed:
            # Location and background
            status_line += f"\n    Location: {getattr(agent, 'location_id', 'Unknown')}"
            status_line += f" | Background: {getattr(agent, 'background', 'Unknown')}"
            
            # Skills (only show those above 50%)
            skills = getattr(agent, 'skills', {})
            if skills:
                status_line += f"\n    Skills: {', '.join(f'{k}:{v}' for k, v in skills.items() if v > 50)}"
            
            # Status and emotional state
            status_line += f"\n    Status: {getattr(agent, 'status', 'Unknown')}"
            status_line += "\n    Emotions: "
            for emotion, level in agent.emotion_state.items():
                if level > 0.3:  # Only show significant emotions
                    status_line += f"{emotion.capitalize()}: {level:.1f} "

            # Show psychological warnings
            warnings = getattr(self, 'get_agent_warnings', lambda x: [])(agent)
            if warnings:
                status_line += f"\n    Warnings: {', '.join(warnings)}"

        return status_line

    def _get_emotion_icon(self, emotion: str) -> str:
        """Get icon for emotional state"""
        icons = {
            "hope": "🌟",
            "fear": "😨",
            "anger": "😠",
            "despair": "😞",
            "determination": "💪",
            "happy": "😊",
            "sad": "😢",
            "stressed": "😰",
            "confident": "😎",
            "tired": "😴",
        }
        return icons.get(emotion.lower(), "😐")

    def get_agent_warnings(self, agent: Agent) -> List[str]:
        """Generate psychological and relationship warnings for agent"""
        warnings = []

        # Psychological state warnings
        if getattr(agent, "stress", 0) > 80:
            warnings.append("🚨 Extreme stress")
        elif getattr(agent, "stress", 0) > 60:
            warnings.append("⚠️ High stress")

        if hasattr(agent, "mood") and agent.mood < 30:
            warnings.append("😞 Depression")
        elif hasattr(agent, "mood") and agent.mood < 50:
            warnings.append("😐 Low morale")

        # Trauma warnings
        if hasattr(agent, "trauma_flags"):
            if "combat_trauma" in agent.trauma_flags:
                warnings.append("💥 Combat trauma")
            if "betrayal_trauma" in agent.trauma_flags:
                warnings.append("🔓 Trust issues")

        return warnings

    # ===== MISSION PLANNING METHODS =====

    def start_planning_session(self) -> Optional[MissionPacket]:
        """Main entry point for mission planning"""
        self.display_header()
        self.display_faction_status()

        while True:
            choice = self.display_main_menu()

            if choice == "1":
                mission_packet = self.plan_new_mission()
                if mission_packet:
                    return mission_packet
            elif choice == "2":
                self.review_agent_status()
            elif choice == "3":
                self.review_location_intel()
            elif choice == "4":
                self.review_relationship_map()
            elif choice == "5":
                break  # End planning, no mission
            else:
                print("Invalid choice. Please try again.")

        return None

    def display_main_menu(self) -> str:
        """Show main planning menu"""
        print("\n🎯 MISSION PLANNING OPTIONS:")
        print("   1. Plan New Mission")
        print("   2. Review Agent Status")
        print("   3. Review Location Intel")
        print("   4. Review Relationship Map")
        print("   5. End Planning Phase")

        return input("\nYour choice (1-5): ").strip()

    def plan_new_mission(self) -> Optional[MissionPacket]:
        """Complete mission planning workflow"""
        print("\n" + "=" * 60)
        print("   MISSION PLANNING WIZARD")
        print("=" * 60)

        # Step 1: Select Mission Type
        mission_type = self.select_mission_type()
        if not mission_type:
            return None

        # Step 2: Select Location
        location = self.select_location(mission_type)
        if not location:
            return None

        # Step 3: Select Agents
        agents = self.select_agents(mission_type, location)
        if not agents:
            return None

        # Step 4: Assign Equipment (simplified for now)
        equipment_assignments = {
            a.id: [] for a in agents
        }  # TODO: Implement equipment system

        # Step 5: Choose Approach
        approach = self.select_tactical_approach(mission_type, location, agents)

        # Step 6: Risk Assessment & Warnings
        if not self.conduct_risk_assessment(agents, mission_type, location, approach):
            return None

        # Step 7: Final Confirmation
        mission_packet = MissionPacket(
            agents=agents,
            location_id=location.id,
            mission_type=mission_type,
            approach=approach,
            equipment_assignments=equipment_assignments,
        )

        if self.confirm_mission(mission_packet):
            return mission_packet

        return None

    def select_mission_type(self) -> Optional[MissionType]:
        """Let player select mission type"""
        print("\n📋 AVAILABLE MISSION TYPES:")
        for i, mtype in enumerate(MissionType, 1):
            print(f"   {i}. {mtype.value.capitalize()}")
        print(f"   {len(MissionType)+1}. Back to main menu")

        try:
            choice = int(input("\nSelect mission type: ")) - 1
            if 0 <= choice < len(MissionType):
                return list(MissionType)[choice]
            elif choice == len(MissionType):
                return None
            else:
                print("❌ Invalid choice!")
                return self.select_mission_type()
        except ValueError:
            print("❌ Please enter a valid number!")
            return self.select_mission_type()

    def select_location(self, mission_type: MissionType) -> Optional[Location]:
        """Select location for mission"""
        locations = list(self.game_state.locations.values())

        print(f"\n📍 SELECT TARGET LOCATION ({mission_type.value}):")
        for i, loc in enumerate(locations, 1):
            print(f"   {i}. {loc.name} (Security: {loc.security_level}/100)")
        print(f"   {len(locations)+1}. Back")

        try:
            choice = int(input("\nSelect location: ")) - 1
            if 0 <= choice < len(locations):
                return locations[choice]
            elif choice == len(locations):
                return None
            else:
                print("❌ Invalid choice!")
                return self.select_location(mission_type)
        except ValueError:
            print("❌ Please enter a valid number!")
            return self.select_location(mission_type)

    def select_agents(
        self, mission_type: MissionType, location: Location
    ) -> List[Agent]:
        """Select agents for mission with psychological assessment"""
        available_agents = [
            a for a in self.game_state.agents.values() if a.status == "available"
        ]

        if not available_agents:
            print("❌ No agents available for missions!")
            return []

        selected_agents = []
        max_team_size = 3

        while len(selected_agents) < max_team_size:
            print(
                f"\n👥 AGENT SELECTION (Selected: {len(selected_agents)}/{max_team_size})"
            )
            print(f"   Mission: {mission_type.value} at {location.name}")

            # Display available agents with status
            self.display_detailed_agent_list(
                available_agents, mission_type, selected_agents
            )

            print("\n   Options:")
            print("   • Enter agent number to select/deselect")
            print("   • Type 'continue' to proceed with current selection")
            print("   • Type 'back' to return to previous step")

            choice = input("\nYour choice: ").strip().lower()

            if choice == "continue":
                if len(selected_agents) > 0:
                    break
                else:
                    print("❌ Must select at least one agent!")
                    continue
            elif choice == "back":
                return []

            try:
                agent_num = int(choice) - 1
                if 0 <= agent_num < len(available_agents):
                    agent = available_agents[agent_num]

                    if agent in selected_agents:
                        selected_agents.remove(agent)
                        print(f"✅ Removed {agent.name} from mission")
                    else:
                        selected_agents.append(agent)
                        print(f"✅ Added {agent.name} to mission")

                        # Show team compatibility if multiple agents
                        if len(selected_agents) > 1:
                            self.display_team_compatibility_preview(selected_agents)
                else:
                    print("❌ Invalid agent number!")
            except ValueError:
                print("❌ Please enter a valid number or command!")

        return selected_agents

    def _get_suitability_color(self, skill_value: float) -> str:
        """Get ANSI color code based on skill suitability"""
        if skill_value >= 70:
            return "\033[92m"  # Green
        elif skill_value >= 40:
            return "\033[93m"  # Yellow
        else:
            return "\033[91m"  # Red

    def _reset_color(self) -> str:
        """Reset ANSI color"""
        return "\033[0m"

    def display_detailed_agent_list(
        self, agents: List[Agent], mission_type: MissionType, selected: List[Agent]
    ):
        """Show agents with psychological state and mission suitability"""
        print(
            "\n📋 AVAILABLE AGENTS (Suitability: \033[92mHigh\033[0m / \033[93mMedium\033[0m / \033[91mLow\033[0m)"
        )
        print(
            f"{'#':<2} {'Name':<12} {'Mood':<5} {'Stress':<6} {'Skill':<6} {'Status':<15} {'Warnings'}"
        )
        print(f"{'='*60}")

        for i, agent in enumerate(agents, 1):
            # Calculate relevant skill for mission
            relevant_skill = self.get_relevant_skill_value(agent, mission_type)

            # Get color based on skill suitability
            color_code = self._get_suitability_color(relevant_skill)
            reset_code = self._reset_color()

            # Determine psychological warnings
            warnings = self.get_agent_warnings(agent)
            warning_text = ", ".join(warnings) if warnings else "✅ Stable"

            # Selection indicator
            selected_indicator = "✓" if agent in selected else " "

            # Apply color to agent name and skill
            colored_name = f"{color_code}{agent.name}{reset_code}"
            colored_skill = f"{color_code}{relevant_skill:.0f}{reset_code}"

            print(
                f"{i:<2} {colored_name:<12} "
                f"{getattr(agent, 'mood', 50):<5.0f} "
                f"{getattr(agent, 'stress', 0):<6.0f} "
                f"{colored_skill:<6} "
                f"{selected_indicator:<15} "
                f"{warning_text}"
            )

    def get_relevant_skill_value(
        self, agent: Agent, mission_type: MissionType
    ) -> float:
        """Get the most relevant skill value for this mission type"""
        # Simplified - would be expanded based on actual skill system
        skill_map = {
            MissionType.INFILTRATION: "stealth",
            MissionType.SABOTAGE: "sabotage",
            MissionType.ASSASSINATION: "marksmanship",
            MissionType.RESCUE: "medical",
            MissionType.PROPAGANDA: "charisma",
            MissionType.RECONNAISSANCE: "perception",
            MissionType.SUPPLY_RUN: "logistics",
        }

        skill_name = skill_map.get(mission_type, "combat")
        return agent.skills.get(skill_name, 50)  # Default to 50 if skill not found

    def display_team_compatibility_preview(self, agents: List[Agent]):
        """Show a quick preview of team dynamics"""
        if hasattr(self.game_state, "evaluate_team_dynamics"):
            team_dynamics = self.game_state.evaluate_team_dynamics(agents)

            if team_dynamics.synergy_bonus > 0.1:
                print(
                    f"   ✅ Strong team synergy: +{team_dynamics.synergy_bonus:.0%} effectiveness"
                )
            elif team_dynamics.synergy_bonus < -0.1:
                print(
                    f"   ⚠️ Team friction: {abs(team_dynamics.synergy_bonus):.0%} penalty"
                )

            if hasattr(team_dynamics, "conflicts") and team_dynamics.conflicts:
                print("   🚨 Relationship issues detected!")

    def select_tactical_approach(
        self, mission_type: MissionType, location: Location, agents: List[Agent]
    ) -> TacticalApproach:
        """Select tactical approach for the mission"""
        print("\n🎯 SELECT TACTICAL APPROACH:")

        # Get recommended approach based on team composition
        recommended = self.calculate_recommended_approach(agents)

        while True:
            print("\nAvailable approaches:")
            for i, approach in enumerate(TacticalApproach, 1):
                rec_marker = " (Recommended)" if approach == recommended else ""
                print(f"{i}. {approach.value.capitalize()}{rec_marker}")

            try:
                choice = (
                    input("\nSelect approach (or 'back' to return): ").strip().lower()
                )
                if choice == "back":
                    return None

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(TacticalApproach):
                    return list(TacticalApproach)[choice_idx]
                else:
                    print("❌ Invalid choice. Please enter a valid number.")
            except ValueError:
                print("❌ Please enter a valid number.")
        # Team dynamics analysis will be shown in the risk assessment
        return recommended

        # Show individual relationships
        print("\n--- AGENT RELATIONSHIPS ---")
        for i, agent_a in enumerate(agents):
            for agent_b in agents[i + 1 :]:
                rel = agent_a.get_relationship_with(agent_b.id)
                trust_icon = "🤝" if rel.trust > 60 else "⚠️" if rel.trust > 30 else "❌"
                affinity_icon = (
                    "💙" if rel.affinity > 60 else "😐" if rel.affinity > 30 else "💔"
                )

                print(
                    f"   {agent_a.name} → {agent_b.name}: {trust_icon} Trust {rel.trust:.0f}, {affinity_icon} Affinity {rel.affinity:.0f}"
                )

                # Show notable history
                if rel.shared_history:
                    recent_history = rel.shared_history[-2:]  # Last 2 events
                    history_str = ", ".join(recent_history)
                    print(f"      History: {history_str}")

        # Get team dynamics for compatibility warnings
        from .relationships import evaluate_team_dynamics
        team_dynamics = evaluate_team_dynamics(self.selected_agents)
        
        if team_dynamics.conflicts:
            print("\n🚨 RELATIONSHIP WARNINGS:")
            for conflict in team_dynamics.conflicts:
                print(f"   • {conflict}")

        if team_dynamics.refusal_risk:
            print("\n❌ REFUSAL RISK:")
            for refusal in team_dynamics.refusal_risk:
                print(f"   • {refusal}")

        if team_dynamics.conflicts or team_dynamics.refusal_risk:
            # Ask player if they want to proceed anyway
            proceed = input("\nProceed with this team composition? (y/n): ")
            return proceed.lower() == "y"

        return True

    def mission_planning_interface(
        self, current_missions_count: int = 0
    ) -> Optional[Tuple[Mission, List[Agent]]]:
        """
        Enhanced mission planning with relationship awareness and multi-mission support

        Args:
            current_missions_count: Number of missions already planned this turn
        """
        self.clear_screen()
        self.display_header()

        # Show current mission plan if any
        if (
            hasattr(self.game_state, "planned_missions")
            and self.game_state.planned_missions
        ):
            print("\n📋 CURRENTLY PLANNED MISSIONS:")
            for i, (m, agents) in enumerate(self.game_state.planned_missions, 1):
                print(
                    f"  {i}. {m.mission_type.value.upper()} with {', '.join(a.name for a in agents)}"
                )

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
                        raise ValueError("At least one agent must be selected")
                    break
                except (ValueError, IndexError) as e:
                    print(f"❌ Invalid selection: {e}. Please try again.")

            # Team compatibility check
            if len(selected_agents) > 1 and hasattr(self, "display_team_analysis"):
                print(f"\nAnalyzing team of {len(selected_agents)} agents...")
                if not self.display_team_analysis(selected_agents):
                    print(
                        "Mission planning cancelled due to team compatibility issues."
                    )
                    input("Press Enter to continue...")
                    return None

            # Create mission
            mission = Mission(
                id=f"mission_{self.game_state.turn_number}_{mission_type.value}",
                mission_type=mission_type,
                faction_id="resistance",
                target_location_id="university",
                participants=[agent.id for agent in selected_agents],
            )

            # Display mission summary
            print("\n📝 MISSION DETAILS:")
            print(f"Type: {mission_type.value.upper()}")
            print(
                f"Assigned agents: {', '.join(agent.name for agent in selected_agents)}"
            )

            if current_missions_count > 0:
                print(
                    f"\nℹ️ You have already planned {current_missions_count} mission{'s' if current_missions_count > 1 else ''} this turn."
                )

            confirm = input("\nAdd this mission to the plan? (y/n): ")
            if confirm.lower() == "y":
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

    def display_available_missions(self) -> List[Mission]:
        """Display available missions for selection"""
        print("\n📋 AVAILABLE MISSIONS:")
        print("-" * 40)

        available_missions = []
        mission_types = [
            (MissionType.PROPAGANDA, "Spread propaganda leaflets"),
            (MissionType.SABOTAGE, "Sabotage government facility"),
            (MissionType.RECRUITMENT, "Recruit new operatives"),
            (MissionType.INTELLIGENCE, "Gather intelligence"),
            (MissionType.FINANCING, "Raise funds for operations"),
        ]

        for i, (mission_type, description) in enumerate(mission_types, 1):
            mission = Mission(
                id=f"mission_{mission_type.value}_{self.game_state.turn_number}",
                mission_type=mission_type,
                faction_id="resistance",  # Default faction
                target_location_id="downtown",  # Default location
            )
            available_missions.append(mission)

            risk_level = self._calculate_mission_risk(mission)
            risk_icon = "🟢" if risk_level < 3 else "🟡" if risk_level < 7 else "🔴"

            print(f"{i}. {mission_type.value.upper()}: {description}")
            print(f"   Risk Level: {risk_icon} {risk_level}/10")

        return available_missions

    def _calculate_mission_risk(self, mission: Mission) -> int:
        """Calculate mission risk level (1-10)"""
        base_risk = {
            MissionType.PROPAGANDA: 3,
            MissionType.RECRUITMENT: 4,
            MissionType.INTELLIGENCE: 6,
            MissionType.FINANCING: 5,
            MissionType.SABOTAGE: 8,
        }

        # Add location-based risk modifiers here if needed
        return base_risk.get(mission.mission_type, 5)

    def display_agent_selection(self) -> List[Agent]:
        """Display agents available for mission assignment"""
        print("\n👥 SELECT OPERATIVES:")
        print("-" * 40)

        available_agents = [
            agent
            for agent in self.game_state.agents.values()
            if agent.status.value == "active"
        ]

        for i, agent in enumerate(available_agents, 1):
            print(f"{i}. {self.display_agent_status(agent, detailed=True)}")

        return available_agents

    def get_player_input(self, prompt: str, valid_options: List[str] = None) -> str:
        """Get validated player input"""
        while True:
            try:
                response = input(f"\n{prompt}: ").strip().lower()

                if valid_options and response not in valid_options:
                    print(f"Invalid option. Choose from: {', '.join(valid_options)}")
                    continue

                return response

            except (KeyboardInterrupt, EOFError):
                print("\nExiting game...")
                return "quit"

    def _get_emotion_icon(self, emotion: str) -> str:
        """Get visual icon for emotional state"""
        emotion_icons = {
            "hope": "😊",
            "fear": "😰",
            "anger": "😠",
            "despair": "😢",
            "determination": "💪",
            "happy": "😊",
            "sad": "😢",
            "stressed": "😰",
            "confident": "😎",
            "tired": "😴",
        }
        return emotion_icons.get(emotion.lower(), "😐")

    def _calculate_mission_risk(
        self, mission_type: MissionType, agents: List[Agent]
    ) -> int:
        """Calculate mission risk level (1-10) based on mission type and agents"""
        risk = 5  # Base risk

        # Adjust based on mission type
        if mission_type in [MissionType.ASSASSINATION, MissionType.SABOTAGE]:
            risk += 3
        elif mission_type in [MissionType.INTEL, MissionType.RECON]:
            risk -= 1

        # Adjust based on number of agents
        if len(agents) < 2:
            risk += 2  # Higher risk with fewer agents
        elif len(agents) > 3:
            risk -= 1  # Lower risk with more agents

        # Adjust based on agent stress levels
        total_stress = sum(agent.stress for agent in agents)
        avg_stress = total_stress / len(agents) if agents else 0
        if avg_stress > 70:
            risk += 2
        elif avg_stress > 50:
            risk += 1

        # Cap risk between 1-10
        return max(1, min(10, risk))

    def _calculate_mission_risk(
        self, mission_type: MissionType, agents: List[Agent]
    ) -> int:
        """Calculate mission risk level (1-10) based on mission type and agents"""
        # Base risk by mission type
        risk_levels = {
            MissionType.INTEL: 3,
            MissionType.RECRUITMENT: 4,
            MissionType.SABOTAGE: 6,
            MissionType.ASSASSINATION: 8,
            MissionType.EXTRACTION: 7,
            MissionType.PROPAGANDA: 4,
            MissionType.TRAINING: 2,
            MissionType.RECON: 3,
            MissionType.INFILTRATION: 7,
            MissionType.ESCAPE: 5,
        }

        # Start with base risk
        risk = risk_levels.get(mission_type, 5)

        # Adjust based on team size
        if len(agents) == 1:
            risk += 1  # Solo missions are riskier
        elif len(agents) > 3:
            risk += 1  # Larger teams are more noticeable

        # Adjust based on agent stress levels
        avg_stress = (
            sum(agent.stress for agent in agents) / len(agents) if agents else 0
        )
        if avg_stress > 70:
            risk += 2
        elif avg_stress > 50:
            risk += 1

        # Cap risk between 1-10
        return max(1, min(10, risk))

    def evaluate_team_compatibility(self, agents: List[Agent]) -> Dict[str, Any]:
        """Evaluate team compatibility and return analysis"""
        if len(agents) <= 1:
            return {"compatible": True, "warnings": [], "synergy": 0, "avg_trust": 50}

        total_trust = 0
        trust_pairs = 0
        warnings = []

        # Check relationships between all agent pairs
        for i, agent_a in enumerate(agents):
            for agent_b in agents[i + 1 :]:
                if hasattr(agent_a, "get_relationship_with"):
                    rel = agent_a.get_relationship_with(agent_b.id)
                    total_trust += rel.trust
                    trust_pairs += 1

                    # Add warnings for problematic relationships
                    if rel.trust < 30:
                        warnings.append(
                            f"Low trust between {agent_a.name} and {agent_b.name}"
                        )
                    if hasattr(rel, "has_conflict") and rel.has_conflict():
                        warnings.append(
                            f"Active conflict between {agent_a.name} and {agent_b.name}"
                        )

        # Calculate average trust (0-100 scale)
        avg_trust = total_trust / trust_pairs if trust_pairs > 0 else 50

        # Calculate synergy bonus (-0.2 to +0.2)
        synergy = (avg_trust - 50) / 250.0

        return {
            "compatible": len(warnings) < 3,  # Allow up to 2 warnings
            "warnings": warnings,
            "synergy": synergy,
            "avg_trust": avg_trust,
        }

    def display_team_analysis(self, agents: List[Agent]) -> bool:
        """Display team analysis and get confirmation"""
        if len(agents) <= 1:
            return True

        analysis = self.evaluate_team_compatibility(agents)

        print("\n" + "🔍 TEAM ANALYSIS " + "🔍" * 10)

        # Display team composition
        print("\n👥 TEAM COMPOSITION:")
        for agent in agents:
            print(f"   • {agent.name} (Stress: {agent.stress}%)")

        # Display trust metrics
        print(f"\n🤝 TEAM TRUST: {analysis['avg_trust']:.0f}/100")
        if analysis["synergy"] > 0.1:
            print(
                f"   ✅ Positive team synergy (+{analysis['synergy']*100:.0f}% effectiveness)"
            )
        elif analysis["synergy"] < -0.1:
            print(
                f"   ⚠️  Negative team synergy ({analysis['synergy']*100:.0f}% effectiveness)"
            )
        else:
            print("   ➖ Neutral team dynamics")

        # Display warnings if any
        if analysis["warnings"]:
            print("\n⚠️  POTENTIAL ISSUES:")
            for warning in analysis["warnings"]:
                print(f"   • {warning}")

        # Always ask for confirmation if there are warnings
        if analysis["warnings"]:
            print("\nProceed with this team despite the warnings?")
            confirm = input("(y/n): ").strip().lower()
            return confirm == "y"

        return True

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
