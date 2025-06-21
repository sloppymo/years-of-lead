#!/usr/bin/env python3
"""
Willow Global Tier Flow Control
Ensures proper therapeutic progression through response tiers
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class TierState(Enum):
    """Current tier state of interaction"""
    INITIAL = "initial"
    TIER_1_ACTIVE = "tier_1_active"
    TIER_1_COMPLETE = "tier_1_complete"
    TIER_1_5_BRIDGE = "tier_1_5_bridge"
    TIER_2_READY = "tier_2_ready"
    TIER_2_ACTIVE = "tier_2_active"
    RESOLUTION = "resolution"
    ESCALATED = "escalated"


@dataclass
class FlowState:
    """Tracks current position in tier flow"""
    user_id: str
    current_tier: TierState = TierState.INITIAL
    tier_1_count: int = 0
    last_tier_1: Optional[datetime] = None
    consent_received: bool = False
    capacity_score: float = 5.0
    arousal_trend: List[float] = None
    
    def __post_init__(self):
        if self.arousal_trend is None:
            self.arousal_trend = []


class GlobalTierFlowController:
    """Master controller for tier progression"""
    
    TIER_RULES = {
        "tier_1_minimum": 2,  # Minimum tier 1 responses before tier 2
        "tier_1_timeout": 300,  # 5 minutes before tier 1 expires
        "capacity_threshold": 3.0,  # Minimum capacity for tier 2
        "arousal_threshold": 7.0,  # Maximum arousal for tier 2
        "consent_keywords": ["ready", "yes", "help", "options", "what can"]
    }
    
    def __init__(self):
        self.user_states: Dict[str, FlowState] = {}
        
    def determine_tier(self, user_id: str, message: str, emotional_state: Dict) -> Tuple[TierState, str]:
        """Determine appropriate tier for response"""
        
        # Get or create user state
        if user_id not in self.user_states:
            self.user_states[user_id] = FlowState(user_id=user_id)
        
        state = self.user_states[user_id]
        
        # Update emotional tracking
        state.arousal_trend.append(emotional_state.get("arousal", 5))
        state.capacity_score = emotional_state.get("capacity", 5)
        
        # Check for escalation triggers
        if self._requires_escalation(message, emotional_state):
            state.current_tier = TierState.ESCALATED
            return TierState.ESCALATED, "Immediate human support required"
        
        # Determine next tier based on rules
        next_tier, rationale = self._apply_tier_rules(state, message, emotional_state)
        
        # Update state
        state.current_tier = next_tier
        if next_tier == TierState.TIER_1_ACTIVE:
            state.tier_1_count += 1
            state.last_tier_1 = datetime.now()
        
        return next_tier, rationale
    
    def _requires_escalation(self, message: str, emotional_state: Dict) -> bool:
        """Check if immediate escalation needed"""
        # High arousal + low capacity + certain keywords
        if emotional_state.get("arousal", 0) > 9.5 and emotional_state.get("capacity", 5) < 2:
            crisis_keywords = ["can't", "help", "emergency", "dying", "hurt"]
            if any(word in message.lower() for word in crisis_keywords):
                return True
        return False
    
    def _apply_tier_rules(self, state: FlowState, message: str, emotional_state: Dict) -> Tuple[TierState, str]:
        """Apply tier progression rules"""
        
        current = state.current_tier
        arousal = emotional_state.get("arousal", 5)
        
        # Initial state -> Always Tier 1
        if current == TierState.INITIAL:
            return TierState.TIER_1_ACTIVE, "Initial contact requires containment"
        
        # Tier 1 Active -> Check if ready for progression
        if current == TierState.TIER_1_ACTIVE:
            # Not enough tier 1 responses yet
            if state.tier_1_count < self.TIER_RULES["tier_1_minimum"]:
                return TierState.TIER_1_ACTIVE, f"Need {self.TIER_RULES['tier_1_minimum'] - state.tier_1_count} more containment responses"
            
            # Check arousal trend
            if len(state.arousal_trend) >= 2:
                arousal_dropping = state.arousal_trend[-1] < state.arousal_trend[-2]
                if arousal_dropping and arousal < self.TIER_RULES["arousal_threshold"]:
                    return TierState.TIER_1_5_BRIDGE, "Arousal reducing, bridge to action"
            
            # Still too activated
            if arousal > self.TIER_RULES["arousal_threshold"]:
                return TierState.TIER_1_ACTIVE, f"Arousal {arousal} too high for tier 2"
            
            return TierState.TIER_1_ACTIVE, "Continue containment"
        
        # Tier 1.5 Bridge -> Check for consent
        if current == TierState.TIER_1_5_BRIDGE:
            # Check for consent signals
            if self._detect_consent(message):
                state.consent_received = True
                return TierState.TIER_2_READY, "Consent received for action"
            
            # Check capacity
            if state.capacity_score < self.TIER_RULES["capacity_threshold"]:
                return TierState.TIER_1_ACTIVE, f"Capacity {state.capacity_score} too low for action"
            
            return TierState.TIER_1_5_BRIDGE, "Awaiting readiness signal"
        
        # Tier 2 Ready -> Deliver action
        if current == TierState.TIER_2_READY:
            return TierState.TIER_2_ACTIVE, "Delivering action options"
        
        # Tier 2 Active -> Monitor for completion
        if current == TierState.TIER_2_ACTIVE:
            if "done" in message.lower() or "thanks" in message.lower():
                return TierState.RESOLUTION, "Moving to resolution"
            return TierState.TIER_2_ACTIVE, "Action in progress"
        
        return current, "Maintaining current tier"
    
    def _detect_consent(self, message: str) -> bool:
        """Detect consent for tier 2 progression"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.TIER_RULES["consent_keywords"])
    
    def get_tier_metrics(self, user_id: str) -> Dict:
        """Get metrics for current interaction"""
        if user_id not in self.user_states:
            return {}
        
        state = self.user_states[user_id]
        return {
            "current_tier": state.current_tier.value,
            "tier_1_count": state.tier_1_count,
            "consent_received": state.consent_received,
            "capacity_score": state.capacity_score,
            "arousal_average": sum(state.arousal_trend) / len(state.arousal_trend) if state.arousal_trend else 0
        }


class TierGatedResponseGenerator:
    """Response generator that enforces tier flow"""
    
    def __init__(self, flow_controller: GlobalTierFlowController):
        self.flow_controller = flow_controller
        self.response_templates = {
            TierState.TIER_1_ACTIVE: [
                "I'm here with you. {validation}. {grounding}",
                "This is {acknowledgment}. Let's {grounding} together",
                "{validation}. Feel {somatic_cue}"
            ],
            TierState.TIER_1_5_BRIDGE: [
                "{acknowledgment}. Help is mobilizing. Would knowing steps help?",
                "I'm arranging support now. When you're ready, we have options",
                "{validation}. Solutions are available when you feel able"
            ],
            TierState.TIER_2_ACTIVE: [
                "When able:\n{action_steps}\n\nOnly what helps right now",
                "Options ready:\n{action_steps}\n\nChoose what works",
                "{action_steps}\n\nNo pressure - your pace"
            ]
        }
    
    def generate_response(self, user_id: str, message: str, emotional_state: Dict) -> Dict:
        """Generate tier-appropriate response"""
        
        # Get appropriate tier
        tier, rationale = self.flow_controller.determine_tier(user_id, message, emotional_state)
        
        # Generate response based on tier
        if tier == TierState.ESCALATED:
            return {
                "tier": "escalation",
                "response": "I'm connecting you with immediate human support. Stay with me.",
                "rationale": rationale
            }
        
        if tier not in self.response_templates:
            tier = TierState.TIER_1_ACTIVE  # Safe default
        
        # Select and populate template
        template = self._select_template(tier)
        response = self._populate_template(template, message, emotional_state)
        
        return {
            "tier": tier.value,
            "response": response,
            "rationale": rationale,
            "metrics": self.flow_controller.get_tier_metrics(user_id)
        }
    
    def _select_template(self, tier: TierState) -> str:
        """Select appropriate template for tier"""
        import random
        return random.choice(self.response_templates.get(tier, []))
    
    def _populate_template(self, template: str, message: str, emotional_state: Dict) -> str:
        """Fill template with appropriate content"""
        # This would be more sophisticated in production
        replacements = {
            "{validation}": "Your frustration is completely valid",
            "{acknowledgment}": "This situation is unacceptable",
            "{grounding}": "breathe through this",
            "{somatic_cue}": "your feet on the floor",
            "{action_steps}": "1. Text HEAT for emergency team\n2. Reply SHELTER for warm space\n3. Text STATUS for updates"
        }
        
        for key, value in replacements.items():
            template = template.replace(key, value)
        
        return template


# Example usage
def demonstrate_tier_flow():
    controller = GlobalTierFlowController()
    generator = TierGatedResponseGenerator(controller)
    
    # Simulate crisis interaction
    interactions = [
        ("My heat is broken and kids are freezing!", {"arousal": 9.5, "capacity": 2}),
        ("I don't know what to do", {"arousal": 9, "capacity": 2.5}),
        ("Okay, breathing", {"arousal": 8, "capacity": 3}),
        ("What can you do to help?", {"arousal": 7, "capacity": 4}),
        ("Yes, I need options", {"arousal": 6.5, "capacity": 4.5})
    ]
    
    for message, state in interactions:
        response = generator.generate_response("user_123", message, state)
        print(f"\nUser: {message}")
        print(f"Tier: {response['tier']} - {response['rationale']}")
        print(f"Response: {response['response']}")
        print(f"Metrics: {response['metrics']}")


if __name__ == "__main__":
    demonstrate_tier_flow()