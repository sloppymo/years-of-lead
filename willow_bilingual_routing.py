#!/usr/bin/env python3
"""
Willow Bilingual Crisis Routing
Detects language switching + high arousal for human escalation
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re
from collections import Counter


@dataclass
class LanguageProfile:
    """Tracks language usage patterns for a user"""
    user_id: str
    primary_language: str = "en"
    detected_languages: Set[str] = field(default_factory=set)
    language_history: List[Dict] = field(default_factory=list)
    code_switch_events: List[Dict] = field(default_factory=list)
    stress_induced_switches: int = 0


class BilingualCrisisDetector:
    """Detects language switching patterns that indicate crisis escalation"""
    
    LANGUAGE_MARKERS = {
        "es": {  # Spanish
            "common_words": ["que", "de", "la", "el", "es", "en", "y", "no", "por", "para"],
            "crisis_words": ["ayuda", "dolor", "miedo", "no puedo", "socorro"],
            "family_terms": ["mi hijo", "mi madre", "mis niños", "mi familia"]
        },
        "zh": {  # Chinese (simplified markers)
            "common_words": ["的", "是", "了", "我", "你", "在", "有", "不", "这", "个"],
            "crisis_words": ["帮助", "救命", "痛", "怕", "不行"],
            "family_terms": ["孩子", "妈妈", "家人"]
        },
        "ar": {  # Arabic
            "common_words": ["في", "من", "على", "إلى", "هذا", "أن", "لا", "ما", "هو", "أنا"],
            "crisis_words": ["ساعدني", "خائف", "ألم", "لا أستطيع"],
            "family_terms": ["طفلي", "أمي", "عائلتي"]
        },
        "tl": {  # Tagalog
            "common_words": ["ang", "ng", "sa", "na", "ay", "at", "hindi", "ko", "siya", "ito"],
            "crisis_words": ["tulong", "takot", "sakit", "hindi ko kaya"],
            "family_terms": ["anak ko", "nanay", "pamilya"]
        }
    }
    
    CRISIS_INDICATORS = {
        "rapid_switch": {"threshold": 2, "window": 60},  # 2 switches in 1 minute
        "mixed_message": {"threshold": 0.3},  # 30% non-English words
        "stress_markers": ["help", "please", "emergency", "now", "urgent"],
        "high_arousal_switch": {"arousal": 8.0}
    }
    
    def __init__(self):
        self.user_profiles: Dict[str, LanguageProfile] = {}
        
    def analyze_message(self, user_id: str, message: str, emotional_state: Dict) -> Dict:
        """Analyze message for language switching and crisis indicators"""
        
        # Get or create profile
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = LanguageProfile(user_id=user_id)
        
        profile = self.user_profiles[user_id]
        
        # Detect languages in message
        detected_langs = self._detect_languages(message)
        primary_lang = self._determine_primary_language(detected_langs)
        
        # Check for code switching
        is_code_switch = self._detect_code_switch(profile, primary_lang, detected_langs)
        
        # Check for crisis language switching
        crisis_switch = self._detect_crisis_switch(
            profile, message, detected_langs, emotional_state
        )
        
        # Update profile
        profile.language_history.append({
            "timestamp": datetime.now(),
            "primary_language": primary_lang,
            "all_languages": list(detected_langs.keys()),
            "arousal": emotional_state.get("arousal", 5),
            "is_switch": is_code_switch,
            "is_crisis": crisis_switch["is_crisis"]
        })
        
        if is_code_switch:
            profile.code_switch_events.append({
                "timestamp": datetime.now(),
                "from_lang": profile.primary_language,
                "to_lang": primary_lang,
                "arousal": emotional_state.get("arousal", 5)
            })
            
        # Update primary language if stable
        if len([h for h in profile.language_history[-5:] if h["primary_language"] == primary_lang]) >= 3:
            profile.primary_language = primary_lang
            
        return {
            "primary_language": primary_lang,
            "detected_languages": list(detected_langs.keys()),
            "is_code_switch": is_code_switch,
            "crisis_indicators": crisis_switch,
            "routing_recommendation": self._determine_routing(profile, crisis_switch, emotional_state)
        }
    
    def _detect_languages(self, message: str) -> Dict[str, float]:
        """Detect languages present in the message"""
        message_lower = message.lower()
        words = re.findall(r'\b\w+\b', message_lower)
        
        if not words:
            return {"en": 1.0}
            
        language_scores: Dict[str, float] = {"en": 0.0}
        
        # Check each language
        for lang, markers in self.LANGUAGE_MARKERS.items():
            score = 0
            for word in words:
                if word in markers["common_words"]:
                    score += 1
                if word in markers["crisis_words"]:
                    score += 2  # Crisis words count more
                    
            if score > 0:
                language_scores[lang] = float(score) / len(words)
        
        # Calculate English score (inverse of others)
        non_english_score = sum(language_scores.values()) - language_scores.get("en", 0)
        language_scores["en"] = max(0, 1 - non_english_score)
        
        # Normalize and filter
        total = sum(language_scores.values())
        if total > 0:
            language_scores = {k: float(v/total) for k, v in language_scores.items() if v > 0.1}
        
        # Ensure return type consistency
        return_scores: Dict[str, float] = {}
        for k, v in language_scores.items():
            return_scores[k] = float(v)
            
        return return_scores
    
    def _determine_primary_language(self, language_scores: Dict[str, float]) -> str:
        """Determine the primary language of the message"""
        if not language_scores:
            return "en"
        return max(language_scores.items(), key=lambda x: x[1])[0]
    
    def _detect_code_switch(self, profile: LanguageProfile, current_primary: str, 
                           detected_langs: Dict[str, float]) -> bool:
        """Detect if code switching occurred"""
        
        # First message - no switch possible
        if not profile.language_history:
            return False
            
        # Check if primary language changed
        last_primary = profile.language_history[-1]["primary_language"]
        if current_primary != last_primary and current_primary != "en":
            return True
            
        # Check if message is heavily mixed
        if len(detected_langs) > 1:
            max_score = max(detected_langs.values())
            if max_score < 0.7:  # No dominant language
                return True
                
        return False
    
    def _detect_crisis_switch(self, profile: LanguageProfile, message: str, 
                             detected_langs: Dict[str, float], emotional_state: Dict) -> Dict:
        """Detect crisis-related language switching"""
        
        indicators = {
            "is_crisis": False,
            "severity": 0.0,
            "reasons": []
        }
        
        arousal = emotional_state.get("arousal", 5)
        
        # High arousal + language switch
        if arousal >= self.CRISIS_INDICATORS["high_arousal_switch"]["arousal"]:
            if self._detect_code_switch(profile, self._determine_primary_language(detected_langs), detected_langs):
                indicators["is_crisis"] = True
                indicators["severity"] += 0.4
                indicators["reasons"].append("high_arousal_switch")
                
        # Rapid switching pattern
        recent_switches = [e for e in profile.code_switch_events 
                          if (datetime.now() - e["timestamp"]).seconds < self.CRISIS_INDICATORS["rapid_switch"]["window"]]
        if len(recent_switches) >= self.CRISIS_INDICATORS["rapid_switch"]["threshold"]:
            indicators["is_crisis"] = True
            indicators["severity"] += 0.3
            indicators["reasons"].append("rapid_switching")
            
        # Mixed language in single message under stress
        if len(detected_langs) > 1 and arousal > 7:
            non_english_ratio = sum(v for k, v in detected_langs.items() if k != "en")
            if non_english_ratio > self.CRISIS_INDICATORS["mixed_message"]["threshold"]:
                indicators["is_crisis"] = True
                indicators["severity"] += 0.3
                indicators["reasons"].append("stressed_mixing")
                
        # Crisis words in non-English
        message_lower = message.lower()
        for lang, markers in self.LANGUAGE_MARKERS.items():
            if lang in detected_langs:
                if any(crisis_word in message_lower for crisis_word in markers["crisis_words"]):
                    indicators["is_crisis"] = True
                    indicators["severity"] += 0.5
                    indicators["reasons"].append(f"crisis_words_{lang}")
                    
        # English stress markers with non-English content
        if any(marker in message_lower for marker in self.CRISIS_INDICATORS["stress_markers"]):
            if any(lang != "en" for lang in detected_langs):
                indicators["is_crisis"] = True
                indicators["severity"] += 0.2
                indicators["reasons"].append("bilingual_stress")
                
        indicators["severity"] = min(1.0, indicators["severity"])
        return indicators
    
    def _determine_routing(self, profile: LanguageProfile, crisis_indicators: Dict, 
                          emotional_state: Dict) -> Dict:
        """Determine routing recommendation"""
        
        recommendation = {
            "route_to_human": False,
            "urgency": "normal",
            "specialist_needed": None,
            "reason": ""
        }
        
        # Crisis language switching detected
        if crisis_indicators["is_crisis"] and crisis_indicators["severity"] > 0.5:
            recommendation["route_to_human"] = True
            recommendation["urgency"] = "high"
            recommendation["reason"] = "crisis_language_switching"
            
            # Determine specialist type
            if profile.primary_language != "en":
                recommendation["specialist_needed"] = f"bilingual_{profile.primary_language}"
            else:
                # Recent non-English usage
                recent_langs = [h["primary_language"] for h in profile.language_history[-5:]]
                non_english = [l for l in recent_langs if l != "en"]
                if non_english:
                    most_common = Counter(non_english).most_common(1)[0][0]
                    recommendation["specialist_needed"] = f"bilingual_{most_common}"
                    
        # High sustained arousal with any non-English
        elif emotional_state.get("arousal", 5) > 8 and profile.detected_languages != {"en"}:
            recommendation["route_to_human"] = True
            recommendation["urgency"] = "medium"
            recommendation["reason"] = "sustained_bilingual_distress"
            
        # Repeated switching pattern
        elif len(profile.code_switch_events) > 5:
            recommendation["route_to_human"] = True
            recommendation["urgency"] = "medium"
            recommendation["reason"] = "complex_language_pattern"
            
        return recommendation


class BilingualResponseRouter:
    """Routes responses based on language analysis"""
    
    def __init__(self, crisis_detector: BilingualCrisisDetector):
        self.detector = crisis_detector
        self.routing_templates = {
            "es": "Estoy conectándote con alguien que habla español. Un momento por favor. 🌍",
            "zh": "正在为您连接中文客服，请稍等。🌍",
            "ar": "سأوصلك بشخص يتحدث العربية. لحظة من فضلك. 🌍",
            "tl": "Iko-connect kita sa taong nagsasalita ng Tagalog. Sandali lang. 🌍",
            "default": "I'm connecting you with someone who can help in your preferred language. One moment. 🌍"
        }
        
    def process_interaction(self, user_id: str, message: str, 
                           emotional_state: Dict, base_response: str) -> Dict:
        """Process interaction and determine routing"""
        
        # Analyze language patterns
        analysis = self.detector.analyze_message(user_id, message, emotional_state)
        
        # Check if human routing needed
        routing = analysis["routing_recommendation"]
        
        if routing["route_to_human"]:
            # Generate routing response
            primary_lang = analysis["primary_language"]
            routing_message = self.routing_templates.get(primary_lang, self.routing_templates["default"])
            
            return {
                "response": routing_message,
                "action": "route_to_human",
                "specialist": routing["specialist_needed"],
                "urgency": routing["urgency"],
                "reason": routing["reason"],
                "language_analysis": analysis
            }
        
        # Check if response should be adapted for language
        if analysis["primary_language"] != "en":
            # In production, this would translate or adapt the response
            adapted_response = self._add_language_acknowledgment(base_response, analysis["primary_language"])
            return {
                "response": adapted_response,
                "action": "continue_ai",
                "language_analysis": analysis
            }
            
        return {
            "response": base_response,
            "action": "continue_ai",
            "language_analysis": analysis
        }
    
    def _add_language_acknowledgment(self, response: str, language: str) -> str:
        """Add language acknowledgment to response"""
        acknowledgments = {
            "es": "I see you're more comfortable in Spanish. ",
            "zh": "I notice you prefer Chinese. ",
            "ar": "I notice you're using Arabic. ",
            "tl": "I see you're using Tagalog. "
        }
        
        prefix = acknowledgments.get(language, "")
        if prefix:
            return prefix + "Continue in whatever language feels natural. " + response
        return response


# Example usage
def demonstrate_bilingual_routing():
    detector = BilingualCrisisDetector()
    router = BilingualResponseRouter(detector)
    
    # Simulate crisis with language switching
    interactions = [
        ("My ceiling is leaking badly!", {"arousal": 7}, "en"),
        ("No sé qué hacer, agua everywhere!", {"arousal": 8.5}, "es/en"),
        ("Por favor ayuda, my kids están scared", {"arousal": 9}, "es/en"),
        ("HELP!! Todo está flooding!!", {"arousal": 9.5}, "es/en")
    ]
    
    base_response = "I'm here with you. Let's address this step by step."
    
    for message, state, desc in interactions:
        print(f"\n--- {desc} ---")
        print(f"User: {message}")
        print(f"Arousal: {state['arousal']}")
        
        result = router.process_interaction("user_123", message, state, base_response)
        
        print(f"Action: {result['action']}")
        print(f"Response: {result['response']}")
        
        if result["action"] == "route_to_human":
            print(f"Routing: {result['urgency']} priority to {result['specialist']}")
            print(f"Reason: {result['reason']}")


if __name__ == "__main__":
    demonstrate_bilingual_routing()