"""
Years of Lead - Enhanced Navigation System

DF/Rimworld-style navigation improvements:
- Number key navigation (1-9)
- Escape key functionality
- Multi-pane layouts
- Context-sensitive menus
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class NavigationPane:
    """Represents a pane in multi-pane layout"""
    name: str
    content_type: str
    width: int
    height: int
    data: Dict[str, Any] = None


class EnhancedNavigation:
    """DF/Rimworld-style navigation system"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        
        # Navigation state
        self.number_navigation = True
        self.escape_stack = []
        self.current_pane = "main"
        self.multi_pane_mode = False
        self.selected_index = 0
        
        # Pane configurations
        self.pane_layouts = {
            "main": {
                "type": "single",
                "content": "menu",
                "items": [
                    ("1", "advance", "Advance Turn/Phase"),
                    ("2", "agents", "Agent Management"),
                    ("3", "missions", "Mission Operations"),
                    ("4", "intelligence", "Intelligence Center"),
                    ("5", "inventory", "Inventory & Storage"),
                    ("6", "equipment", "Equipment Management"),
                    ("7", "relationships", "Agent Relationships"),
                    ("8", "narrative", "Dynamic Narrative"),
                    ("9", "save", "Save/Load Game"),
                    ("esc", "back", "Go Back"),
                    ("?", "help", "Context Help"),
                    ("*", "query", "Query Mode")
                ]
            },
            "agents": {
                "type": "multi",
                "panes": ["list", "details", "status"],
                "items": [
                    ("1", "list", "Agent List"),
                    ("2", "details", "Agent Details"),
                    ("3", "status", "Status Overview"),
                    ("4", "assign", "Assign Tasks"),
                    ("5", "equipment", "Agent Equipment"),
                    ("6", "relationships", "Agent Relationships"),
                    ("esc", "back", "Back to Main"),
                    ("?", "help", "Help")
                ]
            },
            "missions": {
                "type": "multi",
                "panes": ["list", "planning", "status"],
                "items": [
                    ("1", "list", "Mission List"),
                    ("2", "planning", "Mission Planning"),
                    ("3", "status", "Mission Status"),
                    ("4", "create", "Create Mission"),
                    ("5", "execute", "Execute Mission"),
                    ("6", "results", "Mission Results"),
                    ("esc", "back", "Back to Main"),
                    ("?", "help", "Help")
                ]
            },
            "intelligence": {
                "type": "multi",
                "panes": ["events", "patterns", "alerts"],
                "items": [
                    ("1", "events", "Intelligence Events"),
                    ("2", "patterns", "Pattern Analysis"),
                    ("3", "alerts", "Priority Alerts"),
                    ("4", "counter", "Counter-Intelligence"),
                    ("5", "sources", "Intelligence Sources"),
                    ("6", "threats", "Threat Assessment"),
                    ("esc", "back", "Back to Main"),
                    ("?", "help", "Help")
                ]
            }
        }
    
    def handle_input(self, user_input: str) -> str:
        """Handle user input with DF/Rimworld-style navigation"""
        user_input = user_input.strip().lower()
        
        # Handle escape key
        if user_input in ['esc', 'escape', 'q'] and self.escape_stack:
            return self._handle_escape()
        
        # Handle number key navigation (1-9)
        if self.number_navigation and user_input in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return self._handle_number_navigation(user_input)
        
        # Handle context-specific commands
        current_layout = self.pane_layouts.get(self.current_pane, self.pane_layouts["main"])
        for key, action, description in current_layout["items"]:
            if key == user_input:
                return self._execute_action(action)
        
        # Handle arrow keys
        if user_input in ['up', 'down', 'left', 'right']:
            return self._handle_arrow_navigation(user_input)
        
        # Handle enter key
        if user_input in ['enter', 'return', '']:
            return self._execute_selected_item()
        
        return "Invalid command. Type '?' for help or 'esc' to go back."
    
    def _handle_escape(self) -> str:
        """Handle escape key - go back in navigation stack"""
        if self.escape_stack:
            previous_context = self.escape_stack.pop()
            self.current_pane = previous_context
            self.selected_index = 0
            return f"Returned to {previous_context}"
        else:
            return "Already at main menu"
    
    def _handle_number_navigation(self, number: str) -> str:
        """Handle number key navigation (1-9)"""
        index = int(number) - 1
        current_layout = self.pane_layouts.get(self.current_pane, self.pane_layouts["main"])
        items = current_layout["items"]
        
        if 0 <= index < len(items):
            self.selected_index = index
            return f"Selected: {items[index][1]}"
        else:
            return f"No menu item at position {number}"
    
    def _handle_arrow_navigation(self, direction: str) -> str:
        """Handle arrow key navigation"""
        current_layout = self.pane_layouts.get(self.current_pane, self.pane_layouts["main"])
        items = current_layout["items"]
        
        if direction == "up":
            self.selected_index = max(0, self.selected_index - 1)
        elif direction == "down":
            self.selected_index = min(len(items) - 1, self.selected_index + 1)
        
        return f"Selected: {items[self.selected_index][1]}"
    
    def _execute_selected_item(self) -> str:
        """Execute the currently selected menu item"""
        current_layout = self.pane_layouts.get(self.current_pane, self.pane_layouts["main"])
        items = current_layout["items"]
        
        if 0 <= self.selected_index < len(items):
            key, action, description = items[self.selected_index]
            return self._execute_action(action)
        else:
            return "No item selected"
    
    def _execute_action(self, action: str) -> str:
        """Execute a specific action"""
        if action == "back":
            return self._handle_escape()
        elif action == "agents":
            self.escape_stack.append(self.current_pane)
            self.current_pane = "agents"
            self.multi_pane_mode = True
            self.selected_index = 0
            return "Entered agent management (multi-pane mode)"
        elif action == "missions":
            self.escape_stack.append(self.current_pane)
            self.current_pane = "missions"
            self.multi_pane_mode = True
            self.selected_index = 0
            return "Entered mission operations (multi-pane mode)"
        elif action == "intelligence":
            self.escape_stack.append(self.current_pane)
            self.current_pane = "intelligence"
            self.multi_pane_mode = True
            self.selected_index = 0
            return "Entered intelligence operations (multi-pane mode)"
        elif action == "advance":
            return "Advancing turn..."
        elif action == "help":
            return self._show_context_help()
        elif action == "query":
            return "Query mode activated"
        else:
            return f"Executing: {action}"
    
    def _show_context_help(self) -> str:
        """Show context-sensitive help"""
        current_layout = self.pane_layouts.get(self.current_pane, self.pane_layouts["main"])
        
        help_text = f"\n=== {self.current_pane.upper()} HELP ===\n"
        help_text += "Navigation:\n"
        help_text += "• 1-9: Select menu items\n"
        help_text += "• ↑/↓: Navigate with arrows\n"
        help_text += "• Enter: Execute selected item\n"
        help_text += "• Esc: Go back\n"
        help_text += "• ?: Show this help\n\n"
        
        help_text += "Available commands:\n"
        for key, action, description in current_layout["items"]:
            help_text += f"• {key}: {description}\n"
        
        return help_text
    
    def display_interface(self, terminal_width: int = 80, terminal_height: int = 24):
        """Display the current interface"""
        if self.multi_pane_mode:
            self._display_multi_pane(terminal_width, terminal_height)
        else:
            self._display_single_pane(terminal_width, terminal_height)
    
    def _display_single_pane(self, width: int, height: int):
        """Display single pane interface"""
        print("\n" + "=" * width)
        print("📍 RESISTANCE COMMAND CENTER")
        print("=" * width)
        
        current_layout = self.pane_layouts.get(self.current_pane, self.pane_layouts["main"])
        items = current_layout["items"]
        
        print("Commands (Number Keys 1-9 + Enter, or Letter Keys):")
        for i, (key, action, description) in enumerate(items):
            if i == self.selected_index:
                print(f"→ [{key}] {action:<12} - {description}")
            else:
                print(f"  [{key}] {action:<12} - {description}")
        
        print("=" * width)
        print("Navigation: 1-9 to select, Enter to execute, ↑/↓ arrows, Esc to go back")
        
        if self.escape_stack:
            print(f"📍 Path: {' > '.join(self.escape_stack)}")
    
    def _display_multi_pane(self, width: int, height: int):
        """Display multi-pane interface"""
        if self.current_pane == "agents":
            self._display_agent_multi_pane(width, height)
        elif self.current_pane == "missions":
            self._display_mission_multi_pane(width, height)
        elif self.current_pane == "intelligence":
            self._display_intelligence_multi_pane(width, height)
    
    def _display_agent_multi_pane(self, width: int, height: int):
        """Display agent management in multi-pane layout"""
        print("\n" + "=" * width)
        print("🧑 AGENT MANAGEMENT CENTER")
        print("=" * width)
        
        # Split screen into panes
        left_width = width // 2 - 2
        right_width = width // 2 - 2
        
        # Left pane: Agent list
        print(f"{'AGENT LIST':<{left_width}} | {'AGENT DETAILS':<{right_width}}")
        print("-" * left_width + "-+-" + "-" * right_width)
        
        # Get agents for display
        agents = list(self.game_state.agents.values())[:height-6]
        
        for i, agent in enumerate(agents):
            # Left pane: Agent list with status
            status_icon = "🟢" if agent.status == "active" else "🔴"
            stress_bar = self._create_progress_bar(agent.stress, 10)
            left_content = f"{i+1}. {status_icon} {agent.name:<15} {stress_bar}"
            
            # Right pane: Agent details (if selected)
            if i == self.selected_index:
                right_content = f"Stress: {agent.stress}% | Loyalty: {agent.loyalty}%"
                if hasattr(agent, 'emotional_state'):
                    right_content += f"\nTrauma: {agent.emotional_state.trauma_level:.2f}"
            else:
                right_content = ""
            
            print(f"{left_content:<{left_width}} | {right_content:<{right_width}}")
        
        # Bottom navigation
        print("-" * width)
        print("1-6: Agent actions | Esc: Back | ?: Help")
    
    def _display_mission_multi_pane(self, width: int, height: int):
        """Display mission management in multi-pane layout"""
        print("\n" + "=" * width)
        print("🎯 MISSION OPERATIONS CENTER")
        print("=" * width)
        
        # Split screen into panes
        left_width = width // 3 - 1
        center_width = width // 3 - 1
        right_width = width // 3 - 1
        
        # Three panes: Mission list, Planning, Status
        print(f"{'MISSION LIST':<{left_width}} | {'PLANNING':<{center_width}} | {'STATUS':<{right_width}}")
        print("-" * left_width + "-+-" + "-" * center_width + "-+-" + "-" * right_width)
        
        # Sample mission data
        missions = [
            {"name": "Infiltrate University", "type": "infiltration", "difficulty": 0.6, "status": "🟡"},
            {"name": "Downtown Recon", "type": "reconnaissance", "difficulty": 0.4, "status": "⚪"},
            {"name": "Rescue Operation", "type": "rescue", "difficulty": 0.8, "status": "🔴"}
        ]
        
        for i, mission in enumerate(missions):
            left_content = f"{i+1}. {mission['status']} {mission['name']:<15}"
            
            # Planning info (center pane)
            if i == self.selected_index:
                center_content = f"Type: {mission['type']}\nDifficulty: {mission['difficulty']:.1f}"
                right_content = f"Status: Planning"
            else:
                center_content = ""
                right_content = ""
            
            print(f"{left_content:<{left_width}} | {center_content:<{center_width}} | {right_content:<{right_width}}")
        
        # Bottom navigation
        print("-" * width)
        print("1-6: Mission actions | Esc: Back | ?: Help")
    
    def _display_intelligence_multi_pane(self, width: int, height: int):
        """Display intelligence in multi-pane layout"""
        print("\n" + "=" * width)
        print("🔍 INTELLIGENCE OPERATIONS CENTER")
        print("=" * width)
        
        # Split screen into panes
        left_width = width // 3 - 1
        center_width = width // 3 - 1
        right_width = width // 3 - 1
        
        # Three panes: Events, Patterns, Alerts
        print(f"{'INTEL EVENTS':<{left_width}} | {'PATTERNS':<{center_width}} | {'ALERTS':<{right_width}}")
        print("-" * left_width + "-+-" + "-" * center_width + "-+-" + "-" * right_width)
        
        # Sample intelligence data
        intel_events = [
            "Government movement detected",
            "New security measures",
            "Personnel changes observed"
        ]
        
        patterns = [
            "Increased surveillance",
            "Resource relocation",
            "Communication surge"
        ]
        
        alerts = [
            "⚠️ High threat in Downtown",
            "🔴 Critical alert: Agent exposed",
            "🟡 Medium: Pattern detected"
        ]
        
        # Display data in panes
        max_rows = min(len(intel_events), len(patterns), len(alerts), height-6)
        for i in range(max_rows):
            left_content = f"{i+1}. {intel_events[i]:<{left_width-4}}"
            center_content = f"{i+1}. {patterns[i]:<{center_width-4}}"
            right_content = f"{i+1}. {alerts[i]:<{right_width-4}}"
            
            print(f"{left_content:<{left_width}} | {center_content:<{center_width}} | {right_content:<{right_width}}")
        
        # Bottom navigation
        print("-" * width)
        print("1-6: Intel actions | Esc: Back | ?: Help")
    
    def _create_progress_bar(self, value: int, length: int = 10) -> str:
        """Create a visual progress bar"""
        filled = int((value / 100) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    def get_navigation_summary(self) -> Dict[str, Any]:
        """Get navigation system summary"""
        return {
            "current_pane": self.current_pane,
            "multi_pane_mode": self.multi_pane_mode,
            "selected_index": self.selected_index,
            "navigation_stack": self.escape_stack.copy(),
            "number_navigation": self.number_navigation
        } 