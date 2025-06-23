#!/usr/bin/env python3
"""
Willow Response Component Library
Reusable, trauma-informed response elements to reduce generation time
"""

import random
from typing import Dict, List, Optional, Tuple

class WillowResponseLibrary:
    """Library of trauma-informed response components."""
    
    # Tier 1 Opening Validations
    TIER1_OPENINGS = {
        "financial_crisis": [
            "The weight of choosing between {need1} and {need2} is crushing. No one should face these impossible calculations.",
            "When every dollar is already stretched beyond breaking, {new_crisis} feels like drowning. Your exhaustion is real.",
            "{Time_period} of financial terror leaves deep marks. Your body remembers every eviction notice, every shut-off warning."
        ],
        "discrimination": [
            "Being targeted for who you are cuts deeper than any physical wound. Your {identity} is not a reason for punishment.",
            "The cruelty of {discriminatory_act} reveals their failure, not yours. You deserve safety in your own home.",
            "Living under constant threat of {discrimination_type} exhausts the soul. Your vigilance has kept you alive."
        ],
        "maintenance_emergency": [
            "{Duration} without {basic_need} isn't just inconvenient - it's survival mode. Your distress signals health, not weakness.",
            "When home becomes hazardous, the nervous system never rests. {Specific_hazard} threatens your sanctuary.",
            "Begging for basic repairs while being ignored is dehumanizing. Your anger at this neglect is justified."
        ],
        "family_crisis": [
            "The threat of losing {family_member} while managing {housing_issue} splits you in impossible directions.",
            "Protecting {vulnerable_person} while your own foundation crumbles requires superhuman strength.",
            "When {system} threatens your family bonds, the terror is primal. Your fight to keep everyone together is sacred."
        ],
        "medical_emergency": [
            "{Medical_condition} already steals so much. Adding {housing_crisis} feels unconscionably cruel.",
            "Your body needs rest to heal, but {stressor} makes rest impossible. This intersection of crises is inhumane.",
            "Managing {treatment} while facing {threat} asks more than any person should bear. Your overwhelm is proportional."
        ]
    }
    
    # Tier 1 Trauma Recognition
    TRAUMA_RECOGNITION = {
        "systemic_abandonment": [
            "Every system that should protect you has turned away. This coordinated abandonment is not your fault.",
            "You've been passed between agencies like a burden, not a human being. This institutional cruelty is traumatizing.",
            "The safety net has too many holes, and you've fallen through every one. Society has failed its basic contract with you."
        ],
        "chronic_crisis": [
            "Living in perpetual emergency rewires the nervous system. Your hypervigilance is an adaptation, not a disorder.",
            "When crisis becomes chronic, exhaustion becomes bone-deep. You're not weak - you're depleted by circumstances.",
            "{Years/Months} of constant threat would break anyone. Your continued functioning is remarkable."
        ],
        "identity_violence": [
            "Being punished for your {identity_aspect} is violence to the soul. This targeted cruelty leaves invisible wounds.",
            "Having to hide who you are for housing safety is its own trauma. Authenticity shouldn't cost shelter.",
            "The message that you don't belong in safe housing because of {identity} is a lie. You belong. You matter."
        ],
        "compound_trauma": [
            "Each crisis compounds the last - {crisis1} led to {crisis2} which triggered {crisis3}. This avalanche wasn't your fault.",
            "Trauma doesn't queue politely. When {multiple_traumas} hit simultaneously, the overwhelm is exponential.",
            "Your story holds {layer1} within {layer2} within {layer3}. These nested traumas deserve gentle unpacking."
        ]
    }
    
    # Tier 2 Resource Connections
    TIER2_RESOURCES = {
        "legal_support": [
            "I can help connect you with {specific_org} - they specialize in {specific_issue} and often work with people facing {similar_situation}. Their intake line is {contact}.",
            "For immediate legal protection, {organization} offers emergency consultations. They understand {specific_context} and typically respond within {timeframe}.",
            "{Legal_aid_group} has attorneys who specifically handle {issue_type}. Many clients qualify for free representation based on {criteria}."
        ],
        "emergency_assistance": [
            "For immediate {need}, {organization} has emergency funds available. The application typically takes {timeframe} and they understand crisis situations.",
            "{Resource} can provide {specific_help} while we work on longer-term solutions. They're reachable at {contact} and have helped many in your situation.",
            "Let's tackle this from multiple angles: {resource1} for immediate {need1}, {resource2} for {need2}, and {resource3} for ongoing support."
        ],
        "medical_advocacy": [
            "{Medical_legal_org} helps when health crises meet housing problems. They can advocate with both medical providers and landlords.",
            "For {medical_condition} accommodations in housing, {disability_org} provides free advocacy. They know the laws and have template letters.",
            "{Health_justice_org} specifically works at the intersection of {health_issue} and housing rights. They offer both direct service and systemic advocacy."
        ],
        "community_support": [
            "{Community_org} has helped many neighbors facing {similar_issue}. They offer {specific_services} and understand the local context.",
            "The {identity} community has built support networks for exactly this situation. {Organization} can connect you with others who've navigated this.",
            "{Mutual_aid_group} operates on solidarity, not charity. They provide {specific_support} without judgment or requirements."
        ]
    }
    
    # Tier 2 Action Planning
    ACTION_PLANNING = {
        "documentation": [
            "Let's build your evidence file: photos of {condition}, dated records of {communication}, and a timeline of {events}. This creates undeniable proof.",
            "Document everything - even if it feels pointless. Save texts showing {pattern}, photograph {evidence}, and keep a log of {impacts}.",
            "Your paper trail becomes your power. Every {incident} you document, every {communication} you save strengthens your position."
        ],
        "staged_approach": [
            "We'll approach this in layers: First, {immediate_action} for safety. Then {medium_action} for stability. Finally, {long_action} for justice.",
            "Breaking this into steps: Today, {step1}. This week, {step2}. By month's end, {step3}. Each small victory builds momentum.",
            "Let's start with what's most urgent - {priority1}. Once that's stabilized, we can tackle {priority2}, then build toward {priority3}."
        ],
        "rights_assertion": [
            "Your right to {specific_right} is protected under {law/code}. I can help you draft a letter citing these protections.",
            "They may be counting on you not knowing your rights. {Specific_protection} specifically prohibits {their_action}.",
            "Knowledge is power here. {Law/regulation} requires {specific_requirement}. Let's use this to protect you."
        ],
        "collective_action": [
            "You're not alone in this. {Organization} is building collective power around {issue}. There's strength in numbers.",
            "Other tenants may be facing the same {issue}. {Tenant_union} can help you connect and organize together.",
            "When individual complaints are ignored, collective action gets attention. {Group} has experience organizing around {similar_issue}."
        ]
    }
    
    # Closing affirmations
    CLOSING_AFFIRMATIONS = {
        "strength_recognition": [
            "You've survived {duration} of this. That takes extraordinary strength, even when you feel weakest.",
            "Reaching out while in crisis takes courage. You're taking steps to protect yourself and {who/what you're protecting}.",
            "Your persistence in seeking help despite {obstacles} shows your determination to survive. I see that strength."
        ],
        "hope_threading": [
            "Solutions exist, even when they're hidden. We'll work together to uncover them.",
            "This feels endless, but it's not. People in your exact situation have found pathways through.",
            "Each small step matters. Today's {action} plants seeds for tomorrow's stability."
        ],
        "dignity_restoration": [
            "You deserve safe, stable housing simply because you're human. That's not negotiable.",
            "Your worth isn't measured by your crisis. You matter, fully and completely, right now.",
            "Being in crisis doesn't diminish your dignity. You deserve respect and real help."
        ]
    }
    
    # Symbolic language elements
    SYMBOLIC_ELEMENTS = {
        "nature": {
            "trees": ["roots", "branches", "growth rings", "seasons", "storms weathered"],
            "water": ["currents", "tides", "wells", "rain", "rivers finding ways"],
            "earth": ["ground", "foundation", "bedrock", "soil", "planted seeds"],
            "sky": ["horizons", "dawn", "clearing skies", "navigation stars", "breathing room"]
        },
        "traditional": {
            "journey": ["path", "crossroads", "mountains", "valleys", "destinations"],
            "building": ["foundations", "scaffolding", "blueprints", "materials", "shelter"],
            "weaving": ["threads", "patterns", "fabric", "loom", "tapestry"],
            "light": ["shadows", "dawn", "candles", "beacons", "illumination"]
        },
        "minimal": {
            "simple": ["here", "now", "together", "possible", "beginning"],
            "action": ["step", "move", "build", "connect", "protect"],
            "state": ["safe", "heard", "real", "valid", "worthy"]
        }
    }
    
    @classmethod
    def get_opening(cls, crisis_type: str, specific_context: Dict[str, str]) -> str:
        """Get appropriate tier 1 opening for crisis type."""
        templates = cls.TIER1_OPENINGS.get(crisis_type, cls.TIER1_OPENINGS["financial_crisis"])
        template = random.choice(templates)
        
        # Fill in placeholders
        for key, value in specific_context.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, value)
                
        return template
    
    @classmethod
    def get_trauma_recognition(cls, trauma_type: str, details: Optional[Dict] = None) -> str:
        """Get trauma recognition statement."""
        statements = cls.TRAUMA_RECOGNITION.get(trauma_type, cls.TRAUMA_RECOGNITION["systemic_abandonment"])
        statement = random.choice(statements)
        
        if details:
            for key, value in details.items():
                placeholder = f"{{{key}}}"
                if placeholder in statement:
                    statement = statement.replace(placeholder, value)
                    
        return statement
    
    @classmethod
    def get_resource_connection(cls, resource_type: str, specifics: Dict[str, str]) -> str:
        """Get tier 2 resource connection language."""
        templates = cls.TIER2_RESOURCES.get(resource_type, cls.TIER2_RESOURCES["community_support"])
        template = random.choice(templates)
        
        for key, value in specifics.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, value)
                
        return template
    
    @classmethod
    def get_action_plan(cls, plan_type: str, steps: Dict[str, str]) -> str:
        """Get action planning language."""
        templates = cls.ACTION_PLANNING.get(plan_type, cls.ACTION_PLANNING["staged_approach"])
        template = random.choice(templates)
        
        for key, value in steps.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, value)
                
        return template
    
    @classmethod
    def get_closing(cls, closing_type: str, context: Optional[Dict] = None) -> str:
        """Get closing affirmation."""
        closings = cls.CLOSING_AFFIRMATIONS.get(closing_type, cls.CLOSING_AFFIRMATIONS["dignity_restoration"])
        closing = random.choice(closings)
        
        if context:
            for key, value in context.items():
                placeholder = f"{{{key}}}"
                if placeholder in closing:
                    closing = closing.replace(placeholder, value)
                    
        return closing
    
    @classmethod
    def add_symbolic_language(cls, base_text: str, symbolic_type: str = "traditional") -> str:
        """Weave symbolic language into response."""
        if symbolic_type == "none":
            return base_text
            
        symbols = cls.SYMBOLIC_ELEMENTS.get(symbolic_type, cls.SYMBOLIC_ELEMENTS["minimal"])
        
        # Select random symbolic category
        category = random.choice(list(symbols.keys()))
        elements = symbols[category]
        
        # Add 1-2 symbolic elements
        if symbolic_type == "minimal":
            # For minimal, just add one word
            word = random.choice(elements)
            return base_text + f" {word.capitalize()}."
        else:
            # For richer symbolic language, weave in metaphor
            element1, element2 = random.sample(elements, 2)
            
            if symbolic_type == "nature":
                metaphor = f" Like {element1} finding {element2}, we'll navigate this together."
            else:  # traditional
                metaphor = f" We'll build {element1} toward {element2}, step by step."
                
            # Insert metaphor at appropriate point
            sentences = base_text.split('. ')
            if len(sentences) > 2:
                sentences.insert(-1, metaphor)
            else:
                sentences.append(metaphor)
                
            return '. '.join(sentences)
    
    @classmethod
    def build_complete_response(
        cls,
        tier: str,
        crisis_type: str,
        specific_context: Dict[str, str],
        trauma_type: Optional[str] = None,
        resource_info: Optional[Dict[str, str]] = None,
        action_steps: Optional[Dict[str, str]] = None,
        symbolic_type: str = "traditional"
    ) -> str:
        """Build complete response from components."""
        
        if tier == "tier_1":
            # Build tier 1 response
            opening = cls.get_opening(crisis_type, specific_context)
            
            if trauma_type:
                recognition = cls.get_trauma_recognition(trauma_type, specific_context)
                response = f"{opening} {recognition}"
            else:
                response = opening
                
            closing = cls.get_closing("strength_recognition", specific_context)
            response = f"{response} {closing}"
            
        else:  # tier_2
            # Build tier 2 response
            parts = []
            
            if resource_info:
                resource_type = resource_info.pop("type", "community_support")
                parts.append(cls.get_resource_connection(resource_type, resource_info))
                
            if action_steps:
                plan_type = action_steps.pop("type", "staged_approach")
                parts.append(cls.get_action_plan(plan_type, action_steps))
                
            response = " ".join(parts)
            
            if not response:
                # Fallback if no specific resources/actions provided
                response = cls.get_resource_connection("community_support", {
                    "Community_org": "Local tenant support network",
                    "similar_issue": "housing crisis",
                    "specific_services": "emergency assistance and advocacy"
                })
                
            closing = cls.get_closing("hope_threading", specific_context)
            response = f"{response} {closing}"
        
        # Add symbolic language
        response = cls.add_symbolic_language(response, symbolic_type)
        
        return response


def demonstrate_usage():
    """Show how to use the response library."""
    library = WillowResponseLibrary()
    
    # Example 1: Financial crisis tier 1
    tier1_response = library.build_complete_response(
        tier="tier_1",
        crisis_type="financial_crisis",
        specific_context={
            "need1": "medication",
            "need2": "rent",
            "new_crisis": "the eviction notice",
            "Time_period": "Six months"
        },
        trauma_type="systemic_abandonment",
        symbolic_type="nature"
    )
    print("Tier 1 Financial Crisis Response:")
    print(tier1_response)
    print()
    
    # Example 2: Discrimination tier 2
    tier2_response = library.build_complete_response(
        tier="tier_2",
        crisis_type="discrimination",
        specific_context={
            "identity": "disability"
        },
        resource_info={
            "type": "legal_support",
            "specific_org": "Fair Housing Justice Center",
            "specific_issue": "disability discrimination",
            "similar_situation": "accommodation denials",
            "contact": "1-800-555-FAIR"
        },
        action_steps={
            "type": "rights_assertion",
            "specific_right": "reasonable accommodations",
            "law/code": "Fair Housing Act",
            "their_action": "refusing your accommodation request"
        },
        symbolic_type="minimal"
    )
    print("Tier 2 Discrimination Response:")
    print(tier2_response)


if __name__ == "__main__":
    demonstrate_usage()