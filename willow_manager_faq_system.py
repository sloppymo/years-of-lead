#!/usr/bin/env python3
"""
Willow Manager FAQ System
Integrates local laws, regulations, and company policies into Willow's response system
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
from enum import Enum


class PolicyType(Enum):
    LEGAL = "legal"
    COMPANY = "company"
    PROCEDURE = "procedure"
    BEST_PRACTICE = "best_practice"


class JurisdictionLevel(Enum):
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"
    MUNICIPAL = "municipal"


@dataclass
class PolicyDocument:
    """Represents a policy or legal document"""
    id: str
    type: PolicyType
    jurisdiction: Optional[JurisdictionLevel]
    title: str
    content: str
    effective_date: datetime
    expires: Optional[datetime]
    tags: List[str]
    source_url: Optional[str]
    last_updated: datetime


@dataclass
class FAQEntry:
    """Represents a frequently asked question"""
    id: str
    question: str
    answer_template: str
    policy_references: List[str]  # IDs of relevant PolicyDocuments
    scenario_tags: List[str]
    jurisdiction_specific: bool
    last_updated: datetime


class ManagerFAQSystem:
    """FAQ system for property managers integrated with Willow"""
    
    def __init__(self, policy_db_path: str, faq_db_path: str):
        self.policies: Dict[str, PolicyDocument] = {}
        self.faqs: Dict[str, FAQEntry] = {}
        self.jurisdiction_cache: Dict[str, List[str]] = {}
        
        # Load databases
        self._load_policies(policy_db_path)
        self._load_faqs(faq_db_path)
        
    def _load_policies(self, path: str):
        """Load policy documents from database"""
        # In production, this would connect to a real database
        # For demo, using JSON files
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                for policy_data in data:
                    policy = PolicyDocument(**policy_data)
                    self.policies[policy.id] = policy
        except FileNotFoundError:
            # Initialize with sample policies
            self._initialize_sample_policies()
    
    def _load_faqs(self, path: str):
        """Load FAQ entries from database"""
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                for faq_data in data:
                    faq = FAQEntry(**faq_data)
                    self.faqs[faq.id] = faq
        except FileNotFoundError:
            # Initialize with sample FAQs
            self._initialize_sample_faqs()
    
    def _initialize_sample_policies(self):
        """Create sample policy documents"""
        sample_policies = [
            PolicyDocument(
                id="FHA_2024",
                type=PolicyType.LEGAL,
                jurisdiction=JurisdictionLevel.FEDERAL,
                title="Fair Housing Act Compliance",
                content="No discrimination based on race, color, religion, sex, handicap, familial status, or national origin...",
                effective_date=datetime(2024, 1, 1),
                expires=None,
                tags=["discrimination", "accessibility", "reasonable_accommodation"],
                source_url="https://www.hud.gov/program_offices/fair_housing_equal_opp",
                last_updated=datetime(2024, 1, 1)
            ),
            PolicyDocument(
                id="EMERGENCY_REPAIR_POLICY",
                type=PolicyType.COMPANY,
                jurisdiction=None,
                title="Emergency Repair Response Times",
                content="Heat/AC failure: 4-hour response. Water leaks: 2-hour response. Electrical hazards: 1-hour response...",
                effective_date=datetime(2023, 6, 1),
                expires=None,
                tags=["emergency", "maintenance", "response_time"],
                source_url=None,
                last_updated=datetime(2023, 6, 1)
            ),
            PolicyDocument(
                id="RENT_COLLECTION_PROCEDURE",
                type=PolicyType.PROCEDURE,
                jurisdiction=JurisdictionLevel.STATE,
                title="Rent Collection and Late Fee Procedures",
                content="Rent due on 1st. Grace period until 5th. Late fee: 5% after grace period. Notice required after 10 days...",
                effective_date=datetime(2023, 1, 1),
                expires=None,
                tags=["rent", "payment", "late_fees", "eviction"],
                source_url=None,
                last_updated=datetime(2023, 1, 1)
            )
        ]
        
        for policy in sample_policies:
            self.policies[policy.id] = policy
    
    def _initialize_sample_faqs(self):
        """Create sample FAQ entries"""
        sample_faqs = [
            FAQEntry(
                id="FAQ_001",
                question="What are the legal requirements for handling a reasonable accommodation request?",
                answer_template="Under the Fair Housing Act, we must: 1) Accept requests in any form (verbal/written), 2) Engage in interactive process, 3) Grant if reasonable and necessary, 4) Cannot require medical records, only verification of disability-related need. See {FHA_2024} for full details.",
                policy_references=["FHA_2024"],
                scenario_tags=["disability", "accommodation", "legal"],
                jurisdiction_specific=False,
                last_updated=datetime(2024, 1, 1)
            ),
            FAQEntry(
                id="FAQ_002",
                question="How quickly must we respond to emergency maintenance requests?",
                answer_template="Per company policy {EMERGENCY_REPAIR_POLICY}: Heat/AC failure: 4 hours, Water leaks: 2 hours, Electrical hazards: 1 hour. Document all response times and actions taken.",
                policy_references=["EMERGENCY_REPAIR_POLICY"],
                scenario_tags=["emergency", "maintenance", "response_time"],
                jurisdiction_specific=False,
                last_updated=datetime(2023, 6, 1)
            ),
            FAQEntry(
                id="FAQ_003",
                question="What is the proper procedure for collecting late rent?",
                answer_template="Follow {RENT_COLLECTION_PROCEDURE}: 1) Rent due 1st, 2) Grace period through 5th, 3) Late fee (5%) on 6th, 4) Written notice after 10 days, 5) Begin eviction proceedings per state law after proper notice period.",
                policy_references=["RENT_COLLECTION_PROCEDURE"],
                scenario_tags=["rent", "collection", "late_payment"],
                jurisdiction_specific=True,
                last_updated=datetime(2023, 1, 1)
            )
        ]
        
        for faq in sample_faqs:
            self.faqs[faq.id] = faq
    
    def search_faqs(self, query: str, tags: Optional[List[str]] = None, 
                   jurisdiction: Optional[str] = None) -> List[FAQEntry]:
        """Search FAQs by query and optional filters"""
        results = []
        query_lower = query.lower()
        
        for faq in self.faqs.values():
            # Text search
            if query_lower in faq.question.lower() or query_lower in faq.answer_template.lower():
                # Tag filtering
                if tags and not any(tag in faq.scenario_tags for tag in tags):
                    continue
                    
                # Jurisdiction filtering
                if jurisdiction and faq.jurisdiction_specific:
                    # Would check specific jurisdiction requirements here
                    pass
                    
                results.append(faq)
        
        return results
    
    def get_policy_details(self, policy_id: str) -> Optional[PolicyDocument]:
        """Get full policy document by ID"""
        return self.policies.get(policy_id)
    
    def format_faq_response(self, faq: FAQEntry, jurisdiction: Optional[str] = None) -> str:
        """Format FAQ answer with policy references expanded"""
        answer = faq.answer_template
        
        # Replace policy references with links/details
        for policy_id in faq.policy_references:
            if policy_id in self.policies:
                policy = self.policies[policy_id]
                replacement = f"[{policy.title}]"
                if policy.source_url:
                    replacement += f" ({policy.source_url})"
                answer = answer.replace(f"{{{policy_id}}}", replacement)
        
        # Add jurisdiction-specific notes if applicable
        if jurisdiction and faq.jurisdiction_specific:
            answer += f"\n\nNote: This answer is based on {jurisdiction} regulations. Local laws may vary."
        
        return answer


class WillowManagerIntegration:
    """Integrates Manager FAQ system with Willow's response generation"""
    
    def __init__(self, faq_system: ManagerFAQSystem):
        self.faq_system = faq_system
        self.context_analyzer = ContextAnalyzer()
    
    def enhance_response_with_policy(self, 
                                   willow_response: Dict,
                                   scenario_tags: List[str],
                                   jurisdiction: Optional[str] = None) -> Dict:
        """Enhance Willow's response with relevant policy information"""
        
        # Search for relevant FAQs
        relevant_faqs = []
        for tag in scenario_tags:
            faqs = self.faq_system.search_faqs(tag, tags=scenario_tags, jurisdiction=jurisdiction)
            relevant_faqs.extend(faqs)
        
        # Remove duplicates
        seen = set()
        unique_faqs = []
        for faq in relevant_faqs:
            if faq.id not in seen:
                seen.add(faq.id)
                unique_faqs.append(faq)
        
        # Add manager guidance section
        if unique_faqs:
            willow_response["manager_guidance"] = {
                "relevant_policies": [],
                "quick_reference": [],
                "legal_considerations": []
            }
            
            for faq in unique_faqs[:3]:  # Limit to top 3 most relevant
                formatted_answer = self.faq_system.format_faq_response(faq, jurisdiction)
                
                willow_response["manager_guidance"]["quick_reference"].append({
                    "question": faq.question,
                    "answer": formatted_answer,
                    "tags": faq.scenario_tags
                })
                
                # Add policy references
                for policy_id in faq.policy_references:
                    policy = self.faq_system.get_policy_details(policy_id)
                    if policy and policy.id not in [p["id"] for p in willow_response["manager_guidance"]["relevant_policies"]]:
                        willow_response["manager_guidance"]["relevant_policies"].append({
                            "id": policy.id,
                            "title": policy.title,
                            "type": policy.type.value,
                            "key_points": policy.content[:200] + "..."
                        })
                        
                        if policy.type == PolicyType.LEGAL:
                            willow_response["manager_guidance"]["legal_considerations"].append(
                                f"{policy.title}: {policy.content[:150]}..."
                            )
        
        return willow_response


class ContextAnalyzer:
    """Analyzes conversation context to identify relevant policies"""
    
    def extract_scenario_tags(self, message: str, emotional_state: Dict) -> List[str]:
        """Extract relevant tags from user message and emotional state"""
        tags = []
        message_lower = message.lower()
        
        # Emergency indicators
        if any(word in message_lower for word in ["emergency", "urgent", "immediate", "flooding", "fire", "no heat", "no water"]):
            tags.append("emergency")
        
        # Maintenance issues
        if any(word in message_lower for word in ["broken", "repair", "fix", "maintenance", "not working"]):
            tags.append("maintenance")
        
        # Disability/accommodation
        if any(word in message_lower for word in ["disability", "wheelchair", "accommodation", "accessible"]):
            tags.append("accommodation")
            tags.append("disability")
        
        # Payment issues
        if any(word in message_lower for word in ["rent", "payment", "pay", "late", "eviction"]):
            tags.append("rent")
            tags.append("payment")
        
        # High emotional arousal might indicate emergency
        if emotional_state.get("arousal", 0) > 8:
            tags.append("emergency")
        
        return list(set(tags))  # Remove duplicates


# Example usage
def demonstrate_manager_faq():
    """Demonstrate the Manager FAQ system integration"""
    
    # Initialize systems
    faq_system = ManagerFAQSystem("policies.json", "faqs.json")
    integration = WillowManagerIntegration(faq_system)
    
    # Simulate a scenario that needs policy guidance
    scenarios = [
        {
            "message": "Tenant says they need wheelchair ramp installed",
            "emotional_state": {"arousal": 6, "capacity": 7},
            "willow_response": {
                "response": "I understand this accessibility need is important. Let me help coordinate the accommodation request process.",
                "tier": "tier_1"
            }
        },
        {
            "message": "Heat broken for 5 hours in winter, tenant threatening to sue",
            "emotional_state": {"arousal": 9, "capacity": 4},
            "willow_response": {
                "response": "This is an emergency. I'm dispatching heating repair immediately and documenting everything.",
                "tier": "tier_2"
            }
        }
    ]
    
    print("=== WILLOW MANAGER FAQ INTEGRATION DEMO ===\n")
    
    for i, scenario in enumerate(scenarios):
        print(f"--- Scenario {i+1} ---")
        print(f"Tenant Issue: {scenario['message']}")
        print(f"Willow Response: {scenario['willow_response']['response']}")
        
        # Extract tags and enhance response
        tags = integration.context_analyzer.extract_scenario_tags(
            scenario["message"], 
            scenario["emotional_state"]
        )
        
        enhanced_response = integration.enhance_response_with_policy(
            scenario["willow_response"],
            tags,
            jurisdiction="California"
        )
        
        if "manager_guidance" in enhanced_response:
            print("\n📋 MANAGER GUIDANCE:")
            
            # Show relevant policies
            print("\n🔍 Relevant Policies:")
            for policy in enhanced_response["manager_guidance"]["relevant_policies"]:
                print(f"  - {policy['title']} ({policy['type']})")
                print(f"    {policy['key_points']}")
            
            # Show quick reference
            print("\n❓ Quick Reference:")
            for ref in enhanced_response["manager_guidance"]["quick_reference"]:
                print(f"  Q: {ref['question']}")
                print(f"  A: {ref['answer'][:200]}...")
            
            # Show legal considerations
            if enhanced_response["manager_guidance"]["legal_considerations"]:
                print("\n⚖️ Legal Considerations:")
                for consideration in enhanced_response["manager_guidance"]["legal_considerations"]:
                    print(f"  - {consideration}")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    demonstrate_manager_faq()