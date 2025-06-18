#!/usr/bin/env python3
"""
Years of Lead - Enhanced Navigation Demo

Demonstrates DF/Rimworld-style navigation improvements:
- Number key navigation (1-9)
- Escape key functionality
- Multi-pane layouts
- Context-sensitive menus
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"🎮 {title}")
    print("=" * 80)


def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 60)


def create_demo_game_state():
    """Create a demo game state for navigation testing"""
    from game.core import GameState, Agent
    from game.emotional_state import EmotionalState

    # Create game state
    game_state = GameState()
    game_state.agents = {}
    game_state.locations = {
        "downtown": {"name": "Downtown District", "type": "urban"},
        "industrial": {"name": "Industrial District", "type": "industrial"},
        "residential": {"name": "Residential District", "type": "residential"},
        "government": {"name": "Government District", "type": "government"},
    }
    game_state.factions = {
        "resistance": {"name": "Resistance Movement", "type": "rebel"},
        "government": {"name": "Government Forces", "type": "authority"},
        "neutral": {"name": "Neutral Faction", "type": "neutral"},
    }
    game_state.turn_number = 1

    # Create sample agents
    agent_data = [
        {
            "id": "agent_001",
            "name": "Maria Santos",
            "background": "veteran",
            "faction": "resistance",
            "location": "downtown",
            "stress": 65,
            "loyalty": 85,
        },
        {
            "id": "agent_002",
            "name": "James Chen",
            "background": "student",
            "faction": "resistance",
            "location": "residential",
            "stress": 45,
            "loyalty": 70,
        },
        {
            "id": "agent_003",
            "name": "Elena Rodriguez",
            "background": "organizer",
            "faction": "resistance",
            "location": "industrial",
            "stress": 80,
            "loyalty": 90,
        },
        {
            "id": "agent_004",
            "name": "David Kim",
            "background": "insider",
            "faction": "government",
            "location": "government",
            "stress": 90,
            "loyalty": 40,
        },
    ]

    for data in agent_data:
        agent = Agent(
            id=data["id"],
            name=data["name"],
            faction_id=data["faction"],
            location_id=data["location"],
        )
        agent.background = data["background"]
        agent.status = "active"
        agent.stress = data["stress"]
        agent.loyalty = data["loyalty"]

        # Add emotional state
        agent.emotional_state = EmotionalState()
        agent.emotional_state.trauma_level = 0.3
        agent.emotional_state.fear = 0.2
        agent.emotional_state.anger = 0.1
        agent.emotional_state.trust = 0.6

        game_state.agents[agent.id] = agent

    return game_state


def demonstrate_number_navigation(nav_system):
    """Demonstrate number key navigation"""
    print_section("NUMBER KEY NAVIGATION (1-9)")

    print("Testing number key navigation in main menu:")
    for i in range(1, 10):
        result = nav_system.handle_input(str(i))
        print(f"  {i}: {result}")
        time.sleep(0.5)

    print("\nTesting arrow key navigation:")
    nav_system.handle_input("up")
    nav_system.handle_input("down")
    nav_system.handle_input("down")
    print("  Arrow keys work for selection")


def demonstrate_escape_functionality(nav_system):
    """Demonstrate escape key functionality"""
    print_section("ESCAPE KEY FUNCTIONALITY")

    print("Navigating to different panes and using escape to return:")

    # Navigate to agents
    print("  Navigating to Agent Management...")
    result = nav_system.handle_input("2")
    print(f"  Result: {result}")

    # Navigate within agents
    print("  Selecting agent list...")
    result = nav_system.handle_input("1")
    print(f"  Result: {result}")

    # Use escape to go back
    print("  Using escape to go back...")
    result = nav_system.handle_input("esc")
    print(f"  Result: {result}")

    # Navigate to missions
    print("  Navigating to Mission Operations...")
    result = nav_system.handle_input("3")
    print(f"  Result: {result}")

    # Use escape to go back
    print("  Using escape to go back...")
    result = nav_system.handle_input("esc")
    print(f"  Result: {result}")


def demonstrate_multi_pane_layouts(nav_system):
    """Demonstrate multi-pane layouts"""
    print_section("MULTI-PANE LAYOUTS")

    print("Demonstrating different multi-pane layouts:")

    # Agent multi-pane
    print("\n1. Agent Management Multi-Pane:")
    nav_system.handle_input("2")
    nav_system.display_interface(80, 24)

    time.sleep(2)

    # Mission multi-pane
    print("\n2. Mission Operations Multi-Pane:")
    nav_system.handle_input("esc")  # Go back to main
    nav_system.handle_input("3")
    nav_system.display_interface(80, 24)

    time.sleep(2)

    # Intelligence multi-pane
    print("\n3. Intelligence Operations Multi-Pane:")
    nav_system.handle_input("esc")  # Go back to main
    nav_system.handle_input("4")
    nav_system.display_interface(80, 24)

    # Return to main
    nav_system.handle_input("esc")


def demonstrate_context_help(nav_system):
    """Demonstrate context-sensitive help"""
    print_section("CONTEXT-SENSITIVE HELP")

    print("Help in main menu:")
    result = nav_system.handle_input("?")
    print(result)

    time.sleep(1)

    print("\nHelp in agent management:")
    nav_system.handle_input("2")
    result = nav_system.handle_input("?")
    print(result)

    # Return to main
    nav_system.handle_input("esc")


def demonstrate_navigation_flow(nav_system):
    """Demonstrate complete navigation flow"""
    print_section("COMPLETE NAVIGATION FLOW")

    print("Demonstrating a complete navigation session:")
    print("(This simulates user interaction)")

    # Start in main menu
    print("\n📍 Starting in main menu...")
    nav_system.display_interface(80, 24)

    time.sleep(1)

    # Navigate to agents
    print("\n🎯 User presses '2' to enter Agent Management...")
    result = nav_system.handle_input("2")
    print(f"Result: {result}")
    nav_system.display_interface(80, 24)

    time.sleep(1)

    # Navigate within agents
    print("\n🎯 User presses '1' to view Agent List...")
    result = nav_system.handle_input("1")
    print(f"Result: {result}")

    time.sleep(1)

    # Use arrow keys
    print("\n🎯 User presses 'down' arrow to select next item...")
    result = nav_system.handle_input("down")
    print(f"Result: {result}")

    time.sleep(1)

    # Navigate to missions
    print("\n🎯 User presses 'esc' to go back, then '3' for missions...")
    nav_system.handle_input("esc")
    result = nav_system.handle_input("3")
    print(f"Result: {result}")
    nav_system.display_interface(80, 24)

    time.sleep(1)

    # Navigate to intelligence
    print("\n🎯 User presses 'esc' to go back, then '4' for intelligence...")
    nav_system.handle_input("esc")
    result = nav_system.handle_input("4")
    print(f"Result: {result}")
    nav_system.display_interface(80, 24)

    time.sleep(1)

    # Return to main
    print("\n🎯 User presses 'esc' to return to main menu...")
    nav_system.handle_input("esc")
    nav_system.display_interface(80, 24)


def demonstrate_navigation_summary(nav_system):
    """Demonstrate navigation system summary"""
    print_section("NAVIGATION SYSTEM SUMMARY")

    summary = nav_system.get_navigation_summary()

    print("Current Navigation State:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\nNavigation Features Demonstrated:")
    print("  ✅ Number key navigation (1-9)")
    print("  ✅ Arrow key navigation (↑/↓)")
    print("  ✅ Escape key functionality")
    print("  ✅ Multi-pane layouts")
    print("  ✅ Context-sensitive menus")
    print("  ✅ Breadcrumb navigation")
    print("  ✅ Context-sensitive help")


def main():
    """Main demonstration function"""
    print_header("ENHANCED NAVIGATION SYSTEM DEMO")

    print(
        "This demo showcases DF/Rimworld-style navigation improvements for Years of Lead."
    )
    print(
        "Features include number key navigation, escape functionality, and multi-pane layouts."
    )

    # Create demo game state
    game_state = create_demo_game_state()

    # Initialize enhanced navigation
    from game.enhanced_navigation import EnhancedNavigation

    nav_system = EnhancedNavigation(game_state)

    # Run demonstrations
    demonstrate_number_navigation(nav_system)
    demonstrate_escape_functionality(nav_system)
    demonstrate_multi_pane_layouts(nav_system)
    demonstrate_context_help(nav_system)
    demonstrate_navigation_flow(nav_system)
    demonstrate_navigation_summary(nav_system)

    print_header("DEMO COMPLETE")
    print("The enhanced navigation system provides:")
    print("• Familiar DF/Rimworld-style controls")
    print("• Efficient number key navigation")
    print("• Intuitive escape key functionality")
    print("• Information-rich multi-pane layouts")
    print("• Context-sensitive help and menus")
    print(
        "\nThis makes the interface much more accessible to fans of complex simulation games!"
    )


if __name__ == "__main__":
    main()
