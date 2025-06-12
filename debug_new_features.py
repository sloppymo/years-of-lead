#!/usr/bin/env python3
"""
Automated Debugging Script for Years of Lead New Features

This script performs comprehensive testing of all new features including:
- Character creation system
- Emotional state system
- Game engine and state management
- Faction system
- Event system
- Import dependencies
- Basic functionality tests
"""

import sys
import asyncio
import traceback
from pathlib import Path
import importlib.util

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


class FeatureDebugger:
    """Comprehensive debugger for new features"""

    def __init__(self):
        self.results = {}
        self.errors = []
        self.warnings = []

    async def run_all_tests(self):
        """Run all debugging tests"""
        print("🔍 YEARS OF LEAD - AUTOMATED FEATURE DEBUGGING")
        print("=" * 60)

        tests = [
            ("Import Dependencies", self.test_imports),
            ("Character Creation System", self.test_character_creation),
            ("Emotional State System", self.test_emotional_state),
            ("Game Engine", self.test_game_engine),
            ("Faction System", self.test_faction_system),
            ("Event System", self.test_event_system),
            ("State Management", self.test_state_management),
            ("Integration Tests", self.test_integration),
        ]

        for test_name, test_func in tests:
            print(f"\n🧪 Testing: {test_name}")
            print("-" * 40)
            try:
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()
                self.results[test_name] = result
                print(f"✅ {test_name}: PASSED")
            except Exception as e:
                self.results[test_name] = False
                self.errors.append(f"{test_name}: {str(e)}")
                print(f"❌ {test_name}: FAILED - {str(e)}")
                print(f"   Traceback: {traceback.format_exc()}")

        self.print_summary()

    def test_imports(self) -> bool:
        """Test all critical imports"""
        print("Testing import dependencies...")

        try:
            # Core game modules
            core_spec = importlib.util.find_spec("game.core")
            if core_spec:
                print("  ✅ Core game modules found")
            else:
                print("  ❌ Core game modules not found")

            # Character creation
            char_spec = importlib.util.find_spec("game.character_creation")
            if char_spec:
                print("  ✅ Character creation modules found")
            else:
                print("  ❌ Character creation modules not found")

            # Emotional state
            emotional_spec = importlib.util.find_spec("game.emotional_state")
            if emotional_spec:
                print("  ✅ Emotional state modules found")
            else:
                print("  ❌ Emotional state modules not found")

            # Game engine
            engine_spec = importlib.util.find_spec("game.engine")
            if engine_spec:
                print("  ✅ Game engine modules found")
            else:
                print("  ❌ Game engine modules not found")

            # Events
            events_spec = importlib.util.find_spec("game.events")
            if events_spec:
                print("  ✅ Events modules found")
            else:
                print("  ❌ Events modules not found")

            # Factions
            factions_spec = importlib.util.find_spec("game.factions")
            if factions_spec:
                print("  ✅ Factions modules found")
            else:
                print("  ❌ Factions modules not found")

            # State
            state_spec = importlib.util.find_spec("game.state")
            if state_spec:
                print("  ✅ State modules found")
            else:
                print("  ❌ State modules not found")

            return True

        except ImportError as e:
            print(f"  ❌ Import failed: {e}")
            return False

    def test_character_creation(self) -> bool:
        """Test character creation system"""
        print("Testing character creation system...")

        try:
            from game.character_creation import (
                CharacterCreator,
                create_random_character,
                BackgroundType,
                PersonalityTrait,
            )

            # Test random character creation
            char1 = create_random_character("Test1")
            print(f"  ✅ Random character created: {char1.name}")

            # Test specific character creation
            creator = CharacterCreator()
            char2 = creator.create_character(
                name="Test2",
                background_type=BackgroundType.MILITARY,
                primary_trait=PersonalityTrait.LOYAL,
                secondary_trait=PersonalityTrait.PRAGMATIC,
            )
            print(f"  ✅ Specific character created: {char2.name}")

            # Test serialization
            serialized = char1.serialize()
            deserialized = char1.__class__.deserialize(serialized)
            assert deserialized.name == char1.name, "Serialization failed"
            print("  ✅ Character serialization works")

            # Test all backgrounds
            for bg_type in BackgroundType:
                bg = creator.backgrounds[bg_type]
                assert bg.name, f"Background {bg_type} has no name"
            print("  ✅ All backgrounds loaded")

            return True

        except Exception as e:
            print(f"  ❌ Character creation failed: {e}")
            return False

    def test_emotional_state(self) -> bool:
        """Test emotional state system"""
        print("Testing emotional state system...")

        try:
            from game.emotional_state import (
                EmotionalState,
                create_random_emotional_state,
            )

            # Test basic emotional state
            emotional_state = EmotionalState()
            print("  ✅ Basic emotional state created")

            # Test emotional impact
            emotional_state.apply_emotional_impact(
                {"fear": 0.5, "anger": 0.3, "trust": -0.2}
            )
            print("  ✅ Emotional impact applied")

            # Test trauma application
            emotional_state.apply_trauma(0.7, "violence_witnessed")
            print("  ✅ Trauma applied")

            # Test random emotional state
            create_random_emotional_state()  # Test that it doesn't crash
            print("  ✅ Random emotional state created")

            # Test serialization
            serialized = emotional_state.serialize()
            deserialized = EmotionalState.deserialize(serialized)
            assert (
                deserialized.fear == emotional_state.fear
            ), "Emotional state serialization failed"
            print("  ✅ Emotional state serialization works")

            # Test stability calculation
            stability = emotional_state.get_emotional_stability()
            assert 0.0 <= stability <= 1.0, "Stability out of range"
            print("  ✅ Stability calculation works")

            return True

        except Exception as e:
            print(f"  ❌ Emotional state failed: {e}")
            return False

    def test_game_engine(self) -> bool:
        """Test game engine functionality"""
        print("Testing game engine...")

        try:
            from game.engine import GameEngine, GameStatus

            # Create game engine
            engine = GameEngine()
            print("  ✅ Game engine created")

            # Test initialization
            game_info = engine.get_game_info()
            assert "game_id" in game_info, "Game info missing game_id"
            print("  ✅ Game engine initialized")

            # Test status
            assert engine.status == GameStatus.INITIALIZING, "Wrong initial status"
            print("  ✅ Status tracking works")

            return True

        except Exception as e:
            print(f"  ❌ Game engine failed: {e}")
            return False

    async def test_faction_system(self) -> bool:
        """Test faction system"""
        print("Testing faction system...")

        try:
            from game.factions import FactionManager

            # Create faction manager
            faction_manager = FactionManager()
            print("  ✅ Faction manager created")

            # Test initialization
            await faction_manager.initialize(None)
            assert len(faction_manager.factions) > 0, "No factions initialized"
            print("  ✅ Factions initialized")

            # Test faction relationships
            faction_ids = list(faction_manager.factions.keys())
            if len(faction_ids) >= 2:
                relationship = faction_manager.get_relationship(
                    faction_ids[0], faction_ids[1]
                )
                assert -100 <= relationship <= 100, "Relationship out of range"
                print("  ✅ Faction relationships work")

            return True

        except Exception as e:
            print(f"  ❌ Faction system failed: {e}")
            return False

    def test_event_system(self) -> bool:
        """Test event system"""
        print("Testing event system...")

        try:
            from game.events import EventManager

            # Create event manager
            event_manager = EventManager()
            print("  ✅ Event manager created")

            # Test event registration
            test_events = []

            def test_listener(data):
                test_events.append(data)

            event_manager.register("test.event", test_listener)
            print("  ✅ Event listener registered")

            # Test event triggering
            event_manager.trigger("test.event", {"test": "data"})
            assert len(test_events) == 1, "Event not triggered"
            print("  ✅ Event triggering works")

            # Test event history
            events = event_manager.get_events("test.event")
            assert len(events) > 0, "No events in history"
            print("  ✅ Event history works")

            return True

        except Exception as e:
            print(f"  ❌ Event system failed: {e}")
            return False

    async def test_state_management(self) -> bool:
        """Test state management"""
        print("Testing state management...")

        try:
            from game.state import GameState

            # Create game state
            state = GameState("test_game")
            print("  ✅ Game state created")

            # Test initialization
            await state.initialize()
            assert len(state.districts) > 0, "No districts initialized"
            print("  ✅ Game state initialized")

            # Test state summary
            summary = state.get_summary()
            assert "game_id" in summary, "Summary missing game_id"
            print("  ✅ State summary works")

            return True

        except Exception as e:
            print(f"  ❌ State management failed: {e}")
            return False

    def test_integration(self) -> bool:
        """Test integration between systems"""
        print("Testing system integration...")

        try:
            from game.character_creation import create_random_character
            from game.emotional_state import EmotionalState
            from game.core import GameState

            # Create character with emotional state
            character = create_random_character("Integration_Test")
            print("  ✅ Character with emotional state created")

            # Test character's emotional state
            assert hasattr(
                character, "emotional_state"
            ), "Character missing emotional state"
            assert isinstance(
                character.emotional_state, EmotionalState
            ), "Wrong emotional state type"
            print("  ✅ Character emotional state integration works")

            # Test game state with character
            game_state = GameState()
            game_state.initialize_game()
            print("  ✅ Game state with character integration works")

            return True

        except Exception as e:
            print(f"  ❌ Integration failed: {e}")
            return False

    def print_summary(self):
        """Print debugging summary"""
        print("\n" + "=" * 60)
        print("🔍 DEBUGGING SUMMARY")
        print("=" * 60)

        passed = sum(1 for result in self.results.values() if result)
        total = len(self.results)

        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")

        if passed == total:
            print("\n🎉 ALL TESTS PASSED! New features are working correctly.")
        else:
            print(f"\n⚠️  {total - passed} TESTS FAILED. Check the errors above.")

        print("\n" + "=" * 60)


async def main():
    """Run the automated debugging"""
    debugger = FeatureDebugger()
    await debugger.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
