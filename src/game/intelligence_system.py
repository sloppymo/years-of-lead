"""
Years of Lead - Intelligence System

Comprehensive intelligence gathering and analysis system with detailed
event information, narrative consequences, and mechanical effects.
"""

import random
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class IntelligenceType(Enum):
    """Types of intelligence events"""
    GOVERNMENT_MOVEMENT = "government_movement"
    SECURITY_CHANGES = "security_changes"
    ECONOMIC_DATA = "economic_data"
    SOCIAL_UNREST = "social_unrest"
    MILITARY_ACTIVITY = "military_activity"
    CORPORATE_ACTIVITY = "corporate_activity"
    MEDIA_ANALYSIS = "media_analysis"
    INFRASTRUCTURE = "infrastructure"
    PERSONNEL_MOVEMENTS = "personnel_movements"
    COMMUNICATIONS = "communications"


class IntelligencePriority(Enum):
    """Priority levels for intelligence"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntelligenceSource(Enum):
    """Sources of intelligence"""
    INFILTRATOR = "infiltrator"
    INFORMANT = "informant"
    SURVEILLANCE = "surveillance"
    HACKING = "hacking"
    INTERCEPTION = "interception"
    OBSERVATION = "observation"
    INTERROGATION = "interrogation"
    DOCUMENT_THEFT = "document_theft"


@dataclass
class IntelligenceEvent:
    """Individual intelligence event"""
    id: str
    type: IntelligenceType
    priority: IntelligencePriority
    source: IntelligenceSource
    title: str
    description: str
    detailed_report: str
    location: str
    timestamp: datetime
    reliability: float  # 0.0 to 1.0
    urgency: int  # 1-10
    
    # Mechanical effects
    mechanical_effects: Dict[str, Any] = field(default_factory=dict)
    
    # Narrative consequences
    narrative_consequences: List[str] = field(default_factory=list)
    
    # Related events
    related_events: List[str] = field(default_factory=list)
    
    # Action opportunities
    action_opportunities: List[str] = field(default_factory=list)
    
    def get_full_report(self) -> str:
        """Get comprehensive intelligence report"""
        report = f"""
{'=' * 60}
INTELLIGENCE REPORT: {self.title.upper()}
{'=' * 60}

PRIORITY: {self.priority.value.upper()}
TYPE: {self.type.value.replace('_', ' ').title()}
SOURCE: {self.source.value.replace('_', ' ').title()}
LOCATION: {self.location}
TIMESTAMP: {self.timestamp.strftime('%Y-%m-%d %H:%M')}
RELIABILITY: {self.reliability:.1%}
URGENCY: {self.urgency}/10

DESCRIPTION:
{self.description}

DETAILED REPORT:
{self.detailed_report}

MECHANICAL EFFECTS:
"""
        
        for effect, value in self.mechanical_effects.items():
            report += f"  • {effect.replace('_', ' ').title()}: {value}\n"
        
        report += f"""
NARRATIVE CONSEQUENCES:
"""
        
        for consequence in self.narrative_consequences:
            report += f"  • {consequence}\n"
        
        if self.action_opportunities:
            report += f"""
ACTION OPPORTUNITIES:
"""
            for opportunity in self.action_opportunities:
                report += f"  • {opportunity}\n"
        
        if self.related_events:
            report += f"""
RELATED EVENTS:
"""
            for event in self.related_events:
                report += f"  • {event}\n"
        
        return report
    
    def get_summary(self) -> str:
        """Get brief summary of the intelligence"""
        return f"[{self.priority.value.upper()}] {self.title} - {self.location} ({self.reliability:.1%} reliability)"


class IntelligenceDatabase:
    """Database of intelligence events and analysis"""
    
    def __init__(self):
        self.events: Dict[str, IntelligenceEvent] = {}
        self.analysis_reports: Dict[str, str] = {}
        self.patterns: List[Dict[str, Any]] = []
        self.threat_assessments: Dict[str, Dict[str, Any]] = {}
    
    def add_event(self, event: IntelligenceEvent):
        """Add new intelligence event"""
        self.events[event.id] = event
        self._update_analysis()
    
    def get_events_by_type(self, event_type: IntelligenceType) -> List[IntelligenceEvent]:
        """Get all events of a specific type"""
        return [event for event in self.events.values() if event.type == event_type]
    
    def get_events_by_priority(self, priority: IntelligencePriority) -> List[IntelligenceEvent]:
        """Get all events of a specific priority"""
        return [event for event in self.events.values() if event.priority == priority]
    
    def get_recent_events(self, hours: int = 24) -> List[IntelligenceEvent]:
        """Get events from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [event for event in self.events.values() if event.timestamp > cutoff_time]
    
    def get_critical_events(self) -> List[IntelligenceEvent]:
        """Get all critical priority events"""
        return self.get_events_by_priority(IntelligencePriority.CRITICAL)
    
    def _update_analysis(self):
        """Update intelligence analysis and patterns"""
        self._analyze_patterns()
        self._update_threat_assessments()
        self._generate_analysis_reports()
    
    def _analyze_patterns(self):
        """Analyze patterns in intelligence data"""
        # Analyze government movements
        gov_events = self.get_events_by_type(IntelligenceType.GOVERNMENT_MOVEMENT)
        if len(gov_events) >= 3:
            self.patterns.append({
                "type": "government_activity",
                "description": "Increased government activity detected",
                "confidence": 0.8,
                "implications": ["Possible crackdown", "Increased surveillance", "Policy changes"]
            })
        
        # Analyze security changes
        security_events = self.get_events_by_type(IntelligenceType.SECURITY_CHANGES)
        if len(security_events) >= 2:
            self.patterns.append({
                "type": "security_escalation",
                "description": "Security measures being enhanced",
                "confidence": 0.7,
                "implications": ["Harder to operate", "Need for new tactics", "Increased risk"]
            })
    
    def _update_threat_assessments(self):
        """Update threat assessments based on intelligence"""
        # Calculate overall threat level
        critical_events = len(self.get_critical_events())
        high_priority_events = len(self.get_events_by_priority(IntelligencePriority.HIGH))
        
        if critical_events >= 2:
            threat_level = "EXTREME"
        elif critical_events >= 1 or high_priority_events >= 3:
            threat_level = "HIGH"
        elif high_priority_events >= 1:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        self.threat_assessments["overall"] = {
            "level": threat_level,
            "critical_events": critical_events,
            "high_priority_events": high_priority_events,
            "last_updated": datetime.now()
        }
    
    def _generate_analysis_reports(self):
        """Generate analysis reports"""
        # Overall situation report
        situation_report = self._generate_situation_report()
        self.analysis_reports["situation"] = situation_report
        
        # Threat assessment report
        threat_report = self._generate_threat_report()
        self.analysis_reports["threat"] = threat_report
    
    def _generate_situation_report(self) -> str:
        """Generate overall situation report"""
        report = f"""
{'=' * 60}
SITUATION REPORT
{'=' * 60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

OVERALL ASSESSMENT:
"""
        
        total_events = len(self.events)
        critical_events = len(self.get_critical_events())
        high_events = len(self.get_events_by_priority(IntelligencePriority.HIGH))
        
        report += f"Total Intelligence Events: {total_events}\n"
        report += f"Critical Priority Events: {critical_events}\n"
        report += f"High Priority Events: {high_events}\n"
        
        if critical_events > 0:
            report += "\n⚠️  CRITICAL SITUATION: Immediate attention required!\n"
        elif high_events > 0:
            report += "\n⚠️  HIGH ALERT: Situation requires monitoring.\n"
        else:
            report += "\n✅ Situation appears stable.\n"
        
        # Recent activity
        recent_events = self.get_recent_events(24)
        if recent_events:
            report += f"\nRECENT ACTIVITY (Last 24 Hours):\n"
            for event in recent_events[:5]:  # Show top 5
                report += f"  • {event.get_summary()}\n"
        
        # Patterns
        if self.patterns:
            report += f"\nDETECTED PATTERNS:\n"
            for pattern in self.patterns:
                report += f"  • {pattern['description']} (Confidence: {pattern['confidence']:.1%})\n"
                for implication in pattern['implications']:
                    report += f"    - {implication}\n"
        
        return report
    
    def _generate_threat_report(self) -> str:
        """Generate threat assessment report"""
        threat_assessment = self.threat_assessments.get("overall", {})
        
        report = f"""
{'=' * 60}
THREAT ASSESSMENT
{'=' * 60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

THREAT LEVEL: {threat_assessment.get('level', 'UNKNOWN')}
Critical Events: {threat_assessment.get('critical_events', 0)}
High Priority Events: {threat_assessment.get('high_priority_events', 0)}

RECOMMENDATIONS:
"""
        
        threat_level = threat_assessment.get('level', 'LOW')
        
        if threat_level == "EXTREME":
            report += """
• IMMEDIATE ACTION REQUIRED
• Suspend all non-essential operations
• Activate emergency protocols
• Prepare for potential crackdown
• Consider evacuation of key personnel
"""
        elif threat_level == "HIGH":
            report += """
• Exercise extreme caution
• Increase operational security
• Limit high-risk activities
• Monitor all communications
• Prepare contingency plans
"""
        elif threat_level == "MEDIUM":
            report += """
• Maintain normal operations with caution
• Review security procedures
• Monitor situation closely
• Prepare for potential escalation
"""
        else:
            report += """
• Continue normal operations
• Maintain standard security
• Monitor for changes
• Prepare for potential threats
"""
        
        return report


class IntelligenceGenerator:
    """Generate intelligence events procedurally"""
    
    def __init__(self):
        self.event_templates = self._create_event_templates()
    
    def _create_event_templates(self) -> Dict[IntelligenceType, List[Dict[str, Any]]]:
        """Create templates for different intelligence event types"""
        templates = {}
        
        # Government Movement Events
        templates[IntelligenceType.GOVERNMENT_MOVEMENT] = [
            {
                "title": "High-Level Government Meeting",
                "description": "Unusual activity detected at government headquarters",
                "detailed_report": "Multiple high-ranking officials have been observed entering the main government building. The meeting appears to be unscheduled and involves officials from multiple departments including security, economic, and military sectors.",
                "mechanical_effects": {"government_alertness": +2, "surveillance_level": +1},
                "narrative_consequences": [
                    "Possible policy changes being discussed",
                    "Increased government coordination",
                    "Potential crackdown on resistance activities"
                ],
                "action_opportunities": [
                    "Attempt to infiltrate the meeting",
                    "Monitor communications during the meeting",
                    "Prepare for potential policy changes"
                ]
            },
            {
                "title": "Security Force Mobilization",
                "description": "Large-scale movement of security forces detected",
                "detailed_report": "Multiple units of police and military forces have been observed moving through the city. The movement appears coordinated and involves both regular patrol units and specialized response teams.",
                "mechanical_effects": {"security_presence": +3, "heat_level": +2},
                "narrative_consequences": [
                    "Possible large-scale operation planned",
                    "Increased risk for resistance activities",
                    "Potential for civilian casualties"
                ],
                "action_opportunities": [
                    "Track the movement of forces",
                    "Warn resistance cells in affected areas",
                    "Prepare defensive measures"
                ]
            }
        ]
        
        # Security Changes Events
        templates[IntelligenceType.SECURITY_CHANGES] = [
            {
                "title": "New Surveillance System Installation",
                "description": "Advanced surveillance equipment being installed",
                "detailed_report": "Work crews have been observed installing new surveillance equipment in key areas. The equipment appears to be advanced facial recognition and tracking systems, significantly increasing the government's monitoring capabilities.",
                "mechanical_effects": {"surveillance_level": +2, "stealth_difficulty": +1},
                "narrative_consequences": [
                    "Increased difficulty in maintaining anonymity",
                    "More sophisticated tracking of resistance members",
                    "Potential for mass surveillance abuse"
                ],
                "action_opportunities": [
                    "Attempt to sabotage the installation",
                    "Develop counter-surveillance techniques",
                    "Train operatives in new evasion methods"
                ]
            },
            {
                "title": "Checkpoint System Expansion",
                "description": "New security checkpoints being established",
                "detailed_report": "Additional security checkpoints are being established throughout the city. The new checkpoints include advanced scanning equipment and are staffed by both police and military personnel.",
                "mechanical_effects": {"movement_restriction": +2, "heat_level": +1},
                "narrative_consequences": [
                    "Increased difficulty in moving operatives",
                    "More thorough searches of civilians",
                    "Potential for mass arrests"
                ],
                "action_opportunities": [
                    "Map the new checkpoint locations",
                    "Develop bypass routes",
                    "Train operatives in checkpoint evasion"
                ]
            }
        ]
        
        # Economic Data Events
        templates[IntelligenceType.ECONOMIC_DATA] = [
            {
                "title": "Currency Manipulation Detected",
                "description": "Government manipulating currency exchange rates",
                "detailed_report": "Analysis of financial data reveals systematic manipulation of currency exchange rates. The government appears to be artificially inflating the value of the national currency while suppressing alternative currencies.",
                "mechanical_effects": {"funding_difficulty": +1, "black_market_value": +2},
                "narrative_consequences": [
                    "Increased economic pressure on civilians",
                    "Black market becoming more valuable",
                    "Potential for economic collapse"
                ],
                "action_opportunities": [
                    "Establish alternative currency networks",
                    "Exploit black market opportunities",
                    "Use economic instability for recruitment"
                ]
            }
        ]
        
        # Social Unrest Events
        templates[IntelligenceType.SOCIAL_UNREST] = [
            {
                "title": "Protest Movement Growing",
                "description": "Large-scale protests spreading across the city",
                "detailed_report": "Civilian protests have been growing in size and frequency. The protests appear to be spontaneous and involve diverse groups including workers, students, and religious organizations. Government response has been increasingly violent.",
                "mechanical_effects": {"public_support": +2, "government_repression": +1},
                "narrative_consequences": [
                    "Increased public support for resistance",
                    "Government becoming more repressive",
                    "Potential for mass uprising"
                ],
                "action_opportunities": [
                    "Support and coordinate with protesters",
                    "Use protests as cover for operations",
                    "Recruit from protest movements"
                ]
            }
        ]
        
        # Military Activity Events
        templates[IntelligenceType.MILITARY_ACTIVITY] = [
            {
                "title": "Military Equipment Movement",
                "description": "Heavy military equipment being transported",
                "detailed_report": "Large convoys of military vehicles have been observed moving through the city. The convoys include armored vehicles, artillery pieces, and specialized equipment. The movement appears to be part of a larger military operation.",
                "mechanical_effects": {"military_presence": +3, "combat_difficulty": +2},
                "narrative_consequences": [
                    "Possible military crackdown planned",
                    "Increased firepower available to government",
                    "Potential for urban warfare"
                ],
                "action_opportunities": [
                    "Track military movements",
                    "Prepare for potential military action",
                    "Develop anti-armor capabilities"
                ]
            }
        ]
        
        return templates
    
    def generate_event(self, event_type: IntelligenceType, location: str, 
                      priority: IntelligencePriority = IntelligencePriority.MEDIUM,
                      source: IntelligenceSource = IntelligenceSource.OBSERVATION) -> IntelligenceEvent:
        """Generate a new intelligence event"""
        templates = self.event_templates.get(event_type, [])
        
        if not templates:
            # Create a generic template
            template = {
                "title": f"{event_type.value.replace('_', ' ').title()} Event",
                "description": f"Intelligence event of type {event_type.value}",
                "detailed_report": f"Detailed report of {event_type.value} activity in {location}",
                "mechanical_effects": {},
                "narrative_consequences": [],
                "action_opportunities": []
            }
        else:
            template = random.choice(templates)
        
        # Adjust reliability based on source
        reliability = {
            IntelligenceSource.INFILTRATOR: 0.9,
            IntelligenceSource.INFORMANT: 0.7,
            IntelligenceSource.SURVEILLANCE: 0.8,
            IntelligenceSource.HACKING: 0.6,
            IntelligenceSource.INTERCEPTION: 0.8,
            IntelligenceSource.OBSERVATION: 0.5,
            IntelligenceSource.INTERROGATION: 0.4,
            IntelligenceSource.DOCUMENT_THEFT: 0.9
        }.get(source, 0.5)
        
        # Add some randomness
        reliability += random.uniform(-0.1, 0.1)
        reliability = max(0.1, min(1.0, reliability))
        
        # Calculate urgency based on priority
        urgency = {
            IntelligencePriority.LOW: random.randint(1, 3),
            IntelligencePriority.MEDIUM: random.randint(4, 6),
            IntelligencePriority.HIGH: random.randint(7, 8),
            IntelligencePriority.CRITICAL: random.randint(9, 10)
        }.get(priority, 5)
        
        event = IntelligenceEvent(
            id=str(uuid.uuid4()),
            type=event_type,
            priority=priority,
            source=source,
            title=template["title"],
            description=template["description"],
            detailed_report=template["detailed_report"],
            location=location,
            timestamp=datetime.now(),
            reliability=reliability,
            urgency=urgency,
            mechanical_effects=template["mechanical_effects"],
            narrative_consequences=template["narrative_consequences"],
            action_opportunities=template["action_opportunities"]
        )
        
        return event


class IntelligenceUI:
    """User interface for intelligence system"""
    
    def __init__(self, database: IntelligenceDatabase):
        self.database = database
        self.generator = IntelligenceGenerator()
    
    def display_intelligence_menu(self):
        """Display main intelligence menu"""
        while True:
            print("\n" + "=" * 60)
            print("INTELLIGENCE CENTER")
            print("=" * 60)
            print("1. View Recent Intelligence")
            print("2. View Critical Events")
            print("3. View Events by Type")
            print("4. View Situation Report")
            print("5. View Threat Assessment")
            print("6. Generate New Intelligence")
            print("7. Back to Main Menu")
            
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == "1":
                self.view_recent_intelligence()
            elif choice == "2":
                self.view_critical_events()
            elif choice == "3":
                self.view_events_by_type()
            elif choice == "4":
                self.view_situation_report()
            elif choice == "5":
                self.view_threat_assessment()
            elif choice == "6":
                self.generate_new_intelligence()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def view_recent_intelligence(self):
        """View recent intelligence events"""
        recent_events = self.database.get_recent_events(24)
        
        if not recent_events:
            print("\nNo recent intelligence events.")
            return
        
        print(f"\n{'=' * 60}")
        print("RECENT INTELLIGENCE (Last 24 Hours)")
        print(f"{'=' * 60}")
        
        for i, event in enumerate(recent_events, 1):
            print(f"\n{i}. {event.get_summary()}")
            print(f"   {event.description}")
        
        # Allow viewing detailed reports
        while True:
            choice = input(f"\nEnter event number to view details (1-{len(recent_events)}) or 0 to return: ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    break
                elif 1 <= choice_num <= len(recent_events):
                    event = recent_events[choice_num - 1]
                    print(event.get_full_report())
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid event number.")
            except ValueError:
                print("Please enter a valid number.")
    
    def view_critical_events(self):
        """View critical priority events"""
        critical_events = self.database.get_critical_events()
        
        if not critical_events:
            print("\nNo critical intelligence events.")
            return
        
        print(f"\n{'=' * 60}")
        print("CRITICAL INTELLIGENCE EVENTS")
        print(f"{'=' * 60}")
        
        for i, event in enumerate(critical_events, 1):
            print(f"\n{i}. {event.get_summary()}")
            print(f"   {event.description}")
        
        # Allow viewing detailed reports
        while True:
            choice = input(f"\nEnter event number to view details (1-{len(critical_events)}) or 0 to return: ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    break
                elif 1 <= choice_num <= len(critical_events):
                    event = critical_events[choice_num - 1]
                    print(event.get_full_report())
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid event number.")
            except ValueError:
                print("Please enter a valid number.")
    
    def view_events_by_type(self):
        """View events filtered by type"""
        print("\nSelect intelligence type:")
        for i, intel_type in enumerate(IntelligenceType, 1):
            print(f"{i}. {intel_type.value.replace('_', ' ').title()}")
        
        try:
            choice = int(input(f"\nEnter choice (1-{len(IntelligenceType)}): "))
            if 1 <= choice <= len(IntelligenceType):
                selected_type = list(IntelligenceType)[choice - 1]
                events = self.database.get_events_by_type(selected_type)
                
                if not events:
                    print(f"\nNo {selected_type.value} events found.")
                    return
                
                print(f"\n{'=' * 60}")
                print(f"{selected_type.value.replace('_', ' ').upper()} EVENTS")
                print(f"{'=' * 60}")
                
                for i, event in enumerate(events, 1):
                    print(f"\n{i}. {event.get_summary()}")
                    print(f"   {event.description}")
                
                # Allow viewing detailed reports
                while True:
                    detail_choice = input(f"\nEnter event number to view details (1-{len(events)}) or 0 to return: ")
                    try:
                        detail_num = int(detail_choice)
                        if detail_num == 0:
                            break
                        elif 1 <= detail_num <= len(events):
                            event = events[detail_num - 1]
                            print(event.get_full_report())
                            input("\nPress Enter to continue...")
                        else:
                            print("Invalid event number.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    
    def view_situation_report(self):
        """View situation report"""
        report = self.database.analysis_reports.get("situation", "No situation report available.")
        print(report)
        input("\nPress Enter to continue...")
    
    def view_threat_assessment(self):
        """View threat assessment"""
        report = self.database.analysis_reports.get("threat", "No threat assessment available.")
        print(report)
        input("\nPress Enter to continue...")
    
    def generate_new_intelligence(self):
        """Generate new intelligence event"""
        print("\nGenerate New Intelligence Event")
        print("-" * 40)
        
        # Select type
        print("Select intelligence type:")
        for i, intel_type in enumerate(IntelligenceType, 1):
            print(f"{i}. {intel_type.value.replace('_', ' ').title()}")
        
        try:
            type_choice = int(input(f"\nEnter type (1-{len(IntelligenceType)}): "))
            if not (1 <= type_choice <= len(IntelligenceType)):
                print("Invalid choice.")
                return
            
            selected_type = list(IntelligenceType)[type_choice - 1]
            
            # Select location
            locations = ["Government Quarter", "University District", "Industrial Zone", 
                        "Old Town Market", "Suburban Residential", "Downtown Commercial"]
            print("\nSelect location:")
            for i, location in enumerate(locations, 1):
                print(f"{i}. {location}")
            
            location_choice = int(input(f"\nEnter location (1-{len(locations)}): "))
            if not (1 <= location_choice <= len(locations)):
                print("Invalid choice.")
                return
            
            selected_location = locations[location_choice - 1]
            
            # Select priority
            print("\nSelect priority:")
            for i, priority in enumerate(IntelligencePriority, 1):
                print(f"{i}. {priority.value.title()}")
            
            priority_choice = int(input(f"\nEnter priority (1-{len(IntelligencePriority)}): "))
            if not (1 <= priority_choice <= len(IntelligencePriority)):
                print("Invalid choice.")
                return
            
            selected_priority = list(IntelligencePriority)[priority_choice - 1]
            
            # Generate event
            event = self.generator.generate_event(
                event_type=selected_type,
                location=selected_location,
                priority=selected_priority
            )
            
            # Add to database
            self.database.add_event(event)
            
            print(f"\n✅ New intelligence event generated: {event.title}")
            print(f"Priority: {event.priority.value.title()}")
            print(f"Location: {event.location}")
            print(f"Reliability: {event.reliability:.1%}")
            
            # Show full report
            show_report = input("\nView full report? (y/n): ").strip().lower()
            if show_report in ['y', 'yes']:
                print(event.get_full_report())
            
            input("\nPress Enter to continue...")
            
        except ValueError:
            print("Please enter valid numbers.") 