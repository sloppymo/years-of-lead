#!/usr/bin/env python3
"""
Test runner for Phase 2: Mission Execution System
"""

import sys
import os
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.game.mission_execution import (
    MissionExecutor, MissionPhase, ActionType, MissionOutcome,
    ComplicationSeverity, MissionAction, MissionComplication,
    AgentPerformance, MissionReport, NarrativeGenerator
)
from src.game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait
from src.game.relationship_system import RelationshipManager, RelationshipType, RelationshipMetrics
from src.game.legal_system import LegalSystem
from src.game.intelligence_system import IntelligenceDatabase
from src.game.emotional_state import TraumaTriggerType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockMission:
    """Mock mission for testing"""
    def __init__(self, mission_id, mission_type, objective, required_skills):
        self.id = mission_id
        self.mission_type = mission_type
        self.primary_objective = objective
        self.required_skills = required_skills
        self.faction_id = "resistance"


class MockLocation:
    """Mock location for testing"""
    def __init__(self, location_id, security_level):
        self.id = location_id
        self.security_level = security_level


def test_basic_mission_execution():
    """Test basic mission execution flow"""
    print("\n" + "="*60)
    print("Testing Basic Mission Execution")
    print("="*60 + "\n")
    
    # Initialize systems
    legal_system = LegalSystem()
    intelligence_system = IntelligenceDatabase()
    relationship_manager = RelationshipManager()
    executor = MissionExecutor(legal_system, intelligence_system, relationship_manager)
    
    # Create a team
    creator = CharacterCreator()
    team = [
        creator.create_character(
            "Elena Martinez",
            BackgroundType.MILITARY,
            PersonalityTrait.LEADER,
            PersonalityTrait.METHODICAL
        ),
        creator.create_character(
            "Alex Chen",
            BackgroundType.TECHNICAL,
            PersonalityTrait.ANALYTICAL,
            PersonalityTrait.CAUTIOUS
        ),
        creator.create_character(
            "Marcus Johnson",
            BackgroundType.ACTIVIST,
            PersonalityTrait.IDEALISTIC,
            PersonalityTrait.LOYAL
        )
    ]
    
    # Set up relationships
    for i, agent1 in enumerate(team):
        for j, agent2 in enumerate(team):
            if i != j:
                relationship_manager.create_relationship(
                    agent1.id,
                    agent2.id,
                    RelationshipType.COMRADE,
                    RelationshipMetrics(trust=0.7, loyalty=0.8)
                )
    
    # Create mission
    mission = MockMission(
        "sabotage_001",
        "sabotage",
        "Destroy surveillance equipment",
        ["technical", "stealth"]
    )
    
    location = MockLocation("government_facility", 6)
    equipment = {"explosives": 3, "hacking_device": 1, "smoke_grenades": 4}
    
    # Execute mission
    print("Mission Details:")
    print(f"- ID: {mission.id}")
    print(f"- Objective: {mission.primary_objective}")
    print(f"- Location Security: {location.security_level}/10")
    print(f"- Team Size: {len(team)} agents")
    print()
    
    report = executor.execute_mission(mission, team, location, equipment)
    
    # Display results
    print("\nMISSION COMPLETE!")
    print("-" * 60)
    print(report.generate_full_report())
    
    # Summary stats
    print("\nQuick Stats:")
    print(f"- Phases Completed: {len(report.phases_completed)}/{len(list(MissionPhase))}")
    print(f"- Actions Taken: {sum(len(p.actions_taken) for p in report.agent_performance.values())}")
    print(f"- Complications: {len(report.complications)}")
    print(f"- Propaganda Value: {report.propaganda_value:.1%}")
    
    return report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS, MissionOutcome.PARTIAL_SUCCESS]


def test_trauma_trigger_scenario():
    """Test mission with trauma triggers"""
    print("\n" + "="*60)
    print("Testing Mission with Trauma Triggers")
    print("="*60 + "\n")
    
    # Initialize systems
    legal_system = LegalSystem()
    intelligence_system = IntelligenceDatabase()
    relationship_manager = RelationshipManager()
    executor = MissionExecutor(legal_system, intelligence_system, relationship_manager)
    
    # Create team with traumatized member
    creator = CharacterCreator()
    team = [
        creator.create_character(
            "Sarah Williams",
            BackgroundType.ACTIVIST,
            PersonalityTrait.COMPASSIONATE,
            PersonalityTrait.CAUTIOUS
        ),
        creator.create_character(
            "David Park",
            BackgroundType.CRIMINAL,
            PersonalityTrait.PRAGMATIC,
            PersonalityTrait.OPPORTUNISTIC
        )
    ]
    
    # Add trauma to Sarah
    print("Adding trauma to Sarah Williams...")
    team[0].emotional_state.apply_trauma(
        trauma_intensity=0.8,
        event_type="witnessed_violence",
        triggers=[TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES]
    )
    print(f"Sarah's current stress level: {team[0].get_stress_level():.1%}")
    print()
    
    # Create infiltration mission
    mission = MockMission(
        "infiltration_002",
        "infiltration",
        "Steal classified documents",
        ["stealth", "social"]
    )
    
    location = MockLocation("police_station", 8)  # High security
    equipment = {"fake_ids": 2, "camera_jammer": 1}
    
    # Execute mission
    report = executor.execute_mission(mission, team, location, equipment)
    
    # Check for trauma episodes
    sarah_performance = report.agent_performance[team[0].id]
    print("\nSarah's Performance:")
    print(f"- Trauma Triggered: {sarah_performance.trauma_triggered}")
    print(f"- Panic Episodes: {sarah_performance.panic_episodes}")
    print(f"- Performance Score: {sarah_performance.calculate_performance_score():.1%}")
    
    if sarah_performance.trauma_triggered:
        print("\nTrauma affected the mission - checking memorable moments:")
        for moment in report.memorable_moments:
            if "Sarah" in moment or "flashback" in moment.lower():
                print(f"  • {moment}")
    
    return True


def test_betrayal_scenario():
    """Test mission with potential betrayal"""
    print("\n" + "="*60)
    print("Testing Betrayal Scenario")
    print("="*60 + "\n")
    
    # Initialize systems
    legal_system = LegalSystem()
    intelligence_system = IntelligenceDatabase()
    relationship_manager = RelationshipManager()
    executor = MissionExecutor(legal_system, intelligence_system, relationship_manager)
    
    # Create team with trust issues
    creator = CharacterCreator()
    team = [
        creator.create_character(
            "Commander Hayes",
            BackgroundType.MILITARY,
            PersonalityTrait.LEADER,
            PersonalityTrait.RUTHLESS
        ),
        creator.create_character(
            "Agent Rivera",
            BackgroundType.CRIMINAL,
            PersonalityTrait.OPPORTUNISTIC,
            PersonalityTrait.PESSIMISTIC
        ),
        creator.create_character(
            "Tech Specialist Kim",
            BackgroundType.TECHNICAL,
            PersonalityTrait.ANALYTICAL,
            PersonalityTrait.LOYAL
        )
    ]
    
    # Set up strained relationships
    print("Setting up strained relationships...")
    
    # Rivera distrusts everyone
    for other in team:
        if other.id != team[1].id:
            relationship_manager.create_relationship(
                team[1].id,
                other.id,
                RelationshipType.RIVAL,
                RelationshipMetrics(trust=-0.6, loyalty=0.2, fear=0.7)
            )
            relationship_manager.create_relationship(
                other.id,
                team[1].id,
                RelationshipType.SUBORDINATE,
                RelationshipMetrics(trust=0.3, loyalty=0.4, fear=0.5)
            )
    
    # Rivera has low ideology and high fear
    team[1].emotional_state.fear = 0.8
    team[1].ideology_score = 0.2
    
    print(f"Rivera's fear level: {team[1].emotional_state.fear:.1%}")
    print(f"Rivera's ideology score: {team[1].get_ideological_score():.1%}")
    print()
    
    # High-stakes combat mission
    mission = MockMission(
        "assault_003",
        "assault",
        "Eliminate regime official",
        ["combat", "tactics"]
    )
    
    location = MockLocation("regime_compound", 9)
    equipment = {"rifles": 3, "body_armor": 3, "explosives": 2}
    
    # Execute mission
    report = executor.execute_mission(mission, team, location, equipment)
    
    # Check for betrayal
    betrayal_occurred = any(p.betrayal_attempted for p in report.agent_performance.values())
    
    if betrayal_occurred:
        print("\n🚨 BETRAYAL DETECTED!")
        for agent_id, performance in report.agent_performance.items():
            if performance.betrayal_attempted:
                agent = next(a for a in team if a.id == agent_id)
                print(f"- {agent.name} betrayed the team!")
                
                # Find betrayal in memorable moments
                for moment in report.memorable_moments:
                    if "betrayal" in moment.lower():
                        print(f"- {moment}")
    else:
        print("\nNo betrayal occurred this time (it's probabilistic)")
        print("But the conditions were ripe for it...")
    
    print(f"\nMission Outcome: {report.outcome.value}")
    
    return True


def test_narrative_generation():
    """Test narrative generation capabilities"""
    print("\n" + "="*60)
    print("Testing Narrative Generation")
    print("="*60 + "\n")
    
    generator = NarrativeGenerator()
    
    # Create sample reports with different outcomes
    
    # 1. Critical Success
    print("1. Critical Success Narrative:")
    report1 = MissionReport(
        mission_id="test_001",
        start_time=datetime.now(),
        end_time=datetime.now(),
        phases_completed=list(MissionPhase),
        outcome=MissionOutcome.CRITICAL_SUCCESS,
        action_log=[],
        complications=[],
        agent_performance={
            "hero1": AgentPerformance("hero1", [], 0.1, False, {}, False, True, 0, 0, [])
        },
        objectives_completed=["primary", "secondary"],
        objectives_failed=[],
        casualties=[],
        captured_agents=[],
        heat_generated=5,
        public_opinion_shift=0.05,
        resources_gained={"intel": 5},
        resources_lost={},
        narrative_summary="",
        memorable_moments=["Agent's brilliant improvisation saved the day"],
        propaganda_value=0.85,
        symbolic_impact="A decisive blow against tyranny"
    )
    
    summary1 = generator.generate_mission_summary(report1)
    print(f"  {summary1}\n")
    
    # 2. Disaster with Betrayal
    print("2. Disaster with Betrayal Narrative:")
    report2 = MissionReport(
        mission_id="test_002",
        start_time=datetime.now(),
        end_time=datetime.now(),
        phases_completed=[MissionPhase.PLANNING, MissionPhase.INFILTRATION],
        outcome=MissionOutcome.DISASTER,
        action_log=[],
        complications=[
            MissionComplication(
                MissionPhase.EXECUTION,
                ComplicationSeverity.CATASTROPHIC,
                "Agent turned on the team",
                ["all"],
                True,
                "Trust shattered in an instant"
            )
        ],
        agent_performance={
            "traitor": AgentPerformance("traitor", [], 0.0, False, {}, True, False, 0, 0, []),
            "victim1": AgentPerformance("victim1", [], 0.5, True, {}, False, False, 3, 0, [])
        },
        objectives_completed=[],
        objectives_failed=["primary"],
        casualties=["victim1"],
        captured_agents=["victim2"],
        heat_generated=50,
        public_opinion_shift=-0.1,
        resources_gained={},
        resources_lost={"equipment": 10, "safe_houses": 2},
        narrative_summary="",
        memorable_moments=["The traitor's cold smile as they opened fire", "Final words of a fallen comrade"],
        propaganda_value=0.05,
        symbolic_impact="A dark day for the resistance"
    )
    
    summary2 = generator.generate_mission_summary(report2)
    print(f"  {summary2}\n")
    
    return True


def run_all_tests():
    """Run all Phase 2 tests"""
    print("\n" + "="*80)
    print("PHASE 2: MISSION EXECUTION SYSTEM - TEST SUITE")
    print("="*80)
    
    tests = [
        ("Basic Mission Execution", test_basic_mission_execution),
        ("Trauma Trigger Scenario", test_trauma_trigger_scenario),
        ("Betrayal Scenario", test_betrayal_scenario),
        ("Narrative Generation", test_narrative_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
            print(f"\n✓ {test_name} completed")
        except Exception as e:
            results.append((test_name, f"ERROR: {str(e)}"))
            print(f"\n✗ {test_name} failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, result in results:
        status_symbol = "✓" if result == "PASS" else "✗"
        print(f"{status_symbol} {test_name}: {result}")
    
    passed = sum(1 for _, result in results if result == "PASS")
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All Phase 2 tests passed! Mission Execution System is operational.")
    else:
        print("\n⚠️  Some tests failed. Please review the implementation.")


if __name__ == "__main__":
    run_all_tests()