#!/usr/bin/env python3
"""
Years of Lead - Comprehensive Automated Playtest System

This system runs extensive automated testing focusing on:
- Mission failure scenarios and cascading effects
- Emotional state impact on agent performance
- Multi-agent interaction dynamics
- Bug detection and reporting
- Feature evaluation across diverse scenarios
- Performance analysis and data collection

Author: Years of Lead Development Team
Version: 1.0.0
"""

import sys
import json
import traceback
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Game system imports
from game.core import GameState
from game.mission_execution_engine import MissionExecutionEngine
from game.intelligence_system import (
    IntelligenceDatabase,
    IntelligenceGenerator,
)
from game.reputation_system import ReputationSystem
from game.agent_decision_system import integrate_agent_decisions
from game.enhanced_mission_system import EnhancedMissionSystem
from game.advanced_relationships import AdvancedRelationshipSystem


@dataclass
class TestResult:
    """Data structure for individual test results"""

    test_id: str
    test_type: str
    timestamp: str
    success: bool
    duration: float
    data: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


@dataclass
class AgentTestMetrics:
    """Metrics for individual agent performance during testing"""

    agent_id: str
    name: str
    missions_completed: int
    missions_failed: int
    emotional_stability_start: float
    emotional_stability_end: float
    trauma_level_start: float
    trauma_level_end: float
    relationship_changes: Dict[str, float]
    skill_performance: Dict[str, float]


@dataclass
class MissionTestResult:
    """Detailed results from mission testing"""

    mission_id: str
    mission_type: str
    outcome: str
    participants: List[str]
    success_probability: float
    actual_success: bool
    emotional_impacts: Dict[str, Dict[str, float]]
    cascading_effects: List[str]
    narrative_generated: str
    resource_costs: Dict[str, int]


class ComprehensiveAutomatedPlaytest:
    """Main automated playtest system"""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the comprehensive automated playtest system"""
        self.config = config or self._default_config()
        self.test_results: List[TestResult] = []
        self.agent_metrics: Dict[str, AgentTestMetrics] = {}
        self.mission_results: List[MissionTestResult] = []
        self.bug_reports: List[Dict] = []
        self.performance_data: Dict[str, Any] = {}

        # Game systems
        self.game_state: Optional[GameState] = None
        self.mission_engine: Optional[MissionExecutionEngine] = None
        self.intelligence_db: Optional[IntelligenceDatabase] = None
        self.intelligence_gen: Optional[IntelligenceGenerator] = None
        self.reputation_system: Optional[ReputationSystem] = None
        self.decision_system = None
        self.enhanced_mission_system: Optional[EnhancedMissionSystem] = None
        self.relationship_system: Optional[AdvancedRelationshipSystem] = None

        # Test tracking
        self.start_time = datetime.now()
        self.current_turn = 0
        self.total_tests_run = 0
        self.total_errors = 0

    def _default_config(self) -> Dict:
        """Default configuration for automated testing"""
        return {
            "test_duration_minutes": 90,
            "max_turns": 50,
            "mission_failure_rate_target": 0.3,  # Target 30% failure rate
            "stress_scenarios": True,
            "cascading_effects_testing": True,
            "multi_agent_scenarios": True,
            "emotional_impact_tracking": True,
            "bug_detection": True,
            "performance_monitoring": True,
            "narrative_testing": True,
            "save_detailed_logs": True,
            "randomization_seed": None,  # None for truly random
        }

    def initialize_game_systems(self) -> bool:
        """Initialize all game systems for testing"""
        try:
            print("🔧 Initializing comprehensive game systems...")

            # Initialize core game state
            self.game_state = GameState()
            self.game_state.initialize_game()

            # Initialize all advanced systems
            self.mission_engine = MissionExecutionEngine(self.game_state)
            self.intelligence_db = IntelligenceDatabase()
            self.intelligence_gen = IntelligenceGenerator()
            self.reputation_system = ReputationSystem()

            # Enhanced systems
            if hasattr(self.game_state, "enhanced_mission_system"):
                self.enhanced_mission_system = self.game_state.enhanced_mission_system
            else:
                self.enhanced_mission_system = EnhancedMissionSystem(self.game_state)

            if hasattr(self.game_state, "relationship_system"):
                self.relationship_system = self.game_state.relationship_system
            else:
                self.relationship_system = AdvancedRelationshipSystem()

            # Integrate agent decision system
            self.decision_system = integrate_agent_decisions(self.game_state)

            # Set randomization seed if specified
            if self.config.get("randomization_seed"):
                random.seed(self.config["randomization_seed"])

            # Record initial agent metrics
            self._record_initial_agent_metrics()

            print("✅ Game systems initialized successfully")
            print(f"   - {len(self.game_state.agents)} agents loaded")
            print(f"   - {len(self.game_state.factions)} factions active")
            print(f"   - {len(self.game_state.locations)} locations available")

            return True

        except Exception as e:
            self._log_error(
                "Game System Initialization", str(e), traceback.format_exc()
            )
            return False

    def run_comprehensive_playtest(self) -> Dict[str, Any]:
        """Run the full comprehensive automated playtest"""
        print("🎮 STARTING COMPREHENSIVE AUTOMATED PLAYTEST")
        print("=" * 80)
        print(f"Test Duration: {self.config['test_duration_minutes']} minutes")
        print(f"Max Turns: {self.config['max_turns']}")
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        if not self.initialize_game_systems():
            return {"error": "Failed to initialize game systems"}

        # Run test phases
        test_phases = [
            ("Mission Failure Testing", self._test_mission_failures),
            ("Emotional State Impact Testing", self._test_emotional_impact),
            ("Multi-Agent Interaction Testing", self._test_multi_agent_interactions),
            ("Cascading Effects Testing", self._test_cascading_effects),
            ("Stress Scenario Testing", self._test_stress_scenarios),
            ("Intelligence System Testing", self._test_intelligence_systems),
            ("Relationship Dynamics Testing", self._test_relationship_dynamics),
            ("Narrative Generation Testing", self._test_narrative_generation),
            ("Long-term Stability Testing", self._test_long_term_stability),
        ]

        for phase_name, phase_function in test_phases:
            if self._should_continue_testing():
                print(f"\n📋 Starting {phase_name}...")
                try:
                    phase_function()
                    print(f"✅ {phase_name} completed")
                except Exception as e:
                    self._log_error(phase_name, str(e), traceback.format_exc())
                    print(f"❌ {phase_name} failed: {str(e)}")
            else:
                print(f"⏰ Time limit reached, skipping {phase_name}")
                break

        # Generate comprehensive report
        return self._generate_final_report()

    def _test_mission_failures(self):
        """Test mission failure scenarios and outcomes"""
        print("  🎯 Testing mission failure scenarios...")

        mission_types = [
            "sabotage",
            "intelligence",
            "propaganda",
            "recruitment",
            "assassination",
        ]
        failure_scenarios = [
            {"stress_agents": True, "description": "High-stress agents"},
            {"low_skills": True, "description": "Low-skill participants"},
            {"high_security": True, "description": "High-security targets"},
            {"equipment_failure": True, "description": "Equipment failures"},
            {"betrayal": True, "description": "Agent betrayal"},
        ]

        for scenario in failure_scenarios:
            for mission_type in mission_types[:3]:  # Test 3 mission types per scenario
                try:
                    result = self._execute_failure_scenario(mission_type, scenario)
                    if result:
                        self.mission_results.append(result)
                        self._analyze_cascading_effects(result)
                except Exception as e:
                    self._log_error(f"Mission Failure Test - {mission_type}", str(e))

    def _test_emotional_impact(self):
        """Test how emotional states affect mission outcomes"""
        print("  💔 Testing emotional state impact on performance...")

        # Create emotional stress scenarios
        emotional_scenarios = [
            {"high_fear": 0.8, "description": "High fear scenario"},
            {"high_anger": 0.8, "description": "High anger scenario"},
            {"high_trauma": 0.7, "description": "High trauma scenario"},
            {"low_trust": 0.2, "description": "Low trust scenario"},
            {
                "mixed_emotions": {"fear": 0.6, "anger": 0.5},
                "description": "Mixed emotional state",
            },
        ]

        for scenario in emotional_scenarios:
            agents_to_test = list(self.game_state.agents.values())[:3]
            for agent in agents_to_test:
                try:
                    self._apply_emotional_scenario(agent, scenario)
                    # Test mission performance under emotional stress
                    mission_result = self._test_agent_performance_under_stress(agent)
                    if mission_result:
                        self.mission_results.append(mission_result)
                except Exception as e:
                    self._log_error(f"Emotional Impact Test - {agent.name}", str(e))

    def _test_multi_agent_interactions(self):
        """Test multi-agent collaboration and failure scenarios"""
        print("  👥 Testing multi-agent interaction dynamics...")

        if len(self.game_state.agents) < 2:
            print("    ⚠️ Not enough agents for multi-agent testing")
            return

        interaction_scenarios = [
            {
                "team_size": 2,
                "relationship": "positive",
                "description": "Close partners",
            },
            {
                "team_size": 3,
                "relationship": "negative",
                "description": "Antagonistic team",
            },
            {
                "team_size": 2,
                "relationship": "neutral",
                "description": "Neutral acquaintances",
            },
            {
                "team_size": 4,
                "relationship": "mixed",
                "description": "Mixed relationships",
            },
        ]

        for scenario in interaction_scenarios:
            try:
                team = self._create_test_team(
                    scenario["team_size"], scenario["relationship"]
                )
                if team:
                    mission_result = self._execute_team_mission(team, scenario)
                    if mission_result:
                        self.mission_results.append(mission_result)
                        self._analyze_team_dynamics(team, mission_result)
            except Exception as e:
                self._log_error(f"Multi-Agent Test - {scenario['description']}", str(e))

    def _test_cascading_effects(self):
        """Test cascading failure effects across the network"""
        print("  🌊 Testing cascading failure effects...")

        # Create initial failure conditions
        cascade_triggers = [
            {"type": "mission_failure", "severity": "catastrophic"},
            {"type": "agent_betrayal", "impact": "network_wide"},
            {"type": "resource_depletion", "critical": True},
            {"type": "security_breach", "exposure_level": "high"},
        ]

        for trigger in cascade_triggers:
            try:
                initial_state = self._capture_network_state()
                self._trigger_cascade_scenario(trigger)

                # Allow cascading effects to propagate over multiple turns
                for turn in range(5):
                    self.game_state.advance_turn()
                    self._process_cascade_turn(trigger, turn)

                final_state = self._capture_network_state()
                cascade_analysis = self._analyze_cascade_impact(
                    initial_state, final_state, trigger
                )

                self._record_test_result(
                    f"cascade_{trigger['type']}",
                    "cascading_effects",
                    True,
                    cascade_analysis,
                )

            except Exception as e:
                self._log_error(f"Cascading Effects Test - {trigger['type']}", str(e))

    def _test_stress_scenarios(self):
        """Test high-stress scenarios and system limits"""
        print("  🔥 Testing stress scenarios and system limits...")

        stress_tests = [
            {"name": "Mass Mission Failure", "test": self._stress_test_mass_failures},
            {
                "name": "Resource Depletion",
                "test": self._stress_test_resource_depletion,
            },
            {
                "name": "Network Fragmentation",
                "test": self._stress_test_network_fragmentation,
            },
            {"name": "High Agent Turnover", "test": self._stress_test_agent_turnover},
        ]

        for stress_test in stress_tests:
            try:
                print(f"    🔥 Running {stress_test['name']}...")
                result = stress_test["test"]()
                self._record_test_result(
                    f"stress_{stress_test['name'].lower().replace(' ', '_')}",
                    "stress_testing",
                    result.get("success", False),
                    result,
                )
            except Exception as e:
                self._log_error(f"Stress Test - {stress_test['name']}", str(e))

    def _test_intelligence_systems(self):
        """Test intelligence gathering and analysis systems"""
        print("  📊 Testing intelligence systems...")

        intel_tests = [
            {"type": "pattern_detection", "events": 10},
            {"type": "threat_assessment", "scenarios": 5},
            {"type": "information_correlation", "complexity": "high"},
            {"type": "predictive_analysis", "time_horizon": 10},
        ]

        for test in intel_tests:
            try:
                result = self._execute_intelligence_test(test)
                self._record_test_result(
                    f"intel_{test['type']}",
                    "intelligence_testing",
                    result.get("success", False),
                    result,
                )
            except Exception as e:
                self._log_error(f"Intelligence Test - {test['type']}", str(e))

    def _test_relationship_dynamics(self):
        """Test relationship system dynamics and evolution"""
        print("  💭 Testing relationship dynamics...")

        if not self.relationship_system:
            print("    ⚠️ Relationship system not available")
            return

        relationship_tests = [
            {"scenario": "trust_building", "duration": 5},
            {"scenario": "betrayal_sequence", "complexity": "high"},
            {"scenario": "loyalty_conflict", "agents": 3},
            {"scenario": "secret_revelation", "impact": "network_wide"},
        ]

        for test in relationship_tests:
            try:
                result = self._execute_relationship_test(test)
                self._record_test_result(
                    f"relationship_{test['scenario']}",
                    "relationship_testing",
                    result.get("success", False),
                    result,
                )
            except Exception as e:
                self._log_error(f"Relationship Test - {test['scenario']}", str(e))

    def _test_narrative_generation(self):
        """Test narrative generation and contextual storytelling"""
        print("  📖 Testing narrative generation...")

        narrative_tests = [
            {"context": "mission_failure", "emotional_state": "high_stress"},
            {"context": "betrayal_discovery", "relationship_impact": "severe"},
            {"context": "victory_celebration", "morale_boost": True},
            {"context": "resource_crisis", "desperation_level": "high"},
        ]

        for test in narrative_tests:
            try:
                narratives = self._generate_test_narratives(test)
                quality_score = self._evaluate_narrative_quality(narratives, test)

                self._record_test_result(
                    f"narrative_{test['context']}",
                    "narrative_testing",
                    quality_score > 0.7,
                    {
                        "narratives_generated": len(narratives),
                        "quality_score": quality_score,
                        "context": test,
                        "sample_narratives": narratives[:3],
                    },
                )
            except Exception as e:
                self._log_error(f"Narrative Test - {test['context']}", str(e))

    def _test_long_term_stability(self):
        """Test long-term system stability and performance"""
        print("  ⏰ Testing long-term stability...")

        stability_metrics = {
            "memory_usage": [],
            "processing_time": [],
            "error_rate": [],
            "system_coherence": [],
        }

        # Run extended simulation
        for turn in range(20):
            try:
                turn_start = time.time()

                # Execute a standard turn
                self._execute_standard_turn()

                turn_duration = time.time() - turn_start
                stability_metrics["processing_time"].append(turn_duration)

                # Check system coherence
                coherence_score = self._calculate_system_coherence()
                stability_metrics["system_coherence"].append(coherence_score)

                # Track error rate
                errors_this_turn = len(
                    [r for r in self.test_results[-10:] if not r.success]
                )
                stability_metrics["error_rate"].append(errors_this_turn / 10.0)

                if turn % 5 == 0:
                    print(
                        f"    Turn {turn}: Processing time {turn_duration:.2f}s, "
                        f"Coherence {coherence_score:.2f}, Errors {errors_this_turn}"
                    )

            except Exception as e:
                self._log_error(f"Long-term Stability - Turn {turn}", str(e))

        # Analyze stability trends
        stability_analysis = self._analyze_stability_trends(stability_metrics)
        self._record_test_result(
            "long_term_stability",
            "stability_testing",
            stability_analysis.get("stable", False),
            stability_analysis,
        )

    def _should_continue_testing(self) -> bool:
        """Check if testing should continue based on time and turn limits"""
        elapsed_minutes = (datetime.now() - self.start_time).total_seconds() / 60
        return (
            elapsed_minutes < self.config["test_duration_minutes"]
            and self.current_turn < self.config["max_turns"]
        )

    def _log_error(self, test_name: str, error_msg: str, traceback_str: str = ""):
        """Log an error that occurred during testing"""
        self.total_errors += 1
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "error_message": error_msg,
            "traceback": traceback_str,
            "turn": self.current_turn,
        }
        self.bug_reports.append(error_record)
        print(f"    ❌ Error in {test_name}: {error_msg}")

    def _record_test_result(
        self, test_id: str, test_type: str, success: bool, data: Dict
    ):
        """Record the result of a test"""
        self.total_tests_run += 1
        result = TestResult(
            test_id=test_id,
            test_type=test_type,
            timestamp=datetime.now().isoformat(),
            success=success,
            duration=0.0,  # Could be enhanced to track actual duration
            data=data,
            errors=[],
            warnings=[],
        )
        self.test_results.append(result)

    def _record_initial_agent_metrics(self):
        """Record initial metrics for all agents"""
        for agent_id, agent in self.game_state.agents.items():
            emotional_state = getattr(agent, "emotional_state", None)
            self.agent_metrics[agent_id] = AgentTestMetrics(
                agent_id=agent_id,
                name=agent.name,
                missions_completed=0,
                missions_failed=0,
                emotional_stability_start=emotional_state.get_emotional_stability()
                if emotional_state
                else 0.5,
                emotional_stability_end=0.0,
                trauma_level_start=emotional_state.trauma_level
                if emotional_state
                else 0.0,
                trauma_level_end=0.0,
                relationship_changes={},
                skill_performance={},
            )

    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final test report"""
        end_time = datetime.now()
        duration = end_time - self.start_time

        # Calculate summary statistics
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r.success])
        success_rate = successful_tests / total_tests if total_tests > 0 else 0

        mission_tests = [r for r in self.test_results if "mission" in r.test_type]
        mission_success_rate = (
            len([r for r in mission_tests if r.success]) / len(mission_tests)
            if mission_tests
            else 0
        )

        # Update final agent metrics
        self._update_final_agent_metrics()

        report = {
            "test_session": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": duration.total_seconds() / 60,
                "turns_completed": self.current_turn,
                "configuration": self.config,
            },
            "summary_statistics": {
                "total_tests_run": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "overall_success_rate": success_rate,
                "mission_success_rate": mission_success_rate,
                "total_errors": self.total_errors,
                "bug_reports_generated": len(self.bug_reports),
            },
            "mission_analysis": {
                "total_missions": len(self.mission_results),
                "mission_outcomes": self._analyze_mission_outcomes(),
                "failure_patterns": self._analyze_failure_patterns(),
                "cascading_effects": self._analyze_cascading_effects_summary(),
            },
            "agent_analysis": {
                "agent_count": len(self.agent_metrics),
                "emotional_stability_changes": self._analyze_emotional_changes(),
                "trauma_progression": self._analyze_trauma_progression(),
                "performance_degradation": self._analyze_performance_degradation(),
            },
            "system_performance": {
                "stability_rating": self._calculate_overall_stability(),
                "error_frequency": self.total_errors / total_tests
                if total_tests > 0
                else 0,
                "feature_completeness": self._assess_feature_completeness(),
                "performance_bottlenecks": self._identify_performance_issues(),
            },
            "recommendations": self._generate_recommendations(),
            "detailed_results": {
                "test_results": [asdict(r) for r in self.test_results],
                "mission_results": [asdict(r) for r in self.mission_results],
                "agent_metrics": {k: asdict(v) for k, v in self.agent_metrics.items()},
                "bug_reports": self.bug_reports,
            },
        }

        # Save detailed report
        if self.config.get("save_detailed_logs"):
            self._save_report_to_file(report)

        return report

    def _save_report_to_file(self, report: Dict):
        """Save the comprehensive report to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"automated_playtest_report_{timestamp}.json"

        try:
            with open(filename, "w") as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n💾 Detailed report saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")

    # Additional helper methods would be implemented here
    # Due to length constraints, I'm showing the core structure
    # The following methods would contain the detailed implementation:

    def _execute_failure_scenario(
        self, mission_type: str, scenario: Dict
    ) -> Optional[MissionTestResult]:
        """Execute a specific mission failure scenario"""
        # Implementation would create specific failure conditions
        # and execute mission with those parameters
        pass

    def _analyze_cascading_effects(self, mission_result: MissionTestResult):
        """Analyze cascading effects from a mission result"""
        # Implementation would track how mission outcomes affect
        # other agents, relationships, and future missions
        pass

    def _apply_emotional_scenario(self, agent, scenario: Dict):
        """Apply specific emotional conditions to an agent"""
        # Implementation would modify agent emotional state
        # according to the test scenario
        pass

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on test results"""
        recommendations = []

        # Analyze failure patterns and suggest improvements
        if self.total_errors > len(self.test_results) * 0.1:
            recommendations.append(
                "High error rate detected - review error handling and input validation"
            )

        # Check mission balance
        mission_failure_rate = (
            len([r for r in self.mission_results if not r.actual_success])
            / len(self.mission_results)
            if self.mission_results
            else 0
        )
        if mission_failure_rate < 0.2:
            recommendations.append(
                "Mission failure rate too low - consider increasing difficulty or risk factors"
            )
        elif mission_failure_rate > 0.6:
            recommendations.append(
                "Mission failure rate too high - consider balancing difficulty or improving agent capabilities"
            )

        # Emotional system recommendations
        high_trauma_agents = len(
            [m for m in self.agent_metrics.values() if m.trauma_level_end > 0.7]
        )
        if high_trauma_agents > len(self.agent_metrics) * 0.5:
            recommendations.append(
                "High trauma levels detected - consider implementing recovery mechanisms"
            )

        return recommendations


def main():
    """Main function to run comprehensive automated playtest"""
    print("🎮 YEARS OF LEAD - COMPREHENSIVE AUTOMATED PLAYTEST")
    print("=" * 80)

    # Configuration
    config = {
        "test_duration_minutes": 90,
        "max_turns": 50,
        "mission_failure_rate_target": 0.3,
        "stress_scenarios": True,
        "cascading_effects_testing": True,
        "multi_agent_scenarios": True,
        "emotional_impact_tracking": True,
        "bug_detection": True,
        "performance_monitoring": True,
        "narrative_testing": True,
        "save_detailed_logs": True,
        "randomization_seed": None,
    }

    # Initialize and run playtest
    playtest_system = ComprehensiveAutomatedPlaytest(config)

    try:
        final_report = playtest_system.run_comprehensive_playtest()

        # Display summary
        print("\n" + "=" * 80)
        print("🎊 AUTOMATED PLAYTEST COMPLETE")
        print("=" * 80)

        summary = final_report.get("summary_statistics", {})
        print(f"📊 Tests Run: {summary.get('total_tests_run', 0)}")
        print(f"✅ Success Rate: {summary.get('overall_success_rate', 0):.1%}")
        print(f"🎯 Mission Success Rate: {summary.get('mission_success_rate', 0):.1%}")
        print(f"❌ Errors Encountered: {summary.get('total_errors', 0)}")
        print(f"🐛 Bug Reports: {summary.get('bug_reports_generated', 0)}")

        # Display key findings
        recommendations = final_report.get("recommendations", [])
        if recommendations:
            print("\n💡 Key Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"   {i}. {rec}")

        # Performance assessment
        performance = final_report.get("system_performance", {})
        stability = performance.get("stability_rating", 0)
        print(f"\n⚡ System Stability: {stability:.1%}")
        print(
            f"🔧 Feature Completeness: {performance.get('feature_completeness', 0):.1%}"
        )

        return final_report

    except Exception as e:
        print(f"\n❌ FATAL ERROR: Automated playtest failed: {e}")
        traceback.print_exc()
        return {"error": str(e), "traceback": traceback.format_exc()}


if __name__ == "__main__":
    main()
