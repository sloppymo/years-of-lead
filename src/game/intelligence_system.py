"""
Years of Lead - Intelligence System

This module manages intelligence gathering, information flow, and strategic awareness
for both the resistance and government forces.
"""

import random
import uuid
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger(__name__)

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
    """Database of intelligence events and analysis with comprehensive error handling"""
    
    def __init__(self):
        self.events: Dict[str, IntelligenceEvent] = {}
        self.analysis_reports: Dict[str, str] = {}
        self.patterns: List[Dict[str, Any]] = []
        self.threat_assessments: Dict[str, Dict[str, Any]] = {}
        logger.info("IntelligenceDatabase initialized")
    
    def add_event(self, event: IntelligenceEvent):
        """Add new intelligence event with validation"""
        try:
            if not isinstance(event, IntelligenceEvent):
                raise TypeError(f"Event must be IntelligenceEvent, got {type(event)}")
            
            if not event.id:
                raise ValueError("Event must have an ID")
            
            if event.id in self.events:
                logger.warning("Overwriting existing event with ID: %s", event.id)
            
            self.events[event.id] = event
            logger.info("Added intelligence event: %s (Type: %s, Priority: %s)", 
                       event.title, event.type.value, event.priority.value)
            
            self._update_analysis()
            
        except Exception as e:
            logger.error("Failed to add intelligence event: %s", str(e))
            raise
    
    def get_events_by_type(self, event_type: IntelligenceType) -> List[IntelligenceEvent]:
        """Get all events of a specific type with validation"""
        try:
            if not isinstance(event_type, IntelligenceType):
                if isinstance(event_type, str):
                    try:
                        event_type = IntelligenceType(event_type)
                    except ValueError:
                        raise ValueError(f"Invalid event type: {event_type}")
                else:
                    raise TypeError(f"Event type must be IntelligenceType enum, got {type(event_type)}")
            
            events = [event for event in self.events.values() if event.type == event_type]
            logger.debug("Retrieved %d events of type: %s", len(events), event_type.value)
            return events
            
        except Exception as e:
            logger.error("Failed to get events by type %s: %s", event_type, str(e))
            return []
    
    def get_events_by_priority(self, priority: IntelligencePriority) -> List[IntelligenceEvent]:
        """Get all events of a specific priority with validation"""
        try:
            if not isinstance(priority, IntelligencePriority):
                if isinstance(priority, str):
                    try:
                        priority = IntelligencePriority(priority)
                    except ValueError:
                        raise ValueError(f"Invalid priority: {priority}")
                else:
                    raise TypeError(f"Priority must be IntelligencePriority enum, got {type(priority)}")
            
            events = [event for event in self.events.values() if event.priority == priority]
            logger.debug("Retrieved %d events with priority: %s", len(events), priority.value)
            return events
            
        except Exception as e:
            logger.error("Failed to get events by priority %s: %s", priority, str(e))
            return []
    
    def get_recent_events(self, hours: int = 24) -> List[IntelligenceEvent]:
        """Get events from the last N hours with validation"""
        try:
            if not isinstance(hours, int):
                raise TypeError(f"Hours must be an integer, got {type(hours)}")
            if hours < 0:
                raise ValueError(f"Hours cannot be negative: {hours}")
            if hours > 168:  # Max 1 week
                logger.warning("Requesting events from more than 1 week ago: %d hours", hours)
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            events = [event for event in self.events.values() if event.timestamp > cutoff_time]
            logger.debug("Retrieved %d events from last %d hours", len(events), hours)
            return events
            
        except Exception as e:
            logger.error("Failed to get recent events: %s", str(e))
            return []
    
    def get_critical_events(self) -> List[IntelligenceEvent]:
        """Get all critical priority events"""
        return self.get_events_by_priority(IntelligencePriority.CRITICAL)
    
    def _update_analysis(self):
        """Update intelligence analysis and patterns with error handling"""
        try:
            logger.debug("Updating intelligence analysis with %d events", len(self.events))
            self._analyze_patterns()
            self._update_threat_assessments()
            self._generate_analysis_reports()
            logger.debug("Intelligence analysis updated successfully")
            
        except Exception as e:
            logger.error("Failed to update intelligence analysis: %s", str(e))
    
    def _analyze_patterns(self):
        """Analyze patterns in intelligence data with error handling"""
        try:
            self.patterns = []  # Reset patterns
            
            # Analyze government movements
            gov_events = self.get_events_by_type(IntelligenceType.GOVERNMENT_MOVEMENT)
            if len(gov_events) >= 3:
                self.patterns.append({
                    "type": "government_activity",
                    "description": "Increased government activity detected",
                    "confidence": min(0.8, len(gov_events) * 0.2),
                    "implications": ["Possible crackdown", "Increased surveillance", "Policy changes"],
                    "event_count": len(gov_events)
                })
                logger.info("Detected government activity pattern: %d events", len(gov_events))
            
            # Analyze security changes
            security_events = self.get_events_by_type(IntelligenceType.SECURITY_CHANGES)
            if len(security_events) >= 2:
                self.patterns.append({
                    "type": "security_escalation",
                    "description": "Security measures being enhanced",
                    "confidence": min(0.7, len(security_events) * 0.3),
                    "implications": ["Harder to operate", "Need for new tactics", "Increased risk"],
                    "event_count": len(security_events)
                })
                logger.info("Detected security escalation pattern: %d events", len(security_events))
            
            # Analyze economic data
            economic_events = self.get_events_by_type(IntelligenceType.ECONOMIC_DATA)
            if len(economic_events) >= 2:
                self.patterns.append({
                    "type": "economic_manipulation",
                    "description": "Economic manipulation detected",
                    "confidence": min(0.6, len(economic_events) * 0.25),
                    "implications": ["Financial pressure", "Resource scarcity", "Economic warfare"],
                    "event_count": len(economic_events)
                })
            
            logger.debug("Pattern analysis complete: %d patterns detected", len(self.patterns))
            
        except Exception as e:
            logger.error("Failed to analyze patterns: %s", str(e))
            self.patterns = []
    
    def _update_threat_assessments(self):
        """Update threat assessments based on intelligence with error handling"""
        try:
            # Calculate overall threat level
            critical_events = len(self.get_critical_events())
            high_priority_events = len(self.get_events_by_priority(IntelligencePriority.HIGH))
            medium_priority_events = len(self.get_events_by_priority(IntelligencePriority.MEDIUM))
            
            # Determine threat level
            if critical_events >= 2:
                threat_level = "EXTREME"
                threat_score = 9.0
            elif critical_events >= 1 or high_priority_events >= 3:
                threat_level = "HIGH"
                threat_score = 7.0
            elif high_priority_events >= 1 or medium_priority_events >= 5:
                threat_level = "MEDIUM"
                threat_score = 5.0
            else:
                threat_level = "LOW"
                threat_score = 2.0
            
            # Update threat assessment
            self.threat_assessments["overall"] = {
                "level": threat_level,
                "score": threat_score,
                "critical_events": critical_events,
                "high_priority_events": high_priority_events,
                "medium_priority_events": medium_priority_events,
                "total_events": len(self.events),
                "last_updated": datetime.now().isoformat()
            }
            
            logger.info("Threat assessment updated: %s (Score: %.1f)", threat_level, threat_score)
            
        except Exception as e:
            logger.error("Failed to update threat assessments: %s", str(e))
            self.threat_assessments["overall"] = {
                "level": "UNKNOWN",
                "score": 0.0,
                "error": str(e)
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
    """Intelligence event generator with comprehensive error handling"""
    
    def __init__(self):
        """Initialize intelligence generator"""
        self.event_templates = self._create_event_templates()
        logger.info("IntelligenceGenerator initialized with %d event types", len(self.event_templates))
    
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
        """
        Generate an intelligence event with comprehensive validation
        
        Args:
            event_type: Type of intelligence event
            location: Location where event occurred
            priority: Priority level of the event
            source: Source of the intelligence
            
        Returns:
            IntelligenceEvent object
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If input types are incorrect
        """
        try:
            # Validate inputs
            self._validate_event_inputs(event_type, location, priority, source)
            
            logger.info("Generating intelligence event: %s at %s (Priority: %s, Source: %s)", 
                       event_type.value, location, priority.value, source.value)
            
            # Get template for event type
            templates = self.event_templates.get(event_type, [])
            if not templates:
                raise ValueError(f"No templates available for event type: {event_type}")
            
            template = random.choice(templates)
            
            # Generate event data
            event_data = self._generate_event_data(template, location, priority, source)
            
            # Create event
            event = IntelligenceEvent(
                id=str(uuid.uuid4()),
                type=event_type,
                priority=priority,
                source=source,
                title=event_data["title"],
                description=event_data["description"],
                detailed_report=event_data["detailed_report"],
                location=location,
                timestamp=datetime.now(),
                reliability=event_data["reliability"],
                urgency=event_data["urgency"],
                mechanical_effects=event_data["mechanical_effects"],
                narrative_consequences=event_data["narrative_consequences"],
                action_opportunities=event_data["action_opportunities"]
            )
            
            logger.info("Generated intelligence event: %s (ID: %s, Reliability: %.1f%%)", 
                       event.title, event.id, event.reliability * 100)
            
            return event
            
        except Exception as e:
            logger.error("Failed to generate intelligence event: %s", str(e))
            raise
    
    def _validate_event_inputs(self, event_type: IntelligenceType, location: str, 
                             priority: IntelligencePriority, source: IntelligenceSource) -> None:
        """Validate all event generation inputs"""
        # Validate event type
        if not isinstance(event_type, IntelligenceType):
            if isinstance(event_type, str):
                try:
                    event_type = IntelligenceType(event_type)
                except ValueError:
                    raise ValueError(f"Invalid event type: {event_type}")
            else:
                raise TypeError(f"Event type must be IntelligenceType enum, got {type(event_type)}")
        
        # Validate location
        if not isinstance(location, str):
            raise TypeError(f"Location must be a string, got {type(location)}")
        if not location or not location.strip():
            raise ValueError("Location cannot be empty")
        if len(location) > 100:
            raise ValueError("Location too long (max 100 characters)")
        
        # Validate priority
        if not isinstance(priority, IntelligencePriority):
            if isinstance(priority, str):
                try:
                    priority = IntelligencePriority(priority)
                except ValueError:
                    raise ValueError(f"Invalid priority: {priority}")
            else:
                raise TypeError(f"Priority must be IntelligencePriority enum, got {type(priority)}")
        
        # Validate source
        if not isinstance(source, IntelligenceSource):
            if isinstance(source, str):
                try:
                    source = IntelligenceSource(source)
                except ValueError:
                    raise ValueError(f"Invalid source: {source}")
            else:
                raise TypeError(f"Source must be IntelligenceSource enum, got {type(source)}")
        
        logger.debug("Event input validation passed for: %s at %s", event_type.value, location)
    
    def _generate_event_data(self, template: Dict[str, Any], location: str, 
                           priority: IntelligencePriority, source: IntelligenceSource) -> Dict[str, Any]:
        """Generate event data from template with error handling"""
        try:
            # Calculate reliability based on source
            source_reliability = {
                IntelligenceSource.INFILTRATOR: 0.9,
                IntelligenceSource.INFORMANT: 0.7,
                IntelligenceSource.SURVEILLANCE: 0.8,
                IntelligenceSource.HACKING: 0.6,
                IntelligenceSource.INTERCEPTION: 0.7,
                IntelligenceSource.OBSERVATION: 0.5,
                IntelligenceSource.INTERROGATION: 0.8,
                IntelligenceSource.DOCUMENT_THEFT: 0.9
            }
            
            base_reliability = source_reliability.get(source, 0.5)
            reliability = base_reliability + random.uniform(-0.1, 0.1)
            reliability = max(0.1, min(1.0, reliability))
            
            # Calculate urgency based on priority
            urgency_map = {
                IntelligencePriority.LOW: (1, 3),
                IntelligencePriority.MEDIUM: (4, 6),
                IntelligencePriority.HIGH: (7, 8),
                IntelligencePriority.CRITICAL: (9, 10)
            }
            
            urgency_range = urgency_map.get(priority, (5, 5))
            urgency = random.randint(urgency_range[0], urgency_range[1])
            
            # Generate title and description
            title = template["title"].format(location=location)
            description = template["description"].format(location=location)
            
            # Generate detailed report
            detailed_report = self._generate_detailed_report(template, location, priority)
            
            # Generate mechanical effects
            mechanical_effects = self._generate_mechanical_effects(template, priority)
            
            # Generate narrative consequences
            narrative_consequences = self._generate_narrative_consequences(template, location)
            
            # Generate action opportunities
            action_opportunities = self._generate_action_opportunities(template, priority)
            
            return {
                "title": title,
                "description": description,
                "detailed_report": detailed_report,
                "reliability": reliability,
                "urgency": urgency,
                "mechanical_effects": mechanical_effects,
                "narrative_consequences": narrative_consequences,
                "action_opportunities": action_opportunities
            }
            
        except Exception as e:
            logger.error("Failed to generate event data: %s", str(e))
            # Return default data on error
            return {
                "title": f"Intelligence Event at {location}",
                "description": "An intelligence event occurred.",
                "detailed_report": "Detailed information unavailable.",
                "reliability": 0.5,
                "urgency": 5,
                "mechanical_effects": {},
                "narrative_consequences": ["Event occurred"],
                "action_opportunities": ["Monitor situation"]
            }
    
    def _generate_detailed_report(self, template: Dict[str, Any], location: str, 
                                priority: IntelligencePriority) -> str:
        """Generate detailed intelligence report"""
        try:
            base_report = template.get("detailed_report", f"Intelligence report from {location}")
            
            # Add priority-specific details
            priority_details = {
                IntelligencePriority.LOW: "Low priority information.",
                IntelligencePriority.MEDIUM: "Moderate priority intelligence.",
                IntelligencePriority.HIGH: "High priority intelligence requiring immediate attention.",
                IntelligencePriority.CRITICAL: "CRITICAL intelligence requiring immediate action."
            }
            
            priority_text = priority_details.get(priority, "Priority level unknown.")
            
            # Add location-specific details
            location_details = f"Location: {location}. "
            
            return f"{base_report} {location_details} {priority_text}"
            
        except Exception as e:
            logger.error("Failed to generate detailed report: %s", str(e))
            return f"Intelligence report from {location}. Priority: {priority.value}."
    
    def _generate_mechanical_effects(self, template: Dict[str, Any], 
                                   priority: IntelligencePriority) -> Dict[str, Any]:
        """Generate mechanical effects for the intelligence event"""
        try:
            effects = template.get("mechanical_effects", {})
            
            # Add priority-based effects
            if priority == IntelligencePriority.CRITICAL:
                effects["threat_level"] = "increased"
                effects["security_alert"] = "high"
            elif priority == IntelligencePriority.HIGH:
                effects["threat_level"] = "moderate"
                effects["security_alert"] = "medium"
            elif priority == IntelligencePriority.MEDIUM:
                effects["threat_level"] = "low"
                effects["security_alert"] = "low"
            else:  # LOW
                effects["threat_level"] = "minimal"
                effects["security_alert"] = "none"
            
            return effects
            
        except Exception as e:
            logger.error("Failed to generate mechanical effects: %s", str(e))
            return {"threat_level": "unknown"}
    
    def _generate_narrative_consequences(self, template: Dict[str, Any], location: str) -> List[str]:
        """Generate narrative consequences for the intelligence event"""
        try:
            consequences = template.get("narrative_consequences", [])
            
            # Add location-specific consequences
            location_consequences = [
                f"Activity detected in {location}",
                f"Potential threat in {location}",
                f"Surveillance increased in {location}"
            ]
            
            consequences.extend(location_consequences)
            return consequences
            
        except Exception as e:
            logger.error("Failed to generate narrative consequences: %s", str(e))
            return [f"Event occurred in {location}"]
    
    def _generate_action_opportunities(self, template: Dict[str, Any], 
                                     priority: IntelligencePriority) -> List[str]:
        """Generate action opportunities based on intelligence"""
        try:
            opportunities = template.get("action_opportunities", [])
            
            # Add priority-based opportunities
            if priority == IntelligencePriority.CRITICAL:
                opportunities.extend([
                    "Immediate response required",
                    "Alert all operatives",
                    "Prepare emergency protocols"
                ])
            elif priority == IntelligencePriority.HIGH:
                opportunities.extend([
                    "Increase surveillance",
                    "Prepare countermeasures",
                    "Alert leadership"
                ])
            elif priority == IntelligencePriority.MEDIUM:
                opportunities.extend([
                    "Monitor situation",
                    "Gather additional intelligence",
                    "Prepare contingency plans"
                ])
            else:  # LOW
                opportunities.extend([
                    "Continue monitoring",
                    "Document for future reference"
                ])
            
            return opportunities
            
        except Exception as e:
            logger.error("Failed to generate action opportunities: %s", str(e))
            return ["Monitor situation"]


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