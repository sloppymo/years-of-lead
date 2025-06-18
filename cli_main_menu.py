#!/usr/bin/env python3
"""
Years of Lead - CLI Main Menu System

A comprehensive main menu for the CLI version of Years of Lead,
featuring new game, load game, customization, and credits.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class YearsOfLeadMainMenu:
    """Main menu system for Years of Lead CLI"""
    
    def __init__(self):
        self.save_directory = Path("saves")
        self.save_directory.mkdir(exist_ok=True)
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_title_art(self):
        """Print the game title art"""
        title_art = """
██╗   ██╗███████╗ █████╗ ██████╗ ███████╗     ██████╗ ███████╗    ██╗     ███████╗ █████╗ ██████╗ 
╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝    ██╔═══██╗██╔════╝    ██║     ██╔════╝██╔══██╗██╔══██╗
 ╚████╔╝ █████╗  ███████║██████╔╝███████╗    ██║   ██║█████╗      ██║     █████╗  ███████║██║  ██║
  ╚██╔╝  ██╔══╝  ██╔══██║██╔══██╗╚════██║    ██║   ██║██╔══╝      ██║     ██╔══╝  ██╔══██║██║  ██║
   ██║   ███████╗██║  ██║██║  ██║███████║    ╚██████╔╝██║         ███████╗███████╗██║  ██║██████╔╝
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝         ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ 
                                                                                                      
                           ░░░░░ INSURGENCY SIMULATION ░░░░░
        """
        print(title_art)
    
    def print_subtitle(self):
        """Print atmospheric subtitle"""
        subtitle = """
        ┌─────────────────────────────────────────────────────────────────────────────────┐
        │                                                                                 │
        │    In the shadows of an authoritarian regime, resistance cells organize         │
        │    their fight for freedom. Every decision carries weight. Every agent          │
        │    has a story. Every mission could be the last.                                │
        │                                                                                 │
        │                        Welcome to the Years of Lead.                           │
        │                                                                                 │
        └─────────────────────────────────────────────────────────────────────────────────┘
        """
        print(subtitle)
    
    def print_main_menu(self):
        """Print the main menu options"""
        menu = """
        ╔═══════════════════════════════════════════════════════════════════════════════════╗
        ║                                   MAIN MENU                                       ║
        ╠═══════════════════════════════════════════════════════════════════════════════════╣
        ║                                                                                   ║
        ║  [1] 🆕 NEW GAME          - Start a fresh resistance campaign                     ║
        ║                                                                                   ║
        ║  [2] 💾 LOAD GAME         - Continue your struggle against oppression            ║
        ║                                                                                   ║
        ║  [3] ⚙️  CUSTOMIZE GAME    - Configure difficulty and game settings               ║
        ║                                                                                   ║
        ║  [4] 🎭 CHARACTER CREATOR - Design custom agents for the resistance              ║
        ║                                                                                   ║
        ║  [5] 📊 STATISTICS        - View campaign records and achievements               ║
        ║                                                                                   ║
        ║  [6] ℹ️  CREDITS          - Meet the team behind the simulation                   ║
        ║                                                                                   ║
        ║  [7] 📖 HELP & TUTORIAL   - Learn the basics of resistance operations           ║
        ║                                                                                   ║
        ║  [8] ❌ EXIT              - Leave the underground (quit game)                     ║
        ║                                                                                   ║
        ╚═══════════════════════════════════════════════════════════════════════════════════╝
        """
        print(menu)
    
    def new_game_menu(self):
        """Handle new game creation"""
        self.clear_screen()
        print("🆕 STARTING NEW CAMPAIGN")
        print("=" * 80)
        print()
        
        print("Select campaign type:")
        print()
        print("1. 📚 Tutorial Campaign     - Learn the basics with guided missions")
        print("2. 🎯 Standard Campaign     - Balanced challenge for experienced players") 
        print("3. 💀 Hardcore Campaign     - Maximum difficulty, permadeath enabled")
        print("4. 🎨 Custom Campaign       - Configure your own scenario")
        print("5. ← Back to Main Menu")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            self.start_standard_campaign()
        elif choice == "2":
            self.start_standard_campaign()
        elif choice == "3":
            self.start_standard_campaign()
        elif choice == "4":
            self.start_standard_campaign()
        elif choice == "5":
            return
        else:
            print("❌ Invalid choice. Please try again.")
            time.sleep(1)
            self.new_game_menu()
    
    def start_standard_campaign(self):
        """Start standard campaign"""
        print("\n🎯 STARTING CAMPAIGN")
        print("-" * 40)
        print("✓ Initializing resistance network...")
        print("✓ Setting up faction dynamics...")
        print("✓ Preparing narrative systems...")
        print()
        
        time.sleep(2)
        self.launch_cli_game()
    
    def launch_cli_game(self):
        """Launch the actual CLI game"""
        print("🚀 Launching Years of Lead...")
        print()
        
        try:
            # Import and run the CLI game
            from src.main import main as cli_main
            cli_main()
            
        except Exception as e:
            print(f"❌ Error launching game: {e}")
            print("🔄 Returning to main menu...")
            time.sleep(2)
    
    def load_game_menu(self):
        """Handle game loading"""
        self.clear_screen()
        print("💾 LOAD SAVED CAMPAIGN")
        print("=" * 80)
        print("\n❌ No saved campaigns found.")
        print("\nSave/Load functionality coming soon!")
        print("For now, start a new campaign to play.")
        input("\nPress Enter to return to main menu...")
    
    def customize_game_menu(self):
        """Handle game customization"""
        self.clear_screen()
        print("⚙️ GAME CUSTOMIZATION")
        print("=" * 80)
        print("\n⚠️ Game customization coming soon!")
        print("\nPlanned customization options:")
        print("• Difficulty settings")
        print("• Display preferences")
        print("• Audio settings")
        print("• Character defaults")
        print("• Save file management")
        input("\nPress Enter to return to main menu...")
    
    def character_creator_menu(self):
        """Launch character creator"""
        self.clear_screen()
        print("🎭 CHARACTER CREATOR")
        print("=" * 80)
        print()
        print("Design custom agents for your resistance campaigns.")
        print()
        
        try:
            # Try to import character creation
            from game.character_creation_ui import CharacterCreationUI
            
            print("Starting character creation wizard...")
            print()
            
            creator = CharacterCreationUI()
            character = creator.run_character_creation()
            
            if character:
                print(f"\n✅ Character '{character.name}' created successfully!")
                print("Character saved for use in campaigns.")
            else:
                print("\n❌ Character creation cancelled.")
                
        except Exception as e:
            print(f"❌ Character creation not available: {e}")
            print("\nFor now, characters are auto-generated in campaigns.")
        
        input("\nPress Enter to return to main menu...")
    
    def statistics_menu(self):
        """Show game statistics"""
        self.clear_screen()
        print("📊 CAMPAIGN STATISTICS")
        print("=" * 80)
        print("\n⚠️ Statistics tracking coming soon!")
        print("\nPlanned statistics:")
        print("• Total campaigns played")
        print("• Agents recruited")
        print("• Missions completed")
        print("• Success/failure rates")
        print("• Achievements unlocked")
        input("\nPress Enter to return to main menu...")
    
    def credits_menu(self):
        """Show game credits"""
        self.clear_screen()
        print("ℹ️ CREDITS")
        print("=" * 80)
        
        credits = """

        ╔═══════════════════════════════════════════════════════════════════════════════════╗
        ║                              YEARS OF LEAD                                        ║
        ║                           Insurgency Simulator                                    ║
        ╠═══════════════════════════════════════════════════════════════════════════════════╣
        ║                                                                                   ║
        ║  🎮 GAME DESIGN & DEVELOPMENT                                                     ║
        ║     Core Systems Architecture                                                     ║
        ║     Political Simulation Engine                                                   ║
        ║     Character Creation System                                                     ║
        ║     Advanced Relationship Mechanics                                               ║
        ║     Emotional State Modeling (Plutchik's 8-Emotion System)                       ║
        ║     Dynamic Narrative Generation                                                  ║
        ║                                                                                   ║
        ║  🤖 AI SYSTEMS                                                                    ║
        ║     Agent Autonomy Engine                                                         ║
        ║     Mission Execution System                                                      ║
        ║     Intelligence Analysis                                                         ║
        ║     Psychological Trauma Modeling                                                 ║
        ║                                                                                   ║
        ║  📖 NARRATIVE & WORLD BUILDING                                                    ║
        ║     Historical Research                                                           ║
        ║     Political Theory Integration                                                  ║
        ║     Symbolic Systems Design                                                       ║
        ║     Voice Configuration System                                                    ║
        ║                                                                                   ║
        ║  🔧 TECHNICAL IMPLEMENTATION                                                      ║
        ║     Python Backend Architecture                                                   ║
        ║     CLI Interface Design                                                          ║
        ║     Character Integration Systems                                                 ║
        ║     Save/Load Game Mechanics                                                      ║
        ║                                                                                   ║
        ║  🎯 SPECIAL FEATURES                                                              ║
        ║     • 10 Detailed Character Backgrounds                                           ║
        ║     • 16 Personality Traits                                                       ║
        ║     • Advanced Trauma System                                                      ║
        ║     • Sophisticated Emotional Modeling                                            ║
        ║     • Dynamic Mission Outcomes                                                    ║
        ║     • Real-time Intelligence Systems                                              ║
        ║     • Multi-agent Mission Collaboration                                           ║
        ║                                                                                   ║
        ║                        Thank you for playing Years of Lead!                      ║
        ║                                                                                   ║
        ╚═══════════════════════════════════════════════════════════════════════════════════╝
        
        """
        print(credits)
        
        input("Press Enter to return to main menu...")
    
    def help_tutorial_menu(self):
        """Show help and tutorial"""
        self.clear_screen()
        print("📖 HELP & TUTORIAL")
        print("=" * 80)
        print("\n⚠️ Help system coming soon!")
        print("\nFor now, here are the basics:")
        print()
        print("🎯 BASIC GAMEPLAY:")
        print("• Use [1] to advance turns")
        print("• Use [2] to view your agents")
        print("• Use [8] to create missions")
        print("• Use [9] to add agents to missions")
        print("• Use [10] to execute missions")
        print()
        print("🎭 CHARACTER CREATION:")
        print("• Access via main menu option [4]")
        print("• Choose background and personality")
        print("• Allocate skill points")
        print("• Characters integrate into gameplay")
        
        input("\nPress Enter to return to main menu...")
    
    def run(self):
        """Main menu loop"""
        while True:
            self.clear_screen()
            self.print_title_art()
            self.print_subtitle()
            self.print_main_menu()
            
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == "1":
                self.new_game_menu()
            elif choice == "2":
                self.load_game_menu()
            elif choice == "3":
                self.customize_game_menu()
            elif choice == "4":
                self.character_creator_menu()
            elif choice == "5":
                self.statistics_menu()
            elif choice == "6":
                self.credits_menu()
            elif choice == "7":
                self.help_tutorial_menu()
            elif choice == "8":
                print("\n👋 Thank you for fighting the good fight.")
                print("   The resistance will remember your service.")
                print()
                print("   Stay strong. Stay hidden. Stay free.")
                print()
                break
            else:
                print("\n❌ Invalid choice. Please enter a number between 1-8.")
                time.sleep(2)


def main():
    """Launch the main menu"""
    try:
        menu = YearsOfLeadMainMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Game interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please report this bug to the development team.")


if __name__ == "__main__":
    main() 