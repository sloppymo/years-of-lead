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


class TherapyType(Enum):
    """Types of therapy or rest available to agents"""
    REST = "rest"                          # Basic rest and recovery
    PEER_SUPPORT = "peer_support"          # Support from fellow agents
    PROFESSIONAL = "professional"          # Professional therapy (if available)
    MEDITATION = "meditation"              # Self-directed mindfulness
    PHYSICAL_ACTIVITY = "physical_activity" # Exercise and physical outlets
    CREATIVE_EXPRESSION = "creative_expression" # Art, writing, music
    SUBSTANCE_USE = "substance_use"        # Self-medication (risky)


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
    
    def apply_therapy(self, therapy_type: TherapyType, effectiveness: float = 0.5) -> Dict[str, Any]:
        """Apply therapy or rest to reduce trauma and improve emotional state"""
        results = {
            'therapy_type': therapy_type.value,
            'effectiveness': effectiveness,
            'trauma_reduced': 0.0,
            'emotions_improved': {},
            'side_effects': []
        }
        
        # Base effectiveness modified by therapy type
        if therapy_type == TherapyType.REST:
            # Basic rest helps but is limited
            trauma_reduction = effectiveness * 0.1
            emotional_improvement = 0.05
            self.rest_days += 1
            self.last_rest_date = datetime.now()
            
        elif therapy_type == TherapyType.PEER_SUPPORT:
            # Peer support is moderately effective
            trauma_reduction = effectiveness * 0.15
            emotional_improvement = 0.1
            results['emotions_improved']['trust'] = 0.1
            
        elif therapy_type == TherapyType.PROFESSIONAL:
            # Professional therapy is most effective
            trauma_reduction = effectiveness * 0.25
            emotional_improvement = 0.15
            # Process trauma memories
            for memory in self.trauma_memories:
                memory.apply_therapy(effectiveness * 0.2)
                
        elif therapy_type == TherapyType.MEDITATION:
            # Meditation helps with emotional regulation
            trauma_reduction = effectiveness * 0.12
            emotional_improvement = 0.08
            results['emotions_improved']['anticipation'] = 0.05
            
        elif therapy_type == TherapyType.PHYSICAL_ACTIVITY:
            # Exercise helps with anger and stress
            trauma_reduction = effectiveness * 0.1
            emotional_improvement = 0.07
            results['emotions_improved']['anger'] = -0.15
            
        elif therapy_type == TherapyType.CREATIVE_EXPRESSION:
            # Creative outlets help process emotions
            trauma_reduction = effectiveness * 0.13
            emotional_improvement = 0.09
            results['emotions_improved']['sadness'] = -0.1
            
        elif therapy_type == TherapyType.SUBSTANCE_USE:
            # Substance use provides temporary relief but has risks
            trauma_reduction = effectiveness * 0.05  # Very limited real help
            emotional_improvement = 0.15  # Temporary mood boost
            # Side effects
            if random.random() < 0.3:
                results['side_effects'].append("dependency_risk")
                self.trauma_level += 0.05  # Can worsen trauma long-term
            results['emotions_improved']['fear'] = -0.2  # Temporary fear reduction
            results['emotions_improved']['trust'] = -0.05  # Impairs judgment
        
        # Apply trauma reduction
        old_trauma = self.trauma_level
        self.trauma_level = max(0.0, self.trauma_level - trauma_reduction)
        results['trauma_reduced'] = old_trauma - self.trauma_level
        
        # Apply general emotional improvements
        if emotional_improvement > 0:
            positive_impact = {
                'joy': emotional_improvement,
                'trust': emotional_improvement * 0.5,
                'fear': -emotional_improvement * 0.7,
                'sadness': -emotional_improvement * 0.6
            }
            self.apply_emotional_impact(positive_impact)
        
        # Apply specific emotional improvements
        for emotion, change in results['emotions_improved'].items():
            if hasattr(self, emotion):
                current = getattr(self, emotion)
                setattr(self, emotion, max(-1.0, min(1.0, current + change)))
        
        # Record therapy history
        self.therapy_history.append((datetime.now(), therapy_type, effectiveness))
        
        self._clamp_values()
        return results
    
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
        
        if self.stress > 0.8:
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
            'last_rest_date': self.last_rest_date.isoformat() if self.last_rest_date else None
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