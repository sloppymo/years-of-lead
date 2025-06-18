#!/usr/bin/env python3
"""
Years of Lead - Main Entry Point
Launch the insurgency simulator in either CLI or GUI mode
"""

import sys
import os
import argparse

# Add the src directory to the path so we can import our modules
src_path = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, src_path)


def main():
    """Main entry point for Years of Lead"""
    parser = argparse.ArgumentParser(description="Years of Lead - Insurgency Simulator")
    parser.add_argument(
        "--mode",
        choices=["cli", "gui"],
        default="gui",
        help="Interface mode (default: gui)",
    )
    parser.add_argument(
        "--no-ui", action="store_true", help="Force CLI mode (legacy compatibility)"
    )

    args = parser.parse_args()

    # Determine interface mode
    if args.no_ui:
        mode = "cli"
    else:
        mode = args.mode

    print(f"🎮 Starting Years of Lead in {mode.upper()} mode...")

    if mode == "gui":
        try:
            from gui.main_gui import YearsOfLeadGUI

            print("✓ Launching GUI interface...")
            app = YearsOfLeadGUI()
            app.run()
        except ImportError as e:
            print(f"❌ GUI not available: {e}")
            print("📟 Falling back to CLI mode...")
            launch_cli()
        except Exception as e:
            print(f"❌ GUI failed to start: {e}")
            print("📟 Falling back to CLI mode...")
            launch_cli()
    else:
        launch_cli()


def launch_cli():
    """Launch the CLI interface"""
    try:
        # Import and run the existing CLI from src/main.py
        import sys
        import os

        # Add src directory to path
        src_path = os.path.join(os.path.dirname(__file__), "src")
        sys.path.insert(0, src_path)

        # Import necessary components
        from game.core import GameState

        # Initialize game state
        gs = GameState()
        gs.initialize_game()

        print("🎮 CLI interface loaded successfully!")
        print("Use Ctrl+C to exit")

        # Main game loop
        while True:
            try:
                print("\n" + "=" * 50)
                print(f"Turn {gs.turn_number} - {gs.current_phase.name}")
                print("=" * 50)

                # Show available agents
                print("\nAvailable Agents:")
                print("-" * 30)
                for agent in gs.agents.values():
                    print(f"- {agent.name} ({agent.faction_id})")

                # Advance turn (this will trigger the mission planning interface)
                input("\nPress Enter to plan next mission...")
                gs.advance_turn()

            except KeyboardInterrupt:
                print("\nExiting...")
                break

    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        print("📟 Please ensure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
