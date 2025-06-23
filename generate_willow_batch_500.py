#!/usr/bin/env python3
"""
Generate 500 diverse Willow dataset entries using enhanced tools
Organized into 20 thematic batches of 25 entries each
"""

import json
import random
from typing import Dict, List, Tuple
from willow_dataset_generator import WillowGenerator
from willow_response_library import WillowResponseLibrary

class WillowBatchGenerator:
    """Generates large batches of Willow entries efficiently."""
    
    def __init__(self, starting_id: int = 1394):
        self.generator = WillowGenerator(starting_id=starting_id)
        self.library = WillowResponseLibrary()
        self.entries_generated = 0
        
    def generate_scenario_variations(self, base_scenario: Dict, variations: List[Dict], count: int = 5) -> List[Dict]:
        """Generate variations of a base scenario."""
        scenarios = []
        
        for i in range(count):
            var = variations[i % len(variations)]
            scenario = base_scenario.copy()
            scenario.update(var)
            
            # Add unique identifier
            scenario["name"] = f"{base_scenario['name']}_{i+1}"
            
            # Vary arousal/capacity slightly
            scenario["arousal"] = base_scenario["arousal"] + random.uniform(-0.3, 0.3)
            scenario["capacity"] = base_scenario["capacity"] + random.uniform(-0.2, 0.2)
            
            # Ensure within bounds
            scenario["arousal"] = max(5.0, min(9.0, scenario["arousal"]))
            scenario["capacity"] = max(3.0, min(6.0, scenario["capacity"]))
            
            scenarios.append(scenario)
            
        return scenarios
    
    def generate_batch(self, theme_name: str, scenarios: List[Dict]) -> List[Dict]:
        """Generate a batch of entries for a theme."""
        batch = []
        
        for scenario_data in scenarios:
            # Generate tier 1 response
            tier1_response = self.library.build_complete_response(
                tier="tier_1",
                crisis_type=self._infer_crisis_type(scenario_data["category"]),
                specific_context=scenario_data.get("context", {}),
                trauma_type=self._infer_trauma_type(scenario_data.get("issue_type", "multiple_barriers")),
                symbolic_type="traditional" if scenario_data.get("complexity", "high") == "critical" else "minimal"
            )
            
            # Generate tier 2 response with appropriate resources
            resource_info, action_steps = self._generate_resources_for_scenario(scenario_data)
            
            tier2_response = self.library.build_complete_response(
                tier="tier_2",
                crisis_type=self._infer_crisis_type(scenario_data["category"]),
                specific_context=scenario_data.get("context", {}),
                resource_info=resource_info,
                action_steps=action_steps,
                symbolic_type="minimal"
            )
            
            # Create entry
            entry = self.generator.generate_entry(
                scenario_name=f"{theme_name}_{scenario_data['name']}",
                category=scenario_data["category"],
                complexity=scenario_data.get("complexity", "high"),
                issue_type=scenario_data.get("issue_type", "multiple_barriers"),
                tenant_message1=scenario_data["messages"][0],
                willow_response1=tier1_response,
                tenant_message2=scenario_data["messages"][1],
                willow_response2=tier2_response,
                initial_arousal=scenario_data.get("arousal", 8.0),
                initial_capacity=scenario_data.get("capacity", 3.5),
                tier1_technique=self._select_technique_for_scenario(scenario_data, "tier1"),
                tier2_technique=self._select_technique_for_scenario(scenario_data, "tier2"),
                arousal_impacts=(-1.2, -0.8) if scenario_data.get("complexity", "high") == "critical" else (-1.0, -0.6),
                resolution_status=self._determine_resolution_status(scenario_data),
                escalation_path=self._determine_escalation_path(scenario_data)
            )
            
            batch.append(entry)
            self.entries_generated += 1
            
        return batch
    
    def _infer_crisis_type(self, category: str) -> str:
        """Map category to crisis type for response library."""
        mapping = {
            "maintenance_crisis": "maintenance_emergency",
            "eviction": "financial_crisis",
            "health_safety": "medical_emergency",
            "discrimination": "discrimination",
            "financial_distress": "financial_crisis",
            "intersectional_vulnerability": "family_crisis",
            "legal_notice": "family_crisis",
            "boundary_crisis": "family_crisis",
            "complex_grievance": "financial_crisis"
        }
        return mapping.get(category, "financial_crisis")
    
    def _infer_trauma_type(self, issue_type: str) -> str:
        """Map issue type to trauma type."""
        mapping = {
            "multiple_barriers": "compound_trauma",
            "financial_instability": "systemic_abandonment",
            "safety_threat": "chronic_crisis",
            "emotional_overload": "identity_violence"
        }
        return mapping.get(issue_type, "systemic_abandonment")
    
    def _generate_resources_for_scenario(self, scenario: Dict) -> tuple:
        """Generate appropriate resources and action steps for scenario."""
        
        # Enhanced resource mapping
        resource_map = {
            "eviction": {
                "type": "legal_support",
                "specific_org": random.choice(["Housing Justice Project", "Eviction Defense Coalition", "Tenant Legal Aid"]),
                "specific_issue": "eviction defense",
                "similar_situation": random.choice(["emergency evictions", "COVID-related evictions", "retaliatory evictions"]),
                "contact": random.choice(["1-800-EVICTION", "evictionhelp.org", "211"])
            },
            "discrimination": {
                "type": "legal_support",
                "specific_org": random.choice(["Fair Housing Center", "Civil Rights Coalition", "Equal Housing Alliance"]),
                "specific_issue": "housing discrimination",
                "similar_situation": "identity-based harassment",
                "contact": "fairhousing.org/emergency"
            },
            "health_safety": {
                "type": "medical_advocacy",
                "Medical_legal_org": "Health Justice Alliance",
                "medical_condition": "your condition",
                "disability_org": random.choice(["Disability Rights Center", "Independent Living Center", "Accessibility Coalition"]),
                "health_issue": "medical needs",
                "Health_justice_org": "Medical-Legal Partnership"
            },
            "financial_distress": {
                "type": "emergency_assistance",
                "need": random.choice(["rent assistance", "utility assistance", "emergency funds"]),
                "organization": random.choice(["Emergency Rental Assistance", "Community Action Agency", "United Way"]),
                "timeframe": random.choice(["48-72 hours", "3-5 business days", "within a week"]),
                "specific_help": random.choice(["one-time payment", "ongoing assistance", "emergency grant"]),
                "contact": random.choice(["211", "renthelp.org", "local resource hotline"])
            },
            "maintenance_crisis": {
                "type": "emergency_assistance",
                "need": "emergency repairs",
                "organization": "Code Enforcement Hotline",
                "timeframe": "24-48 hours for emergency issues",
                "specific_help": "inspection and enforcement",
                "contact": "311 or housing inspection department"
            }
        }
        
        # Enhanced action mapping
        action_map = {
            "eviction": {
                "type": "rights_assertion",
                "specific_right": random.choice(["proper notice and court process", "right to cure", "habitability defense"]),
                "law/code": random.choice(["state tenant protection laws", "local rent ordinance", "federal fair housing law"]),
                "their_action": "attempting illegal eviction"
            },
            "discrimination": {
                "type": "documentation",
                "condition": "discrimination",
                "communication": "all discriminatory statements",
                "events": "each incident with dates and witnesses",
                "pattern": "the ongoing discrimination",
                "evidence": "all harassment and differential treatment"
            },
            "maintenance_crisis": {
                "type": "staged_approach",
                "immediate_action": random.choice(["document all conditions", "notify landlord in writing", "contact emergency services"]),
                "medium_action": random.choice(["formal repair request", "code inspection request", "tenant union involvement"]),
                "long_action": random.choice(["rent escrow action", "repair and deduct", "constructive eviction claim"])
            },
            "health_safety": {
                "type": "staged_approach",
                "immediate_action": "secure immediate safety",
                "medium_action": "medical documentation",
                "long_action": "accommodation request or relocation"
            },
            "financial_distress": {
                "type": "rights_assertion",
                "specific_right": "payment plan options",
                "law/code": "emergency assistance programs",
                "their_action": "refusing reasonable accommodations"
            }
        }
        
        category = scenario.get("category", "financial_distress")
        resource_info = resource_map.get(category, resource_map["financial_distress"]).copy()
        action_steps = action_map.get(category, action_map["eviction"]).copy()
        
        return resource_info, action_steps
    
    def _select_technique_for_scenario(self, scenario: Dict, tier: str) -> str:
        """Select appropriate technique based on scenario."""
        
        if tier == "tier1":
            technique_map = {
                "maintenance_crisis": ["dual_danger_recognition", "bureaucratic_harm_naming", "dignity_validation"],
                "eviction": ["system_abandonment_naming", "medical_injustice_witnessing", "disaster_timeline_validation"],
                "discrimination": ["identity_affirmation", "discrimination_timing_reveal", "transformation_invisibility_naming"],
                "health_safety": ["medical_injustice_witnessing", "dual_danger_recognition", "disaster_timeline_validation"],
                "financial_distress": ["system_abandonment_naming", "bureaucratic_harm_naming", "separation_grief_holding"],
                "intersectional_vulnerability": ["separation_grief_holding", "paradox_witnessing", "generational_burden_witnessing"],
                "legal_notice": ["bureaucratic_harm_naming", "system_abandonment_naming", "dual_danger_recognition"],
                "boundary_crisis": ["dignity_validation", "grief_space_honoring", "covert_strength_recognition"],
                "complex_grievance": ["compound_trauma_recognition", "systemic_violence_naming", "resistance_honoring"]
            }
        else:  # tier2
            technique_map = {
                "maintenance_crisis": ["evidence_building", "rights_reinforcement", "multi_pathway_support"],
                "eviction": ["medical_legal_support", "multi_pathway_support", "disaster_resource_bridging"],
                "discrimination": ["fair_housing_enforcement", "community_resource_mapping", "coded_discrimination_decoding"],
                "health_safety": ["medical_legal_support", "safety_pathway_mapping", "specialized_intervention_pathway"],
                "financial_distress": ["multi_pathway_support", "benefits_legal_intersection", "disaster_resource_bridging"],
                "intersectional_vulnerability": ["family_preservation_support", "immigration_crisis_resources", "multi_pathway_support"],
                "legal_notice": ["rights_reinforcement", "evidence_building", "multi_pathway_support"],
                "boundary_crisis": ["protected_pathway_mapping", "alternative_pathway_mapping", "community_resource_mapping"],
                "complex_grievance": ["collective_resistance_building", "multi_system_navigation", "transformative_justice_pathways"]
            }
        
        category = scenario.get("category", "financial_distress")
        techniques = technique_map.get(category, ["general_validation"])
        return random.choice(techniques)
    
    def _determine_resolution_status(self, scenario: Dict) -> str:
        """Determine resolution status based on scenario."""
        status_map = {
            "critical": ["defending", "protecting", "stabilizing"],
            "high": ["supporting", "planning", "organizing"],
            "medium": ["redirecting", "planning", "supporting"]
        }
        
        complexity = scenario.get("complexity", "high")
        statuses = status_map.get(complexity, ["supporting"])
        return random.choice(statuses)
    
    def _determine_escalation_path(self, scenario: Dict) -> str:
        """Determine escalation path based on scenario."""
        path_map = {
            "eviction": random.choice(["legal_aid_referral", "eviction_defense_attorney", "tenant_union_support"]),
            "discrimination": random.choice(["fair_housing_enforcement", "civil_rights_complaint", "discrimination_lawsuit"]),
            "maintenance_crisis": random.choice(["code_enforcement", "emergency_repair_order", "habitability_lawsuit"]),
            "health_safety": random.choice(["emergency_services", "APS_referral", "medical_advocacy"]),
            "financial_distress": ["emergency_assistance", "benefits_advocacy", "debt_counseling"],
            "intersectional_vulnerability": "multi_system_advocacy",
            "legal_notice": "legal_consultation",
            "boundary_crisis": "crisis_intervention",
            "complex_grievance": "systemic_advocacy"
        }
        
        category = scenario.get("category", "financial_distress")
        if isinstance(path_map.get(category), list):
            return path_map[category]
        return path_map.get(category, "crisis_support")


def generate_500_entries():
    """Generate 500 entries across 20 themes."""
    
    batch_gen = WillowBatchGenerator(starting_id=1394)
    all_entries = []
    
    # Define 20 themes with 25 entries each
    themes = [
        # Theme 1: Pandemic Aftermath (25 entries)
        {
            "name": "pandemic_aftermath",
            "base_scenarios": [
                {
                    "name": "long_covid_eviction",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Long COVID, can't work full time anymore. Behind 4 months, eviction court tomorrow",
                        "Disability claim denied, say I'm not sick enough. But I can't breathe after 2 hours work"
                    ],
                    "context": {
                        "Medical_condition": "Long COVID",
                        "housing_crisis": "eviction",
                        "duration": "four months"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "pandemic_job_loss",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Restaurant never reopened after COVID. Unemployment ran out, savings gone",
                        "52 years old, no one hiring. Rent due in 3 days, already got pay or quit notice"
                    ],
                    "context": {
                        "need1": "rent",
                        "need2": "employment",
                        "Time_period": "Two years"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "remote_work_ended",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Company ending remote work but I moved home to care for mom during COVID. Can't abandon her",
                        "Choose between job and mom's care. Either way, lose housing. Impossible choice"
                    ],
                    "context": {
                        "family_member": "elderly mother",
                        "need1": "employment",
                        "need2": "caregiving"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "covid_medical_debt",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Hospitalized with COVID last year, $80k in debt. They're garnishing wages, can't pay rent",
                        "Survived COVID to face financial death. Collection calls all day, eviction notice yesterday"
                    ],
                    "context": {
                        "Medical_condition": "COVID recovery",
                        "new_crisis": "medical debt",
                        "need1": "rent",
                        "need2": "debt relief"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "school_closure_childcare",
                    "category": "intersectional_vulnerability",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Kids' school keeps closing for COVID outbreaks. Missing work for childcare, job threatened",
                        "Single mom, no backup care. Boss says one more absence and I'm fired. Then what?"
                    ],
                    "context": {
                        "vulnerable_person": "children",
                        "need1": "childcare",
                        "need2": "job security"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                }
            ]
        },
        
        # Theme 2: Extreme Weather Events (25 entries)
        {
            "name": "extreme_weather",
            "base_scenarios": [
                {
                    "name": "heat_dome_elderly",
                    "category": "health_safety",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Heat dome, 115 degrees, no AC. Landlord says not required. Neighbor died yesterday",
                        "Heart meds make heat dangerous. ER said don't go outside but inside is an oven"
                    ],
                    "context": {
                        "Medical_condition": "heart condition",
                        "Specific_hazard": "extreme heat",
                        "duration": "this heat dome"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "flooding_repeat",
                    "category": "maintenance_crisis",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Third flood this year. Landlord just paints over mold. Kids sick constantly",
                        "Insurance won't cover 'repeat flooding'. Everything we own destroyed again"
                    ],
                    "context": {
                        "Duration": "Third time this year",
                        "basic_need": "safe housing",
                        "Specific_hazard": "toxic mold"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "tornado_damage",
                    "category": "legal_notice",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Tornado damaged roof 2 months ago. Landlord took insurance money but no repairs",
                        "Rain pouring in, ceiling collapsing. He says act of God, not his problem"
                    ],
                    "context": {
                        "housing_issue": "storm damage",
                        "system": "insurance fraud",
                        "duration": "two months"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "wildfire_evacuation",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Evacuated for wildfire, landlord still demanding rent. Lost job when workplace burned",
                        "Living in car with kids, he's threatening to throw out our stuff if we don't pay"
                    ],
                    "context": {
                        "new_crisis": "wildfire displacement",
                        "vulnerable_person": "children",
                        "need1": "shelter",
                        "need2": "belongings preservation"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                },
                {
                    "name": "freeze_burst_pipes",
                    "category": "maintenance_crisis",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Polar vortex, pipes burst everywhere. No water 5 days, toilets backing up",
                        "Landlord in Florida says wait for spring. It's 10 below and we're using buckets"
                    ],
                    "context": {
                        "Duration": "Five days",
                        "basic_need": "water and sanitation",
                        "Specific_hazard": "freezing temperatures"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                }
            ]
        },
        
        # Theme 3: Gig Economy Struggles (25 entries)
        {
            "name": "gig_economy",
            "base_scenarios": [
                {
                    "name": "rideshare_car_breakdown",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Car broke down, only income was Uber. Need $2000 for repairs, rent due tomorrow",
                        "No car means no work means no home. Spiral starting, can't stop it"
                    ],
                    "context": {
                        "need1": "car repairs",
                        "need2": "rent",
                        "new_crisis": "income loss"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "delivery_injury",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Hurt back doing DoorDash, no workers comp for contractors. Can't lift, can't work",
                        "Company says I'm not employee. Landlord doesn't care about my back. Rent still due"
                    ],
                    "context": {
                        "Medical_condition": "back injury",
                        "need1": "rent",
                        "need2": "medical care"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "platform_deactivation",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Instacart deactivated me, no reason given. That was 70% of income, rent due next week",
                        "No appeal process, just cut off. Years of 5-star reviews mean nothing"
                    ],
                    "context": {
                        "new_crisis": "platform deactivation",
                        "need1": "income replacement",
                        "need2": "rent"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "multiple_apps_juggle",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "emotional_overload",
                    "messages": [
                        "Working 5 apps, 14 hours a day, still can't make rent. Gas prices killing me",
                        "Haven't seen kids awake in weeks. Working myself to death for poverty wages"
                    ],
                    "context": {
                        "need1": "sustainable income",
                        "need2": "family time",
                        "duration": "weeks"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "tax_surprise_1099",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "First year gig work, owe $4000 in taxes. No one told me to save. IRS threatening levy",
                        "Thought I was making $15/hour, after taxes and gas it's $6. Now losing apartment too"
                    ],
                    "context": {
                        "new_crisis": "tax debt",
                        "need1": "tax payment",
                        "need2": "rent",
                        "Time_period": "First year"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                }
            ]
        },
        
        # Theme 4: Mental Health Crisis Intersection (25 entries)
        {
            "name": "mental_health_crisis",
            "base_scenarios": [
                {
                    "name": "bipolar_job_loss",
                    "category": "discrimination",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Had manic episode at work, fired immediately. They knew I was bipolar, didn't care",
                        "Medication costs $400/month without job insurance. Rent or sanity, can't afford both"
                    ],
                    "context": {
                        "identity": "bipolar disorder",
                        "Medical_condition": "bipolar disorder",
                        "discriminatory_act": "firing for disability"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "depression_maintenance",
                    "category": "eviction",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Depression so bad couldn't clean. Landlord says I'm hoarder, evicting for health hazard",
                        "Not hoarding, just can't function. Therapist letter ignored. Losing only safe space"
                    ],
                    "context": {
                        "Medical_condition": "severe depression",
                        "housing_issue": "cleanliness standards",
                        "identity_aspect": "mental illness"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "anxiety_inspection_panic",
                    "category": "boundary_crisis",
                    "complexity": "high",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Severe anxiety, landlord demands monthly inspections. Have panic attacks for days before",
                        "Asked for accommodation, he laughed. Says I'm too sensitive for apartment living"
                    ],
                    "context": {
                        "Medical_condition": "severe anxiety",
                        "identity": "anxiety disorder",
                        "Specific_hazard": "forced inspections"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "suicide_attempt_eviction",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Attempted suicide, ambulance came. Landlord found out, says I'm liability, wants me out",
                        "Survived to face homelessness. How does losing housing help mental health?"
                    ],
                    "context": {
                        "Medical_condition": "suicidal ideation",
                        "discriminatory_act": "eviction for mental health crisis",
                        "identity_aspect": "suicide attempt survivor"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "schizophrenia_neighbors",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Neighbors found out I have schizophrenia, petition to evict me. I take meds, never bothered anyone",
                        "20 years stable, good tenant. One word - schizophrenia - and suddenly I'm dangerous"
                    ],
                    "context": {
                        "identity": "schizophrenia",
                        "discriminatory_act": "neighbor harassment",
                        "Time_period": "Twenty years"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                }
            ]
        },
        
        # Theme 5: Criminal Justice Impact (25 entries)
        {
            "name": "criminal_justice",
            "base_scenarios": [
                {
                    "name": "felony_housing_denial",
                    "category": "discrimination",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "10 year old felony, paid my debt. Every apartment runs check, instant denial",
                        "Living in car with daughter. She asks why we can't have home. What do I say?"
                    ],
                    "context": {
                        "identity": "person with record",
                        "discriminatory_act": "blanket ban",
                        "vulnerable_person": "daughter"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "parole_address_requirement",
                    "category": "legal_notice",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Parole needs stable address or back to prison. No one rents to parolees",
                        "30 days to find housing or violated. System sets us up to fail"
                    ],
                    "context": {
                        "identity": "parolee",
                        "housing_issue": "address requirement",
                        "Time_period": "30 days"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "arrest_job_loss",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Arrested at protest, charges dropped but lost job. Behind on rent now",
                        "Exercised free speech, paying with homelessness. Democracy has a price"
                    ],
                    "context": {
                        "new_crisis": "wrongful job loss",
                        "need1": "rent",
                        "need2": "legal vindication"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "prison_medical_debt",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Got cancer in prison, they billed me $50k for treatment. Now free but financially imprisoned",
                        "Survived prison and cancer to face eviction. Medical debt from incarceration destroying me"
                    ],
                    "context": {
                        "Medical_condition": "cancer survivor",
                        "new_crisis": "prison medical debt",
                        "identity": "formerly incarcerated"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "sex_offender_nowhere",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "On registry for consensual teen relationship 20 years ago. Can't live anywhere",
                        "Every place is near school or park. Literally nowhere legal to live"
                    ],
                    "context": {
                        "identity": "registrant",
                        "discriminatory_act": "residence restrictions",
                        "Time_period": "Twenty years"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                }
            ]
        },
        
        # Theme 6: Technology Barriers (25 entries)
        {
            "name": "tech_barriers",
            "base_scenarios": [
                {
                    "name": "digital_only_rent",
                    "category": "boundary_crisis",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Landlord only accepts rent through app. I don't have smartphone or internet",
                        "Tried to pay cash, refused. Now late fee because I can't use their app"
                    ],
                    "context": {
                        "housing_issue": "digital payment requirement",
                        "identity": "digitally excluded"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "internet_work_requirement",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Need internet for remote job but can't afford it. Losing job means losing apartment",
                        "Using McDonald's wifi but they kick me out. Employer threatening termination"
                    ],
                    "context": {
                        "need1": "internet access",
                        "need2": "job retention"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "smartphone_assistance_apps",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "All assistance programs require smartphone apps. Phone broke, can't apply for help",
                        "Food stamps, rent help, everything needs app. No phone means no aid"
                    ],
                    "context": {
                        "new_crisis": "digital exclusion",
                        "need1": "phone replacement",
                        "need2": "assistance access"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "elderly_portal_confusion",
                    "category": "eviction",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "75 years old, they say pay through portal. Don't understand computers, missed payments",
                        "Daughter tried to help but lives far away. Now eviction for 'non-payment'"
                    ],
                    "context": {
                        "identity": "elderly tenant",
                        "housing_issue": "digital payment barriers",
                        "duration": "ongoing confusion"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "cyber_scam_rent",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Scammer posed as landlord online, stole rent money. Real landlord wants payment",
                        "Lost $1500 to fake site. Police say civil matter. Facing eviction for paying wrong person"
                    ],
                    "context": {
                        "new_crisis": "cyber scam",
                        "need1": "rent replacement",
                        "need2": "scam recovery"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                }
            ]
        },
        
        # Theme 7: Disability Access Failures (25 entries)
        {
            "name": "disability_access",
            "base_scenarios": [
                {
                    "name": "wheelchair_bathroom",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Wheelchair can't fit in bathroom. Having accidents, landlord says not his problem",
                        "Destroying my dignity daily. ADA means nothing if no one enforces it"
                    ],
                    "context": {
                        "identity": "wheelchair user",
                        "discriminatory_act": "refusing modifications",
                        "basic_need": "bathroom access"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "autism_noise_sensitivity",
                    "category": "boundary_crisis",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Autistic, need quiet. New neighbors party nightly. Meltdowns affecting work",
                        "Asked landlord for help, says I'm too sensitive. Losing job from exhaustion"
                    ],
                    "context": {
                        "identity": "autistic person",
                        "Medical_condition": "autism",
                        "Specific_hazard": "noise sensitivity"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "visual_impairment_notices",
                    "category": "legal_notice",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Legally blind, keep missing important notices. They tape papers to door, I can't read them",
                        "Missed court date I didn't know about. Default eviction judgment"
                    ],
                    "context": {
                        "identity": "visually impaired",
                        "housing_issue": "inaccessible notices",
                        "discriminatory_act": "failure to accommodate"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "chronic_pain_stairs",
                    "category": "health_safety",
                    "complexity": "high",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Chronic pain, can't do stairs anymore. Landlord won't let me transfer to first floor",
                        "Trapped upstairs for days when pain bad. Missing medical appointments"
                    ],
                    "context": {
                        "Medical_condition": "chronic pain",
                        "Specific_hazard": "stair access",
                        "basic_need": "accessible unit"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "seizure_disorder_alone",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Have seizures, landlord says I can't live alone. But I've managed for years",
                        "Threatening eviction for 'safety'. My independence isn't his choice"
                    ],
                    "context": {
                        "Medical_condition": "seizure disorder",
                        "discriminatory_act": "paternalistic eviction",
                        "identity_aspect": "epilepsy"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                }
            ]
        },
        
        # Theme 8: Family Court Intersections (25 entries)
        {
            "name": "family_court",
            "base_scenarios": [
                {
                    "name": "custody_housing_standard",
                    "category": "legal_notice",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Ex saying apartment too small for overnight visits. Judge threatening to reduce custody",
                        "Can't afford bigger place on child support I pay. Losing home means losing kids"
                    ],
                    "context": {
                        "family_member": "children",
                        "housing_issue": "size requirements",
                        "system": "family court"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "support_payment_rent",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Child support takes 60% of check. Love my kids but can't afford place to see them",
                        "Living in car to pay support. Ex won't let kids visit 'homeless' parent"
                    ],
                    "context": {
                        "need1": "affordable housing",
                        "need2": "visitation rights",
                        "family_member": "children"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "dv_cross_allegations",
                    "category": "legal_notice",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Fled DV, he filed false charges. Now I look like abuser, losing custody and housing",
                        "Landlord got subpoena, wants me out. Abuser winning by lying"
                    ],
                    "context": {
                        "identity": "DV survivor",
                        "housing_issue": "false allegations",
                        "system": "family court"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "grandparent_guardianship",
                    "category": "intersectional_vulnerability",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Raising grandkids, daughter in addiction. Landlord says lease only allows one person",
                        "70 years old, starting over with 3 kids. Threatened with eviction for saving them"
                    ],
                    "context": {
                        "vulnerable_person": "grandchildren",
                        "family_member": "grandchildren",
                        "housing_issue": "occupancy limits"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "foster_reunification",
                    "category": "boundary_crisis",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Getting kids back from foster care but need 3 bedroom. Can't afford it on one income",
                        "6 months to find adequate housing or lose them forever. Impossible timeline"
                    ],
                    "context": {
                        "family_member": "children in foster care",
                        "housing_issue": "reunification requirements",
                        "Time_period": "Six months"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                }
            ]
        },
        
        # Theme 9: Healthcare Worker Crisis (25 entries)
        {
            "name": "healthcare_worker",
            "base_scenarios": [
                {
                    "name": "nurse_burnout_eviction",
                    "category": "eviction",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "ICU nurse, worked whole pandemic. Burned out, took leave, now can't pay rent",
                        "Saved lives for 3 years, no one saving mine. Eviction notice yesterday"
                    ],
                    "context": {
                        "identity": "healthcare worker",
                        "Medical_condition": "burnout",
                        "duration": "three years"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "emt_injury_workers_comp",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Hurt back lifting patient, workers comp denied. Can't work, can't pay rent",
                        "Gave my body to save others, system won't save me. Facing homelessness"
                    ],
                    "context": {
                        "Medical_condition": "work injury",
                        "identity": "EMT",
                        "need1": "workers comp",
                        "need2": "rent"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "home_health_aide_transport",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Home health aide, car died. Can't reach clients, losing income fast",
                        "Help elderly stay housed but can't keep my own housing. Irony hurts"
                    ],
                    "context": {
                        "identity": "home care worker",
                        "need1": "transportation",
                        "need2": "income stability"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "resident_physician_debt",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Medical resident, $300k in loans. Work 80 hours for poverty wages, can't afford rent",
                        "Saving lives while drowning in debt. 4 years till real salary, eviction now"
                    ],
                    "context": {
                        "identity": "medical resident",
                        "new_crisis": "student loan burden",
                        "Time_period": "Four years"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "covid_unit_ptsd",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "PTSD from COVID unit, neighbors complain about nightmares. Landlord wants me out",
                        "Watched hundreds die, now punished for trauma. Heroes to zeros real quick"
                    ],
                    "context": {
                        "Medical_condition": "PTSD",
                        "identity": "COVID nurse",
                        "discriminatory_act": "trauma discrimination"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                }
            ]
        },
        
        # Theme 10: Rural Housing Crisis (25 entries)
        {
            "name": "rural_housing",
            "base_scenarios": [
                {
                    "name": "farm_worker_seasonal",
                    "category": "eviction",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Picking season ended, no work till spring. Landlord won't wait for rent",
                        "Fed this country all summer, now facing winter homeless. Where's justice?"
                    ],
                    "context": {
                        "identity": "farm worker",
                        "Time_period": "off season",
                        "housing_issue": "seasonal eviction"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "trailer_park_sale",
                    "category": "legal_notice",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Trailer park sold to developer. Own my home but not land, must move in 30 days",
                        "Can't afford to move trailer, lifetime of memories being bulldozed"
                    ],
                    "context": {
                        "housing_issue": "park closure",
                        "Time_period": "30 days",
                        "identity": "manufactured home owner"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "well_water_contamination",
                    "category": "health_safety",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Well water contaminated by fracking. Landlord says not his fault, won't fix",
                        "Buying water costs fortune, kids getting sick. No other rentals for 50 miles"
                    ],
                    "context": {
                        "Specific_hazard": "water contamination",
                        "vulnerable_person": "children",
                        "basic_need": "clean water"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "internet_desert_job",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Only housing I can afford has no internet. Need it for remote job, catch-22",
                        "Drive 20 miles to library for wifi. Gas costs eating rent money"
                    ],
                    "context": {
                        "need1": "internet access",
                        "need2": "affordable housing",
                        "identity": "rural resident"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "mining_town_collapse",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Mine closed, whole town dying. Can't sell house, can't afford to leave",
                        "Three generations here, watching it disappear. Rent due on worthless property"
                    ],
                    "context": {
                        "new_crisis": "economic collapse",
                        "Time_period": "Three generations",
                        "identity": "mining family"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                }
            ]
        },
        
        # Theme 11: Student Housing Exploitation (25 entries)
        {
            "name": "student_housing",
            "base_scenarios": [
                {
                    "name": "dorm_closure_international",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "International student, dorms closing for break. Can't go home, borders closed",
                        "University says not their problem. Homeless in foreign country at 19"
                    ],
                    "context": {
                        "identity": "international student",
                        "housing_issue": "dorm closure",
                        "vulnerable_person": "young student"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "predatory_student_landlord",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Landlord knows we're students, charges illegal fees. Security deposit was grocery money",
                        "Threatens to call parents if we complain. Extortion but who believes students?"
                    ],
                    "context": {
                        "identity": "college student",
                        "new_crisis": "illegal fees",
                        "need1": "fee refund",
                        "need2": "food money"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "scholarship_loss_housing",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Lost scholarship due to parent illness, had to miss classes. Now losing housing too",
                        "One family crisis snowballed into academic and housing disaster. Dreams dying"
                    ],
                    "context": {
                        "family_member": "ill parent",
                        "new_crisis": "scholarship loss",
                        "identity": "first-gen student"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "graduate_student_exploitation",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Teaching full course load for stipend that doesn't cover rent. Food bank regular",
                        "Creating knowledge while experiencing poverty. Academia's dirty secret"
                    ],
                    "context": {
                        "identity": "graduate student",
                        "need1": "living wage",
                        "need2": "affordable housing"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                },
                {
                    "name": "student_parent_childcare_housing",
                    "category": "intersectional_vulnerability",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Student family housing waitlist 2 years. Living in car with toddler, attending classes",
                        "Trying to break cycle of poverty, system makes it impossible. Baby deserves better"
                    ],
                    "context": {
                        "vulnerable_person": "toddler",
                        "identity": "student parent",
                        "Time_period": "Two years"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                }
            ]
        },
        
        # Theme 12: Elder Abuse/Neglect (25 entries)
        {
            "name": "elder_housing",
            "base_scenarios": [
                {
                    "name": "reverse_mortgage_trap",
                    "category": "legal_notice",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Husband died, reverse mortgage company demanding full payment. Losing home at 78",
                        "Lived here 45 years, now they're taking it. Where do old widows go?"
                    ],
                    "context": {
                        "identity": "elderly widow",
                        "housing_issue": "reverse mortgage",
                        "Time_period": "45 years"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "elder_financial_abuse",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Grandson stole rent money, too ashamed to report him. Facing eviction at 84",
                        "Raised him, now he's destroying me. Family betrayal hurts worse than poverty"
                    ],
                    "context": {
                        "identity": "elder abuse victim",
                        "family_member": "grandson",
                        "new_crisis": "financial exploitation"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "memory_care_costs",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Wife needs memory care, costs more than our income. Selling home but not enough",
                        "55 years married, now choosing between her care and our shelter"
                    ],
                    "context": {
                        "family_member": "wife with dementia",
                        "Medical_condition": "dementia care needs",
                        "Time_period": "55 years"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "elder_isolation_neglect",
                    "category": "health_safety",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "No family left, can't maintain home. Landlord ignoring repairs, I'm too weak to fight",
                        "Living in decay at 87. Society throws away old people like garbage"
                    ],
                    "context": {
                        "identity": "isolated elder",
                        "basic_need": "habitable conditions",
                        "duration": "final years"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "pension_theft_eviction",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Company stole pension, only have social security. Can't afford rent anywhere",
                        "Worked 40 years for nothing. Golden years are lead - heavy and poisonous"
                    ],
                    "context": {
                        "identity": "pension theft victim",
                        "Time_period": "40 years",
                        "new_crisis": "retirement poverty"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                }
            ]
        },
        
        # Theme 13: LGBTQ+ Housing Discrimination (25 entries)
        {
            "name": "lgbtq_housing",
            "base_scenarios": [
                {
                    "name": "trans_shelter_rejection",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Women's shelter won't take trans women. Men's shelter dangerous. Streets it is",
                        "Fleeing violence to face more violence. No safe place for people like me"
                    ],
                    "context": {
                        "identity": "trans woman",
                        "discriminatory_act": "shelter rejection",
                        "identity_aspect": "trans identity"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "gay_couple_denied",
                    "category": "discrimination",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Applied for apartment, approved till they met us together. Suddenly 'rented'",
                        "2024 and still can't live openly. Love shouldn't disqualify housing"
                    ],
                    "context": {
                        "identity": "gay couple",
                        "discriminatory_act": "couple discrimination",
                        "identity_aspect": "sexual orientation"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "nonbinary_harassment",
                    "category": "boundary_crisis",
                    "complexity": "high",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Neighbors harass me for being nonbinary. Landlord says stop 'provoking' them",
                        "My existence isn't provocation. Paying rent for daily hate"
                    ],
                    "context": {
                        "identity": "nonbinary person",
                        "Specific_hazard": "neighbor harassment",
                        "discriminatory_act": "landlord complicity"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "queer_youth_family_rejection",
                    "category": "intersectional_vulnerability",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Parents kicked me out for being queer. 17, finishing high school from friend's couch",
                        "Chose authenticity over shelter. Homeless but finally free to be myself"
                    ],
                    "context": {
                        "identity": "queer youth",
                        "vulnerable_person": "LGBTQ teen",
                        "family_member": "rejecting parents"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "hiv_status_discrimination",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Landlord found out I'm HIV+, giving 30 day notice. Says other tenants 'uncomfortable'",
                        "Undetectable for years, zero risk. Stigma from the 80s still killing us"
                    ],
                    "context": {
                        "identity": "person with HIV",
                        "Medical_condition": "HIV",
                        "discriminatory_act": "status discrimination"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                }
            ]
        },
        
        # Theme 14: Veteran-Specific Crisis (25 entries)
        {
            "name": "veteran_crisis",
            "base_scenarios": [
                {
                    "name": "va_benefit_delay",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "VA disability claim pending 18 months. Savings gone, eviction imminent",
                        "Fought for country, country won't fight for me. Bureaucracy as enemy"
                    ],
                    "context": {
                        "identity": "disabled veteran",
                        "Time_period": "18 months",
                        "need1": "VA benefits",
                        "need2": "rent"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "tbi_confusion_eviction",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "TBI from IED, forget to pay rent sometimes. Landlord has no patience for war wounds",
                        "Brain injury invisible so they think I'm lying. Losing housing and mind"
                    ],
                    "context": {
                        "Medical_condition": "traumatic brain injury",
                        "identity": "combat veteran",
                        "housing_issue": "payment confusion"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "veteran_family_homeless",
                    "category": "intersectional_vulnerability",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Iraq vet, living in car with wife and baby. VA housing waitlist is years",
                        "Served my country, now my country lets my baby sleep in backseat"
                    ],
                    "context": {
                        "identity": "veteran parent",
                        "vulnerable_person": "baby",
                        "family_member": "wife and child"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                },
                {
                    "name": "moral_injury_isolation",
                    "category": "boundary_crisis",
                    "complexity": "high",
                    "issue_type": "emotional_overload",
                    "messages": [
                        "Can't be around people after Afghanistan. Landlord evicting for 'antisocial behavior'",
                        "Isolation is how I cope with what I've done. Now losing safe space"
                    ],
                    "context": {
                        "Medical_condition": "moral injury",
                        "identity": "Afghanistan veteran",
                        "housing_issue": "behavior complaints"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "veteran_substance_recovery",
                    "category": "discrimination",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "In recovery from pain pills VA prescribed. Landlord found out, wants recovering addicts out",
                        "Got hooked serving country, now punished for healing. Where's honor in that?"
                    ],
                    "context": {
                        "identity": "veteran in recovery",
                        "Medical_condition": "substance recovery",
                        "discriminatory_act": "recovery discrimination"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                }
            ]
        },
        
        # Theme 15: Immigrant/Refugee Specific (25 entries)
        {
            "name": "immigrant_refugee",
            "base_scenarios": [
                {
                    "name": "asylum_work_permit_expired",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Work permit expired, renewal taking months. Lost job, losing apartment",
                        "Fled death threats at home, facing homelessness here. No country wants us"
                    ],
                    "context": {
                        "identity": "asylum seeker",
                        "new_crisis": "work authorization loss",
                        "need1": "permit renewal",
                        "need2": "rent"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "refugee_language_exploitation",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Landlord charging us double because we don't speak English well. No one helps",
                        "Escaped war to be robbed by peace. American dream is nightmare"
                    ],
                    "context": {
                        "identity": "refugee",
                        "discriminatory_act": "language exploitation",
                        "new_crisis": "rent gouging"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "green_card_sponsor_abuse",
                    "category": "boundary_crisis",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Employer sponsors green card, uses it to control me. Abusive but I'm trapped",
                        "Leave job lose status lose housing. Modern slavery with paperwork"
                    ],
                    "context": {
                        "identity": "green card applicant",
                        "housing_issue": "sponsor control",
                        "Specific_hazard": "immigration abuse"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "undocumented_repair_fear",
                    "category": "maintenance_crisis",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Heater broken but scared to complain. Landlord threatens ICE when we ask for repairs",
                        "Children freezing but deportation worse. Living in fear and cold"
                    ],
                    "context": {
                        "identity": "undocumented family",
                        "vulnerable_person": "children",
                        "basic_need": "heat",
                        "Specific_hazard": "ICE threats"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "refugee_trauma_neighbors",
                    "category": "discrimination",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Fireworks trigger war flashbacks, neighbors complain about my screaming. Eviction threatened",
                        "Survived genocide to be punished for trauma. No escape from war sounds"
                    ],
                    "context": {
                        "identity": "war refugee",
                        "Medical_condition": "war trauma",
                        "discriminatory_act": "trauma punishment"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                }
            ]
        },
        
        # Theme 16: Substance Recovery Housing (25 entries)
        {
            "name": "recovery_housing",
            "base_scenarios": [
                {
                    "name": "sober_house_closure",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Sober house closing, 30 days notice. 6 months clean, nowhere safe to go",
                        "Regular apartments won't take recovery history. One closure away from relapse"
                    ],
                    "context": {
                        "identity": "person in recovery",
                        "housing_issue": "facility closure",
                        "Medical_condition": "addiction recovery"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "methadone_clinic_distance",
                    "category": "health_safety",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Only affordable housing 2 hours from methadone clinic. Daily dosing impossible",
                        "Choose between housing and medication. Both keep me alive"
                    ],
                    "context": {
                        "Medical_condition": "opioid recovery",
                        "identity": "methadone patient",
                        "basic_need": "treatment access"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "recovery_discrimination",
                    "category": "discrimination",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Landlord googled me, found old arrest. Says no addicts even though I'm 3 years clean",
                        "Past mistakes are life sentence. Recovery means nothing to them"
                    ],
                    "context": {
                        "identity": "person in recovery",
                        "discriminatory_act": "recovery discrimination",
                        "Time_period": "Three years clean"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "halfway_house_transition",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Aging out of halfway house but minimum wage won't cover any apartment",
                        "Did everything right in recovery, still facing homelessness. System setup to fail"
                    ],
                    "context": {
                        "identity": "halfway house resident",
                        "need1": "affordable housing",
                        "need2": "continued support"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                },
                {
                    "name": "substance_use_eviction",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Relapsed once after mom died, neighbor called landlord. Eviction for 'drug activity'",
                        "One slip in grief and losing everything. Punishment makes recovery harder"
                    ],
                    "context": {
                        "Medical_condition": "substance use disorder",
                        "housing_issue": "zero tolerance",
                        "family_member": "deceased mother"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                }
            ]
        },
        
        # Theme 17: Pregnancy/New Parent Crisis (25 entries)
        {
            "name": "pregnancy_crisis",
            "base_scenarios": [
                {
                    "name": "pregnancy_job_loss",
                    "category": "discrimination",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Fired day after telling boss I'm pregnant. 'Position eliminated' but hiring replacement",
                        "7 months pregnant, no income, eviction filed. Baby coming to homelessness"
                    ],
                    "context": {
                        "Medical_condition": "pregnancy",
                        "discriminatory_act": "pregnancy discrimination",
                        "identity": "pregnant woman"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "bedrest_eviction",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Doctor ordered bedrest, can't work. Landlord says pregnancy isn't disability",
                        "Risk miscarriage from stress of eviction. Losing home might mean losing baby"
                    ],
                    "context": {
                        "Medical_condition": "high-risk pregnancy",
                        "housing_issue": "medical leave eviction",
                        "vulnerable_person": "unborn baby"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                },
                {
                    "name": "postpartum_crisis",
                    "category": "intersectional_vulnerability",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Severe postpartum depression, can't function. Behind on everything, eviction looming",
                        "Can barely care for baby, definitely can't fight eviction. Drowning in hormones and fear"
                    ],
                    "context": {
                        "Medical_condition": "postpartum depression",
                        "vulnerable_person": "newborn",
                        "identity": "new mother"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "nicu_bills_rent",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Baby in NICU 3 months, bills destroying us. Choosing between rent and seeing her",
                        "Parking at hospital costs fortune. Living in car to afford NICU visits"
                    ],
                    "context": {
                        "Medical_condition": "premature baby",
                        "vulnerable_person": "NICU baby",
                        "need1": "medical costs",
                        "need2": "housing"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "single_dad_newborn",
                    "category": "intersectional_vulnerability",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Mom left, I'm alone with newborn. Work won't give paternity leave, losing job",
                        "Society expects moms to handle babies. Single dad means no support, no sympathy"
                    ],
                    "context": {
                        "identity": "single father",
                        "vulnerable_person": "newborn",
                        "need1": "childcare",
                        "need2": "income"
                    },
                    "arousal": 8.4,
                    "capacity": 3.3
                }
            ]
        },
        
        # Theme 18: Utility Crisis Cascades (25 entries)
        {
            "name": "utility_crisis",
            "base_scenarios": [
                {
                    "name": "water_shutoff_dialysis",
                    "category": "health_safety",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Water shut off, I do home dialysis. Without water, kidneys fail in days",
                        "Begged water company, they want $800. My life worth less than water bill"
                    ],
                    "context": {
                        "Medical_condition": "kidney failure",
                        "basic_need": "water for dialysis",
                        "Specific_hazard": "organ failure"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                },
                {
                    "name": "electric_medical_equipment",
                    "category": "health_safety",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Power cut tomorrow, daughter needs ventilator to breathe. Generator costs month's rent",
                        "Electric company knows she'll die, doesn't care. Profit over 8-year-old's life"
                    ],
                    "context": {
                        "vulnerable_person": "ventilator-dependent child",
                        "Medical_condition": "respiratory failure",
                        "basic_need": "electricity for life support"
                    },
                    "arousal": 8.9,
                    "capacity": 3.0
                },
                {
                    "name": "heat_shutoff_elderly",
                    "category": "health_safety",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Gas shut off, no heat. 78 years old with arthritis, bones screaming in cold",
                        "Utility company says payment plan after full payment. Might not survive winter"
                    ],
                    "context": {
                        "identity": "elderly person",
                        "Medical_condition": "arthritis",
                        "basic_need": "heat",
                        "duration": "winter"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "internet_schoolwork",
                    "category": "intersectional_vulnerability",
                    "complexity": "high",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Internet cut, kids can't do homework. School threatening truancy for missing assignments",
                        "Teacher says 'all kids have internet'. Mine study by streetlight"
                    ],
                    "context": {
                        "vulnerable_person": "school children",
                        "basic_need": "internet for education",
                        "system": "school system"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "utility_deposit_trap",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Moving to cheaper place but utility deposits are $1200. Trapped in expensive housing",
                        "Poor tax everywhere. Can't afford to save money by moving"
                    ],
                    "context": {
                        "need1": "utility deposits",
                        "need2": "ability to relocate",
                        "new_crisis": "deposit barriers"
                    },
                    "arousal": 8.2,
                    "capacity": 3.5
                }
            ]
        },
        
        # Theme 19: Domestic Worker Exploitation (25 entries)
        {
            "name": "domestic_worker",
            "base_scenarios": [
                {
                    "name": "live_in_nanny_fired",
                    "category": "eviction",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Live-in nanny 5 years, family fired me with 1 day notice. Job and home gone instantly",
                        "Raised their kids, now homeless. No references because mom jealous of kids loving me"
                    ],
                    "context": {
                        "identity": "domestic worker",
                        "housing_issue": "live-in job loss",
                        "Time_period": "Five years"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "home_care_client_died",
                    "category": "financial_distress",
                    "complexity": "critical",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Cared for elderly man 8 years, he died. Family wants me out today, no final pay",
                        "Gave best years to their father, they treat me like furniture to discard"
                    ],
                    "context": {
                        "identity": "home care worker",
                        "Time_period": "Eight years",
                        "new_crisis": "client death"
                    },
                    "arousal": 8.5,
                    "capacity": 3.2
                },
                {
                    "name": "cleaner_wage_theft",
                    "category": "financial_distress",
                    "complexity": "high",
                    "issue_type": "financial_instability",
                    "messages": [
                        "Clean houses cash only, multiple clients refusing to pay. Can't prove work, can't get rent",
                        "Break my back making their homes beautiful, they break promises"
                    ],
                    "context": {
                        "identity": "house cleaner",
                        "new_crisis": "wage theft",
                        "need1": "owed wages",
                        "need2": "rent"
                    },
                    "arousal": 8.3,
                    "capacity": 3.4
                },
                {
                    "name": "domestic_violence_employer",
                    "category": "boundary_crisis",
                    "complexity": "critical",
                    "issue_type": "safety_threat",
                    "messages": [
                        "Employer sexually harassing me but I live in their guest house. Report means homeless",
                        "Trapped between assault and streets. This isn't work, it's captivity"
                    ],
                    "context": {
                        "identity": "live-in domestic worker",
                        "Specific_hazard": "sexual harassment",
                        "housing_issue": "employer-tied housing"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "undocumented_domestic",
                    "category": "intersectional_vulnerability",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Employer threatening ICE if I complain about conditions. Living in garage, no heat",
                        "They know I'm trapped. Modern slavery hiding in suburban homes"
                    ],
                    "context": {
                        "identity": "undocumented domestic worker",
                        "Specific_hazard": "ICE threats",
                        "basic_need": "safe housing"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                }
            ]
        },
        
        # Theme 20: Complex Multi-System Failures (25 entries)
        {
            "name": "system_failures",
            "base_scenarios": [
                {
                    "name": "foster_disability_aging",
                    "category": "complex_grievance",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Disabled foster kid aging out at 18. No family, no support, no accessible housing",
                        "System raised me broken then abandons me. Where do broken children go?"
                    ],
                    "context": {
                        "identity": "disabled foster youth",
                        "vulnerable_person": "disabled teen",
                        "Medical_condition": "multiple disabilities"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "veteran_immigrant_disability",
                    "category": "complex_grievance",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Served in US military, got injured, now disabled immigrant facing deportation and eviction",
                        "Gave body to America, America discarding broken immigrant soldier"
                    ],
                    "context": {
                        "identity": "immigrant veteran",
                        "Medical_condition": "service disability",
                        "housing_issue": "immigration status"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                },
                {
                    "name": "trans_elder_dementia",
                    "category": "complex_grievance",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Trans elder with dementia, facilities won't take me. Family disowned decades ago",
                        "Fought to be myself whole life, now losing self and shelter"
                    ],
                    "context": {
                        "identity": "trans elder",
                        "Medical_condition": "dementia",
                        "discriminatory_act": "facility rejection"
                    },
                    "arousal": 8.6,
                    "capacity": 3.1
                },
                {
                    "name": "indigenous_foster_trauma",
                    "category": "complex_grievance",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Indigenous kid taken to foster care, aged out traumatized. No connection to tribe or housing",
                        "Stolen from culture, given trauma. Two genocides in one lifetime"
                    ],
                    "context": {
                        "identity": "Indigenous foster survivor",
                        "identity_aspect": "Indigenous identity",
                        "Years/Months": "lifetime"
                    },
                    "arousal": 8.7,
                    "capacity": 3.0
                },
                {
                    "name": "refugee_disability_discrimination",
                    "category": "complex_grievance",
                    "complexity": "critical",
                    "issue_type": "multiple_barriers",
                    "messages": [
                        "Disabled refugee, landlord says too many problems. War took legs, peace taking home",
                        "Survived bombs to face discrimination. No country wants broken refugees"
                    ],
                    "context": {
                        "identity": "disabled refugee",
                        "Medical_condition": "war amputation",
                        "discriminatory_act": "compound discrimination"
                    },
                    "arousal": 8.8,
                    "capacity": 3.0
                }
            ]
        }
    ]
    
    # Generate all batches
    print(f"Generating 500 entries across {len(themes)} themes...")
    
    for theme_data in themes:
        theme_name = theme_data["name"]
        base_scenarios = theme_data["base_scenarios"]
        
        # Generate variations for each base scenario to reach 25 per theme
        theme_scenarios = []
        for base in base_scenarios:
            # Generate 5 variations of each base scenario
            variations = [
                {"messages": [base["messages"][0], base["messages"][1]]},
                {"messages": [base["messages"][0] + " No one listens", base["messages"][1] + " System broken"]},
                {"messages": ["Similar issue: " + base["messages"][0], "Getting worse: " + base["messages"][1]]},
                {"messages": [base["messages"][0] + " Third time this year", base["messages"][1] + " Out of options"]},
                {"messages": ["Emergency: " + base["messages"][0], "Desperate: " + base["messages"][1]]}
            ]
            
            scenario_variations = batch_gen.generate_scenario_variations(base, variations, count=5)
            theme_scenarios.extend(scenario_variations)
        
        # Generate batch for this theme
        batch = batch_gen.generate_batch(theme_name, theme_scenarios[:25])  # Ensure exactly 25
        all_entries.extend(batch)
        
        print(f"Generated {len(batch)} entries for theme: {theme_name}")
    
    return all_entries

def main():
    """Generate and save 500 entries."""
    entries = generate_500_entries()
    
    # Save to file
    filename = "willow_batch_500_entries.jsonl"
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\nTotal entries generated: {len(entries)}")
    print(f"Saved to: {filename}")
    
    # Generate summary statistics
    categories = {}
    complexities = {}
    themes = {}
    
    for entry in entries:
        # Category stats
        cat = entry["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
        # Complexity stats
        comp = entry["complexity_level"]
        complexities[comp] = complexities.get(comp, 0) + 1
        
        # Theme stats
        theme = entry["scenario"].split("_")[0]
        themes[theme] = themes.get(theme, 0) + 1
    
    print("\nCategory Distribution:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} ({count/len(entries)*100:.1f}%)")
    
    print("\nComplexity Distribution:")
    for comp, count in sorted(complexities.items()):
        print(f"  {comp}: {count} ({count/len(entries)*100:.1f}%)")
    
    print(f"\nThemes covered: {len(themes)}")
    print(f"ID Range: {entries[0]['id']} - {entries[-1]['id']}")

if __name__ == "__main__":
    main()