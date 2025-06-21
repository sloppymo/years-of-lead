#!/usr/bin/env python3
"""
Willow Commercial Data Model
Property management interaction tracking for compliance and operational efficiency
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class InteractionOutcome(Enum):
    """Business-focused outcome categories"""
    SELF_RESOLVED = "self_resolved"  # No human intervention needed
    DEFLECTED = "deflected"  # Successfully prevented escalation
    ESCALATED_ROUTINE = "escalated_routine"  # Standard business hours
    ESCALATED_EMERGENCY = "escalated_emergency"  # After-hours/costly
    ABANDONED = "abandoned"  # Tenant left conversation


class LiabilityFlag(Enum):
    """Legal risk indicators"""
    NONE = "none"
    HABITABILITY = "habitability"  # Heat, water, electric issues
    DISCRIMINATION_RISK = "discrimination_risk"  # Protected class mentions
    INJURY_MENTIONED = "injury_mentioned"
    LEGAL_THREAT = "legal_threat"  # Explicit legal action mentioned
    SAFETY_CONCERN = "safety_concern"  # Immediate danger


class CostCategory(Enum):
    """Operational cost impact"""
    ZERO_COST = "zero_cost"  # Fully automated
    LOW_COST = "low_cost"  # < $50 resolution
    MEDIUM_COST = "medium_cost"  # $50-500
    HIGH_COST = "high_cost"  # $500+
    EMERGENCY_COST = "emergency_cost"  # After-hours premium


@dataclass
class WillowInteractionRecord:
    """
    Commercial data entry for each tenant interaction
    Designed for compliance, efficiency tracking, and portfolio analytics
    """
    
    # Core Identifiers
    interaction_id: str
    tenant_id: str
    property_id: str
    portfolio_id: str
    unit_number: str
    
    # Temporal Data
    start_timestamp: datetime
    end_timestamp: Optional[datetime]
    duration_seconds: int
    after_hours: bool  # Premium cost indicator
    
    # Issue Classification (for pattern analysis)
    primary_issue_code: str  # HVAC_01, PLUMB_03, NOISE_02
    severity_score: int  # 1-10 for prioritization
    
    # Interaction Metrics
    total_messages: int
    tenant_messages: int
    willow_messages: int
    average_response_time_ms: float
    
    # Escalation Prevention
    escalation_attempted: bool
    escalation_prevented: bool
    deflection_techniques_used: List[str]  # ["breathing_prompt", "tier_1_containment"]
    human_handoff_avoided: bool
    
    # Compliance Documentation
    full_transcript: List[Dict]  # Complete audit trail
    liability_flags: List[LiabilityFlag]
    compliance_notes: List[str]  # Auto-generated risk documentation
    
    # Language/Accessibility
    primary_language: str
    language_switches_detected: int
    accessibility_accommodations: List[str]
    
    # Business Outcomes
    outcome: InteractionOutcome
    resolution_achieved: bool
    follow_up_required: bool
    estimated_cost_impact: CostCategory
    
    # Operational Efficiency
    ticket_created: bool
    ticket_id: Optional[str]
    work_order_generated: bool
    contractor_dispatch_required: bool
    
    # Tenant Satisfaction Proxy
    sentiment_start: float  # -1 to 1
    sentiment_end: float
    sentiment_delta: float
    profanity_count: int
    
    # Advanced Metrics
    cognitive_load_peak: float  # Highest capacity depletion
    emotional_peak_arousal: float  # Highest stress level
    tier_progression: List[str]  # ["tier_1", "tier_1", "tier_2"]
    symbols_used: Dict[str, int]  # {"nature": 5, "grounding": 3}
    
    # Legal Protection
    consent_documented: bool
    expectations_managed: bool  # Clear boundaries set
    commitments_made: List[str]  # Trackable promises
    
    # Revenue Impact
    retention_risk_score: float  # 0-1 probability of non-renewal
    lifetime_value_impact: float  # Estimated $ impact
    
    def to_analytics_payload(self) -> Dict:
        """Format for business intelligence systems"""
        return {
            "interaction_id": self.interaction_id,
            "property_id": self.property_id,
            "timestamp": self.start_timestamp.isoformat(),
            "duration": self.duration_seconds,
            "outcome": self.outcome.value,
            "cost_category": self.estimated_cost_impact.value,
            "human_avoided": self.human_handoff_avoided,
            "after_hours": self.after_hours,
            "liability_risk": max([f.value for f in self.liability_flags], default="none"),
            "retention_risk": self.retention_risk_score,
            "deflection_success": self.escalation_prevented,
            "issue_code": self.primary_issue_code
        }
    
    def to_compliance_record(self) -> Dict:
        """Format for legal/compliance systems"""
        return {
            "interaction_id": self.interaction_id,
            "tenant_id": self.tenant_id,
            "property_id": self.property_id,
            "timestamp": self.start_timestamp.isoformat(),
            "duration": self.duration_seconds,
            "full_transcript": self.full_transcript,
            "liability_flags": [f.value for f in self.liability_flags],
            "compliance_notes": self.compliance_notes,
            "commitments_made": self.commitments_made,
            "consent_documented": self.consent_documented,
            "primary_language": self.primary_language,
            "accessibility_accommodations": self.accessibility_accommodations
        }


# Example data entry
def create_example_interaction():
    """Example of a real Willow interaction data entry"""
    
    record = WillowInteractionRecord(
        # Identifiers
        interaction_id="INT_20250113_154323_7A9F",
        tenant_id="TEN_0934852",
        property_id="PROP_ATL_0342",
        portfolio_id="PORT_SOUTHEAST_01",
        unit_number="342B",
        
        # Temporal
        start_timestamp=datetime(2025, 1, 13, 15, 43, 23),
        end_timestamp=datetime(2025, 1, 13, 15, 51, 47),
        duration_seconds=504,
        after_hours=False,
        
        # Issue
        primary_issue_code="HVAC_01",  # No heat
        severity_score=8,  # High - habitability issue
        
        # Metrics
        total_messages=12,
        tenant_messages=7,
        willow_messages=5,
        average_response_time_ms=847,
        
        # Escalation Prevention SUCCESS
        escalation_attempted=True,
        escalation_prevented=True,
        deflection_techniques_used=["tier_1_containment", "breathing_prompt", "symbolic_grounding"],
        human_handoff_avoided=True,
        
        # Compliance
        full_transcript=[
            {"timestamp": "2025-01-13T15:43:23", "sender": "tenant", "message": "My heat is broken and kids freezing!!"},
            {"timestamp": "2025-01-13T15:43:26", "sender": "willow", "message": "I'm here with you. Having no heat with children is unacceptable. 🌊"},
            # ... full audit trail
        ],
        liability_flags=[LiabilityFlag.HABITABILITY],
        compliance_notes=[
            "Habitability issue acknowledged at 15:43:26",
            "Tenant mentioned children - vulnerability noted",
            "Emergency dispatch authorized at 15:48:12"
        ],
        
        # Language
        primary_language="en",
        language_switches_detected=0,
        accessibility_accommodations=[],
        
        # Business Outcome
        outcome=InteractionOutcome.DEFLECTED,
        resolution_achieved=True,
        follow_up_required=True,
        estimated_cost_impact=CostCategory.MEDIUM_COST,  # Emergency HVAC ~$300
        
        # Operational
        ticket_created=True,
        ticket_id="TICK_2025_003942",
        work_order_generated=True,
        contractor_dispatch_required=True,
        
        # Satisfaction
        sentiment_start=-0.85,  # Very negative
        sentiment_end=-0.3,  # Improved significantly
        sentiment_delta=0.55,
        profanity_count=0,
        
        # Advanced
        cognitive_load_peak=2.3,  # Low capacity detected
        emotional_peak_arousal=9.2,  # Very high stress
        tier_progression=["tier_1", "tier_1", "tier_1", "tier_2"],
        symbols_used={"nature": 4, "grounding": 4},
        
        # Legal
        consent_documented=True,
        expectations_managed=True,
        commitments_made=["Emergency HVAC dispatch today", "Follow-up within 4 hours"],
        
        # Revenue
        retention_risk_score=0.15,  # Low risk after successful resolution
        lifetime_value_impact=250.00  # Saved potential early termination
    )
    
    return record


# Portfolio-level aggregation
@dataclass 
class PortfolioMetrics:
    """Aggregate metrics for property management companies"""
    
    portfolio_id: str
    reporting_period: str
    
    # Efficiency Metrics
    total_interactions: int
    human_escalations_prevented: int
    deflection_rate: float
    average_resolution_time: float
    after_hours_saves: int
    
    # Cost Metrics  
    estimated_labor_savings: float
    emergency_callout_reduction: float
    legal_exposure_mitigated: int
    
    # Compliance
    documented_interactions: int
    liability_incidents_flagged: int
    discrimination_risks_identified: int
    
    # Tenant Satisfaction
    average_sentiment_improvement: float
    retention_risk_reduction: float
    
    # ROI Calculation
    total_cost_savings: float
    willow_subscription_cost: float
    net_roi: float
    
    def executive_summary(self) -> str:
        return f"""
Portfolio {self.portfolio_id} - {self.reporting_period}
• Deflected {self.human_escalations_prevented:,} escalations ({self.deflection_rate:.1%} rate)
• Saved ${self.estimated_labor_savings:,.0f} in labor costs
• Reduced after-hours calls by {self.after_hours_saves}
• ROI: {self.net_roi:.1%}
• Legal risks identified and documented: {self.liability_incidents_flagged}
        """


if __name__ == "__main__":
    # Example interaction
    interaction = create_example_interaction()
    
    print("=== ANALYTICS PAYLOAD ===")
    print(json.dumps(interaction.to_analytics_payload(), indent=2))
    
    print("\n=== COMPLIANCE RECORD (excerpt) ===")
    compliance = interaction.to_compliance_record()
    compliance["full_transcript"] = "[TRUNCATED]"  # Don't print full transcript
    print(json.dumps(compliance, indent=2))