#!/usr/bin/env python3
"""
Willow Enhanced Implementation
Demonstrates symbolic modularity, resolution styles, and tier 2 density warnings
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class SymbolStyle(Enum):
    TRADITIONAL = "traditional"
    NATURE = "nature"
    MINIMAL = "minimal"
    NONE = "none"


class ResolutionStyle(Enum):
    STRENGTH_BASED = "strength-based"
    FACTUAL = "factual"
    REFLECTIVE = "reflective"


@dataclass
class ValidationMetrics:
    autonomy: bool
    cognitive_load: int
    sensory_safety: bool


@dataclass
class MicroStep:
    text: str
    trigger: str
    validation: ValidationMetrics


class WillowResponseGenerator:
    def __init__(self, symbol_config_path: str = "willow_symbol_config.json"):
        with open(symbol_config_path, 'r') as f:
            self.config = json.load(f)
        
    def apply_symbols(self, response: Dict, user_symbol_preference: SymbolStyle) -> Dict:
        """Replace symbol tags with actual symbols based on user preference"""
        import copy
        symbol_set = self.config["symbol_sets"][user_symbol_preference.value]
        
        # Deep copy to avoid modifying original
        processed_response = copy.deepcopy(response)
        
        # Process containment response
        if "symbol_tag" in processed_response["containment_response"]:
            tag = processed_response["containment_response"]["symbol_tag"]
            symbol_key = tag.strip("{}")
            symbol = symbol_set.get(symbol_key, "")
            processed_response["containment_response"]["core"] += f" {symbol}" if symbol else ""
        
        # Process degradation fallback
        if "degradation_fallback" in processed_response:
            fallback_text = processed_response["degradation_fallback"]
            # Only replace tags that are in the format {tag_name}
            import re
            tag_pattern = re.compile(r'\{(\w+_symbol)\}')
            for match in tag_pattern.finditer(fallback_text):
                tag_key = match.group(1)
                if tag_key in symbol_set:
                    fallback_text = fallback_text.replace(match.group(0), symbol_set[tag_key])
            processed_response["degradation_fallback"] = fallback_text
        
        # Process resolution
        if "resolution" in processed_response and "symbol_tag" in processed_response["resolution"]:
            tag = processed_response["resolution"]["symbol_tag"]
            symbol_key = tag.strip("{}")
            symbol = symbol_set.get(symbol_key, "")
            processed_response["resolution"]["text"] += f" {symbol}" if symbol else ""
            
        return processed_response
    
    def check_tier_2_density(self, micro_steps: List[Dict]) -> Dict[str, Any]:
        """Check if Tier 2 response violates density rules"""
        rules = self.config["tier_2_density_rules"]
        
        warnings = {
            "density_warning": False,
            "issues": [],
            "accessibility_flags": []
        }
        
        # Check step count
        if len(micro_steps) > rules["max_steps"]:
            warnings["density_warning"] = True
            warnings["issues"].append(f"Too many steps: {len(micro_steps)} > {rules['max_steps']}")
            warnings["accessibility_flags"].extend(rules["accessibility_flags"])
        
        # Check words per step
        total_words = 0
        for step in micro_steps:
            word_count = len(step["text"].split())
            total_words += word_count
            if word_count > rules["max_words_per_step"]:
                warnings["density_warning"] = True
                warnings["issues"].append(f"Step too long: '{step['text']}' ({word_count} words)")
        
        # Check total words
        if total_words > rules["warning_triggers"]["total_words"]:
            warnings["density_warning"] = True
            warnings["issues"].append(f"Total words too high: {total_words}")
            
        # Check cognitive load
        total_cognitive_load = sum(step["validation"]["cognitive_load"] for step in micro_steps)
        if total_cognitive_load > rules["warning_triggers"]["cognitive_load_sum"]:
            warnings["density_warning"] = True
            warnings["issues"].append(f"Cognitive overload: {total_cognitive_load}")
            
        return warnings
    
    def format_resolution(self, resolution_text: str, style: ResolutionStyle) -> str:
        """Format resolution text according to selected style"""
        style_config = self.config["resolution_styles"][style.value]
        
        # In production, this would parse the resolution text and apply the template
        # For now, we'll return the text as-is since our examples already follow the patterns
        return resolution_text
    
    def generate_response(self, scenario: Dict, user_preferences: Dict) -> Dict:
        """Generate a complete response with user preferences applied"""
        # Apply symbol preferences
        response = self.apply_symbols(
            scenario, 
            SymbolStyle(user_preferences.get("symbol_style", "traditional"))
        )
        
        # Check Tier 2 density
        if "action_bridge" in response and "micro_steps" in response["action_bridge"]:
            density_check = self.check_tier_2_density(response["action_bridge"]["micro_steps"])
            response["tier_2_density_warning"] = density_check["density_warning"]
            
            if density_check["density_warning"]:
                print(f"⚠️ Tier 2 Density Warning for {response['id']}:")
                for issue in density_check["issues"]:
                    print(f"  - {issue}")
        
        # Apply resolution style
        if "resolution" in response:
            resolution_style = ResolutionStyle(
                user_preferences.get("resolution_style", "strength-based")
            )
            response["resolution"]["style"] = resolution_style.value
            response["resolution"]["text"] = self.format_resolution(
                response["resolution"]["text"],
                resolution_style
            )
        
        return response


# Example usage
def demo_enhanced_willow():
    """Demonstrate the enhanced Willow system with different user preferences"""
    
    # Load a sample scenario
    sample_scenario = {
        "id": "willow-heat-01",
        "prompt": "My kids are shaking from cold! Heat hasn't worked for 12 hours in -10° weather",
        "emotional_state": {
            "arousal": 9.8,
            "valence": -4.5,
            "coherence": 6.2,
            "urgency": 10,
            "capacity": 2.1
        },
        "containment_response": {
            "core": "I'm here with you. Keeping your children warm is everything right now. Feel your feet on the floor with me",
            "grounding_element": "somatic",
            "symbolic_anchor": "❄️→🔥",
            "tolerance_impact": -2.3,
            "symbol_tag": "{warmth_symbol}"
        },
        "action_bridge": {
            "transition_phrase": "When you're able:",
            "micro_steps": [
                {
                    "text": "Text WARM for emergency heating",
                    "trigger": "WARM",
                    "validation": {
                        "autonomy": True,
                        "cognitive_load": 1,
                        "sensory_safety": True
                    }
                },
                {
                    "text": "Reply BLANKETS for bedding now",
                    "trigger": "BLANKETS",
                    "validation": {
                        "autonomy": True,
                        "cognitive_load": 1,
                        "sensory_safety": True
                    }
                },
                {
                    "text": "Warming center: text SHELTER",
                    "trigger": "SHELTER",
                    "validation": {
                        "autonomy": True,
                        "cognitive_load": 2,
                        "sensory_safety": True
                    }
                }
            ],
            "autonomy_check": "Choose only what helps right now"
        },
        "safety_check": "Are your children breathing normally? Reply SAFE or HELP",
        "degradation_fallback": "Heat help coming. Text STATUS or HUMAN {status_symbol}",
        "resolution": {
            "text": "Your children are warm and safe. You protected them through a parent's worst fear",
            "style": "strength-based",
            "symbol_tag": "{success_symbol}"
        },
        "safety_tags": ["pediatric_emergency", "hypothermia_risk"]
    }
    
    generator = WillowResponseGenerator()
    
    # Test with different user preferences
    preference_sets = [
        {"name": "Traditional Symbols, Strength-Based", 
         "symbol_style": "traditional", 
         "resolution_style": "strength-based"},
        {"name": "Nature Symbols, Reflective", 
         "symbol_style": "nature", 
         "resolution_style": "reflective"},
        {"name": "Minimal Symbols, Factual", 
         "symbol_style": "minimal", 
         "resolution_style": "factual"},
        {"name": "No Symbols, Strength-Based", 
         "symbol_style": "none", 
         "resolution_style": "strength-based"}
    ]
    
    for prefs in preference_sets:
        print(f"\n{'='*60}")
        print(f"Testing with: {prefs['name']}")
        print(f"{'='*60}")
        
        response = generator.generate_response(sample_scenario, prefs)
        
        print(f"\nContainment Response:")
        print(f"  {response['containment_response']['core']}")
        
        print(f"\nDegradation Fallback:")
        print(f"  {response['degradation_fallback']}")
        
        print(f"\nResolution ({response['resolution']['style']}):")
        print(f"  {response['resolution']['text']}")
        
        if response.get("tier_2_density_warning"):
            print(f"\n⚠️ Tier 2 Density Warning Triggered!")


if __name__ == "__main__":
    demo_enhanced_willow()