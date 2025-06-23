#!/usr/bin/env python3
"""
Generate 50 diverse Willow dataset entries using enhanced tools
"""

import json
from typing import Dict
from willow_dataset_generator import WillowGenerator
from willow_response_library import WillowResponseLibrary

def generate_batch_50():
    """Generate 50 entries across multiple crisis types."""
    
    generator = WillowGenerator(starting_id=1344)
    library = WillowResponseLibrary()
    
    # Define scenarios across different categories
    scenarios = [
        # Winter/Cold Weather Crises (10 entries)
        {
            "name": "frozen_pipes_elderly",
            "category": "maintenance_crisis",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "82 years old, pipes frozen solid, no water 3 days. Can't lift buckets from neighbor",
                "Arthritis so bad can't turn valves. Grandson tries to help but works doubles"
            ],
            "context": {
                "Duration": "Three days",
                "basic_need": "water",
                "Specific_hazard": "dehydration risk",
                "vulnerable_person": "yourself at 82",
                "duration": "three days",
                "obstacles": "age and isolation"
            },
            "arousal": 8.2,
            "capacity": 3.2
        },
        {
            "name": "heating_oil_empty_kids", 
            "category": "maintenance_crisis",
            "complexity": "critical",
            "issue_type": "financial_instability",
            "messages": [
                "Oil tank empty, no money till Friday. Kids sleeping in coats, baby has asthma",
                "Called churches, all tapped out. Landlord says not his problem. Baby wheezing"
            ],
            "context": {
                "need1": "heating oil",
                "need2": "baby's medication",
                "new_crisis": "the asthma attack risk",
                "Time_period": "This week",
                "vulnerable_person": "your baby",
                "duration": "until Friday"
            },
            "arousal": 8.8,
            "capacity": 3.0
        },
        {
            "name": "space_heater_fire_threat",
            "category": "health_safety",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Using space heaters because furnace broken. Landlord says they're illegal, threatening eviction",
                "What choice do I have? Freeze or homeless? Fire department already warned me"
            ],
            "context": {
                "Duration": "Weeks",
                "basic_need": "heat",
                "Specific_hazard": "fire risk or freezing",
                "duration": "this ongoing nightmare"
            },
            "arousal": 7.8,
            "capacity": 3.6
        },
        {
            "name": "burst_pipe_damage_deposit",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "Pipe burst while at work, landlord blaming me, keeping $2000 deposit. That's my moving money",
                "Says I should've left heat on but he controls thermostat. Now I'm trapped here"
            ],
            "context": {
                "need1": "deposit return",
                "need2": "moving costs",
                "new_crisis": "being trapped in unsafe housing"
            },
            "arousal": 8.0,
            "capacity": 3.5
        },
        {
            "name": "snow_blocked_emergency_exit",
            "category": "health_safety",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Landlord won't clear snow from fire escape. Mom uses wheelchair, we're trapped if fire",
                "Called fire dept, they cited him but nothing changed. Mom terrified every night"
            ],
            "context": {
                "Specific_hazard": "blocked emergency exits",
                "vulnerable_person": "your mother",
                "duration": "every day of winter"
            },
            "arousal": 7.9,
            "capacity": 3.7
        },
        
        # Medical/Health Crises (10 entries)
        {
            "name": "chemo_eviction_threat",
            "category": "eviction",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Cancer treatment wiped savings. 2 months behind, eviction filed. Still have 6 months chemo",
                "Can't work, disability pending 5 months. Lawyer wants $2000 retainer I don't have"
            ],
            "context": {
                "Medical_condition": "Cancer",
                "housing_crisis": "eviction proceedings",
                "treatment": "chemotherapy",
                "threat": "homelessness",
                "duration": "two months",
                "who/what you're protecting": "your chance at survival"
            },
            "arousal": 8.9,
            "capacity": 3.1
        },
        {
            "name": "dialysis_water_shutoff",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Need dialysis 3x week, they shut water off. Can't do home treatment, ER won't take me stable",
                "Landlord says pay or move but I can't miss treatments. Feel like I'm dying"
            ],
            "context": {
                "Medical_condition": "Kidney failure",
                "housing_crisis": "water shutoff",
                "stressor": "inability to do home dialysis",
                "duration": "this crisis"
            },
            "arousal": 8.7,
            "capacity": 3.2
        },
        {
            "name": "wheelchair_stairs_fall",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Fell down stairs again, wheelchair ramp request denied 6 months. Broke ribs this time",
                "They said first floor too expensive but I'm paying same rent. Hospital bills mounting"
            ],
            "context": {
                "identity": "disability",
                "discriminatory_act": "denying wheelchair access",
                "discrimination_type": "disability discrimination"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        {
            "name": "mental_health_noise_complaint",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "PTSD nightmares, neighbors complaining. Landlord says 'take your meds or get out'",
                "VA therapist wrote letter explaining but he laughed. Says no crazy people allowed"
            ],
            "context": {
                "identity": "mental health condition",
                "identity_aspect": "PTSD",
                "Medical_condition": "PTSD",
                "housing_crisis": "discrimination threats"
            },
            "arousal": 8.1,
            "capacity": 3.5
        },
        {
            "name": "oxygen_tank_power_shutoff",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Power shutoff notice but I need electricity for oxygen. Landlord won't intervene with utility",
                "Doctor says I could die without it. Payment plan rejected, they want full $800"
            ],
            "context": {
                "Medical_condition": "COPD",
                "housing_crisis": "power shutoff",
                "threat": "loss of life-sustaining equipment"
            },
            "arousal": 8.8,
            "capacity": 3.0
        },
        
        # Family Separation/Child Safety (10 entries)
        {
            "name": "cps_mold_threat",
            "category": "intersectional_vulnerability",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "CPS investigating because of mold. Landlord won't fix, says I'm troublemaker. Could lose kids",
                "Case worker says fix it or kids go to foster care. But it's not my property!"
            ],
            "context": {
                "family_member": "your children",
                "housing_issue": "dangerous mold",
                "system": "CPS",
                "vulnerable_person": "your children"
            },
            "arousal": 9.0,
            "capacity": 3.0
        },
        {
            "name": "domestic_violence_lease_trap",
            "category": "legal_notice",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Ex found me, landlord won't let me break lease. Says DV isn't his problem, pay or ruin credit",
                "Shelter has space but I'll owe $8000 if I leave. Trapped between debt and danger"
            ],
            "context": {
                "family_member": "yourself",
                "housing_issue": "lease trap",
                "system": "legal system"
            },
            "arousal": 8.7,
            "capacity": 3.1
        },
        {
            "name": "school_district_eviction",
            "category": "eviction",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Eviction means new school district. Son autistic, finally stable here. He'll regress",
                "IEP took 2 years to get right. Starting over will destroy his progress"
            ],
            "context": {
                "vulnerable_person": "your autistic son",
                "housing_issue": "eviction",
                "duration": "this upheaval"
            },
            "arousal": 8.2,
            "capacity": 3.4
        },
        {
            "name": "ice_raid_repair_fear",
            "category": "maintenance_crisis",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Ceiling leak getting worse but scared to call repair. ICE raided building last month",
                "Water dripping on baby's crib. Other tenants say landlord reports undocumented"
            ],
            "context": {
                "Duration": "Weeks",
                "basic_need": "safe shelter",
                "Specific_hazard": "water damage and mold",
                "family_member": "your family",
                "housing_issue": "needed repairs"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        {
            "name": "custody_address_verification",
            "category": "legal_notice",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Ex using my unstable housing in custody fight. Judge wants lease but I'm month-to-month",
                "Landlord refuses stability letter. Says he doesn't get involved in personal drama"
            ],
            "context": {
                "family_member": "your children",
                "housing_issue": "housing instability",
                "system": "family court"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        
        # Discrimination/Identity-Based (10 entries)
        {
            "name": "trans_bathroom_harassment",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Other tenants petitioning to evict me for using bathroom. Landlord says majority rules",
                "Found 'tr*nny leave' on my door. Scared to leave apartment, holding it for hours"
            ],
            "context": {
                "identity": "gender identity",
                "discriminatory_act": "bathroom harassment",
                "discrimination_type": "transphobia",
                "identity_aspect": "trans identity"
            },
            "arousal": 8.5,
            "capacity": 3.3
        },
        {
            "name": "muslim_prayer_eviction",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Eviction notice for 'disturbing noises' aka my prayers. Other tenants play music louder",
                "They said find somewhere 'more suitable for your kind'. 20 days to move"
            ],
            "context": {
                "identity": "religious practice",
                "discriminatory_act": "targeting prayers",
                "discrimination_type": "religious discrimination",
                "identity_aspect": "Muslim faith"
            },
            "arousal": 8.2,
            "capacity": 3.5
        },
        {
            "name": "section8_application_denied",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "Applied for apartment, approved till they heard Section 8. Suddenly it's rented",
                "6th rejection this month. Running out of time, voucher expires in 30 days"
            ],
            "context": {
                "identity": "housing voucher recipient",
                "discriminatory_act": "Section 8 discrimination",
                "discrimination_type": "source of income discrimination"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        {
            "name": "immigrant_language_threat",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Landlord screaming I must speak English in common areas. Threatening lease violation",
                "Was talking to my mother on phone! Says it makes other tenants uncomfortable"
            ],
            "context": {
                "identity": "immigrant status",
                "discriminatory_act": "language policing",
                "discrimination_type": "xenophobia",
                "identity_aspect": "native language"
            },
            "arousal": 8.0,
            "capacity": 3.6
        },
        {
            "name": "disability_parking_denied",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Need accessible parking for wheelchair van. Landlord gave my spot to his friend",
                "Now wheeling from street in rain/snow. Fell twice. He says first come first served"
            ],
            "context": {
                "identity": "disability",
                "discriminatory_act": "denying accessible parking",
                "discrimination_type": "disability discrimination"
            },
            "arousal": 8.1,
            "capacity": 3.5
        },
        
        # Financial/Benefits Intersection (10 entries)
        {
            "name": "ssi_overpayment_rent",
            "category": "financial_distress",
            "complexity": "critical",
            "issue_type": "financial_instability",
            "messages": [
                "SSI says I owe $5000 overpayment, taking whole check. Rent due in 3 days",
                "Appeal could take months. Landlord already filed eviction papers. I did nothing wrong"
            ],
            "context": {
                "need1": "rent",
                "need2": "basic survival",
                "new_crisis": "benefits suspension",
                "Time_period": "Three days"
            },
            "arousal": 8.6,
            "capacity": 3.2
        },
        {
            "name": "unemployment_delay_utilities",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "Unemployment delayed 8 weeks, all utilities shut off. Living by candles, no fridge",
                "Food spoiled, phone dead so can't call unemployment. Using library wifi"
            ],
            "context": {
                "need1": "utilities",
                "need2": "food",
                "new_crisis": "complete disconnection",
                "Time_period": "Eight weeks"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        {
            "name": "snap_cutoff_choose",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "SNAP cut off for missing recertification I never got. Rent or food this month?",
                "Kids already lost weight. School lunch only meal. But eviction means no address for benefits"
            ],
            "context": {
                "need1": "food",
                "need2": "shelter",
                "new_crisis": "benefits loss",
                "vulnerable_person": "your children"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        {
            "name": "workers_comp_denial",
            "category": "financial_distress",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Hurt at work, workers comp denied. Can't work, can't pay rent. Boss fired me",
                "Lawyer wants money upfront. Eviction court next week. Back screaming in pain"
            ],
            "context": {
                "need1": "rent",
                "need2": "medical care",
                "Medical_condition": "work injury",
                "housing_crisis": "eviction"
            },
            "arousal": 8.7,
            "capacity": 3.1
        },
        {
            "name": "child_support_garnish",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "Child support garnishing 65% for arrears from when I was homeless. Can't afford rent",
                "Judge won't modify. Says pay or jail but jail means lose job and housing"
            ],
            "context": {
                "need1": "rent",
                "need2": "avoiding jail",
                "new_crisis": "garnishment",
                "Time_period": "Every month"
            },
            "arousal": 8.2,
            "capacity": 3.5
        },
        
        # Additional Complex Scenarios (25 more entries)
        
        # Elderly/Disability Intersection (5 entries)
        {
            "name": "dementia_eviction_notice",
            "category": "eviction",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Mom has dementia, keeps forgetting to pay rent. Got eviction notice, she doesn't understand",
                "I live 3 states away, trying to get POA but court wants her competent. Catch-22"
            ],
            "context": {
                "vulnerable_person": "your mother with dementia",
                "housing_issue": "eviction",
                "Medical_condition": "dementia",
                "duration": "this crisis",
                "family_member": "your mother"
            },
            "arousal": 8.6,
            "capacity": 3.2
        },
        {
            "name": "hospice_home_repairs",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Dad dying, hospice says house unsafe - no heat, mold. Want to die at home not facility",
                "Landlord says not worth fixing for 'short term tenant'. Dad heard that"
            ],
            "context": {
                "Medical_condition": "terminal illness",
                "housing_crisis": "unsafe conditions",
                "vulnerable_person": "your dying father",
                "basic_need": "dignified death at home",
                "Specific_hazard": "hospice rejection"
            },
            "arousal": 8.8,
            "capacity": 3.0
        },
        {
            "name": "veteran_hoarding_eviction",
            "category": "eviction",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Vietnam vet, they say I'm hoarding but it's my stuff. Eviction for 'health hazard'",
                "VA psych says it's PTSD coping but landlord doesn't care. Where will my things go?"
            ],
            "context": {
                "identity": "veteran status",
                "Medical_condition": "PTSD-related hoarding",
                "housing_issue": "eviction",
                "identity_aspect": "veteran with PTSD"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        {
            "name": "blind_maintenance_access",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "I'm blind, maintenance enters without notice. Can't see who's in my home, terrifying",
                "Asked for audio notice, they say too complicated. Found strange man in bedroom yesterday"
            ],
            "context": {
                "identity": "blindness",
                "discriminatory_act": "refusing accommodation",
                "discrimination_type": "disability discrimination",
                "Specific_hazard": "unauthorized entry"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        {
            "name": "alzheimers_utility_shutoff",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Wife has Alzheimer's, forgot to pay electric. Power cut, her oxygen and medications need refrigeration",
                "Begged utility company, they want $500 deposit plus arrears. We live on social security"
            ],
            "context": {
                "Medical_condition": "Alzheimer's",
                "housing_crisis": "utility shutoff",
                "vulnerable_person": "your wife",
                "need1": "electricity for medical equipment",
                "need2": "refrigeration for medications"
            },
            "arousal": 8.7,
            "capacity": 3.1
        },
        
        # Immigration/Documentation Issues (5 entries)
        {
            "name": "daca_renewal_eviction",
            "category": "eviction",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "DACA renewal delayed, lost job, behind on rent. Landlord threatening ICE if I don't leave",
                "Been here since 2 years old, this is only home I know. Kids born here, where do we go?"
            ],
            "context": {
                "identity": "DACA recipient",
                "housing_issue": "eviction threat",
                "family_member": "your American children",
                "Time_period": "Twenty years"
            },
            "arousal": 8.5,
            "capacity": 3.2
        },
        {
            "name": "asylum_seeker_deposit",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Asylum pending 3 years, work permit expired. Landlord wants 6 months rent as 'security'",
                "Can't work legally but kids need shelter. Caught between laws and survival"
            ],
            "context": {
                "identity": "asylum seeker",
                "need1": "housing deposit",
                "need2": "work authorization",
                "vulnerable_person": "your children"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        {
            "name": "mixed_status_family_repair",
            "category": "maintenance_crisis",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Heater broken, scared to push for repairs. I'm documented but husband isn't",
                "Landlord hints he'll 'check everyone's papers' if we complain. Baby getting sick from cold"
            ],
            "context": {
                "family_member": "your undocumented husband",
                "housing_issue": "heating failure",
                "Duration": "Two weeks",
                "basic_need": "heat",
                "vulnerable_person": "your baby"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        {
            "name": "refugee_language_eviction",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Refugee from Syria, eviction notice all English. Translator says I agreed to leave but I didn't",
                "Neighbors helped read it - only 3 days left. They tricked me with papers I couldn't read"
            ],
            "context": {
                "identity": "refugee status",
                "discriminatory_act": "language exploitation",
                "discrimination_type": "national origin discrimination",
                "Time_period": "Three days"
            },
            "arousal": 8.6,
            "capacity": 3.2
        },
        {
            "name": "tps_expiration_housing",
            "category": "legal_notice",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "TPS expires next month, landlord already asking for new lease with citizen co-signer",
                "20 years here, own business, kids in college. One paper changes everything"
            ],
            "context": {
                "identity": "TPS holder",
                "housing_issue": "lease discrimination",
                "Time_period": "Twenty years",
                "family_member": "your college children"
            },
            "arousal": 8.5,
            "capacity": 3.3
        },
        
        # Youth/Student Crises (5 entries)
        {
            "name": "aged_out_foster_eviction",
            "category": "eviction",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Aged out foster care at 18, first apartment. Don't understand eviction notice, no one taught me",
                "Case worker gone, bio family absent, chosen family broke. System raised me then abandoned me"
            ],
            "context": {
                "identity": "former foster youth",
                "housing_issue": "eviction",
                "Years/Months": "18 years",
                "duration": "this abandonment"
            },
            "arousal": 8.7,
            "capacity": 3.0
        },
        {
            "name": "student_parent_childcare",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Full time student, single mom. Daycare or rent, can't afford both. Eviction looming",
                "So close to degree, 2 semesters left. But baby needs safe place more than I need diploma"
            ],
            "context": {
                "need1": "childcare",
                "need2": "rent",
                "vulnerable_person": "your baby",
                "duration": "two more semesters"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        {
            "name": "lgbtq_youth_kicked_out",
            "category": "discrimination",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Parents kicked me out for being gay. Roommate's landlord says no more people, threatening everyone's lease",
                "19, no credit, no co-signer. Shelters full, couch surfing ending. Winter coming"
            ],
            "context": {
                "identity": "LGBTQ youth",
                "identity_aspect": "sexual orientation",
                "housing_issue": "homelessness",
                "Time_period": "Winter"
            },
            "arousal": 8.8,
            "capacity": 3.0
        },
        {
            "name": "graduate_student_stipend",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "University cut grad stipends mid-semester. Rent due, thesis due, everything falling apart",
                "7 years invested in PhD, but landlord wants money not excuses. Academic dreams vs roof"
            ],
            "context": {
                "need1": "rent",
                "need2": "degree completion",
                "Time_period": "Seven years",
                "new_crisis": "stipend loss"
            },
            "arousal": 8.2,
            "capacity": 3.5
        },
        {
            "name": "teen_parent_discrimination",
            "category": "discrimination",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "17 with baby, emancipated minor. Landlord found out my age, says lease void, get out",
                "Have job, pay rent on time, good tenant. But he says 'no teen moms' policy"
            ],
            "context": {
                "identity": "teen parent",
                "discriminatory_act": "age discrimination",
                "vulnerable_person": "your baby",
                "identity_aspect": "young motherhood"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        
        # Natural Disaster/Climate (5 entries)
        {
            "name": "wildfire_smoke_asthma",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Wildfire smoke, windows don't seal. Son's asthma attacks daily. Landlord says act of God",
                "Hospital bills mounting, missed work for ER visits. Air purifier or rent, not both"
            ],
            "context": {
                "Medical_condition": "severe asthma",
                "housing_crisis": "smoke infiltration",
                "vulnerable_person": "your son",
                "Specific_hazard": "toxic air quality"
            },
            "arousal": 8.6,
            "capacity": 3.2
        },
        {
            "name": "flood_mold_pregnancy",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Apartment flooded 2 months ago, black mold everywhere. I'm pregnant, doctor says it's dangerous",
                "Landlord painted over it, says fixed. Can smell it, feel sick, baby at risk"
            ],
            "context": {
                "Medical_condition": "pregnancy",
                "housing_crisis": "toxic mold",
                "Specific_hazard": "mold exposure",
                "duration": "two months"
            },
            "arousal": 8.8,
            "capacity": 3.0
        },
        {
            "name": "hurricane_price_gouging",
            "category": "financial_distress",
            "complexity": "high",
            "issue_type": "financial_instability",
            "messages": [
                "Hurricane destroyed everything. Landlords tripled rent on remaining units. Price gouging legal?",
                "FEMA hotel voucher expiring, kids start school next week. Nowhere affordable left"
            ],
            "context": {
                "new_crisis": "disaster price gouging",
                "need1": "affordable housing",
                "need2": "school stability",
                "vulnerable_person": "your children"
            },
            "arousal": 8.5,
            "capacity": 3.2
        },
        {
            "name": "earthquake_damage_blame",
            "category": "legal_notice",
            "complexity": "high",
            "issue_type": "multiple_barriers",
            "messages": [
                "Earthquake cracked walls, ceiling falling. Landlord says I caused damage, keeping deposit",
                "Building inspector condemned it but landlord blaming me. Collections threatening credit"
            ],
            "context": {
                "housing_issue": "false damage claims",
                "system": "legal system",
                "new_crisis": "credit destruction"
            },
            "arousal": 8.3,
            "capacity": 3.4
        },
        {
            "name": "heatwave_elderly_building",
            "category": "health_safety",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Heatwave, no AC, 98 inside. Elderly neighbor died yesterday. Landlord says open windows",
                "Heart condition, doctor says heat dangerous. But window units 'not allowed' per lease"
            ],
            "context": {
                "Medical_condition": "heart condition",
                "housing_crisis": "extreme heat",
                "Specific_hazard": "heat stroke risk",
                "duration": "this deadly heatwave"
            },
            "arousal": 8.7,
            "capacity": 3.1
        },
        
        # Domestic Violence/Safety (5 entries)
        {
            "name": "stalker_security_deposit",
            "category": "legal_notice",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Ex stalking, need to move NOW. Landlord wants 60 days notice or lose $3000 deposit",
                "Restraining order but he knows where I live. Safety or money, can't have both"
            ],
            "context": {
                "family_member": "yourself",
                "housing_issue": "lease trap",
                "system": "legal system",
                "need1": "immediate safety",
                "need2": "moving funds"
            },
            "arousal": 8.9,
            "capacity": 3.0
        },
        {
            "name": "dv_shelter_time_limit",
            "category": "intersectional_vulnerability",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "DV shelter 30 day limit up. Apartments want references - abuser was my only rental history",
                "Kids finally feeling safe, now we're out again. System protects then abandons"
            ],
            "context": {
                "family_member": "your children",
                "housing_issue": "shelter time limit",
                "vulnerable_person": "your traumatized children",
                "system": "DV support system"
            },
            "arousal": 8.6,
            "capacity": 3.1
        },
        {
            "name": "protection_order_eviction",
            "category": "eviction",
            "complexity": "high",
            "issue_type": "safety_threat",
            "messages": [
                "Got protection order against neighbor tenant. Landlord evicting ME for 'causing drama'",
                "I'm the victim but losing home. He stays, I go. How is this justice?"
            ],
            "context": {
                "identity": "crime victim",
                "housing_issue": "retaliatory eviction",
                "identity_aspect": "victim status"
            },
            "arousal": 8.4,
            "capacity": 3.3
        },
        {
            "name": "trafficking_survivor_housing",
            "category": "discrimination",
            "complexity": "critical",
            "issue_type": "multiple_barriers",
            "messages": [
                "Trafficking survivor, no rental history for 5 years. Every application rejected",
                "Trying to rebuild but past keeps haunting. They see gaps and assume the worst"
            ],
            "context": {
                "identity": "trafficking survivor",
                "identity_aspect": "survivor status",
                "Years/Months": "Five years",
                "housing_issue": "rental history gaps"
            },
            "arousal": 8.5,
            "capacity": 3.2
        },
        {
            "name": "witness_protection_lease",
            "category": "legal_notice",
            "complexity": "critical",
            "issue_type": "safety_threat",
            "messages": [
                "Testified against gang, need to relocate. Landlord wants full lease buyout $15,000",
                "Marshals say move now but can't help with civil lease. Life in danger over contract"
            ],
            "context": {
                "family_member": "yourself and family",
                "housing_issue": "lease termination",
                "system": "legal system",
                "need1": "immediate relocation",
                "need2": "financial freedom"
            },
            "arousal": 9.0,
            "capacity": 3.0
        }
    ]
    
    # Generate entries
    all_entries = []
    
    for scenario_data in scenarios:
        # Generate tier 1 response
        tier1_response = library.build_complete_response(
            tier="tier_1",
            crisis_type=_infer_crisis_type(scenario_data["category"]),
            specific_context=scenario_data["context"],
            trauma_type=_infer_trauma_type(scenario_data["issue_type"]),
            symbolic_type="traditional" if scenario_data["complexity"] == "critical" else "minimal"
        )
        
        # Generate tier 2 response with appropriate resources
        resource_info, action_steps = _generate_resources_for_scenario(scenario_data)
        
        tier2_response = library.build_complete_response(
            tier="tier_2",
            crisis_type=_infer_crisis_type(scenario_data["category"]),
            specific_context=scenario_data["context"],
            resource_info=resource_info,
            action_steps=action_steps,
            symbolic_type="minimal"
        )
        
        # Create entry
        entry = generator.generate_entry(
            scenario_name=scenario_data["name"],
            category=scenario_data["category"],
            complexity=scenario_data["complexity"],
            issue_type=scenario_data["issue_type"],
            tenant_message1=scenario_data["messages"][0],
            willow_response1=tier1_response,
            tenant_message2=scenario_data["messages"][1],
            willow_response2=tier2_response,
            initial_arousal=scenario_data["arousal"],
            initial_capacity=scenario_data["capacity"],
            tier1_technique=_select_technique_for_scenario(scenario_data, "tier1"),
            tier2_technique=_select_technique_for_scenario(scenario_data, "tier2"),
            arousal_impacts=(-1.2, -0.8) if scenario_data["complexity"] == "critical" else (-1.0, -0.6),
            resolution_status=_determine_resolution_status(scenario_data),
            escalation_path=_determine_escalation_path(scenario_data)
        )
        
        all_entries.append(entry)
    
    return all_entries

def _infer_crisis_type(category: str) -> str:
    """Map category to crisis type for response library."""
    mapping = {
        "maintenance_crisis": "maintenance_emergency",
        "eviction": "financial_crisis",
        "health_safety": "medical_emergency",
        "discrimination": "discrimination",
        "financial_distress": "financial_crisis",
        "intersectional_vulnerability": "family_crisis",
        "legal_notice": "family_crisis"
    }
    return mapping.get(category, "financial_crisis")

def _infer_trauma_type(issue_type: str) -> str:
    """Map issue type to trauma type."""
    mapping = {
        "multiple_barriers": "compound_trauma",
        "financial_instability": "systemic_abandonment",
        "safety_threat": "chronic_crisis",
        "emotional_overload": "identity_violence"
    }
    return mapping.get(issue_type, "systemic_abandonment")

def _generate_resources_for_scenario(scenario: Dict) -> tuple:
    """Generate appropriate resources and action steps for scenario."""
    
    # Resource mapping based on category
    resource_map = {
        "eviction": {
            "type": "legal_support",
            "specific_org": "Housing Justice Project",
            "specific_issue": "eviction defense",
            "similar_situation": "emergency evictions",
            "contact": "1-800-EVICTION"
        },
        "discrimination": {
            "type": "legal_support",
            "specific_org": "Fair Housing Center",
            "specific_issue": "housing discrimination",
            "similar_situation": "identity-based harassment",
            "contact": "fairhousing.org/emergency"
        },
        "health_safety": {
            "type": "medical_advocacy",
            "Medical_legal_org": "Health Justice Alliance",
            "medical_condition": "your condition",
            "disability_org": "Disability Rights Center",
            "health_issue": "medical needs",
            "Health_justice_org": "Medical-Legal Partnership"
        },
        "financial_distress": {
            "type": "emergency_assistance",
            "need": "rent assistance",
            "organization": "Emergency Rental Assistance Program",
            "timeframe": "48-72 hours",
            "specific_help": "one-time payment",
            "contact": "211 or renthelp.org"
        }
    }
    
    # Action mapping
    action_map = {
        "eviction": {
            "type": "rights_assertion",
            "specific_right": "proper notice and court process",
            "law/code": "state tenant protection laws",
            "their_action": "attempting illegal eviction"
        },
        "discrimination": {
            "type": "documentation",
            "condition": "discrimination",
            "communication": "all discriminatory statements",
            "events": "each incident",
            "pattern": "the discrimination",
            "evidence": "all harassment"
        },
        "maintenance_crisis": {
            "type": "staged_approach",
            "immediate_action": "document conditions",
            "medium_action": "formal repair request",
            "long_action": "code enforcement complaint"
        }
    }
    
    resource_info = resource_map.get(scenario["category"], resource_map["financial_distress"])
    action_steps = action_map.get(scenario["category"], action_map["eviction"])
    
    return resource_info.copy(), action_steps.copy()

def _select_technique_for_scenario(scenario: Dict, tier: str) -> str:
    """Select appropriate technique based on scenario."""
    
    if tier == "tier1":
        technique_map = {
            "maintenance_crisis": ["dual_danger_recognition", "bureaucratic_harm_naming", "dignity_validation"],
            "eviction": ["system_abandonment_naming", "medical_injustice_witnessing", "disaster_timeline_validation"],
            "discrimination": ["identity_affirmation", "discrimination_timing_reveal", "transformation_invisibility_naming"],
            "health_safety": ["medical_injustice_witnessing", "dual_danger_recognition", "disaster_timeline_validation"],
            "financial_distress": ["system_abandonment_naming", "bureaucratic_harm_naming", "separation_grief_holding"],
            "intersectional_vulnerability": ["separation_grief_holding", "paradox_witnessing", "generational_burden_witnessing"],
            "legal_notice": ["bureaucratic_harm_naming", "system_abandonment_naming", "dual_danger_recognition"]
        }
    else:  # tier2
        technique_map = {
            "maintenance_crisis": ["evidence_building", "rights_reinforcement", "multi_pathway_support"],
            "eviction": ["medical_legal_support", "multi_pathway_support", "disaster_resource_bridging"],
            "discrimination": ["fair_housing_enforcement", "community_resource_mapping", "coded_discrimination_decoding"],
            "health_safety": ["medical_legal_support", "safety_pathway_mapping", "specialized_intervention_pathway"],
            "financial_distress": ["multi_pathway_support", "benefits_legal_intersection", "disaster_resource_bridging"],
            "intersectional_vulnerability": ["family_preservation_support", "immigration_crisis_resources", "multi_pathway_support"],
            "legal_notice": ["rights_reinforcement", "evidence_building", "multi_pathway_support"]
        }
    
    techniques = technique_map.get(scenario["category"], ["general_validation"])
    return techniques[hash(scenario["name"]) % len(techniques)]

def _determine_resolution_status(scenario: Dict) -> str:
    """Determine resolution status based on scenario."""
    status_map = {
        "critical": ["defending", "protecting", "stabilizing"],
        "high": ["supporting", "planning", "organizing"],
        "medium": ["redirecting", "planning", "supporting"]
    }
    
    statuses = status_map.get(scenario["complexity"], ["supporting"])
    return statuses[hash(scenario["name"]) % len(statuses)]

def _determine_escalation_path(scenario: Dict) -> str:
    """Determine escalation path based on scenario."""
    path_map = {
        "eviction": "legal_aid_referral",
        "discrimination": "fair_housing_enforcement",
        "maintenance_crisis": "code_enforcement",
        "health_safety": "emergency_services",
        "financial_distress": "emergency_assistance",
        "intersectional_vulnerability": "multi_system_advocacy",
        "legal_notice": "legal_consultation"
    }
    
    return path_map.get(scenario["category"], "crisis_support")

def main():
    """Generate and save the batch."""
    print("Generating 50 Willow entries...")
    
    entries = generate_batch_50()
    
    # Save to file
    filename = "willow_batch_50_entries.jsonl"
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Generated {len(entries)} entries")
    print(f"Saved to {filename}")
    
    # Print summary statistics
    categories = {}
    complexities = {}
    techniques = set()
    
    for entry in entries:
        cat = entry["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
        comp = entry["complexity_level"]
        complexities[comp] = complexities.get(comp, 0) + 1
        
        for msg in entry["messages"]:
            if msg["role"] == "willow" and "technique" in msg:
                techniques.add(msg["technique"])
    
    print("\nSummary Statistics:")
    print(f"Categories: {categories}")
    print(f"Complexity Levels: {complexities}")
    print(f"Unique Techniques Used: {len(techniques)}")
    print(f"ID Range: {entries[0]['id']} - {entries[-1]['id']}")

if __name__ == "__main__":
    main()