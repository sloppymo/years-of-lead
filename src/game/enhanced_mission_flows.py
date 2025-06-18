"""Enhanced mission flows with dramatic choices and consequences"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from random import random


class MissionPhase(Enum):
    """Phases of a mission's narrative flow"""

    PREPARATION = auto()
    INFILTRATION = auto()
    EXECUTION = auto()
    CRISIS = auto()
    EXTRACTION = auto()
    AFTERMATH = auto()


@dataclass
class MissionState:
    """Tracks the state of an ongoing mission with choices"""

    mission_id: str
    current_phase: MissionPhase
    agents: List[Any]  # List[Agent] - using Any to avoid circular imports
    success_probability: float
    stress_accumulation: Dict[str, float]  # agent_id -> stress amount
    relationship_changes: Dict[
        str, Dict[str, float]
    ]  # agent_id -> {relationship_id -> change}
    narrative_log: List[str]
    crisis_points: List[Dict[str, Any]]
    player_choices: List[Dict[str, Any]]
    additional_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MissionChoice:
    """A player choice point in the mission flow"""

    id: str
    description: str
    options: List[Dict[str, Any]]
    time_pressure: bool = False
    moral_weight: str = "medium"  # low, medium, high, extreme
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChoiceOutcome:
    """Outcome of a player's choice"""

    success: bool
    narrative: str
    consequences: Dict[str, Any]
    next_phase: Optional[MissionPhase] = None


class InfiltrationMissionFlow:
    """Dramatic mission flow for infiltration missions"""

    def __init__(self, mission_state: MissionState):
        self.state = mission_state
        self._setup_mission()

    def _setup_mission(self):
        """Initialize mission-specific state"""
        self.state.additional_state.update(
            {
                "security_level": random() * 0.5 + 0.25,  # 0.25 - 0.75
                "intel_quality": random() * 0.6 + 0.2,  # 0.2 - 0.8
                "team_cohesion": self._calculate_team_cohesion(),
                "turns_elapsed": 0,
                "alerts_raised": 0,
                "objectives_completed": 0,
                "extraction_available": False,
            }
        )

    def _calculate_team_cohesion(self) -> float:
        """Calculate initial team cohesion based on relationships"""
        if len(self.state.agents) == 1:
            return 0.8  # Solo missions have high cohesion

        total_affinity = 0
        pair_count = 0

        for i, agent1 in enumerate(self.state.agents):
            for agent2 in self.state.agents[i + 1 :]:
                if hasattr(agent1, "get_relationship_with"):
                    rel = agent1.get_relationship_with(agent2.id)
                    if hasattr(rel, "affinity"):
                        total_affinity += rel.affinity
                        pair_count += 1

        return (total_affinity / (pair_count * 100)) if pair_count > 0 else 0.5

    def execute_mission(self) -> Dict[str, Any]:
        """Execute the full mission flow with player choices"""
        self.state.narrative_log.append(
            "Mission initialized. Beginning infiltration..."
        )

        # Main mission loop
        while not self._is_mission_complete():
            self._process_phase()
            self.state.turns_elapsed += 1

        return self._generate_mission_result()

    def _process_phase(self):
        """Process the current mission phase"""
        if self.state.current_phase == MissionPhase.PREPARATION:
            self._handle_preparation()
        elif self.state.current_phase == MissionPhase.INFILTRATION:
            self._handle_infiltration()
        elif self.state.current_phase == MissionPhase.EXECUTION:
            self._handle_execution()
        elif self.state.current_phase == MissionPhase.CRISIS:
            self._handle_crisis()
        elif self.state.current_phase == MissionPhase.EXTRACTION:
            self._handle_extraction()

    def _handle_preparation(self):
        """Handle mission preparation phase"""
        self.state.narrative_log.append("\n🔍 PREPARATION PHASE")

        # Add preparation choices here
        choice = MissionChoice(
            id="prep_approach",
            description="How will your team prepare for this infiltration?",
            options=[
                {
                    "text": "Detailed recon - Gather extensive intel on the target location",
                    "consequences": {
                        "intel_quality": +0.3,
                        "time_penalty": 2,
                        "risk": "delayed_start",
                    },
                    "requirements": {"patience": True},
                },
                {
                    "text": "Quick strike - Move in fast before security is alerted",
                    "consequences": {"surprise": +0.4, "risk": "high_alert"},
                    "requirements": {"speed_over_caution": True},
                },
                {
                    "text": "Social engineering - Infiltrate through staff or visitors",
                    "consequences": {
                        "disguise_quality": 0.7,
                        "risk": "identity_compromise",
                    },
                    "requirements": {"social_skill": 60},
                },
            ],
            moral_weight="medium",
        )

        # In a real implementation, this would present the choice to the player
        # and update mission state based on their selection
        selected_option = choice(choice.options)  # Random selection for example
        self.state.player_choices.append(
            {"phase": "preparation", "choice": selected_option}
        )
        self.state.current_phase = MissionPhase.INFILTRATION

    def _handle_infiltration(self):
        """Handle the infiltration phase"""
        self.state.narrative_log.append("\n👥 INFILTRATION PHASE")
        # Implementation would handle the infiltration sequence
        self.state.current_phase = MissionPhase.EXECUTION

    def _handle_execution(self):
        """Handle the main mission execution"""
        self.state.narrative_log.append("\n🎯 EXECUTION PHASE")
        # Implementation would handle the main mission actions

        # For now, simulate some outcomes
        if random() > 0.3:  # 70% chance of success
            self.state.objectives_completed += 1
            self.state.narrative_log.append("Primary objective completed successfully!")
        else:
            self.state.alerts_raised += 1
            self.state.narrative_log.append(
                "⚠️  Alarm triggered! Security is on high alert!"
            )
            self.state.current_phase = MissionPhase.CRISIS

    def _handle_crisis(self):
        """Handle crisis situations"""
        self.state.narrative_log.append("\n🚨 CRISIS PHASE")
        # Implementation would handle crisis resolution
        self.state.current_phase = MissionPhase.EXTRACTION

    def _handle_extraction(self):
        """Handle extraction phase"""
        self.state.narrative_log.append("\n🏃 EXTRACTION PHASE")
        # Implementation would handle extraction
        self.state.current_phase = MissionPhase.AFTERMATH

    def _is_mission_complete(self) -> bool:
        """Check if mission is complete"""
        return (
            self.state.current_phase == MissionPhase.AFTERMATH
            or self.state.turns_elapsed >= 10
        )

    def _generate_mission_result(self) -> Dict[str, Any]:
        """Generate final mission result"""
        success = self.state.objectives_completed > 0 and self.state.alerts_raised < 2

        return {
            "success": success,
            "objectives_completed": self.state.objectives_completed,
            "alerts_raised": self.state.alerts_raised,
            "turns_elapsed": self.state.turns_elapsed,
            "narrative": "\n".join(self.state.narrative_log),
            "stress_changes": self.state.stress_accumulation,
            "relationship_changes": self.state.relationship_changes,
            "player_choices": [c["choice"]["text"] for c in self.state.player_choices],
        }
