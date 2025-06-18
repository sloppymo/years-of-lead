"""
Years of Lead - Enhanced Simulation Integration System

Comprehensive integration of all enhanced systems:
- Phase 1: Agent Autonomy Enhancement
- Phase 2: Mission Outcome Enhancement  
- Phase 3: Real-time Intelligence Systems
- Phase 4: Dynamic Narrative Generation
- Phase 5: Advanced Trauma and Psychological Impact

This system coordinates all enhanced features into a unified simulation experience.
"""

import random
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class SimulationTurn:
    """Represents a complete simulation turn with all enhanced systems"""
    turn_number: int
    timestamp: datetime
    autonomy_results: Dict[str, Any] = field(default_factory=dict)
    mission_results: Dict[str, Any] = field(default_factory=dict)
    intelligence_results: Dict[str, Any] = field(default_factory=dict)
    narrative_results: Dict[str, Any] = field(default_factory=dict)
    trauma_results: Dict[str, Any] = field(default_factory=dict)
    integration_events: List[Dict[str, Any]] = field(default_factory=list)
    system_synergies: List[Dict[str, Any]] = field(default_factory=list)


class EnhancedSimulationIntegration:
    """Main integration system for all enhanced simulation features"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.turn_history: List[SimulationTurn] = []
        
        # Initialize all enhanced systems
        self.initialize_enhanced_systems()
        
        # Integration parameters
        self.synergy_threshold = 0.6
        self.cross_system_impact_modifier = 0.3
        self.emergent_complexity_enabled = True
        
        # Performance tracking
        self.system_performance: Dict[str, Dict[str, Any]] = {}
        self.integration_metrics: Dict[str, float] = {}
        
        logger.info("Enhanced Simulation Integration System initialized")
    
    def initialize_enhanced_systems(self):
        """Initialize all enhanced simulation systems"""
        
        # Phase 1: Agent Autonomy Enhancement
        try:
            from .enhanced_agent_autonomy import EnhancedAgentAutonomySystem
            self.autonomy_system = EnhancedAgentAutonomySystem(self.game_state)
            logger.info("Agent Autonomy System initialized")
        except ImportError as e:
            logger.warning(f"Could not initialize Agent Autonomy System: {e}")
            self.autonomy_system = None
        
        # Phase 2: Mission Outcome Enhancement
        try:
            from .enhanced_mission_system import EnhancedMissionExecutor
            self.mission_system = EnhancedMissionExecutor(self.game_state)
            logger.info("Mission Enhancement System initialized")
        except ImportError as e:
            logger.warning(f"Could not initialize Mission Enhancement System: {e}")
            self.mission_system = None
        
        # Phase 3: Real-time Intelligence Systems
        try:
            from .enhanced_intelligence_system import EnhancedIntelligenceSystem
            self.intelligence_system = EnhancedIntelligenceSystem(self.game_state)
            logger.info("Intelligence Enhancement System initialized")
        except ImportError as e:
            logger.warning(f"Could not initialize Intelligence Enhancement System: {e}")
            self.intelligence_system = None
        
        # Phase 4: Dynamic Narrative Generation
        try:
            from .enhanced_narrative_system import EnhancedDynamicNarrativeSystem
            self.narrative_system = EnhancedDynamicNarrativeSystem(self.game_state)
            logger.info("Narrative Enhancement System initialized")
        except ImportError as e:
            logger.warning(f"Could not initialize Narrative Enhancement System: {e}")
            self.narrative_system = None
        
        # Phase 5: Advanced Trauma and Psychological Impact
        try:
            from .advanced_trauma_system import AdvancedTraumaSystem
            self.trauma_system = AdvancedTraumaSystem(self.game_state)
            logger.info("Trauma Enhancement System initialized")
        except ImportError as e:
            logger.warning(f"Could not initialize Trauma Enhancement System: {e}")
            self.trauma_system = None
    
    def process_enhanced_turn(self) -> SimulationTurn:
        """Process a complete enhanced simulation turn"""
        
        current_turn = getattr(self.game_state, 'turn_number', len(self.turn_history) + 1)
        timestamp = datetime.now()
        
        # Initialize turn
        turn = SimulationTurn(
            turn_number=current_turn,
            timestamp=timestamp
        )
        
        logger.info(f"Processing enhanced turn {current_turn}")
        
        # Process each enhanced system
        if self.autonomy_system:
            turn.autonomy_results = self.autonomy_system.process_autonomous_decisions()
            logger.debug(f"Autonomy system processed: {len(turn.autonomy_results.get('decisions_made', []))} decisions")
        
        if self.intelligence_system:
            turn.intelligence_results = self.intelligence_system.process_real_time_intelligence()
            logger.debug(f"Intelligence system processed: {len(turn.intelligence_results.get('new_intelligence', []))} events")
        
        if self.narrative_system:
            turn.narrative_results = self.narrative_system.process_dynamic_narrative()
            logger.debug(f"Narrative system processed: {len(turn.narrative_results.get('story_events', []))} events")
        
        if self.trauma_system:
            turn.trauma_results = self.trauma_system.process_trauma_system()
            logger.debug(f"Trauma system processed: {len(turn.trauma_results.get('new_trauma_events', []))} events")
        
        # Process cross-system integration
        turn.integration_events = self._process_cross_system_integration(turn)
        turn.system_synergies = self._identify_system_synergies(turn)
        
        # Apply emergent complexity
        if self.emergent_complexity_enabled:
            self._apply_emergent_complexity(turn)
        
        # Store turn
        self.turn_history.append(turn)
        
        # Update performance metrics
        self._update_performance_metrics(turn)
        
        logger.info(f"Enhanced turn {current_turn} completed with {len(turn.integration_events)} integration events")
        
        return turn
    
    def _process_cross_system_integration(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Process integration between different enhanced systems"""
        integration_events = []
        
        # Autonomy + Intelligence integration
        if turn.autonomy_results and turn.intelligence_results:
            autonomy_intel_events = self._integrate_autonomy_intelligence(turn)
            integration_events.extend(autonomy_intel_events)
        
        # Intelligence + Narrative integration
        if turn.intelligence_results and turn.narrative_results:
            intel_narrative_events = self._integrate_intelligence_narrative(turn)
            integration_events.extend(intel_narrative_events)
        
        # Trauma + Autonomy integration
        if turn.trauma_results and turn.autonomy_results:
            trauma_autonomy_events = self._integrate_trauma_autonomy(turn)
            integration_events.extend(trauma_autonomy_events)
        
        # Narrative + Trauma integration
        if turn.narrative_results and turn.trauma_results:
            narrative_trauma_events = self._integrate_narrative_trauma(turn)
            integration_events.extend(narrative_trauma_events)
        
        # Mission + All systems integration
        if self.mission_system:
            mission_integration_events = self._integrate_mission_systems(turn)
            integration_events.extend(mission_integration_events)
        
        return integration_events
    
    def _integrate_autonomy_intelligence(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Integrate autonomous decisions with intelligence gathering"""
        events = []
        
        # Autonomous agents can gather intelligence
        for decision in turn.autonomy_results.get("decisions_made", []):
            if decision.action_type.value == "gather_intelligence":
                # Check if intelligence system has relevant information
                actionable_intel = turn.intelligence_results.get("actionable_intel", [])
                if actionable_intel:
                    events.append({
                        "type": "autonomy_intelligence_synergy",
                        "description": f"Agent {decision.agent_id} autonomously gathers actionable intelligence",
                        "intelligence_gained": len(actionable_intel),
                        "decision_quality": "enhanced"
                    })
        
        # Intelligence affects autonomous decision quality
        threat_alerts = turn.intelligence_results.get("priority_alerts", [])
        if threat_alerts:
            for decision in turn.autonomy_results.get("decisions_made", []):
                if decision.action_type.value in ["seek_safety", "avoid_threat"]:
                    events.append({
                        "type": "intelligence_autonomy_guidance",
                        "description": f"Intelligence alerts guide agent {decision.agent_id}'s autonomous safety decisions",
                        "decision_effectiveness": "improved",
                        "threat_awareness": "enhanced"
                    })
        
        return events
    
    def _integrate_intelligence_narrative(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Integrate intelligence with narrative generation"""
        events = []
        
        # Intelligence patterns create narrative hooks
        patterns = turn.intelligence_results.get("patterns_detected", [])
        for pattern in patterns:
            if pattern.confidence > 0.8:
                events.append({
                    "type": "intelligence_narrative_pattern",
                    "description": f"High-confidence intelligence pattern '{pattern.description}' generates narrative content",
                    "pattern_type": pattern.pattern_type,
                    "narrative_quality": "enhanced"
                })
        
        # Narrative arcs influence intelligence priorities
        active_arcs = turn.narrative_results.get("arc_advancements", [])
        for arc in active_arcs:
            if arc.get("story_element", {}).get("emotional_impact", {}).get("fear", 0) > 0.3:
                events.append({
                    "type": "narrative_intelligence_priority",
                    "description": f"Narrative fear triggers increased intelligence monitoring",
                    "intelligence_focus": "heightened",
                    "monitoring_intensity": "increased"
                })
        
        return events
    
    def _integrate_trauma_autonomy(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Integrate trauma system with autonomous decisions"""
        events = []
        
        # Trauma affects autonomous decision quality
        new_trauma = turn.trauma_results.get("new_trauma_events", [])
        for trauma in new_trauma:
            agent_id = trauma.get("agent_id")
            if agent_id:
                # Modify agent's autonomy profile based on trauma
                if self.autonomy_system and agent_id in self.autonomy_system.agent_profiles:
                    profile = self.autonomy_system.agent_profiles[agent_id]
                    profile.risk_tolerance = max(0.0, profile.risk_tolerance - 0.2)
                    profile.emotional_stability = max(0.0, profile.emotional_stability - 0.3)
                    
                    events.append({
                        "type": "trauma_autonomy_modification",
                        "description": f"Trauma modifies agent {agent_id}'s autonomous decision-making",
                        "risk_tolerance": "reduced",
                        "emotional_stability": "reduced"
                    })
        
        # Autonomous decisions can trigger trauma recovery
        for decision in turn.autonomy_results.get("decisions_made", []):
            if decision.action_type.value == "seek_medical_help":
                events.append({
                    "type": "autonomy_trauma_recovery",
                    "description": f"Agent {decision.agent_id} autonomously seeks trauma recovery",
                    "recovery_initiated": True,
                    "healing_progress": "started"
                })
        
        return events
    
    def _integrate_narrative_trauma(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Integrate narrative system with trauma system"""
        events = []
        
        # Narrative arcs can trigger trauma events
        for arc in turn.narrative_results.get("new_arcs", []):
            if arc.arc_type.value == "betrayal":
                # Create trauma event from betrayal narrative
                events.append({
                    "type": "narrative_trauma_trigger",
                    "description": f"Betrayal narrative arc triggers trauma for agents {arc.agents_involved}",
                    "trauma_type": "betrayal_trauma",
                    "narrative_cause": "betrayal_arc"
                })
        
        # Trauma events create narrative content
        psychological_crises = turn.trauma_results.get("psychological_crises", [])
        for crisis in psychological_crises:
            events.append({
                "type": "trauma_narrative_content",
                "description": f"Psychological crisis creates narrative content for agent {crisis['agent_id']}",
                "crisis_type": crisis["crisis_type"],
                "narrative_impact": "significant"
            })
        
        return events
    
    def _integrate_mission_systems(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Integrate mission system with all other systems"""
        events = []
        
        # Check for active missions and integrate with other systems
        if hasattr(self.game_state, 'active_missions'):
            for mission in self.game_state.active_missions:
                # Mission + Intelligence integration
                if turn.intelligence_results:
                    actionable_intel = turn.intelligence_results.get("actionable_intel", [])
                    if actionable_intel:
                        events.append({
                            "type": "mission_intelligence_support",
                            "description": f"Intelligence supports mission {mission.get('id', 'unknown')}",
                            "intelligence_quality": "actionable",
                            "mission_effectiveness": "enhanced"
                        })
                
                # Mission + Trauma integration
                if turn.trauma_results:
                    agent_trauma = [t for t in turn.trauma_results.get("new_trauma_events", []) 
                                  if t.get("agent_id") in mission.get("agents", [])]
                    if agent_trauma:
                        events.append({
                            "type": "mission_trauma_impact",
                            "description": f"Trauma affects mission {mission.get('id', 'unknown')} participants",
                            "trauma_count": len(agent_trauma),
                            "mission_risk": "increased"
                        })
        
        return events
    
    def _identify_system_synergies(self, turn: SimulationTurn) -> List[Dict[str, Any]]:
        """Identify synergistic interactions between systems"""
        synergies = []
        
        # Calculate synergy scores between systems
        system_results = {
            "autonomy": turn.autonomy_results,
            "intelligence": turn.intelligence_results,
            "narrative": turn.narrative_results,
            "trauma": turn.trauma_results
        }
        
        # Check for high-impact combinations
        if (system_results["autonomy"] and system_results["intelligence"] and 
            len(system_results["autonomy"].get("decisions_made", [])) > 0 and
            len(system_results["intelligence"].get("actionable_intel", [])) > 0):
            
            synergies.append({
                "type": "autonomy_intelligence_synergy",
                "systems": ["autonomy", "intelligence"],
                "synergy_score": 0.8,
                "description": "Autonomous agents effectively utilize intelligence",
                "impact": "high"
            })
        
        if (system_results["narrative"] and system_results["trauma"] and
            len(system_results["narrative"].get("story_events", [])) > 0 and
            len(system_results["trauma"].get("new_trauma_events", [])) > 0):
            
            synergies.append({
                "type": "narrative_trauma_synergy",
                "systems": ["narrative", "trauma"],
                "synergy_score": 0.7,
                "description": "Trauma events drive narrative development",
                "impact": "medium"
            })
        
        return synergies
    
    def _apply_emergent_complexity(self, turn: SimulationTurn):
        """Apply emergent complexity effects from system interactions"""
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(turn)
        
        if complexity_score > self.synergy_threshold:
            # Generate emergent events
            emergent_events = self._generate_emergent_events(turn, complexity_score)
            turn.integration_events.extend(emergent_events)
            
            # Apply complexity modifiers
            self._apply_complexity_modifiers(turn, complexity_score)
    
    def _calculate_complexity_score(self, turn: SimulationTurn) -> float:
        """Calculate the complexity score for the turn"""
        
        # Base complexity from number of events
        base_complexity = 0.0
        
        base_complexity += len(turn.autonomy_results.get("decisions_made", [])) * 0.1
        base_complexity += len(turn.intelligence_results.get("new_intelligence", [])) * 0.1
        base_complexity += len(turn.narrative_results.get("story_events", [])) * 0.1
        base_complexity += len(turn.trauma_results.get("new_trauma_events", [])) * 0.1
        
        # Synergy bonus
        synergy_bonus = len(turn.system_synergies) * 0.2
        
        # Integration bonus
        integration_bonus = len(turn.integration_events) * 0.05
        
        return min(1.0, base_complexity + synergy_bonus + integration_bonus)
    
    def _generate_emergent_events(self, turn: SimulationTurn, complexity_score: float) -> List[Dict[str, Any]]:
        """Generate emergent events based on complexity"""
        emergent_events = []
        
        # High complexity can trigger unexpected events
        if complexity_score > 0.8:
            emergent_events.append({
                "type": "emergent_crisis",
                "description": "High system complexity triggers an emergent crisis",
                "complexity_level": "critical",
                "systems_affected": ["autonomy", "intelligence", "narrative", "trauma"]
            })
        
        elif complexity_score > 0.6:
            emergent_events.append({
                "type": "emergent_opportunity",
                "description": "System synergy creates unexpected opportunities",
                "complexity_level": "moderate",
                "opportunity_type": "cross_system_benefit"
            })
        
        return emergent_events
    
    def _apply_complexity_modifiers(self, turn: SimulationTurn, complexity_score: float):
        """Apply modifiers based on complexity score"""
        
        # Modify system effectiveness based on complexity
        if complexity_score > 0.7:
            # High complexity can reduce system effectiveness
            for decision in turn.autonomy_results.get("decisions_made", []):
                decision.success_probability *= 0.9  # 10% reduction
        
        elif complexity_score < 0.3:
            # Low complexity can improve system effectiveness
            for decision in turn.autonomy_results.get("decisions_made", []):
                decision.success_probability *= 1.1  # 10% improvement
    
    def _update_performance_metrics(self, turn: SimulationTurn):
        """Update system performance metrics"""
        
        # Calculate system performance
        system_performance = {}
        
        if turn.autonomy_results:
            system_performance["autonomy"] = {
                "decisions_made": len(turn.autonomy_results.get("decisions_made", [])),
                "success_rate": self._calculate_autonomy_success_rate(turn.autonomy_results),
                "efficiency": 0.7  # Placeholder
            }
        
        if turn.intelligence_results:
            system_performance["intelligence"] = {
                "events_generated": len(turn.intelligence_results.get("new_intelligence", [])),
                "patterns_detected": len(turn.intelligence_results.get("patterns_detected", [])),
                "efficiency": 0.8  # Placeholder
            }
        
        if turn.narrative_results:
            system_performance["narrative"] = {
                "story_events": len(turn.narrative_results.get("story_events", [])),
                "arcs_active": len(turn.narrative_results.get("new_arcs", [])),
                "efficiency": 0.6  # Placeholder
            }
        
        if turn.trauma_results:
            system_performance["trauma"] = {
                "trauma_events": len(turn.trauma_results.get("new_trauma_events", [])),
                "recovery_progress": len(turn.trauma_results.get("recovery_progress", [])),
                "efficiency": 0.5  # Placeholder
            }
        
        self.system_performance[f"turn_{turn.turn_number}"] = system_performance
        
        # Calculate integration metrics
        self.integration_metrics[f"turn_{turn.turn_number}"] = {
            "complexity_score": self._calculate_complexity_score(turn),
            "synergy_count": len(turn.system_synergies),
            "integration_events": len(turn.integration_events),
            "overall_efficiency": self._calculate_overall_efficiency(system_performance)
        }
    
    def _calculate_autonomy_success_rate(self, autonomy_results: Dict[str, Any]) -> float:
        """Calculate autonomy system success rate"""
        decisions = autonomy_results.get("decisions_made", [])
        if not decisions:
            return 0.0
        
        successful = sum(1 for d in decisions if getattr(d, 'success_probability', 0) > 0.5)
        return successful / len(decisions)
    
    def _calculate_overall_efficiency(self, system_performance: Dict[str, Dict[str, Any]]) -> float:
        """Calculate overall system efficiency"""
        if not system_performance:
            return 0.0
        
        efficiencies = [perf.get("efficiency", 0.0) for perf in system_performance.values()]
        return sum(efficiencies) / len(efficiencies)
    
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get comprehensive integration system summary"""
        
        if not self.turn_history:
            return {"status": "no_turns_processed"}
        
        latest_turn = self.turn_history[-1]
        
        return {
            "total_turns_processed": len(self.turn_history),
            "latest_turn": latest_turn.turn_number,
            "system_performance": self.system_performance.get(f"turn_{latest_turn.turn_number}", {}),
            "integration_metrics": self.integration_metrics.get(f"turn_{latest_turn.turn_number}", {}),
            "system_synergies": len(latest_turn.system_synergies),
            "integration_events": len(latest_turn.integration_events),
            "overall_complexity": self._calculate_complexity_score(latest_turn),
            "system_status": {
                "autonomy": self.autonomy_system is not None,
                "mission": self.mission_system is not None,
                "intelligence": self.intelligence_system is not None,
                "narrative": self.narrative_system is not None,
                "trauma": self.trauma_system is not None
            }
        }
    
    def run_enhanced_simulation(self, turns: int = 10) -> List[SimulationTurn]:
        """Run the enhanced simulation for a specified number of turns"""
        
        logger.info(f"Starting enhanced simulation for {turns} turns")
        
        simulation_results = []
        
        for turn_num in range(turns):
            logger.info(f"Processing turn {turn_num + 1}/{turns}")
            
            # Update game state turn number
            setattr(self.game_state, 'turn_number', turn_num + 1)
            
            # Process enhanced turn
            turn = self.process_enhanced_turn()
            simulation_results.append(turn)
            
            # Log turn summary
            logger.info(f"Turn {turn_num + 1} completed: "
                       f"{len(turn.autonomy_results.get('decisions_made', []))} autonomy decisions, "
                       f"{len(turn.intelligence_results.get('new_intelligence', []))} intelligence events, "
                       f"{len(turn.narrative_results.get('story_events', []))} narrative events, "
                       f"{len(turn.trauma_results.get('new_trauma_events', []))} trauma events, "
                       f"{len(turn.integration_events)} integration events")
        
        logger.info(f"Enhanced simulation completed. Processed {turns} turns.")
        
        return simulation_results 