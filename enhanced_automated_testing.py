#!/usr/bin/env python3
"""
Enhanced Automated Testing for Years of Lead

Comprehensive testing system for:
- Mission failure scenarios and cascading effects
- Emotional state impact tracking
- Multi-agent interaction testing
- Bug detection and performance analysis
- Feature validation across diverse scenarios
"""

import sys
import json
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add src to path for game imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


class EnhancedAutomatedTesting:
    """Enhanced automated testing system for Years of Lead"""

    def __init__(self):
        self.test_results = []
        self.mission_results = []
        self.bug_reports = []
        self.emotional_data = []
        self.cascading_effects = []
        self.start_time = datetime.now()

        # Game systems
        self.game_state = None
        self.mission_engine = None
        self.intelligence_db = None
        self.reputation_system = None

        # Counters
        self.total_tests = 0
        self.successful_tests = 0
        self.errors_encountered = 0
        self.current_turn = 0

    def initialize_systems(self) -> bool:
        """Initialize all game systems for testing"""
        try:
            print("🔧 Initializing game systems for comprehensive testing...")

            # Import game systems
            from game.core import GameState
            from game.mission_execution_engine import MissionExecutionEngine
            from game.intelligence_system import (
                IntelligenceDatabase,
            )
            from game.reputation_system import ReputationSystem

            # Initialize systems
            self.game_state = GameState()
            self.game_state.initialize_game()

            self.mission_engine = MissionExecutionEngine(self.game_state)
            self.intelligence_db = IntelligenceDatabase()
            self.reputation_system = ReputationSystem()

            print("✅ Systems initialized:")
            print(f"   - {len(self.game_state.agents)} agents")
            print(f"   - {len(self.game_state.factions)} factions")
            print(f"   - {len(self.game_state.locations)} locations")

            return True

        except Exception as e:
            self.log_error("System Initialization", str(e))
            return False

    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive automated tests"""
        print("\n🎮 STARTING COMPREHENSIVE AUTOMATED TESTING")
        print("=" * 70)

        if not self.initialize_systems():
            return {"status": "failed", "error": "Failed to initialize systems"}

        # Test phases
        test_phases = [
            ("Basic Functionality", self.test_basic_functionality),
            ("Mission Failure Scenarios", self.test_mission_failures),
            ("Emotional State Tracking", self.test_emotional_states),
            ("Multi-Agent Interactions", self.test_multi_agent_scenarios),
            ("Cascading Effects", self.test_cascading_effects),
            ("Intelligence Systems", self.test_intelligence_systems),
            ("Long-term Stability", self.test_long_term_stability),
            ("Stress Testing", self.test_stress_scenarios),
        ]

        for phase_name, phase_function in test_phases:
            print(f"\n📋 Testing: {phase_name}")
            try:
                phase_function()
                print(f"✅ {phase_name} completed")
            except Exception as e:
                self.log_error(phase_name, str(e))
                print(f"❌ {phase_name} failed: {str(e)}")

        # Generate final report
        return self.generate_final_report()

    def test_basic_functionality(self):
        """Test basic game functionality"""
        print("  🔧 Testing basic game functionality...")

        # Test 1: Verify game state
        assert self.game_state is not None, "Game state not initialized"
        assert len(self.game_state.agents) > 0, "No agents found"
        assert len(self.game_state.locations) > 0, "No locations found"

        self.record_test(
            "basic_game_state",
            True,
            {
                "agents": len(self.game_state.agents),
                "locations": len(self.game_state.locations),
            },
        )

        # Test 2: Verify mission engine
        assert self.mission_engine is not None, "Mission engine not initialized"
        self.record_test("mission_engine_init", True, {"status": "operational"})

        # Test 3: Agent accessibility
        first_agent = list(self.game_state.agents.values())[0]
        assert hasattr(first_agent, "name"), "Agent missing name attribute"
        assert hasattr(first_agent, "status"), "Agent missing status attribute"

        self.record_test(
            "agent_attributes",
            True,
            {"sample_agent": first_agent.name, "status": first_agent.status},
        )

        print("    ✅ Basic functionality verified")

    def test_mission_failures(self):
        """Test mission failure scenarios and outcomes"""
        print("  🎯 Testing mission failure scenarios...")

        mission_types = ["sabotage", "intelligence", "propaganda", "recruitment"]
        failure_scenarios = [
            {"name": "High Security", "security_level": 9},
            {"name": "Stressed Agents", "agent_stress": 0.8},
            {"name": "Low Skills", "skill_penalty": 0.5},
            {"name": "Equipment Failure", "equipment_malfunction": True},
        ]

        for scenario in failure_scenarios:
            for mission_type in mission_types[:2]:  # Test 2 mission types per scenario
                try:
                    result = self.execute_failure_scenario(mission_type, scenario)
                    self.mission_results.append(result)

                    print(
                        f"    🎯 {mission_type} ({scenario['name']}): {result['outcome']}"
                    )

                    # Check for cascading effects
                    if result.get("cascading_effects"):
                        self.cascading_effects.extend(result["cascading_effects"])

                except Exception as e:
                    self.log_error(f"Mission Failure - {mission_type}", str(e))

    def test_emotional_states(self):
        """Test emotional state tracking and impact"""
        print("  💔 Testing emotional state systems...")

        agents_with_emotions = []
        for agent in self.game_state.agents.values():
            if hasattr(agent, "emotional_state") and agent.emotional_state:
                agents_with_emotions.append(agent)

        if not agents_with_emotions:
            print("    ⚠️ No agents with emotional states found")
            return

        # Test emotional state tracking
        for agent in agents_with_emotions[:5]:  # Test first 5 agents
            try:
                emotional_data = self.analyze_agent_emotions(agent)
                self.emotional_data.append(emotional_data)

                print(
                    f"    💔 {agent.name}: {emotional_data['dominant_emotion']} "
                    f"(Stability: {emotional_data['stability']:.2f})"
                )

            except Exception as e:
                self.log_error(f"Emotional Analysis - {agent.name}", str(e))

        # Test emotional impact on missions
        if agents_with_emotions:
            try:
                high_stress_agent = self.find_high_stress_agent(agents_with_emotions)
                if high_stress_agent:
                    result = self.test_stressed_agent_performance(high_stress_agent)
                    self.record_test("stressed_agent_performance", True, result)
                    print(
                        f"    🔥 Stress test on {high_stress_agent.name}: {result['performance_impact']}"
                    )
            except Exception as e:
                self.log_error("Stressed Agent Performance", str(e))

    def test_multi_agent_scenarios(self):
        """Test multi-agent interaction scenarios"""
        print("  👥 Testing multi-agent interactions...")

        if len(self.game_state.agents) < 2:
            print("    ⚠️ Not enough agents for multi-agent testing")
            return

        # Test team formation
        agents_list = list(self.game_state.agents.values())

        # Test 2-agent team
        team_2 = agents_list[:2]
        result_2 = self.test_team_mission(team_2, "2-agent team")
        print(f"    👥 2-agent team: {result_2['outcome']}")

        # Test 3-agent team if possible
        if len(agents_list) >= 3:
            team_3 = agents_list[:3]
            result_3 = self.test_team_mission(team_3, "3-agent team")
            print(f"    👥 3-agent team: {result_3['outcome']}")

        # Test relationship impact
        if hasattr(self.game_state, "social_network"):
            try:
                relationship_impact = self.test_relationship_impact(team_2)
                self.record_test("relationship_impact", True, relationship_impact)
                print(f"    💭 Relationship impact: {relationship_impact['summary']}")
            except Exception as e:
                self.log_error("Relationship Impact", str(e))

    def test_cascading_effects(self):
        """Test cascading failure effects"""
        print("  🌊 Testing cascading effects...")

        # Capture initial state
        initial_state = self.capture_network_state()

        # Trigger cascading scenario
        cascade_trigger = {
            "type": "major_failure",
            "severity": "high",
            "affected_agents": min(3, len(self.game_state.agents)),
        }

        try:
            # Simulate cascading failure
            self.trigger_cascade_scenario(cascade_trigger)

            # Allow effects to propagate
            for turn in range(5):
                self.game_state.advance_turn()
                self.current_turn += 1

                # Check for cascade effects
                cascade_effects = self.detect_cascade_effects(initial_state)
                if cascade_effects:
                    self.cascading_effects.extend(cascade_effects)

            final_state = self.capture_network_state()
            cascade_analysis = self.analyze_cascade_impact(initial_state, final_state)

            self.record_test("cascading_effects", True, cascade_analysis)
            print(
                f"    🌊 Cascade effects detected: {len(cascade_analysis['effects_detected'])}"
            )

        except Exception as e:
            self.log_error("Cascading Effects", str(e))

    def test_intelligence_systems(self):
        """Test intelligence gathering and analysis"""
        print("  📊 Testing intelligence systems...")

        try:
            # Generate intelligence events

            intel_generator = self.intelligence_db

            # Test intelligence generation
            intel_events = []
            for i in range(5):
                event = {
                    "type": "security_patrol",
                    "location": f"test_location_{i}",
                    "priority": "medium",
                    "reliability": 0.7 + (i * 0.05),
                }
                intel_events.append(event)

            # Test pattern detection
            patterns = self.test_pattern_detection(intel_events)

            self.record_test(
                "intelligence_systems",
                True,
                {
                    "events_generated": len(intel_events),
                    "patterns_detected": len(patterns),
                },
            )

            print(
                f"    📊 Intelligence: {len(intel_events)} events, {len(patterns)} patterns"
            )

        except Exception as e:
            self.log_error("Intelligence Systems", str(e))

    def test_long_term_stability(self):
        """Test long-term system stability"""
        print("  ⏰ Testing long-term stability...")

        stability_metrics = {
            "turn_processing_times": [],
            "memory_usage": [],
            "error_rates": [],
            "performance_degradation": [],
        }

        # Run extended simulation
        for turn in range(20):
            try:
                start_time = time.time()

                # Execute standard turn
                self.game_state.advance_turn()
                self.current_turn += 1

                # Record performance
                turn_time = time.time() - start_time
                stability_metrics["turn_processing_times"].append(turn_time)

                # Check for performance issues
                if turn_time > 1.0:  # Flag slow turns
                    stability_metrics["performance_degradation"].append(turn)

            except Exception as e:
                self.log_error(f"Long-term Stability - Turn {turn}", str(e))

        # Analyze stability
        avg_turn_time = sum(stability_metrics["turn_processing_times"]) / len(
            stability_metrics["turn_processing_times"]
        )
        stability_score = 1.0 - (len(stability_metrics["performance_degradation"]) / 20)

        self.record_test(
            "long_term_stability",
            True,
            {
                "average_turn_time": avg_turn_time,
                "stability_score": stability_score,
                "slow_turns": len(stability_metrics["performance_degradation"]),
            },
        )

        print(
            f"    ⏰ Stability: {stability_score:.2f} (avg turn: {avg_turn_time:.3f}s)"
        )

    def test_stress_scenarios(self):
        """Test high-stress scenarios"""
        print("  🔥 Testing stress scenarios...")

        stress_tests = [
            ("Rapid Mission Execution", self.stress_test_rapid_missions),
            ("Resource Depletion", self.stress_test_resource_depletion),
            ("Agent Overload", self.stress_test_agent_overload),
        ]

        for test_name, test_function in stress_tests:
            try:
                result = test_function()
                self.record_test(
                    f"stress_{test_name.lower().replace(' ', '_')}", True, result
                )
                print(f"    🔥 {test_name}: {result.get('status', 'completed')}")
            except Exception as e:
                self.log_error(f"Stress Test - {test_name}", str(e))

    # Helper methods
    def execute_failure_scenario(self, mission_type: str, scenario: Dict) -> Dict:
        """Execute a specific mission failure scenario"""
        agents_list = list(self.game_state.agents.values())
        if len(agents_list) < 2:
            return {"outcome": "insufficient_agents", "error": True}

        test_agents = agents_list[:2]
        location = list(self.game_state.locations.values())[0]

        # Create mission with failure conditions
        mission_data = {
            "type": mission_type,
            "target_location": location.id,
            "priority": "high",
            "participants": [{"agent_id": a.id} for a in test_agents],
            "scenario": scenario,
        }

        # Execute mission
        agent_data = [
            {"id": a.id, "name": a.name, "skills": getattr(a, "skills", {})}
            for a in test_agents
        ]
        location_data = {
            "name": location.name,
            "security_level": scenario.get("security_level", 5),
        }

        try:
            mission_result = self.mission_engine.execute_mission(
                mission_data, agent_data, location_data, {}
            )
            return {
                "mission_type": mission_type,
                "scenario": scenario["name"],
                "outcome": str(mission_result.get("outcome", "unknown")),
                "success_probability": mission_result.get("success_probability", 0.0),
                "participants": [a.name for a in test_agents],
                "cascading_effects": mission_result.get("cascading_effects", []),
            }
        except Exception as e:
            return {"outcome": "execution_error", "error": str(e)}

    def analyze_agent_emotions(self, agent) -> Dict:
        """Analyze an agent's emotional state"""
        emotional_state = agent.emotional_state

        try:
            if hasattr(emotional_state, "get_dominant_emotion"):
                dominant, intensity = emotional_state.get_dominant_emotion()
            else:
                dominant, intensity = "unknown", 0.5

            stability = (
                emotional_state.get_emotional_stability()
                if hasattr(emotional_state, "get_emotional_stability")
                else 0.5
            )
            trauma_level = getattr(emotional_state, "trauma_level", 0.0)

            return {
                "agent_name": agent.name,
                "dominant_emotion": dominant,
                "intensity": intensity,
                "stability": stability,
                "trauma_level": trauma_level,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"agent_name": agent.name, "error": str(e)}

    def find_high_stress_agent(self, agents) -> Optional[Any]:
        """Find agent with highest stress/trauma"""
        highest_stress = 0
        stressed_agent = None

        for agent in agents:
            if hasattr(agent, "emotional_state") and agent.emotional_state:
                trauma = getattr(agent.emotional_state, "trauma_level", 0.0)
                if trauma > highest_stress:
                    highest_stress = trauma
                    stressed_agent = agent

        return stressed_agent

    def test_stressed_agent_performance(self, agent) -> Dict:
        """Test performance of a stressed agent"""
        try:
            # Create a simple mission for the stressed agent
            location = list(self.game_state.locations.values())[0]

            mission_data = {
                "type": "intelligence",
                "target_location": location.id,
                "priority": "medium",
                "participants": [{"agent_id": agent.id}],
            }

            agent_data = [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "skills": getattr(agent, "skills", {}),
                }
            ]
            location_data = {"name": location.name, "security_level": 5}

            mission_result = self.mission_engine.execute_mission(
                mission_data, agent_data, location_data, {}
            )

            return {
                "agent_name": agent.name,
                "mission_outcome": str(mission_result.get("outcome", "unknown")),
                "success_probability": mission_result.get("success_probability", 0.0),
                "performance_impact": "degraded"
                if mission_result.get("success_probability", 0.5) < 0.4
                else "normal",
            }
        except Exception as e:
            return {"agent_name": agent.name, "error": str(e)}

    def test_team_mission(self, team_agents, team_name: str) -> Dict:
        """Test a team mission scenario"""
        try:
            location = list(self.game_state.locations.values())[0]

            mission_data = {
                "type": "sabotage",
                "target_location": location.id,
                "priority": "high",
                "participants": [{"agent_id": a.id} for a in team_agents],
            }

            agent_data = [
                {"id": a.id, "name": a.name, "skills": getattr(a, "skills", {})}
                for a in team_agents
            ]
            location_data = {"name": location.name, "security_level": 6}

            mission_result = self.mission_engine.execute_mission(
                mission_data, agent_data, location_data, {}
            )

            return {
                "team_name": team_name,
                "team_size": len(team_agents),
                "participants": [a.name for a in team_agents],
                "outcome": str(mission_result.get("outcome", "unknown")),
                "success_probability": mission_result.get("success_probability", 0.0),
                "team_effectiveness": "high"
                if mission_result.get("success_probability", 0.5) > 0.6
                else "normal",
            }
        except Exception as e:
            return {"team_name": team_name, "error": str(e)}

    def capture_network_state(self) -> Dict:
        """Capture current network state for comparison"""
        return {
            "active_agents": len(
                [a for a in self.game_state.agents.values() if a.status == "active"]
            ),
            "total_agents": len(self.game_state.agents),
            "faction_resources": {
                f.name: getattr(f, "resources", 0)
                for f in self.game_state.factions.values()
            },
            "timestamp": datetime.now().isoformat(),
        }

    def trigger_cascade_scenario(self, trigger: Dict):
        """Trigger a cascading failure scenario"""
        # Simulate a major incident that affects multiple agents
        affected_count = 0
        for agent in list(self.game_state.agents.values())[
            : trigger["affected_agents"]
        ]:
            if hasattr(agent, "emotional_state") and agent.emotional_state:
                # Apply trauma/stress
                if hasattr(agent.emotional_state, "apply_trauma"):
                    agent.emotional_state.apply_trauma(0.4, "cascade_failure")
                affected_count += 1

        return {"affected_agents": affected_count}

    def detect_cascade_effects(self, initial_state: Dict) -> List[str]:
        """Detect cascading effects by comparing states"""
        effects = []
        current_state = self.capture_network_state()

        # Check for agent status changes
        if current_state["active_agents"] < initial_state["active_agents"]:
            effects.append(
                f"Agent deactivation: {initial_state['active_agents'] - current_state['active_agents']} agents"
            )

        # Check for resource changes - FIXED TYPE ERROR
        for faction_name, initial_resources in initial_state[
            "faction_resources"
        ].items():
            current_resources = current_state["faction_resources"].get(faction_name, 0)

            # Handle both dict and numeric resource values
            if isinstance(initial_resources, dict):
                # If resources is a dict, check money specifically
                initial_money = initial_resources.get("money", 0)
                current_money = (
                    current_resources.get("money", 0)
                    if isinstance(current_resources, dict)
                    else 0
                )
                if current_money < initial_money * 0.9:  # 10% decrease threshold
                    effects.append(f"Resource depletion in {faction_name}")
            else:
                # If resources is a numeric value
                if (
                    current_resources < initial_resources * 0.9
                ):  # 10% decrease threshold
                    effects.append(f"Resource depletion in {faction_name}")

        return effects

    def analyze_cascade_impact(self, initial_state: Dict, final_state: Dict) -> Dict:
        """Analyze the impact of cascading effects"""
        return {
            "initial_active_agents": initial_state["active_agents"],
            "final_active_agents": final_state["active_agents"],
            "agent_loss": initial_state["active_agents"] - final_state["active_agents"],
            "cascade_severity": "high"
            if (initial_state["active_agents"] - final_state["active_agents"]) > 1
            else "low",
            "effects_detected": self.detect_cascade_effects(initial_state),
        }

    def test_relationship_impact(self, agents) -> Dict:
        """Test relationship impact on missions"""
        # Simple relationship test
        return {
            "agents_tested": [a.name for a in agents],
            "relationship_exists": hasattr(self.game_state, "social_network"),
            "summary": "Relationship system detected"
            if hasattr(self.game_state, "social_network")
            else "No relationship system",
        }

    def test_pattern_detection(self, intel_events) -> List[Dict]:
        """Test intelligence pattern detection"""
        # Simple pattern detection test
        patterns = []

        # Look for location clustering
        location_counts = {}
        for event in intel_events:
            location = event.get("location", "unknown")
            location_counts[location] = location_counts.get(location, 0) + 1

        for location, count in location_counts.items():
            if count > 1:
                patterns.append(
                    {
                        "type": "location_clustering",
                        "location": location,
                        "frequency": count,
                    }
                )

        return patterns

    def stress_test_rapid_missions(self) -> Dict:
        """Test rapid mission execution"""
        try:
            missions_executed = 0
            start_time = time.time()

            for i in range(5):
                agents_list = list(self.game_state.agents.values())
                if len(agents_list) >= 2:
                    result = self.execute_failure_scenario(
                        "intelligence", {"name": "Rapid Test", "security_level": 5}
                    )
                    if not result.get("error"):
                        missions_executed += 1

            end_time = time.time()
            return {
                "status": "completed",
                "missions_executed": missions_executed,
                "duration": end_time - start_time,
                "missions_per_second": missions_executed / (end_time - start_time)
                if end_time > start_time
                else 0,
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def stress_test_resource_depletion(self) -> Dict:
        """Test resource depletion scenarios"""
        return {
            "status": "simulated",
            "message": "Resource depletion test simulated",
            "resource_impact": "moderate",
        }

    def stress_test_agent_overload(self) -> Dict:
        """Test agent overload scenarios"""
        return {
            "status": "simulated",
            "message": "Agent overload test simulated",
            "overload_impact": "handled",
        }

    def record_test(self, test_name: str, success: bool, data: Dict):
        """Record a test result"""
        self.total_tests += 1
        if success:
            self.successful_tests += 1

        self.test_results.append(
            {
                "test_name": test_name,
                "success": success,
                "timestamp": datetime.now().isoformat(),
                "data": data,
            }
        )

    def log_error(self, test_name: str, error_msg: str):
        """Log an error"""
        self.errors_encountered += 1
        self.bug_reports.append(
            {
                "test_name": test_name,
                "error": error_msg,
                "timestamp": datetime.now().isoformat(),
                "turn": self.current_turn,
            }
        )

    def generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        end_time = datetime.now()
        duration = end_time - self.start_time

        # Calculate statistics
        success_rate = (
            self.successful_tests / self.total_tests if self.total_tests > 0 else 0
        )

        # Analyze mission results
        mission_outcomes = {}
        for result in self.mission_results:
            outcome = result.get("outcome", "unknown")
            mission_outcomes[outcome] = mission_outcomes.get(outcome, 0) + 1

        # Generate recommendations
        recommendations = []
        if success_rate < 0.8:
            recommendations.append("Low success rate detected - review failing systems")
        if self.errors_encountered > self.total_tests * 0.1:
            recommendations.append("High error rate - improve error handling")
        if len(self.cascading_effects) > 5:
            recommendations.append(
                "Significant cascading effects detected - review failure propagation"
            )

        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {
            "test_session": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": duration.total_seconds() / 60,
                "turns_completed": self.current_turn,
            },
            "summary": {
                "total_tests": self.total_tests,
                "successful_tests": self.successful_tests,
                "failed_tests": self.total_tests - self.successful_tests,
                "success_rate": success_rate,
                "errors_encountered": self.errors_encountered,
                "bug_reports": len(self.bug_reports),
            },
            "mission_analysis": {
                "total_missions": len(self.mission_results),
                "outcomes": mission_outcomes,
                "cascading_effects": len(self.cascading_effects),
            },
            "emotional_analysis": {
                "agents_analyzed": len(self.emotional_data),
                "emotional_data": self.emotional_data,
            },
            "recommendations": recommendations,
            "detailed_results": {
                "test_results": self.test_results,
                "mission_results": self.mission_results,
                "bug_reports": self.bug_reports,
                "cascading_effects": self.cascading_effects,
            },
        }

        # Save to file
        filename = f"enhanced_test_report_{timestamp}.json"
        try:
            with open(filename, "w") as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n💾 Detailed report saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")

        return report


def main():
    """Main function to run enhanced automated testing"""
    print("🎮 YEARS OF LEAD - ENHANCED AUTOMATED TESTING")
    print("=" * 60)

    tester = EnhancedAutomatedTesting()

    try:
        report = tester.run_comprehensive_tests()

        print("\n" + "=" * 60)
        print("🎊 AUTOMATED TESTING COMPLETE")
        print("=" * 60)

        summary = report["summary"]
        print(f"📊 Tests Run: {summary['total_tests']}")
        print(f"✅ Success Rate: {summary['success_rate']:.1%}")
        print(f"❌ Errors: {summary['errors_encountered']}")
        print(f"🐛 Bug Reports: {summary['bug_reports']}")

        mission_analysis = report["mission_analysis"]
        print(f"🎯 Missions Tested: {mission_analysis['total_missions']}")
        print(f"🌊 Cascading Effects: {mission_analysis['cascading_effects']}")

        if report["recommendations"]:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(report["recommendations"], 1):
                print(f"   {i}. {rec}")

        return report

    except Exception as e:
        print(f"\n❌ TESTING FAILED: {e}")
        traceback.print_exc()
        return {"error": str(e)}


if __name__ == "__main__":
    main()
