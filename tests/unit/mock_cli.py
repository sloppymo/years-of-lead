"""
Enhanced Mock CLI class for comprehensive testing purposes.
"""
from unittest.mock import MagicMock
import sys
import json
from datetime import datetime

class MenuItem:
    """Menu item class for CLI navigation"""
    
    def __init__(self, key, label, description, action):
        """Initialize a menu item"""
        self.key = key
        self.label = label
        self.description = description
        self.action = action
        self.selected = False
        self.position = (0, 0)  # (row, col)

class MockCLI:
    """Enhanced mock version of GameCLI for comprehensive E2E testing"""
    
    def __init__(self, config=None):
        """Initialize the mock CLI with optional configuration"""
        self.selected_index = 0
        self.saves = []
        self.victory = False
        self.defeat = False
        self.turns_advanced = 0
        self.save_metadata = {}
        
        # Enhanced game state tracking
        self.game_state = {
            'turn': 0,
            'agents': 3,
            'public_support': 50,
            'resources': 100,
            'locations_controlled': 1,
            'enemy_strength': 75,
            'events_active': [],
            'missions_completed': 0,
            'agents_wounded': 0,
            'agents_killed': 0
        }
        
        # Statistics tracking
        self.statistics = {
            'commands_executed': 0,
            'saves_created': 0,
            'saves_loaded': 0,
            'saves_deleted': 0,
            'errors_encountered': 0,
            'session_start_time': datetime.now()
        }
        
        # Configuration options
        self.config = config or {
            'auto_save': True,
            'auto_save_interval': 5,
            'max_saves': 10,
            'debug_mode': False,
            'simulation_speed': 'normal'
        }
        
        # Enhanced menu system with categories
        self.current_menu_items = [
            # Core Game Actions
            MenuItem("a", "advance", "Advance Turn", self.advance_turn),
            MenuItem("g", "agents", "Show Agents", self.show_agent_details),
            
            # Save/Load System
            MenuItem("s", "save", "Save/Load Menu", self.save_load_menu),
            
            # Equipment & Inventory
            MenuItem("u", "equipment", "Equipment Menu", self.equipment_menu),
            MenuItem("i", "inventory", "Inventory Menu", self.inventory_menu),
            
            # Mission & Events
            MenuItem("m", "missions", "Mission Menu", self.mission_menu),
            MenuItem("e", "events", "Events", self.events_view),
            
            # Character & Relationships
            MenuItem("c", "character", "Character Creation", self.character_menu),
            MenuItem("r", "relationships", "Relationships Menu", self.relationships_menu),
            
            # Narrative & Information
            MenuItem("y", "narrative", "Narrative Menu", self.narrative_menu),
            MenuItem("n", "narrative_log", "Narrative Log", self.narrative_log),
            MenuItem("l", "location", "Location Details", self.location_details),
            
            # Victory/Defeat Conditions
            MenuItem("v", "victory", "Victory", self.victory_action),
            MenuItem("d", "defeat", "Defeat", self.defeat_action),
            
            # Detection & Security
            MenuItem("t", "detection", "Detection", self.detection_menu),
            
            # Public Opinion & Economy
            MenuItem("p", "public_opinion", "Public Opinion", self.public_opinion),
            
            # System Commands
            MenuItem("?", "help", "Help System", self.display_menu),
            MenuItem("*", "query", "Query Mode", self.display_header),
            MenuItem("q", "quit", "Quit Game", self.quit_action),
        ]
        
        self.current_menu_items[0].selected = True
        
        # Set positions for menu items (for mouse navigation)
        for i, item in enumerate(self.current_menu_items):
            item.position = (i + 4, 2)
        
        # Initialize game state
        self._initialize_game_state()
    
    def _initialize_game_state(self):
        """Initialize the game state with realistic starting values"""
        self.game_state.update({
            'turn': 1,
            'agents': 3,
            'public_support': 45,
            'resources': 100,
            'locations_controlled': 1,
            'enemy_strength': 75,
            'events_active': ['Initial Setup'],
            'missions_completed': 0,
            'agents_wounded': 0,
            'agents_killed': 0
        })
    
    def _update_statistics(self, action_type):
        """Update statistics based on actions performed"""
        self.statistics['commands_executed'] += 1
        if action_type == 'save_created':
            self.statistics['saves_created'] += 1
        elif action_type == 'save_loaded':
            self.statistics['saves_loaded'] += 1
        elif action_type == 'save_deleted':
            self.statistics['saves_deleted'] += 1
        elif action_type == 'error':
            self.statistics['errors_encountered'] += 1
    
    def _check_victory_conditions(self):
        """Check if victory conditions are met"""
        conditions = {
            'public_support': self.game_state['public_support'] >= 75,
            'locations_controlled': self.game_state['locations_controlled'] >= 3,
            'enemy_strength': self.game_state['enemy_strength'] <= 25
        }
        return all(conditions.values()), conditions
    
    def _check_defeat_conditions(self):
        """Check if defeat conditions are met"""
        conditions = {
            'public_support': self.game_state['public_support'] <= 15,
            'agents_remaining': self.game_state['agents'] <= 1,
            'resources': self.game_state['resources'] <= 10
        }
        return any(conditions.values()), conditions
    
    def _simulate_turn_events(self):
        """Simulate random events that occur during turn advancement"""
        import random
        
        events = []
        
        # Random public support change
        support_change = random.randint(-5, 8)
        self.game_state['public_support'] = max(0, min(100, self.game_state['public_support'] + support_change))
        
        # Random resource change
        resource_change = random.randint(-10, 15)
        self.game_state['resources'] = max(0, self.game_state['resources'] + resource_change)
        
        # Random enemy strength change
        enemy_change = random.randint(-3, 5)
        self.game_state['enemy_strength'] = max(0, min(100, self.game_state['enemy_strength'] + enemy_change))
        
        # Random events
        if random.random() < 0.3:  # 30% chance of event
            possible_events = [
                "Agent wounded in action",
                "New intelligence gathered",
                "Public demonstration",
                "Enemy counter-attack",
                "Resource discovery"
            ]
            event = random.choice(possible_events)
            events.append(event)
            
            if "wounded" in event.lower():
                self.game_state['agents_wounded'] += 1
            elif "intelligence" in event.lower():
                self.game_state['enemy_strength'] = max(0, self.game_state['enemy_strength'] - 2)
            elif "demonstration" in event.lower():
                self.game_state['public_support'] = min(100, self.game_state['public_support'] + 3)
        
        return events
    
    def advance_turn(self):
        """Enhanced advance turn with realistic game progression"""
        output = []
        output.append("Advancing turn...")
        
        # Update game state
        self.game_state['turn'] += 1
        self.turns_advanced += 1
        
        # Simulate turn events
        events = self._simulate_turn_events()
        
        # Generate turn summary
        output.append(f"Turn {self.game_state['turn']} completed")
        output.append(f"Public Support: {self.game_state['public_support']}%")
        output.append(f"Resources: {self.game_state['resources']}")
        output.append(f"Enemy Strength: {self.game_state['enemy_strength']}%")
        output.append(f"Agents: {self.game_state['agents']} (Wounded: {self.game_state['agents_wounded']})")
        
        if events:
            output.append("Events this turn:")
            for event in events:
                output.append(f"  - {event}")
        
        # Check victory/defeat conditions
        victory_met, victory_conditions = self._check_victory_conditions()
        defeat_met, defeat_conditions = self._check_defeat_conditions()
        
        if victory_met:
            self.victory = True
            output.append("🎉 VICTORY ACHIEVED! 🎉")
            output.append("All victory conditions met!")
            output.append("Game Over - Victory")
        elif defeat_met:
            self.defeat = True
            output.append("💀 DEFEAT SUFFERED! 💀")
            output.append("Defeat conditions triggered!")
            output.append("Game Over - Defeat")
        
        # Auto-save if enabled
        if self.config['auto_save'] and self.turns_advanced % self.config['auto_save_interval'] == 0:
            auto_save_name = f"autosave_turn_{self.game_state['turn']}"
            self.saves.append(auto_save_name)
            self.save_metadata[auto_save_name] = self._get_save_metadata()
            output.append(f"Auto-save created: {auto_save_name}")
        
        self._update_statistics('turn_advanced')
        return "\n".join(output), True
    
    def _get_save_metadata(self):
        """Generate comprehensive save metadata"""
        return {
            "turn": self.game_state['turn'],
            "agents": self.game_state['agents'],
            "public_support": self.game_state['public_support'],
            "resources": self.game_state['resources'],
            "enemy_strength": self.game_state['enemy_strength'],
            "locations_controlled": self.game_state['locations_controlled'],
            "missions_completed": self.game_state['missions_completed'],
            "save_timestamp": datetime.now().isoformat(),
            "game_version": "1.0.0"
        }
    
    def show_agent_details(self):
        """Enhanced agent details with comprehensive information"""
        output = []
        output.append("=== AGENT DETAILS ===")
        output.append(f"Total Agents: {self.game_state['agents']}")
        output.append(f"Active Agents: {self.game_state['agents'] - self.game_state['agents_wounded']}")
        output.append(f"Wounded Agents: {self.game_state['agents_wounded']}")
        output.append(f"Killed Agents: {self.game_state['agents_killed']}")
        output.append("")
        output.append("Agent Status:")
        for i in range(self.game_state['agents']):
            status = "Wounded" if i < self.game_state['agents_wounded'] else "Active"
            output.append(f"  Agent {i+1}: {status}")
        output.append("")
        output.append("Agent: Test Agent")
        return "\n".join(output), True
    
    def save_load_menu(self):
        """Enhanced save/load menu with comprehensive functionality"""
        output = []
        output.append("=== SAVE/LOAD MENU ===")
        output.append("1. Save Game")
        output.append("2. Load Game")
        output.append("3. Delete Save")
        output.append("4. Save Statistics")
        output.append("5. View Save Metadata")
        output.append("6. Back to Main Menu")
        output.append("")
        output.append("Available saves:")
        
        if not self.saves:
            output.append("  No saves available")
        else:
            for i, save in enumerate(self.saves, 1):
                metadata = self.save_metadata.get(save, {})
                turn = metadata.get('turn', 'Unknown')
                timestamp = metadata.get('save_timestamp', 'Unknown')
                output.append(f"  {i}. {save} (Turn {turn})")
        
        output.append("")
        output.append("Select option (1-6):")
        
        # Simulate save operation
        save_name = f"save_turn_{self.game_state['turn']}"
        self.saves.append(save_name)
        self.save_metadata[save_name] = self._get_save_metadata()
        output.append(f"Saving game as '{save_name}'")
        output.append("Save completed successfully!")
        
        self._update_statistics('save_created')
        return "\n".join(output), True
    
    def equipment_menu(self):
        """Enhanced equipment menu with comprehensive gear management"""
        output = []
        output.append("=== EQUIPMENT MENU ===")
        output.append("Available Equipment Categories:")
        output.append("1. Weapons")
        output.append("2. Armor")
        output.append("3. Tools")
        output.append("4. Communication")
        output.append("5. Medical")
        output.append("6. Back to Main Menu")
        output.append("")
        output.append("Current Equipment Loadout:")
        output.append("  Primary Weapon: Pistol")
        output.append("  Secondary Weapon: Knife")
        output.append("  Armor: Light Vest")
        output.append("  Tools: Lockpick Set")
        output.append("  Communication: Radio")
        output.append("  Medical: First Aid Kit")
        output.append("")
        output.append("Equipment Status: Fully Equipped")
        output.append("Equipment Quality: Standard")
        return "\n".join(output), True
    
    def inventory_menu(self):
        """Enhanced inventory menu with item management"""
        output = []
        output.append("=== INVENTORY MENU ===")
        output.append("Current Inventory:")
        output.append("  Ammunition: 150 rounds")
        output.append("  Medical Supplies: 5 units")
        output.append("  Explosives: 2 units")
        output.append("  Intel Documents: 3 files")
        output.append("  Money: $2,500")
        output.append("  Food: 10 days supply")
        output.append("")
        output.append("Inventory Weight: 45/100 kg")
        output.append("Storage Capacity: 55 kg remaining")
        output.append("")
        output.append("Actions:")
        output.append("1. Use Item")
        output.append("2. Drop Item")
        output.append("3. Trade Items")
        output.append("4. Back to Main Menu")
        return "\n".join(output), True
    
    def mission_menu(self):
        """Enhanced mission menu with mission management"""
        output = []
        output.append("=== MISSION MENU ===")
        output.append("Available Missions:")
        output.append("1. Intelligence Gathering")
        output.append("2. Sabotage Operation")
        output.append("3. Rescue Mission")
        output.append("4. Infiltration")
        output.append("5. Assassination")
        output.append("")
        output.append("Active Missions: 0")
        output.append("Completed Missions: 0")
        output.append("Failed Missions: 0")
        output.append("")
        output.append("Mission Statistics:")
        output.append(f"  Success Rate: {self.game_state['missions_completed']}%")
        output.append("  Average Completion Time: 3 turns")
        output.append("  Risk Level: Medium")
        return "\n".join(output), True
    
    def events_view(self):
        """Enhanced events view with comprehensive event tracking"""
        output = []
        output.append("=== EVENTS LOG ===")
        output.append("Recent Events:")
        output.append("  Turn 1: Initial Setup")
        output.append("  Turn 2: Agent deployed")
        output.append("  Turn 3: Intelligence gathered")
        output.append("")
        output.append("Active Events:")
        for event in self.game_state['events_active']:
            output.append(f"  - {event}")
        output.append("")
        output.append("Event Statistics:")
        output.append("  Total Events: 3")
        output.append("  Positive Events: 2")
        output.append("  Negative Events: 1")
        output.append("  Neutral Events: 0")
        return "\n".join(output), True
    
    def character_menu(self):
        """Enhanced character creation and management"""
        output = []
        output.append("=== CHARACTER CREATION ===")
        output.append("Current Character:")
        output.append("  Name: Agent X")
        output.append("  Role: Infiltrator")
        output.append("  Skills: Stealth, Lockpicking, Combat")
        output.append("  Experience: 150 points")
        output.append("  Level: 3")
        output.append("")
        output.append("Character Statistics:")
        output.append("  Health: 100/100")
        output.append("  Stamina: 85/100")
        output.append("  Morale: 75/100")
        output.append("  Reputation: 60/100")
        output.append("")
        output.append("Available Actions:")
        output.append("1. Train Skills")
        output.append("2. Rest and Recover")
        output.append("3. Change Role")
        output.append("4. View Background")
        return "\n".join(output), True
    
    def relationships_menu(self):
        """Enhanced relationships menu with faction management"""
        output = []
        output.append("=== RELATIONSHIPS MENU ===")
        output.append("Faction Relationships:")
        output.append("  Resistance: Allied (100%)")
        output.append("  Government: Hostile (0%)")
        output.append("  Corporations: Neutral (50%)")
        output.append("  Civilians: Friendly (75%)")
        output.append("  Media: Cautious (40%)")
        output.append("")
        output.append("Individual Contacts:")
        output.append("  Commander: Trusted")
        output.append("  Informant: Reliable")
        output.append("  Trader: Neutral")
        output.append("  Enemy Agent: Hostile")
        output.append("")
        output.append("Relationship Actions:")
        output.append("1. Improve Relations")
        output.append("2. Sabotage Relations")
        output.append("3. Negotiate")
        output.append("4. View History")
        return "\n".join(output), True
    
    def narrative_menu(self):
        """Enhanced narrative menu with story elements"""
        output = []
        output.append("=== NARRATIVE MENU ===")
        output.append("Story Elements:")
        output.append("  Main Plot: Resistance Movement")
        output.append("  Subplot: Internal Betrayal")
        output.append("  Theme: Freedom vs Control")
        output.append("")
        output.append("Current Chapter: Act 1 - Awakening")
        output.append("Story Progress: 25%")
        output.append("")
        output.append("Narrative Choices:")
        output.append("1. View Story Log")
        output.append("2. Make Story Choice")
        output.append("3. View Character Arcs")
        output.append("4. Explore World Lore")
        output.append("")
        output.append("Recent Story Events:")
        output.append("  - Joined the resistance")
        output.append("  - First mission completed")
        output.append("  - Discovered government plot")
        return "\n".join(output), True
    
    def narrative_log(self):
        """Enhanced narrative log with detailed story tracking"""
        output = []
        output.append("=== NARRATIVE LOG ===")
        output.append("Story Timeline:")
        output.append("  Day 1: Awakening to the truth")
        output.append("  Day 2: First contact with resistance")
        output.append("  Day 3: Training and preparation")
        output.append("  Day 4: First mission briefing")
        output.append("  Day 5: Mission execution")
        output.append("")
        output.append("Character Development:")
        output.append("  - Learned about government corruption")
        output.append("  - Developed combat skills")
        output.append("  - Built trust with resistance")
        output.append("  - Faced moral dilemmas")
        output.append("")
        output.append("World Events:")
        output.append("  - Government crackdown begins")
        output.append("  - Resistance cells activate")
        output.append("  - Civil unrest spreads")
        output.append("  - Media censorship increases")
        return "\n".join(output), True
    
    def location_details(self):
        """Enhanced location details with comprehensive information"""
        output = []
        output.append("=== LOCATION DETAILS ===")
        output.append("Current Location: Safe House Alpha")
        output.append("Location Type: Resistance Base")
        output.append("Security Level: High")
        output.append("")
        output.append("Location Features:")
        output.append("  - Armory: Fully stocked")
        output.append("  - Medical Bay: Operational")
        output.append("  - Communication Center: Active")
        output.append("  - Training Facility: Available")
        output.append("  - Storage: 75% capacity")
        output.append("")
        output.append("Surrounding Areas:")
        output.append("  - Downtown District: Government controlled")
        output.append("  - Industrial Zone: Corporate territory")
        output.append("  - Residential Area: Civilian population")
        output.append("  - Military Base: High security")
        output.append("")
        output.append("Location Status: Secure")
        output.append("Evacuation Routes: 3 available")
        return "\n".join(output), True
    
    def victory_action(self):
        """Enhanced victory action with comprehensive victory conditions"""
        output = []
        output.append("=== VICTORY CONDITIONS ===")
        output.append("Victory Requirements:")
        output.append("  ✓ Public Support: 75% or higher")
        output.append("  ✓ Locations Controlled: 3 or more")
        output.append("  ✓ Enemy Strength: 25% or lower")
        output.append("")
        output.append("Current Progress:")
        victory_met, conditions = self._check_victory_conditions()
        for condition, met in conditions.items():
            status = "✓" if met else "✗"
            if condition == 'public_support':
                output.append(f"  {status} Public Support: {self.game_state['public_support']}% (need 75%)")
            elif condition == 'locations_controlled':
                output.append(f"  {status} Locations Controlled: {self.game_state['locations_controlled']} (need 3)")
            elif condition == 'enemy_strength':
                output.append(f"  {status} Enemy Strength: {self.game_state['enemy_strength']}% (need ≤25%)")
        
        if victory_met:
            output.append("")
            output.append("🎉 VICTORY ACHIEVED! 🎉")
            output.append("All conditions met!")
        else:
            output.append("")
            output.append("Victory not yet achieved.")
            output.append("Continue working toward liberation!")
        
        return "\n".join(output), True
    
    def defeat_action(self):
        """Enhanced defeat action with comprehensive defeat conditions"""
        output = []
        output.append("=== DEFEAT CONDITIONS ===")
        output.append("Defeat Triggers:")
        output.append("  ✗ Public Support: 15% or lower")
        output.append("  ✗ Agents Remaining: 1 or fewer")
        output.append("  ✗ Resources: 10 or fewer")
        output.append("")
        output.append("Current Status:")
        defeat_met, conditions = self._check_defeat_conditions()
        for condition, met in conditions.items():
            status = "✗" if met else "✓"
            if condition == 'public_support':
                output.append(f"  {status} Public Support: {self.game_state['public_support']}% (safe above 15%)")
            elif condition == 'agents_remaining':
                output.append(f"  {status} Agents Remaining: {self.game_state['agents']} (safe above 1)")
            elif condition == 'resources':
                output.append(f"  {status} Resources: {self.game_state['resources']} (safe above 10)")
        
        if defeat_met:
            output.append("")
            output.append("💀 DEFEAT SUFFERED! 💀")
            output.append("Defeat conditions triggered!")
        else:
            output.append("")
            output.append("Defeat avoided for now.")
            output.append("Stay vigilant and maintain support!")
        
        return "\n".join(output), True
    
    def detection_menu(self):
        """Enhanced detection menu with security and stealth mechanics"""
        output = []
        output.append("=== DETECTION & SECURITY ===")
        output.append("Current Detection Level: 15%")
        output.append("Security Status: Low Alert")
        output.append("")
        output.append("Detection Factors:")
        output.append("  - Agent Activity: +5%")
        output.append("  - Public Attention: +3%")
        output.append("  - Enemy Intelligence: +7%")
        output.append("  - Stealth Measures: -10%")
        output.append("")
        output.append("Security Measures Active:")
        output.append("  ✓ Identity Protection")
        output.append("  ✓ Communication Encryption")
        output.append("  ✓ Safe House Security")
        output.append("  ✓ Agent Dispersal")
        output.append("")
        output.append("Risk Assessment:")
        output.append("  - Immediate Risk: Low")
        output.append("  - Short-term Risk: Medium")
        output.append("  - Long-term Risk: High")
        output.append("")
        output.append("Recommended Actions:")
        output.append("1. Increase Stealth")
        output.append("2. Reduce Activity")
        output.append("3. Improve Security")
        output.append("4. Evacuate if needed")
        return "\n".join(output), True
    
    def public_opinion(self):
        """Enhanced public opinion with comprehensive tracking"""
        output = []
        output.append("=== PUBLIC OPINION ===")
        output.append(f"Current Public Support: {self.game_state['public_support']}%")
        output.append("")
        output.append("Support by Demographics:")
        output.append("  - Working Class: 65%")
        output.append("  - Middle Class: 45%")
        output.append("  - Upper Class: 25%")
        output.append("  - Youth (18-30): 70%")
        output.append("  - Elderly (60+): 35%")
        output.append("")
        output.append("Support by Region:")
        output.append("  - Urban Areas: 55%")
        output.append("  - Suburban Areas: 45%")
        output.append("  - Rural Areas: 40%")
        output.append("")
        output.append("Recent Changes:")
        output.append("  +5% from successful mission")
        output.append("  -2% from government propaganda")
        output.append("  +3% from media coverage")
        output.append("")
        output.append("Opinion Influencers:")
        output.append("  - Media Coverage: Moderate")
        output.append("  - Government Actions: Negative")
        output.append("  - Resistance Success: Positive")
        output.append("  - Economic Conditions: Neutral")
        return "\n".join(output), True
    
    def quit_action(self):
        """Quit the game"""
        return "Quit Game", True
    
    def _handle_arrow_key(self, direction):
        """Handle arrow key navigation"""
        if direction == "up":
            # Move selection up
            self.current_menu_items[self.selected_index].selected = False
            self.selected_index = (self.selected_index - 1) % len(self.current_menu_items)
            self.current_menu_items[self.selected_index].selected = True
            return "navigation"
        elif direction == "down":
            # Move selection down
            self.current_menu_items[self.selected_index].selected = False
            self.selected_index = (self.selected_index + 1) % len(self.current_menu_items)
            self.current_menu_items[self.selected_index].selected = True
            return "navigation"
        elif direction == "enter":
            # Execute the selected action
            return self.current_menu_items[self.selected_index].action()
        return None
    
    def _handle_mouse_click(self, col, row):
        """Handle mouse click navigation"""
        for i, item in enumerate(self.current_menu_items):
            if item.position == (row, col):
                # Select this item
                self.current_menu_items[self.selected_index].selected = False
                self.selected_index = i
                self.current_menu_items[self.selected_index].selected = True
                # Execute the action
                return self.current_menu_items[self.selected_index].action()
        return None
    
    def display_menu(self):
        """Enhanced help system with comprehensive command listing"""
        output = []
        output.append("=== HELP SYSTEM ===")
        output.append("Available commands:")
        output.append("")
        
        # Group commands by category
        categories = {
            "Core Game Actions": ["a", "g"],
            "Save/Load System": ["s"],
            "Equipment & Inventory": ["u", "i"],
            "Mission & Events": ["m", "e"],
            "Character & Relationships": ["c", "r"],
            "Narrative & Information": ["y", "n", "l"],
            "Victory/Defeat Conditions": ["v", "d"],
            "Detection & Security": ["t"],
            "Public Opinion & Economy": ["p"],
            "System Commands": ["?", "*", "q"]
        }
        
        for category, keys in categories.items():
            output.append(f"{category}:")
            for key in keys:
                for item in self.current_menu_items:
                    if item.key == key:
                        output.append(f"  {key}: {item.description}")
                        break
            output.append("")
        
        output.append("Navigation Tips:")
        output.append("  - Use single letters for quick access")
        output.append("  - Press '?' for help anytime")
        output.append("  - Press '*' for query mode")
        output.append("  - Press 'q' to quit")
        output.append("")
        output.append("Game Statistics:")
        output.append(f"  Commands executed: {self.statistics['commands_executed']}")
        output.append(f"  Session duration: {self._get_session_duration()}")
        output.append(f"  Errors encountered: {self.statistics['errors_encountered']}")
        
        return "\n".join(output), True
    
    def display_header(self):
        """Enhanced query mode with comprehensive system information"""
        output = []
        output.append("Query Mode: ON")
        output.append("RESISTANCE COMMAND CENTER")
        output.append("")
        output.append("=== SYSTEM QUERY ===")
        output.append("Game State Information:")
        output.append(f"  Turn: {self.game_state['turn']}")
        output.append(f"  Public Support: {self.game_state['public_support']}%")
        output.append(f"  Resources: {self.game_state['resources']}")
        output.append(f"  Enemy Strength: {self.game_state['enemy_strength']}%")
        output.append(f"  Agents: {self.game_state['agents']}")
        output.append(f"  Locations Controlled: {self.game_state['locations_controlled']}")
        output.append("")
        output.append("System Information:")
        output.append(f"  Auto-save: {'Enabled' if self.config['auto_save'] else 'Disabled'}")
        output.append(f"  Auto-save interval: {self.config['auto_save_interval']} turns")
        output.append(f"  Max saves: {self.config['max_saves']}")
        output.append(f"  Debug mode: {'Enabled' if self.config['debug_mode'] else 'Disabled'}")
        output.append(f"  Simulation speed: {self.config['simulation_speed']}")
        output.append("")
        output.append("Performance Metrics:")
        output.append(f"  Commands executed: {self.statistics['commands_executed']}")
        output.append(f"  Saves created: {self.statistics['saves_created']}")
        output.append(f"  Saves loaded: {self.statistics['saves_loaded']}")
        output.append(f"  Saves deleted: {self.statistics['saves_deleted']}")
        output.append(f"  Errors: {self.statistics['errors_encountered']}")
        
        return "\n".join(output), True
    
    def _get_session_duration(self):
        """Calculate session duration"""
        duration = datetime.now() - self.statistics['session_start_time']
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        return f"{minutes}m {seconds}s"
    
    def _handle_error(self, error_type, error_message):
        """Handle errors and update statistics"""
        self.statistics['errors_encountered'] += 1
        if self.config['debug_mode']:
            print(f"ERROR [{error_type}]: {error_message}")
    
    def _validate_input(self, user_input):
        """Validate user input and return appropriate response"""
        if not user_input or not user_input.strip():
            return "Invalid command", False
        
        user_input = user_input.strip().lower()
        
        # Check for valid commands
        valid_commands = [item.key for item in self.current_menu_items]
        if user_input not in valid_commands:
            return f"Invalid command: '{user_input}'", False
        
        return user_input, True
    
    def _execute_command(self, command):
        """Execute a command and return the result"""
        try:
            for item in self.current_menu_items:
                if item.key == command:
                    result = item.action()
                    self._update_statistics('command_executed')
                    return result, True
            return "Command not found", False
        except Exception as e:
            self._handle_error("Command Execution", str(e))
            return f"Error executing command: {str(e)}", False
    
    def run(self):
        """Enhanced run loop with comprehensive error handling and statistics"""
        print("RESISTANCE COMMAND CENTER")
        print("Enhanced CLI v2.0 - Type '?' for help, 'q' to quit")
        print("=" * 50)
        
        while True:
            try:
                # Display current game status
                if self.config['debug_mode']:
                    print(f"\n[DEBUG] Turn: {self.game_state['turn']}, Support: {self.game_state['public_support']}%")
                
                # Get user input
                try:
                    user_input = input("> ")
                except EOFError:
                    print("Session ended by user")
                    break
                except KeyboardInterrupt:
                    print("\nSession interrupted")
                    break
                
                # Validate input
                validated_input, is_valid = self._validate_input(user_input)
                if not is_valid:
                    print(validated_input)
                    continue
                
                # Handle special commands
                if validated_input == 'q':
                    print('Quit Game')
                    print(f"Session Statistics: {self.statistics['commands_executed']} commands executed")
                    break
                elif validated_input == '?':
                    result = self.display_menu()
                    if result:
                        print(result)
                elif validated_input == '*':
                    result = self.display_header()
                    if result:
                        print(result)
                else:
                    # Execute regular command
                    result, success = self._execute_command(validated_input)
                    if result:
                        print(result)
                    if not success:
                        self._handle_error("Command Failure", f"Failed to execute: {validated_input}")
                
                # Check for game end conditions
                if self.victory:
                    print("\n🎉 VICTORY ACHIEVED! 🎉")
                    print("Game Over - Victory")
                    break
                elif self.defeat:
                    print("\n💀 DEFEAT SUFFERED! 💀")
                    print("Game Over - Defeat")
                    break
                
            except Exception as e:
                self._handle_error("Runtime Error", str(e))
                print(f"An error occurred: {str(e)}")
                continue
        
        # Final statistics
        print(f"\nSession Summary:")
        print(f"  Commands executed: {self.statistics['commands_executed']}")
        print(f"  Session duration: {self._get_session_duration()}")
        print(f"  Errors encountered: {self.statistics['errors_encountered']}")
        print(f"  Saves created: {self.statistics['saves_created']}")
        print("Thank you for playing Years of Lead!")

# Alias for compatibility with existing tests
GameCLI = MockCLI 