#!/usr/bin/env python3
import json
import random
import os
from typing import Dict, List, Any
from pathlib import Path

# Extended SYLVA closure lines
CLOSURES = [
    "You can rest here.", "Let it be named and left.", "Not everything needs to be named.",
    "That's enough for now.", "We'll build from that ember.", "You're allowed to pause.",
    "The tide always turns eventually.", "The container holds what needs holding.",
    "You don't have to decide right now.", "The boundary honors what is needed.",
    "You don't have to answer that yet.", "The soil still holds the seed.",
    "This part doesn't need to make sense yet.", "The sky still knows your name.",
    "The breath finds its own rhythm.", "Time holds what memory cannot.",
    "The root knows its way to water.", "What needs witnessing will surface.",
    "The space between words has meaning too.", "Even stones learn to soften.",
    "The season knows its own timing.", "What is unfinished is not unfixable.",
    "The horizon holds what cannot be named.", "Silence can be its own answer.",
    "The wound and the gift share the same door.", "You are allowed to not know yet.",
    "The heart's geography is always changing.", "What breaks open also lets light in.",
    "The memory chooses its own moments.", "Some questions live better than answers.",
    "The threshold honors both directions.", "What you protect also protects you."
]

# Extended categories with more nuanced subcategories
CATEGORIES = {
    "trauma": ["body_trust", "memory_fragments", "hypervigilance", "dissociation", "trust_injury", 
               "freeze_response", "trauma_bonding", "somatic_flashbacks", "emotional_numbing"],
    "grief": ["anticipatory_loss", "disenfranchised_grief", "complicated_mourning", "grief_without_death",
              "living_loss", "ambiguous_loss", "secondary_losses", "collective_grief", "inherited_grief"],
    "relationships": ["estrangement", "intimacy_fear", "attachment_injury", "boundary_confusion",
                      "emotional_fusion", "love_addiction", "avoidant_patterns", "betrayal_trauma", "enmeshment"],
    "identity": ["cultural_dislocation", "performative_self", "aging_utility", "sexual_shame",
                 "gender_dysphoria", "adoption_trauma", "religious_deconversion", "career_identity_loss"],
    "body": ["chronic_illness", "body_betrayal", "embodied_anxiety", "somatic_memory",
             "disability_adjustment", "body_dysmorphia", "medical_trauma", "fertility_grief"],
    "existential": ["meaning_void", "mortality_awareness", "purpose_questioning", "spiritual_crisis",
                    "existential_loneliness", "absurdity_confrontation", "freedom_paralysis", "death_anxiety"],
    "family": ["parent_child_repair", "caregiver_fatigue", "generational_trauma", "role_reversal",
               "empty_nest", "family_secrets", "loyalty_conflicts", "scapegoating"],
    "recovery": ["regression_fear", "recovery_shame", "relapse_anxiety", "identity_rebuilding",
                 "sobriety_grief", "recovery_paradox", "spiritual_bypassing", "dry_drunk"],
    "workplace": ["burnout_syndrome", "impostor_feelings", "workplace_trauma", "career_stagnation",
                  "leadership_isolation", "creative_blocks", "performance_anxiety", "retirement_grief"],
    "sexuality": ["sexual_trauma", "desire_discrepancy", "orientation_questioning", "intimacy_dysfunction", 
                  "shame_cycles", "sexual_addiction", "celibacy_struggles", "erotic_awakening"]
}

AGE_GROUPS = ["adolescent", "young_adult", "adult", "middle_aged", "elderly"]
CONTEXTS = ["family", "professional", "body", "existential", "relational", "spiritual", "cultural", "medical"]

# Expanded prompt templates with more variety
PROMPT_TEMPLATES = {
    "trauma": [
        "I freeze when people touch me unexpectedly. My body remembers things my mind wants to forget.",
        "I can't trust my own memory anymore. Sometimes I wonder if what happened really happened.",
        "I feel like I'm watching my life from outside my body. Nothing feels real or solid.",
        "My nervous system is stuck in alarm mode. I scan every room for exits even when I'm safe.",
        "I carry the weight of what was done to me in my shoulders, in my chest, in my bones.",
        "My body betrayed me by responding to touch that wasn't safe. Now I can't tell the difference.",
        "I learned to disappear so well that now I can't find my way back to myself.",
        "The flashbacks hit without warning, pulling me back to moments I thought I'd escaped.",
        "I've become an expert at reading micro-expressions, always scanning for danger.",
        "My trauma happened to a child's body but I carry it in an adult's frame."
    ],
    "grief": [
        "I'm mourning someone who is still alive but no longer the person I knew.",
        "Everyone expects me to be 'over it' by now, but grief doesn't follow anyone's timeline.",
        "I grieve the life I thought I would have, the future that was taken from me.",
        "The absence is louder than any presence ever was. The silence where they used to be.",
        "I'm grieving parts of myself that died when they did.",
        "The world moved on but I'm still frozen in the moment everything changed.",
        "I keep setting the table for two out of habit, then remembering they're gone.",
        "Grief ambushes me in grocery store aisles when I see their favorite foods.",
        "I'm mourning the parent they never became, the grandparent my children will never know.",
        "Some days the grief feels like drowning. Other days it's just a dull ache in my chest."
    ],
    "relationships": [
        "I love them but I can't reach them anymore. We speak different languages now.",
        "I'm afraid if I let them close, they'll see how broken I really am inside.",
        "The space between us has become an ocean. I don't know how to swim back.",
        "I keep people at arm's length because closeness has always meant danger.",
        "We're strangers living in the same house, pretending we know each other.",
        "I give and give until I'm empty, then resent them for taking what I offered.",
        "I fall in love with potential instead of reality, then blame them for not changing.",
        "I've forgotten how to be alone without feeling abandoned.",
        "Love feels like a language I once spoke fluently but now can barely remember.",
        "I attract people who need fixing because it's easier than facing my own brokenness."
    ],
    "identity": [
        "I don't know who I am when I'm not performing for others.",
        "My culture lives in my bones but the world wants me to shed my skin.",
        "I'm aging out of my usefulness. Society discards us when we're no longer productive.",
        "My body carries shame I didn't choose. Someone else's hands left their mark on my soul.",
        "I'm caught between two worlds, belonging fully to neither.",
        "I've spent so long being who others needed me to be that I've lost track of myself.",
        "My gender feels like a costume that doesn't fit, but I don't know what's underneath.",
        "I'm deconstructing the faith that once defined me, left floating in spiritual space.",
        "My career was my identity. Without it, I don't know who I am anymore.",
        "I carry my ancestors' dreams and traumas in equal measure."
    ],
    "body": [
        "My body has become a stranger to me. It betrays me daily with pain I can't explain.",
        "I live in a vessel that doesn't feel like home. My body and I are at war.",
        "The anxiety lives in my chest like a caged bird, wings beating against my ribs.",
        "My body remembers what my mind tries to forget. Trauma is stored in my tissues.",
        "I'm disappearing slowly, cell by cell. This illness is stealing me from myself.",
        "I look in the mirror and see someone I don't recognize staring back.",
        "My body failed me when I needed it most. How do I trust it again?",
        "The medication helps but steals pieces of me in the process.",
        "I'm watching my body age while my mind still feels twenty-five.",
        "My disability shapes how others see me before they know anything else about me."
    ],
    "existential": [
        "I lie awake wondering what the point of any of this is. The meaninglessness is crushing.",
        "I'm terrified of dying and equally terrified of living. Both feel impossible.",
        "I've lost my faith in everything I once held sacred. The ground beneath me has crumbled.",
        "I feel like I'm screaming into a void. Does any of this matter? Do I matter?",
        "Time is running out and I haven't figured out why I'm here.",
        "The universe feels indifferent to my suffering, to my joy, to my existence.",
        "I'm paralyzed by too many choices. Freedom feels like a curse.",
        "Death feels like the only certainty in a world of constant change.",
        "I'm drowning in the absurdity of daily life while cosmic questions consume me.",
        "I used to believe in purpose. Now I'm not sure anything has inherent meaning."
    ],
    "family": [
        "I'm caring for the parent who failed to care for me. The irony is suffocating.",
        "I'm drowning in the needs of everyone around me. I've forgotten how to breathe for myself.",
        "The patterns repeat themselves through generations. We're all prisoners of what came before.",
        "I became the parent to my own parent too young. I never got to be a child.",
        "The family that was supposed to protect me became the thing I needed protection from.",
        "My children left home and I don't know who I am without them to care for.",
        "I'm the keeper of family secrets that are slowly poisoning me from the inside.",
        "I love my family but I can't be around them without losing pieces of myself.",
        "I'm caught between being loyal to my family and being true to myself.",
        "The family scapegoat role follows me everywhere, even into new relationships."
    ],
    "recovery": [
        "I'm terrified I'll go back to who I was before. Recovery feels fragile as glass.",
        "Some days sobriety feels like punishment. I'm grieving my old ways of coping.",
        "I don't know who I am without my addiction. It was my identity for so long.",
        "The shame of relapse is eating me alive. I feel like I've failed everyone including myself.",
        "I'm rebuilding myself from the ruins, but sometimes I miss the familiar destruction.",
        "Recovery stripped away my numbing but didn't teach me how to feel.",
        "I'm sober but not recovering. I'm just existing without my drug of choice.",
        "The spiritual bypassing in recovery culture makes me want to use again.",
        "I got clean but my thinking is still toxic. Sobriety isn't the same as healing.",
        "I'm discovering wounds I medicated for decades. Recovery is archaeological work."
    ],
    "workplace": [
        "I gave everything to this job and it gave me nothing but burnout in return.",
        "I feel like a fraud in every meeting. Someone will discover I don't belong here.",
        "My creativity died somewhere between the deadlines and the office politics.",
        "I'm drowning in other people's emergencies while my own life falls apart.",
        "Retirement feels like death. Without work, who am I?",
        "I'm surrounded by colleagues but feel profoundly isolated and misunderstood.",
        "The harassment at work is subtle but constant. I'm gaslighting myself about its reality.",
        "I climbed the ladder only to discover it was leaning against the wrong wall.",
        "My leadership position feels like performing a role I was never meant to play.",
        "I'm too old to start over but too young to give up. I feel trapped."
    ],
    "sexuality": [
        "My body responds to trauma triggers during intimate moments. Pleasure feels dangerous.",
        "I want connection but my desire has vanished. I'm grieving my erotic self.",
        "I'm questioning everything I thought I knew about my sexual orientation.",
        "The shame around my desires is older than my memory of them.",
        "My partner and I are sexually incompatible but neither of us wants to leave.",
        "I've been celibate so long I've forgotten what longing feels like.",
        "My sexuality awakened late in life and now I don't know what to do with it.",
        "I use sex to avoid intimacy, then wonder why I feel empty afterward.",
        "My body was weaponized against me. How do I reclaim it as my own?",
        "I'm addicted to the chase but terrified of being caught."
    ]
}

def generate_symbolic_response(prompt: str, category: str) -> str:
    """Generate symbolic, metaphorical responses following SYLVA principles"""
    
    response_pools = {
        "trauma": [
            "Your nervous system speaks in a language older than words. The body holds its own truth about safety and danger.",
            "Memory lives in the muscles, in the spaces between breaths. What the mind cannot hold, the body remembers.",
            "You are both the storm and the shelter. The hypervigilance is your system's way of loving you fiercely.",
            "Dissociation is the mind's elegant protection, like mist rising from water. You are learning to inhabit yourself again.",
            "Trust injury leaves its own geography on the heart. The landscape is changed, but not destroyed.",
            "The body's betrayal is also its wisdom. It learned to survive in ways the mind could not.",
            "Disappearing was a masterful skill once. Now you are learning the equally difficult art of being present.",
            "Flashbacks are time travelers carrying messages from a younger self who needed witnessing.",
            "Your vigilance was earned in places where safety was a luxury. The scanning is love in another form.",
            "The child's body held what the child's mind could not comprehend. You carry both the wound and the resilience."
        ],
        "grief": [
            "Grief is love with nowhere to go. It pools in the hollow spaces, seeking its own level.",
            "You are tending a garden of absence. What grows there is both beautiful and unbearable.",
            "The timeline of healing belongs to no clock but your own. Sorrow moves at the speed of rivers.",
            "You carry the weight of their memory like stones in your pockets. Some burdens are treasures in disguise.",
            "Loss rearranges the furniture of the heart. You are learning to navigate a new geography of longing.",
            "The world's amnesia about death makes your grief feel foreign. You are fluent in a language others fear.",
            "Habit is memory in the body. Setting the table for two is a prayer to what was.",
            "Grief ambushes because love doesn't follow schedules. The heart keeps its own calendar.",
            "You mourn not just who they were, but who they might have become. Potential has its own weight.",
            "Some days grief feels like drowning. Other days it's the water that teaches you to float."
        ],
        "relationships": [
            "Distance can be a form of mercy when closeness cuts too deep. The space between holds its own truth.",
            "You are protecting something tender within yourself. Walls can be boundaries in disguise.",
            "Love sometimes requires translation across languages of hurt. Not all meanings survive the crossing.",
            "Intimacy asks us to show our unfinished edges. The fear of being seen completely is ancient wisdom.",
            "You are both reaching and retreating, like tide waters that know their own rhythm.",
            "Giving until empty is martyrdom disguised as love. Your resentment is information about boundaries.",
            "Falling in love with potential is a form of hope. Reality requires a different kind of courage.",
            "Solitude and abandonment are different countries. You are learning to tell them apart.",
            "Love is indeed a language. Fluency returns with practice, patience, and the right teacher.",
            "You attract what you believe you deserve. Healing begins with questioning that belief."
        ],
        "identity": [
            "You exist between definitions, in the liminal spaces where transformation happens. This is sacred ground.",
            "The self is not a fixed star but a constellation, shifting with the seasons of experience.",
            "Your authenticity lives beneath the performance, like roots beneath winter ground. It awaits its season.",
            "Cultural identity flows through your veins like a river with many tributaries. Each stream carries its own music.",
            "Aging is the earth's way of composting our former selves. What emerges feeds what comes next.",
            "Performance becomes prison when we forget it's optional. You are remembering your natural voice.",
            "Gender is a constellation, not a binary star. You are learning to navigate by your own light.",
            "Deconstructing faith is archaeology of the soul. What remains after the excavation is truly yours.",
            "Career death can be identity rebirth. You are discovering who you are beyond what you do.",
            "Ancestors live in your DNA and your choices. You carry their dreams and traumas forward, transformed."
        ],
        "body": [
            "Your body is both witness and sanctuary. It holds the memory of every kindness and every wound.",
            "Pain is the body's attempt at communication in a language we're still learning to speak.",
            "The nervous system operates on its own time, beyond the reach of rational thought. It seeks its own healing.",
            "You are learning to befriend the vessel that carries you. Reconciliation happens in small gestures.",
            "Illness reshapes the architecture of daily life. You are designing new ways to inhabit yourself.",
            "The mirror reflects one moment in time. You are more than any single reflection can hold.",
            "Body betrayal teaches harsh lessons about trust. Forgiveness begins with understanding its survival wisdom.",
            "Medication is alchemy - transforming suffering into possibility, often with its own costs.",
            "The body ages while the spirit remains timeless. You are learning to honor both realities.",
            "Disability reframes ability. You are discovering new ways of moving through the world."
        ],
        "existential": [
            "Meaning is not discovered but created, like paths worn by repeated walking. You are making the way.",
            "The questions that torment you are also doorways. Not all passages lead to answers, but to deeper mysteries.",
            "You stand at the edge of the knowable, where meaning dissolves into silence. This threshold has its own teaching.",
            "Mortality is the shadow that gives life its shape and urgency. You are learning to dance with your own finitude.",
            "The void you stare into also gazes back. In that mutual witnessing lies something approaching grace.",
            "Indifference is the universe's default setting. Your suffering and joy are equally cosmic rebellions.",
            "Paralysis in the face of infinite choice is its own choice. Freedom includes the freedom to not choose.",
            "Death as certainty can be oddly comforting. In a world of variables, it offers one constant.",
            "Absurdity and meaning are dance partners. The cosmic joke may be that both are true simultaneously.",
            "Purpose is not found but forged. Meaning is the fire you kindle in the darkness of uncertainty."
        ],
        "family": [
            "You are rewriting the script that was handed down to you. Each choice is an act of genealogical revision.",
            "Caregiving can be a form of archaeology, excavating love from the sediment of old hurts.",
            "Family patterns move through us like weather systems. You are learning to recognize the storms before they hit.",
            "The child within you still waits for the parent you needed. You are becoming that person for yourself.",
            "Sometimes protection means walking away from the very ground that grew you. Exile can be a form of salvation.",
            "Empty nest is both loss and liberation. You are discovering who you are beyond your children's needs.",
            "Secrets are poison that works slowly. Truth-telling is the antidote, even when it burns.",
            "Family love and family harm often wear the same face. Discernment is the skill you're developing.",
            "Loyalty and authenticity sometimes demand different directions. You are learning to choose yourself.",
            "Scapegoat roles are inherited positions. You are resigning from a job you never applied for."
        ],
        "recovery": [
            "Recovery is not a destination but a daily practice of choosing yourself. The path is made by walking.",
            "You are grieving the relationship with substances that once felt like love. This too is a form of heartbreak.",
            "Sobriety strips away the familiar armor, leaving you tender and raw. You are learning to live in your own skin.",
            "Relapse is not failure but information. The spiral path sometimes loops back to show you how far you've come.",
            "You are excavating your authentic self from beneath layers of numbing. What emerges is both fragile and fierce.",
            "Recovery removed the anesthesia but not the pain. You are learning to feel your way through healing.",
            "Sobriety without recovery is white-knuckling existence. True healing includes the heart and spirit.",
            "Spiritual bypassing is another form of numbing. Real recovery includes the shadow work.",
            "Clean thinking requires more than stopping use. You are rewiring patterns laid down over years.",
            "Archaeological recovery unearths ancient wounds. Each layer excavated brings you closer to your core."
        ],
        "workplace": [
            "Burnout is your system's rebellion against giving more than you have. The exhaustion carries wisdom.",
            "Impostor syndrome speaks the language of unworthiness. You are learning to question its authority.",
            "Creativity requires space to breathe. Deadlines and politics are creative asphyxiation.",
            "Other people's emergencies become your crisis only if you allow it. Boundaries are emergency medicine.",
            "Retirement grief is mourning an identity that served its time. Who you are is larger than what you do.",
            "Professional isolation in crowded offices is its own form of loneliness. Connection requires vulnerability.",
            "Workplace harassment operates in whispers and glances. Your reality doesn't require others' validation.",
            "Success ladders sometimes lean against walls you don't want to climb. Redirection is not retreat.",
            "Leadership is performance art with real consequences. You are learning to lead from authenticity.",
            "Career transitions in midlife are second adolescences. Identity reformation is messy but necessary."
        ],
        "sexuality": [
            "The body remembers trauma in its responses to pleasure. Healing happens at the pace of safety.",
            "Desire is not constant like gravity. It ebbs and flows like tides, responding to invisible moons.",
            "Sexual identity is not fixed geography but flowing water. You are learning to navigate new territories.",
            "Shame around desire is inheritance from others' fears. You are questioning what you were taught to carry.",
            "Sexual incompatibility is a language problem, not a love problem. Some conversations require new vocabulary.",
            "Celibacy can be recovery of your erotic self, not abandonment of it. Fasting sharpens appetite.",
            "Late-blooming sexuality is spring after a long winter. The earth knows how to awaken when it's ready.",
            "Using sex to avoid intimacy is emotional sleight of hand. True connection requires presence, not performance.",
            "Reclaiming a weaponized body is revolutionary work. You are staging a coup against shame.",
            "The addiction to chase is fear of being caught with yourself. The real intimacy is self-acceptance."
        ]
    }
    
    return random.choice(response_pools.get(category, response_pools["existential"]))

def generate_entry(entry_id: int, used_closures: List[str], used_prompts: List[str]) -> Dict[str, Any]:
    """Generate a single SYLVA entry with anti-repetition measures"""
    
    # Select category and details
    category = random.choice(list(CATEGORIES.keys()))
    subcategory = random.choice(CATEGORIES[category])
    age_group = random.choice(AGE_GROUPS)
    context = random.choice(CONTEXTS)
    
    # Generate prompt, avoiding recent repetitions
    available_prompts = [p for p in PROMPT_TEMPLATES[category] if p not in used_prompts[-50:]]
    if not available_prompts:
        available_prompts = PROMPT_TEMPLATES[category]
    
    prompt = random.choice(available_prompts)
    used_prompts.append(prompt)
    
    # Generate symbolic response
    response = generate_symbolic_response(prompt, category)
    
    # Select closure that hasn't been overused in recent entries
    available_closures = [c for c in CLOSURES if used_closures[-30:].count(c) < 3]
    if not available_closures:
        available_closures = CLOSURES
    
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

def generate_batch(start_id: int, batch_size: int, global_used_closures: List[str], global_used_prompts: List[str]) -> List[Dict[str, Any]]:
    """Generate a batch of SYLVA entries"""
    entries = []
    
    for i in range(batch_size):
        entry = generate_entry(start_id + i, global_used_closures, global_used_prompts)
        entries.append(entry)
    
    return entries

def save_batch(entries: List[Dict[str, Any]], batch_num: int):
    """Save batch to JSON file"""
    filename = f"sylva_batch_{batch_num:03d}.json"
    with open(filename, 'w') as f:
        json.dump(entries, f, indent=2)
    return filename

def combine_batches(batch_files: List[str], output_file: str = "sylva_dataset_complete.json"):
    """Combine all batch files into master dataset"""
    all_entries = []
    
    for batch_file in sorted(batch_files):
        if Path(batch_file).exists():
            with open(batch_file, 'r') as f:
                batch_data = json.load(f)
                all_entries.extend(batch_data)
    
    with open(output_file, 'w') as f:
        json.dump(all_entries, f, indent=2)
    
    return len(all_entries)

def generate_full_dataset():
    """Generate the complete SYLVA dataset from entry 41 to 10,000"""
    
    print("🎭 SYLVA Master Dataset Generator")
    print("=" * 50)
    print(f"Target: Entries 41-10,000 ({10000-40} entries total)")
    print(f"Batches: {(10000-40)//100} batches of 100 entries each")
    print()
    
    # Global tracking for variety
    global_used_closures = []
    global_used_prompts = []
    batch_files = []
    
    start_id = 41
    target_id = 10000
    batch_size = 100
    
    batch_num = 1
    current_id = start_id
    
    while current_id < target_id:
        remaining = target_id - current_id
        current_batch_size = min(batch_size, remaining)
        
        print(f"📝 Generating Batch {batch_num}: Entries {current_id}-{current_id + current_batch_size - 1}")
        
        # Generate batch
        batch_entries = generate_batch(current_id, current_batch_size, global_used_closures, global_used_prompts)
        
        # Save batch
        batch_file = save_batch(batch_entries, batch_num)
        batch_files.append(batch_file)
        
        # Progress update
        total_generated = current_id + current_batch_size - start_id
        progress = (total_generated / (target_id - start_id)) * 100
        print(f"✅ Batch {batch_num} complete ({current_batch_size} entries) - {progress:.1f}% total progress")
        
        # Update counters
        current_id += current_batch_size
        batch_num += 1
        
        # Memory management - keep only recent tracking data
        if len(global_used_closures) > 1000:
            global_used_closures = global_used_closures[-500:]
        if len(global_used_prompts) > 1000:
            global_used_prompts = global_used_prompts[-500:]
    
    print(f"\n🎉 All batches generated!")
    print(f"📁 Combining {len(batch_files)} batch files...")
    
    # Combine all batches into master file
    total_entries = combine_batches(batch_files)
    
    print(f"✨ SYLVA Dataset Complete!")
    print(f"📊 Total entries: {total_entries}")
    print(f"💾 Master file: sylva_dataset_complete.json")
    print(f"🧹 Individual batch files preserved for reference")
    
    # Generate summary statistics
    print(f"\n📈 Generation Summary:")
    print(f"   - Entries generated: {total_entries}")
    print(f"   - Unique closures used: {len(set(global_used_closures))}")
    print(f"   - Categories covered: {len(CATEGORIES)}")
    print(f"   - Subcategories: {sum(len(subs) for subs in CATEGORIES.values())}")

if __name__ == "__main__":
    generate_full_dataset()