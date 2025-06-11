#!/usr/bin/env python3
"""
Test and Demonstration Script for Dynamic Narrative Tone System

This script demonstrates the new player-authored narrative system in Years of Lead,
showing how players can influence the tone and style of generated content.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait
from game.dynamic_narrative_tone import (
    DynamicNarrativeToneEngine, VoiceConfiguration, EmotionalTone,
    SymbolicElement, NarrativeStyle, create_default_voice_configurations
)
from game.narrative_engine import NarrativeEngine
from game.core import GameState


def demonstrate_voice_configuration():
    """Demonstrate voice configuration creation and modification"""
    print("🎭 Dynamic Narrative Tone System Demonstration")
    print("=" * 60)

    # Create a character with voice configuration
    creator = CharacterCreator()
    character = creator.create_character(
        name="Alex Rivera",
        background_type=BackgroundType.JOURNALIST,
        primary_trait=PersonalityTrait.PESSIMISTIC,
        secondary_trait=PersonalityTrait.ANALYTICAL
    )

    print(f"\n📝 Created Character: {character.name}")
    print(f"Background: {character.background.name}")
    print(f"Traits: {character.traits.primary_trait.value}, {character.traits.secondary_trait.value}")

    # Show default voice configuration
    voice_config = character.voice_config
    print(f"\n🎵 Default Voice Configuration:")
    print(f"Emotional Tones: {[tone.value for tone in voice_config.emotional_tones]}")
    print(f"Symbolic Preferences: {[symbol.value for symbol in voice_config.symbolic_preferences]}")
    print(f"Style Notes: {[style.value for style in voice_config.style_notes]}")
    print(f"Default Lines: {len(voice_config.player_authored_lines)}")

    for i, line in enumerate(voice_config.player_authored_lines, 1):
        print(f"  {i}. '{line.content}'")
        print(f"     Tone: {line.emotional_tone.value if line.emotional_tone else 'None'}")
        print(f"     Symbols: {[s.value for s in line.symbolic_elements]}")
        print(f"     Style: {[s.value for s in line.style_markers]}")

    return character, voice_config


def demonstrate_player_line_addition():
    """Demonstrate adding player-authored lines"""
    print("\n🖋️  Player Line Addition Demonstration")
    print("-" * 40)

    # Create a voice configuration
    voice_config = VoiceConfiguration("demo_character")

    # Add player lines as described in the user's request
    example_lines = [
        "You mistake gunfire for fireworks. Again.",
        "There's a beauty in broken glass if you squint just right.",
        "The regime sends flowers now. Carnations. Red, of course."
    ]

    print("Adding player-authored lines:")
    for line_text in example_lines:
        line = voice_config.add_player_line(line_text)
        print(f"\n  Added: '{line_text}'")
        print(f"  Detected tone: {line.emotional_tone.value if line.emotional_tone else 'neutral'}")
        print(f"  Symbols found: {[s.value for s in line.symbolic_elements]}")
        print(f"  Style markers: {[s.value for s in line.style_markers]}")

    return voice_config


def demonstrate_narrative_generation():
    """Demonstrate narrative generation with voice configuration"""
    print("\n📖 Narrative Generation Demonstration")
    print("-" * 40)

    # Create tone engine
    tone_engine = DynamicNarrativeToneEngine()

    # Create a character with voice configuration
    voice_config = VoiceConfiguration("cynical_reporter")
    voice_config.emotional_tones = [EmotionalTone.WRY, EmotionalTone.SARDONIC]
    voice_config.symbolic_preferences = [SymbolicElement.CIGARETTES, SymbolicElement.BROKEN_GLASS]
    voice_config.style_notes = [NarrativeStyle.SARCASM_COPING, NarrativeStyle.SHORT_SENTENCES]

    # Add some player lines
    voice_config.add_player_line("You mistake gunfire for fireworks. Again.")
    voice_config.add_player_line("The coffee tastes like yesterday's hopes.")
    voice_config.add_player_line("Perfect. Another crisis. Just what Tuesday needed.")

    # Register with engine
    tone_engine.register_voice_configuration(voice_config)

    # Test base events
    base_events = [
        "You enter the café and order coffee.",
        "A loud sound echoes from the street outside.",
        "The meeting has been postponed indefinitely.",
        "You receive a message from an unknown contact.",
        "The news report discusses recent government policies."
    ]

    print("\nGenerating narratives with voice configuration:")
    for i, base_event in enumerate(base_events, 1):
        enhanced = tone_engine.generate_narrative_with_voice(
            "cynical_reporter",
            base_event,
            {"event_type": "daily_life", "intensity": 0.5}
        )

        print(f"\n{i}. Base: {base_event}")
        print(f"   Enhanced: {enhanced}")

    return tone_engine


def demonstrate_voice_commands():
    """Demonstrate voice command handling"""
    print("\n💬 Voice Command Demonstration")
    print("-" * 40)

    # Create narrative engine with game state
    game_state = GameState()
    narrative_engine = NarrativeEngine(game_state)

    character_id = "test_character"

    # Test various voice commands
    commands = [
        "add_line You smell coffee. Real coffee. You were wrong.",
        "set_tone melancholic",
        "set_symbol coffee",
        "set_style poetic_language",
        "show_config",
        "add_line The statue's missing its head. So is the regime.",
        "show_config"
    ]

    print("Testing voice commands:")
    for command in commands:
        print(f"\n> /voice {command}")
        response = narrative_engine.handle_voice_command(character_id, command)
        print(f"  {response}")

    return narrative_engine


def demonstrate_integration_with_existing_systems():
    """Demonstrate integration with existing narrative systems"""
    print("\n🔗 Integration with Existing Systems")
    print("-" * 40)

    # Create game state and narrative engine
    game_state = GameState()
    narrative_engine = NarrativeEngine(game_state)

    # Create character with voice configuration
    creator = CharacterCreator()
    character = creator.create_character(
        name="Sofia Chen",
        background_type=BackgroundType.ACTIVIST,
        primary_trait=PersonalityTrait.IDEALISTIC,
        secondary_trait=PersonalityTrait.COMPASSIONATE
    )

    # Register character voice with narrative engine
    narrative_engine.register_character_voice(character.id, character.voice_config)

    # Test enhanced narrative generation
    context = {
        "event_type": "resistance_meeting",
        "emotional_context": "hopeful",
        "location": "safe_house"
    }

    base_event = "The resistance cell gathers to plan their next operation."
    enhanced_narrative = narrative_engine.generate_enhanced_narrative(
        character.id, base_event, context
    )

    print(f"Character: {character.name}")
    print(f"Base Event: {base_event}")
    print(f"Enhanced: {enhanced_narrative}")

    # Show voice summary
    print(f"\nVoice Summary:")
    summary = narrative_engine.get_character_voice_summary(character.id)
    print(summary)

    return narrative_engine, character


def test_serialization():
    """Test voice configuration serialization/deserialization"""
    print("\n💾 Serialization Test")
    print("-" * 40)

    # Create voice configuration
    original_config = VoiceConfiguration("test_character")
    original_config.emotional_tones = [EmotionalTone.WRY, EmotionalTone.CYNICAL]
    original_config.symbolic_preferences = [SymbolicElement.CIGARETTES]
    original_config.style_notes = [NarrativeStyle.SARCASM_COPING]
    original_config.add_player_line("Testing serialization.")

    # Serialize
    serialized = original_config.to_dict()
    print("✅ Serialization successful")

    # Deserialize
    restored_config = VoiceConfiguration.from_dict(serialized)
    print("✅ Deserialization successful")

    # Verify
    assert restored_config.character_id == original_config.character_id
    assert restored_config.emotional_tones == original_config.emotional_tones
    assert restored_config.symbolic_preferences == original_config.symbolic_preferences
    assert restored_config.style_notes == original_config.style_notes
    assert len(restored_config.player_authored_lines) == len(original_config.player_authored_lines)

    print("✅ Verification successful - all data preserved")

    return True


def demonstrate_sylva_wren_integration():
    """Demonstrate SYLVA/WREN integration hooks"""
    print("\n🧠 SYLVA/WREN Integration Demonstration")
    print("-" * 40)

    # Create narrative engine
    game_state = GameState()
    narrative_engine = NarrativeEngine(game_state)

    # Enable SYLVA/WREN (simulation mode)
    narrative_engine.sylva_enabled = True
    narrative_engine.wren_enabled = True

    # Create character with emotional voice configuration
    character_id = "emotional_character"
    voice_config = VoiceConfiguration(character_id)
    voice_config.emotional_tones = [EmotionalTone.MELANCHOLIC]
    voice_config.symbolic_preferences = [SymbolicElement.BROKEN_GLASS, SymbolicElement.RAIN]
    voice_config.add_player_line("Memories fall like autumn rain.")

    narrative_engine.register_character_voice(character_id, voice_config)

    # Generate enhanced narrative
    base_event = "You walk through the abandoned district."
    enhanced = narrative_engine.generate_enhanced_narrative(
        character_id,
        base_event,
        {"emotional_context": "nostalgic", "intensity": 0.8}
    )

    print(f"Base Event: {base_event}")
    print(f"SYLVA/WREN Enhanced: {enhanced}")

    return narrative_engine


def run_comprehensive_demo():
    """Run comprehensive demonstration of the dynamic narrative tone system"""
    print("🎮 Years of Lead - Dynamic Narrative Tone System")
    print("🔥 Phase Four Implementation - Player Voice Integration")
    print("=" * 80)

    try:
        # Run demonstrations
        character, voice_config = demonstrate_voice_configuration()
        player_config = demonstrate_player_line_addition()
        tone_engine = demonstrate_narrative_generation()
        narrative_engine = demonstrate_voice_commands()
        integration_engine, integration_character = demonstrate_integration_with_existing_systems()
        serialization_test = test_serialization()
        sylva_wren_engine = demonstrate_sylva_wren_integration()

        print("\n🎉 Demonstration Complete!")
        print("=" * 80)
        print("\n✅ Key Features Demonstrated:")
        print("  • Character voice configuration with automatic trait-based setup")
        print("  • Player-authored line analysis and influence")
        print("  • Dynamic narrative tone filtering")
        print("  • Symbolic element integration")
        print("  • Style pattern recognition and application")
        print("  • Voice command handling (/voice commands)")
        print("  • Integration with existing narrative engine")
        print("  • SYLVA/WREN compatibility hooks")
        print("  • Serialization/deserialization for save games")

        print("\n📝 Usage Examples:")
        print("  /voice add_line You mistake gunfire for fireworks. Again.")
        print("  /voice set_tone wry")
        print("  /voice set_symbol broken_glass")
        print("  /voice set_style one_liners")
        print("  /voice show_config")

        print("\n🎯 System Benefits:")
        print("  • Players can author lines that influence future narrative generation")
        print("  • Character voice remains consistent with personality traits")
        print("  • Emotional tone filtering shapes story atmosphere")
        print("  • Symbolic elements create thematic coherence")
        print("  • Integration with SYLVA/WREN for therapeutic applications")
        print("  • Learning system improves generation over time")

        return True

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_demo()
    if success:
        print("\n🚀 Dynamic Narrative Tone System successfully implemented!")
        print("Ready for integration into Years of Lead gameplay loop.")
    else:
        print("\n💥 Demo failed - check implementation.")
        sys.exit(1)