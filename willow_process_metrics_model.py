#!/usr/bin/env python3
"""
Willow Process Metrics Model
Tracks the emotional and symbolic mechanisms that drive commercial outcomes
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ContainmentQuality(Enum):
    """How well containment principles were maintained"""
    EXCELLENT = "excellent"  # Full tier progression, no premature solutions
    GOOD = "good"  # Minor deviations but recovered
    COMPROMISED = "compromised"  # Jumped to solutions too early
    FAILED = "failed"  # Lost containment entirely


class SymbolicContinuity(Enum):
    """Symbolic anchor persistence throughout interaction"""
    MAINTAINED = "maintained"  # Consistent symbolic presence
    INTERMITTENT = "intermittent"  # Some gaps but mostly present
    BROKEN = "broken"  # Lost symbolic thread
    NONE = "none"  # No symbolic anchoring used


class EmotionalTrajectory(Enum):
    """Path of emotional state change"""
    SMOOTH_DESCENT = "smooth_descent"  # Gradual calming
    STEPPED_DESCENT = "stepped_descent"  # Clear tier transitions
    VOLATILE_RECOVERY = "volatile_recovery"  # Up and down but ended lower
    ESCALATION = "escalation"  # Increased arousal
    PLATEAU = "plateau"  # No significant change


@dataclass
class WillowProcessMetrics:
    """
    Tracks HOW Willow achieved its outcome, not just what the outcome was
    Focus: Emotional containment mechanisms that enable commercial success
    """
    
    # Core Identifiers
    interaction_id: str
    tenant_id: str
    property_id: str
    timestamp: datetime
    
    # Emotional Containment Process
    tier_progression: List[str]  # ["tier_1", "tier_1", "tier_1.5", "tier_2"]
    tier_violations: List[Dict]  # Premature solution attempts
    containment_quality: ContainmentQuality
    autonomy_preserved: bool  # Did we avoid imposing solutions?
    consent_checkpoints: List[Tuple[str, bool]]  # [("ready_for_options", True)]
    
    # Symbolic Tracking
    symbolic_style: str  # "nature", "traditional", "minimal", "none"
    symbolic_consistency: SymbolicContinuity
    symbols_per_tier: Dict[str, int]  # {"tier_1": 4, "tier_2": 2}
    symbolic_gaps: List[str]  # Where continuity broke
    edge_case_symbol_handling: Dict[str, bool]  # {"rapid_fire": True}
    
    # Emotional Trajectory
    arousal_curve: List[float]  # [9.2, 8.7, 8.1, 7.3, 6.5]
    capacity_curve: List[float]  # [5.0, 4.2, 3.1, 3.5, 4.0]
    emotional_trajectory: EmotionalTrajectory
    peak_arousal: float
    arousal_reduction: float  # Peak to final
    capacity_nadir: float  # Lowest point
    capacity_recovery: float  # Nadir to final
    
    # De-escalation Mechanics
    grounding_prompts_used: int
    grounding_acceptance_rate: float  # % of prompts followed
    breathing_synchronization: bool  # Did tenant mirror breathing cues?
    validation_timing: List[Dict]  # When validation was offered vs needed
    
    # Tier Transition Quality
    tier_1_duration_messages: int  # How many messages in containment
    tier_1_arousal_gate_respected: bool  # Was arousal < 7 before tier 2?
    tier_2_consent_explicit: bool  # Clear readiness signal?
    solution_timing_appropriate: bool  # Not too early, not too late
    
    # Language Complexity Adaptation
    initial_complexity_score: float  # Flesch-Kincaid or similar
    final_complexity_score: float
    complexity_adaptations: List[Dict]  # When and why language simplified
    emergency_simplification_triggered: bool
    
    # Trust Building Indicators
    tenant_disclosure_depth: int  # 1-5 scale of vulnerability
    reciprocal_engagement: bool  # Two-way conversation vs monologue
    resistance_moments: List[Dict]  # Where tenant pushed back
    trust_recovery_successful: bool  # Did we rebuild after resistance?
    
    # Resolution Quality
    resolution_type: str  # "accepted", "deferred", "partial", "rejected"
    resolution_autonomy_score: float  # How much tenant owned the solution
    commitments_bilateral: bool  # Both parties made commitments
    follow_through_likelihood: float  # Based on engagement quality
    
    # Clinical Integrity Metrics
    trauma_informed_score: float  # Composite of containment + autonomy + pacing
    therapeutic_container_maintained: bool
    emotional_safety_preserved: bool
    power_dynamics_balanced: bool
    
    # Outcome Indicators (consequences, not causes)
    escalation_avoided: bool
    human_handoff_needed: bool
    tenant_satisfaction_proxy: float  # Derived from trajectory
    retention_risk_delta: float  # Change in retention probability
    compliance_quality: float  # How defensible is this interaction?
    
    def analyze_success_factors(self) -> Dict:
        """Identify which mechanisms drove the outcome"""
        factors = {
            "containment_drove_success": False,
            "symbolic_continuity_critical": False,
            "capacity_adaptation_key": False,
            "trust_building_essential": False,
            "tier_progression_optimal": False
        }
        
        # Containment quality directly correlates with de-escalation
        if self.containment_quality in [ContainmentQuality.EXCELLENT, ContainmentQuality.GOOD]:
            if self.arousal_reduction > 2.0:
                factors["containment_drove_success"] = True
        
        # Symbolic continuity maintains therapeutic container
        if self.symbolic_consistency == SymbolicContinuity.MAINTAINED:
            if self.emotional_trajectory in [EmotionalTrajectory.SMOOTH_DESCENT, 
                                            EmotionalTrajectory.STEPPED_DESCENT]:
                factors["symbolic_continuity_critical"] = True
        
        # Capacity adaptation prevents overwhelm
        if self.capacity_nadir < 3.0 and self.capacity_recovery > 1.0:
            if self.emergency_simplification_triggered and self.escalation_avoided:
                factors["capacity_adaptation_key"] = True
        
        # Trust building enables resolution acceptance
        if self.tenant_disclosure_depth >= 3 and self.trust_recovery_successful:
            if self.resolution_autonomy_score > 0.7:
                factors["trust_building_essential"] = True
        
        # Tier progression timing
        if (self.tier_1_arousal_gate_respected and 
            self.tier_2_consent_explicit and 
            self.solution_timing_appropriate):
            factors["tier_progression_optimal"] = True
        
        return factors
    
    def generate_process_summary(self) -> str:
        """Human-readable summary of what made this interaction work"""
        success_factors = self.analyze_success_factors()
        
        summary = f"Interaction {self.interaction_id}:\n"
        
        # Emotional journey
        summary += f"• Emotional arc: {self.arousal_curve[0]:.1f}→{self.arousal_curve[-1]:.1f} "
        summary += f"({self.emotional_trajectory.value})\n"
        
        # Containment quality
        summary += f"• Containment: {self.containment_quality.value}"
        if self.tier_violations:
            summary += f" ({len(self.tier_violations)} violations)"
        summary += "\n"
        
        # Symbolic continuity
        summary += f"• Symbols: {self.symbolic_consistency.value} "
        summary += f"({sum(self.symbols_per_tier.values())} total)\n"
        
        # Key mechanisms
        summary += "• Success drivers: "
        drivers = [k.replace("_", " ") for k, v in success_factors.items() if v]
        summary += ", ".join(drivers) if drivers else "standard process"
        
        return summary


# Example: What actually gets tracked
def create_process_focused_entry():
    """Example showing process metrics that drive outcomes"""
    
    return WillowProcessMetrics(
        # Identifiers
        interaction_id="INT_20250113_154323_7A9F",
        tenant_id="TEN_0934852", 
        property_id="PROP_ATL_0342",
        timestamp=datetime.now(),
        
        # The HOW: Emotional Containment Process
        tier_progression=["tier_1", "tier_1", "tier_1", "tier_1.5", "tier_2"],
        tier_violations=[],  # None! Perfect progression
        containment_quality=ContainmentQuality.EXCELLENT,
        autonomy_preserved=True,
        consent_checkpoints=[
            ("breathing_acknowledged", True),
            ("ready_for_options", True),
            ("solution_acceptance", True)
        ],
        
        # The HOW: Symbolic Continuity
        symbolic_style="nature",
        symbolic_consistency=SymbolicContinuity.MAINTAINED,
        symbols_per_tier={"tier_1": 4, "tier_1.5": 1, "tier_2": 2},
        symbolic_gaps=[],
        edge_case_symbol_handling={},
        
        # The HOW: Emotional Movement
        arousal_curve=[9.2, 8.7, 8.1, 7.3, 6.5],
        capacity_curve=[5.0, 4.2, 3.1, 3.5, 4.0],
        emotional_trajectory=EmotionalTrajectory.SMOOTH_DESCENT,
        peak_arousal=9.2,
        arousal_reduction=2.7,
        capacity_nadir=3.1,
        capacity_recovery=0.9,
        
        # The HOW: Active Techniques
        grounding_prompts_used=3,
        grounding_acceptance_rate=0.67,  # 2 of 3 followed
        breathing_synchronization=True,
        validation_timing=[
            {"message": 2, "validation_type": "situational", "tenant_response": "positive"},
            {"message": 4, "validation_type": "emotional", "tenant_response": "softening"}
        ],
        
        # The HOW: Careful Progression
        tier_1_duration_messages=4,
        tier_1_arousal_gate_respected=True,  # Waited until < 7
        tier_2_consent_explicit=True,
        solution_timing_appropriate=True,
        
        # The HOW: Adaptation
        initial_complexity_score=8.2,
        final_complexity_score=5.1,
        complexity_adaptations=[
            {"message": 3, "reason": "capacity_drop", "new_score": 6.5},
            {"message": 5, "reason": "capacity_nadir", "new_score": 5.1}
        ],
        emergency_simplification_triggered=False,  # Didn't need it
        
        # The HOW: Relationship Building
        tenant_disclosure_depth=3,
        reciprocal_engagement=True,
        resistance_moments=[
            {"message": 3, "type": "solution_rejection", "response": "return_to_tier_1"}
        ],
        trust_recovery_successful=True,
        
        # The WHAT: Resolution Quality
        resolution_type="accepted",
        resolution_autonomy_score=0.85,
        commitments_bilateral=True,
        follow_through_likelihood=0.78,
        
        # Clinical Integrity (composite scores)
        trauma_informed_score=0.92,
        therapeutic_container_maintained=True,
        emotional_safety_preserved=True,
        power_dynamics_balanced=True,
        
        # Outcomes (consequences of good process)
        escalation_avoided=True,
        human_handoff_needed=False,
        tenant_satisfaction_proxy=0.73,
        retention_risk_delta=-0.15,  # Reduced risk
        compliance_quality=0.95
    )


if __name__ == "__main__":
    # Show what we actually track
    entry = create_process_focused_entry()
    
    print(entry.generate_process_summary())
    print("\n=== SUCCESS FACTOR ANALYSIS ===")
    factors = entry.analyze_success_factors()
    for factor, was_critical in factors.items():
        print(f"{'✓' if was_critical else '○'} {factor.replace('_', ' ').title()}")
    
    print("\n=== KEY INSIGHT ===")
    print("This interaction succeeded because:")
    print("- Containment was never broken (4 Tier 1 messages)")
    print("- Symbolic continuity maintained (7 nature symbols)")
    print("- Capacity crash (3.1) was detected and language adapted")
    print("- Trust was rebuilt after initial solution rejection")
    print("\nThe $500 saved on emergency callout? That's just what happens")
    print("when you respect the therapeutic process.")