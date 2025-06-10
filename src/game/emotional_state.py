"""
Years of Lead - Emotional State System

This module implements the emotional state mechanics for agents,
tracking how traumatic events and experiences affect their psychological well-being.
Based on Plutchik's Wheel of Emotions with trauma persistence modeling.
"""

import math
import random
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from copy import deepcopy
from datetime import datetime, timedelta
from enum import Enum


class TraumaTriggerType(Enum):
    """Types of trauma triggers that can reactivate past trauma"""
    VIOLENCE = "violence"
    BETRAYAL = "betrayal"
    ABANDONMENT = "abandonment"
    CONFINEMENT = "confinement"
    AUTHORITY_FIGURES = "authority_figures"
    CROWDS = "crowds"
    DARKNESS = "darkness"
    LOUD_NOISES = "loud_noises"
    SPECIFIC_LOCATION = "specific_location"
    ANNIVERSARY_DATE = "anniversary_date"


# Therapy System Expansion - ITERATION 016
class SpecificTraumaType(Enum):
    """Specific types of trauma requiring targeted therapy approaches"""
    GUILT = "guilt"                    # Survivor's guilt, moral injury
    GRIEF = "grief"                    # Loss of comrades, family
    ANXIETY = "anxiety"                # Performance anxiety, hypervigilance
    PTSD = "ptsd"                      # Post-traumatic stress disorder
    DEPRESSION = "depression"          # Persistent sadness, hopelessness
    DISSOCIATION = "dissociation"      # Emotional detachment, numbness
    PARANOIA = "paranoia"              # Mistrust, persecution fears
    RAGE = "rage"                      # Uncontrolled anger, revenge obsession

class TherapyStage(Enum):
    """Stages of therapy recovery"""
    INITIAL = "initial"                # First acknowledgment of trauma
    PROCESSING = "processing"          # Working through trauma memories
    INTEGRATION = "integration"        # Incorporating healing into identity
    MAINTENANCE = "maintenance"        # Ongoing support and relapse prevention
    RELAPSE = "relapse"               # Temporary setback in recovery

@dataclass
class TherapySession:
    """Individual therapy session with progress tracking"""
    session_date: datetime
    therapy_type: TherapyType
    duration_hours: float
    therapist_id: Optional[str] = None    # Agent providing peer support
    focus_trauma: Optional[str] = None    # Specific trauma being addressed
    effectiveness: float = 0.0            # Session effectiveness (0-1)
    breakthrough: bool = False            # Major breakthrough achieved
    setback: bool = False                # Setback or resistance encountered
    
@dataclass
class RecoveryArc:
    """Multi-session recovery tracking for specific trauma"""
    trauma_id: str
    trauma_type: SpecificTraumaType
    current_stage: TherapyStage = TherapyStage.INITIAL
    sessions_completed: int = 0
    total_progress: float = 0.0           # Overall recovery progress (0-1)
    relapse_risk: float = 0.3             # Risk of setback (0-1)
    last_session: Optional[datetime] = None
    therapy_sessions: List[TherapySession] = field(default_factory=list)
    
    # Relationship support tracking
    supported_by: List[str] = field(default_factory=list)  # Agent IDs providing support
    mentor_id: Optional[str] = None       # Primary mentor if any
    support_strength: float = 0.0         # Quality of support network (0-1)
    
    def calculate_stage_advancement(self) -> bool:
        """Check if ready to advance to next therapy stage"""
        required_sessions = {
            TherapyStage.INITIAL: 2,
            TherapyStage.PROCESSING: 5,
            TherapyStage.INTEGRATION: 3,
            TherapyStage.MAINTENANCE: 0  # Ongoing
        }
        
        if self.current_stage == TherapyStage.RELAPSE:
            # Need to rebuild progress after relapse
            if self.sessions_completed >= 3 and self.total_progress > 0.4:
                return True
        else:
            required = required_sessions.get(self.current_stage, 0)
            return self.sessions_completed >= required and self.total_progress > 0.6
    
    def calculate_relapse_risk(self) -> float:
        """Calculate current risk of psychological relapse"""
        base_risk = 0.3
        
        # Progress reduces risk
        progress_reduction = self.total_progress * 0.4
        
        # Support network reduces risk
        support_reduction = self.support_strength * 0.3
        
        # Time since last session increases risk
        if self.last_session:
            days_since = (datetime.now() - self.last_session).days
            time_penalty = min(0.2, days_since * 0.01)
        else:
            time_penalty = 0.2
        
        # Stage affects risk
        stage_modifiers = {
            TherapyStage.INITIAL: 0.1,
            TherapyStage.PROCESSING: 0.0,  # Most vulnerable stage
            TherapyStage.INTEGRATION: -0.1,
            TherapyStage.MAINTENANCE: -0.2,
            TherapyStage.RELAPSE: 0.3
        }
        
        stage_modifier = stage_modifiers.get(self.current_stage, 0.0)
        
        risk = base_risk - progress_reduction - support_reduction + time_penalty + stage_modifier
        return max(0.0, min(1.0, risk))


class TherapyType(Enum):
    """Types of therapy or rest available to agents"""
    REST = "rest"                          # Basic rest and recovery
    PEER_SUPPORT = "peer_support"          # Support from fellow agents
    PROFESSIONAL = "professional"          # Professional therapy (if available)
    MEDITATION = "meditation"              # Self-directed mindfulness
    PHYSICAL_ACTIVITY = "physical_activity" # Exercise and physical outlets
    CREATIVE_EXPRESSION = "creative_expression" # Art, writing, music
    SUBSTANCE_USE = "substance_use"        # Self-medication (risky)
    
    # New relationship-based therapy types - ITERATION 016
    MENTOR_GUIDANCE = "mentor_guidance"    # One-on-one mentoring from experienced agent
    GROUP_THERAPY = "group_therapy"        # Group sessions with other trauma survivors
    CONFESSIONAL = "confessional"          # Admitting guilt/mistakes to trusted friend
    SOLIDARITY_RITUAL = "solidarity_ritual" # Shared ceremonies strengthening bonds


@dataclass
class TraumaMemory:
    """Represents a specific traumatic memory with triggers"""
    trauma_type: str
    severity: float
    occurred_date: datetime
    triggers: List[TraumaTriggerType]
    description: str
    times_triggered: int = 0
    last_triggered: Optional[datetime] = None
    therapy_progress: float = 0.0  # 0.0 to 1.0, how much it's been processed
    
    def check_trigger(self, current_triggers: List[TraumaTriggerType]) -> Tuple[bool, float]:
        """Check if this trauma is triggered by current events"""
        matching_triggers = set(self.triggers) & set(current_triggers)
        if matching_triggers:
            # More matches = stronger trigger
            intensity = len(matching_triggers) / len(self.triggers)
            # Recent triggers make it more sensitive
            if self.last_triggered:
                days_since = (datetime.now() - self.last_triggered).days
                if days_since < 7:
                    intensity *= 1.5
            
            # Therapy progress reduces trigger intensity
            intensity *= (1.0 - self.therapy_progress * 0.7)
            
            return True, min(1.0, intensity)
        return False, 0.0
    
    def apply_trigger(self):
        """Record that this trauma was triggered"""
        self.times_triggered += 1
        self.last_triggered = datetime.now()
    
    def apply_therapy(self, therapy_effectiveness: float):
        """Apply therapy progress to this trauma"""
        self.therapy_progress = min(1.0, self.therapy_progress + therapy_effectiveness)


@dataclass
class EmotionalState:
    """
    Represents an agent's emotional state using Plutchik's 8 basic emotions.
    All values are normalized between -1.0 and 1.0.
    """
    fear: float = 0.0           # Fear of danger, government, discovery
    anger: float = 0.0          # Anger at injustice, system, betrayal  
    sadness: float = 0.0        # Grief, loss, despair
    joy: float = 0.0            # Hope, satisfaction, triumph
    trust: float = 0.0          # Faith in cause, comrades, leadership
    anticipation: float = 0.0   # Expectation, planning, future focus
    surprise: float = 0.0       # Shock, unexpected events
    disgust: float = 0.0        # Revulsion at system, betrayal, corruption
    
    # Trauma tracking
    trauma_level: float = 0.0   # Overall accumulated trauma (0.0 to 1.0)
    last_trauma_intensity: float = 0.0  # Intensity of most recent trauma
    trauma_decay_rate: float = 0.02     # How quickly trauma fades
    
    # Extended trauma system
    trauma_memories: List[TraumaMemory] = field(default_factory=list)
    therapy_history: List[Tuple[datetime, TherapyType, float]] = field(default_factory=list)
    rest_days: int = 0  # Days of rest taken
    last_rest_date: Optional[datetime] = None
    
    # Enhanced therapy system - ITERATION 016
    recovery_arcs: Dict[str, RecoveryArc] = field(default_factory=dict)  # trauma_id -> RecoveryArc
    therapy_sessions: List[TherapySession] = field(default_factory=list)
    mentor_relationships: List[str] = field(default_factory=list)  # Agent IDs who can mentor
    therapy_resistance: float = 0.0      # How resistant to therapy (0-1)
    last_relapse: Optional[datetime] = None
    
    def __post_init__(self):
        """Ensure all emotional values are within bounds after initialization"""
        self._clamp_values()
    
    def _clamp_values(self):
        """Ensure all emotional values stay within -1.0 to 1.0 bounds"""
        emotions = ['fear', 'anger', 'sadness', 'joy', 'trust', 'anticipation', 'surprise', 'disgust']
        for emotion in emotions:
            value = getattr(self, emotion)
            setattr(self, emotion, max(-1.0, min(1.0, float(value))))
        
        # Clamp trauma values
        self.trauma_level = max(0.0, min(1.0, self.trauma_level))
        self.last_trauma_intensity = max(0.0, min(1.0, self.last_trauma_intensity))
    
    def copy(self):
        """Create a deep copy of this emotional state"""
        return deepcopy(self)
    
    def apply_drift(self, time_delta: float = 1.0):
        """
        Apply natural emotional drift over time.
        Emotions gradually return toward neutral unless reinforced.
        """
        drift_rate = 0.05 * time_delta  # Base drift rate per time unit
        
        # Emotions drift toward zero (neutral) unless trauma is high
        trauma_resistance = 1.0 - (self.trauma_level * 0.5)  # High trauma slows positive drift
        
        emotions = ['fear', 'anger', 'sadness', 'joy', 'trust', 'anticipation', 'surprise', 'disgust']
        
        for emotion in emotions:
            current_value = getattr(self, emotion)
            
            if current_value > 0:
                # Positive emotions drift down
                drift_amount = min(current_value, drift_rate * trauma_resistance)
                new_value = current_value - drift_amount
            elif current_value < 0:
                # Negative emotions also drift toward neutral, but slower if trauma is high
                if emotion in ['fear', 'sadness'] and self.trauma_level > 0.3:
                    # Fear and sadness persist longer when traumatized
                    effective_drift = drift_rate * trauma_resistance * 0.5
                else:
                    effective_drift = drift_rate * trauma_resistance
                
                drift_amount = min(abs(current_value), effective_drift)
                new_value = current_value + drift_amount
            else:
                new_value = current_value
            
            setattr(self, emotion, new_value)
        
        # Gradually reduce trauma over time
        if self.trauma_level > 0:
            # Rest accelerates trauma recovery
            recovery_rate = self.trauma_decay_rate
            if self.last_rest_date and (datetime.now() - self.last_rest_date).days < 7:
                recovery_rate *= 2.0
            
            self.trauma_level = max(0.0, self.trauma_level - recovery_rate * time_delta)
        
        self._clamp_values()
    
    def apply_emotional_impact(self, impact: Dict[str, float], intensity: float = 1.0):
        """
        Apply an emotional impact from an event.
        
        Args:
            impact: Dictionary mapping emotion names to impact values
            intensity: Multiplier for the impact strength (0.0 to 1.0)
        """
        intensity = max(0.0, min(1.0, intensity))
        
        for emotion, value in impact.items():
            if hasattr(self, emotion):
                current_value = getattr(self, emotion)
                impact_value = value * intensity
                
                # Apply diminishing returns for extreme values
                if abs(current_value) > 0.7:
                    impact_value *= 0.5
                
                new_value = current_value + impact_value
                setattr(self, emotion, new_value)
        
        self._clamp_values()
    
    def apply_trauma(self, trauma_intensity: float, event_type: str = "general", 
                    triggers: Optional[List[TraumaTriggerType]] = None):
        """
        Apply traumatic impact with persistent effects.
        
        Args:
            trauma_intensity: How traumatic the event was (0.0 to 1.0)
            event_type: Type of traumatic event for specialized handling
            triggers: List of trigger types associated with this trauma
        """
        trauma_intensity = max(0.0, min(1.0, trauma_intensity))
        
        # Update trauma tracking
        self.last_trauma_intensity = trauma_intensity
        self.trauma_level = min(1.0, self.trauma_level + trauma_intensity * 0.3)
        
        # Base trauma impacts
        trauma_impact = {
            'fear': trauma_intensity * 0.8,
            'sadness': trauma_intensity * 0.6,
            'anger': trauma_intensity * 0.4,
            'trust': -trauma_intensity * 0.5
        }
        
        # Event-specific trauma modifications and triggers
        default_triggers = []
        if event_type == "violence_witnessed":
            trauma_impact['fear'] += trauma_intensity * 0.4
            trauma_impact['disgust'] = trauma_intensity * 0.3
            default_triggers = [TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES]
        elif event_type == "betrayal":
            trauma_impact['trust'] -= trauma_intensity * 0.8
            trauma_impact['anger'] += trauma_intensity * 0.6
            default_triggers = [TraumaTriggerType.BETRAYAL]
        elif event_type == "loss_of_comrade":
            trauma_impact['sadness'] += trauma_intensity * 0.7
            trauma_impact['anger'] += trauma_intensity * 0.3
            default_triggers = [TraumaTriggerType.ABANDONMENT]
        elif event_type == "imprisonment":
            trauma_impact['fear'] += trauma_intensity * 0.5
            default_triggers = [TraumaTriggerType.CONFINEMENT, TraumaTriggerType.AUTHORITY_FIGURES]
        
        self.apply_emotional_impact(trauma_impact, intensity=1.0)
        
        # Create trauma memory if significant
        if trauma_intensity > 0.3:
            memory = TraumaMemory(
                trauma_type=event_type,
                severity=trauma_intensity,
                occurred_date=datetime.now(),
                triggers=triggers or default_triggers,
                description=f"Traumatic {event_type} event"
            )
            self.trauma_memories.append(memory)
    
    def check_trauma_triggers(self, current_triggers: List[TraumaTriggerType]) -> List[Tuple[TraumaMemory, float]]:
        """Check if current events trigger past traumas"""
        triggered_traumas = []
        
        for memory in self.trauma_memories:
            is_triggered, intensity = memory.check_trigger(current_triggers)
            if is_triggered:
                triggered_traumas.append((memory, intensity))
                memory.apply_trigger()
        
        # Apply emotional impact from triggered traumas
        for memory, intensity in triggered_traumas:
            trigger_impact = {
                'fear': intensity * 0.6,
                'sadness': intensity * 0.4,
                'anger': intensity * 0.3,
                'surprise': intensity * 0.5,
                'trust': -intensity * 0.2
            }
            self.apply_emotional_impact(trigger_impact)
            
            # Increase overall trauma level
            self.trauma_level = min(1.0, self.trauma_level + intensity * 0.1)
        
        return triggered_traumas
    
    def apply_enhanced_therapy(self, therapy_type: TherapyType, duration_hours: float = 1.0,
                             therapist_id: Optional[str] = None, 
                             focus_trauma_id: Optional[str] = None,
                             relationship_strength: float = 0.0) -> Dict[str, Any]:
        """Enhanced therapy system with relationship bonuses and recovery arcs - ITERATION 016"""
        results = {
            'therapy_type': therapy_type.value,
            'duration_hours': duration_hours,
            'therapist_id': therapist_id,
            'effectiveness': 0.0,
            'trauma_reduced': 0.0,
            'emotions_improved': {},
            'side_effects': [],
            'breakthrough': False,
            'setback': False,
            'stage_advancement': False
        }
        
        # Calculate base effectiveness
        base_effectiveness = self._calculate_therapy_effectiveness(therapy_type, duration_hours)
        
        # Apply relationship bonuses
        relationship_bonus = self._calculate_relationship_therapy_bonus(
            therapy_type, therapist_id, relationship_strength
        )
        
        # Apply therapy resistance
        resistance_penalty = self.therapy_resistance * 0.3
        
        # Final effectiveness
        effectiveness = max(0.1, min(1.0, base_effectiveness + relationship_bonus - resistance_penalty))
        results['effectiveness'] = effectiveness
        
        # Create therapy session record
        session = TherapySession(
            session_date=datetime.now(),
            therapy_type=therapy_type,
            duration_hours=duration_hours,
            therapist_id=therapist_id,
            focus_trauma=focus_trauma_id,
            effectiveness=effectiveness
        )
        
        # Check for breakthrough or setback
        if effectiveness > 0.8 and random.random() < 0.2:
            session.breakthrough = True
            results['breakthrough'] = True
            effectiveness *= 1.5  # Breakthrough amplifies benefits
            
        elif effectiveness < 0.3 and random.random() < 0.3:
            session.setback = True
            results['setback'] = True
            self.therapy_resistance = min(1.0, self.therapy_resistance + 0.1)
            results['side_effects'].append('increased_therapy_resistance')
        
        # Apply therapy to specific trauma if specified
        if focus_trauma_id and focus_trauma_id in self.recovery_arcs:
            arc = self.recovery_arcs[focus_trauma_id]
            self._process_recovery_arc_session(arc, session, effectiveness, results)
        else:
            # General trauma reduction
            old_trauma = self.trauma_level
            trauma_reduction = effectiveness * 0.15
            self.trauma_level = max(0.0, self.trauma_level - trauma_reduction)
            results['trauma_reduced'] = old_trauma - self.trauma_level
        
        # Apply therapy-specific effects
        self._apply_therapy_specific_effects(therapy_type, effectiveness, results)
        
        # Record session
        self.therapy_sessions.append(session)
        self.therapy_history.append((datetime.now(), therapy_type, effectiveness))
        
        # Check for relapse risk in all recovery arcs
        self._check_relapse_risks()
        
        self._clamp_values()
        return results
    
    def _calculate_therapy_effectiveness(self, therapy_type: TherapyType, duration: float) -> float:
        """Calculate base therapy effectiveness"""
        base_values = {
            TherapyType.REST: 0.2,
            TherapyType.PEER_SUPPORT: 0.4,
            TherapyType.PROFESSIONAL: 0.7,
            TherapyType.MEDITATION: 0.3,
            TherapyType.PHYSICAL_ACTIVITY: 0.35,
            TherapyType.CREATIVE_EXPRESSION: 0.4,
            TherapyType.SUBSTANCE_USE: 0.5,  # High short-term, low long-term
            TherapyType.MENTOR_GUIDANCE: 0.6,
            TherapyType.GROUP_THERAPY: 0.5,
            TherapyType.CONFESSIONAL: 0.45,
            TherapyType.SOLIDARITY_RITUAL: 0.4
        }
        
        base = base_values.get(therapy_type, 0.3)
        
        # Duration affects effectiveness
        duration_modifier = min(1.2, 1.0 + (duration - 1.0) * 0.1)
        
        return base * duration_modifier
    
    def _calculate_relationship_therapy_bonus(self, therapy_type: TherapyType, 
                                            therapist_id: Optional[str],
                                            relationship_strength: float) -> float:
        """Calculate bonus from relationships in therapy"""
        if not therapist_id:
            return 0.0
        
        # Base relationship bonus
        base_bonus = relationship_strength * 0.3
        
        # Therapy type specific bonuses
        if therapy_type == TherapyType.PEER_SUPPORT:
            # Peer support gets major relationship bonus
            return base_bonus * 1.5
        elif therapy_type == TherapyType.MENTOR_GUIDANCE:
            # Mentoring requires strong relationship
            if therapist_id in self.mentor_relationships:
                return base_bonus * 2.0
            else:
                return base_bonus * 0.5  # Weak mentoring without established relationship
        elif therapy_type == TherapyType.CONFESSIONAL:
            # Confessional requires high trust
            if relationship_strength > 0.7:
                return base_bonus * 1.8
            else:
                return -0.1  # Backfires without trust
        elif therapy_type == TherapyType.GROUP_THERAPY:
            # Group therapy benefits from multiple relationships
            group_size = len(self.mentor_relationships) + 1
            return base_bonus * min(1.5, 1.0 + group_size * 0.1)
        elif therapy_type == TherapyType.SOLIDARITY_RITUAL:
            # Ritual bonding
            return base_bonus * 1.3
        
        return base_bonus
    
    def _process_recovery_arc_session(self, arc: RecoveryArc, session: TherapySession,
                                    effectiveness: float, results: Dict[str, Any]) -> None:
        """Process therapy session for specific recovery arc"""
        arc.sessions_completed += 1
        arc.last_session = session.session_date
        
        # Progress based on effectiveness and stage
        stage_multipliers = {
            TherapyStage.INITIAL: 0.8,
            TherapyStage.PROCESSING: 1.0,
            TherapyStage.INTEGRATION: 1.2,
            TherapyStage.MAINTENANCE: 0.5,
            TherapyStage.RELAPSE: 0.6
        }
        
        stage_mult = stage_multipliers.get(arc.current_stage, 1.0)
        progress_gain = effectiveness * 0.2 * stage_mult
        arc.total_progress = min(1.0, arc.total_progress + progress_gain)
        
        # Check for stage advancement
        if arc.calculate_stage_advancement():
            old_stage = arc.current_stage
            if arc.current_stage == TherapyStage.INITIAL:
                arc.current_stage = TherapyStage.PROCESSING
            elif arc.current_stage == TherapyStage.PROCESSING:
                arc.current_stage = TherapyStage.INTEGRATION
            elif arc.current_stage == TherapyStage.INTEGRATION:
                arc.current_stage = TherapyStage.MAINTENANCE
            elif arc.current_stage == TherapyStage.RELAPSE:
                arc.current_stage = TherapyStage.PROCESSING
            
            results['stage_advancement'] = True
            results['old_stage'] = old_stage.value
            results['new_stage'] = arc.current_stage.value
        
        # Update relapse risk
        arc.relapse_risk = arc.calculate_relapse_risk()
        
        # Reduce trauma level based on progress
        trauma_reduction = progress_gain * 0.5
        old_trauma = self.trauma_level
        self.trauma_level = max(0.0, self.trauma_level - trauma_reduction)
        results['trauma_reduced'] = old_trauma - self.trauma_level
    
    def _apply_therapy_specific_effects(self, therapy_type: TherapyType, 
                                      effectiveness: float, results: Dict[str, Any]) -> None:
        """Apply specific effects based on therapy type"""
        if therapy_type == TherapyType.MENTOR_GUIDANCE:
            # Mentoring builds trust and reduces anxiety
            results['emotions_improved']['trust'] = effectiveness * 0.2
            results['emotions_improved']['fear'] = -effectiveness * 0.15
            
        elif therapy_type == TherapyType.GROUP_THERAPY:
            # Group therapy reduces isolation
            results['emotions_improved']['sadness'] = -effectiveness * 0.2
            results['emotions_improved']['trust'] = effectiveness * 0.15
            
        elif therapy_type == TherapyType.CONFESSIONAL:
            # Confession can provide relief but may increase vulnerability
            if effectiveness > 0.6:
                results['emotions_improved']['guilt_relief'] = effectiveness * 0.3
                results['emotions_improved']['trust'] = effectiveness * 0.1
            else:
                results['side_effects'].append('increased_vulnerability')
                results['emotions_improved']['fear'] = effectiveness * 0.1
                
        elif therapy_type == TherapyType.SOLIDARITY_RITUAL:
            # Rituals strengthen group bonds and purpose
            results['emotions_improved']['trust'] = effectiveness * 0.25
            results['emotions_improved']['anticipation'] = effectiveness * 0.15
            
        elif therapy_type == TherapyType.SUBSTANCE_USE:
            # Substance use - immediate relief but long-term problems
            results['emotions_improved']['fear'] = -effectiveness * 0.3
            results['emotions_improved']['sadness'] = -effectiveness * 0.2
            if random.random() < 0.4:
                results['side_effects'].append('addiction_risk')
                self.therapy_resistance += 0.05
        
        # Apply emotional improvements
        for emotion, change in results['emotions_improved'].items():
            if hasattr(self, emotion):
                current = getattr(self, emotion)
                setattr(self, emotion, max(-1.0, min(1.0, current + change)))
    
    def _check_relapse_risks(self) -> None:
        """Check for psychological relapses in recovery arcs"""
        for arc in self.recovery_arcs.values():
            current_risk = arc.calculate_relapse_risk()
            if random.random() < current_risk:
                self._trigger_relapse(arc)
    
    def _trigger_relapse(self, arc: RecoveryArc) -> None:
        """Trigger a psychological relapse for a recovery arc"""
        arc.current_stage = TherapyStage.RELAPSE
        arc.total_progress *= 0.7  # Lose some progress
        arc.relapse_risk = 0.6  # High risk period
        self.last_relapse = datetime.now()
        
        # Emotional impact of relapse
        relapse_impact = {
            'fear': 0.3,
            'sadness': 0.4,
            'anger': 0.2,
            'trust': -0.3
        }
        self.apply_emotional_impact(relapse_impact)
        
        # Increase trauma level
        self.trauma_level = min(1.0, self.trauma_level + 0.15)
    
    def create_recovery_arc(self, trauma_memory: TraumaMemory, 
                          trauma_type: SpecificTraumaType) -> str:
        """Create new recovery arc for trauma memory"""
        arc_id = f"{trauma_type.value}_{len(self.recovery_arcs)}"
        
        arc = RecoveryArc(
            trauma_id=arc_id,
            trauma_type=trauma_type
        )
        
        self.recovery_arcs[arc_id] = arc
        return arc_id
    
    def add_mentor_relationship(self, mentor_agent_id: str) -> None:
        """Add a mentor relationship for therapy bonuses"""
        if mentor_agent_id not in self.mentor_relationships:
            self.mentor_relationships.append(mentor_agent_id)
    
    def update_support_network(self, arc_id: str, supporter_ids: List[str], 
                             support_quality: float) -> None:
        """Update support network for recovery arc"""
        if arc_id in self.recovery_arcs:
            arc = self.recovery_arcs[arc_id]
            arc.supported_by = supporter_ids
            arc.support_strength = max(0.0, min(1.0, support_quality))
    
    def apply_therapy(self, therapy_type: TherapyType, effectiveness: float = 0.5) -> Dict[str, Any]:
        """Backward-compatible therapy method - delegates to enhanced system"""
        return self.apply_enhanced_therapy(
            therapy_type=therapy_type,
            duration_hours=1.0,
            therapist_id=None,
            focus_trauma_id=None,
            relationship_strength=effectiveness
        )
    
    def needs_therapy(self) -> Tuple[bool, List[str]]:
        """Check if the agent needs therapy and why"""
        reasons = []
        needs_therapy = False
        
        # High trauma level
        if self.trauma_level > 0.6:
            needs_therapy = True
            reasons.append("high_trauma_level")
        
        # Multiple unprocessed trauma memories
        unprocessed = [m for m in self.trauma_memories if m.therapy_progress < 0.3]
        if len(unprocessed) >= 2:
            needs_therapy = True
            reasons.append("multiple_unprocessed_traumas")
        
        # Extreme negative emotions
        if self.fear > 0.8 or self.sadness > 0.8 or self.anger > 0.8:
            needs_therapy = True
            reasons.append("extreme_negative_emotions")
        
        # Low emotional stability
        if self.get_emotional_stability() < 0.3:
            needs_therapy = True
            reasons.append("low_emotional_stability")
        
        # Recently triggered traumas
        recent_triggers = [m for m in self.trauma_memories 
                          if m.last_triggered and (datetime.now() - m.last_triggered).days < 7]
        if recent_triggers:
            needs_therapy = True
            reasons.append("recent_trauma_triggers")
        
        return needs_therapy, reasons
    
    def get_dominant_emotion(self) -> tuple[str, float]:
        """Get the currently dominant emotion and its intensity"""
        emotions = {
            'fear': self.fear,
            'anger': self.anger, 
            'sadness': self.sadness,
            'joy': self.joy,
            'trust': self.trust,
            'anticipation': self.anticipation,
            'surprise': self.surprise,
            'disgust': self.disgust
        }
        
        # Find emotion with highest absolute value
        dominant_emotion = max(emotions.items(), key=lambda x: abs(x[1]))
        return dominant_emotion
    
    def get_emotional_stability(self) -> float:
        """
        Calculate emotional stability (0.0 = very unstable, 1.0 = very stable).
        Based on how extreme the emotions are and trauma level.
        """
        emotions = [self.fear, self.anger, self.sadness, self.joy, 
                   self.trust, self.anticipation, self.surprise, self.disgust]
        
        # Calculate volatility (how extreme emotions are)
        volatility = sum(abs(emotion) for emotion in emotions) / len(emotions)
        
        # Factor in trauma level
        trauma_impact = self.trauma_level * 0.5
        
        # Factor in recent trauma triggers
        recent_triggers = sum(1 for m in self.trauma_memories 
                            if m.last_triggered and (datetime.now() - m.last_triggered).days < 3)
        trigger_impact = recent_triggers * 0.1
        
        # Stability is inverse of volatility and trauma
        stability = max(0.0, 1.0 - volatility - trauma_impact - trigger_impact)
        return stability
    
    def get_combat_effectiveness(self) -> float:
        """Calculate combat effectiveness based on emotional state"""
        base_effectiveness = 1.0
        
        # Negative emotions reduce effectiveness
        if self.fear > 0.7:
            base_effectiveness *= (1.0 - self.fear * 0.3)
        
        # High trauma or extreme negative emotions reduce effectiveness  
        stress_level = max(self.fear, self.sadness, self.anger, self.trauma_level)
        if stress_level > 0.8:
            base_effectiveness *= 0.7
            
        # Anger can increase effectiveness slightly
        if self.anger > 0.5:
            base_effectiveness *= 1.1
            
        # Trauma reduces effectiveness significantly
        if self.trauma_level > 0:
            base_effectiveness *= (1.0 - self.trauma_level * 0.4)
            
            # Recent trauma triggers have stronger effect
            recent_triggers = sum(1 for m in self.trauma_memories 
                                if m.last_triggered and (datetime.now() - m.last_triggered).total_seconds() / 3600 < 24)
            if recent_triggers > 0:
                base_effectiveness *= (0.8 ** recent_triggers)
        
        # Trust increases team effectiveness
        if self.trust > 0.5:
            base_effectiveness *= (1.0 + self.trust * 0.1)
            
        return max(0.1, min(1.5, base_effectiveness))
    
    def get_social_effectiveness(self) -> float:
        """
        Calculate how emotions affect social interactions and recruitment.
        """
        # Helpful emotions for social interactions
        helpful = self.trust * 0.4 + self.joy * 0.3 + self.anticipation * 0.2
        
        # Hindering emotions  
        hindering = self.fear * 0.2 + self.anger * 0.3 + self.sadness * 0.3 + self.disgust * 0.2
        
        # High trauma makes social interaction difficult
        trauma_penalty = self.trauma_level * 0.4
        
        effectiveness = max(0.0, min(1.0, 0.5 + helpful - hindering - trauma_penalty))
        return effectiveness
    
    def is_psychologically_stable(self) -> bool:
        """Check if the agent is psychologically stable enough to operate"""
        # Check for extreme emotional states
        emotions = [abs(self.fear), abs(self.anger), abs(self.sadness), 
                   abs(self.joy), abs(self.trust), abs(self.anticipation), 
                   abs(self.surprise), abs(self.disgust)]
        
        max_emotion = max(emotions)
        
        # Unstable if any emotion is too extreme or trauma is too high
        if max_emotion > 0.9 or self.trauma_level > 0.8:
            return False
        
        # Unstable if too many emotions are highly negative
        negative_count = sum(1 for emotion in [self.fear, self.anger, self.sadness, self.disgust] 
                           if emotion > 0.6)
        
        # Check for recent trauma triggers
        recent_triggers = sum(1 for m in self.trauma_memories 
                            if m.last_triggered and (datetime.now() - m.last_triggered).hours < 48)
        
        return negative_count < 3 and recent_triggers < 2
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize emotional state to dictionary"""
        return {
            'fear': self.fear,
            'anger': self.anger,
            'sadness': self.sadness, 
            'joy': self.joy,
            'trust': self.trust,
            'anticipation': self.anticipation,
            'surprise': self.surprise,
            'disgust': self.disgust,
            'trauma_level': self.trauma_level,
            'last_trauma_intensity': self.last_trauma_intensity,
            'trauma_decay_rate': self.trauma_decay_rate,
            'trauma_memories': [
                {
                    'trauma_type': m.trauma_type,
                    'severity': m.severity,
                    'occurred_date': m.occurred_date.isoformat(),
                    'triggers': [t.value for t in m.triggers],
                    'description': m.description,
                    'times_triggered': m.times_triggered,
                    'last_triggered': m.last_triggered.isoformat() if m.last_triggered else None,
                    'therapy_progress': m.therapy_progress
                }
                for m in self.trauma_memories
            ],
            'therapy_history': [
                (dt.isoformat(), tt.value, eff) for dt, tt, eff in self.therapy_history
            ],
            'rest_days': self.rest_days,
            'last_rest_date': self.last_rest_date.isoformat() if self.last_rest_date else None,
            'recovery_arcs': {
                k: {
                    'trauma_id': arc.trauma_id,
                    'trauma_type': arc.trauma_type.value,
                    'current_stage': arc.current_stage.value,
                    'sessions_completed': arc.sessions_completed,
                    'total_progress': arc.total_progress,
                    'relapse_risk': arc.relapse_risk,
                    'last_session': arc.last_session.isoformat() if arc.last_session else None,
                    'therapy_sessions': [
                        {
                            'session_date': session.session_date.isoformat(),
                            'therapy_type': session.therapy_type.value,
                            'duration_hours': session.duration_hours,
                            'therapist_id': session.therapist_id,
                            'focus_trauma': session.focus_trauma,
                            'effectiveness': session.effectiveness,
                            'breakthrough': session.breakthrough,
                            'setback': session.setback
                        }
                        for session in arc.therapy_sessions
                    ],
                    'supported_by': arc.supported_by,
                    'mentor_id': arc.mentor_id,
                    'support_strength': arc.support_strength
                }
                for k, arc in self.recovery_arcs.items()
            },
            'therapy_sessions': [
                {
                    'session_date': session.session_date.isoformat(),
                    'therapy_type': session.therapy_type.value,
                    'duration_hours': session.duration_hours,
                    'therapist_id': session.therapist_id,
                    'focus_trauma': session.focus_trauma,
                    'effectiveness': session.effectiveness,
                    'breakthrough': session.breakthrough,
                    'setback': session.setback
                }
                for session in self.therapy_sessions
            ],
            'mentor_relationships': self.mentor_relationships,
            'therapy_resistance': self.therapy_resistance,
            'last_relapse': self.last_relapse.isoformat() if self.last_relapse else None
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'EmotionalState':
        """Deserialize emotional state from dictionary"""
        state = cls(
            fear=data['fear'],
            anger=data['anger'],
            sadness=data['sadness'],
            joy=data['joy'],
            trust=data['trust'],
            anticipation=data['anticipation'],
            surprise=data['surprise'],
            disgust=data['disgust'],
            trauma_level=data['trauma_level'],
            last_trauma_intensity=data['last_trauma_intensity'],
            trauma_decay_rate=data['trauma_decay_rate']
        )
        
        # Deserialize trauma memories
        if 'trauma_memories' in data:
            for m_data in data['trauma_memories']:
                memory = TraumaMemory(
                    trauma_type=m_data['trauma_type'],
                    severity=m_data['severity'],
                    occurred_date=datetime.fromisoformat(m_data['occurred_date']),
                    triggers=[TraumaTriggerType(t) for t in m_data['triggers']],
                    description=m_data['description'],
                    times_triggered=m_data['times_triggered'],
                    last_triggered=datetime.fromisoformat(m_data['last_triggered']) if m_data['last_triggered'] else None,
                    therapy_progress=m_data['therapy_progress']
                )
                state.trauma_memories.append(memory)
        
        # Deserialize therapy history
        if 'therapy_history' in data:
            for dt_str, tt_str, eff in data['therapy_history']:
                state.therapy_history.append((
                    datetime.fromisoformat(dt_str),
                    TherapyType(tt_str),
                    eff
                ))
        
        # Deserialize rest data
        state.rest_days = data.get('rest_days', 0)
        if data.get('last_rest_date'):
            state.last_rest_date = datetime.fromisoformat(data['last_rest_date'])
        
        # Deserialize recovery arcs
        if 'recovery_arcs' in data:
            for arc_id, arc_data in data['recovery_arcs'].items():
                arc = RecoveryArc(
                    trauma_id=arc_data['trauma_id'],
                    trauma_type=SpecificTraumaType(arc_data['trauma_type']),
                    current_stage=TherapyStage(arc_data['current_stage']),
                    sessions_completed=arc_data['sessions_completed'],
                    total_progress=arc_data['total_progress'],
                    relapse_risk=arc_data['relapse_risk'],
                    last_session=datetime.fromisoformat(arc_data['last_session']) if arc_data['last_session'] else None
                )
                state.recovery_arcs[arc_id] = arc
                
                # Deserialize therapy sessions
                for session_data in arc_data['therapy_sessions']:
                    session = TherapySession(
                        session_date=datetime.fromisoformat(session_data['session_date']),
                        therapy_type=TherapyType(session_data['therapy_type']),
                        duration_hours=session_data['duration_hours'],
                        therapist_id=session_data['therapist_id'],
                        focus_trauma=session_data['focus_trauma'],
                        effectiveness=session_data['effectiveness'],
                        breakthrough=session_data['breakthrough'],
                        setback=session_data['setback']
                    )
                    arc.therapy_sessions.append(session)
                
                # Deserialize supported_by
                arc.supported_by = arc_data['supported_by']
                
                # Deserialize mentor_id
                arc.mentor_id = arc_data['mentor_id']
                
                # Deserialize support_strength
                arc.support_strength = arc_data['support_strength']
        
        # Deserialize therapy sessions
        if 'therapy_sessions' in data:
            for session_data in data['therapy_sessions']:
                session = TherapySession(
                    session_date=datetime.fromisoformat(session_data['session_date']),
                    therapy_type=TherapyType(session_data['therapy_type']),
                    duration_hours=session_data['duration_hours'],
                    therapist_id=session_data['therapist_id'],
                    focus_trauma=session_data['focus_trauma'],
                    effectiveness=session_data['effectiveness'],
                    breakthrough=session_data['breakthrough'],
                    setback=session_data['setback']
                )
                state.therapy_sessions.append(session)
        
        # Deserialize mentor relationships
        if 'mentor_relationships' in data:
            state.mentor_relationships = data['mentor_relationships']
        
        # Deserialize therapy resistance
        state.therapy_resistance = data['therapy_resistance']
        
        # Deserialize last relapse
        if data.get('last_relapse'):
            state.last_relapse = datetime.fromisoformat(data['last_relapse'])
        
        return state
    
    def __str__(self) -> str:
        """String representation of emotional state"""
        dominant, intensity = self.get_dominant_emotion()
        stability = self.get_emotional_stability()
        needs_help, reasons = self.needs_therapy()
        
        status = f"EmotionalState(dominant={dominant}:{intensity:.2f}, "
        status += f"stability={stability:.2f}, trauma={self.trauma_level:.2f}"
        
        if needs_help:
            status += f", needs_therapy={','.join(reasons)}"
        
        return status + ")"


def create_random_emotional_state(trauma_range: tuple[float, float] = (0.0, 0.3)) -> EmotionalState:
    """
    Create a random emotional state within reasonable bounds.
    Useful for generating initial agent states.
    """
    state = EmotionalState()
    
    # Generate random but balanced emotions
    emotions = ['fear', 'anger', 'sadness', 'joy', 'trust', 'anticipation', 'surprise', 'disgust']
    
    for emotion in emotions:
        # Most emotions start near neutral with some variation
        value = random.gauss(0.0, 0.3)
        setattr(state, emotion, value)
    
    # Set random trauma level within specified range
    min_trauma, max_trauma = trauma_range
    state.trauma_level = random.uniform(min_trauma, max_trauma)
    
    # Maybe add some trauma memories
    if state.trauma_level > 0.2 and random.random() < 0.5:
        # Create a random past trauma
        trauma_types = ["violence_witnessed", "betrayal", "loss_of_comrade", "imprisonment"]
        trauma_type = random.choice(trauma_types)
        
        # Determine triggers based on trauma type
        trigger_map = {
            "violence_witnessed": [TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES],
            "betrayal": [TraumaTriggerType.BETRAYAL],
            "loss_of_comrade": [TraumaTriggerType.ABANDONMENT],
            "imprisonment": [TraumaTriggerType.CONFINEMENT, TraumaTriggerType.AUTHORITY_FIGURES]
        }
        
        memory = TraumaMemory(
            trauma_type=trauma_type,
            severity=random.uniform(0.3, 0.8),
            occurred_date=datetime.now() - timedelta(days=random.randint(30, 365)),
            triggers=trigger_map.get(trauma_type, []),
            description=f"Past {trauma_type} experience"
        )
        state.trauma_memories.append(memory)
    
    state._clamp_values()
    return state 