#!/usr/bin/env python3
"""
Years of Lead - Mission Execution System Demo (Automated)
Non-interactive demonstration for recording
"""

import sys
import os
import time
import random
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


class MockMission:
    """Mock mission for demo"""
    def __init__(self, mission_id, mission_type, objective, required_skills):
        self.id = mission_id
        self.mission_type = mission_type
        self.primary_objective = objective
        self.required_skills = required_skills
        self.faction_id = "resistance"


class MockLocation:
    """Mock location for demo"""
    def __init__(self, location_id, name, security_level):
        self.id = location_id
        self.name = name
        self.security_level = security_level


def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def typewriter_print(text, delay=0.02):
    """Print text with typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_header(title):
    """Print a styled header"""
    print("\n" + "="*80)
    print(f"  {title.upper()}")
    print("="*80 + "\n")


def display_team(team):
    """Display team information"""
    print("\n📋 MISSION TEAM:")
    print("-" * 60)
    for i, agent in enumerate(team, 1):
        stress = agent.get_stress_level()
        ideology = agent.get_ideological_score()
        status = "🟢" if stress < 0.5 else "🟡" if stress < 0.8 else "🔴"
        
        print(f"{i}. {agent.name} ({agent.background.name})")
        print(f"   Traits: {agent.traits.primary_trait.value} / {agent.traits.secondary_trait.value}")
        print(f"   Status: {status} Stress: {stress:.0%} | Ideology: {ideology:.0%}")
        if agent.trauma:
            print(f"   ⚠️  Trauma: {agent.trauma.type.value}")
        print()


def display_mission_briefing(mission, location):
    """Display mission briefing"""
    print("\n📜 MISSION BRIEFING:")
    print("-" * 60)
    print(f"Operation: {mission.id}")
    print(f"Type: {mission.mission_type.upper()}")
    print(f"Objective: {mission.primary_objective}")
    print(f"Location: {location.name}")
    print(f"Security Level: {'█' * location.security_level}{'░' * (10-location.security_level)} ({location.security_level}/10)")
    print(f"Required Skills: {', '.join(mission.required_skills)}")
    print()


def run_demo():
    """Run the mission execution demo automatically"""
    clear_screen()
    
    print_header("Years of Lead - Mission Execution System")
    typewriter_print("Welcome to the Phase 2 demonstration.", 0.02)
    typewriter_print("This demo showcases the tactical mission resolution system.", 0.02)
    
    time.sleep(2)
    
    # Initialize systems
    print("\n🔧 Initializing game systems...")
    time.sleep(1)
    legal_system = LegalSystem()
    intelligence_system = IntelligenceDatabase()
    relationship_manager = RelationshipManager()
    executor = MissionExecutor(legal_system, intelligence_system, relationship_manager)
    creator = CharacterCreator()
    print("✅ Systems initialized")
    
    # Create team
    print("\n👥 Assembling mission team...")
    time.sleep(1)
    
    team = []
    
    # Leader - stable and experienced
    leader = creator.create_character(
        "Sarah Chen",
        BackgroundType.MILITARY,
        PersonalityTrait.LEADER,
        PersonalityTrait.METHODICAL
    )
    team.append(leader)
    
    # Specialist - skilled but traumatized
    specialist = creator.create_character(
        "Marcus Williams",
        BackgroundType.TECHNICAL,
        PersonalityTrait.ANALYTICAL,
        PersonalityTrait.CAUTIOUS
    )
    # Add trauma
    specialist.emotional_state.apply_trauma(
        trauma_intensity=0.7,
        event_type="witnessed_violence",
        triggers=[TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES]
    )
    team.append(specialist)
    
    # Wild card - unpredictable
    wildcard = creator.create_character(
        "Alex Rivera",
        BackgroundType.CRIMINAL,
        PersonalityTrait.RECKLESS,
        PersonalityTrait.OPPORTUNISTIC
    )
    # Make them fearful and low ideology for betrayal potential
    wildcard.emotional_state.fear = 0.8
    wildcard.ideology_score = 0.2
    team.append(wildcard)
    
    # Set up strained relationship between leader and wildcard
    relationship_manager.create_relationship(
        leader.id,
        wildcard.id,
        RelationshipType.SUBORDINATE,
        RelationshipMetrics(trust=0.3, loyalty=0.4, fear=0.5)
    )
    relationship_manager.create_relationship(
        wildcard.id,
        leader.id,
        RelationshipType.RIVAL,
        RelationshipMetrics(trust=-0.5, loyalty=0.2, fear=0.7)
    )
    
    # Good relationship between leader and specialist
    relationship_manager.create_relationship(
        leader.id,
        specialist.id,
        RelationshipType.COMRADE,
        RelationshipMetrics(trust=0.8, loyalty=0.9)
    )
    
    display_team(team)
    
    time.sleep(3)
    
    # Create mission
    clear_screen()
    print_header("Mission Briefing")
    
    mission = MockMission(
        "OPERATION_BLACKOUT",
        "sabotage",
        "Destroy government surveillance hub",
        ["technical", "stealth", "combat"]
    )
    
    location = MockLocation(
        "central_surveillance",
        "Central Intelligence Building - Server Room",
        8  # High security
    )
    
    equipment = {
        "explosives": 3,
        "hacking_kit": 1,
        "emp_device": 1,
        "smoke_grenades": 4,
        "fake_ids": 3
    }
    
    display_mission_briefing(mission, location)
    
    print("📦 EQUIPMENT:")
    print("-" * 60)
    for item, count in equipment.items():
        print(f"• {item.replace('_', ' ').title()}: {count}")
    
    print("\n⚠️  Warning: High security location. Commencing operation...")
    time.sleep(3)
    
    # Execute mission
    clear_screen()
    print_header("Mission Execution")
    print("🎯 Operation BLACKOUT is now underway...\n")
    
    # Store original output for detailed display
    report = executor.execute_mission(mission, team, location, equipment)
    
    # Simulate real-time execution with animations
    phases = [
        ("PLANNING PHASE", "Team gathers for final briefing..."),
        ("INFILTRATION PHASE", "Approaching target location..."),
        ("EXECUTION PHASE", "Engaging primary objective..."),
        ("EXTRACTION PHASE", "Attempting to withdraw..."),
        ("AFTERMATH", "Analyzing mission results...")
    ]
    
    # Show some key actions during execution
    key_actions = [a for a in report.action_log if not a.success or "betrayal" in a.narrative.lower() or "heroic" in a.details.get("description", "").lower()]
    
    for i, (phase_name, description) in enumerate(phases[:len(report.phases_completed)]):
        print(f"\n🔷 {phase_name}")
        typewriter_print(description, 0.02)
        time.sleep(1)
        
        # Show relevant actions for this phase
        phase_actions = [a for a in key_actions if a.phase.value.upper() in phase_name]
        if phase_actions:
            for action in phase_actions[:2]:
                symbol = "✅" if action.success else "❌"
                print(f"\n  {symbol} {action.narrative}")
                time.sleep(0.5)
        
        # Show complications
        phase_complications = [c for c in report.complications if c.phase.value.upper() in phase_name]
        if phase_complications:
            for comp in phase_complications:
                severity_symbols = {
                    ComplicationSeverity.MINOR: "⚠️",
                    ComplicationSeverity.MODERATE: "⚠️⚠️",
                    ComplicationSeverity.MAJOR: "🚨",
                    ComplicationSeverity.CATASTROPHIC: "💥"
                }
                print(f"\n  {severity_symbols.get(comp.severity, '⚠️')} COMPLICATION: {comp.description}")
                time.sleep(1)
    
    time.sleep(2)
    
    # Display results
    clear_screen()
    print_header("Mission Report")
    
    # Outcome banner
    outcome_banners = {
        MissionOutcome.CRITICAL_SUCCESS: ("🎉 CRITICAL SUCCESS! 🎉", "green"),
        MissionOutcome.SUCCESS: ("✅ MISSION SUCCESS", "green"),
        MissionOutcome.PARTIAL_SUCCESS: ("🟡 PARTIAL SUCCESS", "yellow"),
        MissionOutcome.FAILURE: ("❌ MISSION FAILED", "red"),
        MissionOutcome.DISASTER: ("💀 COMPLETE DISASTER", "red"),
        MissionOutcome.ABORTED: ("🚫 MISSION ABORTED", "red")
    }
    
    banner, color = outcome_banners.get(report.outcome, ("UNKNOWN", "white"))
    print(f"\n{banner}\n")
    
    # Summary stats
    print("📊 MISSION STATISTICS:")
    print("-" * 60)
    print(f"Duration: {(report.end_time - report.start_time).total_seconds():.1f} seconds")
    print(f"Phases Completed: {len(report.phases_completed)}/{len(list(MissionPhase))}")
    print(f"Objectives: {len(report.objectives_completed)} completed, {len(report.objectives_failed)} failed")
    print(f"Team Losses: {len(report.casualties)} KIA, {len(report.captured_agents)} captured")
    print(f"Heat Generated: +{report.heat_generated} 🔥")
    print(f"Public Opinion: {report.public_opinion_shift:+.1%}")
    print(f"Propaganda Value: {report.propaganda_value:.0%}")
    
    # Agent performance
    print("\n👥 AGENT PERFORMANCE:")
    print("-" * 60)
    for agent in team:
        perf = report.agent_performance.get(agent.id)
        if perf:
            score = perf.calculate_performance_score()
            status = "☠️ KIA" if agent.id in report.casualties else "🔒 Captured" if agent.id in report.captured_agents else "✅ Extracted"
            
            print(f"\n{agent.name}: {score:.0%} effectiveness - {status}")
            
            if perf.heroic_moment:
                print("  ⭐ Displayed exceptional heroism!")
            if perf.betrayal_attempted:
                print("  🗡️ BETRAYED THE TEAM!")
            if perf.trauma_triggered:
                print("  😰 Suffered trauma episode")
            if perf.panic_episodes > 0:
                print(f"  😱 Panic episodes: {perf.panic_episodes}")
    
    # Memorable moments
    if report.memorable_moments:
        print("\n🎭 MEMORABLE MOMENTS:")
        print("-" * 60)
        for moment in report.memorable_moments:
            print(f"• {moment}")
    
    # Narrative summary
    print("\n📖 MISSION SUMMARY:")
    print("-" * 60)
    typewriter_print(report.narrative_summary, 0.02)
    
    print(f"\n💭 SYMBOLIC IMPACT: {report.symbolic_impact}")
    
    time.sleep(3)
    
    # Show some action highlights
    print("\n\n📝 ACTION HIGHLIGHTS:")
    print("-" * 60)
    
    # Show first few and last few actions
    interesting_actions = []
    
    # Get failed actions, betrayals, and heroic moments
    for action in report.action_log:
        if (not action.success or 
            "betrayal" in action.narrative.lower() or 
            "heroic" in action.details.get("description", "").lower() or
            "trauma" in action.narrative.lower()):
            interesting_actions.append(action)
    
    # If not enough interesting actions, add some successful ones
    if len(interesting_actions) < 5:
        for action in report.action_log:
            if action.success and len(interesting_actions) < 5:
                interesting_actions.append(action)
    
    for i, action in enumerate(interesting_actions[:5]):
        symbol = "✅" if action.success else "❌"
        agent_name = next((a.name for a in team if a.id == action.agent_id), "Unknown")
        print(f"\n{symbol} [{action.phase.value.upper()}] {agent_name}")
        print(f"   {action.narrative}")
    
    time.sleep(2)
    
    print("\n" + "="*80)
    print("End of demonstration. The Years of Lead continues...")
    print("="*80)
    print("\n✊ Join the resistance. The future is unwritten.")


if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()