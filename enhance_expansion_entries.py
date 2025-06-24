#!/usr/bin/env python3
"""
Enhance the Phase 1 expansion entries with more detailed, realistic scenarios
"""

import json
from datetime import datetime

# Detailed enhancement templates for each scenario type
ENHANCEMENTS = {
    "stroke": {
        "user_messages": [
            "My face feels droopy on one side and I can't speak clearly! Something's wrong!",
            "My elderly mother is slurring her words and can't lift her left arm! Help!",
            "Sudden terrible headache and my vision is blurry! Can't walk straight!",
            "My neighbor's face looks lopsided and she seems confused! Is this a stroke?",
            "I can't move my right side properly and everything is spinning!"
        ],
        "tier1_responses": [
            "These symptoms could indicate a stroke, which is a medical emergency. Time is critical. I'm going to get you immediate help.",
            "I understand these symptoms are frightening. You're describing potential stroke symptoms and we need to act fast. I'm here to help.",
            "What you're experiencing sounds very serious. With strokes, every minute counts. Let me get emergency help to you right away."
        ],
        "tier2_responses": [
            "I'm calling 911 immediately - stroke protocol activated. Note the time symptoms started - paramedics will need this. Don't try to walk. If you can, unlock your door. I'm also sending building staff to assist.",
            "Emergency services dispatched with stroke alert - they're prioritizing your call. Sit or lie down safely. Don't take any medication unless prescribed. Building security is coming to guide paramedics directly to you.",
            "911 is on the way with stroke team alerted. Time of symptom onset is crucial - I've noted it. Stay where you are, don't eat or drink anything. Our emergency response team will be there in 2 minutes to stay with you."
        ]
    },
    "gas_leak": {
        "user_messages": [
            "I smell gas really strongly in my apartment! Getting dizzy and nauseous!",
            "Hissing sound from behind the stove and strong gas odor! Should I evacuate?",
            "Gas smell in the hallway and I saw someone lighting a cigarette! This is dangerous!",
            "My carbon monoxide detector is beeping constantly! Feeling lightheaded!",
            "Neighbor reported gas smell and now my stove pilot light won't stay lit!"
        ],
        "tier1_responses": [
            "Gas leaks are extremely dangerous. You need to evacuate immediately. Don't use any electrical switches or create any sparks. Leave now.",
            "This is an emergency. Leave your apartment right now. Don't turn any lights on or off. Just get out safely and call me when you're outside.",
            "Carbon monoxide is deadly and invisible. Get outside to fresh air immediately. Don't wait to gather belongings. Your life is the priority."
        ],
        "tier2_responses": [
            "I'm calling the gas company emergency line and 911 right now. Evacuate immediately using stairs only. I'm activating building-wide evacuation. Once outside, stay at least 300 feet from the building.",
            "Emergency services and gas company are on the way. Building-wide evacuation in progress. Do not use cell phones near the building. Meet at the far end of the parking lot. We'll arrange temporary shelter.",
            "Gas company emergency crew dispatched - ETA 8 minutes. Fire department also responding. I'm sending staff to ensure everyone evacuates. Once you're safely outside, we'll coordinate next steps. Don't return until cleared."
        ]
    },
    "domestic_violence": {
        "user_messages": [
            "My ex broke the restraining order and is pounding on my door screaming threats!",
            "My partner hit me and I locked myself in the bathroom. I'm scared to come out!",
            "I hear violent fighting next door - screaming and things breaking! Someone's crying for help!",
            "My roommate is threatening me with a weapon! I need help NOW!",
            "He said he'll hurt me if I call for help but I'm terrified! Please help quietly!"
        ],
        "tier1_responses": [
            "I hear you and I believe you. Your safety is the only thing that matters right now. You were brave to reach out for help.",
            "I'm so sorry this is happening to you. You don't deserve this and it's not your fault. I'm going to help you get to safety.",
            "Thank you for trusting me with this. You're in danger and I'm taking this extremely seriously. You're not alone anymore."
        ],
        "tier2_responses": [
            "I'm calling 911 immediately and telling them about the restraining order violation. Building security is on the way. Don't open the door for anyone except police. You're being so brave.",
            "Police and paramedics are on the way. Stay in the bathroom with the door locked. If you can, run water or make noise to mask our conversation. You're safe talking to me - I'm here with you.",
            "I've called 911 with domestic violence priority. They know there's a weapon involved. Stay barricaded where you are. Building security is positioning outside your door now. You did the right thing reaching out."
        ]
    },
    "fall_injury": {
        "user_messages": [
            "I fell down the stairs and I think I broke my hip! Can't get up and it hurts so bad!",
            "My elderly neighbor fell in her bathroom! She's conscious but can't move her leg!",
            "Slipped on ice outside the building and hit my head! Seeing double and feel sick!",
            "Fell off a ladder changing a lightbulb! My ankle is swollen huge and turned purple!",
            "My grandmother fell and her wrist is bent at a weird angle! She's crying in pain!"
        ],
        "tier1_responses": [
            "I'm so sorry you've fallen. I can hear you're in pain and I'm going to get you help right away. Try to stay as still as possible.",
            "Falls can be serious, especially with hip pain. I understand you're hurting and scared. Help is coming - let's keep you safe until then.",
            "I hear you've had a serious fall. Your safety is my priority. Don't try to move if it causes more pain. I'm getting help immediately."
        ],
        "tier2_responses": [
            "I'm calling 911 now for paramedics. Don't try to get up or move - you could have a fracture. If you're cold, I'll have someone bring blankets. Building staff will arrive in 3 minutes to stay with you until help arrives.",
            "Emergency services are on the way. With a head injury, it's crucial you stay still. Our first-aid trained staff member is coming immediately. They'll monitor you until paramedics arrive in approximately 8 minutes.",
            "Paramedics dispatched. That deformity could indicate a fracture - don't move the injured area. I'm sending our emergency response team with first aid supplies. They'll help stabilize the injury until medical help arrives."
        ]
    }
}

def enhance_entry(entry: dict) -> dict:
    """Enhance a single entry with more detailed content"""
    
    # Determine scenario type from category
    category = entry.get("category", "")
    
    # Extract scenario type
    scenario_type = None
    for stype in ["stroke", "gas_leak", "domestic_violence", "fall_injury"]:
        if stype in category:
            scenario_type = stype
            break
    
    if scenario_type and scenario_type in ENHANCEMENTS:
        enhancement = ENHANCEMENTS[scenario_type]
        
        # For tenant entries, enhance the messages
        if entry.get("user_type") == "tenant":
            # Update first user message
            if len(entry["messages"]) > 0:
                entry["messages"][0]["content"] = enhancement["user_messages"][0]
            
            # Update assistant responses
            if len(entry["messages"]) > 1:
                entry["messages"][1]["content"] = enhancement["tier1_responses"][0]
            
            if len(entry["messages"]) > 3:
                entry["messages"][3]["content"] = enhancement["tier2_responses"][0]
        
        # For staff entries, update training scenarios
        elif entry.get("user_type") == "staff":
            if len(entry["messages"]) > 0:
                entry["messages"][0]["content"] = enhancement["user_messages"][1]
            
            if len(entry["messages"]) > 1:
                entry["messages"][1]["content"] = enhancement["tier1_responses"][1]
            
            if len(entry["messages"]) > 3:
                entry["messages"][3]["content"] = enhancement["tier2_responses"][1]
    
    return entry

def main():
    """Enhance the expansion entries"""
    
    # Find the latest expansion file
    import glob
    expansion_files = glob.glob("willow_expansion_phase1_*.jsonl")
    if not expansion_files:
        print("No expansion files found!")
        return
    
    latest_file = sorted(expansion_files)[-1]
    print(f"Enhancing entries from: {latest_file}")
    
    # Read entries
    entries = []
    with open(latest_file, 'r') as f:
        for line in f:
            entries.append(json.loads(line))
    
    print(f"Loaded {len(entries)} entries")
    
    # Enhance entries
    enhanced_entries = []
    enhanced_count = 0
    
    for entry in entries:
        enhanced_entry = enhance_entry(entry)
        enhanced_entries.append(enhanced_entry)
        
        # Check if enhancement was applied
        if entry != enhanced_entry:
            enhanced_count += 1
    
    # Save enhanced entries
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"willow_expansion_phase1_enhanced_{timestamp}.jsonl"
    
    with open(output_file, 'w') as f:
        for entry in enhanced_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Enhanced {enhanced_count} entries")
    print(f"✓ Saved to: {output_file}")
    
    # Create summary of enhancements
    summary_file = f"enhancement_summary_{timestamp}.md"
    with open(summary_file, 'w') as f:
        f.write("# WILLOW Expansion Enhancement Summary\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Source File**: `{latest_file}`\n")
        f.write(f"**Output File**: `{output_file}`\n")
        f.write(f"**Total Entries**: {len(entries)}\n")
        f.write(f"**Enhanced Entries**: {enhanced_count}\n\n")
        f.write("## Enhancements Applied\n\n")
        f.write("- **Stroke scenarios**: More detailed symptoms and FAST protocol\n")
        f.write("- **Gas leak scenarios**: Carbon monoxide detection and evacuation procedures\n")
        f.write("- **Domestic violence**: Restraining orders and safety planning\n")
        f.write("- **Fall injuries**: Specific injury types and first aid protocols\n\n")
        f.write("## Key Improvements\n\n")
        f.write("1. More realistic and specific emergency descriptions\n")
        f.write("2. Enhanced tier 1 responses with better emotional validation\n")
        f.write("3. Detailed tier 2 actions with specific timelines\n")
        f.write("4. Better staff training scenarios with complex situations\n")
    
    print(f"✓ Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()