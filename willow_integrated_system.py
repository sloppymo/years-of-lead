#!/usr/bin/env python3
"""
Willow Integrated System
Combines all four critical enhancements into a unified crisis support system
"""

from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

# Import all components
from willow_unified_symbolic_system import UnifiedSymbolicAnchor, SymbolicContext, SymbolicEdgeCaseResolver
from willow_tier_flow_control import GlobalTierFlowController, TierGatedResponseGenerator, TierState
from willow_capacity_decay_tracker import CapacityDecayAnalyzer, CapacityAwareResponseAdapter
from willow_bilingual_routing import BilingualCrisisDetector, BilingualResponseRouter


@dataclass
class UserSession:
    """Maintains complete user session state"""
    user_id: str
    start_time: datetime
    symbolic_context: Optional[SymbolicContext]
    tier_state: TierState
    capacity_profile: Dict
    language_profile: Dict
    interaction_count: int = 0
    escalation_triggered: bool = False


class WillowIntegratedCore:
    """Master orchestrator for all Willow subsystems"""
    
    def __init__(self, config: Dict):
        # Initialize all subsystems
        self.symbolic_anchor = None  # Initialized per user
        self.tier_controller = GlobalTierFlowController()
        self.tier_generator = TierGatedResponseGenerator(self.tier_controller)
        self.capacity_analyzer = CapacityDecayAnalyzer()
        self.capacity_adapter = CapacityAwareResponseAdapter(self.capacity_analyzer)
        self.bilingual_detector = BilingualCrisisDetector()
        self.bilingual_router = BilingualResponseRouter(self.bilingual_detector)
        
        # Session management
        self.active_sessions: Dict[str, UserSession] = {}
        
        # Configuration
        self.config = config
        
    def process_message(self, user_id: str, message: str, 
                       emotional_state: Dict, context: Optional[Dict] = None) -> Dict:
        """Process a user message through all subsystems"""
        
        # Get or create session
        session = self._get_or_create_session(user_id, context)
        session.interaction_count += 1
        
        # Step 1: Bilingual crisis detection
        bilingual_result = self.bilingual_router.process_interaction(
            user_id, message, emotional_state, ""  # Base response filled later
        )
        
        # Check for immediate human routing
        if bilingual_result["action"] == "route_to_human":
            session.escalation_triggered = True
            return {
                "response": bilingual_result["response"],
                "action": "escalate_to_human",
                "specialist": bilingual_result["specialist"],
                "urgency": bilingual_result["urgency"],
                "reason": f"bilingual_crisis: {bilingual_result['reason']}",
                "session_metrics": self._get_session_metrics(session)
            }
        
        # Step 2: Capacity decay analysis
        interaction_data = {
            "message": message,
            "capacity": emotional_state.get("capacity", 5),
            "arousal": emotional_state.get("arousal", 5),
            "response_time": context.get("response_time", 5) if context else 5,
            "tier": "unknown"  # Will be updated
        }
        
        capacity_state = self.capacity_analyzer.track_interaction(user_id, interaction_data)
        
        # Check for capacity-based escalation
        if capacity_state["exhaustion_level"] == "severe":
            session.escalation_triggered = True
            return {
                "response": "I notice you're exhausted. Let me connect you with someone who can help directly. 💙",
                "action": "escalate_to_human",
                "specialist": "crisis_support",
                "urgency": "high",
                "reason": "severe_exhaustion",
                "session_metrics": self._get_session_metrics(session)
            }
        
        # Step 3: Tier flow control
        tier_response = self.tier_generator.generate_response(
            user_id, message, emotional_state
        )
        
        # Update interaction data with tier
        interaction_data["tier"] = tier_response["tier"]
        
        # Check for tier-based escalation
        if tier_response["tier"] == "escalation":
            session.escalation_triggered = True
            return {
                "response": tier_response["response"],
                "action": "escalate_to_human",
                "specialist": "crisis_support",
                "urgency": "immediate",
                "reason": tier_response["rationale"],
                "session_metrics": self._get_session_metrics(session)
            }
        
        # Step 4: Apply capacity adaptations
        adapted_response = self.capacity_adapter.adapt_response(
            user_id, tier_response["response"], interaction_data
        )
        
        # Step 5: Apply symbolic continuity
        if not session.symbolic_context:
            session.symbolic_context = SymbolicContext(
                user_id=user_id,
                preferred_style=context.get("symbol_preference", "traditional") if context else "traditional"
            )
            self.symbolic_anchor = UnifiedSymbolicAnchor(session.symbolic_context)
        
        # Ensure symbolic anchor exists
        if not self.symbolic_anchor:
            self.symbolic_anchor = UnifiedSymbolicAnchor(session.symbolic_context)
            
        final_response = self.symbolic_anchor.wrap_response(
            adapted_response,
            tier_response["tier"],
            emotional_state
        )
        
        # Step 6: Handle edge cases with symbolic continuity
        edge_result = self._check_edge_cases(session, message, emotional_state)
        if edge_result and self.symbolic_anchor:
            edge_resolver = SymbolicEdgeCaseResolver(self.symbolic_anchor)
            edge_response = edge_resolver.handle(edge_result["type"], emotional_state)
            if edge_response:
                final_response = edge_response
        
        # Step 7: Apply language acknowledgment if needed
        if bilingual_result["language_analysis"]["primary_language"] != "en":
            final_response = self.bilingual_router._add_language_acknowledgment(
                final_response,
                bilingual_result["language_analysis"]["primary_language"]
            )
        
        return {
            "response": final_response,
            "action": "continue",
            "tier": tier_response["tier"],
            "session_metrics": self._get_session_metrics(session),
            "subsystem_states": {
                "capacity": capacity_state,
                "language": bilingual_result["language_analysis"],
                "tier": tier_response["metrics"],
                "symbolic": {
                    "current_symbol": session.symbolic_context.last_symbol if session.symbolic_context else "",
                    "style": session.symbolic_context.preferred_style if session.symbolic_context else "traditional"
                }
            }
        }
    
    def _get_or_create_session(self, user_id: str, context: Optional[Dict] = None) -> UserSession:
        """Get existing session or create new one"""
        if user_id not in self.active_sessions:
            self.active_sessions[user_id] = UserSession(
                user_id=user_id,
                start_time=datetime.now(),
                symbolic_context=None,  # Created when needed
                tier_state=TierState.INITIAL,
                capacity_profile={},
                language_profile={}
            )
        return self.active_sessions[user_id]
    
    def _check_edge_cases(self, session: UserSession, message: str, 
                         emotional_state: Dict) -> Optional[Dict]:
        """Check for edge case patterns"""
        
        # Rapid fire detection
        if session.interaction_count > 5:
            recent_time = (datetime.now() - session.start_time).seconds
            if recent_time < 60:  # 5+ messages in 60 seconds
                return {"type": "rapid_fire"}
        
        # Contradiction detection
        # (Would need message history tracking in production)
        
        # Dissociation markers
        if "floating" in message.lower() or "watching myself" in message.lower():
            return {"type": "dissociation"}
            
        return None
    
    def _get_session_metrics(self, session: UserSession) -> Dict:
        """Get comprehensive session metrics"""
        duration = (datetime.now() - session.start_time).seconds
        
        return {
            "session_duration": duration,
            "interaction_count": session.interaction_count,
            "escalation_triggered": session.escalation_triggered,
            "average_response_time": duration / session.interaction_count if session.interaction_count > 0 else 0
        }
    
    def end_session(self, user_id: str) -> Dict:
        """End a user session and return final metrics"""
        if user_id not in self.active_sessions:
            return {"error": "No active session"}
            
        session = self.active_sessions[user_id]
        final_metrics = {
            "session_summary": self._get_session_metrics(session),
            "capacity_profile": self.capacity_analyzer.profiles.get(user_id),
            "language_profile": self.bilingual_detector.user_profiles.get(user_id),
            "tier_progression": self.tier_controller.user_states.get(user_id)
        }
        
        # Clean up
        del self.active_sessions[user_id]
        
        return final_metrics


# Example usage demonstrating full integration
def demonstrate_integrated_system():
    """Show how all systems work together in a crisis"""
    
    # Initialize with configuration
    config = {
        "symbol_preference": "nature",
        "resolution_style": "strength-based",
        "escalation_thresholds": {
            "capacity": 2.0,
            "arousal": 9.5,
            "language_switch_count": 3
        }
    }
    
    willow = WillowIntegratedCore(config)
    
    # Simulate a deteriorating crisis with language switching
    interactions = [
        # Initial contact - English, high arousal
        {
            "message": "My apartment is flooding! Water everywhere!",
            "emotional_state": {"arousal": 9, "capacity": 6, "urgency": 10},
            "context": {"response_time": 2, "symbol_preference": "nature"}
        },
        # Tier 1 response received, still distressed
        {
            "message": "I don't know what to do, everything is getting ruined",
            "emotional_state": {"arousal": 8.5, "capacity": 5, "urgency": 9},
            "context": {"response_time": 5}
        },
        # Language switching begins
        {
            "message": "Por favor, my kids are crying, no sé qué hacer!",
            "emotional_state": {"arousal": 9, "capacity": 4, "urgency": 10},
            "context": {"response_time": 8}
        },
        # Capacity declining rapidly
        {
            "message": "too much... can't...",
            "emotional_state": {"arousal": 8, "capacity": 2, "urgency": 8},
            "context": {"response_time": 15}
        },
        # Full bilingual crisis
        {
            "message": "AYUDA!! Todo está destroyed!! HELP!!",
            "emotional_state": {"arousal": 9.5, "capacity": 1.5, "urgency": 10},
            "context": {"response_time": 20}
        }
    ]
    
    print("=== WILLOW INTEGRATED SYSTEM DEMONSTRATION ===\n")
    
    for i, interaction in enumerate(interactions):
        print(f"--- Interaction {i+1} ---")
        print(f"User: {interaction['message']}")
        print(f"Emotional State: Arousal={interaction['emotional_state']['arousal']}, "
              f"Capacity={interaction['emotional_state']['capacity']}")
        
        result = willow.process_message(
            "user_123",
            interaction["message"],
            interaction["emotional_state"],
            interaction.get("context")
        )
        
        print(f"\nWillow Response: {result['response']}")
        print(f"Action: {result['action']}")
        
        if result["action"] == "escalate_to_human":
            print(f"ESCALATION: {result['urgency']} priority to {result['specialist']}")
            print(f"Reason: {result['reason']}")
            break
        else:
            print(f"Tier: {result['tier']}")
            
            # Show subsystem states
            if "subsystem_states" in result:
                states = result["subsystem_states"]
                print(f"\nSubsystem Status:")
                print(f"  - Capacity: {states['capacity']['exhaustion_level']} exhaustion, "
                      f"current={states['capacity']['current_capacity']:.1f}")
                print(f"  - Language: {states['language']['primary_language']}, "
                      f"code_switch={states['language']['is_code_switch']}")
                print(f"  - Symbol: {states['symbolic']['style']} style")
        
        print()
    
    # End session and show final metrics
    print("\n=== SESSION SUMMARY ===")
    final_metrics = willow.end_session("user_123")
    print(f"Total Duration: {final_metrics['session_summary']['session_duration']} seconds")
    print(f"Total Interactions: {final_metrics['session_summary']['interaction_count']}")
    print(f"Escalation Triggered: {final_metrics['session_summary']['escalation_triggered']}")


if __name__ == "__main__":
    demonstrate_integrated_system()