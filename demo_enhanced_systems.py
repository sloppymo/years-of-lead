#!/usr/bin/env python3
"""
Years of Lead - Enhanced Systems Demonstration

Comprehensive demonstration of all enhanced simulation systems:
- Phase 1: Agent Autonomy Enhancement
- Phase 2: Mission Outcome Enhancement
- Phase 3: Real-time Intelligence Systems
- Phase 4: Dynamic Narrative Generation
- Phase 5: Advanced Trauma and Psychological Impact
- Integration System

This script demonstrates the complete enhanced simulation experience.
"""

import sys
import os
import random
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"🚀 {title}")
    print("=" * 80)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 60)

def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n  🔹 {title}")
    print("  " + "-" * 40)

def create_demo_game_state():
    """Create a demo game state with multiple agents"""
    from game.core import GameState, Agent
    from game.emotional_state import EmotionalState
    from game.relationships import Relationship, BondType
    
    # Create game state
    game_state = GameState()
    game_state.agents = {}
    game_state.locations = {
        "downtown": {"name": "Downtown District", "type": "urban"},
        "industrial": {"name": "Industrial District", "type": "industrial"},
        "residential": {"name": "Residential District", "type": "residential"},
        "government": {"name": "Government District", "type": "government"}
    }
    game_state.factions = {
        "resistance": {"name": "Resistance Movement", "type": "rebel"},
        "government": {"name": "Government Forces", "type": "authority"},
        "neutral": {"name": "Neutral Faction", "type": "neutral"}
    }
    game_state.turn_number = 1
    
    # Create agents with different backgrounds and emotional states
    agent_data = [
        {
            "id": "agent_001", "name": "Maria Santos", "background": "veteran",
            "faction": "resistance", "location": "downtown",
            "stress": 65, "loyalty": 85,
            "trauma": 0.4, "fear": 0.3, "anger": 0.2, "trust": 0.6
        },
        {
            "id": "agent_002", "name": "James Chen", "background": "student",
            "faction": "resistance", "location": "residential",
            "stress": 45, "loyalty": 70,
            "trauma": 0.2, "fear": 0.4, "anger": 0.1, "trust": 0.5
        },
        {
            "id": "agent_003", "name": "Elena Rodriguez", "background": "organizer",
            "faction": "resistance", "location": "industrial",
            "stress": 80, "loyalty": 90,
            "trauma": 0.6, "fear": 0.5, "anger": 0.3, "trust": 0.7
        },
        {
            "id": "agent_004", "name": "David Kim", "background": "insider",
            "faction": "government", "location": "government",
            "stress": 90, "loyalty": 40,
            "trauma": 0.8, "fear": 0.7, "anger": 0.6, "trust": 0.2
        }
    ]
    
    for data in agent_data:
        agent = Agent(
            id=data["id"],
            name=data["name"],
            faction_id=data["faction"],
            location_id=data["location"]
        )
        agent.background = data["background"]
        agent.status = "active"
        agent.stress = data["stress"]
        agent.loyalty = data["loyalty"]
        
        # Add emotional state
        agent.emotional_state = EmotionalState()
        agent.emotional_state.trauma_level = data["trauma"]
        agent.emotional_state.fear = data["fear"]
        agent.emotional_state.anger = data["anger"]
        agent.emotional_state.trust = data["trust"]
        
        # Add skills
        agent.skills = {
            "intelligence": type('obj', (), {'level': random.randint(2, 5)})(),
            "social": type('obj', (), {'level': random.randint(2, 5)})(),
            "combat": type('obj', (), {'level': random.randint(2, 5)})(),
            "technical": type('obj', (), {'level': random.randint(2, 5)})()
        }
        
        # Add relationships
        agent.relationships = {}
        
        game_state.agents[agent.id] = agent
    
    # Create some relationships between agents
    resistance_agents = [aid for aid, agent in game_state.agents.items() 
                        if agent.faction_id == "resistance"]
    
    for i, agent_a_id in enumerate(resistance_agents):
        for agent_b_id in resistance_agents[i+1:]:
            # Create positive relationships between resistance agents
            rel = Relationship(
                agent_id=agent_b_id,
                bond_type=BondType.COMRADE,
                affinity=random.randint(20, 60),
                trust=random.uniform(0.6, 0.9),
                loyalty=random.uniform(0.7, 1.0)
            )
            game_state.agents[agent_a_id].relationships[agent_b_id] = rel
    
    return game_state

def demonstrate_agent_autonomy(game_state):
    """Demonstrate Phase 1: Agent Autonomy Enhancement"""
    print_section("PHASE 1: AGENT AUTONOMY ENHANCEMENT")
    
    try:
        from game.enhanced_agent_autonomy import EnhancedAgentAutonomySystem
        
        print_subsection("Initializing Agent Autonomy System")
        autonomy_system = EnhancedAgentAutonomySystem(game_state)
        
        # Initialize autonomy for all agents
        for agent_id in game_state.agents:
            autonomy_system.initialize_agent_autonomy(agent_id)
        
        print(f"  ✅ Initialized autonomy for {len(game_state.agents)} agents")
        
        print_subsection("Processing Autonomous Decisions")
        results = autonomy_system.process_autonomous_decisions()
        
        print(f"  📊 Decisions Made: {len(results.get('decisions_made', []))}")
        print(f"  🎯 Actions Taken: {len(results.get('actions_taken', []))}")
        print(f"  📖 Narrative Events: {len(results.get('narrative_events', []))}")
        
        # Show some autonomous decisions
        for decision in results.get('decisions_made', [])[:3]:
            agent = game_state.agents.get(decision.agent_id)
            if agent:
                print(f"    • {agent.name}: {decision.action_type.value} (Risk: {decision.risk_level:.2f})")
        
        # Show narrative events
        for event in results.get('narrative_events', [])[:2]:
            print(f"    📝 {event}")
        
        return autonomy_system
        
    except ImportError as e:
        print(f"  ❌ Agent Autonomy System not available: {e}")
        return None

def demonstrate_intelligence_system(game_state):
    """Demonstrate Phase 3: Real-time Intelligence Systems"""
    print_section("PHASE 3: REAL-TIME INTELLIGENCE SYSTEMS")
    
    try:
        from game.enhanced_intelligence_system import EnhancedIntelligenceSystem
        
        print_subsection("Initializing Intelligence System")
        intelligence_system = EnhancedIntelligenceSystem(game_state)
        
        print_subsection("Processing Real-time Intelligence")
        results = intelligence_system.process_real_time_intelligence()
        
        print(f"  📊 New Intelligence: {len(results.get('new_intelligence', []))}")
        print(f"  🔍 Patterns Detected: {len(results.get('patterns_detected', []))}")
        print(f"  ⚠️ Priority Alerts: {len(results.get('priority_alerts', []))}")
        print(f"  🎯 Actionable Intel: {len(results.get('actionable_intel', []))}")
        
        # Show some intelligence events
        for intel in results.get('new_intelligence', [])[:3]:
            print(f"    📡 {intel.content if hasattr(intel, 'content') else 'Intelligence event'}")
        
        # Show patterns
        for pattern in results.get('patterns_detected', [])[:2]:
            print(f"    🔍 Pattern: {pattern.description} (Confidence: {pattern.confidence:.1%})")
        
        # Show alerts
        for alert in results.get('priority_alerts', [])[:2]:
            print(f"    ⚠️ Alert: {alert.get('message', 'Priority alert')}")
        
        return intelligence_system
        
    except ImportError as e:
        print(f"  ❌ Intelligence System not available: {e}")
        return None

def demonstrate_narrative_system(game_state):
    """Demonstrate Phase 4: Dynamic Narrative Generation"""
    print_section("PHASE 4: DYNAMIC NARRATIVE GENERATION")
    
    try:
        from game.enhanced_narrative_system import EnhancedDynamicNarrativeSystem
        
        print_subsection("Initializing Narrative System")
        narrative_system = EnhancedDynamicNarrativeSystem(game_state)
        
        print_subsection("Processing Dynamic Narrative")
        results = narrative_system.process_dynamic_narrative()
        
        print(f"  📖 New Arcs: {len(results.get('new_arcs', []))}")
        print(f"  🔄 Arc Advancements: {len(results.get('arc_advancements', []))}")
        print(f"  📝 Story Events: {len(results.get('story_events', []))}")
        print(f"  🎣 Triggered Hooks: {len(results.get('triggered_hooks', []))}")
        
        # Show narrative arcs
        for arc in results.get('new_arcs', [])[:2]:
            agent_names = [game_state.agents.get(aid, type('obj', (), {'name': f'Agent_{aid}'})).name 
                          for aid in arc.agents_involved]
            print(f"    📖 Arc: {arc.arc_type.value} involving {', '.join(agent_names)}")
        
        # Show story events
        for event in results.get('story_events', [])[:3]:
            print(f"    📝 {event.get('description', 'Story event')}")
        
        return narrative_system
        
    except ImportError as e:
        print(f"  ❌ Narrative System not available: {e}")
        return None

def demonstrate_trauma_system(game_state):
    """Demonstrate Phase 5: Advanced Trauma and Psychological Impact"""
    print_section("PHASE 5: ADVANCED TRAUMA AND PSYCHOLOGICAL IMPACT")
    
    try:
        from game.advanced_trauma_system import AdvancedTraumaSystem
        
        print_subsection("Initializing Trauma System")
        trauma_system = AdvancedTraumaSystem(game_state)
        
        print_subsection("Processing Trauma System")
        results = trauma_system.process_trauma_system()
        
        print(f"  💔 New Trauma Events: {len(results.get('new_trauma_events', []))}")
        print(f"  🔄 Trauma Recovery: {len(results.get('trauma_recovery', []))}")
        print(f"  🧠 Psychological Crises: {len(results.get('psychological_crises', []))}")
        print(f"  ✨ Healing Breakthroughs: {len(results.get('healing_breakthroughs', []))}")
        
        # Show trauma events
        for trauma in results.get('new_trauma_events', [])[:2]:
            agent = game_state.agents.get(trauma.get('agent_id', ''))
            if agent:
                print(f"    💔 {agent.name}: {trauma.get('description', 'Trauma event')}")
        
        # Show psychological crises
        for crisis in results.get('psychological_crises', [])[:2]:
            agent = game_state.agents.get(crisis.get('agent_id', ''))
            if agent:
                print(f"    🧠 {agent.name}: {crisis.get('crisis_type', 'Crisis')} - {crisis.get('description', '')}")
        
        return trauma_system
        
    except ImportError as e:
        print(f"  ❌ Trauma System not available: {e}")
        return None

def demonstrate_mission_system(game_state):
    """Demonstrate Phase 2: Mission Outcome Enhancement"""
    print_section("PHASE 2: MISSION OUTCOME ENHANCEMENT")
    
    try:
        from game.enhanced_mission_system import EnhancedMissionExecutor
        
        print_subsection("Initializing Mission System")
        mission_system = EnhancedMissionExecutor(game_state)
        
        # Create a test mission
        mission = {
            "id": "demo_mission_001",
            "type": "intelligence",
            "difficulty": "medium",
            "description": "Gather intelligence on government activities"
        }
        
        # Select agents for mission
        resistance_agents = [a for a in game_state.agents.values() if a.faction_id == "resistance"]
        mission_agents = resistance_agents[:2]  # Take first 2 resistance agents
        
        agents_data = []
        for agent in mission_agents:
            agents_data.append({
                "id": agent.id,
                "name": agent.name,
                "skills": agent.skills,
                "emotional_state": {
                    "trauma_level": agent.emotional_state.trauma_level,
                    "fear": agent.emotional_state.fear,
                    "anger": agent.emotional_state.anger,
                    "trust": agent.emotional_state.trust
                }
            })
        
        location = {"id": "government", "name": "Government District"}
        resources = {"budget": 1000, "time": 5, "equipment": "standard"}
        
        print_subsection("Executing Enhanced Mission")
        print(f"  🎯 Mission: {mission['description']}")
        print(f"  👥 Agents: {', '.join([agent['name'] for agent in agents_data])}")
        print(f"  📍 Location: {location['name']}")
        
        result = mission_system.execute_enhanced_mission(mission, agents_data, location, resources)
        
        print(f"  📊 Outcome: {result['outcome']}")
        
        # Show collaboration analysis
        collaboration = result.get('collaboration_analysis')
        if collaboration:
            print(f"  🎭 Collaboration Score: {collaboration.group_cohesion:.2f}")
            print(f"  🤝 Trust Synergy: {collaboration.trust_synergy:.2f}")
            print(f"  🛠️ Skill Complementarity: {collaboration.skill_complementarity:.2f}")
        
        # Show consequences
        consequences = result.get('consequences', [])
        print(f"  📋 Consequences: {len(consequences)}")
        for consequence in consequences[:2]:
            print(f"    • {consequence.description}")
        
        # Show emotional impacts
        emotional_impacts = result.get('emotional_impacts', {})
        print(f"  💔 Emotional Impacts: {len(emotional_impacts)} agents affected")
        
        # Show relationship changes
        relationship_changes = result.get('relationship_changes', {})
        print(f"  🔗 Relationship Changes: {len(relationship_changes)} relationships modified")
        
        return mission_system
        
    except ImportError as e:
        print(f"  ❌ Mission System not available: {e}")
        return None

def demonstrate_integration_system(game_state):
    """Demonstrate the complete integration system"""
    print_section("ENHANCED SIMULATION INTEGRATION")
    
    try:
        from game.enhanced_simulation_integration import EnhancedSimulationIntegration
        
        print_subsection("Initializing Integration System")
        integration_system = EnhancedSimulationIntegration(game_state)
        
        print_subsection("Running Enhanced Simulation (3 Turns)")
        
        for turn_num in range(3):
            print(f"\n  🔄 Turn {turn_num + 1}")
            game_state.turn_number = turn_num + 1
            
            turn = integration_system.process_enhanced_turn()
            
            print(f"    📊 Autonomy: {len(turn.autonomy_results.get('decisions_made', []))} decisions")
            print(f"    📡 Intelligence: {len(turn.intelligence_results.get('new_intelligence', []))} events")
            print(f"    📖 Narrative: {len(turn.narrative_results.get('story_events', []))} events")
            print(f"    💔 Trauma: {len(turn.trauma_results.get('new_trauma_events', []))} events")
            print(f"    🔗 Integration: {len(turn.integration_events)} events")
            print(f"    ⚡ Synergies: {len(turn.system_synergies)} synergies")
        
        print_subsection("Integration Summary")
        summary = integration_system.get_integration_summary()
        
        print(f"  📈 Total Turns: {summary.get('total_turns_processed', 0)}")
        print(f"  🎯 System Performance: {summary.get('system_performance', {})}")
        print(f"  🔗 Integration Metrics: {summary.get('integration_metrics', {})}")
        print(f"  ⚡ System Synergies: {summary.get('system_synergies', 0)}")
        
        # Show system status
        system_status = summary.get('system_status', {})
        for system, status in system_status.items():
            status_icon = "✅" if status else "❌"
            print(f"    {status_icon} {system.title()}: {'Active' if status else 'Inactive'}")
        
        return integration_system
        
    except ImportError as e:
        print(f"  ❌ Integration System not available: {e}")
        return None

def demonstrate_agent_state_changes(game_state):
    """Demonstrate how agent states change throughout the simulation"""
    print_section("AGENT STATE EVOLUTION")
    
    print_subsection("Initial Agent States")
    for agent_id, agent in game_state.agents.items():
        print(f"  👤 {agent.name}:")
        print(f"    Stress: {agent.stress}/100")
        print(f"    Loyalty: {agent.loyalty}/100")
        print(f"    Trauma: {agent.emotional_state.trauma_level:.2f}")
        print(f"    Fear: {agent.emotional_state.fear:.2f}")
        print(f"    Anger: {agent.emotional_state.anger:.2f}")
    
    print_subsection("After Enhanced Systems Processing")
    # Process a few turns to show state changes
    try:
        from game.enhanced_simulation_integration import EnhancedSimulationIntegration
        integration_system = EnhancedSimulationIntegration(game_state)
        
        for turn_num in range(2):
            game_state.turn_number = turn_num + 1
            integration_system.process_enhanced_turn()
        
        for agent_id, agent in game_state.agents.items():
            print(f"  👤 {agent.name}:")
            print(f"    Stress: {agent.stress}/100")
            print(f"    Loyalty: {agent.loyalty}/100")
            print(f"    Trauma: {agent.emotional_state.trauma_level:.2f}")
            print(f"    Fear: {agent.emotional_state.fear:.2f}")
            print(f"    Anger: {agent.emotional_state.anger:.2f}")
            
    except ImportError:
        print("  ⚠️ Integration system not available for state evolution demonstration")

def main():
    """Main demonstration function"""
    print_header("YEARS OF LEAD - ENHANCED SYSTEMS DEMONSTRATION")
    print("This demonstration showcases all enhanced simulation systems working together.")
    print("Each phase builds upon the previous ones to create a comprehensive simulation experience.")
    
    # Create demo game state
    print_section("SETTING UP DEMO ENVIRONMENT")
    game_state = create_demo_game_state()
    print(f"  ✅ Created game state with {len(game_state.agents)} agents")
    print(f"  📍 {len(game_state.locations)} locations available")
    print(f"  🏛️ {len(game_state.factions)} factions active")
    
    # Demonstrate each enhanced system
    autonomy_system = demonstrate_agent_autonomy(game_state)
    intelligence_system = demonstrate_intelligence_system(game_state)
    narrative_system = demonstrate_narrative_system(game_state)
    trauma_system = demonstrate_trauma_system(game_state)
    mission_system = demonstrate_mission_system(game_state)
    
    # Demonstrate integration
    integration_system = demonstrate_integration_system(game_state)
    
    # Show agent state evolution
    demonstrate_agent_state_changes(game_state)
    
    # Final summary
    print_header("DEMONSTRATION COMPLETE")
    print("The enhanced Years of Lead simulation systems have been demonstrated.")
    print("\nKey Features Demonstrated:")
    print("  🎯 Agent Autonomy: Agents make independent decisions based on emotional state")
    print("  📡 Intelligence: Real-time intelligence gathering and pattern analysis")
    print("  📖 Narrative: Dynamic story generation based on agent interactions")
    print("  💔 Trauma: Advanced psychological impact and recovery systems")
    print("  🎭 Missions: Enhanced mission outcomes with collaboration effects")
    print("  🔗 Integration: All systems working together seamlessly")
    
    print("\nThe simulation now features:")
    print("  • Autonomous agent behavior with emotional intelligence")
    print("  • Complex mission outcomes with multi-agent collaboration")
    print("  • Real-time intelligence networks with pattern detection")
    print("  • Dynamic narrative generation with emergent storylines")
    print("  • Advanced trauma systems with generational impact")
    print("  • Seamless integration of all systems")
    
    print("\nThis represents a significant enhancement to the core simulation,")
    print("providing a rich, dynamic, and emotionally complex gaming experience.")

if __name__ == "__main__":
    main() 