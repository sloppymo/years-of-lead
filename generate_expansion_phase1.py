#!/usr/bin/env python3
"""
Generate Phase 1 of WILLOW corpus expansion (200 entries)
Focus: High-priority crisis and safety scenarios
"""

import json
import random
from datetime import datetime
from typing import Dict, List

# Crisis scenarios and responses
CRISIS_SCENARIOS = {
    "earthquake": {
        "user_messages": [
            "The building is shaking! Is this an earthquake? What should I do?!",
            "I felt strong tremors and heard cracking sounds from the walls! Help!",
            "Everything is falling off my shelves! I'm under my table - is that right?"
        ],
        "tier1_responses": [
            "I hear you're experiencing an earthquake. Your safety is my immediate priority. You did exactly the right thing by getting under a sturdy table. Stay there until the shaking completely stops.",
            "I understand how frightening this is. You're doing great by staying calm enough to reach out. Drop, cover, and hold on - stay under that table and protect your head and neck."
        ],
        "tier2_responses": [
            "The shaking has stopped. Here's what to do next: First, carefully check yourself for injuries. Then, if you smell gas, don't use any electrical switches or flames. I'm dispatching emergency maintenance to check all units for gas leaks right now.",
            "I'm activating our emergency response protocol immediately. Our team will be doing door-to-door safety checks within 15 minutes. If your door is jammed, they'll help you exit safely. Stay away from windows and don't try to force the door yourself."
        ]
    },
    "flood": {
        "user_messages": [
            "Water is coming into my apartment from everywhere! It's already ankle deep!",
            "The river behind our building is overflowing! Water is in the parking garage!",
            "Flash flood warning! Water is rising fast and I'm on the ground floor!"
        ],
        "tier1_responses": [
            "I understand you're dealing with flooding - this is an emergency situation. Your safety comes first. Are you able to get to higher ground safely?",
            "I hear the urgency in your message about the flooding. This is extremely serious and I'm taking immediate action. First, let's make sure you're safe."
        ],
        "tier2_responses": [
            "I'm dispatching our emergency team immediately and contacting emergency services. Move to the highest floor possible right now - take your phone, medications, and important documents if you can grab them quickly. Don't use elevators.",
            "Emergency flood protocol activated. Our team will arrive in 10 minutes to assist with evacuation. Turn off electricity at the breaker if you can safely access it. Move all valuables to high shelves or upper floors now."
        ]
    },
    "fire": {
        "user_messages": [
            "I smell smoke in the hallway and the fire alarm is going off!",
            "There's smoke coming under my door! Should I evacuate?",
            "Fire in the apartment next door! I can hear screaming!"
        ],
        "tier1_responses": [
            "Fire alarm activation is serious. I need you to evacuate immediately using the stairs, not the elevator. Your safety is the only priority right now.",
            "If you smell smoke, this is a real emergency. Don't wait - evacuate now using the nearest stairwell. Take your keys and phone but don't gather belongings."
        ],
        "tier2_responses": [
            "I'm calling 911 right now and activating full building evacuation. Use the stairs to exit immediately. Meet at the designated assembly point in the parking lot. Don't go back inside for any reason.",
            "Fire department is on the way. If you can't evacuate, seal your door with wet towels, go to a window, and signal for help. I'm staying on the line with you and relaying your location to responders."
        ]
    },
    "heart_attack": {
        "user_messages": [
            "My chest hurts so bad and my arm is numb! I think I'm having a heart attack!",
            "My neighbor collapsed clutching his chest! He's conscious but in pain!",
            "Severe chest pressure and I can't breathe properly! I'm alone and scared!"
        ],
        "tier1_responses": [
            "I understand you're experiencing severe chest pain. This could be a medical emergency and we need to get you help immediately. I'm going to help you through this.",
            "I hear you and I'm taking this very seriously. Chest pain with numbness needs immediate medical attention. You're not alone - I'm here with you."
        ],
        "tier2_responses": [
            "I'm calling 911 immediately. While we wait: Sit down and try to stay calm. If you have aspirin, chew one regular aspirin now unless you're allergic. Unlock your door if possible so paramedics can enter. I'm staying with you.",
            "Emergency services are on the way - ETA 5 minutes. Loosen any tight clothing, sit upright, and breathe slowly. If you have nitroglycerin prescribed, take it now. I'm notifying building security to guide paramedics directly to you."
        ]
    },
    "break_in": {
        "user_messages": [
            "Someone is trying to break into my apartment RIGHT NOW! I hear them at the door!",
            "I just came home and my door was forced open! I'm afraid to go inside!",
            "There's someone in my apartment! I'm hiding in the bedroom closet!"
        ],
        "tier1_responses": [
            "I understand you're in immediate danger. Your safety is the absolute priority. I'm getting help to you right now. Are you in a safe location?",
            "This is terrifying and you did the right thing calling for help. I'm taking immediate action. First, let's make sure you're safe."
        ],
        "tier2_responses": [
            "I'm calling 911 immediately and dispatching building security. Stay hidden and silent. Keep your phone on silent but stay on this line. Police ETA is 4 minutes. Security will be there in 90 seconds.",
            "Police are on the way - I've given them your exact location. Do NOT enter your apartment. Go to a neighbor you trust or wait in a safe, visible area. Building security is coming to meet you right now."
        ]
    },
    "power_outage": {
        "user_messages": [
            "Power just went out in the whole building! My medical equipment needs electricity!",
            "Complete blackout and I'm stuck in the elevator! Getting hard to breathe!",
            "No power for 3 hours now and my insulin needs refrigeration! What do I do?"
        ],
        "tier1_responses": [
            "I understand you have medical equipment that needs power. This is urgent and I'm treating it as a medical emergency. Let me help you immediately.",
            "Being stuck in an elevator during a power outage is terrifying. I'm here with you and getting help right now. Try to stay calm and breathe slowly."
        ],
        "tier2_responses": [
            "I'm dispatching our emergency generator team to set up temporary power for your medical equipment within 15 minutes. I'm also calling your power company to report a medical emergency. Do you have backup batteries? We can bring some.",
            "Elevator emergency rescue has been called - ETA 10 minutes. Building maintenance is manually cranking the elevator to the nearest floor right now. Keep talking to me. Breathe slowly - there's plenty of air."
        ]
    }
}

def generate_tenant_entry(entry_id: str, scenario_type: str, scenario_data: Dict) -> Dict:
    """Generate a tenant-facing entry"""
    
    # Select random messages
    user_msg1 = random.choice(scenario_data["user_messages"])
    tier1_response = random.choice(scenario_data["tier1_responses"])
    tier2_response = random.choice(scenario_data["tier2_responses"])
    
    # Build conversation
    messages = [
        {"role": "user", "content": user_msg1},
        {"role": "assistant", "content": tier1_response, "metadata": {"tier": "tier_1"}},
        {"role": "user", "content": "What should I do now? How long until help arrives?"},
        {"role": "assistant", "content": tier2_response, "metadata": {"tier": "tier_2"}}
    ]
    
    # Determine category
    if scenario_type in ["earthquake", "flood", "fire"]:
        category = "natural_disaster"
    elif scenario_type in ["heart_attack"]:
        category = "medical_emergency"
    elif scenario_type in ["break_in"]:
        category = "security_threat"
    else:
        category = "utility_failure"
    
    return {
        "id": entry_id,
        "user_type": "tenant",
        "category": f"{category}_{scenario_type}",
        "scenario": f"Emergency response: {scenario_type}",
        "messages": messages,
        "complexity_level": "critical",
        "tags": {
            "urgency_level": "immediate",
            "primary_emotion": "fear",
            "legal_risk_level": "high" if scenario_type == "break_in" else "medium",
            "topics": ["emergency", "safety", scenario_type]
        },
        "metadata": {
            "generated_date": datetime.now().isoformat(),
            "expansion_batch": "phase_1"
        }
    }

def generate_staff_entry(entry_id: str, scenario_type: str, scenario_data: Dict) -> Dict:
    """Generate a staff training entry"""
    
    # Build staff training conversation
    messages = [
        {"role": "resident", "content": random.choice(scenario_data["user_messages"])},
        {"role": "staff", "content": random.choice(scenario_data["tier1_responses"]), "tier": "tier_1"},
        {"role": "resident", "content": "Please help me! What's taking so long?"},
        {"role": "staff", "content": random.choice(scenario_data["tier2_responses"]), "tier": "tier_2"},
        {"role": "resident", "content": "Thank you. I'm still scared but that helps."},
        {"role": "staff", "content": "You're being so brave. Help is almost there - just 2 more minutes. I'm staying with you.", "tier": "tier_2"}
    ]
    
    return {
        "id": entry_id,
        "user_type": "staff",
        "category": f"{scenario_type}_response_training",
        "scenario": f"Staff training: {scenario_type} emergency",
        "messages": messages,
        "complexity_level": "high",
        "training_objectives": [
            f"Respond appropriately to {scenario_type} emergencies",
            "Apply two-tier response system",
            "Maintain calm under extreme stress",
            "Coordinate emergency services"
        ],
        "routing_logic": {
            "primary_indicators": [f"{scenario_type}_keywords", "emergency", "immediate_danger"],
            "escalation_triggers": ["life_threat", "multiple_affected", "spreading_danger"],
            "required_notifications": ["911", "building_management", "security"]
        },
        "tags": {
            "urgency_level": "immediate",
            "primary_emotion": "fear",
            "topics": ["emergency", "training", scenario_type]
        }
    }

def generate_phase1_entries():
    """Generate 200 Phase 1 entries"""
    
    entries = []
    entry_counter = 2400  # Start after existing corpus
    
    # Distribution of scenarios
    scenario_counts = {
        "earthquake": 25,
        "flood": 25,
        "fire": 25,
        "heart_attack": 25,
        "break_in": 25,
        "power_outage": 25
    }
    
    # Generate additional scenarios to reach 200
    additional_scenarios = ["stroke", "gas_leak", "domestic_violence", "fall_injury"]
    for scenario in additional_scenarios:
        scenario_counts[scenario] = 12
    
    print("Generating Phase 1 expansion entries...")
    print("-" * 60)
    
    for scenario_type, count in scenario_counts.items():
        print(f"Generating {scenario_type}: {count} entries", end="", flush=True)
        
        # Use existing data or create simple version
        if scenario_type in CRISIS_SCENARIOS:
            scenario_data = CRISIS_SCENARIOS[scenario_type]
        else:
            # Create basic scenario data for additional types
            scenario_data = {
                "user_messages": [f"Emergency! I need help with {scenario_type}!"],
                "tier1_responses": ["I understand this is an emergency. Your safety is my priority. I'm here to help."],
                "tier2_responses": ["I'm dispatching help immediately. Emergency services are on the way."]
            }
        
        for i in range(count):
            # 70% tenant, 30% staff
            if random.random() < 0.7:
                entry_id = f"WILLOW_{entry_counter}"
                entry = generate_tenant_entry(entry_id, scenario_type, scenario_data)
            else:
                entry_id = f"WILLOW_STAFF_{entry_counter}"
                entry = generate_staff_entry(entry_id, scenario_type, scenario_data)
            
            entries.append(entry)
            entry_counter += 1
        
        print(" ✓")
    
    return entries

def main():
    """Main execution"""
    
    print("WILLOW Corpus Expansion - Phase 1")
    print("=" * 60)
    
    # Generate entries
    entries = generate_phase1_entries()
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"willow_expansion_phase1_{timestamp}.jsonl"
    
    print(f"\nWriting {len(entries)} entries to {output_file}...")
    with open(output_file, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Create summary
    summary_file = f"expansion_phase1_summary_{timestamp}.md"
    with open(summary_file, 'w') as f:
        f.write("# WILLOW Expansion Phase 1 Summary\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Entries**: {len(entries)}\n")
        f.write(f"**Output File**: `{output_file}`\n\n")
        f.write("## Scenarios Generated\n\n")
        
        # Count by scenario type
        scenario_counts = {}
        for entry in entries:
            category = entry.get("category", "unknown")
            scenario_counts[category] = scenario_counts.get(category, 0) + 1
        
        for scenario, count in sorted(scenario_counts.items()):
            f.write(f"- {scenario}: {count} entries\n")
        
        f.write("\n## Key Features\n")
        f.write("- Two-tier response system (containment → action)\n")
        f.write("- Immediate emergency protocols\n")
        f.write("- Trauma-informed language\n")
        f.write("- Clear timelines and actions\n")
        f.write("- Mix of tenant (70%) and staff (30%) entries\n")
    
    print(f"✓ Summary saved to: {summary_file}")
    print(f"\n✅ Successfully generated {len(entries)} Phase 1 expansion entries!")
    print("\nNext steps:")
    print("1. Review entries for quality")
    print("2. Add comprehensive tags")
    print("3. Merge with main corpus")

if __name__ == "__main__":
    main()