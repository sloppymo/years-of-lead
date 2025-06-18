#!/usr/bin/env python3
"""
Years of Lead - Victory/Defeat Conditions & Enhanced Save System Demo
This script demonstrates the newly implemented victory/defeat conditions and enhanced save/load system
"""

import os
import sys
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def print_header():
    """Print the demo header"""
    header = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║               🎮 YEARS OF LEAD: VICTORY/DEFEAT & SAVE SYSTEM DEMO                ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  🎯 NEW FEATURES IMPLEMENTED:                                                    ║
║                                                                                  ║
║  🏆 VICTORY/DEFEAT CONDITIONS                                                    ║
║     • Victory when resistance achieves its goals                                 ║
║     • Defeat when resistance is crushed                                          ║
║     • Dynamic win/loss conditions based on game state                            ║
║     • Victory progress tracking                                                  ║
║                                                                                  ║
║  💾 ENHANCED SAVE/LOAD SYSTEM                                                    ║
║     • Rich metadata for each save                                                ║
║     • Turn number, date, and game version                                        ║
║     • Agent count and controlled locations                                       ║
║     • Public support percentage                                                  ║
║     • Resource levels                                                            ║
║     • Victory progress tracking                                                  ║
║     • Active mission count                                                       ║
║                                                                                  ║
║  🔄 IMPROVED GAME FLOW                                                           ║
║     • Clear victory/defeat screens                                               ║
║     • Game over states with summaries                                            ║
║     • Autosave functionality                                                     ║
║     • Detailed save browsing                                                     ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""
    print(header)


def demonstrate_victory_conditions():
    """Demonstrate the victory conditions"""
    print("\n" + "=" * 80)
    print("🏆 VICTORY CONDITIONS DEMONSTRATION")
    print("=" * 80)

    print("\nVictory is achieved when ALL of the following conditions are met:")
    victory_conditions = [
        ("Public Support", "75% or higher", "Currently: 45%"),
        ("Controlled Locations", "3 or more", "Currently: 2/5"),
        ("Enemy Strength", "Below 25%", "Currently: 40%"),
    ]

    print("\n" + "-" * 60)
    print(f"{'Condition':<25} {'Requirement':<20} {'Status':<15}")
    print("-" * 60)
    for condition, requirement, status in victory_conditions:
        print(f"{condition:<25} {requirement:<20} {status:<15}")
    print("-" * 60)

    print("\nVictory Progress: [████████░░] 80%")
    print("\nWhen victory is achieved:")
    print("  • Game displays victory screen")
    print("  • Final narrative summary is generated")
    print("  • Game statistics are displayed")
    print("  • Option to continue playing or start new game")


def demonstrate_defeat_conditions():
    """Demonstrate the defeat conditions"""
    print("\n" + "=" * 80)
    print("💀 DEFEAT CONDITIONS DEMONSTRATION")
    print("=" * 80)

    print("\nDefeat occurs when ANY of the following conditions are met:")
    defeat_conditions = [
        ("Public Support", "Falls below 15%", "Currently: 45%"),
        ("Agents Remaining", "Only 1 or fewer", "Currently: 5"),
        ("Resources", "Below 10", "Currently: 120"),
    ]

    print("\n" + "-" * 60)
    print(f"{'Condition':<25} {'Threshold':<20} {'Status':<15}")
    print("-" * 60)
    for condition, threshold, status in defeat_conditions:
        print(f"{condition:<25} {threshold:<20} {status:<15}")
    print("-" * 60)

    print("\nRisk of Defeat: [██░░░░░░░░] 20%")
    print("\nWhen defeat occurs:")
    print("  • Game displays defeat screen")
    print("  • Failure narrative is generated")
    print("  • Game statistics are displayed")
    print("  • Option to load save or start new game")


def demonstrate_enhanced_save_system():
    """Demonstrate the enhanced save system"""
    print("\n" + "=" * 80)
    print("💾 ENHANCED SAVE SYSTEM DEMONSTRATION")
    print("=" * 80)

    # Show save metadata
    print("\n📊 SAVE METADATA EXAMPLE:")
    print("-" * 60)
    metadata = {
        "save_name": "resistance_university_mission",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "game_version": "1.2.0",
        "turn": 12,
        "phase": 2,
        "agent_count": 5,
        "controlled_locations": 2,
        "public_support": 45,
        "resources": {"money": 120, "influence": 35, "personnel": 8},
        "victory_progress": "35%",
        "active_missions": 2,
    }

    for key, value in metadata.items():
        print(f"{key.replace('_', ' ').title():<20}: {value}")

    # Show save/load menu
    print("\n📋 SAVE/LOAD MENU EXAMPLE:")
    print("-" * 60)
    print("1. Save Game")
    print("2. Load Game")
    print("3. Delete Save")
    print("4. Back")

    # Show save list with metadata
    print("\n📂 SAVE BROWSER WITH METADATA:")
    print("-" * 60)
    saves = [
        {
            "name": "resistance_turn_12",
            "turn": 12,
            "date": "2025-06-10",
            "agents": 5,
            "support": 42,
        },
        {
            "name": "university_mission",
            "turn": 8,
            "date": "2025-06-08",
            "agents": 4,
            "support": 38,
        },
        {
            "name": "autosave_turn_15",
            "turn": 15,
            "date": "2025-06-12",
            "agents": 6,
            "support": 51,
        },
    ]

    for i, save in enumerate(saves, 1):
        print(f"{i}. {save['name']}")
        print(
            f"   Turn: {save['turn']} | Date: {save['date']} | Agents: {save['agents']} | Support: {save['support']}%"
        )

    print("\n🔄 AUTOSAVE FUNCTIONALITY:")
    print("-" * 60)
    print("• Autosaves created at the start of each turn")
    print("• Autosave naming: autosave_turn_X_YYYY-MM-DD")
    print("• Configurable autosave frequency")
    print("• Autosave rotation (keeps last 5 autosaves)")


def demonstrate_game_over_screens():
    """Demonstrate the game over screens"""
    print("\n" + "=" * 80)
    print("🎮 GAME OVER SCREENS")
    print("=" * 80)

    # Victory screen
    print("\n" + "=" * 60)
    print("🏆 VICTORY ACHIEVED!")
    print("=" * 60)
    print("\nThe resistance has succeeded in its goals. The government has fallen,")
    print("and a new era begins for the people. Your leadership has changed history.")
    print("\nFinal Statistics:")
    print("• Turns Played: 32")
    print("• Missions Completed: 18")
    print("• Agents Recruited: 12")
    print("• Public Support: 82%")
    print("• Controlled Locations: 4/5")
    print("\nPress any key to continue...")

    # Defeat screen
    print("\n\n" + "=" * 60)
    print("💀 DEFEAT SUFFERED!")
    print("=" * 60)
    print("\nThe resistance has been crushed. Your remaining agents have been")
    print("captured or gone into hiding. The government's grip tightens further.")
    print("\nFinal Statistics:")
    print("• Turns Survived: 24")
    print("• Missions Completed: 9")
    print("• Agents Lost: 8")
    print("• Public Support: 12%")
    print("• Controlled Locations: 1/5")
    print("\nPress any key to continue...")


def main():
    """Run the demo"""
    print_header()

    choice = input(
        "\nExplore which feature? (1=Victory/Defeat, 2=Save System, 3=Game Over Screens, 4=All): "
    )

    if choice == "1":
        demonstrate_victory_conditions()
        demonstrate_defeat_conditions()
    elif choice == "2":
        demonstrate_enhanced_save_system()
    elif choice == "3":
        demonstrate_game_over_screens()
    else:
        demonstrate_victory_conditions()
        demonstrate_defeat_conditions()
        demonstrate_enhanced_save_system()
        demonstrate_game_over_screens()

    print("\n" + "=" * 80)
    print("🚀 READY TO EXPERIENCE THE NEW FEATURES?")
    print("=" * 80)
    print("Launch the game with:")
    print("  python main.py --mode cli")
    print("\nHappy commanding, operative! 🎮")


if __name__ == "__main__":
    main()
