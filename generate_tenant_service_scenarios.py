#!/usr/bin/env python3
"""
Generate 100 unique tenant service scenarios for Willow
Focus on emotional containment and practical solutions
"""

import json
import random

# Define diverse scenario categories with emotional states
FACILITY_ISSUES = [
    ("squeaky_door", "My door is making a strange squeaking noise when I open it", 4.0, 7.5),
    ("stuck_window", "Window in bedroom won't open, feels painted shut", 4.5, 7.0),
    ("flickering_lights", "Kitchen lights keep flickering on and off", 5.0, 6.8),
    ("loose_doorknob", "Front door handle feels loose and wobbly", 4.8, 7.2),
    ("cracked_wall", "There's a new crack in my living room wall", 5.5, 6.5),
    ("peeling_wallpaper", "Wallpaper in bathroom starting to peel from steam", 3.8, 7.8),
    ("drafty_windows", "Cold air coming through bedroom windows", 4.2, 7.4),
    ("sticky_locks", "Key gets stuck in the lock sometimes", 4.6, 7.1),
    ("uneven_floor", "Floor feels uneven near the kitchen", 4.3, 7.3),
    ("cabinet_alignment", "Kitchen cabinets don't close properly anymore", 4.1, 7.5),
]

APPLIANCE_PROBLEMS = [
    ("dishwasher_noise", "Dishwasher making grinding noise during cycles", 4.7, 7.0),
    ("fridge_warm", "Refrigerator doesn't seem cold enough", 6.0, 6.2),
    ("stove_burner", "One stove burner won't light properly", 5.2, 6.8),
    ("washer_shaking", "Washing machine shakes violently during spin", 5.5, 6.5),
    ("disposal_smell", "Garbage disposal has bad odor", 4.4, 7.2),
    ("microwave_buttons", "Some microwave buttons stopped working", 4.0, 7.6),
    ("dryer_lint", "Dryer taking forever, think lint trap needs cleaning", 3.9, 7.7),
    ("freezer_frost", "Freezer has excessive frost buildup", 4.3, 7.3),
    ("oven_smoke", "Oven smokes when I use it", 5.8, 6.4),
    ("ac_filter", "AC making weird noise, maybe filter needs changing?", 4.5, 7.1),
]

NOISE_CONCERNS = [
    ("upstairs_footsteps", "Upstairs neighbor walks loudly at night", 5.5, 6.5),
    ("dog_barking", "Neighbor's dog barks constantly when they leave", 5.8, 6.2),
    ("music_late", "Next door plays music past quiet hours", 6.0, 6.0),
    ("construction_early", "Construction noise starting before 7am", 6.5, 5.8),
    ("hallway_echo", "Hallway echoes are really loud", 4.2, 7.4),
    ("thin_walls", "Can hear everything through the walls", 5.3, 6.7),
    ("party_noise", "Weekly parties in apartment 3B", 6.2, 5.9),
    ("mechanical_hum", "Strange humming noise from building at night", 4.8, 7.0),
    ("door_slamming", "Neighbors constantly slam their doors", 5.1, 6.8),
    ("parking_lot", "Cars revving engines in parking lot late", 5.4, 6.6),
]

ACCESS_REQUESTS = [
    ("lost_fob", "Lost my key fob for the gym", 3.5, 7.8),
    ("package_room", "Can't access package room with my code", 4.0, 7.5),
    ("roof_deck", "How do I get access to the roof deck?", 3.0, 8.2),
    ("storage_key", "Need a key for my storage unit", 3.3, 7.9),
    ("bike_room", "Bike room code isn't working", 3.8, 7.6),
    ("pool_hours", "What are the pool hours this season?", 2.8, 8.4),
    ("guest_passes", "How do I get guest parking passes?", 3.2, 8.0),
    ("mailbox_combo", "Forgot my mailbox combination", 4.2, 7.4),
    ("laundry_card", "Laundry card not working properly", 4.5, 7.2),
    ("elevator_access", "Need after-hours elevator access for move", 3.6, 7.7),
]

POLICY_QUESTIONS = [
    ("pet_registration", "How do I register my new cat?", 3.0, 8.2),
    ("subletting_rules", "Can I sublet for two months?", 3.5, 7.8),
    ("decoration_policy", "Am I allowed to paint the walls?", 3.2, 8.0),
    ("quiet_hours", "What exactly are the quiet hours?", 3.4, 7.9),
    ("visitor_policy", "How long can guests stay over?", 3.1, 8.1),
    ("parking_rules", "Can I have two cars with one apartment?", 3.6, 7.7),
    ("balcony_rules", "Are grills allowed on balconies?", 3.3, 7.9),
    ("move_out_notice", "How much notice for moving out?", 3.7, 7.6),
    ("rent_grace_period", "Is there a grace period for rent?", 4.0, 7.5),
    ("security_deposit", "When do I get my deposit back?", 3.8, 7.6),
]

MAINTENANCE_SCHEDULING = [
    ("annual_inspection", "When is my annual inspection?", 3.0, 8.2),
    ("filter_replacement", "Can someone change my AC filter?", 3.2, 8.0),
    ("pest_prevention", "Can I schedule preventive pest control?", 3.5, 7.8),
    ("carpet_cleaning", "Is carpet cleaning included?", 3.3, 7.9),
    ("window_washing", "When do windows get cleaned?", 3.1, 8.1),
    ("paint_touch_up", "Can maintenance do paint touch-ups?", 3.4, 7.9),
    ("caulking_tub", "Bathtub needs re-caulking", 3.8, 7.6),
    ("gutter_cleaning", "Are gutters cleaned regularly?", 3.2, 8.0),
    ("smoke_detector", "Smoke detector beeping needs battery", 4.5, 7.2),
    ("thermostat_check", "Thermostat seems off, can someone check?", 3.9, 7.5),
]

EMERGENCY_CONCERNS = [
    ("water_leak", "Water dripping from ceiling!", 7.0, 5.5),
    ("power_outage", "Lost power in half my apartment", 6.5, 5.8),
    ("gas_smell", "Smell gas near the stove", 8.0, 5.0),
    ("locked_out", "Locked myself out of apartment", 6.0, 6.0),
    ("broken_glass", "Window shattered during storm", 7.5, 5.3),
    ("flooding_bathroom", "Toilet overflowing won't stop", 8.5, 4.8),
    ("no_heat_winter", "Heat stopped working and it's freezing", 7.8, 5.2),
    ("smoke_alarm", "Smoke alarm won't stop beeping", 6.8, 5.6),
    ("door_wont_lock", "Front door won't lock properly", 7.2, 5.4),
    ("elevator_stuck", "Elevator stopped between floors with me in it", 8.2, 4.9),
]

PERSONAL_SITUATIONS = [
    ("work_from_home", "Need quiet for important calls, construction loud", 5.0, 6.8),
    ("new_baby", "Just had a baby, worried about noise complaints", 5.5, 6.5),
    ("medical_equipment", "Need reliable power for medical equipment", 6.0, 6.2),
    ("elderly_parent", "Elderly parent visiting, needs grab bars", 4.5, 7.2),
    ("anxiety_crowds", "Anxious about crowded laundry room", 5.2, 6.7),
    ("night_shift", "Work nights, daytime noise affecting sleep", 5.8, 6.3),
    ("disability_access", "Need wheelchair ramp for entrance", 4.8, 7.0),
    ("recovery_surgery", "Recovering from surgery, stairs difficult", 5.3, 6.6),
    ("pet_anxiety", "Dog has separation anxiety, neighbors complaining", 6.2, 5.9),
    ("financial_hardship", "Lost job, worried about next month's rent", 7.0, 5.5),
]

COMMUNITY_ISSUES = [
    ("package_theft", "Packages keep disappearing from lobby", 5.5, 6.5),
    ("parking_disputes", "Someone keeps taking my assigned spot", 5.8, 6.2),
    ("common_area_mess", "People leaving trash in hallways", 5.0, 6.8),
    ("smoking_violations", "Smell smoke in non-smoking building", 5.6, 6.4),
    ("unauthorized_access", "Strangers in building without buzzing", 6.0, 6.0),
    ("graffiti_vandalism", "Graffiti appeared on garage wall", 4.8, 7.0),
    ("bike_theft", "Bikes being stolen from bike room", 6.2, 5.9),
    ("dumpster_overflow", "Dumpsters always overflowing", 4.5, 7.2),
    ("lighting_safety", "Parking lot too dark at night", 5.3, 6.6),
    ("snow_removal", "Walkways icy and dangerous", 6.5, 5.8),
]

COMFORT_REQUESTS = [
    ("temperature_control", "Apartment always too hot even with AC", 4.5, 7.2),
    ("humidity_issues", "Apartment feels very humid", 4.2, 7.4),
    ("ventilation_poor", "Bathroom has no ventilation", 4.6, 7.1),
    ("natural_light", "Can I add skylights for more light?", 3.5, 7.8),
    ("soundproofing", "Can anything be done about noise?", 5.0, 6.8),
    ("air_quality", "Air feels stuffy, any solutions?", 4.3, 7.3),
    ("water_pressure", "Shower pressure really weak", 4.4, 7.2),
    ("closet_space", "Need more storage solutions", 3.8, 7.6),
    ("outdoor_space", "Can I use the courtyard for plants?", 3.2, 8.0),
    ("workspace_needs", "Need better lighting for home office", 3.9, 7.5),
]

def generate_scenario(entry_id: str, scenario_data: tuple, category: str) -> dict:
    """Generate a complete scenario with emotional intelligence"""
    scenario_name, issue, initial_arousal, initial_capacity = scenario_data
    
    messages = []
    
    # Initial tenant message
    messages.append({
        "role": "tenant",
        "content": issue,
        "arousal": initial_arousal,
        "capacity": initial_capacity
    })
    
    # Generate Willow's Tier 1 response based on category and arousal level
    if initial_arousal >= 7.0:  # Emergency level
        acknowledgment = "I can hear this is really urgent and stressful for you."
        solution = "I'm immediately contacting our emergency maintenance team."
        technique = "emergency_containment"
        arousal_impact = -1.5
    elif initial_arousal >= 5.5:  # High concern
        acknowledgment = "I completely understand your frustration with this situation."
        solution = "Let me get this resolved for you right away."
        technique = "active_validation"
        arousal_impact = -1.0
    elif initial_arousal >= 4.0:  # Moderate concern
        acknowledgment = "I understand how this can be bothersome."
        solution = "I'll make sure we address this promptly."
        technique = "empathetic_acknowledgment"
        arousal_impact = -0.8
    else:  # Low concern
        acknowledgment = "Thanks for bringing this to my attention."
        solution = "I'll help you with that right away."
        technique = "friendly_assistance"
        arousal_impact = -0.5
    
    # Customize solution based on category
    if category == "emergency":
        specific_solution = f"Our emergency team will be there within the hour. In the meantime, {get_emergency_advice(scenario_name)}."
    elif category == "noise":
        specific_solution = f"I'll document this and speak with the involved parties. We take noise complaints seriously and will work on a resolution."
    elif category == "personal":
        specific_solution = f"I understand your situation completely. Let me connect you with the right resources and accommodations."
    elif category == "policy":
        specific_solution = f"Great question! {get_policy_info(scenario_name)}. I'll also send you the detailed policy document."
    else:
        specific_solution = f"I'll create a maintenance ticket for this right now. {get_timeline(initial_arousal)}."
    
    tier1_response = f"{acknowledgment} {solution} {specific_solution}"
    
    messages.append({
        "role": "willow",
        "content": tier1_response,
        "tier": "tier_1",
        "technique": technique,
        "arousal_impact": arousal_impact
    })
    
    # Calculate new emotional state
    new_arousal = max(2.0, initial_arousal + arousal_impact)
    new_capacity = min(9.0, initial_capacity + 0.5)
    
    # Add tenant follow-up (70% of time)
    if random.random() < 0.7:
        follow_ups = [
            "Thank you so much for your help!",
            "That's really helpful, I appreciate it.",
            "Oh good, that makes me feel better.",
            "Thanks for understanding.",
            "Great, when should I expect to hear back?",
            "Perfect, that's exactly what I needed.",
            "I really appreciate your quick response.",
            "That's a relief, thank you."
        ]
        
        messages.append({
            "role": "tenant",
            "content": random.choice(follow_ups),
            "arousal": new_arousal,
            "capacity": new_capacity
        })
        
        # Tier 2 response - reassurance and follow-up
        tier2_responses = [
            "You're very welcome! I'll send you a confirmation email with all the details shortly.",
            "My pleasure! I'll personally follow up to ensure everything is resolved properly.",
            "Happy to help! You should receive an update within 24 hours.",
            "Of course! I'm here whenever you need assistance.",
            "Absolutely! I'll make sure this gets priority attention.",
            "You're all set! Feel free to reach out if you need anything else.",
            "I'm glad I could help! I'll monitor this to ensure it's resolved quickly.",
            "It's my pleasure! I'll keep you updated throughout the process."
        ]
        
        messages.append({
            "role": "willow",
            "content": random.choice(tier2_responses),
            "tier": "tier_2",
            "technique": "reassurance_closure",
            "arousal_impact": -0.3
        })
        
        new_arousal = max(2.0, new_arousal - 0.3)
        new_capacity = min(9.0, new_capacity + 0.2)
    
    # Build arousal and capacity curves
    arousal_curve = [initial_arousal]
    capacity_curve = [initial_capacity]
    
    current_arousal = initial_arousal
    current_capacity = initial_capacity
    
    for msg in messages[1:]:
        if msg['role'] == 'willow' and 'arousal_impact' in msg:
            current_arousal = max(2.0, current_arousal + msg['arousal_impact'])
        elif msg['role'] == 'tenant' and 'arousal' in msg:
            current_arousal = msg['arousal']
            current_capacity = msg.get('capacity', current_capacity)
        
        arousal_curve.append(current_arousal)
        capacity_curve.append(current_capacity)
    
    # Determine containment quality
    arousal_reduction = initial_arousal - current_arousal
    if arousal_reduction >= 2.0:
        containment_quality = "excellent"
    elif arousal_reduction >= 1.0:
        containment_quality = "good"
    else:
        containment_quality = "adequate"
    
    return {
        "id": entry_id,
        "scenario": scenario_name,
        "category": category,
        "initial_state": {
            "arousal": initial_arousal,
            "capacity": initial_capacity,
            "issue_type": category
        },
        "messages": messages,
        "process_metrics": {
            "tier_progression": ["tier_1"] if len(messages) == 2 else ["tier_1", "tier_2"],
            "arousal_curve": arousal_curve,
            "capacity_curve": capacity_curve,
            "containment_quality": containment_quality,
            "resolution_effectiveness": "high" if current_arousal < 4.0 else "moderate"
        }
    }

def get_emergency_advice(scenario: str) -> str:
    """Get scenario-specific emergency advice"""
    advice = {
        "water_leak": "please turn off the water valve if you can safely access it",
        "power_outage": "avoid opening the refrigerator and unplug sensitive electronics",
        "gas_smell": "please open windows and avoid using any electrical switches",
        "locked_out": "please wait in a safe area like the lobby",
        "broken_glass": "please stay away from the broken glass area for safety",
        "flooding_bathroom": "turn off the water valve behind the toilet if possible",
        "no_heat_winter": "I'll also bring some space heaters as a temporary solution",
        "smoke_alarm": "if there's no actual smoke, you can temporarily silence it",
        "door_wont_lock": "please stay safe, someone will be there very soon",
        "elevator_stuck": "press the emergency button, help is on the way"
    }
    return advice.get(scenario, "please stay safe while we handle this")

def get_policy_info(scenario: str) -> str:
    """Get scenario-specific policy information"""
    policies = {
        "pet_registration": "You'll need to fill out a pet form and pay a $300 deposit",
        "subletting_rules": "Subletting requires written approval and tenant screening",
        "decoration_policy": "Painting is allowed with approved colors and professional work",
        "quiet_hours": "Quiet hours are 10 PM to 7 AM on weekdays, 11 PM to 8 AM weekends",
        "visitor_policy": "Guests can stay up to 14 consecutive days",
        "parking_rules": "Each unit is entitled to one spot, additional spots are $75/month",
        "balcony_rules": "Electric grills only, no charcoal or open flames",
        "move_out_notice": "We require 60 days written notice before move-out",
        "rent_grace_period": "There's a 5-day grace period with no late fee",
        "security_deposit": "Deposits are returned within 30 days with an itemized statement"
    }
    return policies.get(scenario, "Let me get you the specific policy details")

def get_timeline(arousal: float) -> str:
    """Get appropriate timeline based on urgency"""
    if arousal >= 6.0:
        return "Someone will be there within 2-4 hours"
    elif arousal >= 4.5:
        return "We'll have someone look at this within 24 hours"
    else:
        return "This will be addressed within 2-3 business days"

def main():
    """Generate 100 unique tenant service scenarios"""
    all_scenarios = []
    
    # Combine all categories
    scenarios_by_category = [
        ("facility", FACILITY_ISSUES),
        ("appliance", APPLIANCE_PROBLEMS),
        ("noise", NOISE_CONCERNS),
        ("access", ACCESS_REQUESTS),
        ("policy", POLICY_QUESTIONS),
        ("maintenance", MAINTENANCE_SCHEDULING),
        ("emergency", EMERGENCY_CONCERNS),
        ("personal", PERSONAL_SITUATIONS),
        ("community", COMMUNITY_ISSUES),
        ("comfort", COMFORT_REQUESTS)
    ]
    
    # Generate entries
    entry_num = 101  # Starting from WILLOW_101
    
    # First pass - one from each category to ensure diversity
    for category, scenarios in scenarios_by_category:
        for scenario in scenarios[:10]:  # Take all 10 from each category
            entry_id = f"WILLOW_{entry_num}"
            entry = generate_scenario(entry_id, scenario, category)
            all_scenarios.append(entry)
            entry_num += 1
            
            if entry_num > 200:  # Stop at 100 entries
                break
        if entry_num > 200:
            break
    
    # Write to file
    with open('willow_service_scenarios_100.jsonl', 'w') as f:
        for entry in all_scenarios:
            f.write(json.dumps(entry) + '\n')
    
    # Print summary statistics
    print(f"Generated {len(all_scenarios)} tenant service scenarios")
    print("\nCategory distribution:")
    category_counts = {}
    for entry in all_scenarios:
        cat = entry['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat.capitalize()}: {count}")
    
    print("\nArousal level distribution:")
    arousal_ranges = {"Low (2-4)": 0, "Medium (4-6)": 0, "High (6-8)": 0, "Critical (8+)": 0}
    for entry in all_scenarios:
        arousal = entry['initial_state']['arousal']
        if arousal < 4:
            arousal_ranges["Low (2-4)"] += 1
        elif arousal < 6:
            arousal_ranges["Medium (4-6)"] += 1
        elif arousal < 8:
            arousal_ranges["High (6-8)"] += 1
        else:
            arousal_ranges["Critical (8+)"] += 1
    
    for range_name, count in arousal_ranges.items():
        print(f"  {range_name}: {count}")
    
    print("\nContainment quality:")
    quality_counts = {}
    for entry in all_scenarios:
        quality = entry['process_metrics']['containment_quality']
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
    
    for quality, count in sorted(quality_counts.items()):
        print(f"  {quality.capitalize()}: {count}")
    
    print("\nSaved to: willow_service_scenarios_100.jsonl")

if __name__ == "__main__":
    main()