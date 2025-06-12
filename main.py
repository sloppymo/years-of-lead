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

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
        from src.main import main as cli_main

        cli_main()
    except ImportError as e:
        print(f"❌ CLI interface not found: {e}")
        print("📟 Please check that src/main.py exists and is properly configured.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ CLI interface error: {e}")
        print("📟 Falling back to basic CLI...")
        # Try to run a basic CLI
        try:
            from src.game.core import GameState

            gs = GameState()
            gs.initialize_game()
            print("🎮 Basic CLI loaded successfully!")
            print("Use Ctrl+C to exit")
            while True:
                input("Press Enter to advance turn...")
                gs.advance_turn()
                print(f"Turn {gs.turn_number} completed")
        except Exception as e2:
            print(f"❌ Basic CLI also failed: {e2}")
            sys.exit(1)


if __name__ == "__main__":
    main()
