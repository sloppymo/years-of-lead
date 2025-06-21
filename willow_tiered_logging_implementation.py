#!/usr/bin/env python3
"""
Willow Tiered Logging Implementation
Production-ready logging that tracks process metrics, not just outcomes
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import uuid


class LogTier(Enum):
    """Logging tier levels"""
    CORE = "core"  # Always stored - compliance & KPIs
    BEHAVIORAL = "behavioral"  # Warm storage - tuning data
    FORENSIC = "forensic"  # Cold storage - detailed analysis


@dataclass
class WillowLogEntry:
    """Structured log entry with tiered data"""
    
    # Always included
    interaction_id: str
    tenant_id: str
    property_id: str
    timestamp: datetime
    
    # Tier 1: Core compliance & business metrics
    core_metrics: Dict[str, Any]
    
    # Tier 2: Behavioral/process metrics
    behavioral_metrics: Optional[Dict[str, Any]] = None
    
    # Tier 3: Forensic detail
    forensic_data: Optional[Dict[str, Any]] = None
    
    def to_storage_format(self, include_tiers: List[LogTier]) -> Dict:
        """Convert to storage format based on tier requirements"""
        
        base = {
            "interaction_id": self.interaction_id,
            "tenant_id": self.tenant_id,
            "property_id": self.property_id,
            "timestamp": self.timestamp.isoformat(),
            "core": self.core_metrics
        }
        
        if LogTier.BEHAVIORAL in include_tiers and self.behavioral_metrics:
            base["behavioral"] = self.behavioral_metrics
            
        if LogTier.FORENSIC in include_tiers and self.forensic_data:
            base["forensic"] = self.forensic_data
            
        return base


class WillowLogger:
    """Tiered logging system optimized for process tracking"""
    
    def __init__(self, 
                 enable_behavioral: bool = True,
                 enable_forensic: bool = True,
                 auto_archive_forensic: bool = True):
        
        self.enable_behavioral = enable_behavioral
        self.enable_forensic = enable_forensic
        self.auto_archive_forensic = auto_archive_forensic
        
    def log_interaction(self, 
                       interaction_data: Dict,
                       subsystem_states: Dict) -> WillowLogEntry:
        """Create log entry from interaction data"""
        
        entry = WillowLogEntry(
            interaction_id=str(uuid.uuid4()),
            tenant_id=interaction_data["tenant_id"],
            property_id=interaction_data["property_id"],
            timestamp=datetime.now(),
            core_metrics=self._extract_core_metrics(interaction_data, subsystem_states),
            behavioral_metrics=self._extract_behavioral_metrics(subsystem_states) if self.enable_behavioral else None,
            forensic_data=self._extract_forensic_data(subsystem_states) if self.enable_forensic else None
        )
        
        # Handle storage based on configuration
        self._store_log_entry(entry)
        
        return entry
    
    def _extract_core_metrics(self, interaction_data: Dict, subsystem_states: Dict) -> Dict:
        """Extract Tier 1 core metrics - always collected"""
        
        return {
            # Compliance essentials
            "outcome": interaction_data.get("action", "continue"),
            "escalation_triggered": interaction_data.get("action") == "escalate_to_human",
            "escalation_reason": interaction_data.get("reason", ""),
            "duration_seconds": interaction_data.get("session_metrics", {}).get("duration", 0),
            
            # Business KPIs
            "deflection_successful": interaction_data.get("action") != "escalate_to_human",
            "tier_reached": interaction_data.get("tier", "unknown"),
            "after_hours": interaction_data.get("after_hours", False),
            
            # Risk flags
            "liability_detected": self._check_liability_flags(interaction_data),
            "consent_documented": subsystem_states.get("tier", {}).get("consent_received", False),
            
            # Basic process indicator
            "containment_delivered": subsystem_states.get("tier", {}).get("tier_1_count", 0) > 0
        }
    
    def _extract_behavioral_metrics(self, subsystem_states: Dict) -> Dict:
        """Extract Tier 2 behavioral metrics - for optimization"""
        
        tier_data = subsystem_states.get("tier", {})
        capacity_data = subsystem_states.get("capacity", {})
        language_data = subsystem_states.get("language", {})
        symbolic_data = subsystem_states.get("symbolic", {})
        
        return {
            # Tier progression quality
            "tier_progression": {
                "tier_1_count": tier_data.get("tier_1_count", 0),
                "consent_received": tier_data.get("consent_received", False),
                "arousal_at_tier_2": tier_data.get("arousal_average", 0),
                "capacity_at_tier_2": tier_data.get("capacity_score", 0)
            },
            
            # Symbolic continuity
            "symbolic_tracking": {
                "style_used": symbolic_data.get("style", "none"),
                "current_symbol": symbolic_data.get("current_symbol", ""),
                "consistency_maintained": True  # Would check history in production
            },
            
            # Capacity management
            "capacity_trajectory": {
                "exhaustion_level": capacity_data.get("exhaustion_level", "none"),
                "dissociation_risk": capacity_data.get("dissociation_risk", 0),
                "capacity_adapted": "emergency_simplification" in capacity_data.get("recommendations", [])
            },
            
            # Language handling
            "language_dynamics": {
                "code_switch_detected": language_data.get("is_code_switch", False),
                "primary_language": language_data.get("primary_language", "en"),
                "crisis_language_switching": language_data.get("crisis_indicators", {}).get("is_crisis", False)
            }
        }
    
    def _extract_forensic_data(self, subsystem_states: Dict) -> Dict:
        """Extract Tier 3 forensic data - for deep analysis"""
        
        return {
            # Complete subsystem states
            "full_tier_state": subsystem_states.get("tier", {}),
            "full_capacity_profile": subsystem_states.get("capacity", {}),
            "full_language_analysis": subsystem_states.get("language", {}),
            "full_symbolic_context": subsystem_states.get("symbolic", {}),
            
            # Decision paths
            "tier_decision_rationale": subsystem_states.get("tier", {}).get("rationale", ""),
            "capacity_recommendations": subsystem_states.get("capacity", {}).get("recommendations", []),
            
            # For ML training
            "arousal_curve": subsystem_states.get("capacity", {}).get("arousal_trend", []),
            "message_coherence_scores": []  # Would be populated in production
        }
    
    def _check_liability_flags(self, interaction_data: Dict) -> Dict:
        """Check for liability indicators"""
        
        flags = {
            "habitability": False,
            "discrimination_risk": False,
            "injury_mentioned": False,
            "legal_threat": False
        }
        
        # Simple keyword detection (would be more sophisticated in production)
        message = interaction_data.get("message", "").lower()
        
        if any(word in message for word in ["heat", "water", "electric", "mold"]):
            flags["habitability"] = True
            
        if any(word in message for word in ["lawyer", "sue", "court", "illegal"]):
            flags["legal_threat"] = True
            
        return flags
    
    def _store_log_entry(self, entry: WillowLogEntry):
        """Store log entry according to tier configuration"""
        
        # Tier 1: Always goes to hot storage
        self._store_hot(entry.to_storage_format([LogTier.CORE]))
        
        # Tier 2: Behavioral data to warm storage
        if self.enable_behavioral:
            self._store_warm(entry.to_storage_format([LogTier.CORE, LogTier.BEHAVIORAL]))
        
        # Tier 3: Forensic data to cold storage
        if self.enable_forensic and self.auto_archive_forensic:
            self._archive_cold(entry.to_storage_format([LogTier.FORENSIC]))
    
    def _store_hot(self, data: Dict):
        """Store in hot storage (e.g., Redis, DynamoDB)"""
        # Implementation would connect to actual hot storage
        pass
    
    def _store_warm(self, data: Dict):
        """Store in warm storage (e.g., PostgreSQL, MongoDB)"""
        # Implementation would connect to actual warm storage
        pass
    
    def _archive_cold(self, data: Dict):
        """Archive to cold storage (e.g., S3, BigQuery)"""
        # Implementation would connect to actual cold storage
        pass
    
    def generate_dashboard_metrics(self, entry: WillowLogEntry) -> Dict:
        """Generate dashboard-friendly metrics from log entry"""
        
        core = entry.core_metrics
        behavioral = entry.behavioral_metrics or {}
        
        return {
            "interaction_id": entry.interaction_id,
            "timestamp": entry.timestamp.isoformat(),
            
            # Executive metrics
            "outcome": "DEFLECTED" if core["deflection_successful"] else "ESCALATED",
            "cost_impact": self._calculate_cost_impact(core, behavioral),
            "risk_level": self._calculate_risk_level(core),
            
            # Process quality indicators
            "containment_quality": self._assess_containment_quality(behavioral),
            "symbolic_integrity": behavioral.get("symbolic_tracking", {}).get("consistency_maintained", False),
            "capacity_management": behavioral.get("capacity_trajectory", {}).get("exhaustion_level", "unknown"),
            
            # Actionable insights
            "optimization_opportunities": self._identify_optimizations(behavioral)
        }
    
    def _calculate_cost_impact(self, core: Dict, behavioral: Dict) -> Dict:
        """Calculate estimated cost impact"""
        
        base_cost = 0
        
        if core["deflection_successful"]:
            # Avoided human escalation
            if core["after_hours"]:
                base_cost = 500  # After-hours premium
            else:
                base_cost = 150  # Standard escalation cost
                
        # Adjust based on tier reached
        if core["tier_reached"] == "tier_2" and core["deflection_successful"]:
            base_cost *= 1.2  # Higher value for complete resolution
            
        return {
            "estimated_savings": base_cost,
            "confidence": "high" if behavioral else "medium"
        }
    
    def _calculate_risk_level(self, core: Dict) -> str:
        """Calculate liability risk level"""
        
        flags = core.get("liability_detected", {})
        
        if flags.get("legal_threat"):
            return "high"
        elif flags.get("habitability") or flags.get("injury_mentioned"):
            return "medium"
        elif flags.get("discrimination_risk"):
            return "medium"
        
        return "low"
    
    def _assess_containment_quality(self, behavioral: Dict) -> str:
        """Assess quality of emotional containment"""
        
        if not behavioral:
            return "unknown"
            
        tier_data = behavioral.get("tier_progression", {})
        
        if tier_data.get("tier_1_count", 0) >= 3 and tier_data.get("consent_received"):
            if tier_data.get("arousal_at_tier_2", 10) < 7:
                return "excellent"
            return "good"
        elif tier_data.get("tier_1_count", 0) > 0:
            return "partial"
        
        return "poor"
    
    def _identify_optimizations(self, behavioral: Dict) -> List[str]:
        """Identify optimization opportunities"""
        
        optimizations = []
        
        if not behavioral:
            return ["Enable behavioral tracking for insights"]
            
        # Check for premature tier progression
        if behavioral.get("tier_progression", {}).get("tier_1_count", 0) < 2:
            optimizations.append("Increase containment duration")
            
        # Check for capacity issues
        if behavioral.get("capacity_trajectory", {}).get("exhaustion_level") in ["moderate", "severe"]:
            optimizations.append("Enhance capacity adaptation")
            
        # Check for language switching
        if behavioral.get("language_dynamics", {}).get("crisis_language_switching"):
            optimizations.append("Consider bilingual specialist routing")
            
        return optimizations


# Example usage showing process-focused logging
def demonstrate_process_logging():
    """Show how process metrics drive logging"""
    
    logger = WillowLogger(
        enable_behavioral=True,
        enable_forensic=True,
        auto_archive_forensic=True
    )
    
    # Simulate an interaction
    interaction_data = {
        "tenant_id": "TEN_123",
        "property_id": "PROP_456",
        "action": "continue",  # Successfully deflected
        "tier": "tier_2",
        "after_hours": True,
        "message": "My heat is broken and I'm freezing!",
        "session_metrics": {
            "duration": 423
        }
    }
    
    # Process-focused subsystem states
    subsystem_states = {
        "tier": {
            "tier_1_count": 4,  # Good containment!
            "consent_received": True,
            "arousal_average": 6.5,  # Below threshold
            "capacity_score": 4.2
        },
        "capacity": {
            "exhaustion_level": "mild",
            "dissociation_risk": 0.1,
            "recommendations": ["simplify_language"],
            "arousal_trend": [9.2, 8.5, 7.8, 6.9, 6.5]
        },
        "language": {
            "primary_language": "en",
            "is_code_switch": False,
            "crisis_indicators": {"is_crisis": False}
        },
        "symbolic": {
            "style": "nature",
            "current_symbol": "🌊",
            "consistency_maintained": True
        }
    }
    
    # Create log entry
    entry = logger.log_interaction(interaction_data, subsystem_states)
    
    # Generate dashboard view
    dashboard = logger.generate_dashboard_metrics(entry)
    
    print("=== PROCESS-FOCUSED LOGGING ===\n")
    
    print("Core Metrics (Always Logged):")
    print(f"  Outcome: {dashboard['outcome']}")
    print(f"  Cost Impact: ${dashboard['cost_impact']['estimated_savings']}")
    print(f"  Risk Level: {dashboard['risk_level']}")
    
    print("\nBehavioral Metrics (Process Quality):")
    print(f"  Containment Quality: {dashboard['containment_quality']}")
    print(f"  Tier 1 Messages: {subsystem_states['tier']['tier_1_count']}")
    print(f"  Arousal at Tier 2: {subsystem_states['tier']['arousal_average']}")
    print(f"  Symbolic Integrity: {'✓' if dashboard['symbolic_integrity'] else '✗'}")
    
    print("\nKey Insight:")
    print("  The $500 saved happened BECAUSE:")
    print("  - We maintained containment for 4 messages")
    print("  - Arousal dropped below 7.0 before solutions")
    print("  - Symbolic continuity was preserved")
    print("  - Consent was explicitly received")
    
    print("\nOptimization Opportunities:")
    for opt in dashboard['optimization_opportunities']:
        print(f"  - {opt}")


if __name__ == "__main__":
    demonstrate_process_logging()