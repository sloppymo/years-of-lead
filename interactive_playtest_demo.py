#!/usr/bin/env python3
"""
Years of Lead - Interactive Playtest Demonstration

A guided CLI playthrough to test mission failures, emotional impacts,
cascading effects, and dynamic narrative generation.
"""

import os
import sys
import time
import random
from typing import Dict, List, Any

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🎮 Starting Years of Lead Interactive Playtest Demo...")

try:
    from years_of_lead.core import GameState, Agent, Faction, Location, Task, TaskType, MissionType, AgentRole, SkillType, EquipmentType, Skill, Equipment
    print("✅ Core game systems loaded")
except ImportError as e:
    print(f"❌ Could not import core systems: {e}")
    sys.exit(1)

from game.mission_execution_engine import MissionExecutionEngine, ExecutionOutcome
from game.enhanced_mission_system import EnhancedMissionExecutor
from game.emotional_state import EmotionalState
from loguru import logger


class InteractivePlaytestDemo:
    """Interactive demonstration of Years of Lead gameplay mechanics"""
    
    def __init__(self):
        self.game_state = GameState()
        self.mission_engine = MissionExecutionEngine(self.game_state)
        self.enhanced_mission_executor = EnhancedMissionExecutor(self.game_state)
        self.turn_count = 0
        self.mission_count = 0
        print("✅ Demo initialized")
        
    def setup_playtest_scenario(self):
        """Set up a scenario specifically designed to test failure mechanics"""
        print("🎯 Setting up Playtest Scenario...")
        print("=" * 80)
        
        # Create locations with varying security levels
        locations = [
            Location("university", "University District", security_level=3, unrest_level=8),
            Location("downtown", "Downtown", security_level=9, unrest_level=2),  # High security
            Location("industrial", "Industrial Zone", security_level=6, unrest_level=7),
            Location("government", "Government Quarter", security_level=10, unrest_level=1),  # Maximum security
        ]
        
        for location in locations:
            self.game_state.add_location(location)
        
        # Create factions
        factions = [
            Faction("resistance", "The Resistance", {"money": 100, "influence": 20, "personnel": 5}),
            Faction("students", "Student Movement", {"money": 30, "influence": 40, "personnel": 8}),
        ]
        
        for faction in factions:
            self.game_state.add_faction(faction)
        
        # Create agents with different emotional states for testing
        agents = [
            # Stressed veteran - prone to mission failure
            Agent("alex", "Alex Rivera", "resistance", "university", background="military",
                  skills={SkillType.COMBAT: Skill(SkillType.COMBAT, level=5),
                          SkillType.STEALTH: Skill(SkillType.STEALTH, level=3)},
                  stress=85),  # High stress
            
            # Traumatized operative - emotional instability
            Agent("maria", "Maria Santos", "resistance", "downtown", background="student",
                  skills={SkillType.PERSUASION: Skill(SkillType.PERSUASION, level=4),
                          SkillType.TECHNICAL: Skill(SkillType.TECHNICAL, level=6)},
                  stress=60),
            
            # Inexperienced recruit - low skills
            Agent("carlos", "Carlos Mendez", "students", "industrial", background="civilian",
                  skills={SkillType.SURVIVAL: Skill(SkillType.SURVIVAL, level=2),
                          SkillType.STEALTH: Skill(SkillType.STEALTH, level=1)},
                  stress=30),
            
            # Stable operative - control group
            Agent("elena", "Elena Rodriguez", "students", "university", background="worker",
                  skills={SkillType.TECHNICAL: Skill(SkillType.TECHNICAL, level=7),
                          SkillType.COMBAT: Skill(SkillType.COMBAT, level=4)},
                  stress=20),
        ]
        
        # Set up emotional states with trauma
        for agent in agents:
            emotional_state = EmotionalState()
            
            if agent.id == "alex":
                # Veteran with PTSD
                emotional_state.fear = 0.7
                emotional_state.anger = 0.5
                emotional_state.trauma_level = 0.8
                emotional_state.apply_trauma(0.3, "combat_exposure")
                
            elif agent.id == "maria":
                # Traumatized from previous failure
                emotional_state.sadness = 0.6
                emotional_state.fear = 0.4
                emotional_state.trust = -0.3
                emotional_state.trauma_level = 0.6
                emotional_state.apply_trauma(0.2, "mission_failure")
                
            elif agent.id == "carlos":
                # Anxious newcomer
                emotional_state.fear = 0.5
                emotional_state.anticipation = 0.3
                emotional_state.trust = 0.2
                
            else:  # elena
                # Stable control
                emotional_state.trust = 0.4
                emotional_state.joy = 0.2
                emotional_state.anticipation = 0.3
            
            agent.emotional_state = emotional_state
            self.game_state.add_agent(agent)
        
        print("✅ Scenario setup complete!")
        print(f"   • {len(locations)} locations with varying security levels")
        print(f"   • {len(agents)} agents with different trauma/stress levels")
        print(f"   • Designed to test failure scenarios and cascading effects")
        
    def display_scenario_status(self):
        """Display current scenario status with emotional details"""
        print("\n" + "🎭" * 20)
        print("CURRENT SCENARIO STATUS")
        print("🎭" * 20)
        
        print(f"\n📅 Turn {self.turn_count + 1} | Missions Executed: {self.mission_count}")
        
        print("\n👥 AGENT STATUS & EMOTIONAL STATES:")
        for agent_id, agent in self.game_state.agents.items():
            status_emoji = "✅" if agent.status == "active" else "❌"
            stress_level = "🔴" if agent.stress > 70 else "🟡" if agent.stress > 40 else "🟢"
            
            print(f"\n  {status_emoji} {agent.name} ({agent.background.title()})")
            print(f"     📍 Location: {self.game_state.locations[agent.location_id].name}")
            print(f"     💪 Skills: Combat {getattr(agent.skills.get(SkillType.COMBAT), 'level', 0)}, "
                  f"Stealth {getattr(agent.skills.get(SkillType.STEALTH), 'level', 0)}, "
                  f"Technical {getattr(agent.skills.get(SkillType.TECHNICAL), 'level', 0)}")
            print(f"     {stress_level} Stress: {agent.stress}/100")
            
            if hasattr(agent, 'emotional_state'):
                es = agent.emotional_state
                dominant, intensity = es.get_dominant_emotion()
                trauma_emoji = "🩹" if es.trauma_level > 0.6 else "⚠️" if es.trauma_level > 0.3 else "✨"
                
                print(f"     🧠 Dominant Emotion: {dominant.title()} ({intensity:.2f})")
                print(f"     {trauma_emoji} Trauma Level: {es.trauma_level:.2f}")
                print(f"     🎯 Combat Effectiveness: {es.get_combat_effectiveness():.2f}")
                print(f"     🗣️ Social Effectiveness: {es.get_social_effectiveness():.2f}")
                
                if es.trauma_level > 0.5:
                    print("     ⚠️ HIGH TRAUMA - Mission effectiveness significantly reduced!")
                if agent.stress > 80:
                    print("     🚨 EXTREME STRESS - Agent at risk of breakdown!")
    
    def create_test_mission(self, mission_type: str, difficulty: str = "hard") -> Dict[str, Any]:
        """Create a test mission designed to potentially fail"""
        
        mission_types = {
            "sabotage": {
                "name": "Sabotage Communications Hub",
                "description": "Plant explosives in the government communications center",
                "target_location": "government",
                "base_difficulty": 0.8 if difficulty == "hard" else 0.6,
                "type": "sabotage"
            },
            "assassination": {
                "name": "Eliminate Government Official",
                "description": "Assassinate a key government minister",
                "target_location": "downtown", 
                "base_difficulty": 0.9 if difficulty == "hard" else 0.7,
                "type": "assassination"
            },
            "rescue": {
                "name": "Extract Captured Agent",
                "description": "Rescue a resistance member from government detention",
                "target_location": "government",
                "base_difficulty": 0.85 if difficulty == "hard" else 0.65,
                "type": "rescue"
            },
            "propaganda": {
                "name": "Mass Leaflet Distribution",
                "description": "Distribute anti-government propaganda across the city",
                "target_location": "downtown",
                "base_difficulty": 0.4 if difficulty == "hard" else 0.3,
                "type": "propaganda"
            }
        }
        
        mission_template = mission_types.get(mission_type, mission_types["sabotage"])
        
        return {
            "id": f"test_mission_{self.mission_count}",
            "name": mission_template["name"],
            "description": mission_template["description"],
            "type": mission_template["type"],
            "target_location": mission_template["target_location"],
            "difficulty": difficulty,
            "base_success_chance": 1.0 - mission_template["base_difficulty"],
            "priority": "high",
            "resources_required": {"money": 50, "personnel": 1}
        }
    
    def execute_test_mission(self, mission: Dict[str, Any], selected_agents: List[str]):
        """Execute a mission and analyze results in detail"""
        
        print(f"\n🎯 EXECUTING MISSION: {mission['name']}")
        print("=" * 80)
        print(f"📋 Description: {mission['description']}")
        print(f"📍 Target Location: {mission['target_location']}")
        print(f"⚠️ Difficulty: {mission['difficulty'].title()}")
        print(f"👥 Assigned Agents: {', '.join(selected_agents)}")
        
        # Prepare agent data for mission
        agents_data = []
        for agent_id in selected_agents:
            agent = self.game_state.agents[agent_id]
            agent_data = {
                "id": agent.id,
                "name": agent.name,
                "skills": {skill_type.value: skill.level for skill_type, skill in agent.skills.items()},
                "emotional_state": {
                    "fear": agent.emotional_state.fear,
                    "anger": agent.emotional_state.anger,
                    "trust": agent.emotional_state.trust,
                    "trauma_level": agent.emotional_state.trauma_level
                } if hasattr(agent, 'emotional_state') else {},
                "stress": agent.stress,
                "status": agent.status
            }
            agents_data.append(agent_data)
        
        # Get location data
        target_location = self.game_state.locations[mission['target_location']]
        location_data = {
            "id": target_location.id,
            "name": target_location.name,
            "security_level": target_location.security_level,
            "unrest_level": target_location.unrest_level
        }
        
        # Execute mission using enhanced system
        print("\n🔄 Processing mission execution...")
        
        try:
            # Use enhanced mission executor for detailed results
            result = self.enhanced_mission_executor.execute_enhanced_mission(
                mission, agents_data, location_data, {}
            )
            
            outcome = result["outcome"]
            consequences = result.get("consequences", [])
            emotional_impacts = result.get("emotional_impacts", {})
            relationship_changes = result.get("relationship_changes", {})
            
            print(f"\n🎊 MISSION OUTCOME: {outcome.value.upper().replace('_', ' ')}")
            print("=" * 80)
            
            # Display detailed results
            if outcome in [result["outcome"].PERFECT_SUCCESS, result["outcome"].SUCCESS_WITH_COMPLICATIONS]:
                print("✅ MISSION SUCCESSFUL!")
                print("   The operation achieved its primary objectives.")
            elif outcome in [result["outcome"].PARTIAL_SUCCESS, result["outcome"].PARTIAL_SUCCESS_WITH_CONSEQUENCES]:
                print("🟡 PARTIAL SUCCESS")
                print("   Some objectives achieved, but complications arose.")
            elif outcome in [result["outcome"].TRAGIC_SUCCESS, result["outcome"].PYRRHIC_VICTORY]:
                print("💔 COSTLY SUCCESS")
                print("   Mission succeeded but at great cost to the team.")
            elif outcome in [result["outcome"].BENEFICIAL_FAILURE]:
                print("🔄 BENEFICIAL FAILURE")
                print("   Despite failure, unexpected advantages were gained.")
            else:
                print("❌ MISSION FAILED!")
                print("   The operation did not achieve its objectives.")
            
            # Show consequences in detail
            if consequences:
                print(f"\n📊 CONSEQUENCES ({len(consequences)} total):")
                for i, consequence in enumerate(consequences, 1):
                    print(f"\n  {i}. {consequence.type.upper()}")
                    print(f"     📝 {consequence.description}")
                    
                    if consequence.immediate_effects:
                        print("     ⚡ Immediate Effects:")
                        for effect, value in consequence.immediate_effects.items():
                            print(f"        • {effect}: {value}")
                    
                    if consequence.emotional_impact:
                        print("     🧠 Emotional Impact:")
                        for agent_id, emotions in consequence.emotional_impact.items():
                            agent_name = self.game_state.agents[agent_id].name
                            print(f"        • {agent_name}:")
                            for emotion, change in emotions.items():
                                sign = "+" if change > 0 else ""
                                print(f"          - {emotion}: {sign}{change:.2f}")
                    
                    if hasattr(consequence, 'narrative_hooks') and consequence.narrative_hooks:
                        print("     📖 Narrative Developments:")
                        for hook in consequence.narrative_hooks:
                            print(f"        • {hook}")
            
            # Show collaboration analysis
            if "collaboration_analysis" in result:
                collab = result["collaboration_analysis"]
                print(f"\n🤝 TEAM COLLABORATION ANALYSIS:")
                print(f"   Trust Synergy: {collab.trust_synergy:.2f}")
                print(f"   Skill Complementarity: {collab.skill_complementarity:.2f}")
                print(f"   Communication Efficiency: {collab.communication_efficiency:.2f}")
                print(f"   Group Cohesion: {collab.group_cohesion:.2f}")
                
                if collab.group_cohesion < 0.3:
                    print("   ⚠️ Poor team cohesion contributed to mission difficulties!")
                elif collab.group_cohesion > 0.7:
                    print("   ✨ Excellent teamwork enhanced mission effectiveness!")
            
            # Apply emotional impacts to actual agents
            print(f"\n🧠 EMOTIONAL STATE CHANGES:")
            for agent_id, impacts in emotional_impacts.items():
                agent = self.game_state.agents[agent_id]
                print(f"\n  {agent.name}:")
                
                for emotion, change in impacts.items():
                    if abs(change) > 0.01:  # Only show significant changes
                        sign = "+" if change > 0 else ""
                        change_desc = "increased" if change > 0 else "decreased"
                        print(f"    • {emotion.title()} {change_desc}: {sign}{change:.2f}")
                
                # Check for critical emotional states
                if hasattr(agent, 'emotional_state'):
                    es = agent.emotional_state
                    if es.trauma_level > 0.8:
                        print(f"    🚨 {agent.name} is showing signs of severe trauma!")
                    elif es.trauma_level > 0.6:
                        print(f"    ⚠️ {agent.name} needs psychological support")
                    
                    if not es.is_psychologically_stable():
                        print(f"    💔 {agent.name} is psychologically unstable!")
            
            # Show relationship changes
            if relationship_changes:
                print(f"\n💕 RELATIONSHIP CHANGES:")
                for (agent_a_id, agent_b_id), changes in relationship_changes.items():
                    agent_a = self.game_state.agents[agent_a_id].name
                    agent_b = self.game_state.agents[agent_b_id].name
                    print(f"\n  {agent_a} ↔ {agent_b}:")
                    
                    for aspect, change in changes.items():
                        if abs(change) > 0.01:
                            sign = "+" if change > 0 else ""
                            print(f"    • {aspect.title()}: {sign}{change:.2f}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error executing mission: {e}")
            return None
    
    def analyze_cascading_effects(self):
        """Analyze and display cascading effects across the network"""
        print(f"\n🌊 CASCADING EFFECTS ANALYSIS")
        print("=" * 80)
        
        # Analyze network stress
        total_stress = sum(agent.stress for agent in self.game_state.agents.values())
        avg_stress = total_stress / len(self.game_state.agents)
        
        high_stress_agents = [agent for agent in self.game_state.agents.values() if agent.stress > 70]
        traumatized_agents = [agent for agent in self.game_state.agents.values() 
                             if hasattr(agent, 'emotional_state') and agent.emotional_state.trauma_level > 0.5]
        
        print(f"📊 Network Stress Metrics:")
        print(f"   • Average Stress Level: {avg_stress:.1f}/100")
        print(f"   • High Stress Agents: {len(high_stress_agents)}/{len(self.game_state.agents)}")
        print(f"   • Traumatized Agents: {len(traumatized_agents)}/{len(self.game_state.agents)}")
        
        if len(high_stress_agents) > len(self.game_state.agents) / 2:
            print("   🚨 NETWORK STRESS CRITICAL - Risk of organizational collapse!")
        elif len(traumatized_agents) > 2:
            print("   ⚠️ High trauma levels affecting network effectiveness")
        
        # Faction resource impact
        print(f"\n💰 Faction Resource Status:")
        for faction_id, faction in self.game_state.factions.items():
            print(f"   • {faction.name}: ${faction.resources.get('money', 0)} "
                  f"(Influence: {faction.resources.get('influence', 0)})")
            
            if faction.resources.get('money', 0) < 50:
                print(f"     ⚠️ {faction.name} critically low on funds!")
    
    def run_interactive_playtest(self):
        """Run the interactive playtest demonstration"""
        
        print("\n" + "🎮" * 25)
        print("YEARS OF LEAD - INTERACTIVE PLAYTEST DEMONSTRATION")
        print("Testing Mission Failures & Cascading Effects")
        print("🎮" * 25)
        
        print("\n🎯 This demo will help you test:")
        print("• Mission failure scenarios and consequences")
        print("• Emotional impact on agents")
        print("• Relationship changes between agents")
        print("• Cascading effects across the network")
        print("• Dynamic narrative generation")
        
        input("\nPress Enter to begin...")
        
        self.setup_playtest_scenario()
        
        while True:
            self.display_scenario_status()
            
            print(f"\n{'🎯' * 20}")
            print("PLAYTEST MENU")
            print("🎯" * 20)
            print("\n1. 💥 Execute High-Risk Sabotage Mission (likely to fail)")
            print("2. 🎯 Execute Assassination Mission (extreme difficulty)")
            print("3. 🚁 Execute Rescue Mission (moderate risk)")
            print("4. 📢 Execute Propaganda Mission (low risk)")
            print("5. 🔄 Advance Turn (apply stress decay & trauma recovery)")
            print("6. 🌊 Analyze Cascading Effects")
            print("7. 📊 View Detailed Agent Report")
            print("8. 🎭 Apply Random Stress Event")
            print("9. ❌ Exit Demonstration")
            
            choice = input("\nSelect option (1-9): ").strip()
            
            if choice == "1":
                # High-risk sabotage mission
                mission = self.create_test_mission("sabotage", "hard")
                available_agents = [aid for aid, agent in self.game_state.agents.items() 
                                  if agent.status == "active"]
                
                print(f"\nAvailable agents: {', '.join(available_agents)}")
                selected = input("Enter agent IDs (space-separated): ").strip().split()
                selected = [s for s in selected if s in available_agents]
                
                if selected:
                    result = self.execute_test_mission(mission, selected)
                    self.mission_count += 1
                
            elif choice == "2":
                # Assassination mission
                mission = self.create_test_mission("assassination", "hard")
                available_agents = [aid for aid, agent in self.game_state.agents.items() 
                                  if agent.status == "active"]
                
                print(f"\nAvailable agents: {', '.join(available_agents)}")
                selected = input("Enter agent IDs (space-separated): ").strip().split()
                selected = [s for s in selected if s in available_agents]
                
                if selected:
                    result = self.execute_test_mission(mission, selected)
                    self.mission_count += 1
                
            elif choice == "3":
                # Rescue mission
                mission = self.create_test_mission("rescue", "hard")
                available_agents = [aid for aid, agent in self.game_state.agents.items() 
                                  if agent.status == "active"]
                
                print(f"\nAvailable agents: {', '.join(available_agents)}")
                selected = input("Enter agent IDs (space-separated): ").strip().split()
                selected = [s for s in selected if s in available_agents]
                
                if selected:
                    result = self.execute_test_mission(mission, selected)
                    self.mission_count += 1
                
            elif choice == "4":
                # Low-risk propaganda mission
                mission = self.create_test_mission("propaganda", "normal")
                available_agents = [aid for aid, agent in self.game_state.agents.items() 
                                  if agent.status == "active"]
                
                print(f"\nAvailable agents: {', '.join(available_agents)}")
                selected = input("Enter agent IDs (space-separated): ").strip().split()
                selected = [s for s in selected if s in available_agents]
                
                if selected:
                    result = self.execute_test_mission(mission, selected)
                    self.mission_count += 1
                
            elif choice == "5":
                # Advance turn
                self.advance_turn()
                
            elif choice == "6":
                # Analyze cascading effects
                self.analyze_cascading_effects()
                
            elif choice == "7":
                # Detailed agent report
                self.show_detailed_agent_report()
                
            elif choice == "8":
                # Apply random stress event
                self.apply_random_stress_event()
                
            elif choice == "9":
                print("\n👋 Ending playtest demonstration.")
                print("Thank you for testing Years of Lead!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-9.")
            
            input("\nPress Enter to continue...")
    
    def advance_turn(self):
        """Advance the game turn and apply natural effects"""
        self.turn_count += 1
        print(f"\n⏰ ADVANCING TO TURN {self.turn_count}")
        print("=" * 50)
        
        # Apply stress decay and trauma recovery
        for agent in self.game_state.agents.values():
            # Gradual stress reduction
            old_stress = agent.stress
            agent.stress = max(0, agent.stress - random.randint(5, 15))
            
            print(f"📉 {agent.name}: Stress {old_stress} → {agent.stress}")
            
            # Emotional state changes
            if hasattr(agent, 'emotional_state'):
                agent.emotional_state.apply_drift()
                
                # Slight trauma recovery over time
                if agent.emotional_state.trauma_level > 0:
                    old_trauma = agent.emotional_state.trauma_level
                    agent.emotional_state.trauma_level = max(0.0, 
                        agent.emotional_state.trauma_level - random.uniform(0.01, 0.05))
                    
                    if old_trauma != agent.emotional_state.trauma_level:
                        print(f"🩹 {agent.name}: Trauma recovery {old_trauma:.2f} → {agent.emotional_state.trauma_level:.2f}")
    
    def show_detailed_agent_report(self):
        """Show detailed psychological and operational report for all agents"""
        print(f"\n📋 DETAILED AGENT PSYCHOLOGICAL REPORT")
        print("=" * 80)
        
        for agent in self.game_state.agents.values():
            print(f"\n👤 {agent.name.upper()} ({agent.background.title()})")
            print("-" * 50)
            print(f"📍 Current Location: {self.game_state.locations[agent.location_id].name}")
            print(f"⚡ Status: {agent.status.title()}")
            print(f"🔥 Stress Level: {agent.stress}/100")
            
            if hasattr(agent, 'emotional_state'):
                es = agent.emotional_state
                print(f"\n🧠 PSYCHOLOGICAL PROFILE:")
                print(f"   Fear: {es.fear:.2f} | Anger: {es.anger:.2f} | Trust: {es.trust:.2f}")
                print(f"   Joy: {es.joy:.2f} | Sadness: {es.sadness:.2f}")
                print(f"   Trauma Level: {es.trauma_level:.2f}")
                
                dominant, intensity = es.get_dominant_emotion()
                print(f"   Dominant Emotion: {dominant.title()} ({intensity:.2f})")
                
                stability = es.get_emotional_stability()
                combat_eff = es.get_combat_effectiveness()
                social_eff = es.get_social_effectiveness()
                
                print(f"\n🎯 OPERATIONAL EFFECTIVENESS:")
                print(f"   Psychological Stability: {stability:.2f}")
                print(f"   Combat Effectiveness: {combat_eff:.2f}")
                print(f"   Social Effectiveness: {social_eff:.2f}")
                
                if es.trauma_level > 0.6:
                    print(f"   🚨 CRITICAL: Severe trauma affecting all operations")
                elif es.trauma_level > 0.3:
                    print(f"   ⚠️ WARNING: Moderate trauma reducing effectiveness")
                
                if not es.is_psychologically_stable():
                    print(f"   💔 UNSTABLE: Agent requires immediate psychological intervention")
            
            print(f"\n💪 SKILL ASSESSMENT:")
            for skill_type, skill in agent.skills.items():
                print(f"   {skill_type.value.title()}: {skill.level}/10")
    
    def apply_random_stress_event(self):
        """Apply a random stressful event to test emotional responses"""
        events = [
            ("Government Raid", "A safe house was raided by authorities", 25),
            ("Comrade Captured", "A fellow resistance member was arrested", 20),
            ("Mission Intel Leaked", "Operational security has been compromised", 15),
            ("Public Crackdown", "Government announces martial law", 30),
            ("Betrayal Rumors", "Suspicions of a mole within the organization", 20),
        ]
        
        event_name, description, stress_increase = random.choice(events)
        
        print(f"\n🚨 RANDOM STRESS EVENT: {event_name}")
        print("=" * 60)
        print(f"📝 {description}")
        print(f"⚡ Network Stress Impact: +{stress_increase} to all active agents")
        
        for agent in self.game_state.agents.values():
            if agent.status == "active":
                old_stress = agent.stress
                agent.stress = min(100, agent.stress + stress_increase)
                print(f"   {agent.name}: {old_stress} → {agent.stress}")
                
                # Apply emotional impact
                if hasattr(agent, 'emotional_state'):
                    agent.emotional_state.fear = min(1.0, agent.emotional_state.fear + 0.2)
                    agent.emotional_state.trust = max(-1.0, agent.emotional_state.trust - 0.1)


def main():
    """Run the interactive playtest demonstration"""
    try:
        demo = InteractivePlaytestDemo()
        demo.run_interactive_playtest()
    except KeyboardInterrupt:
        print("\n\n🛑 Demonstration interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        logger.exception("Playtest demonstration error")


if __name__ == "__main__":
    main() 