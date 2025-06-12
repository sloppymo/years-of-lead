"""
Years of Lead - Enhanced Main GUI

Enhanced GUI that showcases all the sophisticated simulation systems:
- Mission execution with emotional integration
- Agent AI decision-making
- Intelligence analysis
- Political simulation
- Relationship dynamics
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from game.core import GameState
from game.agent_decision_system import integrate_agent_decisions
from game.mission_execution_engine import MissionExecutionEngine
from game.reputation_system import ReputationSystem


class EnhancedYearsOfLeadGUI:
    """Enhanced GUI showcasing all simulation systems"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Years of Lead - Complete Simulation")
        self.root.geometry("1200x800")

        # Initialize all systems
        self.game_state = GameState()
        self.game_state.initialize_game()

        self.decision_system = integrate_agent_decisions(self.game_state)
        self.mission_engine = MissionExecutionEngine(self.game_state)
        self.reputation_system = ReputationSystem()

        # Setup UI
        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Setup the enhanced UI"""

        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Simulation Overview
        overview_frame = ttk.Frame(notebook)
        notebook.add(overview_frame, text="Simulation Overview")

        # Title
        title_label = tk.Label(
            overview_frame,
            text="Years of Lead - Complete Simulation",
            font=("Arial", 16, "bold"),
        )
        title_label.pack(pady=10)

        # Status display
        self.status_text = tk.Text(overview_frame, height=30, width=80)
        self.status_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Control buttons
        button_frame = tk.Frame(overview_frame)
        button_frame.pack(pady=10)

        advance_btn = tk.Button(
            button_frame,
            text="Advance Turn",
            command=self.advance_turn,
            bg="#4CAF50",
            fg="white",
        )
        advance_btn.pack(side="left", padx=5)

        auto_btn = tk.Button(
            button_frame,
            text="Auto Play (5 turns)",
            command=self.auto_play,
            bg="#2196F3",
            fg="white",
        )
        auto_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(
            button_frame,
            text="Reset Simulation",
            command=self.reset_simulation,
            bg="#FF5722",
            fg="white",
        )
        reset_btn.pack(side="left", padx=5)

        # Tab 2: Agent Details
        agents_frame = ttk.Frame(notebook)
        notebook.add(agents_frame, text="Agent Status")

        self.agents_text = tk.Text(agents_frame, height=30, width=80)
        self.agents_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 3: Intelligence & Politics
        intel_frame = ttk.Frame(notebook)
        notebook.add(intel_frame, text="Intelligence & Politics")

        self.intel_text = tk.Text(intel_frame, height=30, width=80)
        self.intel_text.pack(fill="both", expand=True, padx=10, pady=10)

    def update_display(self):
        """Update all displays"""
        self.update_overview()
        self.update_agents()
        self.update_intelligence()

        # Schedule next update
        self.root.after(1000, self.update_display)

    def update_overview(self):
        """Update the overview display"""
        self.status_text.delete(1.0, tk.END)

        # Game status
        status = f"""🎮 YEARS OF LEAD SIMULATION STATUS
{'='*50}

📊 Current Turn: {getattr(self.game_state, 'turn_number', 1)}
📍 Phase: {getattr(self.game_state, 'current_phase', 'Unknown').value if hasattr(getattr(self.game_state, 'current_phase', None), 'value') else 'Unknown'}

👥 AGENTS: {len(self.game_state.agents)}
"""

        # Agent summary
        active_agents = sum(
            1 for a in self.game_state.agents.values() if a.status == "active"
        )
        high_trauma = sum(
            1
            for a in self.game_state.agents.values()
            if hasattr(a, "emotional_state") and a.emotional_state.trauma_level > 0.5
        )

        status += f"   Active: {active_agents}\n"
        status += f"   High Trauma: {high_trauma}\n\n"

        # Faction summary
        status += f"🏴 FACTIONS: {len(self.game_state.factions)}\n"
        for faction_id, faction in self.game_state.factions.items():
            resources = getattr(faction, "resources", {})
            money = resources.get("money", 0)
            personnel = resources.get("personnel", 0)
            status += f"   {faction.name}: ${money}, {personnel} personnel\n"

        # Recent events
        status += "\n📖 RECENT EVENTS:\n"
        for event in self.game_state.recent_narrative[-5:]:
            status += f"   • {event}\n"

        self.status_text.insert(tk.END, status)

    def update_agents(self):
        """Update agent details"""
        self.agents_text.delete(1.0, tk.END)

        agents_info = "👥 AGENT DETAILED STATUS\n"
        agents_info += "=" * 50 + "\n\n"

        for agent_id, agent in self.game_state.agents.items():
            agents_info += f"🔸 {agent.name} ({agent.status})\n"
            agents_info += f"   Faction: {agent.faction_id}\n"
            agents_info += f"   Location: {agent.location_id}\n"

            # Emotional state
            emotional_state = getattr(agent, "emotional_state", None)
            if emotional_state:
                dominant, intensity = emotional_state.get_dominant_emotion()
                stability = emotional_state.get_emotional_stability()
                agents_info += f"   Emotion: {dominant} ({intensity:.2f})\n"
                agents_info += f"   Stability: {stability:.2f}\n"
                agents_info += f"   Trauma: {emotional_state.trauma_level:.2f}\n"

            # Relationships
            relationships = getattr(agent, "relationships", {})
            if relationships:
                agents_info += f"   Relationships: {len(relationships)}\n"
                strong_allies = sum(
                    1
                    for rel in relationships.values()
                    if hasattr(rel, "affinity") and rel.affinity > 60
                )
                agents_info += f"   Strong Allies: {strong_allies}\n"

            agents_info += "\n"

        self.agents_text.insert(tk.END, agents_info)

    def update_intelligence(self):
        """Update intelligence and political info"""
        self.intel_text.delete(1.0, tk.END)

        intel_info = "📊 INTELLIGENCE & POLITICAL STATUS\n"
        intel_info += "=" * 50 + "\n\n"

        # Political state
        intel_info += "🏛️ GOVERNMENT RESPONSE:\n"
        intel_info += "   Response Mode: Active Monitoring\n"
        intel_info += "   Heat Level: Medium\n"
        intel_info += "   Crackdown Risk: Low\n\n"

        # Reputation summary
        intel_info += "📰 MEDIA & REPUTATION:\n"
        if self.game_state.agents:
            sample_agent = list(self.game_state.agents.values())[0]
            reputation = self.reputation_system.get_or_create_reputation(
                sample_agent.id
            )
            intel_info += f"   Public Attention: {reputation.notoriety_score:.2f}\n"
            intel_info += (
                f"   Political Pressure: {reputation.get_political_pressure():.2f}\n"
            )

        # Location security
        intel_info += "\n🗺️ LOCATION SECURITY:\n"
        for location_id, location in self.game_state.locations.items():
            intel_info += f"   {location.name}: Security {location.security_level}/10\n"

        self.intel_text.insert(tk.END, intel_info)

    def advance_turn(self):
        """Advance one turn"""
        # Process agent decisions
        for agent_id, agent in self.game_state.agents.items():
            if agent.status == "active":
                decision = self.decision_system.make_agent_decision(agent_id)
                if decision:
                    result = self.decision_system.execute_decision(agent_id, decision)
                    if result.get("success") and result.get("narrative"):
                        self.game_state.recent_narrative.append(result["narrative"])

        # Advance game state
        self.game_state.advance_turn()

        # Add turn event
        turn_num = getattr(self.game_state, "turn_number", 1)
        self.game_state.recent_narrative.append(f"🔄 Turn {turn_num} completed")

    def auto_play(self):
        """Auto-play 5 turns"""
        for _ in range(5):
            self.advance_turn()

        self.game_state.recent_narrative.append("🎮 Auto-play completed (5 turns)")

    def reset_simulation(self):
        """Reset the simulation"""
        self.game_state = GameState()
        self.game_state.initialize_game()
        self.decision_system = integrate_agent_decisions(self.game_state)
        self.reputation_system = ReputationSystem()

        self.game_state.recent_narrative.append("🔄 Simulation reset")

    def run(self):
        """Run the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    print("🎮 Launching Enhanced Years of Lead GUI...")
    app = EnhancedYearsOfLeadGUI()
    app.run()


if __name__ == "__main__":
    main()
