"""
Years of Lead - Mission Execution System

This module implements the turn-based tactical resolution engine for missions,
with phase-based execution, psychological integration, and emergent narrative events.
Inspired by XCOM's tactical depth and RimWorld's narrative generation.
"""

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from .emotional_state import EmotionalState, TraumaTriggerType, TherapyType
from .relationship_system import RelationshipEvent, RelationshipManager
from .character_creation import Character, PersonalityTrait
from .legal_system import CrimeType, LegalSystem
from .intelligence_system import IntelligenceDatabase, IntelligenceEvent


logger = logging.getLogger(__name__)


class MissionPhase(Enum):
    """Phases of mission execution"""
    PLANNING = "planning"
    INFILTRATION = "infiltration"
    EXECUTION = "execution"
    EXTRACTION = "extraction"
    AFTERMATH = "aftermath"


class ActionType(Enum):
    """Types of actions agents can take"""
    STEALTH = "stealth"
    COMBAT = "combat"
    HACKING = "hacking"
    SOCIAL = "social"
    SABOTAGE = "sabotage"
    RECONNAISSANCE = "reconnaissance"
    ESCAPE = "escape"
    SUPPORT = "support"
    LEADERSHIP = "leadership"


class MissionOutcome(Enum):
    """Overall mission outcomes"""
    CRITICAL_SUCCESS = "critical_success"
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    DISASTER = "disaster"
    ABORTED = "aborted"


class ComplicationSeverity(Enum):
    """Severity of complications"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CATASTROPHIC = "catastrophic"


class EmotionalTone(Enum):
    """Emotional tone of mission outcomes for narrative variety"""
    TRIUMPHANT_VICTORY = "triumphant_victory"     # Overwhelming success
    HEROIC_SACRIFICE = "heroic_sacrifice"         # Success through sacrifice  
    TACTICAL_WITHDRAWAL = "tactical_withdrawal"   # Strategic retreat
    DESPERATE_STRUGGLE = "desperate_struggle"     # Barely surviving
    BITTERSWEET_SUCCESS = "bittersweet_success"   # Won but at great cost
    PYRRHIC_VICTORY = "pyrrhic_victory"          # Victory too costly
    FEARFUL_RETREAT = "fearful_retreat"          # Panicked escape
    BETRAYAL_TRAGEDY = "betrayal_tragedy"        # Betrayed by own
    REDEMPTIVE_MOMENT = "redemptive_moment"      # Agent redeems themselves
    AMBIGUOUS_OUTCOME = "ambiguous_outcome"      # Unclear success/failure


@dataclass
class MissionAction:
    """Represents a single action taken during a mission"""
    phase: MissionPhase
    agent_id: str
    action_type: ActionType
    timestamp: datetime
    success: bool
    details: Dict[str, Any]
    narrative: str
    consequences: List[str] = field(default_factory=list)
    
    def to_log_entry(self) -> str:
        """Convert to narrative log entry"""
        status = "✓" if self.success else "✗"
        return f"[{self.phase.value.upper()}] {status} {self.narrative}"


@dataclass
class MissionComplication:
    """Represents an unexpected complication during a mission"""
    phase: MissionPhase
    severity: ComplicationSeverity
    description: str
    affected_agents: List[str]
    resolution_required: bool
    narrative_hook: str
    
    def generate_narrative(self) -> str:
        """Generate narrative description of the complication"""
        severity_descriptors = {
            ComplicationSeverity.MINOR: "slight hiccup",
            ComplicationSeverity.MODERATE: "unexpected challenge",
            ComplicationSeverity.MAJOR: "serious problem",
            ComplicationSeverity.CATASTROPHIC: "complete disaster"
        }
        
        return f"A {severity_descriptors[self.severity]}: {self.description}"


@dataclass
class AgentPerformance:
    """Track individual agent performance during mission"""
    agent_id: str
    actions_taken: List[MissionAction]
    stress_gained: float
    trauma_triggered: bool
    relationships_affected: Dict[str, float]  # agent_id -> relationship change
    betrayal_attempted: bool
    heroic_moment: bool
    panic_episodes: int
    disobedience_count: int
    crimes_committed: List[CrimeType]
    
    def calculate_performance_score(self) -> float:
        """Calculate overall performance rating"""
        successful_actions = sum(1 for action in self.actions_taken if action.success)
        total_actions = len(self.actions_taken)
        
        if total_actions == 0:
            return 0.5
        
        base_score = successful_actions / total_actions
        
        # Modifiers
        if self.heroic_moment:
            base_score += 0.2
        if self.betrayal_attempted:
            base_score -= 0.5
        if self.panic_episodes > 0:
            base_score -= 0.1 * self.panic_episodes
        if self.disobedience_count > 0:
            base_score -= 0.05 * self.disobedience_count
        
        return max(0.0, min(1.0, base_score))


@dataclass
class MissionReport:
    """Complete mission execution report"""
    mission_id: str
    start_time: datetime
    end_time: datetime
    phases_completed: List[MissionPhase]
    outcome: MissionOutcome
    
    # Detailed tracking
    action_log: List[MissionAction]
    complications: List[MissionComplication]
    agent_performance: Dict[str, AgentPerformance]
    
    # Outcomes
    objectives_completed: List[str]
    objectives_failed: List[str]
    casualties: List[str]  # agent_ids
    captured_agents: List[str]
    
    # Consequences
    heat_generated: int
    public_opinion_shift: float
    resources_gained: Dict[str, int]
    resources_lost: Dict[str, int]
    
    # Narrative elements
    narrative_summary: str
    memorable_moments: List[str]
    propaganda_value: float
    symbolic_impact: str
    emotional_tone: Optional[EmotionalTone] = None  # New narrative tone tracking
    
    def generate_full_report(self) -> str:
        """Generate comprehensive narrative report"""
        report = f"MISSION REPORT: {self.mission_id}\n"
        report += f"{'=' * 60}\n\n"
        
        report += f"Outcome: {self.outcome.value.replace('_', ' ').upper()}\n"
        report += f"Duration: {(self.end_time - self.start_time).total_seconds() / 60:.1f} minutes\n\n"
        
        report += "NARRATIVE SUMMARY:\n"
        report += f"{self.narrative_summary}\n\n"
        
        if self.memorable_moments:
            report += "MEMORABLE MOMENTS:\n"
            for moment in self.memorable_moments:
                report += f"• {moment}\n"
            report += "\n"
        
        report += "AGENT PERFORMANCE:\n"
        for agent_id, performance in self.agent_performance.items():
            score = performance.calculate_performance_score()
            report += f"• Agent {agent_id}: {score:.1%} effectiveness\n"
            if performance.heroic_moment:
                report += "  ⭐ Displayed exceptional heroism\n"
            if performance.betrayal_attempted:
                report += "  ⚠️  Attempted betrayal\n"
            if performance.panic_episodes > 0:
                report += f"  😰 Suffered {performance.panic_episodes} panic episodes\n"
        
        report += f"\nHeat Generated: +{self.heat_generated}\n"
        report += f"Public Opinion: {self.public_opinion_shift:+.1%}\n"
        
        if self.casualties or self.captured_agents:
            report += "\nLOSSES:\n"
            for agent_id in self.casualties:
                report += f"• {agent_id} - KIA\n"
            for agent_id in self.captured_agents:
                report += f"• {agent_id} - Captured\n"
        
        return report


class MissionExecutor:
    """Handles the execution of missions with phase-based resolution"""
    
    def __init__(self, 
                 legal_system: LegalSystem,
                 intelligence_system: IntelligenceDatabase,
                 relationship_manager: RelationshipManager):
        self.legal_system = legal_system
        self.intelligence_system = intelligence_system
        self.relationship_manager = relationship_manager
        self.narrative_generator = NarrativeGenerator()  # Initialize enhanced generator
        logger.info("MissionExecutor initialized")
    
    def execute_mission(self,
                       mission: Any,  # Mission object from existing system
                       agents: List[Character],
                       location: Any,
                       equipment: Dict[str, Any]) -> MissionReport:
        """Execute a complete mission through all phases"""
        logger.info(f"Executing mission {mission.id} with {len(agents)} agents")
        
        # Initialize mission tracking
        report = MissionReport(
            mission_id=mission.id,
            start_time=datetime.now(),
            end_time=datetime.now(),  # Will be updated
            phases_completed=[],
            outcome=MissionOutcome.FAILURE,  # Default, will be updated
            action_log=[],
            complications=[],
            agent_performance={agent.id: self._init_agent_performance(agent.id) for agent in agents},
            objectives_completed=[],
            objectives_failed=[],
            casualties=[],
            captured_agents=[],
            heat_generated=0,
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        # Execute each phase
        phases = [
            MissionPhase.PLANNING,
            MissionPhase.INFILTRATION,
            MissionPhase.EXECUTION,
            MissionPhase.EXTRACTION,
            MissionPhase.AFTERMATH
        ]
        
        mission_aborted = False
        
        for phase in phases:
            if mission_aborted:
                break
            
            logger.info(f"Executing phase: {phase.value}")
            phase_result = self._execute_phase(phase, mission, agents, location, equipment, report)
            
            report.phases_completed.append(phase)
            
            # Check for mission abort conditions
            if phase_result.get("abort_mission", False):
                mission_aborted = True
                report.outcome = MissionOutcome.ABORTED
            
            # Update agent states after each phase
            self._update_agent_states(agents, phase_result, report)
            
            # Check for cascading failures
            if self._check_cascade_failure(agents, report):
                mission_aborted = True
                report.outcome = MissionOutcome.DISASTER
        
        # Finalize mission
        report.end_time = datetime.now()
        
        # Calculate final mission outcome
        report.outcome = self._calculate_final_outcome(mission, report)
        
        # Determine emotional tone based on the outcome
        report.emotional_tone = self._determine_emotional_tone(report)
        
        # Apply mission consequences to persistent game state
        self._apply_mission_consequences(mission, agents, report)
        
        # Generate narrative summary
        report.narrative_summary = self.narrative_generator.generate_mission_summary(report)
        
        # Calculate propaganda value and symbolic impact
        report.propaganda_value = self._calculate_propaganda_value(report)
        report.symbolic_impact = self._determine_symbolic_impact(mission, report)
        
        # Log the complete report
        self._log_mission_report(report)
        
        return report
    
    def _init_agent_performance(self, agent_id: str) -> AgentPerformance:
        """Initialize performance tracking for an agent"""
        return AgentPerformance(
            agent_id=agent_id,
            actions_taken=[],
            stress_gained=0.0,
            trauma_triggered=False,
            relationships_affected={},
            betrayal_attempted=False,
            heroic_moment=False,
            panic_episodes=0,
            disobedience_count=0,
            crimes_committed=[]
        )
    
    def _execute_phase(self,
                      phase: MissionPhase,
                      mission: Any,
                      agents: List[Character],
                      location: Any,
                      equipment: Dict[str, Any],
                      report: MissionReport) -> Dict[str, Any]:
        """Execute a single phase of the mission"""
        phase_result = {
            "success": True,
            "complications": [],
            "narrative_events": [],
            "abort_mission": False
        }
        
        # Phase-specific execution
        if phase == MissionPhase.PLANNING:
            phase_result = self._execute_planning_phase(mission, agents, report)
        elif phase == MissionPhase.INFILTRATION:
            phase_result = self._execute_infiltration_phase(mission, agents, location, report)
        elif phase == MissionPhase.EXECUTION:
            phase_result = self._execute_execution_phase(mission, agents, location, equipment, report)
        elif phase == MissionPhase.EXTRACTION:
            phase_result = self._execute_extraction_phase(mission, agents, location, report)
        elif phase == MissionPhase.AFTERMATH:
            phase_result = self._execute_aftermath_phase(mission, agents, report)
        
        return phase_result
    
    def _execute_planning_phase(self,
                               mission: Any,
                               agents: List[Character],
                               report: MissionReport) -> Dict[str, Any]:
        """Execute the planning phase"""
        phase_result = {
            "success": True,
            "complications": [],
            "narrative_events": []
        }
        
        # Check for pre-mission relationship conflicts
        for agent in agents:
            # Check relationships with other team members
            for other_agent in agents:
                if agent.id != other_agent.id:
                    relationship = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                    if relationship and relationship.metrics.trust < -0.5:
                        # Serious trust issues
                        complication = MissionComplication(
                            phase=MissionPhase.PLANNING,
                            severity=ComplicationSeverity.MODERATE,
                            description=f"{agent.name} refuses to work with {other_agent.name}",
                            affected_agents=[agent.id, other_agent.id],
                            resolution_required=True,
                            narrative_hook="Deep mistrust threatens mission cohesion"
                        )
                        report.complications.append(complication)
                        phase_result["complications"].append(complication)
                        
                        # Log the conflict
                        action = MissionAction(
                            phase=MissionPhase.PLANNING,
                            agent_id=agent.id,
                            action_type=ActionType.SOCIAL,
                            timestamp=datetime.now(),
                            success=False,
                            details={"conflict_with": other_agent.id},
                            narrative=f"{agent.name} openly questions {other_agent.name}'s loyalty"
                        )
                        report.action_log.append(action)
        
        # Leader gives briefing (if there is one)
        leader = next((a for a in agents if a.traits.primary_trait == PersonalityTrait.LEADER), None)
        if leader:
            # Leadership check based on skills and emotional state
            leadership_effectiveness = (
                leader.skills.social / 10.0 * 0.5 +
                leader.emotional_state.get_social_effectiveness() * 0.3 +
                (1.0 - leader.get_stress_level()) * 0.2
            )
            
            if leadership_effectiveness > 0.6:
                action = MissionAction(
                    phase=MissionPhase.PLANNING,
                    agent_id=leader.id,
                    action_type=ActionType.LEADERSHIP,
                    timestamp=datetime.now(),
                    success=True,
                    details={"effectiveness": leadership_effectiveness},
                    narrative=f"{leader.name} delivers an inspiring briefing that strengthens resolve"
                )
                report.action_log.append(action)
                report.agent_performance[leader.id].actions_taken.append(action)
                
                # Boost morale
                phase_result["narrative_events"].append(
                    "The team's morale improves from strong leadership"
                )
            else:
                action = MissionAction(
                    phase=MissionPhase.PLANNING,
                    agent_id=leader.id,
                    action_type=ActionType.LEADERSHIP,
                    timestamp=datetime.now(),
                    success=False,
                    details={"effectiveness": leadership_effectiveness},
                    narrative=f"{leader.name} struggles to inspire confidence in the plan"
                )
                report.action_log.append(action)
                report.agent_performance[leader.id].actions_taken.append(action)
        
        # Check for ideological conflicts about mission objectives
        for agent in agents:
            if agent.get_ideological_score() < 0.3:
                if random.random() < 0.3:  # 30% chance of voicing doubts
                    action = MissionAction(
                        phase=MissionPhase.PLANNING,
                        agent_id=agent.id,
                        action_type=ActionType.SOCIAL,
                        timestamp=datetime.now(),
                        success=False,
                        details={"doubt_type": "ideological"},
                        narrative=f"{agent.name} questions whether this mission aligns with their values"
                    )
                    report.action_log.append(action)
                    report.agent_performance[agent.id].actions_taken.append(action)
                    report.agent_performance[agent.id].disobedience_count += 1
        
        return phase_result
    
    def _execute_infiltration_phase(self,
                                   mission: Any,
                                   agents: List[Character],
                                   location: Any,
                                   report: MissionReport) -> Dict[str, Any]:
        """Execute the infiltration phase"""
        phase_result = {
            "success": True,
            "complications": [],
            "narrative_events": []
        }
        
        # Determine infiltration difficulty based on location security
        base_difficulty = location.security_level / 10.0
        
        # Each agent attempts infiltration
        infiltration_failures = 0
        
        for agent in agents:
            # Check for trauma triggers (crowds, darkness, etc.)
            possible_triggers = [TraumaTriggerType.CROWDS, TraumaTriggerType.DARKNESS]
            triggered_traumas = agent.check_trauma_triggers(possible_triggers)
            
            if triggered_traumas:
                # Agent experiences trauma flashback
                report.agent_performance[agent.id].trauma_triggered = True
                report.agent_performance[agent.id].panic_episodes += 1
                
                memory, intensity = triggered_traumas[0]
                action = MissionAction(
                    phase=MissionPhase.INFILTRATION,
                    agent_id=agent.id,
                    action_type=ActionType.STEALTH,
                    timestamp=datetime.now(),
                    success=False,
                    details={"trauma_trigger": memory.trauma_type},
                    narrative=f"{agent.name} freezes as traumatic memories of {memory.description} flood back"
                )
                report.action_log.append(action)
                report.agent_performance[agent.id].actions_taken.append(action)
                report.memorable_moments.append(f"{agent.name}'s haunting flashback during infiltration")
                
                infiltration_failures += 1
                continue
            
            # Calculate infiltration success
            stealth_skill = agent.skills.stealth / 10.0
            stress_penalty = agent.get_stress_level() * 0.3
            effectiveness = agent.emotional_state.get_combat_effectiveness()
            
            infiltration_chance = (stealth_skill * 0.5 + effectiveness * 0.3 + 0.2) - stress_penalty
            
            if random.random() < infiltration_chance - base_difficulty:
                # Successful infiltration
                action = MissionAction(
                    phase=MissionPhase.INFILTRATION,
                    agent_id=agent.id,
                    action_type=ActionType.STEALTH,
                    timestamp=datetime.now(),
                    success=True,
                    details={"method": "stealth"},
                    narrative=f"{agent.name} slips past security undetected"
                )
                report.action_log.append(action)
                report.agent_performance[agent.id].actions_taken.append(action)
            else:
                # Failed infiltration
                infiltration_failures += 1
                
                # Determine failure type
                if agent.traits.primary_trait == PersonalityTrait.RECKLESS:
                    action = MissionAction(
                        phase=MissionPhase.INFILTRATION,
                        agent_id=agent.id,
                        action_type=ActionType.STEALTH,
                        timestamp=datetime.now(),
                        success=False,
                        details={"failure_type": "recklessness"},
                        narrative=f"{agent.name} takes an unnecessary risk and alerts a guard"
                    )
                else:
                    action = MissionAction(
                        phase=MissionPhase.INFILTRATION,
                        agent_id=agent.id,
                        action_type=ActionType.STEALTH,
                        timestamp=datetime.now(),
                        success=False,
                        details={"failure_type": "detected"},
                        narrative=f"{agent.name} is spotted by security cameras"
                    )
                
                report.action_log.append(action)
                report.agent_performance[agent.id].actions_taken.append(action)
                
                # Generate heat
                report.heat_generated += 5
        
        # Check if too many failures compromise the mission
        if infiltration_failures > len(agents) / 2:
            complication = MissionComplication(
                phase=MissionPhase.INFILTRATION,
                severity=ComplicationSeverity.MAJOR,
                description="Multiple agents detected during infiltration",
                affected_agents=[a.id for a in agents],
                resolution_required=True,
                narrative_hook="Alarms begin to sound as the infiltration goes sideways"
            )
            report.complications.append(complication)
            phase_result["complications"].append(complication)
            phase_result["success"] = False
            
            # Add dramatic moment
            report.memorable_moments.append("The team's cover blown in a cascade of security alerts")
        
        return phase_result
    
    def _execute_execution_phase(self,
                                mission: Any,
                                agents: List[Character],
                                location: Any,
                                equipment: Dict[str, Any],
                                report: MissionReport) -> Dict[str, Any]:
        """Execute the main mission objectives"""
        phase_result = {
            "success": True,
            "complications": [],
            "narrative_events": []
        }
        
        # Check for betrayal opportunities
        for agent in agents:
            betrayal_check = self._check_for_betrayal(agent, agents, report)
            if betrayal_check["betrayal_occurred"]:
                # Major complication - betrayal!
                betrayer = agent
                report.agent_performance[betrayer.id].betrayal_attempted = True
                
                action = MissionAction(
                    phase=MissionPhase.EXECUTION,
                    agent_id=betrayer.id,
                    action_type=ActionType.COMBAT,
                    timestamp=datetime.now(),
                    success=True,  # From betrayer's perspective
                    details={"betrayal_type": betrayal_check["reason"]},
                    narrative=f"{betrayer.name} turns on the team - {betrayal_check['reason']}!"
                )
                report.action_log.append(action)
                report.agent_performance[betrayer.id].actions_taken.append(action)
                
                # Create major complication
                complication = MissionComplication(
                    phase=MissionPhase.EXECUTION,
                    severity=ComplicationSeverity.CATASTROPHIC,
                    description=f"Betrayal by {betrayer.name}",
                    affected_agents=[a.id for a in agents],
                    resolution_required=True,
                    narrative_hook="In a shocking turn, one of our own becomes the enemy"
                )
                report.complications.append(complication)
                report.memorable_moments.append(f"{betrayer.name}'s devastating betrayal")
                
                # Apply relationship damage to all team members
                for other_agent in agents:
                    if other_agent.id != betrayer.id:
                        self.relationship_manager.apply_group_event(
                            [other_agent.id],
                            RelationshipEvent.BETRAYAL,
                            intensity=1.0,
                            details={"betrayer": betrayer.id}
                        )
                
                phase_result["abort_mission"] = True
                return phase_result
        
        # Execute primary objective
        success_count = 0
        for agent in agents:
            # Skip if already incapacitated or captured  
            if agent.id in report.casualties or agent.id in report.captured_agents:
                continue
                
            if agent.emotional_state.is_psychologically_stable():
                # Agent can act effectively
                skill_check = self._perform_skill_check(agent, mission.required_skills, mission)
                
                if skill_check["success"]:
                    success_count += 1
                    action = MissionAction(
                        phase=MissionPhase.EXECUTION,
                        agent_id=agent.id,
                        action_type=skill_check["action_type"],
                        timestamp=datetime.now(),
                        success=True,
                        details=skill_check["details"],
                        narrative=skill_check["narrative"]
                    )
                    report.action_log.append(action)
                    report.agent_performance[agent.id].actions_taken.append(action)
                    
                    # Check for heroic moment
                    if skill_check.get("heroic", False):
                        report.agent_performance[agent.id].heroic_moment = True
                        report.memorable_moments.append(f"{agent.name}'s heroic {skill_check['action_type'].value}")
                else:
                    # Failed action
                    action = MissionAction(
                        phase=MissionPhase.EXECUTION,
                        agent_id=agent.id,
                        action_type=skill_check["action_type"],
                        timestamp=datetime.now(),
                        success=False,
                        details=skill_check["details"],
                        narrative=skill_check["narrative"]
                    )
                    report.action_log.append(action)
                    report.agent_performance[agent.id].actions_taken.append(action)
            else:
                # Agent having psychological crisis
                report.agent_performance[agent.id].panic_episodes += 1
                action = MissionAction(
                    phase=MissionPhase.EXECUTION,
                    agent_id=agent.id,
                    action_type=ActionType.SUPPORT,
                    timestamp=datetime.now(),
                    success=False,
                    details={"crisis_type": "psychological"},
                    narrative=f"{agent.name} breaks down under pressure, unable to continue"
                )
                report.action_log.append(action)
                report.agent_performance[agent.id].actions_taken.append(action)
        
        # Determine if objectives were met
        required_successes = max(1, len(agents) // 2)
        if success_count >= required_successes:
            report.objectives_completed.append(mission.primary_objective)
            phase_result["success"] = True
        else:
            report.objectives_failed.append(mission.primary_objective)
            phase_result["success"] = False
        
        # Random dramatic events
        if random.random() < 0.3:
            event = self._generate_dramatic_event(agents, location)
            phase_result["narrative_events"].append(event)
            report.memorable_moments.append(event)
        
        return phase_result
    
    def _execute_extraction_phase(self,
                                 mission: Any,
                                 agents: List[Character],
                                 location: Any,
                                 report: MissionReport) -> Dict[str, Any]:
        """Execute the extraction/escape phase"""
        phase_result = {
            "success": True,
            "complications": [],
            "narrative_events": []
        }
        
        # Extraction is harder if mission execution failed or heat is high
        extraction_difficulty = 0.2  # Reduced from 0.3 for better balance
        if not report.objectives_completed:
            extraction_difficulty += 0.15  # Reduced from 0.2
        if report.heat_generated > 10:
            extraction_difficulty += 0.1
        
        agents_escaped = []
        agents_captured = []
        agents_killed = []
        
        for agent in agents:
            # Skip if already incapacitated
            if agent.id in report.casualties:
                continue
            
            # Calculate escape chance
            escape_skill = max(agent.skills.stealth, agent.skills.combat) / 10.0
            panic_penalty = report.agent_performance[agent.id].panic_episodes * 0.1
            effectiveness = agent.emotional_state.get_combat_effectiveness()
            
            escape_chance = (escape_skill * 0.4 + effectiveness * 0.4 + 0.2) - panic_penalty
            
            if random.random() < escape_chance - extraction_difficulty:
                # Successful escape
                agents_escaped.append(agent.id)
                action = MissionAction(
                    phase=MissionPhase.EXTRACTION,
                    agent_id=agent.id,
                    action_type=ActionType.ESCAPE,
                    timestamp=datetime.now(),
                    success=True,
                    details={"method": "tactical_withdrawal"},
                    narrative=f"{agent.name} successfully escapes the area"
                )
                report.action_log.append(action)
                report.agent_performance[agent.id].actions_taken.append(action)
            else:
                # Failed escape - captured or worse
                if random.random() < 0.8:  # 80% captured, 20% killed
                    agents_captured.append(agent.id)
                    report.captured_agents.append(agent.id)
                    
                    action = MissionAction(
                        phase=MissionPhase.EXTRACTION,
                        agent_id=agent.id,
                        action_type=ActionType.ESCAPE,
                        timestamp=datetime.now(),
                        success=False,
                        details={"outcome": "captured"},
                        narrative=f"{agent.name} is surrounded and captured by security forces"
                    )
                    report.action_log.append(action)
                    report.agent_performance[agent.id].actions_taken.append(action)
                    
                    # Create legal consequences
                    crimes = self._determine_crimes_committed(mission, agent, report)
                    for crime in crimes:
                        # Simplified crime recording - just track the crime type and agent
                        # In a full implementation, this would integrate with the legal system properly
                        report.agent_performance[agent.id].crimes_committed.append(crime)
                else:
                    # Agent killed
                    agents_killed.append(agent.id)
                    report.casualties.append(agent.id)
                    
                    action = MissionAction(
                        phase=MissionPhase.EXTRACTION,
                        agent_id=agent.id,
                        action_type=ActionType.ESCAPE,
                        timestamp=datetime.now(),
                        success=False,
                        details={"outcome": "killed"},
                        narrative=f"{agent.name} is killed during the escape attempt"
                    )
                    report.action_log.append(action)
                    report.agent_performance[agent.id].actions_taken.append(action)
                    report.memorable_moments.append(f"The tragic death of {agent.name}")
        
        # Check if any agents try to rescue captured comrades
        if agents_captured and agents_escaped:
            for agent_id in agents_escaped:
                agent = next(a for a in agents if a.id == agent_id)
                if agent.traits.primary_trait == PersonalityTrait.LOYAL:
                    if random.random() < 0.4:  # 40% chance loyal agents attempt rescue
                        action = MissionAction(
                            phase=MissionPhase.EXTRACTION,
                            agent_id=agent.id,
                            action_type=ActionType.SUPPORT,
                            timestamp=datetime.now(),
                            success=False,
                            details={"rescue_attempt": True},
                            narrative=f"{agent.name} refuses to leave captured comrades behind"
                        )
                        report.action_log.append(action)
                        report.agent_performance[agent.id].actions_taken.append(action)
                        report.agent_performance[agent.id].heroic_moment = True
                        report.memorable_moments.append(f"{agent.name}'s desperate rescue attempt")
        
        # Mission fails if no one escapes
        if not agents_escaped:
            phase_result["success"] = False
            phase_result["abort_mission"] = True
        
        return phase_result
    
    def _execute_aftermath_phase(self,
                               mission: Any,
                               agents: List[Character],
                               report: MissionReport) -> Dict[str, Any]:
        """Handle post-mission consequences and reactions"""
        phase_result = {
            "success": True,
            "complications": [],
            "narrative_events": []
        }
        
        # Media reaction
        if report.heat_generated > 15 or report.casualties:
            media_reaction = self._generate_media_reaction(mission, report)
            phase_result["narrative_events"].append(media_reaction)
            
            # Affect public opinion
            if report.outcome == MissionOutcome.SUCCESS:
                report.public_opinion_shift = random.uniform(0.01, 0.05)
            elif report.casualties:
                report.public_opinion_shift = random.uniform(-0.05, -0.01)
        
        # Government response
        if report.heat_generated > 20:
            self.intelligence_system.add_event(IntelligenceEvent(
                event_type="government_response",
                severity="high",
                description="Authorities launch crackdown in response to resistance activity",
                location_id=location.id,
                faction_ids=[mission.faction_id],
                agent_ids=[a.id for a in agents]
            ))
        
        # Process psychological aftermath for surviving agents
        for agent in agents:
            if agent.id not in report.casualties:
                # Apply stress from mission
                stress_increase = 0.1
                if agent.id in report.captured_agents:
                    stress_increase = 0.5
                elif report.casualties:
                    stress_increase += 0.2  # Witnessing death
                
                report.agent_performance[agent.id].stress_gained = stress_increase
                
                # Apply trauma if witnessed violence or death
                if report.casualties or any(a.action_type == ActionType.COMBAT for a in report.action_log):
                    agent.emotional_state.apply_trauma(
                        trauma_intensity=0.3,
                        event_type="violence_witnessed",
                        triggers=[TraumaTriggerType.VIOLENCE]
                    )
                
                # Update relationships based on mission events
                self._update_relationships_from_mission(agent, agents, report)
        
        return phase_result
    
    def _check_for_betrayal(self,
                           agent: Character,
                           team: List[Character],
                           report: MissionReport) -> Dict[str, Any]:
        """Check if an agent betrays during the mission"""
        betrayal_result = {
            "betrayal_occurred": False,
            "reason": ""
        }
        
        # Get average relationship with team
        total_relationship_strength = 0.0
        relationship_count = 0
        
        for other_agent in team:
            if other_agent.id != agent.id:
                rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                if rel:
                    total_relationship_strength += rel.metrics.calculate_overall_relationship_strength()
                    relationship_count += 1
        
        avg_relationship = total_relationship_strength / relationship_count if relationship_count > 0 else 0.0
        
        # Calculate betrayal probability
        base_betrayal_chance = 0.05  # 5% base chance
        
        # Core modifiers (existing)
        if avg_relationship < -0.3:
            base_betrayal_chance += 0.2  # Poor relationships
        if agent.get_ideological_score() < 0.3:
            base_betrayal_chance += 0.15  # Low ideology
        if agent.emotional_state.fear > 0.7:
            base_betrayal_chance += 0.1  # High fear
        if agent.get_stress_level() > 0.8:
            base_betrayal_chance += 0.1  # Extreme stress
        
        # NEW: Contextual mission modifiers
        # Mission going badly increases betrayal chance
        if report.casualties:
            base_betrayal_chance += 0.05 * len(report.casualties)  # Each death increases chance
        if len(report.objectives_failed) > len(report.objectives_completed):
            base_betrayal_chance += 0.08  # Failing mission increases desperation
        if report.heat_generated > 15:
            base_betrayal_chance += 0.06  # High heat = more pressure
        
        # Agent's personal performance affects loyalty  
        agent_performance = report.agent_performance.get(agent.id)
        if agent_performance:
            failed_actions = len([a for a in agent_performance.actions_taken if not a.success])
            if failed_actions > 2:
                base_betrayal_chance += 0.04  # Personal failures breed desperation
            if agent_performance.panic_episodes > 0:
                base_betrayal_chance += 0.03 * agent_performance.panic_episodes  # Panic weakens resolve
        
        # Trait modifiers (existing)
        if PersonalityTrait.LOYAL in agent.traits.get_all_traits():
            base_betrayal_chance *= 0.3
        if PersonalityTrait.OPPORTUNISTIC in agent.traits.get_all_traits():
            base_betrayal_chance *= 1.5
        
        # NEW: Additional trait considerations
        if PersonalityTrait.CAUTIOUS in agent.traits.get_all_traits():
            base_betrayal_chance *= 1.2  # Cautious agents more likely to save themselves
        if PersonalityTrait.RECKLESS in agent.traits.get_all_traits():
            base_betrayal_chance *= 0.8  # Reckless agents less likely to think it through
        
        if random.random() < base_betrayal_chance:
            betrayal_result["betrayal_occurred"] = True
            
            # Determine reason
            if agent.emotional_state.fear > 0.7:
                betrayal_result["reason"] = "overwhelming fear"
            elif agent.get_ideological_score() < 0.3:
                betrayal_result["reason"] = "ideological differences"
            elif avg_relationship < -0.3:
                betrayal_result["reason"] = "personal vendetta"
            else:
                betrayal_result["reason"] = "self-preservation"
        
        return betrayal_result
    
    def _calculate_faction_performance_modifier(self,
                                              agent: Character,
                                              mission: Any) -> float:
        """Calculate progressive difficulty modifier based on faction performance history"""
        modifier = 0.0
        
        # Default modifier for when no mission data is available
        if not mission or not hasattr(mission, 'faction_id'):
            return 0.0
        
        # Simulate faction performance tracking
        # In a full implementation, this would check actual mission history
        faction_id = mission.faction_id
        
        # Simulate recent failure streak (would be actual data from game state)
        recent_failures = getattr(mission, 'recent_failures', 0)
        
        # Failure streak compensation - help struggling factions
        if recent_failures >= 3:
            modifier += 0.15  # Desperation breeds competence and luck
        elif recent_failures >= 2:
            modifier += 0.08  # Minor assistance for repeated failures
        
        # Success streak challenge - prevent snowballing
        recent_successes = getattr(mission, 'recent_successes', 0)
        if recent_successes >= 3:
            modifier -= 0.05  # Increased surveillance and countermeasures
        
        # Agent experience modifier
        # Agents who have survived multiple missions gain experience
        agent_experience = getattr(agent, 'missions_survived', 0)
        if agent_experience >= 5:
            modifier += 0.05  # Veteran bonus
        elif agent_experience >= 10:
            modifier += 0.1   # Elite veteran bonus
        
        # Faction morale effect (based on agent emotional state as proxy)
        if agent.emotional_state.trust > 0.6 and agent.emotional_state.fear < 0.3:
            modifier += 0.03  # High morale faction
        elif agent.emotional_state.trust < 0.2 or agent.emotional_state.fear > 0.7:
            modifier -= 0.03  # Demoralized faction
        
        # Equipment quality simulation (would be actual equipment stats)
        equipment_quality = getattr(mission, 'equipment_quality', 0.5)  # 0.0 to 1.0
        modifier += (equipment_quality - 0.5) * 0.1  # ±0.05 based on equipment
        
        # Intelligence quality modifier
        intel_quality = getattr(mission, 'intelligence_quality', 0.5)  # 0.0 to 1.0
        modifier += (intel_quality - 0.5) * 0.08  # ±0.04 based on intelligence
        
        # Cap the total modifier to prevent extreme swings
        return max(-0.2, min(0.2, modifier))

    def _calculate_heroic_moment_chance(self,
                                      agent: Character,
                                      mission: Any,
                                      success_chance: float) -> float:
        """Calculate the chance for a heroic moment based on context"""
        base_heroic_chance = 0.1  # 10% baseline
        
        # Trait modifiers
        if agent.traits.primary_trait == PersonalityTrait.LOYAL:
            base_heroic_chance += 0.05  # Loyal agents more likely to go above and beyond
        elif agent.traits.primary_trait == PersonalityTrait.RECKLESS:
            base_heroic_chance += 0.08  # Reckless agents take more heroic risks
        elif agent.traits.primary_trait == PersonalityTrait.CAUTIOUS:
            base_heroic_chance -= 0.03  # Cautious agents less likely to take heroic risks
        
        # Emotional state modifiers
        if agent.emotional_state.anger > 0.6:
            base_heroic_chance += 0.04  # Righteous anger drives heroism
        if agent.emotional_state.trust > 0.7:
            base_heroic_chance += 0.03  # Strong trust in the cause
        if agent.emotional_state.fear > 0.8:
            base_heroic_chance -= 0.05  # High fear inhibits heroism
        
        # Mission context modifiers
        if hasattr(mission, 'casualties') and len(mission.casualties) > 0:
            base_heroic_chance += 0.06  # Tragedy inspires heroism
        
        # Near-failure situations breed heroism
        if success_chance < 0.3:
            base_heroic_chance += 0.05  # Desperation breeds extraordinary effort
        
        # Relationship-driven heroism (protecting teammates)
        team_relationship_avg = getattr(agent, 'team_relationship_avg', 0.5)
        if team_relationship_avg > 0.7:
            base_heroic_chance += 0.04  # Strong bonds inspire heroic protection
        
        return max(0.0, min(0.25, base_heroic_chance))  # Cap at 25%

    def _generate_action_narrative(self,
                                 agent: Character,
                                 action_type: ActionType,
                                 success: bool,
                                 heroic: bool) -> str:
        """Generate contextual narrative for agent actions"""
        if success:
            if heroic:
                # Varied heroic narratives based on action type
                heroic_narratives = {
                    ActionType.COMBAT: [
                        f"{agent.name} charges through enemy fire with impossible courage",
                        f"{agent.name} single-handedly holds off multiple attackers",
                        f"{agent.name} turns certain defeat into glorious victory"
                    ],
                    ActionType.STEALTH: [
                        f"{agent.name} moves like a ghost, avoiding impossible detection",
                        f"{agent.name} infiltrates the most secure areas with supernatural skill",
                        f"{agent.name} slips past guards who later swear no one could have passed"
                    ],
                    ActionType.HACKING: [
                        f"{agent.name} breaks through cyber-defenses that should have been impenetrable",
                        f"{agent.name} turns the enemy's own systems against them",
                        f"{agent.name} pulls off a digital miracle under impossible pressure"
                    ],
                    ActionType.SOCIAL: [
                        f"{agent.name} convinces the enemy through sheer force of conviction",
                        f"{agent.name} turns potential enemies into unexpected allies",
                        f"{agent.name} inspires others with their passionate dedication"
                    ],
                    ActionType.SABOTAGE: [
                        f"{agent.name} destroys the target with surgical precision",
                        f"{agent.name} turns destruction into an art form",
                        f"{agent.name} creates chaos that cripples the enemy for months"
                    ]
                }
                
                narratives = heroic_narratives.get(action_type, [f"{agent.name} performs an incredible feat of {action_type.value}"])
                return random.choice(narratives)
            else:
                # Standard success narratives
                return f"{agent.name} successfully completes their {action_type.value} objective"
        else:
            # Failure narratives with emotional context
            if agent.emotional_state.fear > 0.7:
                return f"{agent.name} freezes as traumatic memories flood back"
            elif agent.emotional_state.anger > 0.8:
                return f"{agent.name} acts recklessly in rage, compromising the objective"
            elif agent.emotional_state.sadness > 0.6:
                return f"{agent.name} struggles with overwhelming despair"
            else:
                return f"{agent.name} fails despite their best efforts"

    def _perform_skill_check(self,
                           agent: Character,
                           required_skills: List[str],
                           mission: Any = None) -> Dict[str, Any]:
        """Perform a skill check for mission actions with progressive difficulty scaling"""
        # Determine best applicable skill
        best_skill = "combat"  # default
        best_level = 0
        
        skill_mapping = {
            "combat": ActionType.COMBAT,
            "stealth": ActionType.STEALTH,
            "hacking": ActionType.HACKING,
            "social": ActionType.SOCIAL,
            "technical": ActionType.SABOTAGE
        }
        
        for skill_name in required_skills:
            if hasattr(agent.skills, skill_name):
                skill_level = getattr(agent.skills, skill_name)
                if skill_level > best_level:
                    best_level = skill_level
                    best_skill = skill_name
        
        # Calculate success chance
        base_chance = best_level / 10.0
        effectiveness_modifier = agent.emotional_state.get_combat_effectiveness()
        final_chance = base_chance * 0.6 + effectiveness_modifier * 0.3 + 0.1  # Added +0.1 base bonus
        
        # NEW: Progressive difficulty scaling based on faction performance
        faction_modifier = self._calculate_faction_performance_modifier(agent, mission)
        final_chance += faction_modifier
        
        # Trait modifiers
        if agent.traits.primary_trait == PersonalityTrait.METHODICAL:
            final_chance += 0.1
        elif agent.traits.primary_trait == PersonalityTrait.RECKLESS:
            final_chance -= 0.1
        
        success = random.random() < final_chance
        
        # NEW: Enhanced heroic moment calculation
        heroic_chance = self._calculate_heroic_moment_chance(agent, mission, final_chance)
        heroic = success and random.random() < heroic_chance
        
        # Generate contextual narrative
        action_type = skill_mapping.get(best_skill, ActionType.SUPPORT)
        narrative = self._generate_action_narrative(agent, action_type, success, heroic)
        
        return {
            "success": success,
            "heroic": heroic,
            "action_type": action_type,
            "details": {"skill_used": best_skill, "chance": final_chance},
            "narrative": narrative
        }
    
    def _update_agent_states(self,
                           agents: List[Character],
                           phase_result: Dict[str, Any],
                           report: MissionReport):
        """Update agent emotional and relationship states after a phase"""
        for agent in agents:
            if agent.id in report.casualties:
                continue
            
            # Apply stress based on phase outcomes
            if not phase_result["success"]:
                agent.emotional_state.apply_emotional_impact({
                    "fear": 0.2,
                    "anger": 0.1,
                    "sadness": 0.1
                })
            
            # Apply complications
            for complication in phase_result.get("complications", []):
                if agent.id in complication.affected_agents:
                    if complication.severity == ComplicationSeverity.CATASTROPHIC:
                        agent.emotional_state.apply_emotional_impact({
                            "fear": 0.4,
                            "surprise": 0.3,
                            "trust": -0.2
                        })
    
    def _check_cascade_failure(self,
                             agents: List[Character],
                             report: MissionReport) -> bool:
        """Check if mission has cascaded into total failure"""
        active_agents = [a for a in agents if a.id not in report.casualties and a.id not in report.captured_agents]
        
        # Mission fails if:
        # 1. No agents remain
        if len(active_agents) == 0:
            return True
        
        # 2. All remaining agents are panicking
        if all(report.agent_performance[a.id].panic_episodes > 0 for a in active_agents):
            return True
        
        # 3. Catastrophic complications
        catastrophic_complications = [c for c in report.complications if c.severity == ComplicationSeverity.CATASTROPHIC]
        if len(catastrophic_complications) >= 2:
            return True
        
        return False
    
    def _calculate_final_outcome(self,
                               mission: Any,
                               report: MissionReport) -> MissionOutcome:
        """Calculate the overall mission outcome"""
        # Count successes and failures
        objectives_success_rate = len(report.objectives_completed) / max(1, len(report.objectives_completed) + len(report.objectives_failed))
        
        # Factor in losses
        total_agents = len(report.agent_performance)
        losses = len(report.casualties) + len(report.captured_agents)
        loss_rate = losses / max(1, total_agents)
        
        # Calculate outcome
        if objectives_success_rate >= 1.0 and loss_rate == 0:
            return MissionOutcome.CRITICAL_SUCCESS
        elif objectives_success_rate >= 0.7 and loss_rate < 0.3:
            return MissionOutcome.SUCCESS
        elif objectives_success_rate >= 0.5 or (objectives_success_rate > 0 and loss_rate < 0.5):
            return MissionOutcome.PARTIAL_SUCCESS
        elif loss_rate >= 0.7:
            return MissionOutcome.DISASTER
        else:
            return MissionOutcome.FAILURE
    
    def _determine_crimes_committed(self,
                                  mission: Any,
                                  agent: Character,
                                  report: MissionReport) -> List[CrimeType]:
        """Determine what crimes an agent committed during the mission"""
        crimes = []
        
        # Check actions taken
        for action in report.agent_performance[agent.id].actions_taken:
            if action.action_type == ActionType.COMBAT:
                crimes.append(CrimeType.ASSAULT)
            elif action.action_type == ActionType.SABOTAGE:
                crimes.append(CrimeType.PROPERTY_DESTRUCTION)
            elif action.action_type == ActionType.HACKING:
                crimes.append(CrimeType.BURGLARY)  # Digital burglary
        
        # Mission-specific crimes
        if hasattr(mission, 'mission_type'):
            if mission.mission_type == "bombing":
                crimes.append(CrimeType.TERRORISM)
            elif mission.mission_type == "theft":
                crimes.append(CrimeType.GRAND_THEFT)
            elif mission.mission_type == "assassination":
                crimes.append(CrimeType.ASSASSINATION)
        
        # If caught during mission, add terrorism charge
        if agent.id in report.captured_agents:
            if CrimeType.TERRORISM not in crimes:
                crimes.append(CrimeType.TERRORISM)
        
        return list(set(crimes))  # Remove duplicates
    
    def _generate_dramatic_event(self,
                               agents: List[Character],
                               location: Any) -> str:
        """Generate a random dramatic event during mission"""
        events = [
            "An unexpected civilian appears, forcing a moral decision",
            "Old intelligence proves dangerously outdated",
            "A security guard shows unexpected sympathy for the cause",
            "Equipment failure at the worst possible moment",
            "An agent recognizes someone from their past",
            "The target turns out to be different than expected",
            "A rival faction interferes with the operation",
            "Media arrives on scene unexpectedly"
        ]
        
        return random.choice(events)
    
    def _generate_media_reaction(self,
                               mission: Any,
                               report: MissionReport) -> str:
        """Generate media reaction to mission"""
        if report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS]:
            reactions = [
                "Underground media celebrates the successful strike against oppression",
                "Mainstream news downplays the resistance success",
                "Social media erupts with support for the resistance",
                "Government spokesperson denies the effectiveness of the operation"
            ]
        else:
            reactions = [
                "State media uses the failed operation as propaganda",
                "Public opinion turns against 'violent extremists'",
                "Captured agents paraded on television",
                "Government announces increased security measures"
            ]
        
        return random.choice(reactions)
    
    def _calculate_propaganda_value(self, report: MissionReport) -> float:
        """Calculate the propaganda value of the mission"""
        value = 0.0
        
        # Success breeds support
        if report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS]:
            value += 0.5
        elif report.outcome == MissionOutcome.PARTIAL_SUCCESS:
            value += 0.2
        
        # Heroic moments inspire
        heroic_agents = sum(1 for p in report.agent_performance.values() if p.heroic_moment)
        value += heroic_agents * 0.1
        
        # Martyrs create sympathy
        if report.casualties:
            value += len(report.casualties) * 0.15
        
        # Betrayal damages the cause
        betrayals = sum(1 for p in report.agent_performance.values() if p.betrayal_attempted)
        value -= betrayals * 0.3
        
        # High heat can backfire
        if report.heat_generated > 20:
            value -= 0.2
        
        return max(0.0, min(1.0, value))
    
    def _determine_symbolic_impact(self,
                                 mission: Any,
                                 report: MissionReport) -> str:
        """Determine the symbolic/narrative impact of the mission"""
        if report.outcome == MissionOutcome.CRITICAL_SUCCESS:
            impacts = [
                "A stunning blow against the regime",
                "Proof that resistance is possible",
                "A rallying cry for the oppressed",
                "The spark that lights the fire"
            ]
        elif report.outcome == MissionOutcome.SUCCESS:
            impacts = [
                "Another victory in the long struggle",
                "Evidence of growing resistance strength",
                "A successful strike against injustice",
                "Progress toward liberation"
            ]
        elif report.outcome == MissionOutcome.DISASTER:
            impacts = [
                "A tragic reminder of the cost of resistance",
                "Martyrs for the cause",
                "A setback that steels resolve",
                "The price of fighting tyranny"
            ]
        else:
            impacts = [
                "A learning experience for the movement",
                "A reminder that the struggle continues",
                "Neither victory nor defeat, but persistence",
                "The long road to freedom"
            ]
        
        return random.choice(impacts)
    
    def _update_relationships_from_mission(self,
                                         agent: Character,
                                         team: List[Character],
                                         report: MissionReport):
        """Enhanced relationship update system with nuanced consequence hooks"""
        performance = report.agent_performance[agent.id]
        
        for other_agent in team:
            if other_agent.id != agent.id and other_agent.id not in report.casualties:
                other_performance = report.agent_performance.get(other_agent.id)
                
                # Base relationship changes from shared experience
                self._apply_shared_experience_effects(agent, other_agent, report)
                
                # Performance-based relationship changes
                self._apply_performance_relationship_effects(agent, other_agent, performance, other_performance, report)
                
                # Emotional state cascading effects
                self._apply_emotional_cascading_effects(agent, other_agent, report)
                
                # Trait-based relationship dynamics
                self._apply_trait_relationship_dynamics(agent, other_agent, report)
    
    def _apply_shared_experience_effects(self, 
                                       agent: Character, 
                                       other_agent: Character, 
                                       report: MissionReport):
        """Apply relationship changes from shared mission experience"""
        # Shared success creates bonds
        if report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS]:
            self.relationship_manager.apply_group_event(
                [agent.id, other_agent.id],
                RelationshipEvent.MISSION_SUCCESS,
                intensity=0.7
            )
        
        # Shared trauma can strengthen or strain relationships
        elif report.outcome in [MissionOutcome.FAILURE, MissionOutcome.DISASTER]:
            # Loyalty trait affects how agents handle shared failure
            if agent.traits.primary_trait == PersonalityTrait.LOYAL:
                # Loyal agents bond through adversity
                self.relationship_manager.apply_group_event(
                    [agent.id, other_agent.id],
                    RelationshipEvent.SHARED_TRAUMA,
                    intensity=0.5
                )
            else:
                # Others may assign blame
                self.relationship_manager.apply_group_event(
                    [agent.id, other_agent.id],
                    RelationshipEvent.MISSION_FAILURE,
                    intensity=0.6,
                    details={"blame_assigned": True}
                )
        
        # High casualties create survivor guilt bonds
        if len(report.casualties) >= 2:
            self.relationship_manager.apply_group_event(
                [agent.id, other_agent.id],
                RelationshipEvent.SURVIVOR_GUILT,
                intensity=0.4
            )
    
    def _apply_performance_relationship_effects(self,
                                              agent: Character,
                                              other_agent: Character,
                                              agent_performance: AgentPerformance,
                                              other_performance: Optional[AgentPerformance],
                                              report: MissionReport):
        """Apply relationship changes based on individual performance"""
        if not other_performance:
            return
            
        # Heroic actions inspire admiration
        if other_performance.heroic_moment:
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel:
                rel.apply_event(RelationshipEvent.SAVED_LIFE, intensity=0.8)
                # Add specific heroic admiration effect
                rel.apply_event(RelationshipEvent.INSPIRED_BY_COURAGE, intensity=0.6)
        
        # Betrayal destroys relationships
        if other_performance.betrayal_attempted:
            self.relationship_manager.apply_group_event(
                [agent.id, other_agent.id],
                RelationshipEvent.BETRAYAL,
                intensity=1.0,
                details={"betrayer": other_agent.id}
            )
        
        # Performance disparity can create tension or respect
        agent_score = agent_performance.calculate_performance_score()
        other_score = other_performance.calculate_performance_score()
        performance_gap = abs(agent_score - other_score)
        
        if performance_gap > 0.4:  # Significant performance difference
            if other_score > agent_score:
                # Other agent performed much better - respect or jealousy
                if agent.traits.primary_trait == PersonalityTrait.LOYAL:
                    # Loyal agents feel respect
                    rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                    if rel:
                        rel.apply_event(RelationshipEvent.PROFESSIONAL_RESPECT, intensity=0.3)
                else:
                    # Others might feel jealousy or inadequacy  
                    rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                    if rel:
                        rel.apply_event(RelationshipEvent.PROFESSIONAL_JEALOUSY, intensity=0.2)
        
        # Panic episodes can strain relationships
        if other_performance.panic_episodes > 1:
            # Some agents lose respect for panicking teammates
            if agent.traits.primary_trait in [PersonalityTrait.METHODICAL, PersonalityTrait.LEADER]:
                rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                if rel:
                    rel.apply_event(RelationshipEvent.LOST_CONFIDENCE, intensity=0.3)
            elif agent.traits.primary_trait == PersonalityTrait.COMPASSIONATE:
                # Compassionate agents offer support instead
                rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                if rel:
                    rel.apply_event(RelationshipEvent.EMOTIONAL_SUPPORT, intensity=0.4)
    
    def _apply_emotional_cascading_effects(self,
                                         agent: Character,
                                         other_agent: Character,
                                         report: MissionReport):
        """Apply emotional state cascading between agents"""
        # Fear is contagious in high-stress situations
        if agent.emotional_state.fear > 0.8 and other_agent.emotional_state.fear > 0.8:
            # Mutual fear can create dependency or distance
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel and rel.metrics.calculate_overall_relationship_strength() > 0.3:
                # Close agents support each other through fear
                rel.apply_event(RelationshipEvent.MUTUAL_SUPPORT, intensity=0.5)
            else:
                # Distant agents blame each other for fear
                rel.apply_event(RelationshipEvent.FEAR_SPIRAL, intensity=0.3)
        
        # Anger alignment can create bonds or conflicts
        if agent.emotional_state.anger > 0.6 and other_agent.emotional_state.anger > 0.6:
            # Both angry - depends on whether anger is aligned
            if agent.traits.primary_trait == other_agent.traits.primary_trait:
                # Similar personalities channel anger together
                rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                if rel:
                    rel.apply_event(RelationshipEvent.SHARED_RIGHTEOUS_ANGER, intensity=0.4)
            else:
                # Different personalities clash when angry
                rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
                if rel:
                    rel.apply_event(RelationshipEvent.PERSONALITY_CLASH, intensity=0.3)
        
        # Trust and hope are strengthening
        if agent.emotional_state.trust > 0.7 and other_agent.emotional_state.trust > 0.7:
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel:
                rel.apply_event(RelationshipEvent.SHARED_CONVICTION, intensity=0.3)
    
    def _apply_trait_relationship_dynamics(self,
                                         agent: Character,
                                         other_agent: Character,
                                         report: MissionReport):
        """Apply trait-based relationship dynamics"""
        # Leadership and follower dynamics
        if (agent.traits.primary_trait == PersonalityTrait.LEADER and 
            other_agent.traits.primary_trait == PersonalityTrait.FOLLOWER):
            # Natural hierarchy can strengthen bonds
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel and report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS]:
                rel.apply_event(RelationshipEvent.EFFECTIVE_LEADERSHIP, intensity=0.4)
        
        # Cautious vs Reckless tension
        if (agent.traits.primary_trait == PersonalityTrait.CAUTIOUS and 
            other_agent.traits.primary_trait == PersonalityTrait.RECKLESS):
            # Opposing approaches create friction
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel:
                rel.apply_event(RelationshipEvent.TACTICAL_DISAGREEMENT, intensity=0.2)
        
        # Compassionate agents build stronger bonds
        if agent.traits.primary_trait == PersonalityTrait.COMPASSIONATE:
            # Compassionate agents naturally improve relationships
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel:
                rel.apply_event(RelationshipEvent.EMOTIONAL_SUPPORT, intensity=0.2)
        
        # Opportunistic agents can damage trust
        if other_agent.traits.primary_trait == PersonalityTrait.OPPORTUNISTIC:
            # Others gradually lose trust in opportunistic agents
            rel = self.relationship_manager.get_relationship(agent.id, other_agent.id)
            if rel:
                rel.apply_event(RelationshipEvent.TRUST_EROSION, intensity=0.1)
    
    def _apply_mission_consequences(self,
                                  mission: Any,
                                  agents: List[Character],
                                  report: MissionReport):
        """Apply all mission consequences to game state"""
        # Update agent statuses
        for agent_id in report.casualties:
            # Mark agent as dead in game state
            logger.info(f"Agent {agent_id} killed in action")
        
        for agent_id in report.captured_agents:
            # Mark agent as captured
            logger.info(f"Agent {agent_id} captured")
        
        # Apply resource changes
        if hasattr(mission, 'faction_id'):
            # Would update faction resources here
            pass
        
        # Generate intelligence events
        if report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS]:
            self.intelligence_system.add_event(IntelligenceEvent(
                event_type="mission_success",
                severity="medium",
                description=f"Successful operation: {report.symbolic_impact}",
                location_id=location.id if 'location' in locals() else None,
                faction_ids=[mission.faction_id] if hasattr(mission, 'faction_id') else [],
                agent_ids=[a.id for a in agents]
            ))
    
    def _log_mission_report(self, report: MissionReport):
        """Log the complete mission report"""
        logger.info(f"Mission {report.mission_id} completed: {report.outcome.value}")
        logger.info(f"Objectives completed: {len(report.objectives_completed)}")
        logger.info(f"Casualties: {len(report.casualties)}")
        logger.info(f"Captured: {len(report.captured_agents)}")
        logger.info(f"Heat generated: {report.heat_generated}")
        logger.info(f"Propaganda value: {report.propaganda_value:.2f}")
        
        # Log full narrative report
        full_report = report.generate_full_report()
        logger.info(f"Full mission report:\n{full_report}")

    def _determine_emotional_tone(self, report: MissionReport) -> EmotionalTone:
        """Determine the emotional tone of the mission outcome"""
        # Count key factors
        total_agents = len(report.agent_performance)
        casualties = len(report.casualties)
        captured = len(report.captured_agents)
        heroes = sum(1 for p in report.agent_performance.values() if p.heroic_moment)
        betrayals = sum(1 for p in report.agent_performance.values() if p.betrayal_attempted)
        panic_episodes = sum(p.panic_episodes for p in report.agent_performance.values())
        
        # Primary tone determination logic
        if betrayals > 0:
            return EmotionalTone.BETRAYAL_TRAGEDY
            
        elif report.outcome == MissionOutcome.CRITICAL_SUCCESS:
            if heroes > 0:
                return EmotionalTone.TRIUMPHANT_VICTORY
            else:
                return EmotionalTone.BITTERSWEET_SUCCESS
                
        elif report.outcome == MissionOutcome.SUCCESS:
            if casualties > 0:
                return EmotionalTone.PYRRHIC_VICTORY
            elif heroes > 0:
                return EmotionalTone.REDEMPTIVE_MOMENT
            else:
                return EmotionalTone.BITTERSWEET_SUCCESS
                
        elif report.outcome == MissionOutcome.PARTIAL_SUCCESS:
            if casualties > total_agents // 2:
                return EmotionalTone.HEROIC_SACRIFICE
            else:
                return EmotionalTone.AMBIGUOUS_OUTCOME
                
        elif report.outcome == MissionOutcome.FAILURE:
            if panic_episodes > total_agents:
                return EmotionalTone.FEARFUL_RETREAT
            elif captured + casualties < total_agents // 2:
                return EmotionalTone.TACTICAL_WITHDRAWAL
            else:
                return EmotionalTone.DESPERATE_STRUGGLE
                
        elif report.outcome == MissionOutcome.DISASTER:
            if heroes > 0:
                return EmotionalTone.HEROIC_SACRIFICE
            else:
                return EmotionalTone.DESPERATE_STRUGGLE
                
        else:
            return EmotionalTone.AMBIGUOUS_OUTCOME


class NarrativeGenerator:
    """Enhanced narrative text generator for mission events with emotional awareness"""
    
    def __init__(self):
        """Initialize with tone-specific narrative templates"""
        self.tone_openings = {
            EmotionalTone.TRIUMPHANT_VICTORY: [
                "In a breathtaking display of tactical brilliance and raw courage",
                "Against impossible odds, the team delivered a crushing blow to the regime",
                "What began as a dangerous mission became a legendary triumph"
            ],
            EmotionalTone.HEROIC_SACRIFICE: [
                "In their darkest hour, heroes emerged from among the resistance",
                "Though victory came at a terrible price, the sacrifice was not in vain",
                "The team faced an impossible choice and chose the path of honor"
            ],
            EmotionalTone.TACTICAL_WITHDRAWAL: [
                "When the situation deteriorated beyond salvage, discipline saved lives",
                "Strategic wisdom prevailed over reckless heroism",
                "The team executed a masterful withdrawal under fire"
            ],
            EmotionalTone.FEARFUL_RETREAT: [
                "Terror gripped the team as the mission collapsed around them",
                "Panic spread through the ranks as everything went wrong",
                "What should have been routine became a nightmare of confusion"
            ],
            EmotionalTone.BETRAYAL_TRAGEDY: [
                "Trust shattered in the worst possible moment",
                "The team's greatest enemy turned out to be one of their own",
                "A shocking betrayal left the resistance reeling"
            ],
            EmotionalTone.REDEMPTIVE_MOMENT: [
                "From the ashes of failure, redemption rose like a phoenix",
                "A moment of grace transformed defeat into inspiration",
                "When all seemed lost, one person's courage changed everything"
            ]
        }
    
    def generate_mission_summary(self, report: MissionReport) -> str:
        """Generate an emotionally aware narrative summary of the entire mission"""
        # Get opening based on emotional tone
        if report.emotional_tone and report.emotional_tone in self.tone_openings:
            opening = random.choice(self.tone_openings[report.emotional_tone])
        else:
            # Fallback to outcome-based opening
            opening = self._get_outcome_opening(report.outcome)
        
        # Build narrative sections
        narrative_parts = [opening]
        
        # Add character focus if there are standout performers
        character_section = self._generate_character_highlights(report)
        if character_section:
            narrative_parts.append(character_section)
        
        # Add tactical analysis
        tactical_section = self._generate_tactical_analysis(report)
        if tactical_section:
            narrative_parts.append(tactical_section)
        
        # Add emotional consequences
        emotional_section = self._generate_emotional_consequences(report)
        if emotional_section:
            narrative_parts.append(emotional_section)
        
        # Add closing based on propaganda value and symbolic impact
        closing = self._generate_symbolic_closing(report)
        narrative_parts.append(closing)
        
        # Combine with appropriate transitions
        return self._combine_narrative_parts(narrative_parts)
    
    def _get_outcome_opening(self, outcome: MissionOutcome) -> str:
        """Fallback opening generator based on mission outcome"""
        openings = {
            MissionOutcome.CRITICAL_SUCCESS: "In a stunning display of coordination and courage",
            MissionOutcome.SUCCESS: "Despite mounting challenges, the team persevered",
            MissionOutcome.PARTIAL_SUCCESS: "The mission achieved mixed but meaningful results",
            MissionOutcome.FAILURE: "What began as a calculated risk ended in disappointment",
            MissionOutcome.DISASTER: "The operation descended into chaos and tragedy",
            MissionOutcome.ABORTED: "Discretion proved the better part of valor"
        }
        return openings.get(outcome, "The mission unfolded in unexpected ways")
    
    def _generate_character_highlights(self, report: MissionReport) -> str:
        """Generate character-focused narrative highlights"""
        highlights = []
        
        # Heroic moments
        heroes = [(agent_id, perf) for agent_id, perf in report.agent_performance.items() if perf.heroic_moment]
        if heroes:
            if len(heroes) == 1:
                agent_id, perf = heroes[0]
                heroic_actions = [action for action in perf.actions_taken if action.success]
                if heroic_actions:
                    highlights.append(f"The mission's turning point came when {agent_id} rose to extraordinary heights")
            else:
                highlights.append(f"Multiple acts of heroism inspired the entire team to push beyond their limits")
        
        # Betrayals
        betrayers = [agent_id for agent_id, perf in report.agent_performance.items() if perf.betrayal_attempted]
        if betrayers:
            if len(betrayers) == 1:
                highlights.append(f"The shocking betrayal by {betrayers[0]} sent shockwaves through the resistance")
            else:
                highlights.append("Multiple betrayals shattered team cohesion at the worst possible moment")
        
        # Psychological breaks
        broken_agents = [agent_id for agent_id, perf in report.agent_performance.items() if perf.panic_episodes > 2]
        if broken_agents and not betrayers:  # Don't overshadow betrayal
            highlights.append(f"The psychological toll became evident as several operatives struggled with the pressure")
        
        return " ".join(highlights) if highlights else ""
    
    def _generate_tactical_analysis(self, report: MissionReport) -> str:
        """Generate tactical situation analysis"""
        analysis_parts = []
        
        # Objective analysis
        total_objectives = len(report.objectives_completed) + len(report.objectives_failed)
        if total_objectives > 0:
            success_rate = len(report.objectives_completed) / total_objectives
            if success_rate >= 0.8:
                analysis_parts.append("The team executed their objectives with clinical precision")
            elif success_rate >= 0.5:
                analysis_parts.append("Key objectives were secured despite mounting complications")
            elif success_rate > 0:
                analysis_parts.append("Partial objectives were achieved through determined effort")
            else:
                analysis_parts.append("Objectives remained frustratingly out of reach")
        
        # Complication handling
        major_complications = [c for c in report.complications if c.severity in [ComplicationSeverity.MAJOR, ComplicationSeverity.CATASTROPHIC]]
        if major_complications:
            if len(major_complications) == 1:
                analysis_parts.append("A major complication forced rapid adaptation")
            else:
                analysis_parts.append("Cascading complications tested every aspect of the team's training")
        
        # Heat management
        if report.heat_generated > 25:
            analysis_parts.append("The operation's visibility generated dangerous attention from authorities")
        elif report.heat_generated < 5:
            analysis_parts.append("The team maintained operational security throughout")
        
        return " ".join(analysis_parts) if analysis_parts else ""
    
    def _generate_emotional_consequences(self, report: MissionReport) -> str:
        """Generate emotional and psychological consequence narrative"""
        consequences = []
        
        # Loss impact
        total_losses = len(report.casualties) + len(report.captured_agents)
        if total_losses > 0:
            if report.casualties and report.captured_agents:
                consequences.append(f"The loss of {len(report.casualties)} lives and capture of {len(report.captured_agents)} comrades left deep scars")
            elif report.casualties:
                if len(report.casualties) == 1:
                    consequences.append("A life lost in service to the cause weighs heavily on survivors")
                else:
                    consequences.append(f"The sacrifice of {len(report.casualties)} brave souls will not be forgotten")
            elif report.captured_agents:
                if len(report.captured_agents) == 1:
                    consequences.append("A comrade's capture adds urgency to the struggle")
                else:
                    consequences.append(f"With {len(report.captured_agents)} operatives in enemy hands, rescue becomes a priority")
        
        # Team bonding through adversity
        if not report.casualties and not report.captured_agents and len(report.complications) > 1:
            consequences.append("Shared adversity forged stronger bonds between team members")
        
        return " ".join(consequences) if consequences else ""
    
    def _generate_symbolic_closing(self, report: MissionReport) -> str:
        """Generate symbolic closing based on propaganda value and impact"""
        if report.propaganda_value > 0.7:
            closings = [
                "This operation will echo through history as a turning point in the struggle",
                "The resistance grows stronger with each bold action against tyranny",
                "Today's victory proves that even the mightiest oppressor can be challenged"
            ]
        elif report.propaganda_value > 0.3:
            closings = [
                "Another step forward on the long road to liberation",
                "The flame of resistance burns brighter with each passing day",
                "Small victories accumulate into unstoppable momentum"
            ]
        elif report.propaganda_value < 0.1:
            closings = [
                "From setbacks, the movement learns and grows stronger",
                "Even in defeat, the cause endures and adapts",
                "Temporary failures cannot extinguish the desire for freedom"
            ]
        else:
            closings = [
                "The struggle continues with renewed determination",
                "Each mission teaches valuable lessons for the future",
                "Progress comes in many forms, not all immediately visible"
            ]
        
        return random.choice(closings)
    
    def _combine_narrative_parts(self, parts: List[str]) -> str:
        """Combine narrative parts with appropriate transitions"""
        if not parts:
            return "The mission unfolded quietly, leaving little mark on history."
        
        if len(parts) == 1:
            return parts[0] + "."
        
        # Add transitions between parts
        transitions = [", ", ". ", ". Meanwhile, ", ". As events unfolded, ", ". In the aftermath, "]
        result = parts[0]
        
        for i, part in enumerate(parts[1:], 1):
            if i == len(parts) - 1:  # Last part
                result += ". " + part
            else:
                transition = transitions[min(i - 1, len(transitions) - 1)]
                result += transition + part
        
        return result + "."