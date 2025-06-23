#!/usr/bin/env python3
"""
Generate expansion scenarios to enhance legal liability protection in Willow corpus.
"""

import json
import random
from typing import Dict, List

# Legal liability categories that need coverage
LIABILITY_CATEGORIES = {
    "discrimination_claims": {
        "description": "Avoiding statements that could be construed as discriminatory",
        "risk_level": "critical",
        "scenarios": [
            "tenant_claims_discrimination",
            "fair_housing_violation_accusation",
            "disability_accommodation_denial_claim",
            "familial_status_complaint",
            "religious_discrimination_allegation"
        ]
    },
    "implied_warranties": {
        "description": "Avoiding creation of implied warranties or guarantees",
        "risk_level": "high",
        "scenarios": [
            "habitability_warranty_trap",
            "repair_timeline_guarantee_request",
            "safety_assurance_demand",
            "pest_free_promise_request",
            "quiet_enjoyment_guarantee"
        ]
    },
    "privacy_violations": {
        "description": "Maintaining tenant privacy rights",
        "risk_level": "high",
        "scenarios": [
            "illegal_entry_accusation",
            "surveillance_complaint",
            "information_disclosure_request",
            "neighbor_information_fishing",
            "police_information_request"
        ]
    },
    "retaliation_claims": {
        "description": "Avoiding actions that could be seen as retaliatory",
        "risk_level": "critical",
        "scenarios": [
            "post_complaint_rent_increase",
            "maintenance_request_eviction_threat",
            "code_violation_report_retaliation",
            "organizing_tenants_pushback",
            "legal_action_threat_response"
        ]
    },
    "contractual_modifications": {
        "description": "Avoiding unauthorized lease modifications",
        "risk_level": "high",
        "scenarios": [
            "verbal_lease_change_request",
            "informal_agreement_trap",
            "lease_waiver_request",
            "payment_plan_commitment",
            "amenity_access_promise"
        ]
    },
    "medical_legal_boundaries": {
        "description": "Avoiding medical advice or diagnoses",
        "risk_level": "critical",
        "scenarios": [
            "mental_health_crisis_advice",
            "medication_recommendation_request",
            "disability_verification_demand",
            "wellness_check_boundaries",
            "medical_emergency_guidance"
        ]
    },
    "financial_commitments": {
        "description": "Avoiding unauthorized financial promises",
        "risk_level": "critical",
        "scenarios": [
            "rent_reduction_promise",
            "deposit_return_guarantee",
            "fee_waiver_commitment",
            "payment_extension_terms",
            "financial_hardship_solutions"
        ]
    },
    "third_party_liability": {
        "description": "Avoiding liability for third-party actions",
        "risk_level": "medium",
        "scenarios": [
            "contractor_guarantee_request",
            "neighbor_behavior_responsibility",
            "guest_injury_liability",
            "delivery_damage_claims",
            "utility_company_issues"
        ]
    }
}

# Legal protection phrases that should be used
PROTECTION_PHRASES = {
    "process_transparency": [
        "I'll need to check our current policies",
        "Let me review the standard procedures",
        "I'll document this concern properly",
        "This will go through our normal review process",
        "I'll forward this to the appropriate department"
    ],
    "non_commitment": [
        "We'll explore what options are available",
        "I'll look into what's possible within our policies",
        "Let's see what we can do within regulations",
        "I'll investigate the available resources",
        "We'll review this according to standard procedures"
    ],
    "documentation": [
        "I'll make sure this is properly documented",
        "Please submit this in writing for our records",
        "I'll note this in our system",
        "This will be recorded for follow-up",
        "I'll ensure proper documentation of your concern"
    ],
    "legal_boundaries": [
        "I can provide information but not legal advice",
        "You may want to consult with legal counsel",
        "I can't make that determination myself",
        "That would require authorization I don't have",
        "This falls outside my scope of authority"
    ]
}

def generate_discrimination_scenario(scenario_type: str, id_num: int) -> Dict:
    """Generate a discrimination claim scenario."""
    scenarios = {
        "tenant_claims_discrimination": {
            "tenant_message": "You're discriminating against me because I'm [protected class]. I know my rights!",
            "context": "Tenant believes routine action is discriminatory",
            "arousal": 8.5,
            "capacity": 4.0
        },
        "fair_housing_violation_accusation": {
            "tenant_message": "This is a Fair Housing violation! You can't treat me differently because of my [status].",
            "context": "Tenant citing Fair Housing Act",
            "arousal": 8.8,
            "capacity": 3.8
        },
        "disability_accommodation_denial_claim": {
            "tenant_message": "You're required by law to accommodate my disability. Denying this is illegal!",
            "context": "Accommodation request dispute",
            "arousal": 8.3,
            "capacity": 4.2
        }
    }
    
    scenario_data = scenarios.get(scenario_type, scenarios["tenant_claims_discrimination"])
    
    return {
        "id": f"WILLOW_{id_num}",
        "scenario": scenario_type,
        "category": "discrimination_claims",
        "complexity_level": "critical",
        "initial_state": {
            "arousal": scenario_data["arousal"],
            "capacity": scenario_data["capacity"],
            "issue_type": "legal_liability"
        },
        "messages": [
            {
                "role": "tenant",
                "content": scenario_data["tenant_message"],
                "arousal": scenario_data["arousal"],
                "capacity": scenario_data["capacity"],
                "legal_threat": True
            },
            {
                "role": "willow",
                "content": "I hear your concern about fair treatment. We take these matters seriously. Let me document your specific concern properly so it can be reviewed according to our equal housing policies.",
                "tier": "tier_1",
                "technique": "acknowledge_without_admission",
                "arousal_impact": -0.3,
                "legal_safety": "high"
            },
            {
                "role": "tenant",
                "content": "Don't just document it, fix it! This is discrimination!",
                "arousal": scenario_data["arousal"] - 0.3,
                "capacity": scenario_data["capacity"],
                "escalation": True
            },
            {
                "role": "willow",
                "content": "Your concern about fair treatment is important. I'll ensure this is properly escalated for review. Can you help me understand the specific situation so I can document it accurately?",
                "tier": "tier_1",
                "technique": "redirect_to_facts",
                "arousal_impact": -0.2,
                "legal_safety": "high"
            },
            {
                "role": "tenant",
                "content": "The situation is [specific complaint details]",
                "arousal": scenario_data["arousal"] - 0.5,
                "capacity": scenario_data["capacity"] + 0.2,
                "providing_details": True
            },
            {
                "role": "willow",
                "content": "Thank you for those details. I'm documenting: 1) Your specific concern 2) The timeline of events 3) Your requested resolution. This will be reviewed by the appropriate team who can properly assess the situation within our policies and regulations.",
                "tier": "tier_2",
                "resolution_type": "proper_escalation",
                "delivery_certainty": "process_based",
                "legal_safety": "maximum"
            }
        ],
        "legal_protection_elements": [
            "no_admission_of_wrongdoing",
            "proper_documentation",
            "appropriate_escalation",
            "policy_based_response"
        ]
    }

def generate_implied_warranty_scenario(scenario_type: str, id_num: int) -> Dict:
    """Generate implied warranty trap scenarios."""
    scenarios = {
        "habitability_warranty_trap": {
            "tenant_message": "Can you guarantee this apartment will always be habitable and safe?",
            "context": "Seeking blanket habitability guarantee",
            "arousal": 6.5,
            "capacity": 5.5
        },
        "repair_timeline_guarantee_request": {
            "tenant_message": "I need you to promise this will be fixed within 24 hours. Can you guarantee that?",
            "context": "Pushing for specific timeline commitment",
            "arousal": 7.8,
            "capacity": 4.8
        }
    }
    
    scenario_data = scenarios.get(scenario_type, scenarios["habitability_warranty_trap"])
    
    return {
        "id": f"WILLOW_{id_num}",
        "scenario": scenario_type,
        "category": "implied_warranties",
        "complexity_level": "high",
        "initial_state": {
            "arousal": scenario_data["arousal"],
            "capacity": scenario_data["capacity"],
            "issue_type": "legal_trap"
        },
        "messages": [
            {
                "role": "tenant",
                "content": scenario_data["tenant_message"],
                "arousal": scenario_data["arousal"],
                "capacity": scenario_data["capacity"],
                "seeking_guarantee": True
            },
            {
                "role": "willow",
                "content": "I understand you want certainty about this. While I can't make guarantees, I can share that we follow all required maintenance standards and respond to issues according to our established procedures.",
                "tier": "tier_1",
                "technique": "deflect_guarantee_request",
                "arousal_impact": -0.2,
                "legal_safety": "high"
            },
            {
                "role": "tenant",
                "content": "That's not good enough. I need a guarantee!",
                "arousal": scenario_data["arousal"] + 0.3,
                "capacity": scenario_data["capacity"] - 0.2,
                "pushing_harder": True
            },
            {
                "role": "willow",
                "content": "I hear that you need certainty about this situation. What I can do is document your specific concerns and ensure they're addressed through our standard procedures. This helps protect everyone's interests.",
                "tier": "tier_1",
                "technique": "acknowledge_need_redirect",
                "arousal_impact": -0.3,
                "legal_safety": "high"
            },
            {
                "role": "tenant",
                "content": "Fine, but what exactly will you do?",
                "arousal": scenario_data["arousal"],
                "capacity": scenario_data["capacity"],
                "accepting_redirect": True
            },
            {
                "role": "willow",
                "content": "Here's our process: 1) I'll document your concern today 2) It will be reviewed by maintenance within standard timeframes 3) You'll receive updates as work progresses 4) All work follows code requirements. This systematic approach helps ensure proper resolution.",
                "tier": "tier_2",
                "resolution_type": "process_explanation",
                "delivery_certainty": "process_based",
                "legal_safety": "maximum"
            }
        ],
        "legal_protection_elements": [
            "no_guarantees_made",
            "process_focus",
            "standard_procedures_referenced",
            "mutual_benefit_framing"
        ]
    }

def generate_privacy_scenario(scenario_type: str, id_num: int) -> Dict:
    """Generate privacy protection scenarios."""
    scenarios = {
        "neighbor_information_fishing": {
            "tenant_message": "My neighbor in 3B seems suspicious. What can you tell me about them? Any criminal history?",
            "context": "Fishing for private tenant information",
            "arousal": 5.5,
            "capacity": 6.5
        },
        "police_information_request": {
            "tenant_message": "The police are asking about my neighbor. What should I tell them? What do you know?",
            "context": "Third party information request",
            "arousal": 7.0,
            "capacity": 5.0
        }
    }
    
    scenario_data = scenarios.get(scenario_type, scenarios["neighbor_information_fishing"])
    
    return {
        "id": f"WILLOW_{id_num}",
        "scenario": scenario_type,
        "category": "privacy_violations",
        "complexity_level": "high",
        "initial_state": {
            "arousal": scenario_data["arousal"],
            "capacity": scenario_data["capacity"],
            "issue_type": "privacy_boundary"
        },
        "messages": [
            {
                "role": "tenant",
                "content": scenario_data["tenant_message"],
                "arousal": scenario_data["arousal"],
                "capacity": scenario_data["capacity"],
                "information_seeking": True
            },
            {
                "role": "willow",
                "content": "I understand your concern. For privacy reasons, I can't share information about other tenants. If you have safety concerns, I can help you report them through proper channels.",
                "tier": "tier_1",
                "technique": "privacy_boundary",
                "arousal_impact": -0.1,
                "legal_safety": "maximum"
            },
            {
                "role": "tenant",
                "content": "But I have a right to know if I'm safe!",
                "arousal": scenario_data["arousal"] + 0.5,
                "capacity": scenario_data["capacity"] - 0.3,
                "pushing_boundary": True
            },
            {
                "role": "willow",
                "content": "Your safety is absolutely important. While I can't share private information, I can: 1) Document any specific safety concerns you have 2) Provide information about building security features 3) Connect you with appropriate resources if needed.",
                "tier": "tier_2",
                "technique": "redirect_to_appropriate_help",
                "arousal_impact": -0.3,
                "legal_safety": "maximum"
            }
        ],
        "legal_protection_elements": [
            "privacy_protection_maintained",
            "no_information_disclosed",
            "appropriate_alternatives_offered",
            "safety_acknowledged_without_breach"
        ]
    }

def generate_expansion_entry(category: str, scenario: str, id_num: int) -> Dict:
    """Generate a single expansion entry based on category."""
    if category == "discrimination_claims":
        return generate_discrimination_scenario(scenario, id_num)
    elif category == "implied_warranties":
        return generate_implied_warranty_scenario(scenario, id_num)
    elif category == "privacy_violations":
        return generate_privacy_scenario(scenario, id_num)
    # Add more category handlers as needed
    else:
        # Default structure for other categories
        return {
            "id": f"WILLOW_{id_num}",
            "scenario": scenario,
            "category": category,
            "complexity_level": "high",
            "initial_state": {
                "arousal": 7.0,
                "capacity": 5.0,
                "issue_type": "legal_liability"
            },
            "messages": [
                {
                    "role": "tenant",
                    "content": f"[Scenario content for {scenario}]",
                    "arousal": 7.0,
                    "capacity": 5.0
                },
                {
                    "role": "willow",
                    "content": "I understand your concern. Let me address this within our policies and procedures.",
                    "tier": "tier_1",
                    "technique": "acknowledge_with_boundaries",
                    "arousal_impact": -0.3,
                    "legal_safety": "high"
                }
            ],
            "legal_protection_elements": ["placeholder"]
        }

def main():
    print("Generating legal liability protection expansion scenarios...")
    
    expansion_entries = []
    id_counter = 2000  # Starting ID for expansion entries
    
    # Generate entries for each category
    for category, details in LIABILITY_CATEGORIES.items():
        print(f"\nGenerating {category} scenarios...")
        
        for scenario in details["scenarios"][:3]:  # Generate 3 per category for now
            entry = generate_expansion_entry(category, scenario, id_counter)
            expansion_entries.append(entry)
            id_counter += 1
    
    # Save expansion entries
    output_file = "willow_legal_liability_expansion.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in expansion_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\nGenerated {len(expansion_entries)} legal liability protection scenarios")
    print(f"Saved to: {output_file}")
    
    # Create summary report
    summary = {
        "total_scenarios": len(expansion_entries),
        "categories_covered": list(LIABILITY_CATEGORIES.keys()),
        "protection_elements": {
            "no_admission_of_wrongdoing": "Never admit fault or liability",
            "proper_documentation": "Document everything properly",
            "appropriate_escalation": "Escalate to proper authority",
            "policy_based_response": "Reference policies and procedures",
            "privacy_protection": "Never disclose private information",
            "no_guarantees": "Avoid making specific promises",
            "process_focus": "Focus on process not outcomes",
            "boundary_maintenance": "Maintain professional boundaries"
        }
    }
    
    with open("legal_liability_expansion_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nKey legal protection strategies implemented:")
    for key, value in summary["protection_elements"].items():
        print(f"  - {key}: {value}")

if __name__ == "__main__":
    main()