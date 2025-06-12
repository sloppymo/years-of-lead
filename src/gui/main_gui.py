"""
Main GUI application for Years of Lead
Desktop interface for the insurgency simulation game
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path

# Import game modules
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from game.core import GameState, Agent, AgentStatus


class YearsOfLeadGUI:
    """Main GUI application for Years of Lead"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Years of Lead - Insurgency Simulator")
        self.root.geometry("1400x900")

        # Initialize game state
        self.game_state = GameState()
        self.game_state.initialize_game()

        # Theme colors
        self.colors = {
            "bg_primary": "#1a1a1a",
            "bg_secondary": "#2d2d2d",
            "bg_panel": "#3a3a3a",
            "text_primary": "#ffffff",
            "text_secondary": "#cccccc",
            "accent_blue": "#4a9eff",
            "accent_orange": "#ff6b35",
            "accent_green": "#6dd400",
            "accent_red": "#ff4757",
            "warn_yellow": "#ffa502",
        }

        # Configure root styling
        self.root.configure(bg=self.colors["bg_primary"])

        # Game state tracking
        self.auto_advance = False
        self.is_paused = False

        # Create UI components
        self.setup_ui()
        self.bind_events()

        # Start the update loop
        self.update_display()

    def setup_ui(self):
        """Set up the main UI layout"""

        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure style
        self.setup_styles()

        # Top panel - Game status and controls
        self.setup_top_panel(main_frame)

        # Middle panel - Main game display
        self.setup_middle_panel(main_frame)

        # Bottom panel - Actions and controls
        self.setup_bottom_panel(main_frame)

    def setup_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()

        # Configure dark theme
        style.theme_use("clam")

        # Frame styles
        style.configure("Dark.TFrame", background=self.colors["bg_panel"])
        style.configure("Primary.TFrame", background=self.colors["bg_primary"])

        # Label styles
        style.configure(
            "Dark.TLabel",
            background=self.colors["bg_panel"],
            foreground=self.colors["text_primary"],
        )
        style.configure(
            "Title.TLabel",
            background=self.colors["bg_panel"],
            foreground=self.colors["accent_blue"],
            font=("Arial", 12, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background=self.colors["bg_panel"],
            foreground=self.colors["accent_green"],
            font=("Arial", 10, "bold"),
        )

        # Button styles
        style.configure(
            "Action.TButton",
            background=self.colors["accent_blue"],
            foreground="white",
            font=("Arial", 10, "bold"),
        )
        style.configure(
            "Danger.TButton",
            background=self.colors["accent_red"],
            foreground="white",
            font=("Arial", 10, "bold"),
        )

    def setup_top_panel(self, parent):
        """Set up the top status panel"""
        top_frame = ttk.Frame(parent, style="Dark.TFrame")
        top_frame.pack(fill="x", pady=(0, 10))

        # Game title and day
        title_frame = ttk.Frame(top_frame, style="Dark.TFrame")
        title_frame.pack(side="left", fill="x", expand=True)

        ttk.Label(
            title_frame,
            text="YEARS OF LEAD",
            style="Title.TLabel",
            font=("Arial", 16, "bold"),
        ).pack(side="left")

        self.day_label = ttk.Label(
            title_frame,
            text=f"Day {self.game_state.turn_number}",
            style="Status.TLabel",
        )
        self.day_label.pack(side="left", padx=(20, 0))

        self.phase_label = ttk.Label(
            title_frame,
            text=f"Phase: {self.game_state.current_phase.value.title()}",
            style="Status.TLabel",
        )
        self.phase_label.pack(side="left", padx=(20, 0))

        # Control buttons
        control_frame = ttk.Frame(top_frame, style="Dark.TFrame")
        control_frame.pack(side="right")

        self.advance_btn = ttk.Button(
            control_frame,
            text="Advance Turn",
            command=self.advance_turn,
            style="Action.TButton",
        )
        self.advance_btn.pack(side="left", padx=5)

        self.auto_btn = ttk.Button(
            control_frame,
            text="Auto Play",
            command=self.toggle_auto_play,
            style="Action.TButton",
        )
        self.auto_btn.pack(side="left", padx=5)

        ttk.Button(
            control_frame,
            text="Save Game",
            command=self.save_game,
            style="Action.TButton",
        ).pack(side="left", padx=5)

        ttk.Button(
            control_frame, text="Quit", command=self.quit_game, style="Danger.TButton"
        ).pack(side="left", padx=5)

    def setup_middle_panel(self, parent):
        """Set up the main display area"""
        middle_frame = ttk.Frame(parent, style="Primary.TFrame")
        middle_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Left panel - Agents and factions
        left_panel = ttk.Frame(middle_frame, style="Dark.TFrame", width=400)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        self.setup_left_panel(left_panel)

        # Center panel - Narrative and events
        center_panel = ttk.Frame(middle_frame, style="Dark.TFrame")
        center_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.setup_center_panel(center_panel)

        # Right panel - Detailed info
        right_panel = ttk.Frame(middle_frame, style="Dark.TFrame", width=350)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        self.setup_right_panel(right_panel)

    def setup_left_panel(self, parent):
        """Set up the left panel with agents and factions"""
        ttk.Label(parent, text="FACTION STATUS", style="Title.TLabel").pack(pady=10)

        # Faction status
        self.faction_frame = ttk.Frame(parent, style="Dark.TFrame")
        self.faction_frame.pack(fill="x", padx=10, pady=(0, 20))

        # Agent list
        ttk.Label(parent, text="AGENTS", style="Title.TLabel").pack(pady=(10, 5))

        # Agent filter buttons
        filter_frame = ttk.Frame(parent, style="Dark.TFrame")
        filter_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.agent_filter = tk.StringVar(value="all")
        ttk.Radiobutton(
            filter_frame,
            text="All",
            variable=self.agent_filter,
            value="all",
            command=self.update_agent_list,
        ).pack(side="left")
        ttk.Radiobutton(
            filter_frame,
            text="Active",
            variable=self.agent_filter,
            value="active",
            command=self.update_agent_list,
        ).pack(side="left")
        ttk.Radiobutton(
            filter_frame,
            text="Captured",
            variable=self.agent_filter,
            value="captured",
            command=self.update_agent_list,
        ).pack(side="left")

        # Agent listbox with scrollbar
        agent_list_frame = ttk.Frame(parent, style="Dark.TFrame")
        agent_list_frame.pack(fill="both", expand=True, padx=10)

        self.agent_listbox = tk.Listbox(
            agent_list_frame,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            selectbackground=self.colors["accent_blue"],
            font=("Consolas", 10),
        )
        agent_scrollbar = ttk.Scrollbar(agent_list_frame, orient="vertical")

        self.agent_listbox.config(yscrollcommand=agent_scrollbar.set)
        agent_scrollbar.config(command=self.agent_listbox.yview)

        self.agent_listbox.pack(side="left", fill="both", expand=True)
        agent_scrollbar.pack(side="right", fill="y")

        # Bind agent selection
        self.agent_listbox.bind("<<ListboxSelect>>", self.on_agent_select)

    def setup_center_panel(self, parent):
        """Set up the center narrative panel"""
        ttk.Label(parent, text="NARRATIVE & EVENTS", style="Title.TLabel").pack(pady=10)

        # Main narrative display
        self.narrative_text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Georgia", 11),
            height=15,
        )
        self.narrative_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Recent events
        events_frame = ttk.Frame(parent, style="Dark.TFrame")
        events_frame.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(events_frame, text="Recent Events", style="Title.TLabel").pack()

        self.events_listbox = tk.Listbox(
            events_frame,
            height=6,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
            font=("Arial", 9),
        )
        self.events_listbox.pack(fill="x", pady=5)

    def setup_right_panel(self, parent):
        """Set up the right panel with detailed information"""
        ttk.Label(parent, text="AGENT DETAILS", style="Title.TLabel").pack(pady=10)

        # Agent details frame
        self.details_frame = ttk.Frame(parent, style="Dark.TFrame")
        self.details_frame.pack(fill="both", expand=True, padx=10)

        # Emotional state visualization
        self.setup_emotional_display()

        # Selected agent info
        self.agent_info_text = scrolledtext.ScrolledText(
            self.details_frame,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Consolas", 10),
            height=10,
        )
        self.agent_info_text.pack(fill="x", pady=10)

        # Location info
        ttk.Label(
            self.details_frame, text="Location Status", style="Title.TLabel"
        ).pack(pady=(10, 5))

        self.location_info_text = tk.Text(
            self.details_frame,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Arial", 9),
            height=8,
        )
        self.location_info_text.pack(fill="x")

    def setup_emotional_display(self):
        """Set up emotional state visualization"""
        emotion_frame = ttk.Frame(self.details_frame, style="Dark.TFrame")
        emotion_frame.pack(fill="x", pady=10)

        ttk.Label(emotion_frame, text="Emotional State", style="Title.TLabel").pack()

        # Create canvas for emotion visualization
        self.emotion_canvas = tk.Canvas(
            emotion_frame,
            width=300,
            height=150,
            bg=self.colors["bg_secondary"],
            highlightthickness=0,
        )
        self.emotion_canvas.pack(pady=5)

    def setup_bottom_panel(self, parent):
        """Set up the bottom action panel"""
        bottom_frame = ttk.Frame(parent, style="Dark.TFrame")
        bottom_frame.pack(fill="x")

        ttk.Label(bottom_frame, text="ACTIONS", style="Title.TLabel").pack(pady=(10, 5))

        # Action buttons
        action_grid = ttk.Frame(bottom_frame, style="Dark.TFrame")
        action_grid.pack(fill="x", padx=10, pady=10)

        # Row 1 - Agent actions
        ttk.Button(
            action_grid,
            text="View Agent Details",
            command=self.show_agent_details,
            style="Action.TButton",
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            action_grid,
            text="Assign Mission",
            command=self.assign_mission,
            style="Action.TButton",
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            action_grid,
            text="Move Agent",
            command=self.move_agent,
            style="Action.TButton",
        ).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(
            action_grid,
            text="Manage Relationships",
            command=self.manage_relationships,
            style="Action.TButton",
        ).grid(row=0, column=3, padx=5, pady=5)

        # Row 2 - Game actions
        ttk.Button(
            action_grid,
            text="Faction Overview",
            command=self.show_faction_overview,
            style="Action.TButton",
        ).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(
            action_grid,
            text="Location Report",
            command=self.show_location_report,
            style="Action.TButton",
        ).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            action_grid,
            text="Create Mission",
            command=self.create_mission,
            style="Action.TButton",
        ).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(
            action_grid,
            text="Game Statistics",
            command=self.show_statistics,
            style="Action.TButton",
        ).grid(row=1, column=3, padx=5, pady=5)

    def bind_events(self):
        """Bind keyboard and window events"""
        self.root.bind("<Control-s>", lambda e: self.save_game())
        self.root.bind("<Control-q>", lambda e: self.quit_game())
        self.root.bind("<space>", lambda e: self.advance_turn())
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

    def update_display(self):
        """Update all display elements"""
        self.update_status_labels()
        self.update_faction_status()
        self.update_agent_list()
        self.update_narrative()
        self.update_events()
        self.update_selected_agent()

        # Schedule next update
        self.root.after(1000, self.update_display)

    def update_status_labels(self):
        """Update the top status labels"""
        self.day_label.config(text=f"Day {self.game_state.turn_number}")
        self.phase_label.config(
            text=f"Phase: {self.game_state.current_phase.value.title()}"
        )

    def update_faction_status(self):
        """Update faction status display"""
        # Build once and update labels thereafter to prevent flicker
        if not hasattr(self, "_faction_widgets"):
            self._faction_widgets = {}

        existing_ids = set(self._faction_widgets.keys())

        # Create or update widgets for each faction
        for faction_id, faction in self.game_state.factions.items():
            if faction_id not in self._faction_widgets:
                # Build UI container for this faction
                faction_frame = ttk.Frame(self.faction_frame, style="Dark.TFrame")
                faction_frame.pack(fill="x", pady=5)

                name_label = ttk.Label(
                    faction_frame, text=faction.name, style="Status.TLabel"
                )
                name_label.pack(anchor="w")

                resource_label = ttk.Label(
                    faction_frame, style="Dark.TLabel", font=("Consolas", 9)
                )
                resource_label.pack(anchor="w")

                self._faction_widgets[faction_id] = {
                    "frame": faction_frame,
                    "name_label": name_label,
                    "resource_label": resource_label,
                }
            # Update labels if values changed
            widgets = self._faction_widgets[faction_id]
            widgets["name_label"].config(text=faction.name)

            resources = faction.resources
            resource_text = (
                f"💰 {resources.get('money', 0)} | "
                f"👥 {resources.get('personnel', 0)} | "
                f"📈 {resources.get('influence', 0)}"
            )
            widgets["resource_label"].config(text=resource_text)

        # Remove UI for factions that no longer exist
        for removed_id in existing_ids - set(self.game_state.factions.keys()):
            widgets = self._faction_widgets.pop(removed_id)
            widgets["frame"].destroy()

    def update_agent_list(self):
        """Update the agent list based on current filter"""
        self.agent_listbox.delete(0, tk.END)

        filter_value = self.agent_filter.get()

        for agent_id, agent in self.game_state.agents.items():
            # Apply filter
            if filter_value == "active" and agent.status != AgentStatus.ACTIVE:
                continue
            elif filter_value == "captured" and agent.status != AgentStatus.ARRESTED:
                continue

            # Format agent display
            status_icon = self.get_status_icon(agent.status)
            faction_name = self.game_state.factions[agent.faction_id].name
            location_name = self.game_state.locations[agent.location_id].name

            display_text = (
                f"{status_icon} {agent.name} ({faction_name[:8]}) - {location_name}"
            )
            self.agent_listbox.insert(tk.END, display_text)

    def get_status_icon(self, status: AgentStatus) -> str:
        """Get icon for agent status"""
        icons = {
            AgentStatus.ACTIVE: "🟢",
            AgentStatus.ARRESTED: "🔴",
            AgentStatus.INJURED: "🟡",
            AgentStatus.DEAD: "💀",
        }
        return icons.get(status, "⚪")

    def update_narrative(self):
        """Update the narrative display"""
        # Get recent narrative entries
        if hasattr(self.game_state, "recent_narrative"):
            narrative_text = "\n\n".join(self.game_state.recent_narrative[-5:])

            self.narrative_text.config(state="normal")
            self.narrative_text.delete(1.0, tk.END)
            self.narrative_text.insert(1.0, narrative_text)
            self.narrative_text.config(state="disabled")
            self.narrative_text.see(tk.END)

    def update_events(self):
        """Update the events list"""
        self.events_listbox.delete(0, tk.END)

        # Get status summary for events
        try:
            status = self.game_state.get_status_summary()

            # Add active events (if available)
            active_events = status.get("active_events", [])
            if active_events:
                for event in active_events[-10:]:  # Last 10 events
                    self.events_listbox.insert(tk.END, f"⚡ {event}")

            # Add recent narrative as events
            recent_narrative = status.get("recent_narrative", [])
            for event in recent_narrative[-5:]:  # Last 5 narrative events
                self.events_listbox.insert(tk.END, f"📝 {event}")

        except Exception as e:
            # Fallback: show basic event info
            self.events_listbox.insert(tk.END, "📊 Game events will appear here")
            self.events_listbox.insert(
                tk.END, f"⚠️ Status update error: {str(e)[:50]}..."
            )

    def update_selected_agent(self):
        """Update the selected agent details"""
        selection = self.agent_listbox.curselection()
        if not selection:
            return

        # Get selected agent
        agent_index = selection[0]
        list(self.game_state.agents.keys())

        # Apply filter to get correct agent
        filter_value = self.agent_filter.get()
        filtered_agents = []

        for agent_id, agent in self.game_state.agents.items():
            if filter_value == "active" and agent.status != AgentStatus.ACTIVE:
                continue
            elif filter_value == "captured" and agent.status != AgentStatus.ARRESTED:
                continue
            filtered_agents.append(agent_id)

        if agent_index < len(filtered_agents):
            agent_id = filtered_agents[agent_index]
            agent = self.game_state.agents[agent_id]

            self.display_agent_details(agent)
            self.display_emotional_state(agent)
            self.display_location_info(agent)

    def display_agent_details(self, agent: Agent):
        """Display detailed agent information"""
        info_text = []
        info_text.append(f"Name: {agent.name}")
        info_text.append(f"Faction: {self.game_state.factions[agent.faction_id].name}")
        info_text.append(
            f"Location: {self.game_state.locations[agent.location_id].name}"
        )
        info_text.append(f"Status: {agent.status.value.title()}")
        info_text.append(f"Background: {agent.background.title()}")
        info_text.append(f"Loyalty: {agent.loyalty}%")
        info_text.append(f"Stress: {agent.stress}%")
        info_text.append("")

        # Skills
        info_text.append("Skills:")
        for skill_type, skill in agent.skills.items():
            info_text.append(f"  {skill_type.value.title()}: {skill.level}")
        info_text.append("")

        # Equipment
        info_text.append("Equipment:")
        for equipment in agent.equipment:
            info_text.append(f"  • {equipment.name}")

        # Relationships
        if agent.relationships:
            info_text.append("")
            info_text.append("Key Relationships:")
            for other_id, relationship in list(agent.relationships.items())[:5]:
                other_agent = self.game_state.agents.get(other_id)
                if other_agent:
                    info_text.append(
                        f"  {other_agent.name}: Affinity {relationship.affinity:.1f}"
                    )

        self.agent_info_text.config(state="normal")
        self.agent_info_text.delete(1.0, tk.END)
        self.agent_info_text.insert(1.0, "\n".join(info_text))
        self.agent_info_text.config(state="disabled")

    def display_emotional_state(self, agent: Agent):
        """Display agent's emotional state visually"""
        self.emotion_canvas.delete("all")

        if not hasattr(agent, "emotional_state") or agent.emotional_state is None:
            return

        # Get individual emotion values
        emotions = {
            "fear": agent.emotional_state.fear,
            "anger": agent.emotional_state.anger,
            "sadness": agent.emotional_state.sadness,
            "joy": agent.emotional_state.joy,
            "trust": agent.emotional_state.trust,
            "anticipation": agent.emotional_state.anticipation,
            "surprise": agent.emotional_state.surprise,
            "disgust": agent.emotional_state.disgust,
        }

        bar_height = 15
        bar_spacing = 20
        y_start = 20

        for i, (emotion, value) in enumerate(emotions.items()):
            y = y_start + i * bar_spacing
            bar_width = int(abs(value) * 200)  # Scale to 200 pixels max

            # Color based on emotion type
            color = self.get_emotion_color(emotion)

            # Draw bar background
            self.emotion_canvas.create_rectangle(
                80,
                y,
                280,
                y + bar_height,
                fill=self.colors["bg_primary"],
                outline="white",
            )

            # Draw filled bar
            if bar_width > 0:
                self.emotion_canvas.create_rectangle(
                    80, y, 80 + bar_width, y + bar_height, fill=color, outline=""
                )

            # Label
            self.emotion_canvas.create_text(
                5,
                y + bar_height // 2,
                text=emotion.title(),
                anchor="w",
                fill="white",
                font=("Arial", 9),
            )

            # Value
            self.emotion_canvas.create_text(
                285,
                y + bar_height // 2,
                text=f"{value:.2f}",
                anchor="w",
                fill="white",
                font=("Arial", 8),
            )

    def get_emotion_color(self, emotion: str) -> str:
        """Get color for emotion visualization"""
        emotion_colors = {
            "joy": self.colors["accent_green"],
            "sadness": "#4a90e2",
            "anger": self.colors["accent_red"],
            "fear": "#9b59b6",
            "disgust": "#f39c12",
            "surprise": self.colors["warn_yellow"],
            "trust": self.colors["accent_blue"],
            "anticipation": "#ff7675",
        }
        return emotion_colors.get(emotion.lower(), self.colors["text_secondary"])

    def display_location_info(self, agent: Agent):
        """Display information about the agent's current location"""
        location = self.game_state.locations[agent.location_id]

        info_text = []
        info_text.append(f"Location: {location.name}")
        info_text.append(f"Security Level: {location.security_level}/10")
        info_text.append(f"Unrest Level: {location.unrest_level}/10")
        info_text.append("")

        # Agents in this location
        agents_here = [
            a
            for a in self.game_state.agents.values()
            if a.location_id == agent.location_id
        ]
        info_text.append(f"Agents Here ({len(agents_here)}):")
        for a in agents_here[:5]:  # Show first 5
            faction_name = self.game_state.factions[a.faction_id].name
            info_text.append(f"  • {a.name} ({faction_name})")

        if len(agents_here) > 5:
            info_text.append(f"  ... and {len(agents_here) - 5} more")

        self.location_info_text.config(state="normal")
        self.location_info_text.delete(1.0, tk.END)
        self.location_info_text.insert(1.0, "\n".join(info_text))
        self.location_info_text.config(state="disabled")

    # Event handlers
    def on_agent_select(self, event):
        """Handle agent selection in listbox"""
        self.update_selected_agent()

    def advance_turn(self):
        """Advance the game by one turn"""
        try:
            self.game_state.advance_turn()
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to advance turn: {str(e)}")

    def toggle_auto_play(self):
        """Toggle automatic turn advancement"""
        self.auto_advance = not self.auto_advance
        self.auto_btn.config(text="Stop Auto" if self.auto_advance else "Auto Play")

        if self.auto_advance:
            self.auto_play_loop()

    def auto_play_loop(self):
        """Auto-advance turns with delay"""
        if self.auto_advance and not self.is_paused:
            self.advance_turn()
            self.root.after(3000, self.auto_play_loop)  # 3 second delay

    def save_game(self):
        """Save the current game state"""
        try:
            # Simple save implementation
            import pickle

            save_path = Path("savegames")
            save_path.mkdir(exist_ok=True)

            with open(save_path / "current_game.pkl", "wb") as f:
                pickle.dump(self.game_state, f)

            messagebox.showinfo("Save Game", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save game: {str(e)}")

    def quit_game(self):
        """Quit the application"""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.quit()

    # Action button handlers
    def show_agent_details(self):
        """Show detailed agent information window"""
        selection = self.agent_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an agent first.")
            return

        # Implementation for detailed agent window would go here
        messagebox.showinfo("Agent Details", "Detailed agent window would open here.")

    def assign_mission(self):
        """Assign a mission to selected agent"""
        messagebox.showinfo(
            "Assign Mission", "Mission assignment dialog would open here."
        )

    def move_agent(self):
        """Move agent to different location"""
        messagebox.showinfo("Move Agent", "Agent movement dialog would open here.")

    def manage_relationships(self):
        """Manage agent relationships"""
        messagebox.showinfo(
            "Relationships", "Relationship management window would open here."
        )

    def show_faction_overview(self):
        """Show faction overview"""
        messagebox.showinfo(
            "Faction Overview", "Faction overview window would open here."
        )

    def show_location_report(self):
        """Show location report"""
        messagebox.showinfo(
            "Location Report", "Location report window would open here."
        )

    def create_mission(self):
        """Create a new mission"""
        messagebox.showinfo(
            "Create Mission", "Mission creation dialog would open here."
        )

    def show_statistics(self):
        """Show game statistics"""
        messagebox.showinfo("Statistics", "Game statistics window would open here.")

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


# Main entry point for GUI
if __name__ == "__main__":
    app = YearsOfLeadGUI()
    app.run()
