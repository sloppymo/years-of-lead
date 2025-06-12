#!/usr/bin/env python3
"""
Test script for Years of Lead GUI
Simple test to verify the GUI launches correctly
"""

import sys
import os
import pytest

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

pytest.skip(
    "Legacy interactive GUI demo – excluded from automated test run",
    allow_module_level=True,
)


def test_gui_import():
    """Test that GUI modules can be imported"""
    try:
        from gui.main_gui import YearsOfLeadGUI

        # Verify import was successful
        assert YearsOfLeadGUI is not None
        print("✓ GUI module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ GUI import failed: {e}")
        return False


def test_game_import():
    """Test that game modules can be imported"""
    try:
        from game.core import GameState, Agent, Faction, GamePhase, AgentStatus

        # Verify imports were successful
        assert all(
            cls is not None
            for cls in [GameState, Agent, Faction, GamePhase, AgentStatus]
        )
        print("✓ Game modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Game import failed: {e}")
        return False


def test_gui_launch():
    """Test launching the GUI"""
    try:
        from gui.main_gui import YearsOfLeadGUI

        print("🎮 Launching GUI...")
        print("Note: Close the GUI window to continue testing")

        app = YearsOfLeadGUI()
        app.run()

        print("✓ GUI launched and closed successfully")
        return True
    except Exception as e:
        print(f"❌ GUI failed to launch: {e}")
        return False


def main():
    """Run GUI tests"""
    print("🧪 Testing Years of Lead GUI...")
    print("=" * 50)

    # Test imports
    game_ok = test_game_import()
    gui_ok = test_gui_import()

    if not game_ok or not gui_ok:
        print("\n❌ Import tests failed. Cannot proceed with GUI test.")
        return False

    print("\n" + "=" * 50)
    print("🎮 GUI Import Tests Passed!")
    print("=" * 50)

    # Ask user if they want to test GUI launch
    response = input("\nDo you want to test GUI launch? (y/n): ").lower().strip()

    if response in ["y", "yes"]:
        print("\n" + "=" * 50)
        print("🚀 Launching GUI Test...")
        print("=" * 50)

        launch_ok = test_gui_launch()

        if launch_ok:
            print("\n✅ All GUI tests passed!")
            return True
        else:
            print("\n❌ GUI launch test failed!")
            return False
    else:
        print("\n✅ Import tests completed successfully!")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
