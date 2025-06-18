#!/usr/bin/env python3
"""
Years of Lead - DF-Style Interface Demo

This script demonstrates the new Dwarf Fortress-style navigation improvements:
- Single-key hotkeys throughout the interface
- Context-sensitive help (? key) 
- Query mode for detailed object inspection (* key)
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_demo_header():
    """Print the demo introduction"""
    header = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                      🎮 YEARS OF LEAD: DF-STYLE INTERFACE DEMO                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  🎯 NEW FEATURES IMPLEMENTED:                                                    ║
║                                                                                  ║
║  ⚡ SINGLE-KEY HOTKEYS                                                           ║
║     • [A] Advance  [G] Agents   [N] Narrative  [T] Tasks                       ║
║     • [L] Locations [E] Events  [M] Missions   [C] Create                      ║
║     • [R] Recruit  [X] Execute  [P] Politics   [Q] Quit                        ║
║     • [?] Help     [*] Query Mode                                               ║
║                                                                                  ║
║  📖 CONTEXT-SENSITIVE HELP                                                      ║
║     • Press [?] anywhere for relevant help                                      ║
║     • Different help for each screen/context                                    ║
║     • Includes navigation tips and command explanations                         ║
║                                                                                  ║
║  🔍 QUERY MODE (DF-STYLE INSPECTION)                                            ║
║     • Press [*] to toggle query mode                                            ║
║     • Type any object name to inspect instantly                                 ║
║     • Deep dive into agents, locations, factions                                ║
║     • System queries: skills, trauma, coordination, etc.                        ║
║                                                                                  ║
║  📍 BREADCRUMB NAVIGATION                                                       ║
║     • Shows your current path in nested menus                                   ║
║     • Easy to see where you are in the interface                                ║
║                                                                                  ║
║  🎨 ENHANCED VISUAL DESIGN                                                      ║
║     • Progress bars for security/unrest levels                                  ║
║     • Star ratings for skills (★★★☆☆)                                          ║
║     • Color-coded status indicators                                             ║
║     • Structured tables and clear layouts                                       ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

🎮 DEMO INSTRUCTIONS:
1. Launch the game normally: python main.py --mode cli
2. Try the new single-key commands (just press the letter + Enter)
3. Press [?] in any screen to see context help
4. Press [*] to toggle query mode, then type object names
5. In agent screen, try typing agent names or "skills" or "trauma"
6. Notice the enhanced visual feedback and navigation aids

🔥 DF PLAYER TIPS:
• The interface now has the navigation efficiency you expect
• Query mode works like DF's 'q' key - inspect anything instantly
• Context help eliminates the need to memorize commands
• Single-key navigation makes complex operations much faster
• Enhanced information density with visual organization

Ready to experience the improved interface? Launch with:
    python main.py --mode cli

OR use the enhanced CLI launcher:
    python cli_main_menu.py
"""
    print(header)

def demonstrate_features():
    """Show specific examples of the new features"""
    print("\n🔍 QUERY MODE EXAMPLES:")
    print("━" * 50)
    print("When query mode is active, you can type:")
    print("• Agent names: 'maria', 'chen', 'dmitri'")
    print("• Location names: 'university', 'downtown', 'factory'") 
    print("• System queries:")
    print("  - 'skills'       → Complete skills reference")
    print("  - 'trauma'       → Psychological trauma system")
    print("  - 'coordination' → Mission coordination mechanics")
    print("  - 'roles'        → Agent role descriptions")
    print("  - 'difficulty'   → Mission difficulty factors")
    print("  - 'equipment'    → Equipment system overview")
    
    print("\n⚡ SINGLE-KEY NAVIGATION:")
    print("━" * 50)
    print("Just press the key + Enter (no more typing full words):")
    print("G → Agent details    M → Missions      T → Task assignment")
    print("L → Locations        E → Events        C → Create mission")
    print("A → Advance turn     P → Public opinion Q → Quit")
    print("? → Context help     * → Query mode")
    
    print("\n📖 CONTEXT HELP EXAMPLES:")
    print("━" * 50)
    print("Press [?] in different screens to see:")
    print("• Main menu: Complete command reference + navigation tips")
    print("• Agent screen: Agent management help + query commands")
    print("• Mission screen: Mission system help + coordination guide")
    print("• Always relevant to your current context!")
    
    print("\n🎨 VISUAL IMPROVEMENTS:")
    print("━" * 50)
    print("Enhanced displays include:")
    print("• Security bars: [████████░░] 8/10")
    print("• Skill ratings: Combat ★★★★☆ (8/10)")
    print("• Status icons: 🟢 Active  🟡 Stressed  🔴 Captured")
    print("• Priority levels: 🔥 Urgent  ⚡ Normal  📝 Low")
    print("• Stress warnings: ⚠️ HIGH STRESS when agents are overworked")

def show_comparison():
    """Show before/after comparison"""
    print("\n📊 BEFORE vs AFTER COMPARISON:")
    print("═" * 60)
    
    print("\n🔴 OLD INTERFACE:")
    print("• Had to type full commands: 'agents', 'missions', 'addtask'")
    print("• No context help - had to remember everything")
    print("• Limited object inspection")
    print("• Plain text displays")
    print("• No query system")
    
    print("\n🟢 NEW DF-STYLE INTERFACE:")
    print("• Single-key commands: G, M, T")
    print("• Context-sensitive help with ?")
    print("• Deep object inspection with query mode")
    print("• Rich visual displays with bars, stars, icons")
    print("• Instant access to any information")
    
    print("\n🏆 DF PLAYER RATING IMPROVEMENT:")
    print("Navigation Efficiency:  C+ → A    (Single-key hotkeys)")
    print("Context Sensitivity:    C  → A-   (? help system)")
    print("Information Access:     B  → A    (Query mode)")
    print("Visual Organization:    A- → A    (Enhanced displays)")
    print("OVERALL:                ⭐⭐⭐⭐ → ⭐⭐⭐⭐⭐")

def main():
    """Run the demo"""
    print_demo_header()
    
    choice = input("\nWould you like to see detailed feature examples? (y/n): ").strip().lower()
    if choice == 'y':
        demonstrate_features()
        show_comparison()
    
    print("\n" + "="*60)
    print("🚀 READY TO EXPERIENCE THE ENHANCED INTERFACE?")
    print("="*60)
    print("Launch the game with:")
    print("  python main.py --mode cli")
    print("\nOr use the main menu:")
    print("  python cli_main_menu.py")
    print("\nHappy commanding, operative! 🎮")

if __name__ == "__main__":
    main() 