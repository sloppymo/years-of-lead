"""
Years of Lead - Complete Core Simulation Engine

This module completes and expands the core simulation with advanced features:
- Enhanced turn processing with relationship integration
- Advanced mission execution with real-time events
- Dynamic world state management
- Comprehensive agent progression systems
- Advanced faction dynamics
- Real-time intelligence and counter-intelligence
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import random

from .entities import Agent, GameState
from .relationships import Relationship


class SimulationPhase(Enum):
    """Enhanced simulation phases with relationship processing"""

    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    RELATIONSHIP_PROCESSING = "relationship_processing"
    INTELLIGENCE_UPDATE = "intelligence_update"
    FACTION_DYNAMICS = "faction_dynamics"
    WORLD_EVENTS = "world_events"


class AgentActivity(Enum):
    """Detailed agent activities"""

    REST = "rest"
    TRAINING = "training"
    MISSION_PLANNING = "mission_planning"
    MISSION_EXECUTION = "mission_execution"
    INTELLIGENCE_GATHERING = "intelligence_gathering"
    RECRUITMENT = "recruitment"
    PROPAGANDA = "propaganda"
    SABOTAGE = "sabotage"
    RESCUE = "rescue"
    INFILTRATION = "infiltration"
    EXFILTRATION = "exfiltration"
    HEALING = "healing"
    INTERROGATION = "interrogation"
    ESCAPE = "escape"
    HIDING = "hiding"
    NETWORKING = "networking"
    COUNTER_INTELLIGENCE = "counter_intelligence"


class WorldEventType(Enum):
    """Enhanced world events"""

    SECURITY_CRACKDOWN = "security_crackdown"
    CIVIL_UNREST = "civil_unrest"
    INFORMANT_BETRAYAL = "informant_betrayal"
    SUPPLY_DROP = "supply_drop"
    AGENT_ESCAPE = "agent_escape"
    GOVERNMENT_ANNOUNCEMENT = "government_announcement"
    WEATHER_EVENT = "weather_event"
    BLACKOUT = "blackout"
    MASS_ARREST = "mass_arrest"
    PROTEST_ERUPTS = "protest_erupts"
    ECONOMIC_CRISIS = "economic_crisis"
    MEDIA_SCANDAL = "media_scandal"
    DIPLOMATIC_INCIDENT = "diplomatic_incident"
    NATURAL_DISASTER = "natural_disaster"
    TECHNOLOGICAL_BREAKTHROUGH = "technological_breakthrough"
    SOCIAL_MOVEMENT = "social_movement"
    MILITARY_OPERATION = "military_operation"
    INTELLIGENCE_LEAK = "intelligence_leak"
    CORRUPTION_SCANDAL = "corruption_scandal"


@dataclass
class AgentSchedule:
    """Agent's schedule for the current phase"""

    agent_id: str
    activity: AgentActivity
    location_id: str
    duration: int = 1  # How many phases this activity lasts
    priority: int = 1  # 1-5 scale
    coordination_with: List[str] = field(default_factory=list)  # Other agents
    equipment_used: List[str] = field(default_factory=list)
    risk_level: int = 1  # 1-5 scale
    success_modifiers: Dict[str, float] = field(default_factory=dict)


@dataclass
class IntelligenceReport:
    """Intelligence gathered by agents"""

    id: str
    source_agent_id: str
    target_location_id: str
    intelligence_type: str  # "security", "personnel", "resources", "plans"
    content: str
    reliability: float  # 0.0-1.0
    freshness: float  # 0.0-1.0, decays over time
    access_level: int  # 1-5, who can see this
    gathered_turn: int
    expires_turn: Optional[int] = None


@dataclass
class CounterIntelligenceOperation:
    """Counter-intelligence operations"""

    id: str
    target_agent_id: str
    operation_type: str  # "surveillance", "interrogation", "infiltration"
    intensity: float  # 0.0-1.0
    duration: int
    success_chance: float
    consequences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorldEvent:
    """Enhanced world events with complex effects"""

    id: str
    event_type: WorldEventType
    location_id: Optional[str] = None
    affected_factions: List[str] = field(default_factory=list)
    description: str
    severity: float  # 0.0-1.0
    duration: int
    effects: Dict[str, Any] = field(default_factory=dict)
    triggers: List[str] = field(default_factory=list)  # What can trigger this
    consequences: List[str] = field(default_factory=list)
    media_coverage: bool = False
    political_impact: float = 0.0  # -1.0 to 1.0


class CompleteCoreSimulation:
    """Complete core simulation engine with all advanced features"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.current_phase = SimulationPhase.MORNING
        self.turn_number = 1
        self.phase_number = 0

        # Enhanced tracking
        self.agent_schedules: Dict[str, AgentSchedule] = {}
        self.intelligence_reports: List[IntelligenceReport] = []
        self.counter_intelligence_ops: List[CounterIntelligenceOperation] = []
        self.active_world_events: List[WorldEvent] = []
        self.relationship_processing_queue: List[Tuple[str, str]] = []
        self.faction_dynamics_timer = 0
        self.intelligence_update_timer = 0

        # Performance tracking
        self.performance_metrics = {
            "agents_processed": 0,
            "relationships_updated": 0,
            "events_generated": 0,
            "missions_completed": 0,
            "intelligence_gathered": 0,
        }

        # Advanced features
        self.enable_relationship_processing = True
        self.enable_intelligence_system = True
        self.enable_counter_intelligence = True
        self.enable_dynamic_events = True
        self.enable_faction_dynamics = True

    def advance_simulation(self) -> Dict[str, Any]:
        """Advance the complete simulation by one phase"""
        results = {
            "phase": self.current_phase.value,
            "turn": self.turn_number,
            "events": [],
            "narrative": [],
            "metrics": {},
        }

        # Process current phase
        phase_results = self._process_current_phase()
        results["events"].extend(phase_results["events"])
        results["narrative"].extend(phase_results["narrative"])

        # Process relationships if enabled
        if self.enable_relationship_processing:
            relationship_results = self._process_relationships()
            results["events"].extend(relationship_results["events"])
            results["narrative"].extend(relationship_results["narrative"])

        # Process intelligence if enabled
        if self.enable_intelligence_system:
            intelligence_results = self._process_intelligence()
            results["events"].extend(intelligence_results["events"])
            results["narrative"].extend(intelligence_results["narrative"])

        # Process counter-intelligence if enabled
        if self.enable_counter_intelligence:
            counter_results = self._process_counter_intelligence()
            results["events"].extend(counter_results["events"])
            results["narrative"].extend(counter_results["narrative"])

        # Process faction dynamics if enabled
        if self.enable_faction_dynamics:
            faction_results = self._process_faction_dynamics()
            results["events"].extend(faction_results["events"])
            results["narrative"].extend(faction_results["narrative"])

        # Process world events if enabled
        if self.enable_dynamic_events:
            world_results = self._process_world_events()
            results["events"].extend(world_results["events"])
            results["narrative"].extend(world_results["narrative"])

        # Update timers and advance phase
        self._advance_phase()

        # Update performance metrics
        results["metrics"] = self.performance_metrics.copy()

        return results

    def _process_current_phase(self) -> Dict[str, Any]:
        """Process the current simulation phase"""
        results = {"events": [], "narrative": []}

        if self.current_phase == SimulationPhase.MORNING:
            results = self._process_morning_phase()
        elif self.current_phase == SimulationPhase.AFTERNOON:
            results = self._process_afternoon_phase()
        elif self.current_phase == SimulationPhase.EVENING:
            results = self._process_evening_phase()
        elif self.current_phase == SimulationPhase.NIGHT:
            results = self._process_night_phase()

        return results

    def _process_morning_phase(self) -> Dict[str, Any]:
        """Process morning phase - planning and preparation"""
        results = {"events": [], "narrative": []}

        # Morning activities
        for agent_id, agent in self.game_state.agents.items():
            if agent.status == "active":
                # Morning recovery and planning
                if agent.stress > 0:
                    recovery = min(10, agent.stress // 4)
                    agent.stress = max(0, agent.stress - recovery)
                    results["narrative"].append(
                        f"{agent.name} recovers from stress (-{recovery})"
                    )

                # Generate morning tasks
                morning_task = self._generate_morning_task(agent)
                if morning_task:
                    self.agent_schedules[agent_id] = morning_task
                    results["narrative"].append(
                        f"{agent.name} plans {morning_task.activity.value}"
                    )

        results["narrative"].append("=== Morning Phase - Planning and Recovery ===")
        return results

    def _process_afternoon_phase(self) -> Dict[str, Any]:
        """Process afternoon phase - active operations"""
        results = {"events": [], "narrative": []}

        # Execute scheduled activities
        for agent_id, schedule in self.agent_schedules.items():
            if schedule.activity in [
                AgentActivity.MISSION_EXECUTION,
                AgentActivity.SABOTAGE,
                AgentActivity.RECRUITMENT,
                AgentActivity.PROPAGANDA,
            ]:
                activity_result = self._execute_agent_activity(agent_id, schedule)
                results["events"].extend(activity_result["events"])
                results["narrative"].extend(activity_result["narrative"])

        results["narrative"].append("=== Afternoon Phase - Active Operations ===")
        return results

    def _process_evening_phase(self) -> Dict[str, Any]:
        """Process evening phase - intelligence and networking"""
        results = {"events": [], "narrative": []}

        # Evening activities
        for agent_id, schedule in self.agent_schedules.items():
            if schedule.activity in [
                AgentActivity.INTELLIGENCE_GATHERING,
                AgentActivity.NETWORKING,
                AgentActivity.COUNTER_INTELLIGENCE,
            ]:
                activity_result = self._execute_agent_activity(agent_id, schedule)
                results["events"].extend(activity_result["events"])
                results["narrative"].extend(activity_result["narrative"])

        results["narrative"].append(
            "=== Evening Phase - Intelligence and Networking ==="
        )
        return results

    def _process_night_phase(self) -> Dict[str, Any]:
        """Process night phase - stealth operations and rest"""
        results = {"events": [], "narrative": []}

        # Night activities
        for agent_id, schedule in self.agent_schedules.items():
            if schedule.activity in [
                AgentActivity.INFILTRATION,
                AgentActivity.ESCAPE,
                AgentActivity.HIDING,
                AgentActivity.REST,
            ]:
                activity_result = self._execute_agent_activity(agent_id, schedule)
                results["events"].extend(activity_result["events"])
                results["narrative"].extend(activity_result["narrative"])

        # Night recovery for all agents
        for agent_id, agent in self.game_state.agents.items():
            if agent.status == "active":
                night_recovery = min(15, agent.stress // 3)
                agent.stress = max(0, agent.stress - night_recovery)

        results["narrative"].append("=== Night Phase - Stealth Operations and Rest ===")
        return results

    def _process_relationships(self) -> Dict[str, Any]:
        """Process relationship dynamics between agents"""
        results = {"events": [], "narrative": []}

        # Process relationship queue
        for agent1_id, agent2_id in self.relationship_processing_queue[
            :10
        ]:  # Process 10 per phase
            if (
                agent1_id in self.game_state.agents
                and agent2_id in self.game_state.agents
            ):
                relationship_result = self._process_agent_relationship(
                    agent1_id, agent2_id
                )
                results["events"].extend(relationship_result["events"])
                results["narrative"].extend(relationship_result["narrative"])
                self.performance_metrics["relationships_updated"] += 1

        # Remove processed relationships
        self.relationship_processing_queue = self.relationship_processing_queue[10:]

        # Generate new relationship interactions
        new_interactions = self._generate_relationship_interactions()
        self.relationship_processing_queue.extend(new_interactions)

        return results

    def _process_intelligence(self) -> Dict[str, Any]:
        """Process intelligence gathering and analysis"""
        results = {"events": [], "narrative": []}

        # Update intelligence freshness
        for report in self.intelligence_reports:
            report.freshness = max(0.0, report.freshness - 0.1)
            if report.freshness <= 0.0:
                results["narrative"].append(
                    f"Intelligence report {report.id} has expired"
                )

        # Remove expired intelligence
        self.intelligence_reports = [
            r for r in self.intelligence_reports if r.freshness > 0.0
        ]

        # Process intelligence gathering activities
        for agent_id, schedule in self.agent_schedules.items():
            if schedule.activity == AgentActivity.INTELLIGENCE_GATHERING:
                intel_result = self._gather_intelligence(agent_id, schedule)
                results["events"].extend(intel_result["events"])
                results["narrative"].extend(intel_result["narrative"])
                self.performance_metrics["intelligence_gathered"] += 1

        return results

    def _process_counter_intelligence(self) -> Dict[str, Any]:
        """Process counter-intelligence operations"""
        results = {"events": [], "narrative": []}

        # Update counter-intelligence operations
        for op in self.counter_intelligence_ops:
            op.duration -= 1
            if op.duration <= 0:
                # Resolve operation
                op_result = self._resolve_counter_intelligence_operation(op)
                results["events"].extend(op_result["events"])
                results["narrative"].extend(op_result["narrative"])

        # Remove completed operations
        self.counter_intelligence_ops = [
            op for op in self.counter_intelligence_ops if op.duration > 0
        ]

        return results

    def _process_faction_dynamics(self) -> Dict[str, Any]:
        """Process faction-level dynamics and politics"""
        results = {"events": [], "narrative": []}

        self.faction_dynamics_timer += 1
        if self.faction_dynamics_timer >= 4:  # Every 4 phases
            self.faction_dynamics_timer = 0

            for faction_id, faction in self.game_state.factions.items():
                # Update faction cohesion
                cohesion_result = self._update_faction_cohesion(faction_id)
                results["events"].extend(cohesion_result["events"])
                results["narrative"].extend(cohesion_result["narrative"])

                # Check for faction fractures
                fracture_result = self._check_faction_fractures(faction_id)
                results["events"].extend(fracture_result["events"])
                results["narrative"].extend(fracture_result["narrative"])

        return results

    def _process_world_events(self) -> Dict[str, Any]:
        """Process world events and their effects"""
        results = {"events": [], "narrative": []}

        # Update active events
        for event in self.active_world_events:
            event.duration -= 1
            if event.duration <= 0:
                # Event expires
                results["narrative"].append(
                    f"World event '{event.description}' has ended"
                )
            else:
                # Apply ongoing effects
                effects_result = self._apply_world_event_effects(event)
                results["events"].extend(effects_result["events"])
                results["narrative"].extend(effects_result["narrative"])

        # Remove expired events
        self.active_world_events = [
            e for e in self.active_world_events if e.duration > 0
        ]

        # Generate new world events
        if random.random() < 0.1:  # 10% chance per phase
            new_event = self._generate_world_event()
            if new_event:
                self.active_world_events.append(new_event)
                results["events"].append(new_event)
                results["narrative"].append(f"New world event: {new_event.description}")
                self.performance_metrics["events_generated"] += 1

        return results

    def _generate_morning_task(self, agent: Agent) -> Optional[AgentSchedule]:
        """Generate a morning task for an agent"""
        # Simple task generation based on agent status and faction goals
        faction = self.game_state.factions.get(agent.faction_id)
        if not faction:
            return None

        # Determine activity based on faction goal
        goal_activities = {
            "expand_influence": [AgentActivity.PROPAGANDA, AgentActivity.NETWORKING],
            "recruit_members": [AgentActivity.RECRUITMENT, AgentActivity.NETWORKING],
            "gather_intelligence": [
                AgentActivity.INTELLIGENCE_GATHERING,
                AgentActivity.INFILTRATION,
            ],
            "disrupt_government": [
                AgentActivity.SABOTAGE,
                AgentActivity.MISSION_PLANNING,
            ],
            "protect_territory": [
                AgentActivity.COUNTER_INTELLIGENCE,
                AgentActivity.TRAINING,
            ],
        }

        available_activities = goal_activities.get(
            faction.current_goal, [AgentActivity.REST]
        )
        chosen_activity = random.choice(available_activities)

        # Find suitable location
        suitable_locations = [
            loc_id
            for loc_id, location in self.game_state.locations.items()
            if location.security_level
            < 7  # Avoid high-security areas for morning activities
        ]

        if not suitable_locations:
            return None

        location_id = random.choice(suitable_locations)

        return AgentSchedule(
            agent_id=agent.id,
            activity=chosen_activity,
            location_id=location_id,
            duration=1,
            priority=random.randint(1, 3),
            risk_level=random.randint(1, 3),
        )

    def _execute_agent_activity(
        self, agent_id: str, schedule: AgentSchedule
    ) -> Dict[str, Any]:
        """Execute an agent's scheduled activity"""
        results = {"events": [], "narrative": []}

        agent = self.game_state.agents.get(agent_id)
        if not agent or agent.status != "active":
            return results

        # Calculate success chance based on activity type
        success_chance = self._calculate_activity_success_chance(agent, schedule)

        # Roll for success
        roll = random.random()
        success = roll <= success_chance

        # Generate narrative
        activity_narrative = self._generate_activity_narrative(agent, schedule, success)
        results["narrative"].append(activity_narrative)

        # Apply outcomes
        outcomes = self._apply_activity_outcomes(agent, schedule, success)
        results["events"].extend(outcomes["events"])
        results["narrative"].extend(outcomes["narrative"])

        # Update agent
        self._update_agent_from_activity(agent, schedule, success)

        return results

    def _calculate_activity_success_chance(
        self, agent: Agent, schedule: AgentSchedule
    ) -> float:
        """Calculate success chance for an activity"""
        base_chance = 0.5

        # Skill modifiers
        skill_modifier = 0.0
        if schedule.activity == AgentActivity.SABOTAGE:
            skill_modifier = agent.get_skill_level("technical") * 0.05
        elif schedule.activity == AgentActivity.INTELLIGENCE_GATHERING:
            skill_modifier = agent.get_skill_level("intelligence") * 0.05
        elif schedule.activity == AgentActivity.RECRUITMENT:
            skill_modifier = agent.get_skill_level("persuasion") * 0.05
        elif schedule.activity == AgentActivity.PROPAGANDA:
            skill_modifier = agent.get_skill_level("persuasion") * 0.05

        # Location modifiers
        location = self.game_state.locations.get(schedule.location_id)
        location_modifier = 0.0
        if location:
            if schedule.activity in [
                AgentActivity.SABOTAGE,
                AgentActivity.INFILTRATION,
            ]:
                location_modifier = -(location.security_level - 5) * 0.1
            elif schedule.activity == AgentActivity.PROPAGANDA:
                location_modifier = (location.unrest_level - 5) * 0.1

        # Stress penalty
        stress_penalty = -(agent.stress / 100.0) * 0.3

        # Equipment bonus
        equipment_bonus = 0.0
        for equipment in agent.equipment:
            if equipment.condition > 50:
                equipment_bonus += 0.05

        final_chance = (
            base_chance
            + skill_modifier
            + location_modifier
            + stress_penalty
            + equipment_bonus
        )
        return max(0.05, min(0.95, final_chance))

    def _generate_activity_narrative(
        self, agent: Agent, schedule: AgentSchedule, success: bool
    ) -> str:
        """Generate narrative for an activity"""
        location_name = self.game_state.locations.get(
            schedule.location_id, "unknown location"
        ).name

        activity_descriptions = {
            AgentActivity.SABOTAGE: f"{agent.name} attempts sabotage at {location_name}",
            AgentActivity.INTELLIGENCE_GATHERING: f"{agent.name} gathers intelligence at {location_name}",
            AgentActivity.RECRUITMENT: f"{agent.name} attempts recruitment at {location_name}",
            AgentActivity.PROPAGANDA: f"{agent.name} spreads propaganda at {location_name}",
            AgentActivity.INFILTRATION: f"{agent.name} infiltrates {location_name}",
            AgentActivity.REST: f"{agent.name} rests and recovers",
            AgentActivity.TRAINING: f"{agent.name} trains and improves skills",
        }

        base_description = activity_descriptions.get(
            schedule.activity, f"{agent.name} performs {schedule.activity.value}"
        )

        if success:
            return f"✅ {base_description} - Success!"
        else:
            return f"❌ {base_description} - Failed!"

    def _apply_activity_outcomes(
        self, agent: Agent, schedule: AgentSchedule, success: bool
    ) -> Dict[str, Any]:
        """Apply the outcomes of an activity"""
        results = {"events": [], "narrative": []}

        if success:
            # Success outcomes
            if schedule.activity == AgentActivity.SABOTAGE:
                # Reduce location security
                location = self.game_state.locations.get(schedule.location_id)
                if location:
                    location.security_level = max(1, location.security_level - 1)
                    results["narrative"].append(f"Security reduced at {location.name}")

            elif schedule.activity == AgentActivity.INTELLIGENCE_GATHERING:
                # Generate intelligence report
                intel_report = self._create_intelligence_report(
                    agent, schedule.location_id
                )
                self.intelligence_reports.append(intel_report)
                results["narrative"].append(
                    f"Intelligence gathered: {intel_report.content[:50]}..."
                )

            elif schedule.activity == AgentActivity.RECRUITMENT:
                # Add resources to faction
                faction = self.game_state.factions.get(agent.faction_id)
                if faction:
                    faction.gain_resources({"personnel": 1})
                    results["narrative"].append(f"New recruit joins {faction.name}")

            elif schedule.activity == AgentActivity.PROPAGANDA:
                # Increase unrest
                location = self.game_state.locations.get(schedule.location_id)
                if location:
                    location.unrest_level = min(10, location.unrest_level + 1)
                    results["narrative"].append(f"Unrest increased at {location.name}")

            # Skill improvement
            skill_gain = random.randint(5, 15)
            if schedule.activity == AgentActivity.SABOTAGE:
                agent.gain_skill_experience("technical", skill_gain)
            elif schedule.activity == AgentActivity.INTELLIGENCE_GATHERING:
                agent.gain_skill_experience("intelligence", skill_gain)
            elif schedule.activity == AgentActivity.RECRUITMENT:
                agent.gain_skill_experience("persuasion", skill_gain)

            # Stress reduction from success
            agent.stress = max(0, agent.stress - 5)

        else:
            # Failure outcomes
            agent.stress = min(100, agent.stress + 10)

            # Risk of detection
            if random.random() < 0.2:  # 20% chance of detection
                detection_result = self._handle_agent_detection(agent, schedule)
                results["events"].extend(detection_result["events"])
                results["narrative"].extend(detection_result["narrative"])

        return results

    def _update_agent_from_activity(
        self, agent: Agent, schedule: AgentSchedule, success: bool
    ):
        """Update agent state based on activity"""
        # Equipment degradation
        for equipment in agent.equipment:
            if random.random() < 0.1:  # 10% chance of degradation
                equipment.condition = max(0, equipment.condition - 5)

        # Experience gain
        if success:
            agent.experience_points += random.randint(10, 25)

        # Update last activity
        agent.last_task_phase = self.phase_number

    def _create_intelligence_report(
        self, agent: Agent, location_id: str
    ) -> IntelligenceReport:
        """Create an intelligence report"""
        location = self.game_state.locations.get(location_id, "Unknown Location")

        intel_types = ["security", "personnel", "resources", "plans"]
        intel_type = random.choice(intel_types)

        content_templates = {
            "security": [
                f"Security patrols at {location} follow a {random.choice(['regular', 'irregular', 'predictable'])} pattern",
                f"Security systems at {location} appear to be {random.choice(['basic', 'advanced', 'outdated'])}",
                f"Guard rotation at {location} occurs every {random.randint(2, 8)} hours",
            ],
            "personnel": [
                f"Estimated {random.randint(5, 50)} personnel at {location}",
                f"Key personnel at {location} include {random.choice(['military officers', 'civilian staff', 'security personnel'])}",
                f"Staff morale at {location} appears {random.choice(['high', 'low', 'mixed'])}",
            ],
            "resources": [
                f"Significant {random.choice(['weapons', 'supplies', 'vehicles', 'communications equipment'])} at {location}",
                f"Resource stockpiles at {location} are {random.choice(['well-maintained', 'depleted', 'overstocked'])}",
                f"Supply routes to {location} are {random.choice(['vulnerable', 'heavily defended', 'unknown'])}",
            ],
            "plans": [
                f"Rumors of {random.choice(['military operation', 'security crackdown', 'personnel transfer'])} at {location}",
                f"Planned {random.choice(['maintenance', 'upgrade', 'expansion'])} at {location} in coming weeks",
                f"Strategic importance of {location} appears to be {random.choice(['high', 'medium', 'low'])}",
            ],
        }

        content = random.choice(content_templates[intel_type])

        return IntelligenceReport(
            id=f"intel_{len(self.intelligence_reports) + 1}",
            source_agent_id=agent.id,
            target_location_id=location_id,
            intelligence_type=intel_type,
            content=content,
            reliability=random.uniform(0.6, 0.9),
            freshness=1.0,
            access_level=random.randint(1, 3),
            gathered_turn=self.turn_number,
            expires_turn=self.turn_number + random.randint(5, 15),
        )

    def _handle_agent_detection(
        self, agent: Agent, schedule: AgentSchedule
    ) -> Dict[str, Any]:
        """Handle agent detection by authorities"""
        results = {"events": [], "narrative": []}

        # Determine detection severity
        severity = random.random()

        if severity < 0.3:
            # Minor detection - increased suspicion
            results["narrative"].append(f"{agent.name} attracts minor suspicion")
            agent.stress += 15

        elif severity < 0.7:
            # Moderate detection - pursuit
            results["narrative"].append(f"{agent.name} is pursued by authorities")
            agent.stress += 25

            # Chance of capture
            if random.random() < 0.3:
                agent.status = "captured"
                results["narrative"].append(f"{agent.name} has been captured!")
                results["events"].append(
                    {
                        "type": "agent_captured",
                        "agent_id": agent.id,
                        "location_id": schedule.location_id,
                    }
                )

        else:
            # Major detection - immediate capture
            agent.status = "captured"
            results["narrative"].append(f"{agent.name} has been captured!")
            results["events"].append(
                {
                    "type": "agent_captured",
                    "agent_id": agent.id,
                    "location_id": schedule.location_id,
                }
            )

        return results

    def _process_agent_relationship(
        self, agent1_id: str, agent2_id: str
    ) -> Dict[str, Any]:
        """Process relationship dynamics between two agents"""
        results = {"events": [], "narrative": []}

        agent1 = self.game_state.agents.get(agent1_id)
        agent2 = self.game_state.agents.get(agent2_id)

        if not agent1 or not agent2:
            return results

        # Get or create relationship
        relationship = self._get_or_create_relationship(agent1_id, agent2_id)

        # Process relationship changes
        trust_change = random.randint(-5, 5)
        loyalty_change = random.randint(-3, 3)

        relationship.trust = max(0, min(100, relationship.trust + trust_change))
        relationship.loyalty = max(0, min(100, relationship.loyalty + loyalty_change))

        # Generate relationship narrative
        if abs(trust_change) > 3 or abs(loyalty_change) > 2:
            narrative = self._generate_relationship_narrative(
                agent1, agent2, trust_change, loyalty_change
            )
            results["narrative"].append(narrative)

        return results

    def _get_or_create_relationship(
        self, agent1_id: str, agent2_id: str
    ) -> Relationship:
        """Get existing relationship or create new one"""
        # This would integrate with the existing relationship system
        # For now, create a simple relationship
        return Relationship(
            agent1_id=agent1_id,
            agent2_id=agent2_id,
            trust=50,
            loyalty=50,
            affinity=0,
            bond_type="acquaintance",
        )

    def _generate_relationship_narrative(
        self, agent1: Agent, agent2: Agent, trust_change: int, loyalty_change: int
    ) -> str:
        """Generate narrative for relationship changes"""
        if trust_change > 0 and loyalty_change > 0:
            return f"🤝 {agent1.name} and {agent2.name} grow closer"
        elif trust_change < 0 and loyalty_change < 0:
            return f"💔 {agent1.name} and {agent2.name} grow distant"
        elif trust_change > 0:
            return f"🤝 {agent1.name} gains trust in {agent2.name}"
        elif loyalty_change > 0:
            return f"💪 {agent1.name} shows loyalty to {agent2.name}"
        else:
            return f"😐 {agent1.name} and {agent2.name} have mixed feelings"

    def _generate_relationship_interactions(self) -> List[Tuple[str, str]]:
        """Generate new relationship interactions"""
        interactions = []

        # Find agents in same locations
        location_agents = {}
        for agent_id, agent in self.game_state.agents.items():
            if agent.status == "active":
                if agent.location_id not in location_agents:
                    location_agents[agent.location_id] = []
                location_agents[agent.location_id].append(agent_id)

        # Generate interactions for agents in same locations
        for location_id, agent_ids in location_agents.items():
            if len(agent_ids) >= 2:
                # Randomly pair agents
                for _ in range(
                    min(3, len(agent_ids) // 2)
                ):  # Max 3 interactions per location
                    if len(agent_ids) >= 2:
                        agent1 = random.choice(agent_ids)
                        agent_ids.remove(agent1)
                        agent2 = random.choice(agent_ids)
                        agent_ids.remove(agent2)
                        interactions.append((agent1, agent2))

        return interactions

    def _gather_intelligence(
        self, agent_id: str, schedule: AgentSchedule
    ) -> Dict[str, Any]:
        """Process intelligence gathering activity"""
        results = {"events": [], "narrative": []}

        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return results

        # Create intelligence report
        intel_report = self._create_intelligence_report(agent, schedule.location_id)
        self.intelligence_reports.append(intel_report)

        results["narrative"].append(
            f"📊 {agent.name} gathers intelligence: {intel_report.content[:50]}..."
        )

        return results

    def _resolve_counter_intelligence_operation(
        self, operation: CounterIntelligenceOperation
    ) -> Dict[str, Any]:
        """Resolve a counter-intelligence operation"""
        results = {"events": [], "narrative": []}

        # Roll for success
        success = random.random() <= operation.success_chance

        target_agent = self.game_state.agents.get(operation.target_agent_id)
        if not target_agent:
            return results

        if success:
            # Operation successful
            if operation.operation_type == "surveillance":
                results["narrative"].append(
                    f"🔍 {target_agent.name} is under surveillance"
                )
                target_agent.stress += 20
            elif operation.operation_type == "interrogation":
                results["narrative"].append(f"🚨 {target_agent.name} is interrogated")
                target_agent.stress += 40
                if random.random() < 0.3:
                    target_agent.status = "captured"
                    results["narrative"].append(
                        f"{target_agent.name} has been captured!"
                    )
            elif operation.operation_type == "infiltration":
                results["narrative"].append(
                    f"🕵️ Counter-intelligence infiltrates {target_agent.name}'s network"
                )
        else:
            # Operation failed
            results["narrative"].append(
                f"❌ Counter-intelligence operation against {target_agent.name} fails"
            )

        return results

    def _update_faction_cohesion(self, faction_id: str) -> Dict[str, Any]:
        """Update faction cohesion based on member relationships"""
        results = {"events": [], "narrative": []}

        faction = self.game_state.factions.get(faction_id)
        if not faction:
            return results

        # Calculate cohesion based on member relationships
        faction_members = [
            a for a in self.game_state.agents.values() if a.faction_id == faction_id
        ]

        if len(faction_members) < 2:
            return results

        # Simple cohesion calculation (would be more complex in full implementation)
        avg_loyalty = sum(member.loyalty for member in faction_members) / len(
            faction_members
        )

        # Update faction resources based on cohesion
        if avg_loyalty > 70:
            faction.gain_resources({"influence": 5})
            results["narrative"].append(
                f"{faction.name} gains influence from high cohesion"
            )
        elif avg_loyalty < 30:
            faction.spend_resources({"influence": 5})
            results["narrative"].append(
                f"{faction.name} loses influence from low cohesion"
            )

        return results

    def _check_faction_fractures(self, faction_id: str) -> Dict[str, Any]:
        """Check for faction fractures and splits"""
        results = {"events": [], "narrative": []}

        faction = self.game_state.factions.get(faction_id)
        if not faction:
            return results

        faction_members = [
            a for a in self.game_state.agents.values() if a.faction_id == faction_id
        ]

        if len(faction_members) < 3:
            return results

        # Check for low cohesion
        avg_loyalty = sum(member.loyalty for member in faction_members) / len(
            faction_members
        )

        if (
            avg_loyalty < 25 and random.random() < 0.1
        ):  # 10% chance if cohesion is very low
            # Faction fractures
            results["narrative"].append(
                f"💥 {faction.name} fractures due to low cohesion!"
            )

            # Create splinter faction
            splinter_members = [m for m in faction_members if m.loyalty < 30]
            if splinter_members:
                results["events"].append(
                    {
                        "type": "faction_fracture",
                        "original_faction": faction_id,
                        "splinter_members": [m.id for m in splinter_members],
                    }
                )

        return results

    def _apply_world_event_effects(self, event: WorldEvent) -> Dict[str, Any]:
        """Apply ongoing effects of a world event"""
        results = {"events": [], "narrative": []}

        # Apply effects to affected factions
        for faction_id in event.affected_factions:
            faction = self.game_state.factions.get(faction_id)
            if faction:
                if event.event_type == WorldEventType.SECURITY_CRACKDOWN:
                    faction.spend_resources({"influence": 10})
                elif event.event_type == WorldEventType.CIVIL_UNREST:
                    faction.gain_resources({"influence": 5})
                elif event.event_type == WorldEventType.ECONOMIC_CRISIS:
                    faction.spend_resources({"money": 50})

        # Apply effects to locations
        if event.location_id:
            location = self.game_state.locations.get(event.location_id)
            if location:
                if event.event_type == WorldEventType.SECURITY_CRACKDOWN:
                    location.security_level = min(10, location.security_level + 2)
                elif event.event_type == WorldEventType.CIVIL_UNREST:
                    location.unrest_level = min(10, location.unrest_level + 3)

        return results

    def _generate_world_event(self) -> Optional[WorldEvent]:
        """Generate a new world event"""
        event_type = random.choice(list(WorldEventType))

        # Select location
        location_id = (
            random.choice(list(self.game_state.locations.keys()))
            if self.game_state.locations
            else None
        )

        # Select affected factions
        affected_factions = random.sample(
            list(self.game_state.factions.keys()), min(2, len(self.game_state.factions))
        )

        # Generate description
        descriptions = {
            WorldEventType.SECURITY_CRACKDOWN: "Government launches major security crackdown",
            WorldEventType.CIVIL_UNREST: "Civil unrest spreads across the city",
            WorldEventType.ECONOMIC_CRISIS: "Economic crisis affects all factions",
            WorldEventType.MEDIA_SCANDAL: "Major media scandal rocks the establishment",
            WorldEventType.NATURAL_DISASTER: "Natural disaster disrupts operations",
        }

        description = descriptions.get(
            event_type, f"{event_type.value.replace('_', ' ').title()} occurs"
        )

        return WorldEvent(
            id=f"event_{len(self.active_world_events) + 1}",
            event_type=event_type,
            location_id=location_id,
            affected_factions=affected_factions,
            description=description,
            severity=random.uniform(0.3, 0.8),
            duration=random.randint(2, 6),
            political_impact=random.uniform(-0.5, 0.5),
        )

    def _advance_phase(self):
        """Advance to the next simulation phase"""
        phases = list(SimulationPhase)
        current_index = phases.index(self.current_phase)

        if current_index < len(phases) - 1:
            self.current_phase = phases[current_index + 1]
        else:
            # Start new turn
            self.turn_number += 1
            self.current_phase = SimulationPhase.MORNING

        self.phase_number += 1

    def get_simulation_status(self) -> Dict[str, Any]:
        """Get comprehensive simulation status"""
        return {
            "turn": self.turn_number,
            "phase": self.current_phase.value,
            "phase_number": self.phase_number,
            "active_agents": len(
                [a for a in self.game_state.agents.values() if a.status == "active"]
            ),
            "scheduled_activities": len(self.agent_schedules),
            "intelligence_reports": len(self.intelligence_reports),
            "counter_intelligence_ops": len(self.counter_intelligence_ops),
            "active_world_events": len(self.active_world_events),
            "pending_relationships": len(self.relationship_processing_queue),
            "performance_metrics": self.performance_metrics.copy(),
            "enabled_features": {
                "relationship_processing": self.enable_relationship_processing,
                "intelligence_system": self.enable_intelligence_system,
                "counter_intelligence": self.enable_counter_intelligence,
                "dynamic_events": self.enable_dynamic_events,
                "faction_dynamics": self.enable_faction_dynamics,
            },
        }
