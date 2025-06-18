"""
Years of Lead - Advanced Trauma and Psychological Impact System

Phase 5: Advanced Trauma and Psychological Impact Enhancement
Implements persistent, intergenerational trauma and emotional scars that 
affect agents over time and can be passed to future generations.
"""

import random
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class TraumaType(Enum):
    """Types of psychological trauma"""
    COMBAT_TRAUMA = "combat_trauma"
    BETRAYAL_TRAUMA = "betrayal_trauma"
    WITNESS_TRAUMA = "witness_trauma"
    INTERROGATION_TRAUMA = "interrogation_trauma"
    LOSS_TRAUMA = "loss_trauma"
    ISOLATION_TRAUMA = "isolation_trauma"
    TORTURE_TRAUMA = "torture_trauma"
    SURVIVAL_GUILT = "survival_guilt"
    MORAL_INJURY = "moral_injury"
    IDENTITY_TRAUMA = "identity_trauma"


class TraumaSeverity(Enum):
    """Severity levels of trauma"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


class RecoveryMethod(Enum):
    """Methods for trauma recovery"""
    THERAPY = "therapy"
    MEDICATION = "medication"
    SOCIAL_SUPPORT = "social_support"
    REST_AND_RECOVERY = "rest_and_recovery"
    SPIRITUAL_HEALING = "spiritual_healing"
    CREATIVE_EXPRESSION = "creative_expression"
    PHYSICAL_ACTIVITY = "physical_activity"
    PROFESSIONAL_HELP = "professional_help"


@dataclass
class TraumaEvent:
    """A specific traumatic event"""
    id: str
    trauma_type: TraumaType
    severity: TraumaSeverity
    timestamp: datetime
    description: str
    source_agent_id: Optional[str] = None
    location: Optional[str] = None
    witnesses: List[str] = field(default_factory=list)
    emotional_impact: Dict[str, float] = field(default_factory=dict)
    physical_impact: Dict[str, float] = field(default_factory=dict)
    recovery_progress: float = 0.0
    is_healing: bool = False
    healing_rate: float = 0.1
    triggers: List[str] = field(default_factory=list)
    coping_mechanisms: List[str] = field(default_factory=list)
    
    def update_recovery(self, time_passed: float):
        """Update trauma recovery progress"""
        if self.is_healing:
            self.recovery_progress = min(1.0, self.recovery_progress + (self.healing_rate * time_passed))
            if self.recovery_progress >= 1.0:
                self.is_healing = True
                self.recovery_progress = 1.0
    
    def get_current_impact(self) -> Dict[str, float]:
        """Get current emotional impact based on recovery progress"""
        current_impact = {}
        for emotion, value in self.emotional_impact.items():
            current_impact[emotion] = value * (1.0 - self.recovery_progress)
        return current_impact


@dataclass
class EmotionalScar:
    """A persistent emotional scar from trauma"""
    id: str
    trauma_event_id: str
    emotion_type: str
    intensity: float
    created_timestamp: datetime
    last_triggered: Optional[datetime] = None
    trigger_conditions: List[Dict[str, Any]] = field(default_factory=list)
    coping_strategies: List[str] = field(default_factory=list)
    recovery_progress: float = 0.0
    is_permanent: bool = False
    
    def check_trigger(self, context: Dict[str, Any]) -> bool:
        """Check if scar is triggered by current context"""
        for condition in self.trigger_conditions:
            if self._evaluate_trigger_condition(condition, context):
                return True
        return False
    
    def _evaluate_trigger_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a trigger condition"""
        condition_type = condition.get("type")
        
        if condition_type == "location":
            return context.get("location") == condition.get("location")
        elif condition_type == "agent_present":
            return condition.get("agent_id") in context.get("agents_present", [])
        elif condition_type == "emotion_level":
            emotion = condition.get("emotion")
            threshold = condition.get("threshold", 0.5)
            return context.get("emotional_state", {}).get(emotion, 0.0) > threshold
        elif condition_type == "stress_level":
            threshold = condition.get("threshold", 70)
            return context.get("stress_level", 0) > threshold
        
        return False
    
    def update_recovery(self, time_passed: float):
        """Update scar recovery progress"""
        if not self.is_permanent:
            self.recovery_progress = min(1.0, self.recovery_progress + (0.05 * time_passed))


@dataclass
class GenerationalTrauma:
    """Trauma passed down through generations"""
    id: str
    original_trauma_id: str
    generation: int
    inherited_agent_id: str
    trauma_type: TraumaType
    intensity_modifier: float = 0.7  # Reduced intensity in later generations
    manifestation_type: str = "emotional"  # emotional, behavioral, cognitive
    inherited_triggers: List[str] = field(default_factory=list)
    family_patterns: List[str] = field(default_factory=list)
    created_timestamp: datetime = field(default_factory=datetime.now)
    
    def get_effective_intensity(self) -> float:
        """Get effective trauma intensity for this generation"""
        base_intensity = 1.0
        return base_intensity * (self.intensity_modifier ** self.generation)


@dataclass
class RecoveryProgram:
    """A structured recovery program for trauma"""
    id: str
    agent_id: str
    trauma_event_ids: List[str]
    methods: List[RecoveryMethod]
    start_timestamp: datetime
    duration_days: int
    success_probability: float
    cost: int
    requirements: Dict[str, Any] = field(default_factory=dict)
    progress: float = 0.0
    active: bool = True
    completed: bool = False
    
    def update_progress(self, daily_progress: float):
        """Update recovery program progress"""
        self.progress = min(1.0, self.progress + daily_progress)
        if self.progress >= 1.0:
            self.completed = True
            self.active = False
    
    def get_daily_progress(self) -> float:
        """Calculate daily progress based on methods and conditions"""
        base_progress = 0.1
        
        # Method effectiveness
        method_effectiveness = {
            RecoveryMethod.THERAPY: 0.3,
            RecoveryMethod.MEDICATION: 0.2,
            RecoveryMethod.SOCIAL_SUPPORT: 0.15,
            RecoveryMethod.REST_AND_RECOVERY: 0.1,
            RecoveryMethod.SPIRITUAL_HEALING: 0.1,
            RecoveryMethod.CREATIVE_EXPRESSION: 0.1,
            RecoveryMethod.PHYSICAL_ACTIVITY: 0.1,
            RecoveryMethod.PROFESSIONAL_HELP: 0.25
        }
        
        total_effectiveness = sum(method_effectiveness.get(method, 0.1) for method in self.methods)
        
        return base_progress * total_effectiveness


class AdvancedTraumaSystem:
    """Advanced trauma and psychological impact system"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.trauma_events: Dict[str, TraumaEvent] = {}
        self.emotional_scars: Dict[str, List[EmotionalScar]] = defaultdict(list)
        self.generational_trauma: Dict[str, List[GenerationalTrauma]] = defaultdict(list)
        self.recovery_programs: Dict[str, RecoveryProgram] = {}
        
        # System parameters
        self.trauma_decay_rate = 0.02  # Natural decay per day
        self.scar_formation_threshold = 0.8  # Trauma level for scar formation
        self.generational_inheritance_chance = 0.3  # 30% chance of inheritance
        self.max_generations = 3  # Maximum generations for trauma inheritance
        self.recovery_facility_cost = 500
        self.therapy_cost = 200
        
        # Tracking
        self.trauma_statistics: Dict[str, Any] = {}
        self.recovery_statistics: Dict[str, Any] = {}
        self.generational_patterns: Dict[str, List[str]] = defaultdict(list)
        
        self._initialize_trauma_system()
    
    def _initialize_trauma_system(self):
        """Initialize the trauma system"""
        logger.info("Initializing Advanced Trauma System")
        
        # Initialize trauma statistics
        self.trauma_statistics = {
            "total_trauma_events": 0,
            "active_trauma_events": 0,
            "total_emotional_scars": 0,
            "generational_trauma_count": 0,
            "recovery_programs_active": 0,
            "recovery_success_rate": 0.0
        }
    
    def process_trauma_system(self) -> Dict[str, Any]:
        """Process trauma system for the current turn"""
        results = {
            "new_trauma_events": [],
            "trauma_recovery": [],
            "scar_formation": [],
            "generational_inheritance": [],
            "recovery_progress": [],
            "psychological_crises": [],
            "healing_breakthroughs": []
        }
        
        # Process existing trauma events
        trauma_recovery = self._process_trauma_recovery()
        results["trauma_recovery"] = trauma_recovery
        
        # Check for new trauma events
        new_trauma = self._check_for_new_trauma_events()
        results["new_trauma_events"] = new_trauma
        
        # Process emotional scar formation
        scar_formation = self._process_scar_formation()
        results["scar_formation"] = scar_formation
        
        # Process generational trauma inheritance
        generational_inheritance = self._process_generational_inheritance()
        results["generational_inheritance"] = generational_inheritance
        
        # Process recovery programs
        recovery_progress = self._process_recovery_programs()
        results["recovery_progress"] = recovery_progress
        
        # Check for psychological crises
        psychological_crises = self._check_psychological_crises()
        results["psychological_crises"] = psychological_crises
        
        # Check for healing breakthroughs
        healing_breakthroughs = self._check_healing_breakthroughs()
        results["healing_breakthroughs"] = healing_breakthroughs
        
        # Update statistics
        self._update_trauma_statistics()
        
        return results
    
    def _process_trauma_recovery(self) -> List[Dict[str, Any]]:
        """Process natural trauma recovery"""
        recovery_results = []
        
        for trauma_id, trauma_event in self.trauma_events.items():
            if trauma_event.is_healing:
                # Update recovery progress
                old_progress = trauma_event.recovery_progress
                trauma_event.update_recovery(1.0)  # 1 day passed
                
                if trauma_event.recovery_progress != old_progress:
                    recovery_results.append({
                        "trauma_id": trauma_id,
                        "old_progress": old_progress,
                        "new_progress": trauma_event.recovery_progress,
                        "agent_id": trauma_event.source_agent_id,
                        "trauma_type": trauma_event.trauma_type.value
                    })
                    
                    # Update agent emotional state
                    if trauma_event.source_agent_id:
                        agent = self.game_state.agents.get(trauma_event.source_agent_id)
                        if agent and hasattr(agent, 'emotional_state'):
                            current_impact = trauma_event.get_current_impact()
                            for emotion, value in current_impact.items():
                                if hasattr(agent.emotional_state, emotion):
                                    current_value = getattr(agent.emotional_state, emotion)
                                    new_value = max(-1.0, min(1.0, current_value + value))
                                    setattr(agent.emotional_state, emotion, new_value)
        
        return recovery_results
    
    def _check_for_new_trauma_events(self) -> List[Dict[str, Any]]:
        """Check for new trauma events based on game state"""
        new_trauma_events = []
        
        # Check agent states for trauma triggers
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'emotional_state'):
                continue
            
            # Check for high stress trauma
            if agent.stress > 90:
                trauma_event = self._create_stress_trauma(agent_id, agent.stress)
                if trauma_event:
                    new_trauma_events.append(trauma_event)
            
            # Check for emotional breakdown trauma
            emotional_state = agent.emotional_state
            dominant_emotion, intensity = emotional_state.get_dominant_emotion()
            if intensity > 0.9:
                trauma_event = self._create_emotional_breakdown_trauma(agent_id, dominant_emotion, intensity)
                if trauma_event:
                    new_trauma_events.append(trauma_event)
            
            # Check for relationship betrayal trauma
            if hasattr(agent, 'relationships'):
                for other_id, relationship in agent.relationships.items():
                    if relationship.affinity < -50 and relationship.trust < 0.1:
                        trauma_event = self._create_betrayal_trauma(agent_id, other_id)
                        if trauma_event:
                            new_trauma_events.append(trauma_event)
        
        return new_trauma_events
    
    def _create_stress_trauma(self, agent_id: str, stress_level: int) -> Optional[Dict[str, Any]]:
        """Create trauma event from extreme stress"""
        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return None
        
        trauma_event = TraumaEvent(
            id=f"stress_trauma_{agent_id}_{len(self.trauma_events)}",
            trauma_type=TraumaType.ISOLATION_TRAUMA,
            severity=TraumaSeverity.MODERATE if stress_level < 95 else TraumaSeverity.SEVERE,
            timestamp=datetime.now(),
            description=f"{agent.name} experiences psychological trauma from extreme stress",
            source_agent_id=agent_id,
            emotional_impact={"fear": 0.3, "anxiety": 0.4, "despair": 0.2},
            physical_impact={"fatigue": 0.3, "insomnia": 0.2}
        )
        
        self.trauma_events[trauma_event.id] = trauma_event
        
        return {
            "trauma_id": trauma_event.id,
            "agent_id": agent_id,
            "trauma_type": trauma_event.trauma_type.value,
            "severity": trauma_event.severity.value,
            "description": trauma_event.description
        }
    
    def _create_emotional_breakdown_trauma(self, agent_id: str, emotion: str, intensity: float) -> Optional[Dict[str, Any]]:
        """Create trauma event from emotional breakdown"""
        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return None
        
        trauma_event = TraumaEvent(
            id=f"breakdown_trauma_{agent_id}_{len(self.trauma_events)}",
            trauma_type=TraumaType.IDENTITY_TRAUMA,
            severity=TraumaSeverity.SEVERE,
            timestamp=datetime.now(),
            description=f"{agent.name} suffers trauma from emotional breakdown",
            source_agent_id=agent_id,
            emotional_impact={emotion: 0.5, "shame": 0.3, "confusion": 0.4},
            physical_impact={"exhaustion": 0.4}
        )
        
        self.trauma_events[trauma_event.id] = trauma_event
        
        return {
            "trauma_id": trauma_event.id,
            "agent_id": agent_id,
            "trauma_type": trauma_event.trauma_type.value,
            "severity": trauma_event.severity.value,
            "description": trauma_event.description
        }
    
    def _create_betrayal_trauma(self, agent_id: str, betrayer_id: str) -> Optional[Dict[str, Any]]:
        """Create trauma event from betrayal"""
        agent = self.game_state.agents.get(agent_id)
        betrayer = self.game_state.agents.get(betrayer_id)
        if not agent or not betrayer:
            return None
        
        trauma_event = TraumaEvent(
            id=f"betrayal_trauma_{agent_id}_{betrayer_id}_{len(self.trauma_events)}",
            trauma_type=TraumaType.BETRAYAL_TRAUMA,
            severity=TraumaSeverity.SEVERE,
            timestamp=datetime.now(),
            description=f"{agent.name} suffers trauma from betrayal by {betrayer.name}",
            source_agent_id=agent_id,
            emotional_impact={"anger": 0.4, "sadness": 0.5, "trust": -0.6, "paranoia": 0.3},
            physical_impact={"stress": 0.4}
        )
        
        self.trauma_events[trauma_event.id] = trauma_event
        
        return {
            "trauma_id": trauma_event.id,
            "agent_id": agent_id,
            "trauma_type": trauma_event.trauma_type.value,
            "severity": trauma_event.severity.value,
            "description": trauma_event.description
        }
    
    def _process_scar_formation(self) -> List[Dict[str, Any]]:
        """Process formation of emotional scars from trauma"""
        scar_formation_results = []
        
        for trauma_id, trauma_event in self.trauma_events.items():
            if trauma_event.recovery_progress < 0.2 and not trauma_event.is_healing:
                # Check if trauma is severe enough to form scars
                if trauma_event.severity in [TraumaSeverity.SEVERE, TraumaSeverity.CRITICAL, TraumaSeverity.CATASTROPHIC]:
                    # Create emotional scars
                    scars_created = self._create_emotional_scars(trauma_event)
                    if scars_created:
                        scar_formation_results.extend(scars_created)
        
        return scar_formation_results
    
    def _create_emotional_scars(self, trauma_event: TraumaEvent) -> List[Dict[str, Any]]:
        """Create emotional scars from a trauma event"""
        scars_created = []
        
        for emotion, intensity in trauma_event.emotional_impact.items():
            if intensity > 0.3:  # Only create scars for significant emotions
                scar = EmotionalScar(
                    id=f"scar_{trauma_event.id}_{emotion}",
                    trauma_event_id=trauma_event.id,
                    emotion_type=emotion,
                    intensity=intensity,
                    created_timestamp=datetime.now(),
                    trigger_conditions=self._generate_trigger_conditions(trauma_event, emotion),
                    coping_strategies=self._generate_coping_strategies(emotion),
                    is_permanent=intensity > 0.7
                )
                
                agent_id = trauma_event.source_agent_id
                if agent_id:
                    self.emotional_scars[agent_id].append(scar)
                    
                    scars_created.append({
                        "scar_id": scar.id,
                        "agent_id": agent_id,
                        "emotion": emotion,
                        "intensity": intensity,
                        "is_permanent": scar.is_permanent
                    })
        
        return scars_created
    
    def _generate_trigger_conditions(self, trauma_event: TraumaEvent, emotion: str) -> List[Dict[str, Any]]:
        """Generate trigger conditions for emotional scars"""
        conditions = []
        
        # Location-based triggers
        if trauma_event.location:
            conditions.append({
                "type": "location",
                "location": trauma_event.location
            })
        
        # Agent-based triggers
        if trauma_event.source_agent_id:
            conditions.append({
                "type": "agent_present",
                "agent_id": trauma_event.source_agent_id
            })
        
        # Emotion-based triggers
        conditions.append({
            "type": "emotion_level",
            "emotion": emotion,
            "threshold": 0.5
        })
        
        # Stress-based triggers
        conditions.append({
            "type": "stress_level",
            "threshold": 70
        })
        
        return conditions
    
    def _generate_coping_strategies(self, emotion: str) -> List[str]:
        """Generate coping strategies for emotional scars"""
        strategies = []
        
        emotion_strategies = {
            "fear": ["deep_breathing", "grounding_techniques", "safety_planning"],
            "anger": ["physical_exercise", "creative_expression", "time_out"],
            "sadness": ["social_connection", "self_care", "professional_help"],
            "anxiety": ["mindfulness", "progressive_relaxation", "cognitive_restructuring"],
            "paranoia": ["reality_checking", "trust_building", "safety_validation"],
            "shame": ["self_compassion", "vulnerability_sharing", "forgiveness_practice"]
        }
        
        strategies.extend(emotion_strategies.get(emotion, ["general_coping"]))
        
        return strategies
    
    def _process_generational_inheritance(self) -> List[Dict[str, Any]]:
        """Process generational trauma inheritance"""
        inheritance_results = []
        
        # Check for new agents that might inherit trauma
        for agent_id, agent in self.game_state.agents.items():
            if agent_id not in self.generational_trauma:
                # Check if agent has family connections with traumatized agents
                family_trauma = self._check_family_trauma_inheritance(agent_id)
                if family_trauma:
                    inheritance_results.extend(family_trauma)
        
        return inheritance_results
    
    def _check_family_trauma_inheritance(self, agent_id: str) -> List[Dict[str, Any]]:
        """Check for family trauma inheritance"""
        inheritance_results = []
        
        # Look for family relationships with traumatized agents
        agent = self.game_state.agents.get(agent_id)
        if not agent or not hasattr(agent, 'relationships'):
            return inheritance_results
        
        for other_id, relationship in agent.relationships.items():
            if relationship.bond_type.value == "family":
                # Check if family member has trauma
                family_trauma = self._get_agent_trauma(other_id)
                if family_trauma and random.random() < self.generational_inheritance_chance:
                    # Create generational trauma
                    generational_trauma = self._create_generational_trauma(agent_id, other_id, family_trauma)
                    if generational_trauma:
                        inheritance_results.append(generational_trauma)
        
        return inheritance_results
    
    def _get_agent_trauma(self, agent_id: str) -> Optional[TraumaEvent]:
        """Get the most significant trauma for an agent"""
        agent_trauma = [t for t in self.trauma_events.values() if t.source_agent_id == agent_id]
        if not agent_trauma:
            return None
        
        # Return the most severe trauma
        return max(agent_trauma, key=lambda t: t.severity.value)
    
    def _create_generational_trauma(self, child_id: str, parent_id: str, parent_trauma: TraumaEvent) -> Optional[Dict[str, Any]]:
        """Create generational trauma inheritance"""
        generational_trauma = GenerationalTrauma(
            id=f"generational_{child_id}_{parent_trauma.id}",
            original_trauma_id=parent_trauma.id,
            generation=1,
            inherited_agent_id=child_id,
            trauma_type=parent_trauma.trauma_type,
            inherited_triggers=parent_trauma.triggers.copy(),
            family_patterns=[f"inherited_from_{parent_id}"]
        )
        
        self.generational_trauma[child_id].append(generational_trauma)
        
        return {
            "generational_trauma_id": generational_trauma.id,
            "child_id": child_id,
            "parent_id": parent_id,
            "trauma_type": generational_trauma.trauma_type.value,
            "intensity": generational_trauma.get_effective_intensity()
        }
    
    def _process_recovery_programs(self) -> List[Dict[str, Any]]:
        """Process active recovery programs"""
        recovery_results = []
        
        for program_id, program in self.recovery_programs.items():
            if program.active:
                # Calculate daily progress
                daily_progress = program.get_daily_progress()
                old_progress = program.progress
                
                # Update progress
                program.update_progress(daily_progress)
                
                if program.progress != old_progress:
                    recovery_results.append({
                        "program_id": program_id,
                        "agent_id": program.agent_id,
                        "old_progress": old_progress,
                        "new_progress": program.progress,
                        "daily_progress": daily_progress,
                        "completed": program.completed
                    })
                    
                    # Apply recovery effects if completed
                    if program.completed:
                        self._apply_recovery_effects(program)
        
        return recovery_results
    
    def _apply_recovery_effects(self, program: RecoveryProgram):
        """Apply effects of completed recovery program"""
        agent = self.game_state.agents.get(program.agent_id)
        if not agent or not hasattr(agent, 'emotional_state'):
            return
        
        # Reduce trauma levels
        for trauma_id in program.trauma_event_ids:
            trauma_event = self.trauma_events.get(trauma_id)
            if trauma_event:
                trauma_event.recovery_progress = min(1.0, trauma_event.recovery_progress + 0.3)
                trauma_event.is_healing = True
        
        # Improve emotional state
        emotional_improvements = {
            "fear": -0.2,
            "anxiety": -0.2,
            "sadness": -0.15,
            "anger": -0.1,
            "hope": 0.2,
            "trust": 0.1
        }
        
        for emotion, improvement in emotional_improvements.items():
            if hasattr(agent.emotional_state, emotion):
                current_value = getattr(agent.emotional_state, emotion)
                new_value = max(-1.0, min(1.0, current_value + improvement))
                setattr(agent.emotional_state, emotion, new_value)
        
        # Reduce stress
        agent.stress = max(0, agent.stress - 20)
    
    def _check_psychological_crises(self) -> List[Dict[str, Any]]:
        """Check for psychological crises"""
        crisis_results = []
        
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'emotional_state'):
                continue
            
            # Check for crisis conditions
            crisis_conditions = self._evaluate_crisis_conditions(agent)
            if crisis_conditions:
                crisis_results.append({
                    "agent_id": agent_id,
                    "crisis_type": crisis_conditions["type"],
                    "severity": crisis_conditions["severity"],
                    "description": crisis_conditions["description"],
                    "required_intervention": crisis_conditions["intervention_needed"]
                })
        
        return crisis_results
    
    def _evaluate_crisis_conditions(self, agent) -> Optional[Dict[str, Any]]:
        """Evaluate if agent is in psychological crisis"""
        
        # Multiple trauma events
        agent_trauma = [t for t in self.trauma_events.values() if t.source_agent_id == agent.id]
        if len(agent_trauma) >= 3:
            return {
                "type": "multiple_trauma",
                "severity": "critical",
                "description": f"{agent.name} is overwhelmed by multiple traumatic experiences",
                "intervention_needed": "immediate_therapy"
            }
        
        # Severe emotional state
        emotional_state = agent.emotional_state
        dominant_emotion, intensity = emotional_state.get_dominant_emotion()
        if intensity > 0.95:
            return {
                "type": "emotional_crisis",
                "severity": "severe",
                "description": f"{agent.name} is experiencing an emotional crisis",
                "intervention_needed": "emotional_support"
            }
        
        # High stress with trauma
        if agent.stress > 95 and agent_trauma:
            return {
                "type": "stress_crisis",
                "severity": "moderate",
                "description": f"{agent.name} is experiencing a stress-related crisis",
                "intervention_needed": "stress_management"
            }
        
        return None
    
    def _check_healing_breakthroughs(self) -> List[Dict[str, Any]]:
        """Check for healing breakthroughs"""
        breakthrough_results = []
        
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'emotional_state'):
                continue
            
            # Check for breakthrough conditions
            breakthrough = self._evaluate_breakthrough_conditions(agent)
            if breakthrough:
                breakthrough_results.append(breakthrough)
        
        return breakthrough_results
    
    def _evaluate_breakthrough_conditions(self, agent) -> Optional[Dict[str, Any]]:
        """Evaluate if agent has experienced a healing breakthrough"""
        
        # Significant improvement in emotional state
        emotional_state = agent.emotional_state
        positive_emotions = ["joy", "trust", "hope", "anticipation"]
        positive_sum = sum(max(0, getattr(emotional_state, emotion, 0)) for emotion in positive_emotions)
        
        if positive_sum > 1.5:  # Significant positive emotional state
            return {
                "agent_id": agent.id,
                "type": "emotional_breakthrough",
                "description": f"{agent.name} experiences a breakthrough in emotional healing",
                "effects": {"positive_emotions": positive_sum, "stress_reduction": 15}
            }
        
        # Recovery from severe trauma
        agent_trauma = [t for t in self.trauma_events.values() if t.source_agent_id == agent.id]
        recovered_trauma = [t for t in agent_trauma if t.recovery_progress > 0.8]
        
        if len(recovered_trauma) > 0 and len(recovered_trauma) == len(agent_trauma):
            return {
                "agent_id": agent.id,
                "type": "trauma_recovery_breakthrough",
                "description": f"{agent.name} achieves breakthrough in trauma recovery",
                "effects": {"trauma_reduction": len(recovered_trauma), "resilience_increase": 0.2}
            }
        
        return None
    
    def create_recovery_program(self, agent_id: str, methods: List[RecoveryMethod], duration_days: int = 30) -> Optional[RecoveryProgram]:
        """Create a recovery program for an agent"""
        agent = self.game_state.agents.get(agent_id)
        if not agent:
            return None
        
        # Get agent's trauma events
        agent_trauma = [t.id for t in self.trauma_events.values() if t.source_agent_id == agent_id]
        if not agent_trauma:
            return None
        
        program = RecoveryProgram(
            id=f"recovery_{agent_id}_{len(self.recovery_programs)}",
            agent_id=agent_id,
            trauma_event_ids=agent_trauma,
            methods=methods,
            start_timestamp=datetime.now(),
            duration_days=duration_days,
            success_probability=0.7,
            cost=len(methods) * self.therapy_cost
        )
        
        self.recovery_programs[program.id] = program
        
        return program
    
    def _update_trauma_statistics(self):
        """Update trauma system statistics"""
        active_trauma = [t for t in self.trauma_events.values() if not t.is_healing]
        active_programs = [p for p in self.recovery_programs.values() if p.active]
        completed_programs = [p for p in self.recovery_programs.values() if p.completed]
        
        self.trauma_statistics = {
            "total_trauma_events": len(self.trauma_events),
            "active_trauma_events": len(active_trauma),
            "total_emotional_scars": sum(len(scars) for scars in self.emotional_scars.values()),
            "generational_trauma_count": sum(len(trauma) for trauma in self.generational_trauma.values()),
            "recovery_programs_active": len(active_programs),
            "recovery_success_rate": len(completed_programs) / max(1, len(self.recovery_programs))
        }
    
    def get_trauma_summary(self) -> Dict[str, Any]:
        """Get comprehensive trauma system summary"""
        
        return {
            "trauma_statistics": self.trauma_statistics,
            "recovery_statistics": self.recovery_statistics,
            "generational_patterns": dict(self.generational_patterns),
            "system_efficiency": self._calculate_trauma_system_efficiency(),
            "crisis_indicators": self._get_crisis_indicators(),
            "recovery_opportunities": self._get_recovery_opportunities()
        }
    
    def _calculate_trauma_system_efficiency(self) -> float:
        """Calculate trauma system efficiency"""
        
        if not self.trauma_events:
            return 0.0
        
        # Recovery rate
        total_trauma = len(self.trauma_events)
        healing_trauma = sum(1 for t in self.trauma_events.values() if t.is_healing)
        recovery_rate = healing_trauma / total_trauma
        
        # Program success rate
        program_success = self.trauma_statistics["recovery_success_rate"]
        
        # Scar management
        total_scars = self.trauma_statistics["total_emotional_scars"]
        managed_scars = sum(1 for scars in self.emotional_scars.values() 
                          for scar in scars if scar.coping_strategies)
        scar_management_rate = managed_scars / max(1, total_scars)
        
        overall_efficiency = (
            recovery_rate * 0.4 +
            program_success * 0.3 +
            scar_management_rate * 0.3
        )
        
        return min(1.0, overall_efficiency)
    
    def _get_crisis_indicators(self) -> List[Dict[str, Any]]:
        """Get indicators of potential psychological crises"""
        indicators = []
        
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'emotional_state'):
                continue
            
            # High trauma load
            agent_trauma = [t for t in self.trauma_events.values() if t.source_agent_id == agent_id]
            if len(agent_trauma) >= 2:
                indicators.append({
                    "agent_id": agent_id,
                    "type": "high_trauma_load",
                    "severity": "moderate",
                    "description": f"Agent has {len(agent_trauma)} trauma events"
                })
            
            # Emotional instability
            emotional_state = agent.emotional_state
            dominant_emotion, intensity = emotional_state.get_dominant_emotion()
            if intensity > 0.8:
                indicators.append({
                    "agent_id": agent_id,
                    "type": "emotional_instability",
                    "severity": "high",
                    "description": f"High {dominant_emotion} intensity: {intensity:.2f}"
                })
        
        return indicators
    
    def _get_recovery_opportunities(self) -> List[Dict[str, Any]]:
        """Get opportunities for trauma recovery"""
        opportunities = []
        
        for agent_id, agent in self.game_state.agents.items():
            if not hasattr(agent, 'emotional_state'):
                continue
            
            # Agents with trauma but no recovery program
            agent_trauma = [t for t in self.trauma_events.values() if t.source_agent_id == agent_id]
            active_program = any(p.agent_id == agent_id and p.active 
                               for p in self.recovery_programs.values())
            
            if agent_trauma and not active_program:
                opportunities.append({
                    "agent_id": agent_id,
                    "type": "recovery_program_needed",
                    "trauma_count": len(agent_trauma),
                    "recommended_methods": self._recommend_recovery_methods(agent_trauma)
                })
        
        return opportunities
    
    def _recommend_recovery_methods(self, trauma_events: List[TraumaEvent]) -> List[RecoveryMethod]:
        """Recommend recovery methods based on trauma types"""
        methods = []
        
        trauma_types = [t.trauma_type for t in trauma_events]
        
        if TraumaType.BETRAYAL_TRAUMA in trauma_types:
            methods.extend([RecoveryMethod.THERAPY, RecoveryMethod.SOCIAL_SUPPORT])
        
        if TraumaType.COMBAT_TRAUMA in trauma_types:
            methods.extend([RecoveryMethod.PROFESSIONAL_HELP, RecoveryMethod.PHYSICAL_ACTIVITY])
        
        if TraumaType.ISOLATION_TRAUMA in trauma_types:
            methods.extend([RecoveryMethod.SOCIAL_SUPPORT, RecoveryMethod.CREATIVE_EXPRESSION])
        
        if TraumaType.MORAL_INJURY in trauma_types:
            methods.extend([RecoveryMethod.SPIRITUAL_HEALING, RecoveryMethod.THERAPY])
        
        # Add general methods if not enough specific ones
        if len(methods) < 2:
            methods.extend([RecoveryMethod.REST_AND_RECOVERY, RecoveryMethod.MEDICATION])
        
        return methods[:3]  # Limit to 3 methods 