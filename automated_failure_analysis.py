#!/usr/bin/env python3
"""
Enhanced Automated Failure Analysis for Years of Lead
Comprehensive testing of mission failures, emotional impact, and cascading effects
"""

import json
import random
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path for game imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

class FailureAnalyzer:
    def __init__(self):
        self.data = {
            "missions": [], 
            "analysis": {},
            "emotional_impact": [],
            "cascading_effects": [],
            "agent_performance": [],
            "system_stability": {}
        }
        self.game_state = None
        self.mission_engine = None
        self.test_count = 0
        self.error_count = 0
    
    def run_analysis(self):
        print("🤖 Running Enhanced Automated Failure Analysis")
        print("=" * 60)
        print("Testing: Mission failures, emotional impact, cascading effects")
        print("=" * 60)
        
        # Initialize game systems
        if not self.initialize_game_systems():
            print("❌ Failed to initialize game systems")
            return
        
        # Run comprehensive tests
        self.test_mission_failures()
        self.test_emotional_impact()
        self.test_cascading_effects() 
        self.test_multi_agent_scenarios()
        self.test_system_stability()
        
        # Analyze patterns
        self.analyze_patterns()
        self.save_results()
    
    def initialize_game_systems(self):
        """Initialize game systems for real testing"""
        try:
            from game.core import GameState
            from game.mission_execution_engine import MissionExecutionEngine
            
            print("🔧 Initializing game systems...")
            self.game_state = GameState()
            self.game_state.initialize_game()
            
            self.mission_engine = MissionExecutionEngine(self.game_state)
            
            print(f"✅ Systems initialized: {len(self.game_state.agents)} agents, "
                  f"{len(self.game_state.locations)} locations")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            return False
    
    def test_mission_failures(self):
        """Test actual mission failure scenarios"""
        print("\n🎯 Testing Mission Failure Scenarios...")
        
        mission_types = ["sabotage", "intelligence", "propaganda", "recruitment"]
        failure_scenarios = [
            {"name": "High Security", "security_level": 9},
            {"name": "Stressed Agents", "stress_modifier": 0.8},
            {"name": "Poor Equipment", "equipment_failure": True},
            {"name": "Betrayal Risk", "betrayal_chance": 0.3}
        ]
        
        for scenario in failure_scenarios:
            for mission_type in mission_types[:2]:  # Test 2 types per scenario
                try:
                    result = self.execute_real_mission(mission_type, scenario)
                    self.data["missions"].append(result)
                    print(f"  🎯 {mission_type} ({scenario['name']}): {result['outcome']}")
                    self.test_count += 1
                except Exception as e:
                    print(f"  ❌ Error in {mission_type}: {e}")
                    self.error_count += 1
    
    def test_emotional_impact(self):
        """Test emotional state impact on performance"""
        print("\n💔 Testing Emotional Impact...")
        
        # Find agents with emotional states
        emotional_agents = []
        for agent in self.game_state.agents.values():
            if hasattr(agent, 'emotional_state') and agent.emotional_state:
                emotional_agents.append(agent)
        
        if not emotional_agents:
            print("  ⚠️ No agents with emotional states found")
            return
        
        # Test emotional impact
        for agent in emotional_agents[:3]:  # Test first 3
            try:
                emotional_data = self.analyze_agent_emotions(agent)
                self.data["emotional_impact"].append(emotional_data)
                print(f"  💔 {agent.name}: {emotional_data['dominant_emotion']} "
                      f"(Trauma: {emotional_data['trauma_level']:.2f})")
                self.test_count += 1
            except Exception as e:
                print(f"  ❌ Error analyzing {agent.name}: {e}")
                self.error_count += 1
    
    def test_cascading_effects(self):
        """Test cascading failure effects"""
        print("\n🌊 Testing Cascading Effects...")
        
        try:
            # Capture initial state
            initial_state = self.capture_network_state()
            
            # Trigger multiple failures
            cascade_effects = []
            for i in range(3):
                failure_result = self.trigger_cascade_failure(i)
                cascade_effects.append(failure_result)
                print(f"  🌊 Cascade {i+1}: {failure_result['impact']}")
                self.test_count += 1
            
            # Analyze cascading impact
            final_state = self.capture_network_state()
            cascade_analysis = self.analyze_cascade_impact(initial_state, final_state)
            self.data["cascading_effects"] = cascade_analysis
            
        except Exception as e:
            print(f"  ❌ Cascading effects test failed: {e}")
            self.error_count += 1
    
    def test_multi_agent_scenarios(self):
        """Test multi-agent interactions"""
        print("\n👥 Testing Multi-Agent Scenarios...")
        
        if len(self.game_state.agents) < 2:
            print("  ⚠️ Not enough agents for multi-agent testing")
            return
        
        agents_list = list(self.game_state.agents.values())
        
        # Test 2-agent mission
        try:
            team_result = self.test_team_mission(agents_list[:2], "2-agent team")
            self.data["agent_performance"].append(team_result)
            print(f"  👥 2-agent team: {team_result['outcome']}")
            self.test_count += 1
        except Exception as e:
            print(f"  ❌ 2-agent test failed: {e}")
            self.error_count += 1
        
        # Test 3-agent mission if possible
        if len(agents_list) >= 3:
            try:
                team_result = self.test_team_mission(agents_list[:3], "3-agent team")
                self.data["agent_performance"].append(team_result)
                print(f"  👥 3-agent team: {team_result['outcome']}")
                self.test_count += 1
            except Exception as e:
                print(f"  ❌ 3-agent test failed: {e}")
                self.error_count += 1
    
    def test_system_stability(self):
        """Test system stability over time"""
        print("\n⏰ Testing System Stability...")
        
        stability_metrics = []
        
        # Run stability test over multiple turns
        for turn in range(10):
            try:
                import time
                start_time = time.time()
                
                # Advance game turn
                self.game_state.advance_turn()
                
                # Measure performance
                turn_time = time.time() - start_time
                stability_metrics.append({
                    "turn": turn,
                    "processing_time": turn_time,
                    "active_agents": len([a for a in self.game_state.agents.values() if a.status == "active"])
                })
                
                self.test_count += 1
                
            except Exception as e:
                print(f"  ❌ Stability test turn {turn} failed: {e}")
                self.error_count += 1
        
        # Analyze stability
        avg_time = sum(m["processing_time"] for m in stability_metrics) / len(stability_metrics)
        self.data["system_stability"] = {
            "average_turn_time": avg_time,
            "stability_score": 1.0 - (self.error_count / max(self.test_count, 1)),
            "metrics": stability_metrics
        }
        
        print(f"  ⏰ Stability: {avg_time:.3f}s avg turn time, "
              f"{self.data['system_stability']['stability_score']:.3f} stability score")
        
    def execute_real_mission(self, mission_type, scenario):
        """Execute a real mission with failure scenario"""
        if not self.game_state or len(self.game_state.agents) < 2:
            return {"outcome": "INSUFFICIENT_AGENTS", "error": True}
        
        # Select agents
        agents_list = list(self.game_state.agents.values())
        test_agents = agents_list[:2]
        location = list(self.game_state.locations.values())[0]
        
        # Create mission data
        mission_data = {
            "type": mission_type,
            "target_location": location.id,
            "priority": "high",
            "participants": [{"agent_id": a.id} for a in test_agents],
            "scenario": scenario
        }
        
        # Prepare agent data
        agent_data = []
        for agent in test_agents:
            agent_data.append({
                "id": agent.id,
                "name": agent.name,
                "skills": getattr(agent, "skills", {}),
                "emotional_state": {}
            })
        
        # Prepare location data with scenario modifications
        location_data = {
            "name": location.name,
            "security_level": scenario.get("security_level", 5)
        }
        
        try:
            # Execute mission through mission engine
            mission_result = self.mission_engine.execute_mission(
                mission_data, agent_data, location_data, {}
            )
            
            return {
                "mission_type": mission_type,
                "scenario": scenario["name"],
                "outcome": str(mission_result.get("outcome", "UNKNOWN")),
                "success_probability": mission_result.get("success_probability", 0.0),
                "participants": [a.name for a in test_agents],
                "resource_costs": mission_result.get("resource_costs", {}),
                "narrative": mission_result.get("narrative", ""),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "mission_type": mission_type,
                "scenario": scenario["name"],
                "outcome": "EXECUTION_ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_agent_emotions(self, agent):
        """Analyze an agent's emotional state"""
        if not hasattr(agent, 'emotional_state') or not agent.emotional_state:
            return {"agent_name": agent.name, "error": "No emotional state"}
        
        emotional_state = agent.emotional_state
        
        try:
            # Get dominant emotion
            if hasattr(emotional_state, 'get_dominant_emotion'):
                dominant, intensity = emotional_state.get_dominant_emotion()
            else:
                dominant, intensity = "unknown", 0.5
            
            # Get stability
            stability = emotional_state.get_emotional_stability() if hasattr(emotional_state, 'get_emotional_stability') else 0.5
            
            # Get trauma level
            trauma_level = getattr(emotional_state, 'trauma_level', 0.0)
            
            return {
                "agent_name": agent.name,
                "dominant_emotion": dominant,
                "intensity": intensity,
                "stability": stability,
                "trauma_level": trauma_level,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"agent_name": agent.name, "error": str(e)}
    
    def capture_network_state(self):
        """Capture current network state"""
        return {
            "active_agents": len([a for a in self.game_state.agents.values() if a.status == "active"]),
            "total_agents": len(self.game_state.agents),
            "faction_count": len(self.game_state.factions),
            "location_count": len(self.game_state.locations),
            "timestamp": datetime.now().isoformat()
        }
    
    def trigger_cascade_failure(self, cascade_id):
        """Trigger a cascading failure scenario"""
        try:
            # Simulate different types of cascading failures
            cascade_types = ["agent_loss", "resource_depletion", "security_breach", "morale_collapse"]
            cascade_type = cascade_types[cascade_id % len(cascade_types)]
            
            if cascade_type == "agent_loss":
                # Mark an agent as compromised
                agents_list = list(self.game_state.agents.values())
                if agents_list:
                    agent = agents_list[cascade_id % len(agents_list)]
                    if hasattr(agent, 'emotional_state') and agent.emotional_state:
                        if hasattr(agent.emotional_state, 'apply_trauma'):
                            agent.emotional_state.apply_trauma(0.5, "cascade_failure")
                
                return {
                    "type": cascade_type,
                    "impact": "agent_compromised",
                    "affected_agent": agent.name if agents_list else "none"
                }
            
            elif cascade_type == "resource_depletion":
                return {
                    "type": cascade_type,
                    "impact": "resource_shortage",
                    "severity": "moderate"
                }
            
            elif cascade_type == "security_breach":
                return {
                    "type": cascade_type,
                    "impact": "exposure_risk",
                    "threat_level": "elevated"
                }
            
            else:  # morale_collapse
                return {
                    "type": cascade_type,
                    "impact": "network_instability",
                    "morale_effect": "negative"
                }
                
        except Exception as e:
            return {"type": "cascade_error", "impact": str(e)}
    
    def analyze_cascade_impact(self, initial_state, final_state):
        """Analyze the impact of cascading effects"""
        return {
            "initial_active_agents": initial_state["active_agents"],
            "final_active_agents": final_state["active_agents"],
            "agent_loss": initial_state["active_agents"] - final_state["active_agents"],
            "impact_severity": "high" if (initial_state["active_agents"] - final_state["active_agents"]) > 1 else "low",
            "network_stability": "unstable" if (initial_state["active_agents"] - final_state["active_agents"]) > 0 else "stable"
        }
    
    def test_team_mission(self, team_agents, team_name):
        """Test a team mission scenario"""
        if not team_agents or not self.game_state:
            return {"outcome": "NO_AGENTS", "error": True}
        
        location = list(self.game_state.locations.values())[0]
        
        mission_data = {
            "type": "intelligence",
            "target_location": location.id,
            "priority": "medium",
            "participants": [{"agent_id": a.id} for a in team_agents]
        }
        
        agent_data = [{"id": a.id, "name": a.name, "skills": getattr(a, "skills", {})} for a in team_agents]
        location_data = {"name": location.name, "security_level": 6}
        
        try:
            mission_result = self.mission_engine.execute_mission(mission_data, agent_data, location_data, {})
            
            return {
                "team_name": team_name,
                "team_size": len(team_agents),
                "participants": [a.name for a in team_agents],
                "outcome": str(mission_result.get("outcome", "UNKNOWN")),
                "success_probability": mission_result.get("success_probability", 0.0),
                "team_effectiveness": "high" if mission_result.get("success_probability", 0.5) > 0.6 else "normal"
            }
        except Exception as e:
            return {"team_name": team_name, "outcome": "ERROR", "error": str(e)}
    
    def simulate_mission_failure(self, mission_num):
        """Legacy method - kept for compatibility"""
        # Simple simulation as fallback
        base_failure_chance = 0.3 + (mission_num * 0.15)
        outcome = "FAILURE" if random.random() < base_failure_chance else "SUCCESS"
        
        return {
            "mission_id": mission_num,
            "outcome": outcome,
            "stress_impact": random.randint(10, 30) if outcome == "FAILURE" else random.randint(-5, 5),
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_patterns(self):
        """Analyze comprehensive failure patterns and system performance"""
        
        # Analyze mission patterns
        failures = [m for m in self.data["missions"] if "FAILURE" in str(m.get("outcome", "")).upper()]
        total_missions = len(self.data["missions"])
        
        # Mission analysis
        mission_analysis = {
            "total_missions": total_missions,
            "failure_rate": len(failures) / total_missions if total_missions > 0 else 0,
            "mission_types": {},
            "scenario_performance": {}
        }
        
        # Analyze by mission type and scenario
        for mission in self.data["missions"]:
            mission_type = mission.get("mission_type", "unknown")
            scenario = mission.get("scenario", "unknown")
            outcome = mission.get("outcome", "unknown")
            
            # Track mission type performance
            if mission_type not in mission_analysis["mission_types"]:
                mission_analysis["mission_types"][mission_type] = {"total": 0, "failures": 0}
            mission_analysis["mission_types"][mission_type]["total"] += 1
            if "FAILURE" in str(outcome).upper():
                mission_analysis["mission_types"][mission_type]["failures"] += 1
            
            # Track scenario performance
            if scenario not in mission_analysis["scenario_performance"]:
                mission_analysis["scenario_performance"][scenario] = {"total": 0, "failures": 0}
            mission_analysis["scenario_performance"][scenario]["total"] += 1
            if "FAILURE" in str(outcome).upper():
                mission_analysis["scenario_performance"][scenario]["failures"] += 1
        
        # Emotional impact analysis
        emotional_analysis = {
            "agents_analyzed": len(self.data["emotional_impact"]),
            "high_trauma_agents": len([e for e in self.data["emotional_impact"] if e.get("trauma_level", 0) > 0.5]),
            "unstable_agents": len([e for e in self.data["emotional_impact"] if e.get("stability", 1.0) < 0.5]),
            "dominant_emotions": {}
        }
        
        # Analyze dominant emotions
        for emotional_data in self.data["emotional_impact"]:
            emotion = emotional_data.get("dominant_emotion", "unknown")
            emotional_analysis["dominant_emotions"][emotion] = emotional_analysis["dominant_emotions"].get(emotion, 0) + 1
        
        # System performance analysis
        system_analysis = {
            "total_tests": self.test_count,
            "total_errors": self.error_count,
            "error_rate": self.error_count / max(self.test_count, 1),
            "stability_score": self.data.get("system_stability", {}).get("stability_score", 0.0),
            "average_turn_time": self.data.get("system_stability", {}).get("average_turn_time", 0.0)
        }
        
        # Cascading effects analysis
        cascading_analysis = self.data.get("cascading_effects", {})
        
        # Generate recommendations
        recommendations = self.generate_recommendations(mission_analysis, emotional_analysis, system_analysis)
        
        # Compile comprehensive analysis
        self.data["analysis"] = {
            "mission_analysis": mission_analysis,
            "emotional_analysis": emotional_analysis,
            "system_analysis": system_analysis,
            "cascading_analysis": cascading_analysis,
            "recommendations": recommendations,
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests_run": self.test_count,
                "total_errors": self.error_count,
                "overall_success_rate": 1.0 - (self.error_count / max(self.test_count, 1))
            }
        }
        
        # Display comprehensive results
        print(f"\n📊 COMPREHENSIVE ANALYSIS RESULTS")
        print("=" * 60)
        print(f"🎯 Mission Analysis:")
        print(f"   Total Missions: {mission_analysis['total_missions']}")
        print(f"   Failure Rate: {mission_analysis['failure_rate']:.1%}")
        
        print(f"\n💔 Emotional Impact:")
        print(f"   Agents Analyzed: {emotional_analysis['agents_analyzed']}")
        print(f"   High Trauma: {emotional_analysis['high_trauma_agents']}")
        print(f"   Unstable: {emotional_analysis['unstable_agents']}")
        
        print(f"\n⚡ System Performance:")
        print(f"   Total Tests: {system_analysis['total_tests']}")
        print(f"   Error Rate: {system_analysis['error_rate']:.1%}")
        print(f"   Stability Score: {system_analysis['stability_score']:.3f}")
        
        if recommendations:
            print(f"\n💡 Key Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"   {i}. {rec}")
    
    def generate_recommendations(self, mission_analysis, emotional_analysis, system_analysis):
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Mission balance recommendations
        if mission_analysis["failure_rate"] < 0.2:
            recommendations.append("Mission failure rate is low - consider increasing difficulty or risk factors")
        elif mission_analysis["failure_rate"] > 0.7:
            recommendations.append("Mission failure rate is very high - consider balancing difficulty")
        
        # Emotional health recommendations
        if emotional_analysis["high_trauma_agents"] > emotional_analysis["agents_analyzed"] * 0.5:
            recommendations.append("High trauma levels detected - implement trauma recovery mechanisms")
        
        if emotional_analysis["unstable_agents"] > emotional_analysis["agents_analyzed"] * 0.3:
            recommendations.append("Many unstable agents - review emotional state management")
        
        # System performance recommendations
        if system_analysis["error_rate"] > 0.1:
            recommendations.append("High error rate detected - review error handling and input validation")
        
        if system_analysis["stability_score"] < 0.8:
            recommendations.append("System stability is concerning - investigate performance bottlenecks")
        
        if system_analysis["average_turn_time"] > 0.5:
            recommendations.append("Turn processing is slow - optimize game loop performance")
        
        # Mission type specific recommendations
        for mission_type, stats in mission_analysis["mission_types"].items():
            if stats["total"] > 0:
                failure_rate = stats["failures"] / stats["total"]
                if failure_rate > 0.8:
                    recommendations.append(f"{mission_type} missions have very high failure rate - review balance")
        
        return recommendations
    
    def save_results(self):
        """Save comprehensive analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_failure_analysis_{timestamp}.json"
        
        # Add metadata
        self.data["metadata"] = {
            "test_version": "enhanced_v1.0",
            "timestamp": timestamp,
            "test_duration": (datetime.now() - datetime.fromisoformat(self.data.get("test_start", datetime.now().isoformat()))).total_seconds() if "test_start" in self.data else 0,
            "game_systems_tested": ["missions", "emotions", "cascading_effects", "multi_agent", "stability"]
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            
            print(f"\n💾 Enhanced analysis saved to: {filename}")
            
            # Also save a summary report
            summary_filename = f"test_summary_{timestamp}.txt"
            with open(summary_filename, 'w') as f:
                f.write("YEARS OF LEAD - ENHANCED AUTOMATED TESTING SUMMARY\n")
                f.write("=" * 60 + "\n\n")
                
                analysis = self.data.get("analysis", {})
                
                f.write("MISSION ANALYSIS:\n")
                mission_analysis = analysis.get("mission_analysis", {})
                f.write(f"  Total Missions: {mission_analysis.get('total_missions', 0)}\n")
                f.write(f"  Failure Rate: {mission_analysis.get('failure_rate', 0):.1%}\n\n")
                
                f.write("EMOTIONAL IMPACT:\n")
                emotional_analysis = analysis.get("emotional_analysis", {})
                f.write(f"  Agents Analyzed: {emotional_analysis.get('agents_analyzed', 0)}\n")
                f.write(f"  High Trauma: {emotional_analysis.get('high_trauma_agents', 0)}\n")
                f.write(f"  Unstable: {emotional_analysis.get('unstable_agents', 0)}\n\n")
                
                f.write("SYSTEM PERFORMANCE:\n")
                system_analysis = analysis.get("system_analysis", {})
                f.write(f"  Total Tests: {system_analysis.get('total_tests', 0)}\n")
                f.write(f"  Error Rate: {system_analysis.get('error_rate', 0):.1%}\n")
                f.write(f"  Stability Score: {system_analysis.get('stability_score', 0):.3f}\n\n")
                
                recommendations = analysis.get("recommendations", [])
                if recommendations:
                    f.write("RECOMMENDATIONS:\n")
                    for i, rec in enumerate(recommendations, 1):
                        f.write(f"  {i}. {rec}\n")
            
            print(f"📋 Summary report saved to: {summary_filename}")
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

if __name__ == "__main__":
    print("🎮 YEARS OF LEAD - ENHANCED AUTOMATED TESTING")
    print("=" * 60)
    print("Comprehensive testing of mission failures, emotional impact, and cascading effects")
    print("=" * 60)
    
    analyzer = FailureAnalyzer()
    analyzer.data["test_start"] = datetime.now().isoformat()
    analyzer.run_analysis()
    
    print("\n🎊 ENHANCED AUTOMATED TESTING COMPLETE!")
    print("=" * 60) 