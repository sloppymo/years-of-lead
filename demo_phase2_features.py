#!/usr/bin/env python3
"""
SYLVA Phase 2 Features Demo
Demonstrates the enhanced symbolic intelligence features including:
- Emotion frequency tracking (7/30/90 day summaries)
- Subsystem tension mapping (🔥/🌳/🌙 balance analysis)
- Ritual closure intensity scaling (light/medium/heavy endings)
- Drift-aware pattern summaries
- User archetype modeling
- Session typing (emergent/reflective/dispersive)
- Symbolic arc detection
- Memory weight scoring (emotional gravity)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from utils.memory_log import MemoryLogger


def create_sample_interactions():
    """Create sample interactions to demonstrate Phase 2 features."""

    # Initialize systems with temporary memory file
    memory_logger = MemoryLogger("/tmp/sylva_phase2_demo.json")

    # Sample interactions representing different emotional states and patterns
    sample_interactions = [
        # Week 1: Beginning - High emotional intensity, mixed subsystems
        {
            "user_input": "I feel completely shattered and broken inside",
            "subsystem": "MARROW",
            "archetype": "the_spiral",
            "days_ago": 21,
        },
        {
            "user_input": "Everything feels overwhelming and too much to handle",
            "subsystem": "AURA",
            "archetype": "the_tide",
            "days_ago": 20,
        },
        {
            "user_input": "I'm scared and don't feel safe anywhere",
            "subsystem": "ROOT",
            "archetype": "the_mountain",
            "days_ago": 19,
        },
        # Week 2: Middle - Sustained MARROW work
        {
            "user_input": "The grief feels like it will never end",
            "subsystem": "MARROW",
            "archetype": "the_well",
            "days_ago": 14,
        },
        {
            "user_input": "I'm angry at everything and everyone",
            "subsystem": "MARROW",
            "archetype": "the_ember",
            "days_ago": 13,
        },
        {
            "user_input": "The shame burns deep inside me",
            "subsystem": "MARROW",
            "archetype": "the_cave",
            "days_ago": 12,
        },
        # Week 3: Transition - Moving toward integration
        {
            "user_input": "I'm starting to think about what this all means",
            "subsystem": "ROOT",
            "archetype": "the_bridge",
            "days_ago": 7,
        },
        {
            "user_input": "Maybe I need to reflect on these patterns",
            "subsystem": "ROOT",
            "archetype": "the_river",
            "days_ago": 6,
        },
        # Week 4: Recent - Boundary work and closure
        {
            "user_input": "I need to protect what I've learned",
            "subsystem": "AURA",
            "archetype": "the_mask",
            "days_ago": 3,
        },
        {
            "user_input": "The mirror shows me something new",
            "subsystem": "AURA",
            "archetype": "the_mirror",
            "days_ago": 2,
        },
        {
            "user_input": "I feel like I'm finding my rhythm again",
            "subsystem": "AURA",
            "archetype": "the_tide",
            "days_ago": 1,
        },
    ]

    # Log interactions with backdated timestamps
    for interaction in sample_interactions:
        # Calculate timestamp
        target_date = datetime.now() - timedelta(days=interaction["days_ago"])

        # Temporarily modify the interaction timestamp
        memory_data = memory_logger._read_memory()

        # Create interaction entry
        interaction_entry = {
            "timestamp": target_date.isoformat(),
            "user_input": interaction["user_input"],
            "sylva_response": f"The {interaction['archetype'].replace('_', ' ')} holds wisdom for this moment.",
            "subsystem": interaction["subsystem"],
            "emotion": None,  # Will be detected
            "archetype_used": interaction["archetype"],
            "memory_weight": 0.0,  # Will be calculated
            "session_id": target_date.strftime("%Y%m%d"),
            "interaction_id": target_date.strftime("%Y%m%d_%H%M%S"),
        }

        # Detect emotion and calculate weight
        if interaction["user_input"]:
            emotion_counts = memory_logger.pattern_engine.analyze_emotions(
                [interaction["user_input"]]
            )
            detected_emotion = memory_logger.pattern_engine.get_dominant_emotion(
                emotion_counts
            )
            interaction_entry["emotion"] = detected_emotion

            memory_weight = memory_logger.archetype_engine.calculate_memory_weight(
                interaction["user_input"], detected_emotion, interaction["subsystem"]
            )
            interaction_entry["memory_weight"] = memory_weight

            # Track archetype preference
            memory_logger.archetype_engine.track_archetype_preference(
                interaction["user_input"],
                interaction["subsystem"],
                interaction["archetype"],
            )

        # Add to memory
        memory_data["interactions"].append(interaction_entry)

        # Update subsystem activity
        if interaction["subsystem"] in memory_data["subsystem_activity"]:
            memory_data["subsystem_activity"][interaction["subsystem"]] += 1

        memory_logger._write_memory(memory_data)

    return memory_logger


def demonstrate_phase2_features():
    """Demonstrate all Phase 2 features with sample data."""

    print("🌙 SYLVA Phase 2 Features Demo")
    print("=" * 60)
    print("Demonstrating Adaptive Symbolic Intelligence v2.3.0")
    print()

    # Create sample data
    print("📝 Creating sample interaction history...")
    memory_logger = create_sample_interactions()
    pattern_engine = memory_logger.pattern_engine
    archetype_engine = memory_logger.archetype_engine

    # Get memory data for analysis
    memory_data = memory_logger._read_memory()
    interactions = memory_data.get("interactions", [])

    print(f"✓ Created {len(interactions)} sample interactions across 3 weeks")
    print()

    # 1. EMOTION FREQUENCY TRACKING
    print("🔮 1. Emotion Frequency Tracking (7/30/90 day summaries)")
    print("-" * 50)

    emotion_frequencies = pattern_engine.analyze_emotion_frequencies(interactions)

    for timeframe, emotions in emotion_frequencies.items():
        days = timeframe.replace("_days", "")
        print(f"\n📊 {days} Day Analysis:")
        if emotions:
            for emotion, count in sorted(
                emotions.items(), key=lambda x: x[1], reverse=True
            ):
                bar = "█" * min(count, 10) + "░" * (10 - min(count, 10))
                print(f"   {emotion.title()}: {bar} {count}")
        else:
            print("   No emotions detected in this timeframe")

    print()

    # 2. SUBSYSTEM TENSION MAPPING
    print("🧠 2. Subsystem Tension Mapping (🔥/🌳/🌙 balance analysis)")
    print("-" * 55)

    subsystem_tension = pattern_engine.analyze_subsystem_tension(interactions)

    print(f'Balance State: {subsystem_tension["balance"]}')
    print(f'Tension Level: {subsystem_tension["tension_level"]}')
    print(f'Dominant Subsystem: {subsystem_tension["dominant_subsystem"]}')
    print()

    print("Subsystem Ratios:")
    for subsystem, ratio in subsystem_tension["ratios"].items():
        symbol = {"MARROW": "🔥", "ROOT": "🌳", "AURA": "🌙"}[subsystem]
        bar_length = int(ratio * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"   {symbol} {subsystem}: {bar} {ratio:.1%}")

    print()

    # 3. RITUAL CLOSURE INTENSITY SCALING
    print("🕯️ 3. Ritual Closure Intensity Scaling")
    print("-" * 40)

    # Test different intensity levels
    recent_emotions = emotion_frequencies.get("7_days", {})
    ritual_intensity = pattern_engine.determine_ritual_intensity(
        recent_emotions, subsystem_tension
    )

    print(f"Determined Intensity: {ritual_intensity}")
    print()

    print("Sample Ritual Closures by Intensity:")
    for intensity in ["light", "medium", "heavy"]:
        closure = pattern_engine.generate_ritual_closure(intensity)
        print(f'   {intensity.title()}: "{closure}"')

    print()

    # 4. DRIFT-AWARE PATTERN SUMMARIES
    print("🌊 4. Drift-Aware Pattern Detection")
    print("-" * 35)

    drift_pattern = pattern_engine.detect_drift_patterns(interactions)

    if drift_pattern:
        print(f"Detected Drift: {drift_pattern}")
    else:
        print("No significant drift patterns detected")

    print()

    # 5. USER ARCHETYPE MODELING
    print("🏛️ 5. User Archetype Modeling")
    print("-" * 30)

    user_summary = archetype_engine.get_user_summary()

    print(f'Total Interactions: {user_summary["total_interactions"]}')
    print(f'Profile Age: {user_summary["profile_age_days"]} days')
    print(f'Dominant Session Type: {user_summary["dominant_session_type"]}')
    print()

    print("Preferred Archetypes by Subsystem:")
    for subsystem, archetype in user_summary["preferred_archetypes"].items():
        symbol = {"MARROW": "🔥", "ROOT": "🌳", "AURA": "🌙"}[subsystem]
        archetype_name = archetype.replace("_", " ").title()
        print(f"   {symbol} {subsystem}: {archetype_name}")

    print()

    print("Session Type Distribution:")
    session_dist = user_summary["session_distribution"]
    total_sessions = sum(session_dist.values()) or 1
    for session_type, count in session_dist.items():
        percentage = (count / total_sessions) * 100
        bar_length = int(percentage / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"   {session_type.title()}: {bar} {count} ({percentage:.1f}%)")

    print()

    # 6. SESSION TYPING
    print("🎭 6. Session Typing (emergent/reflective/dispersive)")
    print("-" * 50)

    # Test session type detection
    recent_inputs = [i.get("user_input", "") for i in interactions[-5:]]
    current_session_type = archetype_engine.detect_session_type(recent_inputs)

    print(f"Current Session Type: {current_session_type}")
    print()

    print("Session Type Characteristics:")
    for session_type, data in archetype_engine.session_types.items():
        print(f'   {session_type.title()}: {data["characteristics"]}')

    print()

    # 7. SYMBOLIC ARC DETECTION
    print("🌀 7. Symbolic Arc Detection")
    print("-" * 28)

    symbolic_arc = archetype_engine.detect_symbolic_arc(interactions)

    if symbolic_arc:
        print(f'Arc Type: {symbolic_arc["type"]}')
        print(f'Description: {symbolic_arc["description"]}')
        print(f'Entries Analyzed: {symbolic_arc["entries_analyzed"]}')
        print(f'Dominant Emotions: {symbolic_arc["dominant_emotions"]}')
        print(f'Subsystem Flow: {" → ".join(symbolic_arc["subsystem_flow"])}')
    else:
        print("No symbolic arc detected (insufficient data or no clear pattern)")

    print()

    # 8. MEMORY WEIGHT SCORING
    print("⚖️ 8. Memory Weight Scoring (emotional gravity)")
    print("-" * 45)

    # Show memory weights for recent interactions
    weighted_interactions = [
        (i.get("memory_weight", 0.0), i.get("user_input", ""))
        for i in interactions[-5:]
        if i.get("memory_weight")
    ]

    if weighted_interactions:
        print("Recent Memory Weights (0.0 = light, 1.0 = heavy):")
        for weight, user_input in sorted(weighted_interactions, reverse=True):
            weight_bar = "█" * int(weight * 10) + "░" * (10 - int(weight * 10))
            truncated_input = (
                user_input[:50] + "..." if len(user_input) > 50 else user_input
            )
            print(f'   {weight:.2f} {weight_bar} "{truncated_input}"')
    else:
        print("No weighted memories available")

    print()

    # 9. ENHANCED SYMBOLIC SUMMARY
    print("✨ 9. Enhanced Symbolic Summary (Integration)")
    print("-" * 45)

    enhanced_summary = memory_logger.generate_enhanced_summary(days=7)
    print(f'"{enhanced_summary}"')

    print()

    # 10. PHASE 2 COMPREHENSIVE ANALYSIS
    print("🔬 10. Phase 2 Comprehensive Analysis")
    print("-" * 38)

    phase2_analysis = memory_logger.get_phase2_analysis()

    print("Analysis Components:")
    for component in phase2_analysis.keys():
        if component != "analysis_timestamp":
            status = "✓" if phase2_analysis[component] else "○"
            print(f'   {status} {component.replace("_", " ").title()}')

    print(f'\nAnalysis Timestamp: {phase2_analysis["analysis_timestamp"]}')
    print(f'Average Memory Weight: {phase2_analysis["average_memory_weight"]:.3f}')

    print()
    print("🌟 Phase 2 Demo Complete!")
    print("All adaptive symbolic intelligence features are operational.")

    # Cleanup
    import os

    try:
        os.remove("/tmp/sylva_phase2_demo.json")
        os.remove("/tmp/user_archetype_profile.json")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    demonstrate_phase2_features()
