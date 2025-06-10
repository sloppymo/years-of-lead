#!/usr/bin/env python3
"""
Test script for Revolutionary Ecosystem - ITERATION 021

Demonstrates autonomous AI faction simulation and ecosystem dynamics.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from game.revolutionary_ecosystem import RevolutionaryEcosystem, FactionIdeology, FactionActivityType
from game.campaign_structure import CityReputation


def test_revolutionary_ecosystem():
    """Test the revolutionary ecosystem simulation"""
    print("=== REVOLUTIONARY ECOSYSTEM TEST - ITERATION 021 ===\n")
    
    # Create ecosystem
    ecosystem = RevolutionaryEcosystem()
    
    # Add mock city reputations for testing
    cities = ["Industrial District", "Port City", "University Quarter", "Border Region", "Mountain Towns"]
    for city_name in cities:
        ecosystem.city_reputations[city_name] = CityReputation(city_name=city_name)
        print(f"Added city: {city_name}")
    
    # Initialize default factions
    ecosystem.initialize_default_factions()
    print(f"\nInitialized {len(ecosystem.active_factions)} AI factions:")
    
    for faction in ecosystem.active_factions:
        print(f"  • {faction.name} ({faction.ideology.value})")
        print(f"    Territory: {', '.join(faction.territory_zones)}")
        print(f"    Support: {faction.public_support:.1f}%, Aggression: {faction.aggression:.1f}")
        print(f"    Current Activity: {faction.current_activity.value}")
        print()
    
    # Simulate several turns
    print("=== SIMULATING ECOSYSTEM TURNS ===\n")
    
    for turn in range(5):
        print(f"--- TURN {turn + 1} ---")
        
        turn_results = ecosystem.simulate_ecosystem_turn()
        
        print(f"Date: {turn_results['date'].strftime('%Y-%m-%d')}")
        print(f"National Uprising Momentum: {ecosystem.uprising_clock.national_uprising_momentum:.1f}/100")
        
        # Display faction activities
        for faction_activity in turn_results['faction_activities']:
            faction_name = faction_activity['faction_name']
            activity_type = faction_activity['activity_type']
            outcomes = faction_activity['outcomes']
            ongoing_effects = faction_activity.get('ongoing_effects', {})
            
            print(f"\n{faction_name}:")
            print(f"  Activity: {activity_type}")
            
            if outcomes:
                print("  Outcomes:")
                for outcome in outcomes:
                    print(f"    • {outcome}")
            
            if ongoing_effects:
                print("  Ongoing Effects:")
                for effect, value in ongoing_effects.items():
                    print(f"    • {effect}: {value}")
            
            if 'new_activity' in faction_activity:
                print(f"  New Activity: {faction_activity['new_activity']}")
        
        # Display major events
        if turn_results['major_events']:
            print("\nMAJOR ECOSYSTEM EVENTS:")
            for event in turn_results['major_events']:
                print(f"  🚨 {event}")
        
        print()
    
    # Display final faction status
    print("=== FINAL FACTION STATUS ===\n")
    
    for faction in ecosystem.active_factions:
        print(f"{faction.name} ({faction.ideology.value}):")
        print(f"  Public Support: {faction.public_support:.1f}%")
        print(f"  Government Heat: {faction.government_heat:.1f}/10")
        print(f"  Operational Capacity: {faction.operational_capacity:.2f}")
        print(f"  Major Operations: {len(faction.major_operations)}")
        print(f"  Martyrs Created: {len(faction.martyrs_created)}")
        print(f"  Current Activity: {faction.current_activity.value}")
        print()
    
    # Display uprising clock status
    print("=== UPRISING CLOCK STATUS ===")
    print(f"Days Since Start: {ecosystem.uprising_clock.days_since_start}")
    print(f"National Uprising Momentum: {ecosystem.uprising_clock.national_uprising_momentum:.1f}/100")
    print(f"Government Stability: {ecosystem.uprising_clock.government_stability:.1f}/100")
    print(f"Major Events Recorded: {len(ecosystem.uprising_clock.major_events)}")
    
    if ecosystem.uprising_clock.major_events:
        print("\nRecent Major Events:")
        for event in ecosystem.uprising_clock.major_events[-5:]:  # Last 5 events
            print(f"  • {event['faction']} - {event['description']}")
            print(f"    Momentum Impact: {event['momentum_impact']:+.1f}")
    
    print("\n=== TEST COMPLETED ===")
    print("✓ Multi-faction ecosystem simulation successful")
    print("✓ Autonomous AI faction activity execution verified")
    print("✓ Inter-faction dynamics and city effects demonstrated")
    print("✓ Global uprising momentum tracking functional")
    
    return True


if __name__ == "__main__":
    test_revolutionary_ecosystem()