"""
GUI Components for Years of Lead
Specialized panels and dialogs for the desktop interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

from game.core import AgentStatus


class StatusPanel(ttk.Frame):
    """Panel for displaying game status information"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, style="Dark.TFrame", **kwargs)
        self.colors = colors
        self.setup_ui()

    def setup_ui(self):
        """Set up the status panel UI"""
        ttk.Label(self, text="GAME STATUS", style="Title.TLabel").pack(pady=5)

        # Status indicators
        self.status_frame = ttk.Frame(self, style="Dark.TFrame")
        self.status_frame.pack(fill="x", padx=10, pady=5)

        # Day counter
        self.day_label = ttk.Label(
            self.status_frame, text="Day: 1", style="Status.TLabel"
        )
        self.day_label.pack(anchor="w")

        # Phase indicator
        self.phase_label = ttk.Label(
            self.status_frame, text="Phase: Planning", style="Status.TLabel"
        )
        self.phase_label.pack(anchor="w")

        # Active agents
        self.agents_label = ttk.Label(
            self.status_frame, text="Active Agents: 0/0", style="Status.TLabel"
        )
        self.agents_label.pack(anchor="w")

    def update_status(self, game_state):
        """Update status display with current game state"""
        self.day_label.config(text=f"Day: {game_state.turn_number}")
        self.phase_label.config(text=f"Phase: {game_state.current_phase.value.title()}")

        # Count active agents
        active_agents = sum(
            1
            for agent in game_state.agents.values()
            if agent.status == AgentStatus.ACTIVE
        )
        total_agents = len(game_state.agents)
        self.agents_label.config(text=f"Active Agents: {active_agents}/{total_agents}")


class NarrativePanel(ttk.Frame):
    """Panel for displaying narrative text and events"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, style="Dark.TFrame", **kwargs)
        self.colors = colors
        self.setup_ui()

    def setup_ui(self):
        """Set up the narrative panel UI"""
        ttk.Label(self, text="NARRATIVE", style="Title.TLabel").pack(pady=5)

        # Main narrative text area
        self.narrative_text = tk.Text(
            self,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Georgia", 11),
            height=12,
            state="disabled",
        )
        self.narrative_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar for narrative
        narrative_scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.narrative_text.yview
        )
        self.narrative_text.config(yscrollcommand=narrative_scrollbar.set)
        narrative_scrollbar.pack(side="right", fill="y")

    def add_narrative(self, text: str):
        """Add narrative text to the display"""
        self.narrative_text.config(state="normal")
        self.narrative_text.insert(tk.END, f"{text}\n\n")
        self.narrative_text.config(state="disabled")
        self.narrative_text.see(tk.END)

    def clear_narrative(self):
        """Clear all narrative text"""
        self.narrative_text.config(state="normal")
        self.narrative_text.delete(1.0, tk.END)
        self.narrative_text.config(state="disabled")


class ActionPanel(ttk.Frame):
    """Panel for game actions and controls"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, style="Dark.TFrame", **kwargs)
        self.colors = colors
        self.setup_ui()

    def setup_ui(self):
        """Set up the action panel UI"""
        ttk.Label(self, text="ACTIONS", style="Title.TLabel").pack(pady=5)

        # Action buttons frame
        self.buttons_frame = ttk.Frame(self, style="Dark.TFrame")
        self.buttons_frame.pack(fill="x", padx=10, pady=5)

        # Create action buttons
        self.create_action_buttons()

    def create_action_buttons(self):
        """Create the action buttons"""
        actions = [
            ("Advance Turn", self.advance_turn),
            ("Auto Play", self.toggle_auto),
            ("Save Game", self.save_game),
            ("Load Game", self.load_game),
            ("Quit", self.quit_game),
        ]

        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(
                self.buttons_frame, text=text, command=command, style="Action.TButton"
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")

        # Configure grid weights
        for i in range(3):
            self.buttons_frame.columnconfigure(i, weight=1)

    def advance_turn(self):
        """Advance turn action"""
        # This will be connected to the main game logic
        pass

    def toggle_auto(self):
        """Toggle auto-play action"""
        pass

    def save_game(self):
        """Save game action"""
        pass

    def load_game(self):
        """Load game action"""
        pass

    def quit_game(self):
        """Quit game action"""
        pass


class AgentDetailPanel(ttk.Frame):
    """Panel for displaying detailed agent information"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, style="Dark.TFrame", **kwargs)
        self.colors = colors
        self.setup_ui()

    def setup_ui(self):
        """Set up the agent detail panel UI"""
        ttk.Label(self, text="AGENT DETAILS", style="Title.TLabel").pack(pady=5)

        # Agent info frame
        self.info_frame = ttk.Frame(self, style="Dark.TFrame")
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Agent name
        self.name_label = ttk.Label(
            self.info_frame, text="No agent selected", style="Title.TLabel"
        )
        self.name_label.pack(anchor="w")

        # Agent details text
        self.details_text = tk.Text(
            self.info_frame,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Consolas", 10),
            height=15,
            state="disabled",
        )
        self.details_text.pack(fill="both", expand=True, pady=5)

    def display_agent(self, agent):
        """Display agent information"""
        if not agent:
            self.name_label.config(text="No agent selected")
            self.details_text.config(state="normal")
            self.details_text.delete(1.0, tk.END)
            self.details_text.config(state="disabled")
            return

        self.name_label.config(text=agent.name)

        # Build agent details text
        details = []
        details.append(f"Name: {agent.name}")
        details.append(f"Status: {agent.status.value.title()}")
        details.append(f"Background: {agent.background.title()}")
        details.append(f"Loyalty: {agent.loyalty}%")
        details.append(f"Stress: {agent.stress}%")
        details.append("")

        # Skills
        details.append("Skills:")
        for skill_type, skill in agent.skills.items():
            details.append(f"  {skill_type.value.title()}: {skill.level}")
        details.append("")

        # Equipment
        details.append("Equipment:")
        for equipment in agent.equipment:
            details.append(f"  • {equipment.name}")

        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, "\n".join(details))
        self.details_text.config(state="disabled")


class LocationPanel(ttk.Frame):
    """Panel for displaying location information"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, style="Dark.TFrame", **kwargs)
        self.colors = colors
        self.setup_ui()

    def setup_ui(self):
        """Set up the location panel UI"""
        ttk.Label(self, text="LOCATIONS", style="Title.TLabel").pack(pady=5)

        # Location listbox
        self.location_listbox = tk.Listbox(
            self,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            selectbackground=self.colors["accent_blue"],
            font=("Consolas", 10),
            height=8,
        )
        self.location_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        # Location details
        self.location_details = tk.Text(
            self,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Arial", 9),
            height=6,
            state="disabled",
        )
        self.location_details.pack(fill="x", padx=10, pady=5)

    def update_locations(self, locations: Dict[str, Any]):
        """Update location list"""
        self.location_listbox.delete(0, tk.END)

        for location_id, location in locations.items():
            display_text = f"📍 {location.name} (Sec: {location.security_level}, Unrest: {location.unrest_level})"
            self.location_listbox.insert(tk.END, display_text)

    def display_location_details(self, location):
        """Display detailed location information"""
        if not location:
            self.location_details.config(state="normal")
            self.location_details.delete(1.0, tk.END)
            self.location_details.config(state="disabled")
            return

        details = []
        details.append(f"Location: {location.name}")
        details.append(f"Security Level: {location.security_level}/10")
        details.append(f"Unrest Level: {location.unrest_level}/10")
        details.append("")
        details.append("Agents in this location:")

        # This would be populated with actual agent data
        details.append("  (Agent list would appear here)")

        self.location_details.config(state="normal")
        self.location_details.delete(1.0, tk.END)
        self.location_details.insert(1.0, "\n".join(details))
        self.location_details.config(state="disabled")


class EmotionalVisualization(ttk.Frame):
    """Canvas-based emotional state visualization"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, style="Dark.TFrame", **kwargs)
        self.colors = colors
        self.setup_ui()

    def setup_ui(self):
        """Set up the emotional visualization UI"""
        ttk.Label(self, text="EMOTIONAL STATE", style="Title.TLabel").pack(pady=5)

        # Canvas for emotion visualization
        self.canvas = tk.Canvas(
            self,
            width=300,
            height=200,
            bg=self.colors["bg_secondary"],
            highlightthickness=0,
        )
        self.canvas.pack(pady=5)

    def visualize_emotions(self, emotions: Dict[str, float]):
        """Visualize emotional state as bars"""
        self.canvas.delete("all")

        if not emotions:
            return

        bar_height = 15
        bar_spacing = 20
        y_start = 20
        max_width = 250

        for i, (emotion, value) in enumerate(emotions.items()):
            y = y_start + i * bar_spacing
            bar_width = int(value * max_width)

            # Color based on emotion type
            color = self.get_emotion_color(emotion)

            # Draw bar background
            self.canvas.create_rectangle(
                50,
                y,
                50 + max_width,
                y + bar_height,
                fill=self.colors["bg_primary"],
                outline="white",
            )

            # Draw filled bar
            if bar_width > 0:
                self.canvas.create_rectangle(
                    50, y, 50 + bar_width, y + bar_height, fill=color, outline=""
                )

            # Label
            self.canvas.create_text(
                5,
                y + bar_height // 2,
                text=emotion.title(),
                anchor="w",
                fill="white",
                font=("Arial", 9),
            )

            # Value
            self.canvas.create_text(
                305,
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


class MissionDialog(tk.Toplevel):
    """Dialog for creating and managing missions"""

    def __init__(self, parent, colors: Dict[str, str], **kwargs):
        super().__init__(parent, **kwargs)
        self.colors = colors
        self.result = None

        self.title("Create Mission")
        self.geometry("500x400")
        self.configure(bg=self.colors["bg_primary"])

        self.setup_ui()

    def setup_ui(self):
        """Set up the mission dialog UI"""
        # Mission type selection
        ttk.Label(self, text="Mission Type", style="Title.TLabel").pack(pady=10)

        self.mission_type = tk.StringVar(value="gather_info")
        mission_types = [
            ("Gather Information", "gather_info"),
            ("Sabotage", "sabotage"),
            ("Recruitment", "recruit"),
            ("Propaganda", "propaganda"),
            ("Move", "move"),
        ]

        for text, value in mission_types:
            ttk.Radiobutton(
                self, text=text, variable=self.mission_type, value=value
            ).pack(anchor="w", padx=20)

        # Target location
        ttk.Label(self, text="Target Location", style="Title.TLabel").pack(pady=(20, 5))
        self.location_var = tk.StringVar()
        self.location_combo = ttk.Combobox(self, textvariable=self.location_var)
        self.location_combo.pack(padx=20, pady=5, fill="x")

        # Difficulty
        ttk.Label(self, text="Difficulty", style="Title.TLabel").pack(pady=(20, 5))
        self.difficulty_var = tk.IntVar(value=5)
        difficulty_scale = ttk.Scale(
            self, from_=1, to=10, variable=self.difficulty_var, orient="horizontal"
        )
        difficulty_scale.pack(padx=20, pady=5, fill="x")

        # Description
        ttk.Label(self, text="Description", style="Title.TLabel").pack(pady=(20, 5))
        self.description_text = tk.Text(self, height=4, wrap=tk.WORD)
        self.description_text.pack(padx=20, pady=5, fill="both", expand=True)

        # Buttons
        button_frame = ttk.Frame(self, style="Dark.TFrame")
        button_frame.pack(fill="x", padx=20, pady=20)

        ttk.Button(
            button_frame,
            text="Create Mission",
            command=self.create_mission,
            style="Action.TButton",
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="Cancel", command=self.cancel, style="Danger.TButton"
        ).pack(side="right", padx=5)

    def create_mission(self):
        """Create the mission and close dialog"""
        self.result = {
            "type": self.mission_type.get(),
            "location": self.location_var.get(),
            "difficulty": self.difficulty_var.get(),
            "description": self.description_text.get(1.0, tk.END).strip(),
        }
        self.destroy()

    def cancel(self):
        """Cancel mission creation"""
        self.result = None
        self.destroy()


class AgentMovementDialog(tk.Toplevel):
    """Dialog for moving agents between locations"""

    def __init__(self, parent, colors: Dict[str, str], agent, locations, **kwargs):
        super().__init__(parent, **kwargs)
        self.colors = colors
        self.agent = agent
        self.locations = locations
        self.result = None

        self.title(f"Move {agent.name}")
        self.geometry("400x300")
        self.configure(bg=self.colors["bg_primary"])

        self.setup_ui()

    def setup_ui(self):
        """Set up the movement dialog UI"""
        ttk.Label(self, text=f"Move {self.agent.name}", style="Title.TLabel").pack(
            pady=10
        )

        # Current location
        current_location = self.locations[self.agent.location_id].name
        ttk.Label(
            self, text=f"Current Location: {current_location}", style="Status.TLabel"
        ).pack(pady=5)

        # Target location selection
        ttk.Label(self, text="Target Location", style="Title.TLabel").pack(pady=(20, 5))

        self.target_location = tk.StringVar()
        location_names = [loc.name for loc in self.locations.values()]
        self.location_combo = ttk.Combobox(
            self, textvariable=self.target_location, values=location_names
        )
        self.location_combo.pack(padx=20, pady=5, fill="x")

        # Movement type
        ttk.Label(self, text="Movement Type", style="Title.TLabel").pack(pady=(20, 5))

        self.movement_type = tk.StringVar(value="normal")
        ttk.Radiobutton(
            self, text="Normal Movement", variable=self.movement_type, value="normal"
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            self, text="Stealth Movement", variable=self.movement_type, value="stealth"
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            self, text="Rush Movement", variable=self.movement_type, value="rush"
        ).pack(anchor="w", padx=20)

        # Buttons
        button_frame = ttk.Frame(self, style="Dark.TFrame")
        button_frame.pack(fill="x", padx=20, pady=20)

        ttk.Button(
            button_frame,
            text="Move Agent",
            command=self.move_agent,
            style="Action.TButton",
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="Cancel", command=self.cancel, style="Danger.TButton"
        ).pack(side="right", padx=5)

    def move_agent(self):
        """Execute agent movement"""
        target_name = self.target_location.get()
        if not target_name:
            messagebox.showwarning("No Target", "Please select a target location.")
            return

        # Find location ID by name
        target_id = None
        for loc_id, location in self.locations.items():
            if location.name == target_name:
                target_id = loc_id
                break

        if target_id:
            self.result = {
                "agent_id": self.agent.id,
                "target_location_id": target_id,
                "movement_type": self.movement_type.get(),
            }
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid target location.")

    def cancel(self):
        """Cancel movement"""
        self.result = None
        self.destroy()
