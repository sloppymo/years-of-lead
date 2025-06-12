#!/usr/bin/env python3
"""
Demonstration script for the Dynamic Relationships and Social Network System

This script shows how the relationship system works in Years of Lead,
including relationship creation, updates, narrative generation, and social network analysis.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from game.core import GameState
from game.relationships import EventType
from game.narrative_engine import NarrativeEngine


def demonstrate_relationship_system():
    """Demonstrate the relationship system functionality"""

    print("🎭 YEARS OF LEAD - Dynamic Relationships & Social Networks")
    print("=" * 60)

    # Initialize game state
    print("\n1. Initializing game state...")
    game_state = GameState()
    game_state.initialize_game()

    print(f"   - Created {len(game_state.agents)} agents")
    print(f"   - Created {len(game_state.factions)} factions")
    print(f"   - Created {len(game_state.locations)} locations")

    # Show initial relationships
    print("\n2. Initial relationships:")
    for agent_id, agent in game_state.agents.items():
        print(
            f"   {agent.name} ({agent.background}) - {len(agent.relationships)} relationships"
        )
        for other_id, rel in agent.relationships.items():
            other_agent = game_state.agents[other_id]
            print(
                f"     -> {other_agent.name}: {rel.bond_type.value} (affinity: {rel.affinity:.1f}, trust: {rel.trust:.2f})"
            )

    # Show social tags
    print("\n3. Agent social tags:")
    for agent_id, agent in game_state.agents.items():
        print(f"   {agent.name}: {', '.join(sorted(agent.social_tags))}")

    # Demonstrate relationship updates
    print("\n4. Demonstrating relationship events:")

    # Get two agents
    maria = game_state.agents["agent_maria"]
    sofia = game_state.agents["agent_sofia"]

    print(f"   {maria.name} and {sofia.name} start with a strong ally relationship")

    # Apply some events
    events_to_demonstrate = [
        (EventType.SHARED_RISK, "They face danger together"),
        (EventType.COOPERATION, "They work together successfully"),
        (EventType.CONFLICT, "They have a disagreement over strategy"),
    ]

    for event_type, description in events_to_demonstrate:
        print(f"\n   Event: {description}")

        # Get current relationship
        rel = game_state.social_network.get_relationship(maria.id, sofia.id)
        print(
            f"   Before: affinity={rel.affinity:.1f}, trust={rel.trust:.2f}, loyalty={rel.loyalty:.2f}"
        )

        # Apply event
        game_state.update_relationship(maria.id, sofia.id, event_type=event_type)

        # Get updated relationship
        rel = game_state.social_network.get_relationship(maria.id, sofia.id)
        print(
            f"   After:  affinity={rel.affinity:.1f}, trust={rel.trust:.2f}, loyalty={rel.loyalty:.2f}"
        )

    # Demonstrate narrative generation
    print("\n5. Narrative generation:")
    narrative_engine = NarrativeEngine(game_state)

    # Generate some narratives
    for i in range(3):
        narrative = narrative_engine.apply_relationship_effects(
            maria, sofia, {"type": "cooperation", "context": f"mission_{i}"}
        )
        print(f"   {narrative}")

    # Demonstrate social network analysis
    print("\n6. Social network analysis:")

    # Get social circles
    maria_circle = game_state.get_social_circle("agent_maria")
    print(f"   {maria.name}'s social circle ({len(maria_circle)} connections):")
    for agent_id, rel in maria_circle:
        other_agent = game_state.agents[agent_id]
        print(
            f"     - {other_agent.name}: {rel.bond_type.value} (strength: {rel.get_strength():.2f})"
        )

    # Get influential agents
    influential = game_state.get_most_influential("agent_maria", radius=2)
    print(f"\n   Most influential agents near {maria.name}:")
    for agent_id, influence in influential[:3]:  # Top 3
        other_agent = game_state.agents[agent_id]
        print(f"     - {other_agent.name}: influence {influence:.2f}")

    # Get social clusters
    clusters = game_state.get_social_clusters()
    print(f"\n   Social clusters ({len(clusters)} clusters):")
    for cluster_id, cluster in clusters.items():
        agent_names = [game_state.agents[agent_id].name for agent_id in cluster]
        print(f"     - {cluster_id}: {', '.join(agent_names)}")

    # Demonstrate faction cohesion
    print("\n7. Faction cohesion:")
    for faction_id, faction in game_state.factions.items():
        cohesion = game_state.get_faction_cohesion(faction_id)
        print(f"   {faction.name}: cohesion {cohesion:.2f}")

    # Demonstrate relationship decay
    print("\n8. Relationship decay over time:")
    rel = game_state.social_network.get_relationship(maria.id, sofia.id)
    print(f"   {maria.name} and {sofia.name} relationship before decay:")
    print(
        f"     affinity={rel.affinity:.1f}, trust={rel.trust:.2f}, loyalty={rel.loyalty:.2f}"
    )

    # Apply decay
    game_state.social_network.decay_all_relationships()

    rel = game_state.social_network.get_relationship(maria.id, sofia.id)
    print("   After decay:")
    print(
        f"     affinity={rel.affinity:.1f}, trust={rel.trust:.2f}, loyalty={rel.loyalty:.2f}"
    )

    # Demonstrate game turn with relationships
    print("\n9. Game turn with relationship events:")
    print("   Advancing game turn...")

    initial_narrative_length = len(game_state.recent_narrative)
    game_state.advance_turn()

    print(
        f"   Generated {len(game_state.recent_narrative) - initial_narrative_length} new narrative events:"
    )
    for narrative in game_state.recent_narrative[-3:]:  # Last 3 events
        print(f"     - {narrative}")

    # Show template statistics
    print("\n10. Narrative template statistics:")
    stats = narrative_engine.get_template_statistics()
    print(f"   Total templates: {stats['total_templates']}")
    print("   Templates by emotional tone:")
    for tone, count in stats["templates_by_emotional_tone"].items():
        print(f"     - {tone}: {count}")

    print("\n✅ Relationship system demonstration complete!")
    print("\nKey features demonstrated:")
    print("  • Dynamic relationship creation and management")
    print("  • Event-driven relationship updates")
    print("  • Social network analysis and clustering")
    print("  • Narrative generation with relationship context")
    print("  • Faction cohesion calculation")
    print("  • Relationship decay over time")
    print("  • SYLVA/WREN integration ready")


if __name__ == "__main__":
    demonstrate_relationship_system()
