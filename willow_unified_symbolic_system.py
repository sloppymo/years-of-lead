#!/usr/bin/env python3
"""
Willow Unified Symbolic System
Ensures symbolic continuity across all response types
"""

from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class SymbolicContext:
    """Maintains symbolic continuity throughout interaction"""
    user_id: str
    preferred_style: str = "traditional"
    last_symbol: str = ""
    symbol_history: List[Dict] = field(default_factory=list)
    emotional_trajectory: List[Dict] = field(default_factory=list)


class UnifiedSymbolicAnchor:
    """Ensures every response maintains symbolic consistency"""
    
    SYMBOL_CONTINUITY_MAP = {
        "crisis_escalation": {
            "traditional": ["💙", "🫂", "🌟"],
            "nature": ["🌊", "🌿", "🌅"],
            "minimal": ["•", "→", "✓"],
            "none": ["", "", ""]
        },
        "edge_case_grounding": {
            "traditional": {"rapid_fire": "⚡→💙", "contradiction": "🔄", "silence": "...💙"},
            "nature": {"rapid_fire": "🌪️→🌊", "contradiction": "🍃", "silence": "...🌿"},
            "minimal": {"rapid_fire": "!→•", "contradiction": "~", "silence": "...•"},
            "none": {"rapid_fire": "", "contradiction": "", "silence": ""}
        }
    }
    
    def __init__(self, symbolic_context: SymbolicContext):
        self.context = symbolic_context
        
    def wrap_response(self, response: str, response_type: str, emotional_state: Dict) -> str:
        """Wrap any response with appropriate symbolic anchoring"""
        
        # Get appropriate symbol based on context
        symbol = self._select_symbol(response_type, emotional_state)
        
        # Track symbol usage
        self.context.symbol_history.append({
            "symbol": symbol,
            "type": response_type,
            "arousal": emotional_state.get("arousal", 5)
        })
        
        # Apply symbol with proper spacing
        if symbol:
            if response_type in ["edge_case", "escalation"]:
                # For edge cases, integrate symbol more naturally
                return self._integrate_edge_symbol(response, symbol)
            else:
                # Standard tier responses
                return f"{response} {symbol}"
        return response
    
    def _select_symbol(self, response_type: str, emotional_state: Dict) -> str:
        """Select contextually appropriate symbol"""
        arousal = emotional_state.get("arousal", 5)
        
        # High arousal: use grounding symbols
        if arousal > 8:
            symbol_set = self.SYMBOL_CONTINUITY_MAP["crisis_escalation"][self.context.preferred_style]
            return symbol_set[0]  # Primary grounding symbol
        
        # Edge cases: use specific symbols
        if response_type.startswith("edge_"):
            edge_type = response_type.split("_", 1)[1]
            return self.SYMBOL_CONTINUITY_MAP["edge_case_grounding"][self.context.preferred_style].get(edge_type, "")
        
        # Normal progression
        if self.context.last_symbol:
            # Maintain continuity
            return self.context.last_symbol
        
        return self.SYMBOL_CONTINUITY_MAP["crisis_escalation"][self.context.preferred_style][1]
    
    def _integrate_edge_symbol(self, response: str, symbol: str) -> str:
        """Naturally integrate symbols into edge case responses"""
        if "breathe" in response.lower():
            return response.replace("breathe", f"breathe {symbol}")
        elif response.endswith("."):
            return response[:-1] + f" {symbol}"
        else:
            return f"{response} {symbol}"


class SymbolicEdgeCaseResolver:
    """Edge case handler with symbolic continuity"""
    
    def __init__(self, symbolic_anchor: UnifiedSymbolicAnchor):
        self.anchor = symbolic_anchor
        self.protocols = {
            "rapid_fire": {
                "base_response": "I see many messages - let's slow down together. Breathe with me: in... out...",
                "symbolic_integration": "embedded"
            },
            "contradiction": {
                "base_response": "Changing your mind is okay. I'm here whether you need action or just presence.",
                "symbolic_integration": "suffix"
            },
            "language_switch": {
                "base_response": "I notice you're switching languages. Continue in whatever feels natural.",
                "symbolic_integration": "embedded"
            },
            "dissociation": {
                "base_response": "I'm here with you in this moment. Notice one thing you can touch right now.",
                "symbolic_integration": "suffix"
            }
        }
    
    def handle(self, edge_type: str, emotional_state: Dict) -> Optional[str]:
        """Generate symbolically consistent edge case response"""
        if edge_type not in self.protocols:
            return None
            
        protocol = self.protocols[edge_type]
        base_response = protocol["base_response"]
        
        # Apply symbolic anchoring
        return self.anchor.wrap_response(
            base_response,
            f"edge_{edge_type}",
            emotional_state
        )


# Example: Maintaining continuity across response types
def demonstrate_symbolic_continuity():
    # User in crisis
    context = SymbolicContext(
        user_id="tenant_123",
        preferred_style="nature"
    )
    
    anchor = UnifiedSymbolicAnchor(context)
    edge_resolver = SymbolicEdgeCaseResolver(anchor)
    
    # Tier 1 response
    tier1 = "I'm here with you. This flooding is overwhelming."
    print("Tier 1:", anchor.wrap_response(tier1, "tier_1", {"arousal": 9}))
    
    # Edge case occurs
    edge = edge_resolver.handle("rapid_fire", {"arousal": 9.5})
    print("Edge Case:", edge)
    
    # Tier 2 follows
    tier2 = "When ready:\n1. FLOOD - stop water\n2. SAVE - protect items"
    print("Tier 2:", anchor.wrap_response(tier2, "tier_2", {"arousal": 8}))