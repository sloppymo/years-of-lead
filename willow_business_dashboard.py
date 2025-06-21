#!/usr/bin/env python3
"""
Willow Business Dashboard
Real-time operational metrics for property management companies
"""

from datetime import datetime, timedelta
from typing import Dict, List
import json


class WillowOperationalDashboard:
    """
    Executive dashboard for property management operations
    Focus: Cost savings, deflection rates, liability mitigation
    """
    
    def generate_realtime_metrics(self, portfolio_id: str) -> Dict:
        """Generate real-time operational metrics"""
        
        # This would pull from actual database in production
        return {
            "dashboard_generated": datetime.now().isoformat(),
            "portfolio_id": portfolio_id,
            
            "current_24h_metrics": {
                "total_interactions": 847,
                "human_escalations_prevented": 612,
                "deflection_rate": 72.2,
                "avg_resolution_time_seconds": 342,
                
                "cost_savings": {
                    "labor_hours_saved": 153,
                    "labor_cost_saved": 6885.00,  # $45/hr * 153
                    "after_hours_callouts_prevented": 23,
                    "after_hours_savings": 11500.00,  # $500/callout * 23
                    "total_24h_savings": 18385.00
                },
                
                "liability_protection": {
                    "habitability_issues_documented": 47,
                    "legal_threats_defused": 3,
                    "discrimination_risks_flagged": 2,
                    "injury_mentions_escalated": 1,
                    "compliance_documentation_rate": 100.0
                }
            },
            
            "current_month_metrics": {
                "interactions": 24329,
                "deflection_rate": 71.8,
                "human_touches_avoided": 17468,
                "estimated_fte_reduction": 8.7,  # Full-time equivalents
                
                "financial_impact": {
                    "labor_savings": 197640.00,
                    "emergency_callout_savings": 167500.00,
                    "legal_cost_avoidance": 45000.00,  # Estimated
                    "total_savings": 410140.00,
                    "willow_cost": 12500.00,  # Monthly subscription
                    "net_savings": 397640.00,
                    "roi_percentage": 3181.1
                },
                
                "tenant_retention": {
                    "high_risk_tenants_identified": 234,
                    "retention_interventions": 189,
                    "estimated_turnover_prevented": 67,
                    "turnover_cost_avoided": 201000.00  # $3k per unit
                }
            },
            
            "issue_patterns": {
                "top_issues": [
                    {"code": "HVAC_01", "count": 3421, "avg_cost": 285},
                    {"code": "PLUMB_03", "count": 2156, "avg_cost": 175},
                    {"code": "NOISE_02", "count": 1893, "avg_cost": 0},
                    {"code": "PEST_01", "count": 1234, "avg_cost": 425},
                    {"code": "LOCK_04", "count": 987, "avg_cost": 95}
                ],
                "predictive_maintenance_opportunities": 14,
                "bulk_contract_negotiation_potential": 89500.00
            },
            
            "compliance_metrics": {
                "audit_ready_interactions": 24329,
                "average_documentation_quality": 98.7,
                "fair_housing_compliance_rate": 99.9,
                "ada_accommodation_tracking": 156,
                "legal_discovery_ready": True
            },
            
            "operational_efficiency": {
                "property_manager_interruptions_prevented": 8934,
                "average_pm_focus_time_gained_daily": 2.3,  # hours
                "maintenance_dispatch_automation_rate": 67.8,
                "vendor_coordination_automated": 1245
            }
        }
    
    def generate_executive_summary(self, metrics: Dict) -> str:
        """Generate C-suite friendly summary"""
        
        monthly = metrics["current_month_metrics"]["financial_impact"]
        
        return f"""
WILLOW EXECUTIVE SUMMARY - {metrics['portfolio_id']}
Generated: {metrics['dashboard_generated']}

💰 FINANCIAL IMPACT (Current Month)
• Net Savings: ${monthly['net_savings']:,.0f}
• ROI: {monthly['roi_percentage']:.0%}
• FTE Reduction: {metrics['current_month_metrics']['estimated_fte_reduction']:.1f} positions

📊 OPERATIONAL EFFICIENCY
• Deflection Rate: {metrics['current_month_metrics']['deflection_rate']:.1%}
• Human Touches Avoided: {metrics['current_month_metrics']['human_touches_avoided']:,}
• After-Hours Calls Prevented: {metrics['current_24h_metrics']['cost_savings']['after_hours_callouts_prevented']} (last 24h)

⚖️ RISK MITIGATION
• Legal Threats Defused: {metrics['current_24h_metrics']['liability_protection']['legal_threats_defused']}
• Compliance Documentation: {metrics['current_24h_metrics']['liability_protection']['compliance_documentation_rate']:.0f}%
• Habitability Issues Tracked: {metrics['current_24h_metrics']['liability_protection']['habitability_issues_documented']}

🏠 RETENTION IMPACT
• High-Risk Tenants Identified: {metrics['current_month_metrics']['tenant_retention']['high_risk_tenants_identified']}
• Estimated Turnover Prevented: {metrics['current_month_metrics']['tenant_retention']['estimated_turnover_prevented']} units
• Turnover Cost Avoided: ${metrics['current_month_metrics']['tenant_retention']['turnover_cost_avoided']:,.0f}
        """
    
    def generate_property_manager_view(self, property_id: str) -> Dict:
        """Individual property manager dashboard"""
        
        return {
            "property_id": property_id,
            "timestamp": datetime.now().isoformat(),
            
            "my_workload_impact": {
                "interruptions_prevented_today": 23,
                "focus_time_gained_hours": 2.7,
                "escalations_handled_for_me": 18,
                "tickets_auto_created": 12,
                "maintenance_auto_scheduled": 7
            },
            
            "active_issues": {
                "high_priority_open": 3,
                "willow_monitoring": 8,
                "resolved_today": 31,
                "follow_ups_scheduled": 5
            },
            
            "tenant_health": {
                "at_risk_tenants": [
                    {"unit": "342B", "risk_score": 0.78, "issue": "Repeated HVAC"},
                    {"unit": "516A", "risk_score": 0.65, "issue": "Payment stress"}
                ],
                "satisfaction_trending_up": 67,
                "satisfaction_trending_down": 12
            },
            
            "compliance_alerts": {
                "requires_attention": 1,
                "auto_documented": 42,
                "legal_risk_flagged": 0
            }
        }


# Sample interaction data that shows commercial focus
def show_actual_data_entry():
    """Display what an actual Willow data entry looks like"""
    
    entry = {
        "interaction_id": "INT_20250113_221547_3BF2",
        "property_id": "PROP_CHI_0892",
        "timestamp": "2025-01-13T22:15:47",
        "duration": 423,
        "outcome": "deflected",
        "cost_category": "zero_cost",
        "human_avoided": True,
        "after_hours": True,  # 10:15 PM - would've been $500 emergency call
        "liability_risk": "habitability",
        "retention_risk": 0.23,
        "deflection_success": True,
        "issue_code": "HVAC_01",
        
        # The actual interaction (simplified)
        "interaction_summary": {
            "tenant_initial_state": "Furious, mentioned lawyers, children cold",
            "willow_techniques": ["tier_1_containment", "symbolic_grounding", "capacity_monitoring"],
            "resolution": "Tenant accepted morning appointment, provided space heater location",
            "commitments_tracked": ["First appointment 8am", "Follow-up call by noon"],
            "sentiment_change": [-0.9, -0.2]  # Major de-escalation
        },
        
        # Business value of this single interaction
        "value_generated": {
            "after_hours_callout_avoided": 500.00,
            "property_manager_sleep_protected": True,
            "legal_threat_neutralized": True,
            "tenant_retention_probability_increase": 0.15,
            "compliance_documentation_complete": True
        }
    }
    
    return entry


if __name__ == "__main__":
    dashboard = WillowOperationalDashboard()
    
    # Show executive metrics
    metrics = dashboard.generate_realtime_metrics("PORT_MIDWEST_02")
    print(dashboard.generate_executive_summary(metrics))
    
    # Show single interaction value
    print("\n=== SINGLE INTERACTION VALUE ===")
    entry = show_actual_data_entry()
    print(json.dumps(entry, indent=2))
    
    print(f"\n💵 This one 7-minute interaction saved ${entry['value_generated']['after_hours_callout_avoided']}")
    print("✅ Prevented legal escalation")
    print("😴 Let property manager sleep")
    print("📋 Created perfect compliance record"
    
    # Property manager view
    print("\n=== PROPERTY MANAGER DASHBOARD ===")
    pm_view = dashboard.generate_property_manager_view("PROP_CHI_0892")
    print(f"Today Willow handled {pm_view['my_workload_impact']['escalations_handled_for_me']} angry tenants for you")
    print(f"You gained {pm_view['my_workload_impact']['focus_time_gained_hours']:.1f} hours of focus time")
    print(f"High-risk retention alerts: {len(pm_view['tenant_health']['at_risk_tenants'])}")