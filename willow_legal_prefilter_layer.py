#!/usr/bin/env python3
"""
Willow Legal Pre-Filter Layer
Intercepts and redirects legal queries before main AI processing
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
import json
from datetime import datetime


class LegalCategory(Enum):
    """Categories of legal concerns"""
    LAWSUIT_THREAT = "lawsuit_threat"
    DISCRIMINATION_CLAIM = "discrimination_claim"
    RIGHTS_ASSERTION = "rights_assertion"
    LEGAL_ADVICE_SEEKING = "legal_advice_seeking"
    REGULATORY_COMPLAINT = "regulatory_complaint"
    LIABILITY_QUESTION = "liability_question"
    EVICTION_CHALLENGE = "eviction_challenge"
    HARASSMENT_CLAIM = "harassment_claim"


@dataclass
class FilterResult:
    """Result of pre-filter analysis"""
    triggered: bool
    category: Optional[LegalCategory]
    confidence: float
    redirect_response: str
    manager_alert: Optional[str]
    keywords_matched: List[str]
    context_flags: List[str]


class LegalPreFilter:
    """Pre-filter layer for legal content detection"""
    
    def __init__(self):
        # Primary trigger keywords (high confidence)
        self.primary_triggers = {
            'sue', 'lawsuit', 'lawyer', 'attorney', 'legal action',
            'court', 'judge', 'litigation', 'prosecute', 'damages',
            'discrimination', 'harassment', 'retaliation', 'illegal',
            'unlawful', 'violation', 'rights', 'fair housing',
            'ada', 'fha', 'hud', 'constructive eviction',
            'breach', 'negligence', 'liability', 'complaint'
        }
        
        # Secondary indicators (medium confidence)
        self.secondary_indicators = {
            'report', 'authorities', 'government', 'agency',
            'investigate', 'document', 'evidence', 'witness',
            'hostile', 'unsafe', 'dangerous', 'unlivable',
            'health department', 'building inspector', 'news',
            'social media', 'review', 'warn others'
        }
        
        # Context amplifiers (increase confidence when present)
        self.context_amplifiers = {
            'going to', 'will', 'plan to', 'considering',
            'thinking about', 'might', 'should i', 'can i',
            'have to', 'need to', 'want to', 'trying to'
        }
        
        # Phrases requiring immediate redirect
        self.immediate_redirect_phrases = [
            r'i(?:\'m| am) (?:going to|gonna) sue',
            r'see you in court',
            r'hear from my (?:lawyer|attorney)',
            r'is this (?:legal|illegal)',
            r'(?:my|i know my) rights',
            r'(?:racial|sexual|age) discrimination',
            r'hostile (?:environment|housing)',
            r'constructive eviction',
            r'breach of (?:contract|lease)',
            r'violat(?:ing|ed) (?:the law|my rights)',
            r'fair housing (?:violation|complaint)',
            r'report(?:ing)? (?:you|this) to'
        ]
        
        # Category patterns
        self.category_patterns = {
            LegalCategory.LAWSUIT_THREAT: [
                r'sue', r'lawsuit', r'court', r'litigation'
            ],
            LegalCategory.DISCRIMINATION_CLAIM: [
                r'discriminat', r'bias', r'unfair treatment',
                r'because (?:i\'m|i am|of my)'
            ],
            LegalCategory.RIGHTS_ASSERTION: [
                r'my rights', r'tenant rights', r'know my rights',
                r'right to', r'entitled to'
            ],
            LegalCategory.LEGAL_ADVICE_SEEKING: [
                r'is (?:this|it) legal', r'can (?:you|they) legally',
                r'what (?:are|\'re) my options', r'legal(?:ly)?'
            ],
            LegalCategory.REGULATORY_COMPLAINT: [
                r'report to', r'file (?:a )?complaint',
                r'health department', r'building code'
            ],
            LegalCategory.LIABILITY_QUESTION: [
                r'liable', r'liability', r'responsible for',
                r'fault', r'negligence'
            ],
            LegalCategory.EVICTION_CHALLENGE: [
                r'can\'t evict', r'illegal eviction',
                r'eviction notice', r'fight (?:the )?eviction'
            ],
            LegalCategory.HARASSMENT_CLAIM: [
                r'harass', r'intimidat', r'threaten',
                r'hostile', r'retaliat'
            ]
        }
        
        # Response templates by category
        self.response_templates = {
            LegalCategory.LAWSUIT_THREAT: (
                "I understand you're considering legal action. While I can't "
                "discuss legal matters, I can help document your concerns for "
                "your records. Would you like me to note the specific issues "
                "you're experiencing?"
            ),
            LegalCategory.DISCRIMINATION_CLAIM: (
                "I hear that you feel you've been treated unfairly. I can't "
                "make legal determinations, but I can document your experience "
                "and provide information about tenant resources and advocacy groups."
            ),
            LegalCategory.RIGHTS_ASSERTION: (
                "Tenant rights are important. While I can't provide legal "
                "interpretations, I can share general information about "
                "tenancy and connect you with tenant advocacy resources."
            ),
            LegalCategory.LEGAL_ADVICE_SEEKING: (
                "That sounds like a legal question. I'm not able to provide "
                "legal advice, but I can help you find appropriate resources "
                "or document your concerns for when you speak with a professional."
            ),
            LegalCategory.REGULATORY_COMPLAINT: (
                "I understand you're considering filing a complaint. While I "
                "can't advise on regulatory matters, I can help document the "
                "issues and provide contact information for relevant agencies."
            ),
            LegalCategory.LIABILITY_QUESTION: (
                "Questions about liability are legal matters I can't address. "
                "I can help document the situation and connect you with "
                "resources for proper legal guidance."
            ),
            LegalCategory.EVICTION_CHALLENGE: (
                "Eviction concerns are serious legal matters. I can't provide "
                "legal advice, but I can connect you with tenant advocacy "
                "groups and legal aid resources who can help."
            ),
            LegalCategory.HARASSMENT_CLAIM: (
                "I'm sorry you're experiencing this. While I can't make legal "
                "determinations about harassment, I can document your concerns "
                "and provide information about support resources."
            )
        }
        
        # Compile regex patterns
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for efficiency"""
        self.redirect_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.immediate_redirect_phrases
        ]
        
        self.category_regex = {}
        for category, patterns in self.category_patterns.items():
            self.category_regex[category] = [
                re.compile(pattern, re.IGNORECASE) 
                for pattern in patterns
            ]
    
    def analyze_message(self, message: str) -> FilterResult:
        """
        Analyze message for legal content requiring pre-filtering
        
        Args:
            message: Tenant message to analyze
            
        Returns:
            FilterResult with redirect decision and response
        """
        message_lower = message.lower()
        
        # Check for immediate redirect phrases
        for pattern in self.redirect_patterns:
            if pattern.search(message):
                category = self._determine_category(message)
                return self._create_redirect_result(
                    category=category,
                    confidence=0.95,
                    message=message,
                    keywords_matched=self._extract_keywords(message)
                )
        
        # Calculate confidence based on keyword presence
        confidence, keywords = self._calculate_confidence(message_lower)
        
        # Determine if redirect needed
        if confidence >= 0.7:
            category = self._determine_category(message)
            return self._create_redirect_result(
                category=category,
                confidence=confidence,
                message=message,
                keywords_matched=keywords
            )
        
        # No redirect needed
        return FilterResult(
            triggered=False,
            category=None,
            confidence=confidence,
            redirect_response="",
            manager_alert=None,
            keywords_matched=keywords,
            context_flags=[]
        )
    
    def _calculate_confidence(self, message: str) -> Tuple[float, List[str]]:
        """Calculate confidence score for legal content"""
        keywords_found = []
        score = 0.0
        
        # Check primary triggers (0.3 each)
        for trigger in self.primary_triggers:
            if trigger in message:
                keywords_found.append(trigger)
                score += 0.3
        
        # Check secondary indicators (0.15 each)
        for indicator in self.secondary_indicators:
            if indicator in message:
                keywords_found.append(indicator)
                score += 0.15
        
        # Check context amplifiers (0.1 boost)
        has_amplifier = False
        for amplifier in self.context_amplifiers:
            if amplifier in message:
                has_amplifier = True
                break
        
        if has_amplifier and keywords_found:
            score += 0.1
        
        # Cap at 1.0
        confidence = min(score, 1.0)
        
        return confidence, keywords_found
    
    def _determine_category(self, message: str) -> LegalCategory:
        """Determine the legal category of the message"""
        scores = {}
        
        for category, patterns in self.category_regex.items():
            score = 0
            for pattern in patterns:
                if pattern.search(message):
                    score += 1
            scores[category] = score
        
        # Return category with highest score, default to general seeking
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        return LegalCategory.LEGAL_ADVICE_SEEKING
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extract all legal keywords from message"""
        message_lower = message.lower()
        keywords = []
        
        for trigger in self.primary_triggers:
            if trigger in message_lower:
                keywords.append(trigger)
        
        for indicator in self.secondary_indicators:
            if indicator in message_lower:
                keywords.append(indicator)
        
        return keywords
    
    def _create_redirect_result(
        self,
        category: LegalCategory,
        confidence: float,
        message: str,
        keywords_matched: List[str]
    ) -> FilterResult:
        """Create a redirect result with appropriate response"""
        
        # Get base response
        response = self.response_templates.get(
            category,
            "That sounds like a legal matter. I can't provide legal advice, "
            "but I can help document your concerns or connect you with "
            "appropriate resources."
        )
        
        # Create manager alert
        manager_alert = self._create_manager_alert(
            category, confidence, message, keywords_matched
        )
        
        # Determine context flags
        context_flags = self._determine_context_flags(message)
        
        return FilterResult(
            triggered=True,
            category=category,
            confidence=confidence,
            redirect_response=response,
            manager_alert=manager_alert,
            keywords_matched=keywords_matched,
            context_flags=context_flags
        )
    
    def _create_manager_alert(
        self,
        category: LegalCategory,
        confidence: float,
        message: str,
        keywords: List[str]
    ) -> str:
        """Create alert for manager interface"""
        alert = f"""⚠️ LEGAL CONTENT DETECTED
Category: {category.value}
Confidence: {confidence:.1%}
Keywords: {', '.join(keywords)}
Original message: {message}

Recommended actions:
1. Review interaction history
2. Consider legal counsel consultation
3. Document all communications
4. Ensure compliance with fair housing laws
"""
        return alert
    
    def _determine_context_flags(self, message: str) -> List[str]:
        """Determine additional context flags"""
        flags = []
        
        # Check urgency
        if any(word in message.lower() for word in ['now', 'immediately', 'today']):
            flags.append('urgent')
        
        # Check emotion level
        if '!' in message or message.isupper():
            flags.append('high_emotion')
        
        # Check if threat
        if any(word in message.lower() for word in ['will sue', 'going to sue']):
            flags.append('active_threat')
        
        return flags


class PreFilterMiddleware:
    """Middleware to integrate pre-filter with main system"""
    
    def __init__(self):
        self.pre_filter = LegalPreFilter()
        self.filter_log = []
    
    def process_message(self, message: str, metadata: Dict) -> Tuple[bool, Dict]:
        """
        Process message through pre-filter
        
        Returns:
            (should_continue, response_data)
        """
        # Run pre-filter analysis
        result = self.pre_filter.analyze_message(message)
        
        # Log the interaction
        self._log_interaction(message, result, metadata)
        
        if result.triggered:
            # Create response data for legal redirect
            response_data = {
                'response': result.redirect_response,
                'category': result.category.value if result.category else None,
                'confidence': result.confidence,
                'manager_alert': result.manager_alert,
                'flags': result.context_flags,
                'pre_filtered': True
            }
            return False, response_data
        
        # Continue to main processing
        return True, {'pre_filtered': False}
    
    def _log_interaction(self, message: str, result: FilterResult, metadata: Dict):
        """Log interaction for analysis"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'tenant_id': metadata.get('tenant_id'),
            'message': message,
            'triggered': result.triggered,
            'category': result.category.value if result.category else None,
            'confidence': result.confidence,
            'keywords': result.keywords_matched
        }
        self.filter_log.append(log_entry)


def create_training_examples():
    """Generate training examples for the pre-filter"""
    pre_filter = LegalPreFilter()
    examples = []
    
    # Test messages
    test_messages = [
        # Clear legal threats
        "I'm going to sue you for this!",
        "You'll hear from my lawyer about this",
        "This is discrimination and I'm filing a complaint",
        "I know my rights and this is illegal",
        
        # Questions seeking legal advice
        "Is it legal for you to charge this fee?",
        "Can you legally enter without notice?",
        "What are my rights as a tenant?",
        
        # Borderline cases
        "This doesn't seem right to me",
        "I'm documenting everything that happens",
        "Other tenants should know about this",
        
        # Non-legal concerns
        "My sink is broken and needs repair",
        "The noise is really bothering me",
        "Can we discuss the rent payment?"
    ]
    
    for message in test_messages:
        result = pre_filter.analyze_message(message)
        examples.append({
            'input': message,
            'triggered': result.triggered,
            'confidence': result.confidence,
            'category': result.category.value if result.category else None,
            'response': result.redirect_response if result.triggered else None
        })
    
    return examples


if __name__ == "__main__":
    # Test the pre-filter
    middleware = PreFilterMiddleware()
    
    test_cases = [
        "I'm going to sue you for negligence!",
        "Is this mold situation even legal?",
        "My heater has been broken for a week",
        "This is discrimination because I have kids",
        "I need to report this to the health department"
    ]
    
    print("Pre-Filter Test Results:")
    print("=" * 50)
    
    for message in test_cases:
        should_continue, response = middleware.process_message(
            message, 
            {'tenant_id': 'test123'}
        )
        
        print(f"\nMessage: {message}")
        print(f"Continue to main: {should_continue}")
        if not should_continue:
            print(f"Redirect response: {response['response'][:100]}...")
            print(f"Category: {response['category']}")
            print(f"Confidence: {response['confidence']:.1%}")