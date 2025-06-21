#!/usr/bin/env python3
"""
Comprehensive test suite for Willow Integrated Crisis Support System
Tests all four critical integration points
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Import all Willow components
from willow_unified_symbolic_system import UnifiedSymbolicAnchor, SymbolicContext
from willow_tier_flow_control import GlobalTierFlowController, TierState
from willow_capacity_decay_tracker import CapacityDecayAnalyzer
from willow_bilingual_routing import BilingualCrisisDetector
from willow_integrated_system import WillowIntegratedCore


class TestSymbolicContinuity:
    """Test unified symbolic anchors across all response types"""
    
    def test_symbol_persistence_across_tiers(self):
        """Symbols should persist through tier transitions"""
        context = SymbolicContext(user_id="test_user", preferred_style="nature")
        anchor = UnifiedSymbolicAnchor(context)
        
        # Tier 1 response
        tier1_response = anchor.wrap_response(
            "I'm here with you", 
            "tier_1", 
            {"arousal": 9}
        )
        assert "🌊" in tier1_response  # High arousal grounding symbol
        
        # Tier 2 response - should maintain continuity
        tier2_response = anchor.wrap_response(
            "When ready: 1. Call emergency",
            "tier_2",
            {"arousal": 7}
        )
        assert "🌊" in tier2_response or "🌿" in tier2_response
        
    def test_edge_case_symbolic_integration(self):
        """Edge cases should maintain symbolic consistency"""
        context = SymbolicContext(user_id="test_user", preferred_style="traditional")
        anchor = UnifiedSymbolicAnchor(context)
        
        # Rapid fire edge case
        rapid_response = anchor.wrap_response(
            "I see many messages - let's slow down together. Breathe with me",
            "edge_rapid_fire",
            {"arousal": 9}
        )
        assert "💙" in rapid_response
        
    def test_symbol_style_switching(self):
        """Test switching between symbol styles"""
        styles = ["traditional", "nature", "minimal", "none"]
        
        for style in styles:
            context = SymbolicContext(user_id="test_user", preferred_style=style)
            anchor = UnifiedSymbolicAnchor(context)
            
            response = anchor.wrap_response(
                "Test message",
                "tier_1",
                {"arousal": 8}
            )
            
            if style == "none":
                # No symbols should be added
                assert response == "Test message"
            else:
                # Should have some symbol
                assert len(response) > len("Test message")


class TestGlobalTierFlow:
    """Test tier flow control enforcement"""
    
    def test_tier_1_minimum_enforcement(self):
        """Should require minimum Tier 1 responses"""
        controller = GlobalTierFlowController()
        
        # First interaction - should be Tier 1
        tier1, _ = controller.determine_tier(
            "test_user",
            "Emergency!",
            {"arousal": 8, "capacity": 5}
        )
        assert tier1 == TierState.TIER_1_ACTIVE
        
        # Second interaction - still Tier 1 (minimum not met)
        tier2, rationale = controller.determine_tier(
            "test_user",
            "Help me!",
            {"arousal": 7, "capacity": 5}
        )
        assert tier2 == TierState.TIER_1_ACTIVE
        assert "1 more containment" in rationale
        
    def test_arousal_gating(self):
        """High arousal should block Tier 2"""
        controller = GlobalTierFlowController()
        
        # Setup: Meet tier 1 minimum
        for _ in range(3):
            controller.determine_tier(
                "test_user",
                "Message",
                {"arousal": 8.5, "capacity": 5}
            )
        
        # High arousal should block progression
        tier, rationale = controller.determine_tier(
            "test_user",
            "What can you do?",
            {"arousal": 8, "capacity": 5}
        )
        assert tier != TierState.TIER_2_READY
        assert "too high" in rationale
        
    def test_consent_detection(self):
        """Consent keywords should enable Tier 2"""
        controller = GlobalTierFlowController()
        
        # Setup: Get to bridge state
        state = controller.user_states.get("test_user")
        if not state:
            controller.determine_tier("test_user", "Test", {"arousal": 5})
            state = controller.user_states["test_user"]
        
        state.current_tier = TierState.TIER_1_5_BRIDGE
        state.tier_1_count = 3
        
        # Consent message
        tier, _ = controller.determine_tier(
            "test_user",
            "Yes, I'm ready for options",
            {"arousal": 6, "capacity": 4}
        )
        assert tier == TierState.TIER_2_READY
        
    def test_escalation_trigger(self):
        """High arousal + low capacity should trigger escalation"""
        controller = GlobalTierFlowController()
        
        tier, _ = controller.determine_tier(
            "test_user",
            "I can't do this anymore help",
            {"arousal": 9.8, "capacity": 1.5}
        )
        assert tier == TierState.ESCALATED


class TestCapacityDecay:
    """Test capacity decay tracking and adaptation"""
    
    def test_rapid_decline_detection(self):
        """Should detect rapid capacity drops"""
        analyzer = CapacityDecayAnalyzer()
        
        # Initial interaction
        result1 = analyzer.track_interaction("test_user", {
            "capacity": 6,
            "arousal": 7,
            "message": "Help needed",
            "response_time": 3
        })
        
        # Rapid decline
        result2 = analyzer.track_interaction("test_user", {
            "capacity": 3,  # 3 point drop
            "arousal": 8,
            "message": "can't think",
            "response_time": 5
        })
        
        assert result2["decay_detected"]
        assert result2["decay_type"] == "rapid_decline"
        
    def test_dissociation_detection(self):
        """Should detect dissociation markers"""
        analyzer = CapacityDecayAnalyzer()
        
        result = analyzer.track_interaction("test_user", {
            "capacity": 4,
            "arousal": 7,
            "message": "feeling like I'm floating away",
            "response_time": 15
        })
        
        assert result["dissociation_risk"] > 0.3
        
    def test_exhaustion_levels(self):
        """Should correctly categorize exhaustion levels"""
        analyzer = CapacityDecayAnalyzer()
        
        # Severe exhaustion
        result = analyzer.track_interaction("test_user", {
            "capacity": 1.5,
            "arousal": 6,
            "message": "...",
            "response_time": 30
        })
        
        assert result["exhaustion_level"] == "severe"
        assert "emergency_simplification" in result["recommendations"]
        
    def test_language_simplification(self):
        """Should simplify language based on capacity"""
        from willow_capacity_decay_tracker import CapacityAwareResponseAdapter
        
        analyzer = CapacityDecayAnalyzer()
        adapter = CapacityAwareResponseAdapter(analyzer)
        
        # Low capacity interaction
        base_response = "I understand this is overwhelming. When you're ready:\n1. Text HELP\n2. Call emergency"
        
        adapted = adapter.adapt_response("test_user", base_response, {
            "capacity": 1.5,
            "arousal": 7,
            "message": "can't",
            "response_time": 25
        })
        
        # Should be emergency simplified
        assert len(adapted) < len(base_response)
        assert "💙" in adapted


class TestBilingualRouting:
    """Test bilingual crisis detection and routing"""
    
    def test_language_detection(self):
        """Should detect multiple languages"""
        detector = BilingualCrisisDetector()
        
        # Spanish detection
        result = detector.analyze_message(
            "test_user",
            "No puedo más, necesito ayuda",
            {"arousal": 7}
        )
        assert result["primary_language"] == "es"
        
        # Mixed language
        result = detector.analyze_message(
            "test_user",
            "Help me por favor!",
            {"arousal": 8}
        )
        assert "es" in result["detected_languages"]
        assert "en" in result["detected_languages"]
        
    def test_crisis_language_switching(self):
        """Should detect crisis-induced language switching"""
        detector = BilingualCrisisDetector()
        
        # English baseline
        detector.analyze_message(
            "test_user",
            "My apartment is flooding",
            {"arousal": 7}
        )
        
        # Spanish switch under stress
        result = detector.analyze_message(
            "test_user",
            "AYUDA! No sé qué hacer!",
            {"arousal": 9}
        )
        
        assert result["is_code_switch"]
        assert result["crisis_indicators"]["is_crisis"]
        assert result["routing_recommendation"]["route_to_human"]
        
    def test_bilingual_routing_messages(self):
        """Should provide language-appropriate routing messages"""
        from willow_bilingual_routing import BilingualResponseRouter
        
        detector = BilingualCrisisDetector()
        router = BilingualResponseRouter(detector)
        
        result = router.process_interaction(
            "test_user",
            "Socorro! Emergency!",
            {"arousal": 9.5},
            "Base response"
        )
        
        assert result["action"] == "route_to_human"
        assert "español" in result["response"] or "Spanish" in result["specialist"]


class TestIntegratedSystem:
    """Test the complete integrated system"""
    
    @pytest.fixture
    def willow_system(self):
        config = {
            "symbol_preference": "nature",
            "escalation_thresholds": {
                "capacity": 2.0,
                "arousal": 9.5,
                "language_switch_count": 3
            }
        }
        return WillowIntegratedCore(config)
    
    def test_full_crisis_flow(self, willow_system):
        """Test complete crisis interaction flow"""
        # Initial high-stress contact
        result1 = willow_system.process_message(
            "test_user",
            "Flooding everywhere! Help!",
            {"arousal": 9, "capacity": 5}
        )
        
        assert result1["action"] == "continue"
        assert result1["tier"] == "tier_1_active"
        assert "🌊" in result1["response"]  # Nature symbol
        
        # Capacity decline
        result2 = willow_system.process_message(
            "test_user",
            "can't handle this",
            {"arousal": 8, "capacity": 3}
        )
        
        assert result2["action"] == "continue"
        # Should still be Tier 1 (minimum not met)
        
        # Language switch under stress
        result3 = willow_system.process_message(
            "test_user",
            "No puedo más! HELP!",
            {"arousal": 9, "capacity": 2.5}
        )
        
        # Should acknowledge language but continue (not severe enough)
        assert "Spanish" in result3["response"] or "Continue in whatever" in result3["response"]
        
        # Severe exhaustion
        result4 = willow_system.process_message(
            "test_user",
            "...",
            {"arousal": 7, "capacity": 1.5}
        )
        
        # Should escalate due to severe exhaustion
        assert result4["action"] == "escalate_to_human"
        assert "exhaustion" in result4["reason"]
        
    def test_multiple_escalation_paths(self, willow_system):
        """Test that different subsystems can trigger escalation"""
        # Path 1: Capacity-based escalation
        result = willow_system.process_message(
            "user1",
            "can't anymore",
            {"arousal": 6, "capacity": 1}
        )
        assert result["action"] == "escalate_to_human"
        assert "exhaustion" in result["reason"]
        
        # Path 2: Tier-based escalation
        result = willow_system.process_message(
            "user2",
            "I can't breathe help emergency",
            {"arousal": 9.8, "capacity": 1.8}
        )
        assert result["action"] == "escalate_to_human"
        
        # Path 3: Bilingual crisis escalation
        willow_system.process_message(
            "user3",
            "Everything is broken",
            {"arousal": 8, "capacity": 5}
        )
        
        result = willow_system.process_message(
            "user3",
            "AYUDA SOCORRO!!",
            {"arousal": 9.5, "capacity": 4}
        )
        assert result["action"] == "escalate_to_human"
        assert "bilingual" in result["reason"]
        
    def test_session_metrics(self, willow_system):
        """Test session tracking and metrics"""
        # Run several interactions
        for i in range(3):
            willow_system.process_message(
                "test_user",
                f"Message {i}",
                {"arousal": 7-i, "capacity": 5+i}
            )
        
        # End session and check metrics
        metrics = willow_system.end_session("test_user")
        
        assert metrics["session_summary"]["interaction_count"] == 3
        assert "capacity_profile" in metrics
        assert "language_profile" in metrics
        assert "tier_progression" in metrics


class TestErrorHandling:
    """Test system resilience and error handling"""
    
    def test_missing_emotional_state(self):
        """Should handle missing emotional state gracefully"""
        willow = WillowIntegratedCore({})
        
        result = willow.process_message(
            "test_user",
            "Help needed",
            {}  # Empty emotional state
        )
        
        assert result["action"] in ["continue", "escalate_to_human"]
        assert "response" in result
        
    def test_symbol_system_failure(self):
        """Should degrade gracefully if symbol system fails"""
        willow = WillowIntegratedCore({"symbol_preference": "invalid_style"})
        
        result = willow.process_message(
            "test_user",
            "Emergency",
            {"arousal": 8, "capacity": 5}
        )
        
        # Should still provide response
        assert result["response"]
        assert result["action"] == "continue"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])