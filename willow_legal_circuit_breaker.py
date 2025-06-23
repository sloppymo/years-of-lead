#!/usr/bin/env python3
"""
Willow Legal Circuit Breaker System
Prevents AI from providing legal advice or creating liability
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re


class LegalRiskLevel(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResponseType(Enum):
    NORMAL = "normal"
    REDIRECT = "redirect"
    CONTAINMENT = "containment"
    ESCALATION = "escalation"


@dataclass
class LegalTrigger:
    """Represents a legal trigger pattern"""
    pattern: str
    risk_level: LegalRiskLevel
    category: str
    redirect_template: str


@dataclass
class CircuitBreakerResponse:
    """Response when legal circuit breaker is triggered"""
    original_query: str
    risk_level: LegalRiskLevel
    tenant_response: str
    manager_alert: Optional[str]
    documentation: Dict[str, Any]
    flags: List[str]


class LegalCircuitBreaker:
    """
    Pre-filters tenant messages for legal content and provides safe responses
    """
    
    def __init__(self):
        self.triggers = self._initialize_triggers()
        self.redirect_templates = self._initialize_templates()
        
    def _initialize_triggers(self) -> List[LegalTrigger]:
        """Initialize legal trigger patterns"""
        return [
            # Critical triggers
            LegalTrigger(
                pattern=r"\b(sue|suing|lawsuit|litigation)\b",
                risk_level=LegalRiskLevel.CRITICAL,
                category="legal_threat",
                redirect_template="legal_threat_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(discrimination|discriminate|discriminating)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="discrimination_claim",
                redirect_template="discrimination_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(illegal|unlawful|against the law)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="illegality_claim",
                redirect_template="legal_determination_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(ADA|disability act|accommodation)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="ada_compliance",
                redirect_template="ada_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(retaliation|retaliating|retaliate)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="retaliation_claim",
                redirect_template="retaliation_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(harassment|harassing|harassed)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="harassment_claim",
                redirect_template="harassment_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(constructive eviction|forced out)\b",
                risk_level=LegalRiskLevel.CRITICAL,
                category="constructive_eviction",
                redirect_template="eviction_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(fair housing|housing rights|tenant rights)\b",
                risk_level=LegalRiskLevel.MEDIUM,
                category="rights_assertion",
                redirect_template="rights_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(report you|file a complaint|housing authority)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="regulatory_threat",
                redirect_template="regulatory_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(lawyer|attorney|legal counsel)\b",
                risk_level=LegalRiskLevel.HIGH,
                category="legal_representation",
                redirect_template="lawyer_redirect"
            ),
            # Medium risk triggers
            LegalTrigger(
                pattern=r"\b(violat\w+|breach\w+)\s+(lease|contract|agreement)\b",
                risk_level=LegalRiskLevel.MEDIUM,
                category="contract_dispute",
                redirect_template="contract_redirect"
            ),
            LegalTrigger(
                pattern=r"\b(know my rights|legal rights|entitled to)\b",
                risk_level=LegalRiskLevel.MEDIUM,
                category="rights_awareness",
                redirect_template="rights_redirect"
            )
        ]
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize safe redirect templates"""
        return {
            "legal_threat_redirect": (
                "I understand you're considering legal action. While I can't discuss legal matters, "
                "I can help document your concerns for your records. Would you like me to note "
                "the specific issues you're experiencing?"
            ),
            "discrimination_redirect": (
                "I hear that you're experiencing something that feels unfair. While I can't make "
                "legal determinations, I can document your concerns and connect you with tenant "
                "advocacy resources who specialize in these matters."
            ),
            "legal_determination_redirect": (
                "That's an important question about legal compliance. I'm not able to make legal "
                "determinations, but I can help you document the situation and provide contact "
                "information for tenant rights organizations."
            ),
            "ada_redirect": (
                "Accessibility and accommodations are important. While I can't provide legal advice "
                "about ADA compliance, I can help document your accommodation needs and connect you "
                "with disability rights advocates."
            ),
            "retaliation_redirect": (
                "I understand you're concerned about possible retaliation. While I can't make legal "
                "assessments, I can help you document events with dates and details, which could be "
                "helpful if you consult with a housing advocate."
            ),
            "harassment_redirect": (
                "I'm sorry you're experiencing this. While I can't make legal determinations about "
                "harassment, I can help you document incidents and connect you with appropriate "
                "support resources."
            ),
            "eviction_redirect": (
                "Housing stability is crucial. While I can't provide legal advice about eviction, "
                "I strongly encourage you to contact a tenant rights attorney or legal aid "
                "organization immediately. I can provide their contact information."
            ),
            "rights_redirect": (
                "Understanding your rights is important. While I can't provide legal interpretations, "
                "I can connect you with tenant advocacy groups who can explain your rights and options."
            ),
            "regulatory_redirect": (
                "I understand you may want to file a complaint. While I can't advise on regulatory "
                "matters, I can provide contact information for the appropriate housing authorities "
                "and help you document your concerns."
            ),
            "lawyer_redirect": (
                "I understand you're considering legal representation. While I can't discuss legal "
                "strategy, I can help ensure your concerns are documented and provide information "
                "about legal aid resources if helpful."
            ),
            "contract_redirect": (
                "Questions about lease terms are important. While I can't interpret legal documents, "
                "I can help you document your concerns and suggest resources for lease review."
            ),
            "default_redirect": (
                "That sounds like an important legal question. While I'm not able to provide legal "
                "advice or make legal determinations, I can help document your concerns and connect "
                "you with appropriate resources."
            )
        }
    
    def check_message(self, message: str) -> Tuple[bool, Optional[LegalTrigger]]:
        """
        Check if message contains legal triggers
        Returns (is_triggered, trigger_info)
        """
        message_lower = message.lower()
        
        # Check each trigger pattern
        highest_risk_trigger = None
        highest_risk_level = LegalRiskLevel.NONE
        
        for trigger in self.triggers:
            if re.search(trigger.pattern, message_lower):
                if self._compare_risk_levels(trigger.risk_level, highest_risk_level) > 0:
                    highest_risk_trigger = trigger
                    highest_risk_level = trigger.risk_level
        
        return (highest_risk_trigger is not None, highest_risk_trigger)
    
    def _compare_risk_levels(self, level1: LegalRiskLevel, level2: LegalRiskLevel) -> int:
        """Compare risk levels (-1, 0, 1)"""
        risk_order = {
            LegalRiskLevel.NONE: 0,
            LegalRiskLevel.LOW: 1,
            LegalRiskLevel.MEDIUM: 2,
            LegalRiskLevel.HIGH: 3,
            LegalRiskLevel.CRITICAL: 4
        }
        return risk_order[level1] - risk_order[level2]
    
    def generate_safe_response(self, 
                             message: str, 
                             trigger: LegalTrigger,
                             context: Optional[Dict] = None) -> CircuitBreakerResponse:
        """Generate a safe response when legal trigger is detected"""
        
        # Get appropriate template
        template = self.redirect_templates.get(
            trigger.redirect_template,
            self.redirect_templates["default_redirect"]
        )
        
        # Generate manager alert for high-risk triggers
        manager_alert = None
        if trigger.risk_level in [LegalRiskLevel.HIGH, LegalRiskLevel.CRITICAL]:
            manager_alert = self._generate_manager_alert(message, trigger, context)
        
        # Create documentation
        documentation = {
            "timestamp": "2024-01-15T10:30:00Z",  # Would be datetime.now() in production
            "trigger_category": trigger.category,
            "risk_level": trigger.risk_level.value,
            "original_message": message,
            "context": context or {}
        }
        
        # Set appropriate flags
        flags = [trigger.category, "legal_redirect"]
        if trigger.risk_level == LegalRiskLevel.CRITICAL:
            flags.append("urgent_review")
        
        return CircuitBreakerResponse(
            original_query=message,
            risk_level=trigger.risk_level,
            tenant_response=template,
            manager_alert=manager_alert,
            documentation=documentation,
            flags=flags
        )
    
    def _generate_manager_alert(self, 
                               message: str, 
                               trigger: LegalTrigger,
                               context: Optional[Dict]) -> str:
        """Generate manager alert for high-risk situations"""
        
        alert_templates = {
            "legal_threat": (
                "⚠️ LEGAL THREAT DETECTED\n"
                "Tenant mentioned potential legal action.\n"
                "Original message: {message}\n"
                "Recommended actions:\n"
                "1. Review interaction history\n"
                "2. Consult with legal counsel\n"
                "3. Document all communications\n"
                "4. Do not admit fault or make promises"
            ),
            "discrimination_claim": (
                "⚠️ DISCRIMINATION CONCERN\n"
                "Tenant raised potential discrimination issue.\n"
                "Original message: {message}\n"
                "Recommended actions:\n"
                "1. Review fair housing compliance\n"
                "2. Document objective business reasons for any actions\n"
                "3. Consider legal consultation\n"
                "4. Ensure consistent treatment of all tenants"
            ),
            "constructive_eviction": (
                "🚨 CRITICAL: CONSTRUCTIVE EVICTION CLAIM\n"
                "Tenant may be claiming forced displacement.\n"
                "Original message: {message}\n"
                "IMMEDIATE ACTIONS REQUIRED:\n"
                "1. Contact legal counsel immediately\n"
                "2. Document all maintenance/habitability efforts\n"
                "3. Preserve all communications\n"
                "4. Do not take any adverse actions"
            )
        }
        
        template = alert_templates.get(
            trigger.category,
            "⚠️ LEGAL RISK DETECTED\nCategory: {category}\nMessage: {message}\nReview required."
        )
        
        return template.format(
            message=message,
            category=trigger.category
        )
    
    def process_conversation(self, 
                           message: str,
                           conversation_history: List[Dict],
                           tenant_context: Dict) -> Dict[str, Any]:
        """
        Main entry point for processing tenant messages
        """
        # Check for legal triggers
        is_triggered, trigger = self.check_message(message)
        
        if not is_triggered:
            # No legal issues detected, proceed normally
            return {
                "action": "proceed",
                "risk_level": LegalRiskLevel.NONE,
                "response": None
            }
        
        # Legal trigger detected - generate safe response
        safe_response = self.generate_safe_response(
            message=message,
            trigger=trigger,
            context={
                "conversation_history": conversation_history,
                "tenant_context": tenant_context
            }
        )
        
        # Return circuit breaker response
        return {
            "action": "redirect",
            "risk_level": safe_response.risk_level,
            "response": safe_response,
            "require_human_review": trigger.risk_level in [LegalRiskLevel.HIGH, LegalRiskLevel.CRITICAL]
        }


class TrainingDataGenerator:
    """Generate training data for legal circuit breaker"""
    
    def __init__(self, circuit_breaker: LegalCircuitBreaker):
        self.circuit_breaker = circuit_breaker
    
    def generate_training_examples(self) -> List[Dict]:
        """Generate training examples for the circuit breaker"""
        examples = []
        
        # Legal threat examples
        legal_threats = [
            "I'm going to sue you for this!",
            "My lawyer will be contacting you",
            "This is grounds for a lawsuit",
            "I'll see you in court",
            "Expect to hear from my attorney"
        ]
        
        for threat in legal_threats:
            _, trigger = self.circuit_breaker.check_message(threat)
            if trigger:
                response = self.circuit_breaker.generate_safe_response(threat, trigger)
                examples.append({
                    "id": f"LEGAL_TRAIN_{len(examples)+1}",
                    "input": threat,
                    "output": response.tenant_response,
                    "category": "legal_threat",
                    "flags": response.flags
                })
        
        # Discrimination claims
        discrimination_claims = [
            "This is discrimination because of my race",
            "You're treating me differently because I have kids",
            "This is disability discrimination",
            "You're discriminating against my religion",
            "This is housing discrimination"
        ]
        
        for claim in discrimination_claims:
            _, trigger = self.circuit_breaker.check_message(claim)
            if trigger:
                response = self.circuit_breaker.generate_safe_response(claim, trigger)
                examples.append({
                    "id": f"LEGAL_TRAIN_{len(examples)+1}",
                    "input": claim,
                    "output": response.tenant_response,
                    "category": "discrimination_claim",
                    "flags": response.flags
                })
        
        # Rights assertions
        rights_assertions = [
            "I know my rights as a tenant",
            "This violates my lease agreement",
            "You're breaking the law",
            "This is illegal under state law",
            "The fair housing act protects me"
        ]
        
        for assertion in rights_assertions:
            _, trigger = self.circuit_breaker.check_message(assertion)
            if trigger:
                response = self.circuit_breaker.generate_safe_response(assertion, trigger)
                examples.append({
                    "id": f"LEGAL_TRAIN_{len(examples)+1}",
                    "input": assertion,
                    "output": response.tenant_response,
                    "category": "rights_assertion",
                    "flags": response.flags
                })
        
        return examples


# Example usage
if __name__ == "__main__":
    # Initialize circuit breaker
    circuit_breaker = LegalCircuitBreaker()
    
    # Test various messages
    test_messages = [
        "The heater is broken and it's freezing",  # Normal - should pass through
        "I'm going to sue you for negligence!",    # Legal threat - should trigger
        "This is discrimination!",                  # Discrimination - should trigger
        "My lawyer says this is illegal",          # Legal reference - should trigger
        "Can you fix the sink please?",            # Normal - should pass through
    ]
    
    print("Legal Circuit Breaker Test Results:")
    print("=" * 50)
    
    for message in test_messages:
        result = circuit_breaker.process_conversation(
            message=message,
            conversation_history=[],
            tenant_context={"tenant_id": "TEST_001"}
        )
        
        print(f"\nMessage: {message}")
        print(f"Action: {result['action']}")
        print(f"Risk Level: {result['risk_level'].value}")
        
        if result['action'] == 'redirect':
            print(f"Safe Response: {result['response'].tenant_response}")
            if result['response'].manager_alert:
                print(f"Manager Alert: {result['response'].manager_alert[:100]}...")
    
    # Generate training data
    print("\n\nGenerating Training Data...")
    print("=" * 50)
    
    generator = TrainingDataGenerator(circuit_breaker)
    training_examples = generator.generate_training_examples()
    
    print(f"Generated {len(training_examples)} training examples")
    
    # Show sample
    print("\nSample Training Example:")
    print(training_examples[0])