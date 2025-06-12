#!/usr/bin/env python3
"""
Years of Lead - Betrayal Tree Visualization Tool

Visualizes betrayal plans, trigger conditions, cascading effects, and trust networks
for development and debugging purposes.
"""

import os
import sys
import json
from typing import Dict, List, Any
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from game.core import GameState


class BetrayalTreeVisualizer:
    """Visualizes betrayal plans, trust networks, and cascading effects"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.relationship_manager = getattr(game_state, "relationship_manager", None)

    def analyze_betrayal_network(self) -> Dict[str, Any]:
        """Analyze the current betrayal network and potential cascades"""
        analysis = {
            "active_betrayal_plans": [],
            "trust_vulnerabilities": [],
            "cascade_potential": {},
            "loyalty_distribution": {},
            "co_conspirator_networks": {},
        }

        # Collect betrayal plans
        for agent_id, agent in self.game_state.agents.items():
            if hasattr(agent, "planned_betrayal") and agent.planned_betrayal:
                plan_data = {
                    "betrayer": agent_id,
                    "betrayer_name": agent.name,
                    "target": agent.planned_betrayal.target_agent,
                    "trigger_conditions": agent.planned_betrayal.trigger_conditions,
                    "timing": agent.planned_betrayal.preferred_timing,
                    "co_conspirators": agent.planned_betrayal.potential_co_conspirators,
                    "confidence": agent.planned_betrayal.plan_confidence,
                }
                analysis["active_betrayal_plans"].append(plan_data)

        # Analyze trust vulnerabilities
        if hasattr(self.game_state, "get_all_relationships"):
            for relationship in self.game_state.get_all_relationships():
                if relationship.trust < 0.3:  # Low trust threshold
                    analysis["trust_vulnerabilities"].append(
                        {
                            "agent_a": relationship.agent_a,
                            "agent_b": relationship.agent_b,
                            "trust": relationship.trust,
                            "loyalty": relationship.loyalty,
                            "affinity": relationship.affinity,
                        }
                    )

        # Calculate cascade potential
        for plan in analysis["active_betrayal_plans"]:
            cascade_score = self._calculate_cascade_potential(plan)
            analysis["cascade_potential"][plan["betrayer"]] = cascade_score

        # Analyze loyalty distribution
        for agent_id, agent in self.game_state.agents.items():
            faction_loyalty = getattr(agent, "loyalty", 50) / 100.0
            analysis["loyalty_distribution"][agent_id] = {
                "name": agent.name,
                "faction": agent.faction_id,
                "loyalty": faction_loyalty,
            }

        return analysis

    def _calculate_cascade_potential(self, betrayal_plan: Dict[str, Any]) -> float:
        """Calculate the potential for a betrayal to trigger cascading effects"""
        betrayal_plan["betrayer"]
        target = betrayal_plan["target"]
        co_conspirators = betrayal_plan.get("co_conspirators", [])

        # Base cascade potential from co-conspirators
        cascade_score = len(co_conspirators) * 0.2

        # Add potential from target's relationships
        if hasattr(self.game_state, "get_agent_relationships"):
            target_relationships = self.game_state.get_agent_relationships(target)
            for rel_agent, relationship in target_relationships:
                if (
                    relationship.trust > 0.7
                ):  # High trust relationships are more vulnerable
                    cascade_score += 0.1

        # Factor in faction cohesion
        if hasattr(self.game_state, "get_faction_cohesion"):
            target_agent = self.game_state.agents.get(target)
            if target_agent:
                faction_cohesion = self.game_state.get_faction_cohesion(
                    target_agent.faction_id
                )
                cascade_score *= (
                    1.0 - faction_cohesion
                )  # Lower cohesion = higher cascade

        return min(cascade_score, 1.0)

    def visualize_betrayal_tree(self, output_path: str = "betrayal_tree.png"):
        """Create a tree visualization of betrayal plans and relationships"""
        analysis = self.analyze_betrayal_network()
        G = nx.DiGraph()

        # Add agent nodes
        for agent_id, agent in self.game_state.agents.items():
            loyalty = (
                analysis["loyalty_distribution"].get(agent_id, {}).get("loyalty", 0.5)
            )

            # Color based on loyalty
            if loyalty > 0.7:
                color = "lightgreen"
            elif loyalty > 0.4:
                color = "yellow"
            else:
                color = "lightcoral"

            G.add_node(
                agent_id,
                node_type="agent",
                color=color,
                label=agent.name,
                loyalty=loyalty,
            )

        # Add betrayal plan nodes and edges
        betrayal_count = 0
        for plan in analysis["active_betrayal_plans"]:
            betrayal_count += 1
            betrayal_node = f"betrayal_{betrayal_count}"

            # Color based on cascade potential
            cascade = analysis["cascade_potential"].get(plan["betrayer"], 0)
            if cascade > 0.6:
                betrayal_color = "darkred"
            elif cascade > 0.3:
                betrayal_color = "orange"
            else:
                betrayal_color = "pink"

            G.add_node(
                betrayal_node,
                node_type="betrayal",
                color=betrayal_color,
                label=f"Betrayal\n{plan['timing']}",
                confidence=plan["confidence"],
            )

            # Add edges
            G.add_edge(plan["betrayer"], betrayal_node, relation="plans")
            G.add_edge(betrayal_node, plan["target"], relation="targets")

            # Add co-conspirator edges
            for conspirator in plan["co_conspirators"]:
                if conspirator in self.game_state.agents:
                    G.add_edge(conspirator, betrayal_node, relation="supports")

        # Create visualization
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(G, k=3, iterations=50)

        # Draw nodes by type
        agent_nodes = [n for n in G.nodes() if G.nodes[n].get("node_type") == "agent"]
        betrayal_nodes = [
            n for n in G.nodes() if G.nodes[n].get("node_type") == "betrayal"
        ]

        # Draw agent nodes
        agent_colors = [G.nodes[n]["color"] for n in agent_nodes]
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=agent_nodes,
            node_color=agent_colors,
            node_size=1000,
            alpha=0.8,
        )

        # Draw betrayal nodes
        betrayal_colors = [G.nodes[n]["color"] for n in betrayal_nodes]
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=betrayal_nodes,
            node_color=betrayal_colors,
            node_size=600,
            node_shape="s",
            alpha=0.8,
        )

        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.6, arrows=True)

        # Add labels
        labels = {}
        for node in G.nodes():
            labels[node] = G.nodes[node].get("label", node)

        nx.draw_networkx_labels(G, pos, labels, font_size=8)

        plt.title("Years of Lead - Betrayal Network Analysis")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    def visualize_trust_heatmap(self, output_path: str = "trust_heatmap.png"):
        """Create a heatmap of trust relationships between agents"""
        agent_ids = list(self.game_state.agents.keys())
        agent_names = [self.game_state.agents[aid].name for aid in agent_ids]

        # Create trust matrix
        trust_matrix = []
        for i, agent_a in enumerate(agent_ids):
            row = []
            for j, agent_b in enumerate(agent_ids):
                if i == j:
                    row.append(1.0)  # Self-trust
                else:
                    # Get relationship trust
                    if hasattr(self.game_state, "get_relationship"):
                        rel = self.game_state.get_relationship(agent_a, agent_b)
                        if rel:
                            row.append(rel.trust)
                        else:
                            row.append(0.5)  # Neutral
                    else:
                        row.append(0.5)
            trust_matrix.append(row)

        # Create heatmap
        plt.figure(figsize=(12, 10))
        im = plt.imshow(trust_matrix, cmap="RdYlGn", vmin=0, vmax=1, alpha=0.8)

        # Add labels
        plt.xticks(range(len(agent_names)), agent_names, rotation=45, ha="right")
        plt.yticks(range(len(agent_names)), agent_names)

        # Add text annotations
        for i in range(len(agent_ids)):
            for j in range(len(agent_ids)):
                plt.text(
                    j,
                    i,
                    f"{trust_matrix[i][j]:.2f}",
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                )

        plt.colorbar(im, label="Trust Level")
        plt.title("Agent Trust Heatmap")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    def export_betrayal_analysis(self, output_path: str = "betrayal_analysis.json"):
        """Export detailed betrayal analysis to JSON"""
        analysis = self.analyze_betrayal_network()

        # Add timestamps and metadata
        analysis["analysis_timestamp"] = datetime.now().isoformat()
        analysis["turn_number"] = self.game_state.turn_number
        analysis["total_agents"] = len(self.game_state.agents)

        # Calculate summary statistics
        analysis["summary"] = {
            "total_betrayal_plans": len(analysis["active_betrayal_plans"]),
            "total_trust_vulnerabilities": len(analysis["trust_vulnerabilities"]),
            "average_loyalty": sum(
                a["loyalty"] for a in analysis["loyalty_distribution"].values()
            )
            / len(analysis["loyalty_distribution"])
            if analysis["loyalty_distribution"]
            else 0,
            "high_cascade_risk_count": sum(
                1 for score in analysis["cascade_potential"].values() if score > 0.6
            ),
            "network_stability": 1.0
            - (
                len(analysis["trust_vulnerabilities"])
                / (len(self.game_state.agents) * (len(self.game_state.agents) - 1) / 2)
            )
            if len(self.game_state.agents) > 1
            else 1.0,
        }

        with open(output_path, "w") as f:
            json.dump(analysis, f, indent=2)

        return analysis

    def predict_betrayal_cascade(self, initial_betrayer: str) -> List[Dict[str, Any]]:
        """Predict the potential cascade effects of a betrayal"""
        cascade_events = []

        if initial_betrayer not in self.game_state.agents:
            return cascade_events

        # Start with initial betrayal
        initial_agent = self.game_state.agents[initial_betrayer]
        if (
            hasattr(initial_agent, "planned_betrayal")
            and initial_agent.planned_betrayal
        ):
            target = initial_agent.planned_betrayal.target_agent

            cascade_events.append(
                {
                    "event_type": "initial_betrayal",
                    "betrayer": initial_betrayer,
                    "target": target,
                    "turn": self.game_state.turn_number,
                    "probability": initial_agent.planned_betrayal.plan_confidence,
                }
            )

            # Predict secondary betrayals
            secondary_betrayers = self._find_secondary_betrayers(
                initial_betrayer, target
            )
            for secondary in secondary_betrayers:
                cascade_events.append(
                    {
                        "event_type": "secondary_betrayal",
                        "betrayer": secondary["agent"],
                        "target": secondary["target"],
                        "turn": self.game_state.turn_number + secondary["delay"],
                        "probability": secondary["probability"],
                        "trigger": f"Response to {initial_betrayer}'s betrayal",
                    }
                )

        return cascade_events

    def _find_secondary_betrayers(
        self, initial_betrayer: str, initial_target: str
    ) -> List[Dict[str, Any]]:
        """Find agents likely to betray in response to an initial betrayal"""
        secondary_betrayers = []

        for agent_id, agent in self.game_state.agents.items():
            if agent_id == initial_betrayer or agent_id == initial_target:
                continue

            # Check if agent has relationship with either betrayer or target
            betrayer_relationship = None
            target_relationship = None

            if hasattr(self.game_state, "get_relationship"):
                betrayer_relationship = self.game_state.get_relationship(
                    agent_id, initial_betrayer
                )
                target_relationship = self.game_state.get_relationship(
                    agent_id, initial_target
                )

            # Calculate betrayal probability based on relationships
            betrayal_probability = 0.0
            potential_target = None
            delay = 1

            # If agent trusts the target more than the betrayer, might betray the betrayer
            if (
                target_relationship
                and betrayer_relationship
                and target_relationship.trust > betrayer_relationship.trust + 0.3
            ):
                betrayal_probability = (
                    target_relationship.trust - betrayer_relationship.trust
                ) * 0.5
                potential_target = initial_betrayer
                delay = 1

            # If agent has low loyalty, might betray their faction
            faction_loyalty = getattr(agent, "loyalty", 50) / 100.0
            if faction_loyalty < 0.3:
                betrayal_probability = max(betrayal_probability, 1.0 - faction_loyalty)
                if not potential_target:
                    # Find highest trust agent in same faction to betray
                    same_faction_agents = [
                        a
                        for a in self.game_state.agents.values()
                        if a.faction_id == agent.faction_id and a.id != agent_id
                    ]
                    if same_faction_agents:
                        potential_target = same_faction_agents[0].id
                        delay = 2

            if betrayal_probability > 0.2 and potential_target:
                secondary_betrayers.append(
                    {
                        "agent": agent_id,
                        "target": potential_target,
                        "probability": betrayal_probability,
                        "delay": delay,
                    }
                )

        return sorted(
            secondary_betrayers, key=lambda x: x["probability"], reverse=True
        )[:3]


def simulate_tick():
    """Simulate a single game tick for testing"""
    game_state = GameState()
    game_state.initialize_game()

    # Advance one turn to generate some data
    if hasattr(game_state, "advance_turn"):
        game_state.advance_turn()

    return game_state


if __name__ == "__main__":
    # Create test game state
    game_state = simulate_tick()

    # Create visualizer
    visualizer = BetrayalTreeVisualizer(game_state)

    # Generate visualizations
    print("Analyzing betrayal network...")
    analysis = visualizer.analyze_betrayal_network()
    print(f"Found {len(analysis['active_betrayal_plans'])} active betrayal plans")
    print(f"Found {len(analysis['trust_vulnerabilities'])} trust vulnerabilities")

    print("Creating betrayal tree visualization...")
    tree_path = visualizer.visualize_betrayal_tree()
    print(f"Saved betrayal tree to: {tree_path}")

    print("Creating trust heatmap...")
    heatmap_path = visualizer.visualize_trust_heatmap()
    print(f"Saved trust heatmap to: {heatmap_path}")

    print("Exporting betrayal analysis...")
    analysis_data = visualizer.export_betrayal_analysis()
    print(f"Network stability: {analysis_data['summary']['network_stability']:.2f}")

    # Test cascade prediction
    if analysis["active_betrayal_plans"]:
        first_betrayer = analysis["active_betrayal_plans"][0]["betrayer"]
        print(f"Predicting cascade for betrayer: {first_betrayer}")
        cascade = visualizer.predict_betrayal_cascade(first_betrayer)
        for event in cascade:
            print(
                f"  {event['event_type']}: {event['betrayer']} -> {event['target']} (p={event['probability']:.2f})"
            )
    else:
        print("No active betrayal plans to analyze")
