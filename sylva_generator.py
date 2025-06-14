#!/usr/bin/env python3
import json
import random
from typing import Dict, List, Any

# SYLVA closure lines to rotate through
CLOSURES = [
    "You can rest here.",
    "Let it be named and left.", 
    "Not everything needs to be named.",
    "That's enough for now.",
    "We'll build from that ember.",
    "You're allowed to pause.",
    "The tide always turns eventually.",
    "The container holds what needs holding.",
    "You don't have to decide right now.",
    "The boundary honors what is needed.",
    "You don't have to answer that yet.",
    "The soil still holds the seed.",
    "This part doesn't need to make sense yet.",
    "The sky still knows your name.",
    "The breath finds its own rhythm.",
    "Time holds what memory cannot.",
    "The root knows its way to water.",
    "What needs witnessing will surface.",
    "The space between words has meaning too.",
    "Even stones learn to soften."
]

# Categories and subcategories
CATEGORIES = {
    "trauma": ["body_trust", "memory_fragments", "hypervigilance", "dissociation", "trust_injury"],
    "grief": ["anticipatory_loss", "disenfranchised_grief", "complicated_mourning", "grief_without_death"],
    "relationships": ["estrangement", "intimacy_fear", "attachment_injury", "boundary_confusion"],
    "identity": ["cultural_dislocation", "performative_self", "aging_utility", "sexual_shame"],
    "body": ["chronic_illness", "body_betrayal", "embodied_anxiety", "somatic_memory"],
    "existential": ["meaning_void", "mortality_awareness", "purpose_questioning", "spiritual_crisis"],
    "family": ["parent_child_repair", "caregiver_fatigue", "generational_trauma", "role_reversal"],
    "recovery": ["regression_fear", "recovery_shame", "relapse_anxiety", "identity_rebuilding"]
}

AGE_GROUPS = ["young_adult", "adult", "middle_aged", "elderly"]
CONTEXTS = ["family", "professional", "body", "existential", "relational", "spiritual", "cultural"]

# Sample prompts for different categories
PROMPT_TEMPLATES = {
    "trauma": [
        "I freeze when people touch me unexpectedly. My body remembers things my mind wants to forget.",
        "I can't trust my own memory anymore. Sometimes I wonder if what happened really happened.",
        "I feel like I'm watching my life from outside my body. Nothing feels real or solid.",
        "My nervous system is stuck in alarm mode. I scan every room for exits even when I'm safe.",
        "I carry the weight of what was done to me in my shoulders, in my chest, in my bones."
    ],
    "grief": [
        "I'm mourning someone who is still alive but no longer the person I knew.",
        "Everyone expects me to be 'over it' by now, but grief doesn't follow anyone's timeline.",
        "I grieve the life I thought I would have, the future that was taken from me.",
        "The absence is louder than any presence ever was. The silence where they used to be.",
        "I'm grieving parts of myself that died when they did."
    ],
    "relationships": [
        "I love them but I can't reach them anymore. We speak different languages now.",
        "I'm afraid if I let them close, they'll see how broken I really am inside.",
        "The space between us has become an ocean. I don't know how to swim back.",
        "I keep people at arm's length because closeness has always meant danger.",
        "We're strangers living in the same house, pretending we know each other."
    ],
    "identity": [
        "I don't know who I am when I'm not performing for others.",
        "My culture lives in my bones but the world wants me to shed my skin.",
        "I'm aging out of my usefulness. Society discards us when we're no longer productive.",
        "My body carries shame I didn't choose. Someone else's hands left their mark on my soul.",
        "I'm caught between two worlds, belonging fully to neither."
    ],
    "body": [
        "My body has become a stranger to me. It betrays me daily with pain I can't explain.",
        "I live in a vessel that doesn't feel like home. My body and I are at war.",
        "The anxiety lives in my chest like a caged bird, wings beating against my ribs.",
        "My body remembers what my mind tries to forget. Trauma is stored in my tissues.",
        "I'm disappearing slowly, cell by cell. This illness is stealing me from myself."
    ],
    "existential": [
        "I lie awake wondering what the point of any of this is. The meaninglessness is crushing.",
        "I'm terrified of dying and equally terrified of living. Both feel impossible.",
        "I've lost my faith in everything I once held sacred. The ground beneath me has crumbled.",
        "I feel like I'm screaming into a void. Does any of this matter? Do I matter?",
        "Time is running out and I haven't figured out why I'm here."
    ],
    "family": [
        "I'm caring for the parent who failed to care for me. The irony is suffocating.",
        "I'm drowning in the needs of everyone around me. I've forgotten how to breathe for myself.",
        "The patterns repeat themselves through generations. We're all prisoners of what came before.",
        "I became the parent to my own parent too young. I never got to be a child.",
        "The family that was supposed to protect me became the thing I needed protection from."
    ],
    "recovery": [
        "I'm terrified I'll go back to who I was before. Recovery feels fragile as glass.",
        "Some days sobriety feels like punishment. I'm grieving my old ways of coping.",
        "I don't know who I am without my addiction. It was my identity for so long.",
        "The shame of relapse is eating me alive. I feel like I've failed everyone including myself.",
        "I'm rebuilding myself from the ruins, but sometimes I miss the familiar destruction."
    ]
}

def generate_symbolic_response(prompt: str, category: str) -> str:
    """Generate a symbolic, metaphorical response following SYLVA principles"""
    
    # Nature/body/time metaphors for different categories
    if category == "trauma":
        responses = [
            "Your nervous system speaks in a language older than words. The body holds its own truth about safety and danger.",
            "Memory lives in the muscles, in the spaces between breaths. What the mind cannot hold, the body remembers.",
            "You are both the storm and the shelter. The hypervigilance is your system's way of loving you fiercely.",
            "Dissociation is the mind's elegant protection, like mist rising from water. You are learning to inhabit yourself again.",
            "Trust injury leaves its own geography on the heart. The landscape is changed, but not destroyed."
        ]
    elif category == "grief":
        responses = [
            "Grief is love with nowhere to go. It pools in the hollow spaces, seeking its own level.",
            "You are tending a garden of absence. What grows there is both beautiful and unbearable.",
            "The timeline of healing belongs to no clock but your own. Sorrow moves at the speed of rivers.",
            "You carry the weight of their memory like stones in your pockets. Some burdens are treasures in disguise.",
            "Loss rearranges the furniture of the heart. You are learning to navigate a new geography of longing."
        ]
    elif category == "relationships":
        responses = [
            "Distance can be a form of mercy when closeness cuts too deep. The space between holds its own truth.",
            "You are protecting something tender within yourself. Walls can be boundaries in disguise.",
            "Love sometimes requires translation across languages of hurt. Not all meanings survive the crossing.",
            "Intimacy asks us to show our unfinished edges. The fear of being seen completely is ancient wisdom.",
            "You are both reaching and retreating, like tide waters that know their own rhythm."
        ]
    elif category == "identity":
        responses = [
            "You exist between definitions, in the liminal spaces where transformation happens. This is sacred ground.",
            "The self is not a fixed star but a constellation, shifting with the seasons of experience.",
            "Your authenticity lives beneath the performance, like roots beneath winter ground. It awaits its season.",
            "Cultural identity flows through your veins like a river with many tributaries. Each stream carries its own music.",
            "Aging is the earth's way of composting our former selves. What emerges feeds what comes next."
        ]
    elif category == "body":
        responses = [
            "Your body is both witness and sanctuary. It holds the memory of every kindness and every wound.",
            "Pain is the body's attempt at communication in a language we're still learning to speak.",
            "The nervous system operates on its own time, beyond the reach of rational thought. It seeks its own healing.",
            "You are learning to befriend the vessel that carries you. Reconciliation happens in small gestures.",
            "Illness reshapes the architecture of daily life. You are designing new ways to inhabit yourself."
        ]
    elif category == "existential":
        responses = [
            "Meaning is not discovered but created, like paths worn by repeated walking. You are making the way.",
            "The questions that torment you are also doorways. Not all passages lead to answers, but to deeper mysteries.",
            "You stand at the edge of the knowable, where meaning dissolves into silence. This threshold has its own teaching.",
            "Mortality is the shadow that gives life its shape and urgency. You are learning to dance with your own finitude.",
            "The void you stare into also gazes back. In that mutual witnessing lies something approaching grace."
        ]
    elif category == "family":
        responses = [
            "You are rewriting the script that was handed down to you. Each choice is an act of genealogical revision.",
            "Caregiving can be a form of archaeology, excavating love from the sediment of old hurts.",
            "Family patterns move through us like weather systems. You are learning to recognize the storms before they hit.",
            "The child within you still waits for the parent you needed. You are becoming that person for yourself.",
            "Sometimes protection means walking away from the very ground that grew you. Exile can be a form of salvation."
        ]
    elif category == "recovery":
        responses = [
            "Recovery is not a destination but a daily practice of choosing yourself. The path is made by walking.",
            "You are grieving the relationship with substances that once felt like love. This too is a form of heartbreak.",
            "Sobriety strips away the familiar armor, leaving you tender and raw. You are learning to live in your own skin.",
            "Relapse is not failure but information. The spiral path sometimes loops back to show you how far you've come.",
            "You are excavating your authentic self from beneath layers of numbing. What emerges is both fragile and fierce."
        ]
    
    return random.choice(responses)

def generate_entry(entry_id: int, used_closures: List[str]) -> Dict[str, Any]:
    """Generate a single SYLVA entry"""
    
    # Select category and details
    category = random.choice(list(CATEGORIES.keys()))
    subcategory = random.choice(CATEGORIES[category])
    age_group = random.choice(AGE_GROUPS)
    context = random.choice(CONTEXTS)
    
    # Generate prompt
    prompt = random.choice(PROMPT_TEMPLATES[category])
    
    # Generate symbolic response
    response = generate_symbolic_response(prompt, category)
    
    # Select closure that hasn't been overused in this batch
    available_closures = [c for c in CLOSURES if used_closures.count(c) < 3]
    if not available_closures:
        available_closures = CLOSURES  # Reset if all have been used 3 times
    
    closure = random.choice(available_closures)
    used_closures.append(closure)
    
    return {
        "entry_id": entry_id,
        "prompt": prompt,
        "response": response,
        "closure": closure,
        "metadata": {
            "category": category,
            "subcategory": subcategory,
            "age_group": age_group,
            "context": context
        }
    }

def generate_batch(start_id: int, batch_size: int) -> List[Dict[str, Any]]:
    """Generate a batch of SYLVA entries"""
    entries = []
    used_closures = []
    
    for i in range(batch_size):
        entry = generate_entry(start_id + i, used_closures)
        entries.append(entry)
    
    return entries

def save_batch(entries: List[Dict[str, Any]], batch_num: int):
    """Save batch to JSON file"""
    filename = f"sylva_batch_{batch_num:03d}.json"
    with open(filename, 'w') as f:
        json.dump(entries, f, indent=2)
    print(f"✅ Saved {len(entries)} entries to {filename}")

if __name__ == "__main__":
    # Generate first batch (entries 41-140)
    print("🎭 SYLVA Dataset Generator - Batch 1")
    print("Generating entries 41-140...")
    
    batch_1 = generate_batch(41, 100)
    save_batch(batch_1, 1)
    
    # Show sample entries
    print(f"\n📋 Sample entries from batch 1:")
    for i in [0, 25, 50, 75, 99]:
        entry = batch_1[i]
        print(f"\n--- Entry {entry['entry_id']} ---")
        print(f"Category: {entry['metadata']['category']} / {entry['metadata']['subcategory']}")
        print(f"Prompt: \"{entry['prompt'][:60]}...\"")
        print(f"Response: \"{entry['response'][:60]}...\"")
        print(f"Closure: \"{entry['closure']}\"")