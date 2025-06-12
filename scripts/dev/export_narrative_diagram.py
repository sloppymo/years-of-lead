#!/usr/bin/env python3
"""
Years of Lead - Narrative Diagram Export Tool

Exports visual diagrams of narrative flows, symbolic elements, and story branching
for development and analysis purposes.
"""

import os
import sys
import json
from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from game.core import GameState


class NarrativeDiagramExporter:
    """Exports narrative flow diagrams and symbolic element visualizations"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.narrative_engine = (
            game_state.narrative_engine
            if hasattr(game_state, "narrative_engine")
            else None
        )
        self.relationship_manager = (
            game_state.relationship_manager
            if hasattr(game_state, "relationship_manager")
            else None
        )

    def export_narrative_flow_diagram(self, output_path: str = "narrative_flow.png"):
        """Export a diagram showing narrative flow and template usage"""
        G = nx.DiGraph()

        # Add nodes for narrative templates and categories
        template_categories = {
            "relationship_events": "lightblue",
            "secret_revelation": "lightcoral",
            "betrayal_narratives": "darkred",
            "memory_formation": "lightgreen",
            "ideological_conflict": "orange",
            "emotional_bonding": "pink",
            "trust_building": "lightgray",
            "faction_dynamics": "purple",
        }

        for category, color in template_categories.items():
            G.add_node(category, node_type="category", color=color)

        # Add agent nodes
        for agent_id, agent in self.game_state.agents.items():
            G.add_node(
                f"agent_{agent_id}", node_type="agent", color="gold", label=agent.name
            )

        # Add memory nodes for each agent
        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "memory_journal") and agent.memory_journal:
                for memory in agent.memory_journal:
                    memory_node = f"memory_{memory.id}"
                    G.add_node(
                        memory_node,
                        node_type="memory",
                        color="lightgreen",
                        label=f"Memory: {memory.emotional_tone}",
                    )
                    G.add_edge(f"agent_{agent_id}", memory_node, relation="remembers")

        # Add secret nodes
        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "secrets") and agent.secrets:
                for secret in agent.secrets:
                    secret_node = f"secret_{secret.id}"
                    G.add_node(
                        secret_node,
                        node_type="secret",
                        color="red",
                        label=f"Secret: {secret.secret_type.value}",
                    )
                    G.add_edge(f"agent_{agent_id}", secret_node, relation="holds")

                    # Add edges to agents who know the secret
                    for knower_id in secret.known_by:
                        if knower_id in self.game_state.agents:
                            G.add_edge(
                                f"agent_{knower_id}", secret_node, relation="knows"
                            )

        # Create visualization
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(G, k=3, iterations=50)

        # Draw nodes by type
        node_colors = []
        node_sizes = []
        for node in G.nodes():
            node_data = G.nodes[node]
            node_colors.append(node_data.get("color", "gray"))
            if node_data.get("node_type") == "agent":
                node_sizes.append(1000)
            elif node_data.get("node_type") == "category":
                node_sizes.append(1500)
            else:
                node_sizes.append(500)

        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8
        )
        nx.draw_networkx_edges(G, pos, alpha=0.6, arrows=True)

        # Add labels
        labels = {}
        for node in G.nodes():
            node_data = G.nodes[node]
            if "label" in node_data:
                labels[node] = node_data["label"]
            else:
                labels[node] = node.replace("_", "\n")

        nx.draw_networkx_labels(G, pos, labels, font_size=8)

        # Create legend
        legend_elements = [
            mpatches.Patch(color="gold", label="Agents"),
            mpatches.Patch(color="lightgreen", label="Memories"),
            mpatches.Patch(color="red", label="Secrets"),
            mpatches.Patch(color="lightblue", label="Narrative Categories"),
        ]
        plt.legend(handles=legend_elements, loc="upper right")

        plt.title("Years of Lead - Narrative Flow Diagram")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    def export_symbolic_element_map(self, output_path: str = "symbolic_elements.png"):
        """Export a map of symbolic elements and their connections"""
        G = nx.Graph()

        # Collect symbolic elements from memories
        symbolic_elements = set()
        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "memory_journal") and agent.memory_journal:
                for memory in agent.memory_journal:
                    if hasattr(memory, "symbolic_elements"):
                        symbolic_elements.update(memory.symbolic_elements)

        # Add symbolic elements as nodes
        for element in symbolic_elements:
            G.add_node(element, node_type="symbol", color="yellow")

        # Add ideology nodes
        ideology_types = [
            "radical",
            "pacifist",
            "individualist",
            "traditional",
            "nationalist",
            "materialist",
        ]
        for ideology in ideology_types:
            G.add_node(f"ideology_{ideology}", node_type="ideology", color="lightblue")

        # Add emotion nodes
        emotion_types = [
            "hope",
            "fear",
            "anger",
            "despair",
            "joy",
            "trust",
            "surprise",
            "sadness",
        ]
        for emotion in emotion_types:
            G.add_node(f"emotion_{emotion}", node_type="emotion", color="pink")

        # Connect agents to their ideologies and emotions
        for agent_id, agent in self.game_state.agents.items():
            agent_node = f"agent_{agent.name}"
            G.add_node(agent_node, node_type="agent", color="gold")

            # Connect to ideologies
            if hasattr(agent, "ideology_vector"):
                for ideology, value in agent.ideology_vector.items():
                    if value > 0.6:  # Strong ideology
                        G.add_edge(agent_node, f"ideology_{ideology}", weight=value)

            # Connect to emotions
            if hasattr(agent, "emotion_state"):
                for emotion, value in agent.emotion_state.items():
                    if value > 0.4:  # Strong emotion
                        G.add_edge(agent_node, f"emotion_{emotion}", weight=value)

        # Create visualization
        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(G, k=2, iterations=50)

        # Draw nodes by type
        node_colors = [G.nodes[node].get("color", "gray") for node in G.nodes()]
        node_sizes = [
            800 if G.nodes[node].get("node_type") == "agent" else 400
            for node in G.nodes()
        ]

        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8
        )
        nx.draw_networkx_edges(G, pos, alpha=0.4)
        nx.draw_networkx_labels(G, pos, font_size=8)

        # Create legend
        legend_elements = [
            mpatches.Patch(color="gold", label="Agents"),
            mpatches.Patch(color="yellow", label="Symbolic Elements"),
            mpatches.Patch(color="lightblue", label="Ideologies"),
            mpatches.Patch(color="pink", label="Emotions"),
        ]
        plt.legend(handles=legend_elements, loc="upper right")

        plt.title("Years of Lead - Symbolic Element Map")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    def export_narrative_analytics(self, output_path: str = "narrative_analytics.json"):
        """Export detailed narrative analytics"""
        analytics = {
            "turn_number": self.game_state.turn_number,
            "total_agents": len(self.game_state.agents),
            "total_factions": len(self.game_state.factions),
            "narrative_metrics": {},
            "symbolic_analysis": {},
            "relationship_patterns": {},
        }

        # Analyze memories
        total_memories = 0
        memory_tones = {}
        symbolic_frequency = {}

        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "memory_journal") and agent.memory_journal:
                total_memories += len(agent.memory_journal)
                for memory in agent.memory_journal:
                    tone = memory.emotional_tone
                    memory_tones[tone] = memory_tones.get(tone, 0) + 1

                    if hasattr(memory, "symbolic_elements"):
                        for element in memory.symbolic_elements:
                            symbolic_frequency[element] = (
                                symbolic_frequency.get(element, 0) + 1
                            )

        analytics["narrative_metrics"] = {
            "total_memories": total_memories,
            "memory_emotional_tones": memory_tones,
            "average_memories_per_agent": total_memories / len(self.game_state.agents)
            if self.game_state.agents
            else 0,
        }

        analytics["symbolic_analysis"] = {
            "symbolic_element_frequency": symbolic_frequency,
            "most_common_symbols": sorted(
                symbolic_frequency.items(), key=lambda x: x[1], reverse=True
            )[:5],
        }

        # Analyze relationships
        total_secrets = 0
        secret_types = {}
        betrayal_plans = 0

        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "secrets") and agent.secrets:
                total_secrets += len(agent.secrets)
                for secret in agent.secrets:
                    secret_type = secret.secret_type.value
                    secret_types[secret_type] = secret_types.get(secret_type, 0) + 1

            if hasattr(agent, "planned_betrayal") and agent.planned_betrayal:
                betrayal_plans += 1

        analytics["relationship_patterns"] = {
            "total_secrets": total_secrets,
            "secret_type_distribution": secret_types,
            "active_betrayal_plans": betrayal_plans,
        }

        # Export to file
        with open(output_path, "w") as f:
            json.dump(analytics, f, indent=2)

        return analytics


def simulate_tick():
    """Simulate a single game tick for testing"""
    game_state = GameState()
    game_state.initialize_game()

    # Advance one turn to generate some data
    if hasattr(game_state, "advance_turn"):
        game_state.advance_turn()

    return game_state


def visualize_symbol(symbol: str, game_state: Optional[GameState] = None):
    """Visualize a specific symbolic element and its connections"""
    if game_state is None:
        game_state = simulate_tick()

    NarrativeDiagramExporter(game_state)

    # Create symbol-specific visualization
    G = nx.Graph()
    symbol_node = f"symbol_{symbol}"
    G.add_node(symbol_node, node_type="symbol", color="yellow")

    # Find agents connected to this symbol
    connected_agents = []
    for agent_id, agent in game_state.agents.items():
        if hasattr(agent, "memory_journal") and agent.memory_journal:
            for memory in agent.memory_journal:
                if (
                    hasattr(memory, "symbolic_elements")
                    and symbol in memory.symbolic_elements
                ):
                    agent_node = f"agent_{agent.name}"
                    G.add_node(agent_node, node_type="agent", color="gold")
                    G.add_edge(symbol_node, agent_node)
                    connected_agents.append(agent.name)

    if G.number_of_nodes() > 1:
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)

        node_colors = [G.nodes[node].get("color", "gray") for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.8)
        nx.draw_networkx_edges(G, pos, alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_size=10)

        plt.title(f"Symbol '{symbol}' Connections")
        plt.axis("off")
        plt.tight_layout()

        output_path = f"symbol_{symbol}_connections.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path, connected_agents
    else:
        return None, []


if __name__ == "__main__":
    # Create test game state
    game_state = simulate_tick()

    # Create exporter
    exporter = NarrativeDiagramExporter(game_state)

    # Export diagrams
    print("Exporting narrative flow diagram...")
    flow_path = exporter.export_narrative_flow_diagram()
    print(f"Saved to: {flow_path}")

    print("Exporting symbolic element map...")
    symbol_path = exporter.export_symbolic_element_map()
    print(f"Saved to: {symbol_path}")

    print("Exporting narrative analytics...")
    analytics = exporter.export_narrative_analytics()
    print(
        f"Analytics exported with {analytics['narrative_metrics']['total_memories']} total memories"
    )

    # Test symbol visualization
    print("Testing symbol visualization...")
    test_symbols = ["betrayal", "loyalty", "fear", "hope"]
    for symbol in test_symbols:
        path, agents = visualize_symbol(symbol, game_state)
        if path:
            print(f"Symbol '{symbol}' connects to agents: {agents}")
        else:
            print(f"Symbol '{symbol}' has no connections")
