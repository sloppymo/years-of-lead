#!/usr/bin/env python3
"""
Quick test runner for Phase 1 implementation verification
"""

import sys
import traceback
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, 'src')

from game.relationship_system import (
    RelationshipType, RelationshipEvent, RelationshipMetrics,
    RelationshipHistory, Relationship, RelationshipManager,
    create_initial_cell_relationships
)
from game.emotional_state import EmotionalState, TraumaTriggerType, TherapyType
from game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait

def test_relationship_creation():
    """Test basic relationship creation"""
    print("Testing relationship creation...")
    
    manager = RelationshipManager()
    rel = manager.create_relationship(
        "agent1", "agent2",
        RelationshipType.COMRADE
    )
    
    assert rel is not None
    assert rel.character_id == "agent1"
    assert rel.target_id == "agent2"
    print("✅ Relationship creation works")

def test_betrayal_mechanics():
    """Test betrayal calculation"""
    print("\nTesting betrayal mechanics...")
    
    # Create a relationship with betrayal potential
    rel = Relationship(
        character_id="agent1",
        target_id="agent2",
        relationship_type=RelationshipType.COMRADE,
        metrics=RelationshipMetrics(
            trust=-0.5,
            loyalty=0.2,
            fear=0.8,
            ideological_proximity=0.2
        ),
        history=RelationshipHistory()
    )
    
    # Check betrayal probability
    betrayal_occurs, probability, reason = rel.check_for_betrayal(
        external_pressure=0.7,
        character_trauma=0.5
    )
    
    assert probability > 0.5  # High probability due to poor metrics
    print(f"✅ Betrayal mechanics work (probability: {probability:.2f})")

def test_trauma_integration():
    """Test trauma system integration"""
    print("\nTesting trauma system...")
    
    # Create a character
    creator = CharacterCreator()
    char = creator.create_character(
        name="Test Agent",
        background_type=BackgroundType.MILITARY,
        primary_trait=PersonalityTrait.LOYAL,
        secondary_trait=PersonalityTrait.CAUTIOUS,
        has_trauma=True
    )
    
    # Apply trauma
    char.emotional_state.apply_trauma(
        trauma_intensity=0.7,
        event_type="violence_witnessed",
        triggers=[TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES]
    )
    
    # Check trauma triggers
    triggered = char.check_trauma_triggers([TraumaTriggerType.VIOLENCE])
    assert len(triggered) > 0
    
    print("✅ Trauma system integration works")

def test_therapy_system():
    """Test therapy application"""
    print("\nTesting therapy system...")
    
    # Create emotional state with trauma
    state = EmotionalState(
        fear=0.8,
        sadness=0.7,
        trauma_level=0.6
    )
    
    # Apply therapy
    results = state.apply_therapy(TherapyType.PROFESSIONAL, effectiveness=0.7)
    
    assert results['trauma_reduced'] > 0
    assert state.trauma_level < 0.6
    print(f"✅ Therapy system works (trauma reduced by {results['trauma_reduced']:.2f})")

def test_group_cohesion():
    """Test group cohesion analysis"""
    print("\nTesting group cohesion...")
    
    # Create a cell
    members = ["leader", "member1", "member2"]
    manager = create_initial_cell_relationships(members, leader_id="leader")
    
    # Apply successful mission
    manager.apply_group_event(
        members,
        RelationshipEvent.MISSION_SUCCESS
    )
    
    # Check cohesion
    cohesion = manager.check_group_cohesion(members)
    
    assert cohesion['cohesion_rating'] in ["Excellent", "Good", "Fair", "Poor", "Critical"]
    print(f"✅ Group cohesion analysis works (rating: {cohesion['cohesion_rating']})")

def test_relationship_events():
    """Test relationship event application"""
    print("\nTesting relationship events...")
    
    rel = Relationship(
        character_id="agent1",
        target_id="agent2",
        relationship_type=RelationshipType.COMRADE,
        metrics=RelationshipMetrics(),
        history=RelationshipHistory()
    )
    
    # Test various events
    events_tested = 0
    
    # Mission success
    rel.apply_event(RelationshipEvent.MISSION_SUCCESS)
    assert rel.metrics.trust > 0
    events_tested += 1
    
    # Saved life
    initial_loyalty = rel.metrics.loyalty
    rel.apply_event(RelationshipEvent.SAVED_LIFE)
    assert rel.metrics.loyalty > initial_loyalty
    events_tested += 1
    
    # Betrayal
    rel.apply_event(RelationshipEvent.BETRAYAL)
    assert rel.metrics.trust < 0
    assert rel.metrics.betrayal_potential > 0.4
    events_tested += 1
    
    print(f"✅ Relationship events work ({events_tested} events tested)")

def main():
    """Run all tests"""
    print("=== PHASE 1 IMPLEMENTATION TEST ===\n")
    
    tests = [
        test_relationship_creation,
        test_betrayal_mechanics,
        test_trauma_integration,
        test_therapy_system,
        test_group_cohesion,
        test_relationship_events
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} failed: {str(e)}")
            traceback.print_exc()
    
    print(f"\n=== TEST SUMMARY ===")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {len(tests)}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Phase 1 implementation is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)