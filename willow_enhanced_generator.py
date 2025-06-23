#!/usr/bin/env python3
"""
Enhanced Willow Dataset Generator
Specifically optimized for trauma-informed tenant support scenarios
"""

import json
import random
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import re

@dataclass
class TraumaMarkers:
    """Tracks trauma indicators in tenant communication."""
    dissociation_phrases: List[str]
    panic_indicators: List[str] 
    shutdown_signals: List[str]
    anger_escalation: List[str]
    desperation_markers: List[str]

@dataclass
class CulturalContext:
    """Cultural and linguistic context tracking."""
    primary_language: str
    cultural_background: Optional[str]
    communication_style: str  # direct, indirect, formal, etc.
    trust_indicators: List[str]
    barrier_types: List[str]

class WillowEnhancedGenerator:
    """Enhanced generator with Willow-specific optimizations."""
    
    # Trauma-informed phrase detection
    TRAUMA_INDICATORS = {
        "dissociation": [
            "can't think", "brain fog", "not real", "watching myself",
            "numb", "floating", "disconnected", "can't feel"
        ],
        "panic": [
            "can't breathe", "heart racing", "going to die", "emergency",
            "right now", "can't wait", "please help", "desperate"
        ],
        "shutdown": [
            "whatever", "doesn't matter", "too tired", "give up",
            "can't anymore", "done trying", "no point", "why bother"
        ],
        "anger": [
            "sick of this", "had enough", "sue", "lawyer", 
            "rights", "illegal", "discrimination", "unfair"
        ],
        "desperation": [
            "last chance", "nowhere to go", "end of rope", "please",
            "begging", "anything", "whatever it takes", "no options"
        ]
    }
    
    # Enhanced tier 1 techniques for specific trauma responses
    TRAUMA_RESPONSIVE_TECHNIQUES = {
        "dissociation_grounding": [
            "sensory_anchor_offering", "present_moment_acknowledgment",
            "body_awareness_gentle", "timeline_orientation"
        ],
        "panic_containment": [
            "breath_space_creation", "immediate_safety_affirmation",
            "nervous_system_recognition", "co_regulation_presence"
        ],
        "shutdown_warming": [
            "micro_engagement", "energy_conservation_honoring",
            "minimal_demand_presence", "witness_without_pushing"
        ],
        "anger_channeling": [
            "righteous_anger_validation", "injustice_naming",
            "power_acknowledgment", "resistance_honoring"
        ],
        "desperation_holding": [
            "crisis_container_building", "hope_fragment_finding",
            "survival_strength_mirroring", "possibility_gentle_seeding"
        ]
    }
    
    # Culturally responsive elements
    CULTURAL_ADAPTATIONS = {
        "communication_styles": {
            "high_context": {
                "indirection_level": "high",
                "metaphor_use": "frequent",
                "silence_comfort": "high"
            },
            "low_context": {
                "indirection_level": "low",
                "metaphor_use": "minimal",
                "silence_comfort": "low"
            },
            "formal_hierarchical": {
                "respect_markers": "high",
                "title_use": "consistent",
                "distance_maintenance": "yes"
            }
        },
        "trust_building_patterns": {
            "collective_culture": ["family_consideration", "community_impact", "group_harmony"],
            "individual_culture": ["personal_autonomy", "individual_rights", "self_determination"],
            "trauma_informed": ["consistency_proof", "small_steps", "control_returning"]
        }
    }
    
    # Realistic conversation flow patterns
    CONVERSATION_PATTERNS = {
        "crisis_escalation": {
            "flow": ["problem_statement", "barrier_reveal", "desperation_peak", "exhaustion"],
            "arousal_pattern": [7.5, 8.2, 9.0, 7.8],
            "capacity_pattern": [4.0, 3.5, 3.0, 3.2]
        },
        "trust_building": {
            "flow": ["cautious_opening", "test_response", "gradual_reveal", "collaboration"],
            "arousal_pattern": [7.0, 6.8, 6.5, 6.2],
            "capacity_pattern": [3.8, 4.0, 4.3, 4.5]
        },
        "shutdown_recovery": {
            "flow": ["minimal_engagement", "micro_response", "small_opening", "gentle_expansion"],
            "arousal_pattern": [5.5, 5.8, 6.2, 6.5],
            "capacity_pattern": [2.8, 3.0, 3.3, 3.6]
        }
    }
    
    # Willow-specific response components
    RESPONSE_COMPONENTS = {
        "validation": {
            "emotional": "Your {emotion} makes complete sense given {context}",
            "systemic": "The system has failed you by {specific_failure}",
            "historical": "{Time_period} of {struggle} would exhaust anyone",
            "somatic": "Your body is telling the truth about {experience}"
        },
        "containment": {
            "immediate": "Right now, in this moment, you're {safety_affirmation}",
            "boundary": "We'll take this {pace_description}",
            "capacity": "You've been carrying {burden} with {limited_resource}",
            "rhythm": "Let's {action} while honoring {need}"
        },
        "resources": {
            "emergency": "For immediate {need}: {specific_resource} at {contact}",
            "rights": "You have the right to {specific_right} under {law/policy}",
            "community": "{Local_org} specializes in {specific_situation}",
            "timeline": "This typically takes {realistic_timeframe} but {variables}"
        }
    }
    
    def __init__(self, starting_id: int = 1344):
        self.current_id = starting_id
        self.entries = []
        self.conversation_memory = {}  # Track conversation patterns
        
    def detect_trauma_state(self, message: str) -> Dict[str, float]:
        """Detect trauma indicators in tenant message."""
        message_lower = message.lower()
        scores = {}
        
        for trauma_type, indicators in self.TRAUMA_INDICATORS.items():
            count = sum(1 for indicator in indicators if indicator in message_lower)
            scores[trauma_type] = min(count / len(indicators), 1.0)
            
        return scores
    
    def select_trauma_responsive_technique(self, trauma_scores: Dict[str, float]) -> str:
        """Select appropriate technique based on trauma state."""
        # Find dominant trauma state
        if not trauma_scores:
            return "general_validation"
            
        dominant = max(trauma_scores.items(), key=lambda x: x[1])
        trauma_type, score = dominant
        
        if score < 0.2:
            return "general_validation"
            
        # Map to specific technique category
        technique_map = {
            "dissociation": "dissociation_grounding",
            "panic": "panic_containment",
            "shutdown": "shutdown_warming",
            "anger": "anger_channeling",
            "desperation": "desperation_holding"
        }
        
        category = technique_map.get(trauma_type, "general_validation")
        techniques = self.TRAUMA_RESPONSIVE_TECHNIQUES.get(category, ["general_validation"])
        
        return random.choice(techniques)
    
    def generate_culturally_responsive_response(
        self,
        base_response: str,
        cultural_context: Optional[CulturalContext] = None
    ) -> str:
        """Adapt response for cultural context."""
        if not cultural_context:
            return base_response
            
        # Add cultural adaptations
        if cultural_context.communication_style == "high_context":
            # Add more metaphor and indirection
            base_response = self._add_metaphorical_language(base_response)
        elif cultural_context.communication_style == "formal_hierarchical":
            # Add respect markers
            base_response = self._add_formal_markers(base_response)
            
        # Add language switching recognition if applicable
        if cultural_context.primary_language != "English":
            base_response += f" If it's easier to communicate in {cultural_context.primary_language}, that's completely okay."
            
        return base_response
    
    def _add_metaphorical_language(self, response: str) -> str:
        """Add culturally appropriate metaphors."""
        metaphors = [
            "Like a tree bending in the storm, you've shown incredible flexibility",
            "This burden is like carrying water in broken vessels",
            "Your strength is like a river that finds its way around obstacles"
        ]
        # Add metaphor at appropriate point
        sentences = response.split('. ')
        if len(sentences) > 1:
            sentences.insert(1, random.choice(metaphors))
        return '. '.join(sentences)
    
    def _add_formal_markers(self, response: str) -> str:
        """Add formal respect markers."""
        # This is simplified - in practice would be more sophisticated
        response = response.replace("you", "you", 1)  # Could replace with formal "you" in other languages
        return response
    
    def calculate_realistic_progression(
        self,
        initial_arousal: float,
        initial_capacity: float,
        conversation_pattern: str = "crisis_escalation"
    ) -> Tuple[List[float], List[float]]:
        """Calculate realistic arousal/capacity progression."""
        pattern = self.CONVERSATION_PATTERNS.get(conversation_pattern, self.CONVERSATION_PATTERNS["crisis_escalation"])
        
        # Adjust pattern to initial values
        arousal_pattern = pattern["arousal_pattern"]
        capacity_pattern = pattern["capacity_pattern"]
        
        # Scale to match initial values
        arousal_adjusted = [initial_arousal + (p - arousal_pattern[0]) for p in arousal_pattern]
        capacity_adjusted = [initial_capacity + (p - capacity_pattern[0]) for p in capacity_pattern]
        
        # Add realistic variation
        arousal_final = [round(a + random.uniform(-0.2, 0.2), 1) for a in arousal_adjusted]
        capacity_final = [round(c + random.uniform(-0.1, 0.1), 1) for c in capacity_adjusted]
        
        return arousal_final, capacity_final
    
    def generate_enhanced_entry(
        self,
        scenario_name: str,
        category: str,
        complexity: str,
        tenant_messages: List[str],
        conversation_pattern: str = "crisis_escalation",
        cultural_context: Optional[CulturalContext] = None,
        initial_arousal: float = 7.5,
        initial_capacity: float = 3.8,
        additional_context: Optional[Dict] = None
    ) -> Dict:
        """Generate entry with enhanced Willow-specific features."""
        
        # Detect trauma states in messages
        trauma_states = [self.detect_trauma_state(msg) for msg in tenant_messages]
        
        # Calculate realistic progression
        arousal_curve, capacity_curve = self.calculate_realistic_progression(
            initial_arousal, initial_capacity, conversation_pattern
        )
        
        # Generate appropriate techniques
        techniques = [self.select_trauma_responsive_technique(state) for state in trauma_states]
        
        # Build conversation with 4 messages (2 tenant, 2 Willow)
        messages = []
        for i in range(2):
            # Tenant message
            messages.append({
                "role": "tenant",
                "content": tenant_messages[i] if i < len(tenant_messages) else tenant_messages[-1],
                "arousal": arousal_curve[i*2],
                "capacity": capacity_curve[i*2],
                "trauma_markers": trauma_states[i] if i < len(trauma_states) else {}
            })
            
            # Generate Willow response
            tier = "tier_1" if i == 0 else "tier_2"
            technique = techniques[i] if i < len(techniques) else techniques[-1]
            
            # This is where you'd generate the actual response content
            # For now, using placeholder
            willow_content = f"[Generated {tier} response using {technique}]"
            
            if cultural_context:
                willow_content = self.generate_culturally_responsive_response(
                    willow_content, cultural_context
                )
            
            messages.append({
                "role": "willow",
                "content": willow_content,
                "tier": tier,
                "technique": technique,
                "arousal_impact": arousal_curve[i*2+1] - arousal_curve[i*2],
                "symbolic_language": "traditional" if i == 0 else "minimal"
            })
        
        # Build entry
        entry = {
            "id": f"WILLOW_{self.current_id}",
            "scenario": scenario_name,
            "category": category,
            "complexity_level": complexity,
            "initial_state": {
                "arousal": initial_arousal,
                "capacity": initial_capacity,
                "trauma_indicators": trauma_states[0],
                "conversation_pattern": conversation_pattern
            },
            "messages": messages,
            "process_metrics": {
                "tier_progression": ["tier_1", "tier_2"],
                "arousal_curve": arousal_curve,
                "capacity_curve": capacity_curve,
                "trauma_responsive_techniques": techniques,
                "conversation_pattern": conversation_pattern,
                "cultural_adaptations": cultural_context.__dict__ if cultural_context else None,
                "containment_quality": self._assess_containment_quality(arousal_curve),
                "therapeutic_alliance": self._assess_alliance_building(capacity_curve),
                "crisis_stabilization": arousal_curve[-1] < arousal_curve[0]
            }
        }
        
        if additional_context:
            entry["additional_context"] = additional_context
            
        self.current_id += 1
        return entry
    
    def _assess_containment_quality(self, arousal_curve: List[float]) -> str:
        """Assess quality of emotional containment."""
        start, end = arousal_curve[0], arousal_curve[-1]
        peak = max(arousal_curve)
        
        if end < start - 1.5:
            return "excellent"
        elif end < start - 0.5:
            return "good"
        elif end <= start:
            return "adequate"
        else:
            return "needs_support"
    
    def _assess_alliance_building(self, capacity_curve: List[float]) -> str:
        """Assess therapeutic alliance building."""
        start, end = capacity_curve[0], capacity_curve[-1]
        
        if end > start + 1.0:
            return "strong"
        elif end > start + 0.5:
            return "developing"
        elif end >= start:
            return "maintained"
        else:
            return "fragile"
    
    def generate_batch_with_theme(
        self,
        theme: str,
        count: int,
        base_scenarios: List[Tuple[str, List[str]]],
        pattern_distribution: Optional[Dict[str, float]] = None
    ) -> List[Dict]:
        """Generate themed batch with specific conversation patterns."""
        
        if not pattern_distribution:
            pattern_distribution = {
                "crisis_escalation": 0.4,
                "trust_building": 0.4,
                "shutdown_recovery": 0.2
            }
        
        batch = []
        patterns = list(pattern_distribution.keys())
        weights = list(pattern_distribution.values())
        
        for i in range(count):
            # Select scenario and pattern
            scenario_name, tenant_messages = base_scenarios[i % len(base_scenarios)]
            pattern = random.choices(patterns, weights=weights)[0]
            
            # Add theme to scenario name
            themed_name = f"{theme}_{scenario_name}"
            
            # Generate entry
            entry = self.generate_enhanced_entry(
                scenario_name=themed_name,
                category=self._infer_category(theme),
                complexity="high",
                tenant_messages=tenant_messages,
                conversation_pattern=pattern,
                initial_arousal=random.uniform(7.0, 8.5),
                initial_capacity=random.uniform(3.2, 4.2)
            )
            
            batch.append(entry)
            
        return batch
    
    def _infer_category(self, theme: str) -> str:
        """Infer category from theme."""
        category_map = {
            "eviction": "eviction",
            "discrimination": "discrimination", 
            "maintenance": "maintenance_crisis",
            "medical": "health_safety",
            "family": "intersectional_vulnerability",
            "financial": "financial_distress"
        }
        
        for key, category in category_map.items():
            if key in theme.lower():
                return category
                
        return "complex_grievance"
    
    def export_training_ready(self, entries: List[Dict], filename: str):
        """Export in training-ready format with metadata."""
        
        # Add metadata
        metadata = {
            "dataset_version": "2.0",
            "generation_date": datetime.now().isoformat(),
            "total_entries": len(entries),
            "entry_id_range": f"WILLOW_{entries[0]['id'].split('_')[1]}-{entries[-1]['id'].split('_')[1]}",
            "features": {
                "trauma_detection": True,
                "cultural_adaptation": True,
                "conversation_patterns": True,
                "realistic_progression": True
            },
            "quality_metrics": self._calculate_dataset_metrics(entries)
        }
        
        # Write metadata
        with open(filename.replace('.jsonl', '_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Write entries
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def _calculate_dataset_metrics(self, entries: List[Dict]) -> Dict:
        """Calculate quality metrics for dataset."""
        metrics = {
            "avg_containment_quality": {},
            "conversation_patterns": {},
            "trauma_responsive_coverage": set(),
            "cultural_adaptations": 0
        }
        
        for entry in entries:
            pm = entry.get("process_metrics", {})
            
            # Containment quality
            quality = pm.get("containment_quality", "unknown")
            metrics["avg_containment_quality"][quality] = metrics["avg_containment_quality"].get(quality, 0) + 1
            
            # Patterns
            pattern = pm.get("conversation_pattern", "unknown")
            metrics["conversation_patterns"][pattern] = metrics["conversation_patterns"].get(pattern, 0) + 1
            
            # Techniques
            techniques = pm.get("trauma_responsive_techniques", [])
            metrics["trauma_responsive_coverage"].update(techniques)
            
            # Cultural
            if pm.get("cultural_adaptations"):
                metrics["cultural_adaptations"] += 1
                
        # Convert set to list for JSON serialization
        metrics["trauma_responsive_coverage"] = list(metrics["trauma_responsive_coverage"])
        
        return metrics

def main():
    """Example usage of enhanced generator."""
    generator = WillowEnhancedGenerator(starting_id=1344)
    
    # Example with cultural context
    cultural_context = CulturalContext(
        primary_language="Spanish",
        cultural_background="Latin American",
        communication_style="high_context",
        trust_indicators=["family_mentioned", "respectful_distance"],
        barrier_types=["language", "documentation_fear"]
    )
    
    # Generate single entry
    entry = generator.generate_enhanced_entry(
        scenario_name="undocumented_repair_fear",
        category="maintenance_crisis",
        complexity="high",
        tenant_messages=[
            "Bathroom flooding but scared to call. No papers, they find out they call ICE",
            "Water everywhere, kids crying, but what if they report us?"
        ],
        conversation_pattern="trust_building",
        cultural_context=cultural_context,
        initial_arousal=8.2,
        initial_capacity=3.4
    )
    
    print(f"Generated entry {entry['id']} with trauma-responsive techniques: {entry['process_metrics']['trauma_responsive_techniques']}")

if __name__ == "__main__":
    main()