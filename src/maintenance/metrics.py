"""
Metrics collection for maintenance mode.

Think of this as the game's health monitoring system. Just like a 
fitness tracker measures your heart rate and steps, this measures
the game's narrative quality, performance, and emotional consistency.
"""

import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re
from collections import Counter

class GameHealthMetrics:
    """Collects and analyzes game health metrics"""
    
    def __init__(self, game_instance=None):
        self.game = game_instance
        self.metrics_history = []
        self.performance_samples = []
        self.narrative_samples = []
        self.emotional_samples = []
        
        # Enhanced metrics analyzers - ITERATION 018
        self.narrative_analyzer = NarrativeCoherenceAnalyzer()
        self.emotional_analyzer = EmotionalConsistencyAnalyzer()
        self.tactical_analyzer = TacticalClarityAnalyzer()
    
    def measure_narrative_coherence(self) -> float:
        """
        Enhanced narrative coherence measurement using advanced analyzer.
        
        Returns a score from 0 (incoherent) to 1 (perfect).
        """
        try:
            if not self.game:
                return 0.7  # Default reasonable score
            
            # Gather mission reports for analysis
            mission_reports = getattr(self.game, 'recent_mission_reports', [])
            if not mission_reports:
                return self.measure_basic_narrative_coherence()  # Fallback to basic method
            
            coherence_scores = []
            for report in mission_reports[-5:]:  # Analyze last 5 missions
                mission_scores = self.narrative_analyzer.analyze_mission_narrative(report)
                mission_coherence = statistics.mean([
                    mission_scores.get('tone_consistency', 0.8),
                    mission_scores.get('cause_effect_logic', 0.8),
                    mission_scores.get('character_voice', 0.8),
                    mission_scores.get('vocabulary_variety', 0.8)
                ])
                
                # Apply repetition penalty
                repetition_penalty = mission_scores.get('repetition_penalty', 0.0)
                mission_coherence = max(0.1, mission_coherence - repetition_penalty)
                
                coherence_scores.append(mission_coherence)
            
            overall_coherence = statistics.mean(coherence_scores) if coherence_scores else 0.8
            return min(1.0, max(0.0, overall_coherence))
            
        except Exception as e:
            print(f"Error in enhanced narrative coherence measurement: {e}")
            return self.measure_basic_narrative_coherence()
    
    def measure_basic_narrative_coherence(self) -> float:
        """Basic narrative coherence as fallback"""
        try:
            # Analyze recent narrative events (original implementation)
            recent_events = getattr(self.game, 'recent_events', [])
            if not recent_events:
                return 0.8  # No events to analyze, assume good
            
            # Check for repetition
            descriptions = [event.get('description', '') for event in recent_events[-10:]]
            unique_descriptions = set(descriptions)
            repetition_score = len(unique_descriptions) / max(len(descriptions), 1)
            
            # Check for variety in vocabulary
            all_words = []
            for desc in descriptions:
                all_words.extend(desc.lower().split())
            
            unique_words = set(all_words)
            vocabulary_variety = min(1.0, len(unique_words) / max(len(all_words), 1) * 5)
            
            # Combine scores
            coherence_score = (repetition_score + vocabulary_variety) / 2
            return min(1.0, max(0.0, coherence_score))
            
        except Exception as e:
            print(f"Error measuring basic narrative coherence: {e}")
            return 0.7
    
    def measure_emotional_consistency(self) -> float:
        """
        Enhanced emotional consistency measurement using advanced analyzer.
        
        Returns a score from 0 (chaotic) to 1 (perfectly consistent).
        """
        try:
            if not self.game:
                return 0.8  # Default good score
                
            # Get agents for analysis
            agents = getattr(self.game, 'agents', [])
            if not agents:
                return 0.8
            
            # Use enhanced emotional analyzer
            consistency_analysis = self.emotional_analyzer.analyze_emotional_consistency(agents)
            
            # Calculate weighted overall score
            weights = {
                'state_stability': 0.25,
                'trauma_response': 0.2,
                'therapy_effectiveness': 0.2,
                'emotional_progression': 0.2,
                'behavioral_alignment': 0.15
            }
            
            weighted_score = 0.0
            for metric, weight in weights.items():
                if metric in consistency_analysis:
                    weighted_score += consistency_analysis[metric] * weight
                else:
                    weighted_score += 0.8 * weight  # Default value
            
            return min(1.0, max(0.0, weighted_score))
                
        except Exception as e:
            print(f"Error in enhanced emotional consistency measurement: {e}")
            return self.measure_basic_emotional_consistency()
    
    def measure_basic_emotional_consistency(self) -> float:
        """Basic emotional consistency as fallback"""
        try:
            # Check emotional state changes (original implementation)
            agents = getattr(self.game, 'agents', [])
            if not agents:
                return 0.8
            
            consistency_scores = []
            
            for agent in agents:
                emotional_state = getattr(agent, 'emotional_state', {})
                if not emotional_state:
                    continue
                
                # Check if emotions are within reasonable bounds
                bounds_check = all(
                    -1.0 <= value <= 1.0 
                    for value in emotional_state.values()
                    if isinstance(value, (int, float))
                )
                
                if bounds_check:
                    consistency_scores.append(1.0)
                else:
                    consistency_scores.append(0.0)
            
            if consistency_scores:
                return statistics.mean(consistency_scores)
            else:
                return 0.8
                
        except Exception as e:
            print(f"Error measuring basic emotional consistency: {e}")
            return 0.8
    
    def measure_tactical_clarity(self) -> float:
        """
        New metric: Measure tactical clarity and mission execution logic.
        
        Returns a score from 0 (chaotic) to 1 (perfectly clear).
        """
        try:
            if not self.game:
                return 0.8  # Default good score
            
            # Gather mission reports for tactical analysis
            mission_reports = getattr(self.game, 'recent_mission_reports', [])
            if not mission_reports:
                return 0.8  # No missions to analyze
            
            # Use tactical analyzer
            clarity_analysis = self.tactical_analyzer.analyze_tactical_clarity(mission_reports[-10:])
            
            # Extract overall clarity score
            return clarity_analysis.get('overall_clarity', 0.8)
            
        except Exception as e:
            print(f"Error measuring tactical clarity: {e}")
            return 0.8
    
    def measure_performance(self) -> float:
        """
        Measures game performance metrics.
        
        Returns a score from 0 (very slow) to 1 (optimal performance).
        """
        try:
            # Measure initialization time
            start_time = time.time()
            
            if self.game:
                # Try to perform a typical game operation
                test_operation_start = time.time()
                # Simulate a game step or update
                if hasattr(self.game, 'step'):
                    self.game.step()
                elif hasattr(self.game, 'update'):
                    self.game.update()
                test_operation_time = time.time() - test_operation_start
            else:
                test_operation_time = 0.01  # Simulate fast operation
            
            total_time = time.time() - start_time
            
            # Normalize performance score
            # Under 0.05s = 1.0, over 0.5s = 0.0
            performance_score = max(0.0, min(1.0, (0.5 - total_time) / 0.45))
            
            self.performance_samples.append(performance_score)
            
            # Keep only recent samples
            if len(self.performance_samples) > 50:
                self.performance_samples = self.performance_samples[-50:]
            
            return performance_score
            
        except Exception as e:
            print(f"Error measuring performance: {e}")
            return 0.5
    
    def get_performance_trend(self) -> str:
        """Get performance trend over recent samples"""
        if len(self.performance_samples) < 3:
            return "insufficient_data"
        
        recent = self.performance_samples[-5:]
        older = self.performance_samples[-10:-5] if len(self.performance_samples) >= 10 else []
        
        if not older:
            return "stable"
        
        recent_avg = statistics.mean(recent)
        older_avg = statistics.mean(older)
        
        if recent_avg > older_avg * 1.1:
            return "improving"
        elif recent_avg < older_avg * 0.9:
            return "degrading"
        else:
            return "stable"
    
    def measure_test_coverage(self, project_root: Path) -> float:
        """Measure test coverage percentage"""
        try:
            import subprocess
            import json
            
            result = subprocess.run(
                ["python3", "-m", "pytest", "--cov=src", "--cov-report=json", "-q"],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            if result.returncode == 0:
                coverage_file = project_root / "coverage.json"
                if coverage_file.exists():
                    with open(coverage_file) as f:
                        coverage_data = json.load(f)
                        return coverage_data.get("totals", {}).get("percent_covered", 0) / 100
            
            return 0.0
            
        except Exception as e:
            print(f"Error measuring test coverage: {e}")
            return 0.0
    
    def collect_comprehensive_metrics(self, project_root: Path = None) -> Dict:
        """Collect all available metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "narrative_coherence": self.measure_narrative_coherence(),
            "emotional_consistency": self.measure_emotional_consistency(),
            "performance": self.measure_performance(),
            "performance_trend": self.get_performance_trend(),
            "tactical_clarity": self.measure_tactical_clarity()
        }
        
        if project_root:
            metrics["test_coverage"] = self.measure_test_coverage(project_root)
        
        # Calculate overall health score
        health_components = [
            metrics["narrative_coherence"],
            metrics["emotional_consistency"],
            metrics["performance"],
            metrics["tactical_clarity"]
        ]
        
        if "test_coverage" in metrics:
            health_components.append(metrics["test_coverage"])
        
        metrics["overall_health"] = statistics.mean(health_components)
        
        # Store in history
        self.metrics_history.append(metrics)
        
        # Keep only recent history
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return metrics
    
    def get_health_summary(self) -> Dict:
        """Get a summary of recent health trends"""
        if not self.metrics_history:
            return {"status": "no_data", "recommendations": []}
        
        recent_metrics = self.metrics_history[-10:] if len(self.metrics_history) >= 10 else self.metrics_history
        
        if len(recent_metrics) < 2:
            return {"status": "insufficient_data", "recommendations": []}
        
        # Calculate trends
        health_scores = [m["overall_health"] for m in recent_metrics]
        performance_scores = [m["performance"] for m in recent_metrics]
        narrative_scores = [m["narrative_coherence"] for m in recent_metrics]
        
        health_trend = "stable"
        if len(health_scores) >= 3:
            if health_scores[-1] > health_scores[-3] * 1.05:
                health_trend = "improving"
            elif health_scores[-1] < health_scores[-3] * 0.95:
                health_trend = "declining"
        
        recommendations = []
        
        # Generate recommendations based on scores
        avg_performance = statistics.mean(performance_scores)
        avg_narrative = statistics.mean(narrative_scores)
        
        if avg_performance < 0.6:
            recommendations.append("Consider performance optimization")
        
        if avg_narrative < 0.7:
            recommendations.append("Review narrative variety and coherence")
        
        if health_trend == "declining":
            recommendations.append("System health is declining - investigate recent changes")
        
        return {
            "status": health_trend,
            "overall_health": statistics.mean(health_scores),
            "performance_avg": avg_performance,
            "narrative_avg": avg_narrative,
            "recommendations": recommendations
        }
    
    def export_metrics(self, output_path: Path):
        """Export metrics history to file"""
        import json
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "metrics_count": len(self.metrics_history),
            "health_summary": self.get_health_summary(),
            "metrics_history": self.metrics_history
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Metrics exported to {output_path}")

# Metrics System Expansion - ITERATION 018
class NarrativeCoherenceAnalyzer:
    """Advanced narrative coherence analysis with cause-effect tracking"""
    
    def __init__(self):
        self.narrative_elements = []
        self.cause_effect_chains = []
        self.tone_consistency_history = []
        self.repetition_patterns = {}
    
    def analyze_mission_narrative(self, mission_report: Dict) -> Dict[str, float]:
        """Analyze narrative coherence for a single mission"""
        scores = {
            'tone_consistency': 0.8,
            'cause_effect_logic': 0.8,
            'character_voice': 0.8,
            'vocabulary_variety': 0.8,
            'emotional_resonance': 0.8
        }
        
        narrative_text = mission_report.get('narrative_summary', '')
        emotional_tone = mission_report.get('emotional_tone', '')
        participants = mission_report.get('participants', [])
        
        if narrative_text:
            # Analyze tone consistency
            scores['tone_consistency'] = self._analyze_tone_consistency(narrative_text, emotional_tone)
            
            # Analyze vocabulary variety  
            scores['vocabulary_variety'] = self._analyze_vocabulary_variety(narrative_text)
            
            # Check for repetition patterns
            scores['repetition_penalty'] = self._check_repetition_patterns(narrative_text)
        
        # Analyze cause-effect logic from mission events
        if 'action_log' in mission_report:
            scores['cause_effect_logic'] = self._analyze_cause_effect_logic(mission_report['action_log'])
        
        # Analyze character voice consistency
        if participants:
            scores['character_voice'] = self._analyze_character_voices(mission_report, participants)
        
        return scores
    
    def _analyze_tone_consistency(self, narrative_text: str, expected_tone: str) -> float:
        """Analyze if narrative tone matches expected emotional tone"""
        tone_indicators = {
            'triumphant_victory': ['triumph', 'victory', 'success', 'brilliant', 'heroic'],
            'tragic': ['loss', 'sacrifice', 'tragic', 'sorrow', 'mourning'],
            'fearful_retreat': ['fear', 'retreat', 'escape', 'panic', 'terrifying'],
            'desperate_struggle': ['desperate', 'struggle', 'barely', 'barely survived'],
            'tactical_withdrawal': ['tactical', 'strategic', 'withdraw', 'regroup']
        }
        
        if expected_tone not in tone_indicators:
            return 0.8  # Unknown tone, assume reasonable
        
        expected_words = tone_indicators[expected_tone]
        text_lower = narrative_text.lower()
        
        matches = sum(1 for word in expected_words if word in text_lower)
        total_expected = len(expected_words)
        
        # Score based on presence of appropriate tone words
        tone_score = min(1.0, (matches / total_expected) + 0.5)
        
        # Penalty for contradictory tone words
        other_tones = {k: v for k, v in tone_indicators.items() if k != expected_tone}
        contradictions = 0
        for tone_words in other_tones.values():
            contradictions += sum(1 for word in tone_words if word in text_lower)
        
        contradiction_penalty = min(0.3, contradictions * 0.1)
        return max(0.1, tone_score - contradiction_penalty)
    
    def _analyze_vocabulary_variety(self, text: str) -> float:
        """Measure vocabulary diversity and sophistication"""
        words = re.findall(r'\b\w+\b', text.lower())
        if len(words) < 5:
            return 0.8
        
        unique_words = set(words)
        variety_ratio = len(unique_words) / len(words)
        
        # Check for sophisticated vocabulary
        sophisticated_words = [
            'coordination', 'tactical', 'strategic', 'reconnaissance', 'intelligence',
            'infiltration', 'extraction', 'surveillance', 'operational', 'contingency'
        ]
        
        sophistication_bonus = sum(1 for word in sophisticated_words if word in text.lower())
        sophistication_score = min(0.2, sophistication_bonus * 0.05)
        
        return min(1.0, variety_ratio * 1.5 + sophistication_score)
    
    def _check_repetition_patterns(self, text: str) -> float:
        """Check for repetitive patterns that reduce narrative quality"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 2:
            return 0.0
        
        # Check for repeated sentence structures
        structure_patterns = []
        for sentence in sentences:
            words = sentence.strip().split()
            if len(words) > 3:
                # Create pattern from first 3 words
                pattern = ' '.join(words[:3]).lower()
                structure_patterns.append(pattern)
        
        if len(structure_patterns) < 2:
            return 0.0
        
        pattern_counts = Counter(structure_patterns)
        repeated_patterns = sum(1 for count in pattern_counts.values() if count > 1)
        
        repetition_penalty = min(0.3, repeated_patterns * 0.1)
        return repetition_penalty
    
    def _analyze_cause_effect_logic(self, action_log: List[Dict]) -> float:
        """Analyze logical cause-effect relationships in mission events"""
        if len(action_log) < 2:
            return 0.8
        
        logical_sequences = 0
        total_sequences = len(action_log) - 1
        
        for i in range(len(action_log) - 1):
            current_action = action_log[i]
            next_action = action_log[i + 1]
            
            # Check for logical progression
            if self._is_logical_sequence(current_action, next_action):
                logical_sequences += 1
        
        return logical_sequences / total_sequences if total_sequences > 0 else 0.8
    
    def _is_logical_sequence(self, action1: Dict, action2: Dict) -> bool:
        """Check if two actions form a logical sequence"""
        # Simple logic checks
        outcome1 = action1.get('outcome', 'unknown')
        action_type2 = action2.get('action_type', 'unknown')
        
        # If first action failed, next should be defensive or escape
        if outcome1 == 'failure':
            return action_type2 in ['escape', 'retreat', 'defensive', 'medical']
        
        # If first action succeeded, next can be progression
        if outcome1 == 'success':
            return True  # Most sequences are valid after success
        
        return True  # Default to logical
    
    def _analyze_character_voices(self, mission_report: Dict, participants: List) -> float:
        """Analyze consistency of character voices and behavior"""
        if not participants:
            return 0.8
        
        character_consistency_score = 0.8
        
        # Check if character actions match their traits/emotional states
        for participant in participants:
            character_id = participant.get('agent_id') if isinstance(participant, dict) else str(participant)
            performance = mission_report.get('agent_performance', {}).get(character_id, {})
            
            if performance:
                # Check if performance aligns with character capabilities
                # This is a simplified check - in real implementation would check against character data
                action_count = len(performance.get('actions', []))
                if action_count > 0:
                    character_consistency_score += 0.1
        
        return min(1.0, character_consistency_score)

class EmotionalConsistencyAnalyzer:
    """Advanced emotional consistency tracking across agent states"""
    
    def __init__(self):
        self.emotional_state_history = {}
        self.trauma_response_patterns = []
        self.therapy_effectiveness_tracking = []
    
    def analyze_emotional_consistency(self, agents: List) -> Dict[str, float]:
        """Comprehensive emotional consistency analysis"""
        if not agents:
            return {'overall_consistency': 0.8}
        
        consistency_scores = {
            'state_stability': 0.8,
            'trauma_response': 0.8,
            'therapy_effectiveness': 0.8,
            'emotional_progression': 0.8,
            'behavioral_alignment': 0.8
        }
        
        total_agents = len(agents)
        stable_agents = 0
        
        for agent in agents:
            emotional_state = getattr(agent, 'emotional_state', None)
            if not emotional_state:
                continue
            
            agent_scores = self._analyze_agent_emotional_consistency(agent)
            
            # Aggregate scores
            for key in consistency_scores:
                if key in agent_scores:
                    consistency_scores[key] += agent_scores[key] / total_agents
            
            # Track emotional stability
            if self._is_emotionally_stable(emotional_state):
                stable_agents += 1
        
        # Calculate overall consistency
        consistency_scores['overall_consistency'] = statistics.mean(list(consistency_scores.values()))
        consistency_scores['stability_ratio'] = stable_agents / total_agents if total_agents > 0 else 0
        
        return consistency_scores
    
    def _analyze_agent_emotional_consistency(self, agent) -> Dict[str, float]:
        """Analyze emotional consistency for individual agent"""
        emotional_state = getattr(agent, 'emotional_state', None)
        if not emotional_state:
            return {}
        
        scores = {}
        agent_id = getattr(agent, 'id', 'unknown')
        
        # Track emotional state changes
        current_emotions = self._extract_emotion_values(emotional_state)
        if agent_id in self.emotional_state_history:
            previous_emotions = self.emotional_state_history[agent_id][-1] if self.emotional_state_history[agent_id] else current_emotions
            scores['emotional_progression'] = self._analyze_emotional_progression(previous_emotions, current_emotions)
        
        # Update history
        if agent_id not in self.emotional_state_history:
            self.emotional_state_history[agent_id] = []
        self.emotional_state_history[agent_id].append(current_emotions)
        
        # Keep only recent history
        if len(self.emotional_state_history[agent_id]) > 20:
            self.emotional_state_history[agent_id] = self.emotional_state_history[agent_id][-20:]
        
        # Analyze trauma response consistency
        if hasattr(emotional_state, 'trauma_level'):
            scores['trauma_response'] = self._analyze_trauma_response_consistency(emotional_state)
        
        # Analyze therapy effectiveness
        if hasattr(emotional_state, 'recovery_arcs'):
            scores['therapy_effectiveness'] = self._analyze_therapy_consistency(emotional_state)
        
        return scores
    
    def _extract_emotion_values(self, emotional_state) -> Dict[str, float]:
        """Extract emotion values from emotional state"""
        emotions = {}
        for emotion in ['fear', 'anger', 'sadness', 'joy', 'trust', 'anticipation', 'surprise', 'disgust']:
            if hasattr(emotional_state, emotion):
                emotions[emotion] = getattr(emotional_state, emotion)
        
        if hasattr(emotional_state, 'trauma_level'):
            emotions['trauma_level'] = emotional_state.trauma_level
        
        return emotions
    
    def _analyze_emotional_progression(self, previous: Dict[str, float], current: Dict[str, float]) -> float:
        """Analyze if emotional changes are realistic and gradual"""
        if not previous or not current:
            return 0.8
        
        total_change = 0.0
        dramatic_changes = 0
        
        for emotion in previous:
            if emotion in current:
                change = abs(current[emotion] - previous[emotion])
                total_change += change
                
                # Flag dramatic changes (more than 0.5 in one step)
                if change > 0.5:
                    dramatic_changes += 1
        
        # Reasonable emotional progression should be gradual
        average_change = total_change / len(previous) if previous else 0
        
        # Score based on gradual vs dramatic changes
        if average_change < 0.2:  # Very gradual
            base_score = 1.0
        elif average_change < 0.4:  # Moderate
            base_score = 0.8
        else:  # Dramatic
            base_score = 0.6
        
        # Penalty for too many dramatic changes
        dramatic_penalty = dramatic_changes * 0.1
        
        return max(0.1, base_score - dramatic_penalty)
    
    def _analyze_trauma_response_consistency(self, emotional_state) -> float:
        """Analyze if trauma responses are consistent and realistic"""
        trauma_level = getattr(emotional_state, 'trauma_level', 0)
        fear_level = getattr(emotional_state, 'fear', 0)
        
        # High trauma should correlate with some negative emotions
        if trauma_level > 0.7:
            if fear_level < 0.3 and getattr(emotional_state, 'sadness', 0) < 0.3:
                return 0.5  # Inconsistent - high trauma but no emotional impact
        
        # Check recovery arc consistency
        if hasattr(emotional_state, 'recovery_arcs'):
            recovery_arcs = emotional_state.recovery_arcs
            if recovery_arcs:
                for arc in recovery_arcs.values():
                    # Recovery progress should reduce trauma impact
                    if arc.total_progress > 0.8 and trauma_level > 0.5:
                        return 0.6  # Inconsistent - high recovery but high trauma
        
        return 0.9  # Generally consistent
    
    def _analyze_therapy_consistency(self, emotional_state) -> float:
        """Analyze therapy effectiveness and recovery arc realism"""
        if not hasattr(emotional_state, 'recovery_arcs'):
            return 0.8
        
        recovery_arcs = emotional_state.recovery_arcs
        if not recovery_arcs:
            return 0.8
        
        consistency_score = 0.8
        
        for arc in recovery_arcs.values():
            # Check realistic progression through therapy stages
            if arc.current_stage.value == 'maintenance' and arc.total_progress < 0.7:
                consistency_score -= 0.1  # Shouldn't reach maintenance without progress
            
            # Check relapse risk calculation
            if arc.total_progress > 0.9 and arc.relapse_risk > 0.5:
                consistency_score -= 0.1  # High progress should reduce relapse risk
        
        return max(0.1, consistency_score)
    
    def _is_emotionally_stable(self, emotional_state) -> bool:
        """Check if emotional state is within stable bounds"""
        # Check if all emotions are within reasonable bounds (-1.0 to 1.0)
        for emotion in ['fear', 'anger', 'sadness', 'joy', 'trust', 'anticipation', 'surprise', 'disgust']:
            if hasattr(emotional_state, emotion):
                value = getattr(emotional_state, emotion)
                if not (-1.0 <= value <= 1.0):
                    return False
        
        # Check trauma level bounds
        if hasattr(emotional_state, 'trauma_level'):
            trauma = emotional_state.trauma_level
            if not (0.0 <= trauma <= 1.0):
                return False
        
        return True

class TacticalClarityAnalyzer:
    """Analyzes clarity and logic of tactical mission execution"""
    
    def __init__(self):
        self.mission_execution_history = []
        self.objective_completion_patterns = []
    
    def analyze_tactical_clarity(self, mission_reports: List[Dict]) -> Dict[str, float]:
        """Analyze tactical clarity across multiple missions"""
        if not mission_reports:
            return {'overall_clarity': 0.8}
        
        clarity_scores = {
            'objective_clarity': 0.8,
            'execution_logic': 0.8,
            'resource_management': 0.8,
            'risk_assessment': 0.8,
            'team_coordination': 0.8
        }
        
        total_missions = len(mission_reports)
        
        for mission in mission_reports:
            mission_scores = self._analyze_mission_tactical_clarity(mission)
            
            for key in clarity_scores:
                if key in mission_scores:
                    clarity_scores[key] += mission_scores[key] / total_missions
        
        clarity_scores['overall_clarity'] = statistics.mean(list(clarity_scores.values()))
        
        return clarity_scores
    
    def _analyze_mission_tactical_clarity(self, mission_report: Dict) -> Dict[str, float]:
        """Analyze tactical clarity for a single mission"""
        scores = {}
        
        # Analyze objective completion clarity
        objectives_completed = mission_report.get('objectives_completed', [])
        objectives_failed = mission_report.get('objectives_failed', [])
        total_objectives = len(objectives_completed) + len(objectives_failed)
        
        if total_objectives > 0:
            completion_ratio = len(objectives_completed) / total_objectives
            scores['objective_clarity'] = completion_ratio
        
        # Analyze execution logic
        action_log = mission_report.get('action_log', [])
        if action_log:
            scores['execution_logic'] = self._analyze_execution_logic(action_log)
        
        # Analyze team coordination
        agent_performance = mission_report.get('agent_performance', {})
        if agent_performance:
            scores['team_coordination'] = self._analyze_team_coordination(agent_performance)
        
        return scores
    
    def _analyze_execution_logic(self, action_log: List[Dict]) -> float:
        """Analyze if mission execution follows logical tactical principles"""
        if len(action_log) < 2:
            return 0.8
        
        logical_actions = 0
        total_actions = len(action_log)
        
        for i, action in enumerate(action_log):
            # Check if action type is appropriate for phase
            phase = action.get('phase', 'unknown')
            action_type = action.get('action_type', 'unknown')
            
            if self._is_action_appropriate_for_phase(action_type, phase):
                logical_actions += 1
        
        return logical_actions / total_actions if total_actions > 0 else 0.8
    
    def _is_action_appropriate_for_phase(self, action_type: str, phase: str) -> bool:
        """Check if action type is appropriate for mission phase"""
        phase_appropriate_actions = {
            'planning': ['reconnaissance', 'intelligence', 'preparation'],
            'infiltration': ['stealth', 'movement', 'surveillance'],
            'execution': ['combat', 'objective', 'sabotage'],
            'extraction': ['escape', 'withdrawal', 'evasion'],
            'aftermath': ['medical', 'debriefing', 'cleanup']
        }
        
        if phase not in phase_appropriate_actions:
            return True  # Unknown phase, assume appropriate
        
        appropriate_actions = phase_appropriate_actions[phase]
        return any(appropriate in action_type.lower() for appropriate in appropriate_actions)
    
    def _analyze_team_coordination(self, agent_performance: Dict) -> float:
        """Analyze how well the team worked together"""
        if not agent_performance:
            return 0.8
        
        success_rates = []
        for agent_id, performance in agent_performance.items():
            actions = performance.get('actions', [])
            if actions:
                successful_actions = sum(1 for action in actions if action.get('outcome') == 'success')
                success_rate = successful_actions / len(actions)
                success_rates.append(success_rate)
        
        if not success_rates:
            return 0.8
        
        # Good coordination = similar success rates across team
        avg_success = statistics.mean(success_rates)
        success_variance = statistics.variance(success_rates) if len(success_rates) > 1 else 0
        
        # Lower variance = better coordination
        coordination_score = max(0.3, avg_success - success_variance)
        
        return min(1.0, coordination_score) 