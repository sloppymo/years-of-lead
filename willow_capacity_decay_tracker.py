#!/usr/bin/env python3
"""
Willow Capacity Index Decay Tracker
Monitors cognitive capacity degradation across interactions
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import math


@dataclass
class CapacitySnapshot:
    """Single point-in-time capacity measurement"""
    timestamp: datetime
    raw_capacity: float  # 0-10 scale
    arousal_level: float
    message_coherence: float  # 0-1 scale
    response_latency: float  # seconds
    interaction_type: str  # tier_1, tier_2, edge_case
    

@dataclass
class CapacityProfile:
    """Tracks capacity trends for a user"""
    user_id: str
    baseline_capacity: float = 5.0
    current_capacity: float = 5.0
    capacity_history: deque = field(default_factory=lambda: deque(maxlen=50))
    decay_events: List[Dict] = field(default_factory=list)
    dissociation_markers: List[Dict] = field(default_factory=list)
    exhaustion_threshold_crossed: bool = False
    

class CapacityDecayAnalyzer:
    """Analyzes capacity patterns to detect exhaustion and dissociation"""
    
    DECAY_INDICATORS = {
        "rapid_decline": {"threshold": -2.0, "window": 300},  # 2 point drop in 5 min
        "sustained_low": {"threshold": 3.0, "duration": 600},  # Below 3 for 10 min
        "volatility": {"variance": 2.0, "window": 300},  # High variance
        "dissociation": {"coherence_drop": 0.3, "latency_spike": 2.0}
    }
    
    EXHAUSTION_SIGNALS = {
        "linguistic": ["tired", "can't think", "too much", "overwhelmed", "done"],
        "pattern": ["single_word_responses", "increasing_latency", "coherence_decline"],
        "behavioral": ["help_rejection", "tier_2_avoidance", "communication_breakdown"]
    }
    
    def __init__(self):
        self.profiles: Dict[str, CapacityProfile] = {}
        
    def track_interaction(self, user_id: str, interaction_data: Dict) -> Dict:
        """Track capacity for a single interaction"""
        
        # Get or create profile
        if user_id not in self.profiles:
            self.profiles[user_id] = CapacityProfile(user_id=user_id)
        
        profile = self.profiles[user_id]
        
        # Create capacity snapshot
        snapshot = CapacitySnapshot(
            timestamp=datetime.now(),
            raw_capacity=interaction_data.get("capacity", 5.0),
            arousal_level=interaction_data.get("arousal", 5.0),
            message_coherence=self._calculate_coherence(interaction_data.get("message", "")),
            response_latency=interaction_data.get("response_time", 0),
            interaction_type=interaction_data.get("tier", "unknown")
        )
        
        # Add to history
        profile.capacity_history.append(snapshot)
        
        # Analyze for decay patterns
        decay_analysis = self._analyze_decay_patterns(profile)
        
        # Check for dissociation
        dissociation_risk = self._detect_dissociation(profile, interaction_data)
        
        # Update current capacity with decay factor
        profile.current_capacity = self._calculate_adjusted_capacity(profile)
        
        return {
            "current_capacity": profile.current_capacity,
            "decay_detected": decay_analysis["decay_detected"],
            "decay_type": decay_analysis.get("type"),
            "dissociation_risk": dissociation_risk,
            "exhaustion_level": self._calculate_exhaustion_level(profile),
            "recommendations": self._generate_recommendations(profile, decay_analysis)
        }
    
    def _calculate_coherence(self, message: str) -> float:
        """Calculate message coherence (simplified)"""
        if not message:
            return 0.0
            
        # Simple heuristics
        words = message.split()
        
        # Factors that indicate coherence
        coherence_score = 1.0
        
        # Very short messages
        if len(words) < 3:
            coherence_score *= 0.7
            
        # All caps
        if message.isupper() and len(message) > 5:
            coherence_score *= 0.8
            
        # Repetition
        if len(set(words)) < len(words) * 0.7:
            coherence_score *= 0.8
            
        # Sentence structure
        if not any(punct in message for punct in ['.', '!', '?']):
            coherence_score *= 0.9
            
        return max(0.0, min(1.0, coherence_score))
    
    def _analyze_decay_patterns(self, profile: CapacityProfile) -> Dict:
        """Detect capacity decay patterns"""
        
        if len(profile.capacity_history) < 3:
            return {"decay_detected": False}
        
        recent_history = list(profile.capacity_history)[-10:]
        
        # Check rapid decline
        if len(recent_history) >= 2:
            recent_drop = recent_history[-1].raw_capacity - recent_history[-2].raw_capacity
            if recent_drop <= self.DECAY_INDICATORS["rapid_decline"]["threshold"]:
                return {
                    "decay_detected": True,
                    "type": "rapid_decline",
                    "severity": abs(recent_drop)
                }
        
        # Check sustained low capacity
        recent_capacities = [s.raw_capacity for s in recent_history[-5:]]
        if all(c < self.DECAY_INDICATORS["sustained_low"]["threshold"] for c in recent_capacities):
            return {
                "decay_detected": True,
                "type": "sustained_low",
                "duration": (recent_history[-1].timestamp - recent_history[-5].timestamp).seconds
            }
        
        # Check volatility
        if len(recent_capacities) >= 3:
            variance = sum((c - sum(recent_capacities)/len(recent_capacities))**2 for c in recent_capacities) / len(recent_capacities)
            if variance > self.DECAY_INDICATORS["volatility"]["variance"]:
                return {
                    "decay_detected": True,
                    "type": "high_volatility",
                    "variance": variance
                }
        
        return {"decay_detected": False}
    
    def _detect_dissociation(self, profile: CapacityProfile, interaction_data: Dict) -> float:
        """Detect dissociation markers"""
        
        risk_score = 0.0
        message = interaction_data.get("message", "").lower()
        
        # Linguistic markers
        dissociation_phrases = [
            "floating", "not real", "watching myself", "far away",
            "can't feel", "numb", "detached", "outside looking in"
        ]
        
        if any(phrase in message for phrase in dissociation_phrases):
            risk_score += 0.4
            
        # Third person self-reference
        if any(word in message for word in ["she", "he", "they"]) and "i" not in message:
            risk_score += 0.3
            
        # Coherence drop
        if len(profile.capacity_history) >= 2:
            coherence_drop = profile.capacity_history[-2].message_coherence - profile.capacity_history[-1].message_coherence
            if coherence_drop > self.DECAY_INDICATORS["dissociation"]["coherence_drop"]:
                risk_score += 0.3
        
        # Response latency spike
        if profile.capacity_history:
            avg_latency = sum(s.response_latency for s in list(profile.capacity_history)[-5:-1]) / 4 if len(profile.capacity_history) > 1 else 0
            current_latency = profile.capacity_history[-1].response_latency
            if avg_latency > 0 and current_latency > avg_latency * self.DECAY_INDICATORS["dissociation"]["latency_spike"]:
                risk_score += 0.2
        
        # Record if significant
        if risk_score > 0.5:
            profile.dissociation_markers.append({
                "timestamp": datetime.now(),
                "risk_score": risk_score,
                "markers": interaction_data
            })
        
        return min(1.0, risk_score)
    
    def _calculate_adjusted_capacity(self, profile: CapacityProfile) -> float:
        """Calculate capacity with decay factors applied"""
        
        if not profile.capacity_history:
            return profile.baseline_capacity
        
        current_raw = profile.capacity_history[-1].raw_capacity
        
        # Apply time-based decay
        time_factor = 1.0
        if len(profile.capacity_history) >= 2:
            time_diff = (profile.capacity_history[-1].timestamp - profile.capacity_history[-2].timestamp).seconds
            if time_diff > 300:  # 5 minutes
                time_factor = 0.9  # Slight recovery
            elif time_diff < 30:  # Rapid interactions
                time_factor = 0.95  # Slight decay
        
        # Apply arousal penalty
        arousal_factor = 1.0
        current_arousal = profile.capacity_history[-1].arousal_level
        if current_arousal > 8:
            arousal_factor = 0.8
        elif current_arousal > 6:
            arousal_factor = 0.9
        
        # Apply exhaustion factor
        exhaustion_factor = 1.0
        if profile.exhaustion_threshold_crossed:
            exhaustion_factor = 0.7
        
        adjusted = current_raw * time_factor * arousal_factor * exhaustion_factor
        
        return max(0.1, min(10.0, adjusted))
    
    def _calculate_exhaustion_level(self, profile: CapacityProfile) -> str:
        """Determine exhaustion level"""
        
        if profile.current_capacity < 2:
            return "severe"
        elif profile.current_capacity < 3.5:
            return "moderate"
        elif profile.current_capacity < 5:
            return "mild"
        return "none"
    
    def _generate_recommendations(self, profile: CapacityProfile, decay_analysis: Dict) -> List[str]:
        """Generate response recommendations based on capacity state"""
        
        recommendations = []
        
        if decay_analysis.get("type") == "rapid_decline":
            recommendations.append("immediate_grounding")
            recommendations.append("simplify_language")
            recommendations.append("offer_pause")
            
        if decay_analysis.get("type") == "sustained_low":
            recommendations.append("suggest_human_support")
            recommendations.append("minimize_choices")
            recommendations.append("use_tier_1_only")
            
        if profile.current_capacity < 3:
            recommendations.append("emergency_simplification")
            recommendations.append("single_step_only")
            recommendations.append("increase_validation")
            
        if profile.dissociation_markers:
            recommendations.append("grounding_priority")
            recommendations.append("present_moment_focus")
            recommendations.append("sensory_anchoring")
            
        return recommendations


class CapacityAwareResponseAdapter:
    """Adapts responses based on capacity analysis"""
    
    def __init__(self, decay_analyzer: CapacityDecayAnalyzer):
        self.analyzer = decay_analyzer
        
    def adapt_response(self, user_id: str, base_response: str, interaction_data: Dict) -> str:
        """Adapt response based on capacity state"""
        
        # Get capacity analysis
        capacity_state = self.analyzer.track_interaction(user_id, interaction_data)
        
        # Apply adaptations based on recommendations
        adapted = base_response
        
        if "emergency_simplification" in capacity_state["recommendations"]:
            # Strip to absolute essentials
            adapted = self._emergency_simplify(adapted)
            
        elif "simplify_language" in capacity_state["recommendations"]:
            # Moderate simplification
            adapted = self._simplify_language(adapted)
            
        if "grounding_priority" in capacity_state["recommendations"]:
            # Add grounding prefix
            adapted = "Feel your feet on the floor. " + adapted
            
        if "offer_pause" in capacity_state["recommendations"]:
            # Add pause option
            adapted += " Reply PAUSE if you need a moment."
            
        return adapted
    
    def _emergency_simplify(self, text: str) -> str:
        """Emergency simplification for severe exhaustion"""
        # In production, this would be more sophisticated
        lines = text.split('\n')
        essential = lines[0] if lines else text
        
        # Keep only first sentence
        if '.' in essential:
            essential = essential.split('.')[0] + '.'
            
        return essential + " I'm here. 💙"
    
    def _simplify_language(self, text: str) -> str:
        """Moderate language simplification"""
        # Simplified version
        replacements = {
            "I understand how": "I hear that",
            "This situation is": "This is",
            "I'm arranging for": "Getting",
            "immediately": "now",
            "assistance": "help"
        }
        
        simplified = text
        for original, simple in replacements.items():
            simplified = simplified.replace(original, simple)
            
        return simplified


# Example usage
def demonstrate_capacity_decay():
    analyzer = CapacityDecayAnalyzer()
    adapter = CapacityAwareResponseAdapter(analyzer)
    
    # Simulate declining capacity
    interactions = [
        {"message": "My ceiling collapsed and water everywhere!", "capacity": 8, "arousal": 9, "response_time": 2},
        {"message": "I don't know what to do", "capacity": 6, "arousal": 8.5, "response_time": 5},
        {"message": "too much", "capacity": 4, "arousal": 8, "response_time": 12},
        {"message": "can't", "capacity": 2, "arousal": 7.5, "response_time": 20},
        {"message": "...", "capacity": 1, "arousal": 7, "response_time": 45}
    ]
    
    base_response = "I understand this is overwhelming. When you're ready:\n1. Text HELP for immediate support\n2. Reply SAFE if you're in a secure location\n3. Text BREATHE for grounding exercises"
    
    for i, interaction in enumerate(interactions):
        print(f"\n--- Interaction {i+1} ---")
        print(f"User: {interaction['message']}")
        
        # Adapt response based on capacity
        adapted = adapter.adapt_response("user_123", base_response, interaction)
        
        # Get current state
        profile = analyzer.profiles["user_123"]
        
        print(f"Capacity: {profile.current_capacity:.1f}")
        print(f"Response: {adapted}")


if __name__ == "__main__":
    demonstrate_capacity_decay()