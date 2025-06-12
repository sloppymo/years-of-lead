#!/usr/bin/env python3
"""
Equipment Profile and Search System Demonstration

This script demonstrates the complete equipment and search system for Years of Lead,
using the exact specifications provided by the user for equipment profiles and
search encounters.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from game.equipment_system import (
    ConsequenceType,
    ConsequenceRule,
    SearchEncounterManager,
    PlayerUniformType,
    create_custom_equipment,
    create_custom_encounter,
)
from game.dynamic_narrative_tone import DynamicNarrativeToneEngine
from game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait


def demonstrate_equipment_profile_system():
    """Demonstrate equipment profile creation and concealment mechanics"""
    print("🔫 Equipment Profile System Demonstration")
    print("=" * 60)

    # Create the exact equipment profile from user's example
    compact_pistol_data = {
        "item_id": "wpn_001",
        "name": "compact pistol",
        "category": "weapon",
        "concealable": True,
        "concealment_rating": 0.7,
        "container_bonus": 0.1,
        "legal_status": "restricted",
        "detected_if_searched": True,
        "associated_flags": ["unregistered_serial", "smuggled"],
        "description": "Small, easily concealed handgun",
        "weight": 1.2,
        "bulk": 0.8,
    }

    # Create equipment using the custom creation function
    compact_pistol = create_custom_equipment(compact_pistol_data)

    # Add the uniform-specific consequence rule as specified
    compact_pistol.consequence_rules["if_player_uniformed"] = ConsequenceRule(
        condition="if_player_uniformed",
        consequence=ConsequenceType.CONFISCATE_AND_WARN,
        description="Weapon confiscated from uniformed personnel",
    )

    print(f"📋 Equipment Profile: {compact_pistol.name}")
    print(f"   Category: {compact_pistol.category.value}")
    print(f"   Legal Status: {compact_pistol.legal_status.value}")
    print(f"   Base Concealment: {compact_pistol.concealment_rating}")
    print(f"   Container Bonus: {compact_pistol.container_bonus}")
    print(f"   Associated Flags: {list(compact_pistol.associated_flags)}")

    # Test concealment with different contexts
    contexts = [
        {"has_container": False, "equipment_flags": set()},
        {"has_container": True, "equipment_flags": set()},
        {"has_container": True, "equipment_flags": {"unregistered_serial"}},
    ]

    print("\n🎯 Concealment Ratings:")
    for i, context in enumerate(contexts, 1):
        concealment = compact_pistol.get_effective_concealment(
            container_present=context["has_container"],
            equipment_flags=context["equipment_flags"],
        )
        container_text = (
            "with container" if context["has_container"] else "no container"
        )
        flags_text = (
            f"flags: {context['equipment_flags']}"
            if context["equipment_flags"]
            else "no flags"
        )
        print(f"   {i}. {concealment:.2f} ({container_text}, {flags_text})")

    # Test consequence determination
    player_contexts = [
        {"uniformed": False, "has_permit": False},
        {"uniformed": False, "has_permit": True},
        {"uniformed": True, "uniform_type": PlayerUniformType.MEDICAL},
    ]

    print("\n⚖️  Consequences by Context:")
    for i, context in enumerate(player_contexts, 1):
        consequence_rule = compact_pistol.get_consequence(context)
        uniform_text = (
            f"uniformed ({context.get('uniform_type', 'N/A')})"
            if context.get("uniformed")
            else "civilian"
        )
        permit_text = "with permit" if context.get("has_permit") else "no permit"
        print(
            f"   {i}. {consequence_rule.consequence.value} ({uniform_text}, {permit_text})"
        )
        print(f"      Description: {consequence_rule.description}")

    return compact_pistol


def demonstrate_search_encounter_system():
    """Demonstrate search encounter creation and execution"""
    print("\n🔍 Search Encounter System Demonstration")
    print("=" * 60)

    # Create the exact search encounter from user's example
    encounter_data = {
        "encounter_id": "search_chkpt_alpha",
        "location": "Checkpoint Alpha",
        "description": "Heavily fortified military checkpoint",
        "trigger": {
            "zone": "occupied",
            "curfew_active": True,
            "player_flagged": True,
            "check_probability": 0.55,
        },
        "npc_profile": {
            "search_rigor": 0.6,
            "tech_bonus": 0.3,
            "disposition": "paranoid",
            "experience_level": 0.8,
        },
        "player_response_options": [
            {
                "id": "comply",
                "text": "You open your bag and remain silent.",
                "outcome": "begin_item_reveal",
                "suspicion_modifier": 0.0,
            },
            {
                "id": "deflect",
                "text": "Do you really need to do this? I'm just trying to get home.",
                "outcome": "suspicion_roll_plus_0.2",
                "suspicion_modifier": 0.2,
            },
            {
                "id": "resist",
                "text": "You step back and prepare to run.",
                "outcome": "combat_or_pursuit_triggered",
                "suspicion_modifier": 0.8,
            },
        ],
    }

    # Create encounter using custom creation function
    checkpoint_alpha = create_custom_encounter(encounter_data)

    print(f"🏛️  Search Encounter: {checkpoint_alpha.encounter_id}")
    print(f"   Location: {checkpoint_alpha.location}")
    print(f"   Description: {checkpoint_alpha.description}")

    print("\n🎯 Trigger Conditions:")
    print(f"   Zone: {checkpoint_alpha.trigger.zone}")
    print(f"   Curfew Required: {checkpoint_alpha.trigger.curfew_active}")
    print(f"   Player Flagged: {checkpoint_alpha.trigger.player_flagged}")
    print(f"   Check Probability: {checkpoint_alpha.trigger.check_probability}")

    print("\n👮 NPC Profile:")
    print(f"   Search Rigor: {checkpoint_alpha.npc_profile.search_rigor}")
    print(f"   Tech Bonus: {checkpoint_alpha.npc_profile.tech_bonus}")
    print(f"   Disposition: {checkpoint_alpha.npc_profile.disposition.value}")
    print(f"   Experience Level: {checkpoint_alpha.npc_profile.experience_level}")
    print(
        f"   Effective Search Rating: {checkpoint_alpha.npc_profile.get_effective_search_rating():.2f}"
    )

    print("\n💬 Player Response Options:")
    for i, response in enumerate(checkpoint_alpha.player_response_options, 1):
        print(f"   {i}. [{response.response_id}] {response.text}")
        print(f"      Outcome: {response.outcome}")
        print(f"      Suspicion Modifier: +{response.suspicion_modifier}")

    # Test trigger conditions
    test_contexts = [
        {"current_zone": "occupied", "curfew_active": True, "player_flagged": True},
        {"current_zone": "occupied", "curfew_active": False, "player_flagged": True},
        {"current_zone": "free", "curfew_active": True, "player_flagged": True},
    ]

    print("\n🎲 Trigger Testing:")
    for i, context in enumerate(test_contexts, 1):
        should_trigger = checkpoint_alpha.trigger.should_trigger(context)
        zone = context["current_zone"]
        curfew = "curfew" if context["curfew_active"] else "no curfew"
        flagged = "flagged" if context["player_flagged"] else "not flagged"
        result = "✅ TRIGGERS" if should_trigger else "❌ No trigger"
        print(f"   {i}. {zone}, {curfew}, {flagged} → {result}")

    return checkpoint_alpha


def demonstrate_detection_formula():
    """Demonstrate the detection formula and probability calculations"""
    print("\n🎯 Detection Formula Demonstration")
    print("=" * 60)

    # Create equipment and encounter
    compact_pistol_data = {
        "item_id": "wpn_001",
        "name": "compact pistol",
        "category": "weapon",
        "concealment_rating": 0.7,
        "container_bonus": 0.1,
        "legal_status": "restricted",
    }

    compact_pistol = create_custom_equipment(compact_pistol_data)

    # Create search encounter
    encounter_data = {
        "encounter_id": "test_search",
        "location": "Test Location",
        "trigger": {"check_probability": 1.0},
        "npc_profile": {
            "search_rigor": 0.6,
            "tech_bonus": 0.3,
            "disposition": "paranoid",
        },
    }

    encounter = create_custom_encounter(encounter_data)

    print(
        "📊 Detection Formula: search_rigor + tech_bonus + rng - (concealment_rating + player_bonus)"
    )
    print(f"   Search Rigor: {encounter.npc_profile.search_rigor}")
    print(f"   Tech Bonus: {encounter.npc_profile.tech_bonus}")
    print("   Disposition Modifier: +0.2 (paranoid)")
    print(
        f"   Effective Search Rating: {encounter.npc_profile.get_effective_search_rating():.2f}"
    )

    print(f"\n🎯 Item: {compact_pistol.name}")
    print(f"   Base Concealment: {compact_pistol.concealment_rating}")

    # Test different player contexts
    player_contexts = [
        {"concealment_bonus": 0.0, "has_container": False, "description": "No bonuses"},
        {
            "concealment_bonus": 0.2,
            "has_container": False,
            "description": "Skill bonus (+0.2)",
        },
        {
            "concealment_bonus": 0.0,
            "has_container": True,
            "description": "Container bonus",
        },
        {"concealment_bonus": 0.2, "has_container": True, "description": "All bonuses"},
    ]

    print("\n🎲 Detection Probabilities (10 rolls each):")
    for context in player_contexts:
        print(f"\n   {context['description']}:")

        # Calculate effective concealment
        effective_concealment = compact_pistol.get_effective_concealment(
            container_present=context["has_container"]
        )
        total_concealment = effective_concealment + context["concealment_bonus"]

        print(f"   Total Concealment: {total_concealment:.2f}")

        # Run multiple detection attempts
        detections = 0
        detection_probs = []

        for _ in range(10):
            prob = encounter.calculate_detection_probability(compact_pistol, context)
            detection_probs.append(prob)
            if prob > 0.5:  # Simplified threshold for demo
                detections += 1

        avg_prob = sum(detection_probs) / len(detection_probs)
        print(f"   Average Detection Probability: {avg_prob:.2f}")
        print(f"   Detections (>50% prob): {detections}/10")


def demonstrate_full_search_execution():
    """Demonstrate complete search encounter execution"""
    print("\n🎬 Full Search Encounter Execution")
    print("=" * 60)

    # Create search manager
    search_manager = SearchEncounterManager()

    # Create player inventory with multiple items
    inventory_items = [
        {
            "item_id": "wpn_001",
            "name": "compact pistol",
            "category": "weapon",
            "concealment_rating": 0.7,
            "legal_status": "restricted",
            "associated_flags": ["unregistered_serial"],
        },
        {
            "item_id": "doc_001",
            "name": "forged papers",
            "category": "document",
            "concealment_rating": 0.9,
            "legal_status": "contraband",
        },
        {
            "item_id": "med_001",
            "name": "medical supplies",
            "category": "medical",
            "concealment_rating": 0.2,
            "legal_status": "legal",
        },
    ]

    # Register equipment
    inventory_profiles = []
    for item_data in inventory_items:
        equipment = create_custom_equipment(item_data)
        search_manager.register_equipment(equipment)
        inventory_profiles.append(equipment)
        print(
            f"📦 Registered: {equipment.name} (concealment: {equipment.concealment_rating}, legal: {equipment.legal_status.value})"
        )

    # Execute search with different player contexts
    player_contexts = [
        {
            "description": "Civilian, no permits, no bonuses",
            "uniformed": False,
            "has_permit": False,
            "concealment_bonus": 0.0,
            "has_container": False,
        },
        {
            "description": "Medical uniform, with permits, skill bonus",
            "uniformed": True,
            "uniform_type": PlayerUniformType.MEDICAL,
            "has_permit": True,
            "concealment_bonus": 0.3,
            "has_container": True,
        },
    ]

    for i, context in enumerate(player_contexts, 1):
        print(f"\n🎭 Scenario {i}: {context['description']}")
        print("-" * 50)

        # Execute search using the checkpoint encounter
        results = search_manager.execute_encounter(
            "search_chkpt_alpha", [item["item_id"] for item in inventory_items], context
        )

        print(f"📍 Location: {results['location']}")
        print(f"🔍 Detected Items: {len(results['detected_items'])}")

        if results["detected_items"]:
            for item in results["detected_items"]:
                print(f"   ❌ {item.name} (concealment: {item.concealment_rating})")

        print(f"🙈 Missed Items: {len(results['missed_items'])}")
        if results["missed_items"]:
            for item in results["missed_items"]:
                print(f"   ✅ {item.name} (concealment: {item.concealment_rating})")

        print("⚖️  Consequences:")
        if results["consequences"]:
            for cons in results["consequences"]:
                print(f"   • {cons['item']}: {cons['consequence']}")
                print(f"     {cons['description']}")
        else:
            print("   • No consequences")

        print(f"🚨 Suspicion Level: {results['suspicion_level']:.2f}")

        print("\n📖 Narrative:")
        print(f"   {results['narrative']}")


def demonstrate_narrative_integration():
    """Demonstrate integration with the dynamic narrative tone system"""
    print("\n🎭 Narrative Integration Demonstration")
    print("=" * 60)

    # Create character with voice configuration
    creator = CharacterCreator()
    character = creator.create_character(
        name="Marcus Chen",
        background_type=BackgroundType.CRIMINAL,
        primary_trait=PersonalityTrait.CAUTIOUS,
        secondary_trait=PersonalityTrait.OPPORTUNISTIC,
    )

    # Set up narrative tone engine
    tone_engine = DynamicNarrativeToneEngine()
    tone_engine.register_voice_configuration(character.voice_config)

    # Add some search-specific voice lines
    character.voice_config.add_player_line(
        "Another checkpoint. They're getting more thorough."
    )
    character.voice_config.add_player_line(
        "The guard's eyes linger too long on your bag."
    )
    character.voice_config.add_player_line(
        "You keep your breathing steady. Show no fear."
    )

    print(f"👤 Character: {character.name}")
    print(f"   Background: {character.background.name}")
    print(
        f"   Traits: {character.traits.primary_trait.value}, {character.traits.secondary_trait.value}"
    )
    print(
        f"   Voice Tones: {[tone.value for tone in character.voice_config.emotional_tones]}"
    )

    # Create search scenario
    # search_manager = SearchEncounterManager()

    # Base search events
    base_events = [
        "You approach the checkpoint with steady steps.",
        "The guard signals for you to open your bag.",
        "A thorough search reveals your hidden items.",
        "The officer examines your identification papers.",
        "You're waved through after the inspection.",
    ]

    print("\n📝 Enhanced Search Narratives:")
    for i, base_event in enumerate(base_events, 1):
        enhanced = tone_engine.generate_narrative_with_voice(
            character.id,
            base_event,
            {
                "event_type": "search_encounter",
                "tension_level": 0.7,
                "location": "checkpoint",
            },
        )

        print(f"\n{i}. Base: {base_event}")
        print(f"   Enhanced: {enhanced}")


def demonstrate_equipment_flags():
    """Demonstrate equipment flags and their effects"""
    print("\n🏷️  Equipment Flags Demonstration")
    print("=" * 60)

    # Create search manager to access flag system
    search_manager = SearchEncounterManager()

    print("📋 Available Equipment Flags:")
    for flag_id, flag in search_manager.flag_registry.items():
        print(f"   • {flag.name} ({flag_id})")
        print(f"     Description: {flag.description}")
        print(f"     Concealment Modifier: {flag.concealment_modifier:+.1f}")
        print(f"     Suspicion Modifier: {flag.suspicion_modifier:+.1f}")

    # Demonstrate flag effects on the compact pistol
    pistol_data = {
        "item_id": "wpn_001",
        "name": "compact pistol",
        "category": "weapon",
        "concealment_rating": 0.7,
        "legal_status": "restricted",
        "associated_flags": ["unregistered_serial", "smuggled"],
    }

    pistol = create_custom_equipment(pistol_data)

    print(f"\n🔫 Equipment: {pistol.name}")
    print(f"   Base Concealment: {pistol.concealment_rating}")
    print(f"   Associated Flags: {list(pistol.associated_flags)}")

    # Note: Flag effects would be calculated in the actual system
    # This is a simplified demonstration
    print("\n⚠️  Flag Effects (simulated):")
    print("   • Unregistered Serial: -0.0 concealment, +0.3 suspicion")
    print("   • Smuggled: -0.1 concealment, +0.2 suspicion")
    print("   • Combined Effect: Harder to hide, much more suspicious if found")


def run_comprehensive_demonstration():
    """Run complete demonstration of the equipment and search system"""
    print("🎮 Years of Lead - Equipment Profile & Search System")
    print("🔍 Comprehensive System Demonstration")
    print("=" * 80)

    try:
        # Run all demonstrations
        demonstrate_equipment_profile_system()
        demonstrate_search_encounter_system()
        demonstrate_detection_formula()
        demonstrate_full_search_execution()
        demonstrate_narrative_integration()
        demonstrate_equipment_flags()

        print("\n🎉 Demonstration Complete!")
        print("=" * 80)

        print("\n✅ Key Features Demonstrated:")
        print("  • Equipment profiles with concealment and legal status")
        print("  • Search encounters with trigger conditions")
        print(
            "  • Detection formula: search_rigor + tech_bonus + rng - (concealment + player_bonus)"
        )
        print("  • Consequence system based on legal status and context")
        print("  • Player response options with different outcomes")
        print("  • NPC disposition effects on search behavior")
        print("  • Equipment flags for additional complexity")
        print("  • Integration with dynamic narrative tone system")

        print("\n📊 System Statistics:")
        # Create a search manager to get statistics
        stats_manager = SearchEncounterManager()
        summary = stats_manager.get_encounter_summary()
        print(f"  • Total Encounters: {summary['total_encounters']}")
        print(f"  • Total Equipment: {summary['total_equipment']}")
        print(f"  • Total Flags: {summary['total_flags']}")
        print(f"  • Equipment Categories: {len(summary['equipment_categories'])}")

        print("\n🎯 Example Consequences by Legal Status:")
        print("  • LEGAL: Mild suspicion only")
        print("  • RESTRICTED: Interrogation and confiscation (no permit)")
        print("  • PROHIBITED: Arrest")
        print("  • CONTRABAND: Arrest and flag player")

        print("\n🎲 Detection Factors:")
        print("  • Search Rigor: Base NPC search capability")
        print("  • Tech Bonus: Technology assistance (scanners, etc.)")
        print("  • Disposition: NPC attitude (-0.1 to +0.3 modifier)")
        print("  • Experience: NPC skill level")
        print("  • Concealment Rating: Item's hidability")
        print("  • Container Bonus: Additional concealment in bags/containers")
        print("  • Player Bonuses: Skills, circumstances, etc.")
        print("  • Equipment Flags: Modify concealment and suspicion")

        return True

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_demonstration()
    if success:
        print("\n🚀 Equipment and Search System fully operational!")
        print("Ready for integration into Years of Lead gameplay.")
    else:
        print("\n💥 Demo failed - check implementation.")
        sys.exit(1)
