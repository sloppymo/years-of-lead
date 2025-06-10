"""
Performance Validation Pipeline - ITERATION 019

Tests to validate that iterations 011-018 have measurably improved:
- Narrative variety and coherence
- Emotional reactivity and consistency  
- Tactical balance and intelligence
- Overall system health metrics
"""

import pytest
import statistics
from datetime import datetime, timedelta
from pathlib import Path
import sys
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from maintenance.metrics import GameHealthMetrics, NarrativeCoherenceAnalyzer, EmotionalConsistencyAnalyzer, TacticalClarityAnalyzer
from game.emotional_state import EmotionalState, TherapyType, SpecificTraumaType, TraumaMemory, TraumaTriggerType
from game.factions import FactionDynamics
from game.mission_planning import LocationProfile, PropagandaMessage
from game.intelligence_system import IntelligenceDatabase, IntelligenceQuality, IntelligenceTrait

class MockGameInstance:
    """Mock game instance for testing metrics"""
    
    def __init__(self):
        self.agents = []
        self.recent_events = []
        self.recent_mission_reports = []
        self.faction_dynamics = FactionDynamics()
        self.intelligence_db = IntelligenceDatabase()
    
    def add_mock_agent(self, agent_id: str, emotional_state: EmotionalState):
        """Add mock agent with emotional state"""
        class MockAgent:
            def __init__(self, agent_id, emotional_state):
                self.id = agent_id
                self.emotional_state = emotional_state
        
        agent = MockAgent(agent_id, emotional_state)
        self.agents.append(agent)
        return agent
    
    def add_mock_mission_report(self, report_data: dict):
        """Add mock mission report for testing"""
        self.recent_mission_reports.append(report_data)

class TestEnhancedTherapySystem:
    """Test that enhanced therapy system (Iteration 016) improves emotional consistency"""
    
    def test_therapy_progression_tracking(self):
        """Test that therapy recovery arcs provide realistic progression"""
        emotional_state = EmotionalState()
        
        # Create recovery arc for PTSD
        trauma_memory = TraumaMemory(
            trauma_type="violence_witnessed",
            severity=0.8,
            occurred_date=datetime.now(),
            triggers=[TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES],
            description="Witnessed teammate being shot"
        )
        
        arc_id = emotional_state.create_recovery_arc(trauma_memory, SpecificTraumaType.PTSD)
        
        # Simulate therapy sessions
        initial_trauma = emotional_state.trauma_level
        therapy_results = []
        
        for session in range(10):
            result = emotional_state.apply_enhanced_therapy(
                therapy_type=TherapyType.PROFESSIONAL,
                duration_hours=1.0,
                focus_trauma_id=arc_id,
                relationship_strength=0.7
            )
            therapy_results.append(result)
        
        # Validate progression
        arc = emotional_state.recovery_arcs[arc_id]
        
        assert arc.sessions_completed == 10
        assert arc.total_progress > 0.0, "Therapy should show progress"
        assert emotional_state.trauma_level < initial_trauma, "Trauma level should decrease"
        
        # Check for stage advancement
        stage_advancements = sum(1 for result in therapy_results if result.get('stage_advancement', False))
        assert stage_advancements > 0, "Should have some stage advancements"
    
    def test_relationship_therapy_bonuses(self):
        """Test that relationship bonuses improve therapy effectiveness"""
        emotional_state = EmotionalState()
        emotional_state.add_mentor_relationship("mentor_001")
        
        # Test mentor guidance without established relationship
        weak_result = emotional_state.apply_enhanced_therapy(
            therapy_type=TherapyType.MENTOR_GUIDANCE,
            therapist_id="stranger_001",
            relationship_strength=0.2
        )
        
        # Test mentor guidance with established relationship
        strong_result = emotional_state.apply_enhanced_therapy(
            therapy_type=TherapyType.MENTOR_GUIDANCE,
            therapist_id="mentor_001",
            relationship_strength=0.9
        )
        
        assert strong_result['effectiveness'] > weak_result['effectiveness'], \
            "Mentor guidance should be more effective with established relationships"
    
    def test_relapse_system(self):
        """Test that relapse system creates realistic setbacks"""
        emotional_state = EmotionalState()
        
        # Create recovery arc
        trauma_memory = TraumaMemory(
            trauma_type="grief",
            severity=0.6,
            occurred_date=datetime.now(),
            triggers=[TraumaTriggerType.ABANDONMENT],
            description="Lost close friend in mission"
        )
        
        arc_id = emotional_state.create_recovery_arc(trauma_memory, SpecificTraumaType.GRIEF)
        arc = emotional_state.recovery_arcs[arc_id]
        
        # Simulate high relapse risk scenario
        arc.total_progress = 0.3  # Low progress
        arc.support_strength = 0.1  # Poor support
        arc.last_session = datetime.now() - timedelta(days=30)  # No recent therapy
        
        # Check relapse risk calculation
        relapse_risk = arc.calculate_relapse_risk()
        assert relapse_risk > 0.5, "Should have high relapse risk with poor conditions"
        
        # Improve conditions
        arc.total_progress = 0.8
        arc.support_strength = 0.9
        arc.last_session = datetime.now()
        
        improved_risk = arc.calculate_relapse_risk()
        assert improved_risk < relapse_risk, "Improved conditions should reduce relapse risk"

class TestReactiveIntelligence:
    """Test that reactive intelligence system (Iteration 017) creates dynamic information quality"""
    
    def test_intelligence_quality_degradation(self):
        """Test that intelligence quality degrades under pressure"""
        intel_db = IntelligenceDatabase()
        
        # Simulate multiple mission failures
        for _ in range(3):
            intel_db.update_from_mission_outcome(
                outcome='failure',
                heat_level=8.0,
                faction_morale=40.0,
                faction_loyalty=30.0
            )
        
        # Check that quality degraded
        current_quality = intel_db.reactivity.calculate_current_quality()
        assert current_quality < 0.7, "Quality should degrade after multiple failures"
        
        # Check trap probability increased
        assert intel_db.reactivity.trap_probability > 0.3, "Trap probability should increase with high heat"
    
    def test_trap_intelligence_detection(self):
        """Test that trap intelligence includes warning indicators"""
        intel_db = IntelligenceDatabase()
        
        # Force high trap probability
        intel_db.reactivity.trap_probability = 0.8
        
        # Generate intelligence - should often be traps
        trap_count = 0
        total_generated = 20
        
        for _ in range(total_generated):
            from game.intelligence_system import IntelligenceType
            event = intel_db.generate_reactive_intelligence(
                event_type=IntelligenceType.FACILITY_SECURITY,
                location="test_location"
            )
            
            if event.is_trap():
                trap_count += 1
                assert len(event.trap_indicators) > 0, "Trap intelligence should have warning indicators"
                assert 'EASY TARGET' in str(event.action_opportunities), "Traps should look tempting"
        
        assert trap_count > 0, "Should generate some trap intelligence with high probability"
    
    def test_intelligence_source_compromise(self):
        """Test that failed missions can compromise intelligence sources"""
        intel_db = IntelligenceDatabase()
        
        # Add some sources
        intel_db.reactivity.source_reliability = {
            'source_001': 0.8,
            'source_002': 0.9,
            'source_003': 0.7
        }
        
        initial_compromised = len(intel_db.reactivity.compromised_sources)
        
        # Simulate multiple disasters - should compromise sources
        for _ in range(5):
            intel_db.update_from_mission_outcome(
                outcome='disaster',
                heat_level=9.0,
                faction_morale=20.0,
                faction_loyalty=15.0
            )
        
        final_compromised = len(intel_db.reactivity.compromised_sources)
        assert final_compromised > initial_compromised, "Disasters should compromise some sources"

class TestFactionDynamics:
    """Test that faction dynamics system (Iteration 011) creates organizational evolution"""
    
    def test_faction_health_impacts(self):
        """Test that faction health responds to mission outcomes"""
        faction = FactionDynamics()
        
        initial_morale = faction.morale
        initial_loyalty = faction.loyalty
        
        # Simulate mission with betrayal
        faction.apply_mission_impact(
            outcome='failure',
            mission_type='infiltration',
            agents_lost=1,
            betrayal_occurred=True,
            heroic_actions=0
        )
        
        assert faction.loyalty < initial_loyalty, "Betrayal should damage loyalty"
        assert faction.morale < initial_morale, "Failure should damage morale"
        
        # Simulate heroic success
        faction.apply_mission_impact(
            outcome='critical_success',
            mission_type='propaganda',
            agents_lost=0,
            betrayal_occurred=False,
            heroic_actions=2
        )
        
        assert faction.morale > initial_morale, "Heroic success should boost morale"

class TestSymbolicGeography:
    """Test that symbolic geography system (Iteration 012) affects mission dynamics"""
    
    def test_location_symbolic_modifiers(self):
        """Test that location symbolism affects mission parameters"""
        # Create location with high symbolic value
        location = LocationProfile(location_name="Liberation Square")
        location.assign_symbolic_identity()
        
        # Check that symbolism affects mission planning
        initial_modifiers = location.get_mission_modifiers()
        
        # Should have some symbolic effects
        assert any(abs(value) > 0.1 for value in initial_modifiers.values()), \
            "Symbolic locations should have meaningful modifiers"
        
        # Test emotional resonance
        resonance = location.emotional_resonance
        assert -1.0 <= resonance <= 1.0, "Emotional resonance should be within bounds"

class TestMetricsValidation:
    """Test that enhanced metrics system (Iteration 018) detects quality improvements"""
    
    def test_narrative_coherence_analysis(self):
        """Test that narrative analyzer detects coherence patterns"""
        analyzer = NarrativeCoherenceAnalyzer()
        
        # Create high-quality mission report
        good_report = {
            'narrative_summary': "The team executed a brilliant tactical infiltration. Through careful coordination and strategic patience, they achieved their objective without casualties.",
            'emotional_tone': 'triumphant_victory',
            'participants': ['agent_001', 'agent_002'],
            'action_log': [
                {'action_type': 'reconnaissance', 'outcome': 'success', 'phase': 'planning'},
                {'action_type': 'stealth', 'outcome': 'success', 'phase': 'infiltration'},
                {'action_type': 'objective', 'outcome': 'success', 'phase': 'execution'}
            ]
        }
        
        good_scores = analyzer.analyze_mission_narrative(good_report)
        
        # Create low-quality mission report
        bad_report = {
            'narrative_summary': "The team did stuff. They did more stuff. Stuff happened again.",
            'emotional_tone': 'triumphant_victory',
            'participants': ['agent_001'],
            'action_log': [
                {'action_type': 'random', 'outcome': 'failure', 'phase': 'planning'},
                {'action_type': 'combat', 'outcome': 'failure', 'phase': 'planning'}  # Illogical sequence
            ]
        }
        
        bad_scores = analyzer.analyze_mission_narrative(bad_report)
        
        # Good report should score higher
        assert good_scores['vocabulary_variety'] > bad_scores['vocabulary_variety'], \
            "Good report should have better vocabulary variety"
        assert good_scores['cause_effect_logic'] > bad_scores['cause_effect_logic'], \
            "Good report should have better logical flow"
    
    def test_emotional_consistency_tracking(self):
        """Test emotional consistency analyzer detects realistic vs unrealistic changes"""
        analyzer = EmotionalConsistencyAnalyzer()
        
        # Create agent with gradual emotional changes (realistic)
        game = MockGameInstance()
        
        # Agent with realistic emotional progression
        realistic_state = EmotionalState(fear=0.3, sadness=0.2, trauma_level=0.4)
        realistic_agent = game.add_mock_agent("realistic_agent", realistic_state)
        
        # Simulate gradual changes
        analyzer.emotional_state_history["realistic_agent"] = [
            {'fear': 0.5, 'sadness': 0.4, 'trauma_level': 0.6},  # Previous state
        ]
        
        realistic_scores = analyzer.analyze_emotional_consistency([realistic_agent])
        
        # Agent with dramatic unrealistic changes
        dramatic_state = EmotionalState(fear=-0.8, sadness=0.9, trauma_level=0.1)  # Dramatic shift
        dramatic_agent = game.add_mock_agent("dramatic_agent", dramatic_state)
        
        analyzer.emotional_state_history["dramatic_agent"] = [
            {'fear': 0.8, 'sadness': -0.5, 'trauma_level': 0.9},  # Completely different
        ]
        
        dramatic_scores = analyzer.analyze_emotional_consistency([dramatic_agent])
        
        # Realistic changes should score higher
        assert realistic_scores['overall_consistency'] > dramatic_scores['overall_consistency'], \
            "Gradual changes should score higher than dramatic shifts"
    
    def test_tactical_clarity_assessment(self):
        """Test tactical clarity analyzer measures mission execution quality"""
        analyzer = TacticalClarityAnalyzer()
        
        # High-clarity mission
        clear_mission = {
            'objectives_completed': ['infiltrate', 'extract_intel', 'escape'],
            'objectives_failed': [],
            'action_log': [
                {'action_type': 'reconnaissance', 'phase': 'planning'},
                {'action_type': 'stealth', 'phase': 'infiltration'},
                {'action_type': 'objective', 'phase': 'execution'},
                {'action_type': 'escape', 'phase': 'extraction'}
            ],
            'agent_performance': {
                'agent_001': {'actions': [{'outcome': 'success'}, {'outcome': 'success'}]},
                'agent_002': {'actions': [{'outcome': 'success'}, {'outcome': 'success'}]}
            }
        }
        
        # Low-clarity mission
        unclear_mission = {
            'objectives_completed': [],
            'objectives_failed': ['infiltrate', 'extract_intel'],
            'action_log': [
                {'action_type': 'combat', 'phase': 'planning'},  # Illogical
                {'action_type': 'reconnaissance', 'phase': 'extraction'}  # Wrong phase
            ],
            'agent_performance': {
                'agent_001': {'actions': [{'outcome': 'failure'}, {'outcome': 'failure'}]},
                'agent_002': {'actions': [{'outcome': 'success'}, {'outcome': 'failure'}]}
            }
        }
        
        clear_scores = analyzer.analyze_tactical_clarity([clear_mission])
        unclear_scores = analyzer.analyze_tactical_clarity([unclear_mission])
        
        assert clear_scores['overall_clarity'] > unclear_scores['overall_clarity'], \
            "Well-executed mission should have higher clarity than chaotic one"

class TestSystemIntegration:
    """Test that all enhanced systems work together to improve overall health"""
    
    def test_comprehensive_health_improvement(self):
        """Test that enhanced systems collectively improve health metrics"""
        # Create game instance with enhanced systems
        game = MockGameInstance()
        metrics = GameHealthMetrics(game)
        
        # Add high-quality agents with realistic emotional states
        for i in range(3):
            emotional_state = EmotionalState(fear=0.2, trust=0.6, trauma_level=0.1)
            game.add_mock_agent(f"agent_{i}", emotional_state)
        
        # Add high-quality mission reports
        game.add_mock_mission_report({
            'narrative_summary': "Through careful planning and excellent teamwork, the mission succeeded brilliantly.",
            'emotional_tone': 'triumphant_victory',
            'participants': ['agent_0', 'agent_1'],
            'action_log': [
                {'action_type': 'reconnaissance', 'outcome': 'success', 'phase': 'planning'},
                {'action_type': 'objective', 'outcome': 'success', 'phase': 'execution'}
            ],
            'objectives_completed': ['primary_objective'],
            'objectives_failed': [],
            'agent_performance': {
                'agent_0': {'actions': [{'outcome': 'success'}]},
                'agent_1': {'actions': [{'outcome': 'success'}]}
            }
        })
        
        # Collect comprehensive metrics
        health_metrics = metrics.collect_comprehensive_metrics()
        
        # Validate high-quality metrics
        assert health_metrics['narrative_coherence'] >= 0.7, \
            f"Narrative coherence should be high: {health_metrics['narrative_coherence']}"
        assert health_metrics['emotional_consistency'] >= 0.7, \
            f"Emotional consistency should be high: {health_metrics['emotional_consistency']}"
        assert health_metrics['tactical_clarity'] >= 0.7, \
            f"Tactical clarity should be high: {health_metrics['tactical_clarity']}"
        assert health_metrics['overall_health'] >= 0.7, \
            f"Overall health should be high: {health_metrics['overall_health']}"

def test_performance_validation_suite():
    """Main validation test that ensures recent improvements work"""
    print("\n=== PERFORMANCE VALIDATION SUITE - ITERATION 019 ===")
    
    # Test individual systems
    therapy_test = TestEnhancedTherapySystem()
    therapy_test.test_therapy_progression_tracking()
    therapy_test.test_relationship_therapy_bonuses()
    therapy_test.test_relapse_system()
    print("✓ Enhanced Therapy System validated")
    
    intel_test = TestReactiveIntelligence()
    intel_test.test_intelligence_quality_degradation()
    intel_test.test_trap_intelligence_detection()
    intel_test.test_intelligence_source_compromise()
    print("✓ Reactive Intelligence System validated")
    
    faction_test = TestFactionDynamics()
    faction_test.test_faction_health_impacts()
    print("✓ Faction Dynamics System validated")
    
    geography_test = TestSymbolicGeography()
    geography_test.test_location_symbolic_modifiers()
    print("✓ Symbolic Geography System validated")
    
    metrics_test = TestMetricsValidation()
    metrics_test.test_narrative_coherence_analysis()
    metrics_test.test_emotional_consistency_tracking()
    metrics_test.test_tactical_clarity_assessment()
    print("✓ Enhanced Metrics System validated")
    
    integration_test = TestSystemIntegration()
    integration_test.test_comprehensive_health_improvement()
    print("✓ System Integration validated")
    
    print("\n=== ALL VALIDATION TESTS PASSED ===")
    print("Iterations 011-018 have successfully enhanced:")
    print("  • Narrative variety and coherence")
    print("  • Emotional reactivity and consistency")
    print("  • Tactical balance and intelligence")
    print("  • Overall system health measurement")
    
    return True

if __name__ == "__main__":
    test_performance_validation_suite()