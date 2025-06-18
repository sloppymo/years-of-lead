#!/usr/bin/env python3
"""
Years of Lead - Add Character to CLI Game

This script shows how to create custom characters and add them
to your existing CLI game session.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from game.character_creation import BackgroundType, PersonalityTrait
from integration_demo import CharacterGameIntegrator


def quick_add_character_examples():
    """Show how to quickly add pre-designed characters to your game"""

    integrator = CharacterGameIntegrator()

    print("🎮 ADDING CUSTOM CHARACTERS TO YOUR CLI GAME")
    print("=" * 60)

    print("\n📋 Current Game Agents:")
    for agent_id, agent in integrator.game_state.agents.items():
        print(f"  • {agent.name} - {agent.faction_id} - Status: {agent.status}")

    print("\n🎭 Creating 3 Custom Characters for Your Game...")

    # Character 1: Tech Specialist
    print("\n--- CHARACTER 1: TECH SPECIALIST ---")
    char1 = integrator.character_creator.quick_create_character("Maya Chen")
    agent1 = integrator.add_character_to_game(
        char1, "resistance", "university_district"
    )

    print(f"✅ {char1.name} ({char1.background.name})")
    print(
        f"   Primary Skills: Hacking({char1.skills.hacking}) Technical({char1.skills.technical})"
    )
    print("   Specialization: Technical operations and cyber warfare")
    print(f"   Game Status: Added to {agent1.faction_id} faction")

    # Character 2: Social Infiltrator
    print("\n--- CHARACTER 2: SOCIAL INFILTRATOR ---")
    char2 = integrator.character_creator.quick_create_character("Dmitri Volkov")
    agent2 = integrator.add_character_to_game(
        char2, "urban_liberation", "government_quarter"
    )

    print(f"✅ {char2.name} ({char2.background.name})")
    print(
        f"   Primary Skills: Social({char2.skills.social}) Stealth({char2.skills.stealth})"
    )
    print("   Specialization: Infiltration and social manipulation")
    print(f"   Game Status: Added to {agent2.faction_id} faction")

    # Character 3: Combat Veteran
    print("\n--- CHARACTER 3: COMBAT VETERAN ---")
    char3 = integrator.character_creator.quick_create_character("Sarah Martinez")
    agent3 = integrator.add_character_to_game(char3, "underground", "industrial_zone")

    print(f"✅ {char3.name} ({char3.background.name})")
    print(
        f"   Primary Skills: Combat({char3.skills.combat}) Survival({char3.skills.survival})"
    )
    print("   Specialization: Direct action and military operations")
    print(f"   Game Status: Added to {agent3.faction_id} faction")

    print("\n📊 UPDATED GAME STATE:")
    print(f"Total Agents: {len(integrator.game_state.agents)}")
    print(
        f"Resistance: {len([a for a in integrator.game_state.agents.values() if a.faction_id == 'resistance'])} agents"
    )
    print(
        f"Urban Liberation: {len([a for a in integrator.game_state.agents.values() if a.faction_id == 'urban_liberation'])} agents"
    )
    print(
        f"Underground: {len([a for a in integrator.game_state.agents.values() if a.faction_id == 'underground'])} agents"
    )

    print("\n📖 Recent Narrative Events:")
    for narrative in integrator.game_state.recent_narrative[-6:]:
        print(f"  • {narrative}")

    print("\n🎮 To use these characters in your CLI game:")
    print("   1. Start the game: python main.py --mode cli")
    print("   2. Use command [2] to see all agents including your custom ones")
    print("   3. Use command [4] to assign tasks to your custom characters")
    print("   4. Use command [8] to create missions with your custom characters")

    return integrator.game_state


def integrate_character_into_main_game():
    """Show how the integration affects the actual main game"""

    print("\n🔧 INTEGRATION WITH MAIN GAME CLI")
    print("=" * 50)

    print("When you add custom characters to the game, they become fully integrated:")
    print()
    print("✅ Appear in agent lists (command [2] in CLI)")
    print("✅ Can be assigned tasks (command [4] in CLI)")
    print("✅ Can join missions (command [9] in CLI)")
    print("✅ Participate in turn advancement (command [1] in CLI)")
    print("✅ Generate narrative events based on their personalities")
    print("✅ Use their custom skills for mission success calculations")
    print("✅ React emotionally to events based on their psychological profile")
    print("✅ Form relationships with other agents based on compatibility")

    print("\n📝 EXAMPLE CLI COMMANDS WITH YOUR CUSTOM CHARACTERS:")
    print()
    print("python main.py --mode cli")
    print("  [2] - See Maya Chen, Dmitri Volkov, Sarah Martinez in agent list")
    print("  [4] Maya Chen - Assign hacking tasks to the tech specialist")
    print("  [8] - Create infiltration mission using Dmitri's social skills")
    print("  [9] Sarah Martinez - Add combat veteran to rescue mission")
    print("  [1] - Advance turn and see how their personalities affect outcomes")


def create_character_for_specific_mission():
    """Create a character designed for a specific mission type"""

    print("\n🎯 CREATING MISSION-SPECIFIC CHARACTERS")
    print("=" * 50)

    mission_types = {
        "assassination": {
            "background": BackgroundType.MILITARY,
            "traits": [PersonalityTrait.RUTHLESS, PersonalityTrait.PRAGMATIC],
            "description": "Cold, efficient killer for high-value targets",
        },
        "intelligence": {
            "background": BackgroundType.JOURNALIST,
            "traits": [PersonalityTrait.ANALYTICAL, PersonalityTrait.CAUTIOUS],
            "description": "Information gatherer and analyst",
        },
        "propaganda": {
            "background": BackgroundType.ACTIVIST,
            "traits": [PersonalityTrait.IDEALISTIC, PersonalityTrait.LEADER],
            "description": "Charismatic speaker for recruitment and morale",
        },
        "sabotage": {
            "background": BackgroundType.TECHNICAL,
            "traits": [PersonalityTrait.CREATIVE, PersonalityTrait.RECKLESS],
            "description": "Technical saboteur with unconventional methods",
        },
        "recruitment": {
            "background": BackgroundType.RELIGIOUS,
            "traits": [PersonalityTrait.COMPASSIONATE, PersonalityTrait.OPTIMISTIC],
            "description": "Inspiring recruiter who builds trust",
        },
    }

    integrator = CharacterGameIntegrator()

    print("Select mission type for character optimization:")
    for i, (mission_type, info) in enumerate(mission_types.items(), 1):
        print(f"{i}. {mission_type.title()} - {info['description']}")

    try:
        choice = int(input(f"\nEnter choice (1-{len(mission_types)}): "))
        mission_type = list(mission_types.keys())[choice - 1]
        mission_info = mission_types[mission_type]

        print(f"\n🎭 Creating character optimized for {mission_type} missions...")

        # Create specialized character
        character = integrator.character_creator.quick_create_character(
            f"Agent_{mission_type.title()}"
        )

        # Show how character fits the mission
        print(f"\n✅ {character.name} Created!")
        print(f"Background: {character.background.name} (Optimal for {mission_type})")
        print(f"Personality: {character.traits.get_trait_description()}")
        print(f"Mission Fit: {mission_info['description']}")

        # Add to game
        agent = integrator.add_character_to_game(character)

        print(f"\n🎮 {character.name} is now ready for {mission_type} missions!")
        print(f"In CLI game, use command [8] to create {mission_type} missions")
        print(f"Then use command [9] to add {character.name} to the mission")

    except (ValueError, IndexError):
        print("❌ Invalid choice")


def main():
    """Main function for character integration"""

    print("🎮 YEARS OF LEAD - CHARACTER INTEGRATION HELPER")
    print("=" * 60)
    print()
    print("How would you like to add characters to your game?")
    print()
    print("1. Quick Add - Add 3 pre-designed characters")
    print("2. Create Custom Character")
    print("3. Create Mission-Specific Character")
    print("4. Show Integration Guide")
    print("5. Exit")

    choice = input("\nEnter choice (1-5): ").strip()

    if choice == "1":
        quick_add_character_examples()
        integrate_character_into_main_game()

    elif choice == "2":
        integrator = CharacterGameIntegrator()
        print("\n🎭 Starting Interactive Character Creation...")
        character = integrator.character_creator.run_character_creation()

        if character:
            print(f"\n🔗 Adding {character.name} to your game...")
            agent = integrator.add_character_to_game(character)
            print(f"✅ {character.name} is now active in your CLI game!")
            integrate_character_into_main_game()

    elif choice == "3":
        create_character_for_specific_mission()
        integrate_character_into_main_game()

    elif choice == "4":
        integrate_character_into_main_game()

    elif choice == "5":
        print("👋 Goodbye!")

    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
