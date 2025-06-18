#!/usr/bin/env python3
"""
Years of Lead - Enhanced Navigation, Save/Load System, and Victory/Defeat Demo
This script demonstrates the newly implemented features:
1. Enhanced navigation with arrow keys and mouse support
2. Comprehensive save/load system with metadata
3. Victory and defeat conditions with game over screens
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
║            🎮 YEARS OF LEAD: ENHANCED NAVIGATION & GAME SYSTEMS DEMO             ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  🎯 NEW FEATURES IMPLEMENTED:                                                    ║
║                                                                                  ║
║  🖱️ ENHANCED NAVIGATION                                                          ║
║     • Arrow key navigation (↑/↓ to select, Enter to execute)                     ║
║     • Mouse support (click to select, double-click to execute)                   ║
║     • Visual selection indicators and breadcrumb navigation                      ║
║     • Preserved keyboard shortcuts for power users                               ║
║                                                                                  ║
║  💾 COMPREHENSIVE SAVE/LOAD SYSTEM                                               ║
║     • Rich metadata for each save                                                ║
║     • Turn number, date, and game version                                        ║
║     • Agent count and controlled locations                                       ║
║     • Public support percentage                                                  ║
║     • Victory progress tracking                                                  ║
║     • Autosave functionality                                                     ║
║                                                                                  ║
║  🏆 VICTORY/DEFEAT CONDITIONS                                                    ║
║     • Dynamic win/loss conditions based on game state                            ║
║     • Victory when resistance achieves its goals                                 ║
║     • Defeat when resistance is crushed                                          ║
║     • Game over screens with statistics                                          ║
║     • Victory/defeat autosaves                                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""
    print(header)


def demonstrate_navigation():
    """Demonstrate the enhanced navigation features"""
    print("\n" + "=" * 80)
    print("🖱️ ENHANCED NAVIGATION DEMONSTRATION")
    print("=" * 80)

    print("\nThe game now supports multiple navigation methods:")

    print("\n1. KEYBOARD SHORTCUTS (Power User Mode)")
    print("   • Single-key commands (A for advance, G for agents, etc.)")
    print("   • Fast and efficient for experienced players")
    print("   • Compatible with all previous keyboard shortcuts")

    print("\n2. ARROW KEY NAVIGATION")
    print("   • Use ↑/↓ arrow keys to move selection")
    print("   • Press Enter to execute selected command")
    print("   • Visual indicators show current selection")
    print("   • Works in all menus and submenus")

    print("\n3. MOUSE NAVIGATION")
    print("   • Click on menu items to select them")
    print("   • Double-click to execute commands")
    print("   • Intuitive and beginner-friendly")

    print("\nAll navigation methods work together seamlessly!")
    print("• The game detects and responds to your preferred input method")
    print("• Switch between methods at any time")
    print("• Breadcrumb navigation shows your current location in nested menus")


def demonstrate_save_load():
    """Demonstrate the enhanced save/load system"""
    print("\n" + "=" * 80)
    print("💾 ENHANCED SAVE/LOAD SYSTEM DEMONSTRATION")
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

    # Show save browser with metadata
    print("\n📂 SAVE BROWSER WITH METADATA:")
    print("-" * 80)
    print(
        f"{'#':<3} {'Name':<20} {'Turn':<5} {'Date':<20} {'Agents':<7} {'Support':<8} {'Progress':<10} {'Type':<8}"
    )
    print("-" * 80)

    saves = [
        {
            "name": "resistance_turn_12",
            "turn": 12,
            "date": "2025-06-10",
            "agents": 5,
            "support": 42,
            "progress": "38%",
            "type": "Manual",
        },
        {
            "name": "university_mission",
            "turn": 8,
            "date": "2025-06-08",
            "agents": 4,
            "support": 38,
            "progress": "25%",
            "type": "Manual",
        },
        {
            "name": "autosave_turn_15",
            "turn": 15,
            "date": "2025-06-12",
            "agents": 6,
            "support": 51,
            "progress": "45%",
            "type": "Autosave",
        },
        {
            "name": "victory_turn_30",
            "turn": 30,
            "date": "2025-06-15",
            "agents": 8,
            "support": 78,
            "progress": "100%",
            "type": "Victory",
        },
    ]

    for i, save in enumerate(saves, 1):
        print(
            f"{i:<3} {save['name'][:20]:<20} {save['turn']:<5} {save['date'][:20]:<20} {save['agents']:<7} {save['support']}%{'':<3} {save['progress']:<10} {save['type']:<8}"
        )

    print("\n🔄 AUTOSAVE FUNCTIONALITY:")
    print("-" * 60)
    print("• Autosaves created at the start of each turn")
    print("• Autosave naming: autosave_turn_X_YYYY-MM-DD")
    print("• Victory/defeat saves created automatically")
    print("• Special metadata for different save types")


def demonstrate_victory_defeat():
    """Demonstrate the victory/defeat conditions"""
    print("\n" + "=" * 80)
    print("🏆 VICTORY/DEFEAT CONDITIONS DEMONSTRATION")
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

    # Show victory screen
    print("\n" + "=" * 60)
    print("🏆 VICTORY ACHIEVED!")
    print("=" * 60)

    print("\nThe resistance has succeeded in its goals. The government has fallen,")
    print("and a new era begins for the people. Your leadership has changed history.")

    print("\nFinal Statistics:")
    print("• Turns Played: 32")
    print("• Agents Recruited: 12")
    print("• Public Support: 82%")
    print("• Controlled Locations: 4/5")
    print("• Victory saved as: victory_turn_32_20250615_184532")

    # Show defeat screen
    print("\n\n" + "=" * 60)
    print("💀 DEFEAT SUFFERED!")
    print("=" * 60)

    print("\nThe resistance has been crushed. Your remaining agents have been")
    print("captured or gone into hiding. The government's grip tightens further.")

    print("\nFinal Statistics:")
    print("• Turns Survived: 24")
    print("• Agents Remaining: 1")
    print("• Public Support: 12%")
    print("• Controlled Locations: 1/5")
    print("• Defeat saved as: defeat_turn_24_20250615_184532")


def main():
    """Run the demo"""
    print_header()

    choice = input(
        "\nExplore which feature? (1=Navigation, 2=Save/Load, 3=Victory/Defeat, 4=All): "
    )

    if choice == "1":
        demonstrate_navigation()
    elif choice == "2":
        demonstrate_save_load()
    elif choice == "3":
        demonstrate_victory_defeat()
    else:
        demonstrate_navigation()
        demonstrate_save_load()
        demonstrate_victory_defeat()

    print("\n" + "=" * 80)
    print("🚀 READY TO EXPERIENCE THE NEW FEATURES?")
    print("=" * 80)
    print("Launch the game with:")
    print("  python src/main.py")
    print("\nHappy commanding, operative! 🎮")


if __name__ == "__main__":
    main()
