"""
Years of Lead - Enhanced Real-time Intelligence System

Phase 3: Intelligence Systems Enhancement
Implements continuous intelligence gathering, counter-intelligence operations,
and pattern analysis for actionable insights.
"""

import random
import uuid
import logging
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class IntelligenceSource(Enum):
    """Enhanced intelligence sources"""

    AGENT_NETWORK = "agent_network"
    SURVEILLANCE = "surveillance"
    SIGNAL_INTERCEPT = "signal_intercept"
    HUMAN_ASSETS = "human_assets"
    TECHNICAL_RECON = "technical_recon"
    SOCIAL_ENGINEERING = "social_engineering"
    DOCUMENT_THEFT = "document_theft"
    INTERROGATION = "interrogation"
    DEFECTOR_INTEL = "defector_intel"
    PATTERN_ANALYSIS = "pattern_analysis"


class ThreatLevel(Enum):
    """Threat assessment levels"""

    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    IMMINENT = "imminent"


class CounterIntelOp(Enum):
    """Counter-intelligence operation types"""

    SURVEILLANCE_DETECTION = "surveillance_detection"
    DISINFORMATION = "disinformation"
    DOUBLE_AGENT = "double_agent"
    SECURITY_AUDIT = "security_audit"
    COMMUNICATION_SECURITY = "communication_security"
    MOLE_HUNT = "mole_hunt"
    DECEPTION = "deception"


@dataclass
class RealTimeIntelEvent:
    """Real-time intelligence event"""

    id: str
    timestamp: datetime
    source: IntelligenceSource
    type: str
    location: str
    priority: str
    reliability: float
    content: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
    verification_status: str = "unverified"
    actionable: bool = False
    threat_level: ThreatLevel = ThreatLevel.LOW
    related_events: List[str] = field(default_factory=list)

    # Real-time tracking
    freshness: float = 1.0
    decay_rate: float = 0.1
    follow_up_required: bool = False

    def update_freshness(self, time_passed: float):
        """Update intelligence freshness over time"""
        self.freshness = max(0.0, self.freshness - (self.decay_rate * time_passed))

    def is_stale(self) -> bool:
        """Check if intelligence is too old to be useful"""
        return self.freshness < 0.2


@dataclass
class IntelligencePattern:
    """Detected intelligence pattern"""

    id: str
    pattern_type: str
    events_involved: List[str]
    confidence: float
    description: str
    implications: List[str]
    recommended_actions: List[str]
    threat_assessment: ThreatLevel
    created_timestamp: datetime
    last_updated: datetime


@dataclass
class CounterIntelligenceOperation:
    """Counter-intelligence operation"""

    id: str
    operation_type: CounterIntelOp
    target: str  # What/who is being protected
    status: str  # "active", "completed", "failed"
    effectiveness: float
    resources_committed: Dict[str, int]
    duration: int  # Turns
    success_probability: float
    discovered_threats: List[str] = field(default_factory=list)
    cost: int = 0


class EnhancedIntelligenceSystem:
    """Enhanced real-time intelligence system"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.real_time_events: List[RealTimeIntelEvent] = []
        self.intelligence_patterns: List[IntelligencePattern] = []
        self.counter_intel_ops: List[CounterIntelligenceOperation] = []

        # System parameters
        self.max_events_stored = 100
        self.pattern_detection_threshold = 3
        self.counter_intel_budget = 1000
        self.threat_escalation_threshold = 0.7

        # Tracking systems
        self.source_reliability: Dict[IntelligenceSource, float] = {}
        self.location_threat_levels: Dict[str, ThreatLevel] = {}
        self.agent_intel_performance: Dict[str, Dict[str, Any]] = {}

        # Real-time queues
        self.incoming_intelligence: List[RealTimeIntelEvent] = []
        self.priority_alerts: List[Dict[str, Any]] = []
        self.actionable_intelligence: List[RealTimeIntelEvent] = []

        self._initialize_baseline_data()

    def _initialize_baseline_data(self):
        """Initialize baseline intelligence data"""
        # Initialize source reliability
        for source in IntelligenceSource:
            self.source_reliability[source] = random.uniform(0.6, 0.9)

        # Initialize location threat levels
        if hasattr(self.game_state, "locations"):
            for location_id in self.game_state.locations.keys():
                self.location_threat_levels[location_id] = ThreatLevel.LOW

    def process_real_time_intelligence(self) -> Dict[str, Any]:
        """Process real-time intelligence gathering and analysis"""
        results = {
            "new_intelligence": [],
            "patterns_detected": [],
            "threat_assessments": {},
            "counter_intel_results": [],
            "actionable_intel": [],
            "priority_alerts": [],
        }

        # Generate new intelligence from active sources
        new_intel = self._generate_continuous_intelligence()

        # Add new intelligence to the system
        for event in new_intel:
            self.real_time_events.append(event)

        # Limit stored events to max capacity
        if len(self.real_time_events) > self.max_events_stored:
            self.real_time_events = self.real_time_events[-self.max_events_stored :]

        results["new_intelligence"] = new_intel

        # Update existing intelligence freshness
        self._update_intelligence_freshness()

        # Perform pattern analysis
        new_patterns = self._perform_pattern_analysis()
        results["patterns_detected"] = new_patterns

        # Update threat assessments
        threat_updates = self._update_threat_assessments()
        results["threat_assessments"] = threat_updates

        # Process counter-intelligence operations
        counter_results = self._process_counter_intelligence()
        results["counter_intel_results"] = counter_results

        # Identify actionable intelligence
        actionable = self._identify_actionable_intelligence()
        results["actionable_intel"] = actionable

        # Generate priority alerts
        alerts = self._generate_priority_alerts()
        results["priority_alerts"] = alerts

        return results

    def _generate_continuous_intelligence(self) -> List[RealTimeIntelEvent]:
        """Generate continuous intelligence from various sources"""
        new_intel = []

        # Agent network intelligence
        agent_intel = self._generate_agent_network_intel()
        new_intel.extend(agent_intel)

        # Technical surveillance
        tech_intel = self._generate_technical_intelligence()
        new_intel.extend(tech_intel)

        # Human assets intelligence
        human_intel = self._generate_human_assets_intel()
        new_intel.extend(human_intel)

        # Signal intercepts
        signal_intel = self._generate_signal_intelligence()
        new_intel.extend(signal_intel)

        return new_intel

    def _generate_agent_network_intel(self) -> List[RealTimeIntelEvent]:
        """Generate intelligence from agent network"""
        intel_events = []

        if not hasattr(self.game_state, "agents"):
            return intel_events

        # Active agents can generate intelligence
        active_agents = [
            a for a in self.game_state.agents.values() if a.status == "active"
        ]

        for agent in active_agents:
            # Check if agent generates intelligence this turn
            intel_chance = 0.3  # Base 30% chance

            # Modify based on agent skills
            if hasattr(agent, "skills") and "intelligence" in agent.skills:
                skill_level = agent.skills["intelligence"].level
                intel_chance += (skill_level - 2) * 0.1

            # Modify based on emotional state
            if hasattr(agent, "emotional_state"):
                # Fear reduces intelligence gathering
                fear_penalty = getattr(agent.emotional_state, "fear", 0) * 0.2
                intel_chance -= fear_penalty

                # Anticipation increases it
                anticipation_bonus = (
                    getattr(agent.emotional_state, "anticipation", 0) * 0.1
                )
                intel_chance += anticipation_bonus

            if random.random() < intel_chance:
                intel_event = self._create_agent_intel_event(agent)
                if intel_event:
                    intel_events.append(intel_event)

        return intel_events

    def _create_agent_intel_event(self, agent) -> Optional[RealTimeIntelEvent]:
        """Create intelligence event from agent observation"""

        intel_types = [
            ("government_movement", "Government forces observed moving through area"),
            ("security_change", "New security measures detected at target location"),
            ("personnel_change", "Key personnel movements noted"),
            ("communication_pattern", "Unusual communication patterns observed"),
            ("resource_movement", "Strategic resources being relocated"),
            ("civilian_sentiment", "Public sentiment analysis from local contacts"),
        ]

        intel_type, base_description = random.choice(intel_types)

        # Determine reliability based on agent's track record
        base_reliability = 0.7
        if agent.id in self.agent_intel_performance:
            performance = self.agent_intel_performance[agent.id]
            success_rate = performance.get("success_rate", 0.7)
            base_reliability = success_rate

        # Add some randomness
        reliability = max(0.1, min(1.0, base_reliability + random.uniform(-0.2, 0.2)))

        event = RealTimeIntelEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source=IntelligenceSource.AGENT_NETWORK,
            type=intel_type,
            location=agent.location_id,
            priority="medium",
            reliability=reliability,
            content=f"{agent.name} reports: {base_description}",
            raw_data={
                "agent_id": agent.id,
                "agent_location": agent.location_id,
                "agent_stress": agent.stress,
                "observation_quality": reliability,
            },
        )

        return event

    def _generate_technical_intelligence(self) -> List[RealTimeIntelEvent]:
        """Generate intelligence from technical surveillance"""
        intel_events = []

        # Simulate technical intelligence gathering
        tech_sources = [
            ("electronic_surveillance", "Electronic surveillance data"),
            ("satellite_imagery", "Satellite imagery analysis"),
            ("communication_intercept", "Communication intercept"),
            ("digital_forensics", "Digital forensics discovery"),
        ]

        # Generate 1-3 technical intel events per turn
        num_events = random.randint(1, 3)

        for _ in range(num_events):
            if random.random() < 0.4:  # 40% chance per potential event
                source_type, description = random.choice(tech_sources)

                event = RealTimeIntelEvent(
                    id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source=IntelligenceSource.TECHNICAL_RECON,
                    type=source_type,
                    location=self._get_random_location(),
                    priority=random.choice(["low", "medium", "high"]),
                    reliability=random.uniform(
                        0.8, 0.95
                    ),  # Technical intel generally reliable
                    content=f"Technical surveillance: {description}",
                    raw_data={"technical_source": source_type},
                )

                intel_events.append(event)

        return intel_events

    def _generate_human_assets_intel(self) -> List[RealTimeIntelEvent]:
        """Generate intelligence from human assets (non-agent sources)"""
        intel_events = []

        # Simulate human intelligence sources
        asset_types = [
            (
                "government_insider",
                "Government insider provides classified information",
            ),
            ("military_contact", "Military contact reports troop movements"),
            ("corporate_source", "Corporate source reveals resource allocation"),
            ("civilian_informant", "Civilian informant shares local intelligence"),
        ]

        # Generate 0-2 human asset events per turn
        num_events = random.randint(0, 2)

        for _ in range(num_events):
            if random.random() < 0.3:  # 30% chance per potential event
                asset_type, description = random.choice(asset_types)

                # Human assets have variable reliability
                reliability = random.uniform(0.5, 0.9)

                event = RealTimeIntelEvent(
                    id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source=IntelligenceSource.HUMAN_ASSETS,
                    type=asset_type,
                    location=self._get_random_location(),
                    priority=random.choice(["medium", "high"]),
                    reliability=reliability,
                    content=f"Human asset report: {description}",
                    raw_data={
                        "asset_type": asset_type,
                        "risk_level": 1.0 - reliability,
                    },
                )

                intel_events.append(event)

        return intel_events

    def _generate_signal_intelligence(self) -> List[RealTimeIntelEvent]:
        """Generate signal intelligence from communications intercepts"""
        intel_events = []

        signal_types = [
            ("radio_intercept", "Radio communication intercepted"),
            ("phone_tap", "Phone conversation recorded"),
            ("digital_intercept", "Digital communication captured"),
            ("encryption_break", "Encrypted message decoded"),
        ]

        # Generate 0-1 signal intel events per turn
        if random.random() < 0.25:  # 25% chance per turn
            signal_type, description = random.choice(signal_types)

            # Signal intel reliability depends on encryption/security
            reliability = random.uniform(0.6, 0.85)

            event = RealTimeIntelEvent(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                source=IntelligenceSource.SIGNAL_INTERCEPT,
                type=signal_type,
                location=self._get_random_location(),
                priority=random.choice(["high", "critical"]),
                reliability=reliability,
                content=f"Signal intelligence: {description}",
                raw_data={"signal_type": signal_type},
            )

            intel_events.append(event)

        return intel_events

    def _get_random_location(self) -> str:
        """Get a random location from available locations"""
        if hasattr(self.game_state, "locations") and self.game_state.locations:
            return random.choice(list(self.game_state.locations.keys()))
        return "unknown_location"

    def _update_intelligence_freshness(self):
        """Update freshness of existing intelligence"""
        for event in self.real_time_events:
            event.update_freshness(1.0)  # 1 turn passed

        # Remove stale intelligence
        self.real_time_events = [e for e in self.real_time_events if not e.is_stale()]

    def _perform_pattern_analysis(self) -> List[IntelligencePattern]:
        """Perform pattern analysis on collected intelligence"""
        new_patterns = []

        # Collect recent events for analysis
        recent_events = [e for e in self.real_time_events if e.freshness > 0.5]

        if len(recent_events) < self.pattern_detection_threshold:
            return new_patterns

        # Analyze patterns by type
        type_patterns = self._analyze_type_patterns(recent_events)
        new_patterns.extend(type_patterns)

        # Analyze location patterns
        location_patterns = self._analyze_location_patterns(recent_events)
        new_patterns.extend(location_patterns)

        # Analyze temporal patterns
        temporal_patterns = self._analyze_temporal_patterns(recent_events)
        new_patterns.extend(temporal_patterns)

        # Cross-reference patterns
        cross_patterns = self._analyze_cross_reference_patterns(recent_events)
        new_patterns.extend(cross_patterns)

        return new_patterns

    def _analyze_type_patterns(
        self, events: List[RealTimeIntelEvent]
    ) -> List[IntelligencePattern]:
        """Analyze patterns by intelligence type"""
        patterns = []

        # Group events by type
        type_groups = defaultdict(list)
        for event in events:
            type_groups[event.type].append(event)

        for intel_type, type_events in type_groups.items():
            if len(type_events) >= 3:  # Pattern threshold
                confidence = min(0.9, len(type_events) * 0.2)

                pattern = IntelligencePattern(
                    id=str(uuid.uuid4()),
                    pattern_type="type_clustering",
                    events_involved=[e.id for e in type_events],
                    confidence=confidence,
                    description=f"Increased {intel_type} activity detected",
                    implications=[
                        f"Government may be escalating {intel_type} operations",
                        "Possible security crackdown incoming",
                        "Need to adjust operational security",
                    ],
                    recommended_actions=[
                        f"Increase monitoring of {intel_type} activities",
                        "Review security protocols",
                        "Prepare contingency plans",
                    ],
                    threat_assessment=self._assess_pattern_threat(type_events),
                    created_timestamp=datetime.now(),
                    last_updated=datetime.now(),
                )

                patterns.append(pattern)

        return patterns

    def _analyze_location_patterns(
        self, events: List[RealTimeIntelEvent]
    ) -> List[IntelligencePattern]:
        """Analyze patterns by location"""
        patterns = []

        # Group events by location
        location_groups = defaultdict(list)
        for event in events:
            location_groups[event.location].append(event)

        for location, location_events in location_groups.items():
            if len(location_events) >= 4:  # Higher threshold for location patterns
                confidence = min(0.85, len(location_events) * 0.15)

                pattern = IntelligencePattern(
                    id=str(uuid.uuid4()),
                    pattern_type="location_focus",
                    events_involved=[e.id for e in location_events],
                    confidence=confidence,
                    description=f"Concentrated activity in {location}",
                    implications=[
                        f"{location} is becoming a focus of attention",
                        "Possible government operation planned",
                        "Agents in area may be at risk",
                    ],
                    recommended_actions=[
                        f"Increase security measures in {location}",
                        "Consider relocating assets",
                        "Deploy counter-surveillance",
                    ],
                    threat_assessment=ThreatLevel.HIGH,
                    created_timestamp=datetime.now(),
                    last_updated=datetime.now(),
                )

                patterns.append(pattern)

        return patterns

    def _analyze_temporal_patterns(
        self, events: List[RealTimeIntelEvent]
    ) -> List[IntelligencePattern]:
        """Analyze temporal patterns in intelligence"""
        patterns = []

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Look for rapid succession of events (potential operations)
        rapid_sequences = []
        current_sequence = [sorted_events[0]] if sorted_events else []

        for i in range(1, len(sorted_events)):
            time_diff = (
                sorted_events[i].timestamp - sorted_events[i - 1].timestamp
            ).total_seconds()

            if time_diff < 3600:  # Within 1 hour (rapid succession)
                current_sequence.append(sorted_events[i])
            else:
                if len(current_sequence) >= 3:
                    rapid_sequences.append(current_sequence)
                current_sequence = [sorted_events[i]]

        # Check final sequence
        if len(current_sequence) >= 3:
            rapid_sequences.append(current_sequence)

        for sequence in rapid_sequences:
            pattern = IntelligencePattern(
                id=str(uuid.uuid4()),
                pattern_type="temporal_clustering",
                events_involved=[e.id for e in sequence],
                confidence=0.8,
                description=f"Rapid sequence of {len(sequence)} intelligence events",
                implications=[
                    "Possible coordinated government operation",
                    "Intelligence gathering surge detected",
                    "Heightened alert status warranted",
                ],
                recommended_actions=[
                    "Implement emergency protocols",
                    "Increase communication security",
                    "Prepare for possible raids",
                ],
                threat_assessment=ThreatLevel.HIGH,
                created_timestamp=datetime.now(),
                last_updated=datetime.now(),
            )

            patterns.append(pattern)

        return patterns

    def _analyze_cross_reference_patterns(
        self, events: List[RealTimeIntelEvent]
    ) -> List[IntelligencePattern]:
        """Analyze cross-referenced patterns between different sources"""
        patterns = []

        # Group by source
        source_groups = defaultdict(list)
        for event in events:
            source_groups[event.source].append(event)

        # Look for corroborating intelligence from multiple sources
        for location in set(e.location for e in events):
            location_events = [e for e in events if e.location == location]
            source_types = set(e.source for e in location_events)

            if len(source_types) >= 3 and len(location_events) >= 4:
                confidence = min(0.95, len(source_types) * 0.25)

                pattern = IntelligencePattern(
                    id=str(uuid.uuid4()),
                    pattern_type="multi_source_correlation",
                    events_involved=[e.id for e in location_events],
                    confidence=confidence,
                    description=f"Multiple sources confirm activity in {location}",
                    implications=[
                        "High confidence intelligence correlation",
                        f"Significant operations likely in {location}",
                        "Cross-source verification achieved",
                    ],
                    recommended_actions=[
                        "Prioritize intelligence from this area",
                        "Deploy additional assets for confirmation",
                        "Prepare operational response",
                    ],
                    threat_assessment=ThreatLevel.CRITICAL,
                    created_timestamp=datetime.now(),
                    last_updated=datetime.now(),
                )

                patterns.append(pattern)

        return patterns

    def _assess_pattern_threat(self, events: List[RealTimeIntelEvent]) -> ThreatLevel:
        """Assess threat level for a pattern"""

        # Base threat on number and priority of events
        high_priority_count = sum(
            1 for e in events if e.priority in ["high", "critical"]
        )
        total_events = len(events)

        threat_score = (high_priority_count / total_events) * 100

        if threat_score >= 80:
            return ThreatLevel.CRITICAL
        elif threat_score >= 60:
            return ThreatLevel.HIGH
        elif threat_score >= 40:
            return ThreatLevel.MODERATE
        elif threat_score >= 20:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.MINIMAL

    def _update_threat_assessments(self) -> Dict[str, Any]:
        """Update threat assessments based on current intelligence"""
        threat_updates = {}

        # Update location-based threats
        for location in self.location_threat_levels.keys():
            location_events = [
                e
                for e in self.real_time_events
                if e.location == location and e.freshness > 0.3
            ]

            if location_events:
                new_threat = self._calculate_location_threat(location_events)
                old_threat = self.location_threat_levels[location]

                if new_threat != old_threat:
                    self.location_threat_levels[location] = new_threat
                    threat_updates[location] = {
                        "old_level": old_threat,
                        "new_level": new_threat,
                        "reason": "Intelligence pattern analysis",
                    }

        return threat_updates

    def _calculate_location_threat(
        self, events: List[RealTimeIntelEvent]
    ) -> ThreatLevel:
        """Calculate threat level for a location based on intelligence"""

        if not events:
            return ThreatLevel.LOW

        # Weight by event priority and reliability
        threat_score = 0.0

        for event in events:
            priority_weight = {"low": 1, "medium": 2, "high": 3, "critical": 4}.get(
                event.priority, 1
            )
            reliability_weight = event.reliability
            freshness_weight = event.freshness

            threat_score += priority_weight * reliability_weight * freshness_weight

        # Normalize by number of events
        normalized_score = threat_score / len(events)

        if normalized_score >= 3.5:
            return ThreatLevel.CRITICAL
        elif normalized_score >= 2.8:
            return ThreatLevel.HIGH
        elif normalized_score >= 2.0:
            return ThreatLevel.MODERATE
        elif normalized_score >= 1.2:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.MINIMAL

    def _process_counter_intelligence(self) -> List[Dict[str, Any]]:
        """Process active counter-intelligence operations"""
        results = []

        # Update existing operations
        completed_ops = []
        for op in self.counter_intel_ops:
            op.duration -= 1

            if op.duration <= 0:
                result = self._resolve_counter_intel_operation(op)
                results.append(result)
                completed_ops.append(op)

        # Remove completed operations
        for op in completed_ops:
            self.counter_intel_ops.remove(op)

        # Consider launching new counter-intel operations
        new_ops = self._consider_new_counter_intel_ops()
        for op in new_ops:
            self.counter_intel_ops.append(op)
            results.append(
                {
                    "operation_id": op.id,
                    "type": "launched",
                    "operation_type": op.operation_type.value,
                    "target": op.target,
                }
            )

        return results

    def _resolve_counter_intel_operation(
        self, op: CounterIntelligenceOperation
    ) -> Dict[str, Any]:
        """Resolve a completed counter-intelligence operation"""

        # Roll for success
        success_roll = random.random()
        success = success_roll <= op.success_probability

        result = {
            "operation_id": op.id,
            "type": "completed",
            "operation_type": op.operation_type.value,
            "target": op.target,
            "success": success,
            "threats_discovered": [],
            "intelligence_gained": [],
            "security_improved": False,
        }

        if success:
            op.status = "completed"

            # Generate specific results based on operation type
            if op.operation_type == CounterIntelOp.SURVEILLANCE_DETECTION:
                # Detect enemy surveillance
                detected_surveillance = random.randint(1, 3)
                result["threats_discovered"] = [
                    f"surveillance_team_{i}" for i in range(detected_surveillance)
                ]
                result["security_improved"] = True

            elif op.operation_type == CounterIntelOp.MOLE_HUNT:
                # Search for internal threats
                if random.random() < 0.3:  # 30% chance of finding something
                    result["threats_discovered"] = ["potential_mole_identified"]
                    result["intelligence_gained"] = [
                        "Internal security breach detected"
                    ]

            elif op.operation_type == CounterIntelOp.DISINFORMATION:
                # Spread false information
                result["intelligence_gained"] = ["Disinformation campaign successful"]
                result["enemy_confusion"] = True

            elif op.operation_type == CounterIntelOp.SECURITY_AUDIT:
                # Security assessment
                vulnerabilities = random.randint(2, 5)
                result["vulnerabilities_found"] = vulnerabilities
                result["security_improved"] = True
        else:
            op.status = "failed"
            result["failure_reason"] = "Operation compromised or ineffective"

        return result

    def _consider_new_counter_intel_ops(self) -> List[CounterIntelligenceOperation]:
        """Consider launching new counter-intelligence operations"""
        new_ops = []

        # Check if we need counter-intel based on threat levels
        high_threat_locations = [
            loc
            for loc, threat in self.location_threat_levels.items()
            if threat in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        ]

        for location in high_threat_locations[:2]:  # Limit to 2 new ops per turn
            if random.random() < 0.4:  # 40% chance to launch op
                op_type = random.choice(list(CounterIntelOp))

                new_op = CounterIntelligenceOperation(
                    id=str(uuid.uuid4()),
                    operation_type=op_type,
                    target=location,
                    status="active",
                    effectiveness=random.uniform(0.6, 0.9),
                    resources_committed={
                        "agents": random.randint(1, 3),
                        "budget": random.randint(100, 500),
                    },
                    duration=random.randint(2, 5),
                    success_probability=random.uniform(0.5, 0.8),
                )

                new_ops.append(new_op)

        return new_ops

    def _identify_actionable_intelligence(self) -> List[RealTimeIntelEvent]:
        """Identify intelligence that can be acted upon"""
        actionable = []

        for event in self.real_time_events:
            if self._is_actionable(event):
                event.actionable = True
                actionable.append(event)

        return actionable

    def _is_actionable(self, event: RealTimeIntelEvent) -> bool:
        """Determine if intelligence event is actionable"""

        # Must be fresh and reliable
        if event.freshness < 0.5 or event.reliability < 0.6:
            return False

        # Must be high priority
        if event.priority not in ["high", "critical"]:
            return False

        # Specific actionable types
        actionable_types = [
            "government_movement",
            "security_change",
            "personnel_change",
            "resource_movement",
        ]

        return event.type in actionable_types

    def _generate_priority_alerts(self) -> List[Dict[str, Any]]:
        """Generate priority alerts based on intelligence analysis"""
        alerts = []

        # Critical threat level alerts
        for location, threat_level in self.location_threat_levels.items():
            if threat_level == ThreatLevel.CRITICAL:
                alerts.append(
                    {
                        "type": "critical_threat",
                        "location": location,
                        "message": f"CRITICAL: Imminent threat detected in {location}",
                        "recommended_action": "Evacuate assets, implement emergency protocols",
                    }
                )

        # Pattern-based alerts
        for pattern in self.intelligence_patterns:
            if pattern.confidence > 0.8 and pattern.threat_assessment in [
                ThreatLevel.HIGH,
                ThreatLevel.CRITICAL,
            ]:
                alerts.append(
                    {
                        "type": "pattern_alert",
                        "pattern_type": pattern.pattern_type,
                        "message": f"HIGH CONFIDENCE: {pattern.description}",
                        "recommended_actions": pattern.recommended_actions[
                            :2
                        ],  # Top 2 actions
                    }
                )

        # Rapid intelligence accumulation alerts
        recent_events = [e for e in self.real_time_events if e.freshness > 0.8]
        if len(recent_events) > 8:  # Many recent events
            alerts.append(
                {
                    "type": "intelligence_surge",
                    "message": f"Intelligence surge detected: {len(recent_events)} recent events",
                    "recommended_action": "Review all recent intelligence for patterns",
                }
            )

        return alerts

    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get comprehensive intelligence system summary"""

        recent_events = [e for e in self.real_time_events if e.freshness > 0.5]

        return {
            "total_intelligence_events": len(self.real_time_events),
            "recent_events": len(recent_events),
            "active_patterns": len(self.intelligence_patterns),
            "counter_intel_operations": len(self.counter_intel_ops),
            "threat_levels": {
                loc: threat.value for loc, threat in self.location_threat_levels.items()
            },
            "source_performance": self._get_source_performance_summary(),
            "actionable_intelligence": len(
                [e for e in self.real_time_events if e.actionable]
            ),
            "system_efficiency": self._calculate_system_efficiency(),
        }

    def _get_source_performance_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get performance summary for intelligence sources"""
        summary = {}

        for source in IntelligenceSource:
            source_events = [e for e in self.real_time_events if e.source == source]

            if source_events:
                avg_reliability = sum(e.reliability for e in source_events) / len(
                    source_events
                )
                actionable_count = sum(1 for e in source_events if e.actionable)

                summary[source.value] = {
                    "events_generated": len(source_events),
                    "average_reliability": avg_reliability,
                    "actionable_intelligence": actionable_count,
                    "efficiency": actionable_count / len(source_events)
                    if source_events
                    else 0,
                }

        return summary

    def _calculate_system_efficiency(self) -> float:
        """Calculate overall intelligence system efficiency"""

        if not self.real_time_events:
            return 0.0

        # Efficiency based on actionable intelligence ratio
        actionable_count = sum(1 for e in self.real_time_events if e.actionable)
        actionable_ratio = actionable_count / len(self.real_time_events)

        # Pattern detection efficiency
        pattern_efficiency = len(self.intelligence_patterns) / max(
            1, len(self.real_time_events) // 10
        )

        # Counter-intel coverage
        counter_intel_coverage = len(self.counter_intel_ops) / max(
            1, len(self.location_threat_levels)
        )

        overall_efficiency = (
            actionable_ratio * 0.5
            + min(1.0, pattern_efficiency) * 0.3
            + min(1.0, counter_intel_coverage) * 0.2
        )

        return min(1.0, overall_efficiency)


class IntelligenceOperationalImpact:
    """System for applying intelligence insights to operations"""

    def __init__(self, intelligence_system: EnhancedIntelligenceSystem):
        self.intel_system = intelligence_system
        self.operational_modifiers: Dict[str, Dict[str, float]] = {}
        self.intelligence_driven_opportunities: List[Dict[str, Any]] = []
        self.threat_based_restrictions: Dict[str, List[str]] = {}

    def get_location_operational_impact(self, location: str) -> Dict[str, Any]:
        """Get operational impact for a specific location"""

        threat_level = self.intel_system.location_threat_levels.get(
            location, ThreatLevel.LOW
        )
        location_events = [
            e
            for e in self.intel_system.real_time_events
            if e.location == location and e.freshness > 0.4
        ]

        impact = {
            "threat_level": threat_level.value,
            "mission_success_modifier": 0.0,
            "detection_risk_modifier": 0.0,
            "available_opportunities": [],
            "operational_restrictions": [],
            "recommended_precautions": [],
        }

        # Apply threat level modifiers
        threat_modifiers = {
            ThreatLevel.MINIMAL: {"success": 0.1, "detection": -0.1},
            ThreatLevel.LOW: {"success": 0.0, "detection": 0.0},
            ThreatLevel.MODERATE: {"success": -0.1, "detection": 0.1},
            ThreatLevel.HIGH: {"success": -0.2, "detection": 0.3},
            ThreatLevel.CRITICAL: {"success": -0.4, "detection": 0.5},
            ThreatLevel.IMMINENT: {"success": -0.6, "detection": 0.8},
        }

        modifiers = threat_modifiers.get(
            threat_level, {"success": 0.0, "detection": 0.0}
        )
        impact["mission_success_modifier"] = modifiers["success"]
        impact["detection_risk_modifier"] = modifiers["detection"]

        # Generate specific recommendations based on intelligence
        if threat_level in [
            ThreatLevel.HIGH,
            ThreatLevel.CRITICAL,
            ThreatLevel.IMMINENT,
        ]:
            impact["operational_restrictions"] = [
                "Avoid high-profile operations",
                "Increase operational security",
                "Use indirect approaches only",
                "Consider postponing non-essential missions",
            ]
            impact["recommended_precautions"] = [
                "Deploy counter-surveillance",
                "Use alternative communication methods",
                "Prepare extraction routes",
                "Implement emergency protocols",
            ]

        # Intelligence-driven opportunities
        for event in location_events:
            if event.actionable and event.type in [
                "personnel_change",
                "security_change",
                "resource_movement",
            ]:
                impact["available_opportunities"].append(
                    {
                        "type": event.type,
                        "description": event.content,
                        "reliability": event.reliability,
                        "window": f"{int(event.freshness * 10)} turns remaining",
                    }
                )

        return impact

    def get_mission_intelligence_support(
        self, mission: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get intelligence support for a specific mission"""

        mission_location = mission.get("location", "unknown")
        mission_type = mission.get("type", "unknown")

        support = {
            "intelligence_quality": "none",
            "actionable_intel": [],
            "threat_warnings": [],
            "tactical_advantages": [],
            "success_probability_modifier": 0.0,
            "detection_risk_modifier": 0.0,
        }

        # Gather relevant intelligence
        location_intel = [
            e
            for e in self.intel_system.real_time_events
            if e.location == mission_location and e.freshness > 0.3
        ]

        if not location_intel:
            return support

        # Determine intelligence quality
        avg_reliability = sum(e.reliability for e in location_intel) / len(
            location_intel
        )
        if avg_reliability >= 0.8:
            support["intelligence_quality"] = "excellent"
            support["success_probability_modifier"] = 0.3
        elif avg_reliability >= 0.7:
            support["intelligence_quality"] = "good"
            support["success_probability_modifier"] = 0.2
        elif avg_reliability >= 0.5:
            support["intelligence_quality"] = "fair"
            support["success_probability_modifier"] = 0.1
        else:
            support["intelligence_quality"] = "poor"
            support["success_probability_modifier"] = -0.1

        # Extract actionable intelligence
        for event in location_intel:
            if event.actionable:
                support["actionable_intel"].append(
                    {
                        "type": event.type,
                        "content": event.content,
                        "reliability": event.reliability,
                        "tactical_value": self._assess_tactical_value(
                            event, mission_type
                        ),
                    }
                )

        # Generate threat warnings
        high_priority_events = [
            e for e in location_intel if e.priority in ["high", "critical"]
        ]
        for event in high_priority_events:
            support["threat_warnings"].append(
                {
                    "warning": event.content,
                    "priority": event.priority,
                    "reliability": event.reliability,
                }
            )

        # Identify tactical advantages
        support["tactical_advantages"] = self._identify_tactical_advantages(
            location_intel, mission_type
        )

        return support

    def _assess_tactical_value(
        self, event: RealTimeIntelEvent, mission_type: str
    ) -> float:
        """Assess tactical value of intelligence for a mission type"""

        # Base tactical value matrix
        tactical_matrix = {
            "sabotage": {
                "security_change": 0.9,
                "personnel_change": 0.7,
                "resource_movement": 0.6,
                "government_movement": 0.4,
            },
            "infiltration": {
                "security_change": 0.8,
                "personnel_change": 0.9,
                "communication_pattern": 0.7,
                "government_movement": 0.5,
            },
            "intelligence": {
                "communication_pattern": 0.9,
                "personnel_change": 0.8,
                "security_change": 0.6,
                "resource_movement": 0.5,
            },
            "surveillance": {
                "personnel_change": 0.9,
                "communication_pattern": 0.8,
                "government_movement": 0.7,
                "security_change": 0.6,
            },
        }

        mission_matrix = tactical_matrix.get(mission_type, {})
        base_value = mission_matrix.get(event.type, 0.3)

        # Modify by reliability and freshness
        reliability_modifier = event.reliability
        freshness_modifier = event.freshness

        return base_value * reliability_modifier * freshness_modifier

    def _identify_tactical_advantages(
        self, events: List[RealTimeIntelEvent], mission_type: str
    ) -> List[Dict[str, Any]]:
        """Identify tactical advantages from intelligence"""
        advantages = []

        for event in events:
            tactical_value = self._assess_tactical_value(event, mission_type)

            if tactical_value > 0.6:
                advantage = {
                    "description": f"Intelligence advantage: {event.content}",
                    "type": event.type,
                    "tactical_value": tactical_value,
                    "recommended_exploitation": self._recommend_exploitation(
                        event, mission_type
                    ),
                }
                advantages.append(advantage)

        return advantages

    def _recommend_exploitation(
        self, event: RealTimeIntelEvent, mission_type: str
    ) -> str:
        """Recommend how to exploit intelligence for tactical advantage"""

        exploitation_map = {
            (
                "security_change",
                "sabotage",
            ): "Target security weakness during transition period",
            (
                "personnel_change",
                "infiltration",
            ): "Exploit confusion during personnel changeover",
            (
                "communication_pattern",
                "intelligence",
            ): "Intercept communications during pattern window",
            (
                "resource_movement",
                "sabotage",
            ): "Disrupt resource transport at vulnerable point",
            (
                "government_movement",
                "surveillance",
            ): "Monitor government forces from predicted positions",
        }

        key = (event.type, mission_type)
        return exploitation_map.get(
            key, "Use intelligence to optimize mission timing and approach"
        )


class IntelligenceSystemIntegration:
    """Integration layer connecting enhanced intelligence with existing systems"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.enhanced_intel = EnhancedIntelligenceSystem(game_state)
        self.operational_impact = IntelligenceOperationalImpact(self.enhanced_intel)

    def process_turn_intelligence(self) -> Dict[str, Any]:
        """Process intelligence for the current turn and apply impacts"""

        # Process real-time intelligence
        intel_results = self.enhanced_intel.process_real_time_intelligence()

        # Apply operational impacts
        operational_updates = self._apply_operational_impacts()

        # Update agent intelligence performance
        agent_updates = self._update_agent_intelligence_performance()

        # Generate strategic recommendations
        strategic_recs = self._generate_strategic_recommendations()

        return {
            "intelligence_results": intel_results,
            "operational_updates": operational_updates,
            "agent_updates": agent_updates,
            "strategic_recommendations": strategic_recs,
            "system_summary": self.enhanced_intel.get_intelligence_summary(),
        }

    def _apply_operational_impacts(self) -> Dict[str, Any]:
        """Apply intelligence insights to operational parameters"""
        updates = {}

        # Update location-based operational parameters
        if hasattr(self.game_state, "locations"):
            for location_id in self.game_state.locations.keys():
                impact = self.operational_impact.get_location_operational_impact(
                    location_id
                )

                # Store impact data for use by mission system
                if not hasattr(self.game_state, "intelligence_impacts"):
                    self.game_state.intelligence_impacts = {}

                self.game_state.intelligence_impacts[location_id] = impact
                updates[location_id] = impact

        return updates

    def _update_agent_intelligence_performance(self) -> Dict[str, Any]:
        """Update agent performance based on intelligence contributions"""
        updates = {}

        if not hasattr(self.game_state, "agents"):
            return updates

        # Track which agents contributed intelligence
        recent_events = [
            e for e in self.enhanced_intel.real_time_events if e.freshness > 0.8
        ]

        for event in recent_events:
            if event.source == IntelligenceSource.AGENT_NETWORK:
                agent_id = event.raw_data.get("agent_id")
                if agent_id and agent_id in self.game_state.agents:
                    # Update agent intelligence performance tracking
                    if agent_id not in self.enhanced_intel.agent_intel_performance:
                        self.enhanced_intel.agent_intel_performance[agent_id] = {
                            "events_generated": 0,
                            "success_count": 0,
                            "success_rate": 0.7,
                        }

                    perf = self.enhanced_intel.agent_intel_performance[agent_id]
                    perf["events_generated"] += 1

                    # Consider event successful if it's actionable or high reliability
                    if event.actionable or event.reliability > 0.8:
                        perf["success_count"] += 1

                    perf["success_rate"] = (
                        perf["success_count"] / perf["events_generated"]
                    )

                    updates[agent_id] = {
                        "intelligence_contribution": True,
                        "event_reliability": event.reliability,
                        "success_rate": perf["success_rate"],
                    }

        return updates

    def _generate_strategic_recommendations(self) -> List[Dict[str, Any]]:
        """Generate strategic recommendations based on intelligence analysis"""
        recommendations = []

        # Pattern-based recommendations
        for pattern in self.enhanced_intel.intelligence_patterns:
            if pattern.confidence > 0.7:
                recommendations.append(
                    {
                        "type": "pattern_based",
                        "priority": pattern.threat_assessment.value,
                        "pattern": pattern.pattern_type,
                        "description": pattern.description,
                        "recommended_actions": pattern.recommended_actions,
                    }
                )

        # Threat-based recommendations
        critical_locations = [
            loc
            for loc, threat in self.enhanced_intel.location_threat_levels.items()
            if threat in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        ]

        for location in critical_locations:
            recommendations.append(
                {
                    "type": "threat_response",
                    "priority": "high",
                    "location": location,
                    "description": f"High threat level detected in {location}",
                    "recommended_actions": [
                        "Increase security measures",
                        "Deploy counter-intelligence",
                        "Consider asset relocation",
                    ],
                }
            )

        # Opportunity-based recommendations
        actionable_intel = [
            e for e in self.enhanced_intel.real_time_events if e.actionable
        ]
        if len(actionable_intel) > 3:
            recommendations.append(
                {
                    "type": "opportunity",
                    "priority": "medium",
                    "description": f"{len(actionable_intel)} actionable intelligence opportunities available",
                    "recommended_actions": [
                        "Review actionable intelligence",
                        "Plan operations to exploit opportunities",
                        "Coordinate multiple operations for maximum impact",
                    ],
                }
            )

        return recommendations

    def get_mission_intelligence_briefing(
        self, mission: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get comprehensive intelligence briefing for a mission"""

        # Get basic intelligence support
        intel_support = self.operational_impact.get_mission_intelligence_support(
            mission
        )

        # Get location operational impact
        location_impact = self.operational_impact.get_location_operational_impact(
            mission.get("location", "unknown")
        )

        # Combine into comprehensive briefing
        briefing = {
            "mission_id": mission.get("id", "unknown"),
            "location": mission.get("location", "unknown"),
            "intelligence_quality": intel_support["intelligence_quality"],
            "threat_level": location_impact["threat_level"],
            "success_modifier": intel_support["success_probability_modifier"]
            + location_impact["mission_success_modifier"],
            "detection_risk_modifier": location_impact["detection_risk_modifier"],
            "actionable_intelligence": intel_support["actionable_intel"],
            "threat_warnings": intel_support["threat_warnings"],
            "tactical_advantages": intel_support["tactical_advantages"],
            "operational_restrictions": location_impact["operational_restrictions"],
            "recommended_precautions": location_impact["recommended_precautions"],
            "available_opportunities": location_impact["available_opportunities"],
        }

        return briefing


# Integration functions for existing systems
def enhance_mission_with_intelligence(mission_executor, intelligence_integration):
    """Enhance mission execution with intelligence support"""

    def enhanced_execute_mission(mission, agents, location, resources):
        """Enhanced mission execution with intelligence briefing"""

        # Get intelligence briefing
        intel_briefing = intelligence_integration.get_mission_intelligence_briefing(
            mission
        )

        # Apply intelligence modifiers to mission
        original_success_prob = mission.get("success_probability", 0.5)
        intel_modifier = intel_briefing["success_modifier"]
        enhanced_success_prob = max(
            0.05, min(0.95, original_success_prob + intel_modifier)
        )

        # Apply detection risk modifier
        original_detection_risk = mission.get("detection_risk", 0.3)
        detection_modifier = intel_briefing["detection_risk_modifier"]
        enhanced_detection_risk = max(
            0.05, min(0.95, original_detection_risk + detection_modifier)
        )

        # Create enhanced mission object
        enhanced_mission = mission.copy()
        enhanced_mission["success_probability"] = enhanced_success_prob
        enhanced_mission["detection_risk"] = enhanced_detection_risk
        enhanced_mission["intelligence_briefing"] = intel_briefing

        # Execute with original system
        result = mission_executor.execute_mission(
            enhanced_mission, agents, location, resources
        )

        # Add intelligence effects to result
        result["intelligence_effects"] = {
            "briefing_quality": intel_briefing["intelligence_quality"],
            "success_modifier": intel_modifier,
            "detection_modifier": detection_modifier,
            "tactical_advantages_used": len(intel_briefing["tactical_advantages"]),
            "threat_warnings": len(intel_briefing["threat_warnings"]),
        }

        return result

    return enhanced_execute_mission


def integrate_intelligence_with_agent_decisions(
    agent_autonomy_system, intelligence_integration
):
    """Integrate intelligence insights with agent autonomous decisions"""

    def intelligence_informed_decisions(agent, decision_context):
        """Make decisions informed by intelligence"""

        # Get location intelligence impact
        location_impact = (
            intelligence_integration.operational_impact.get_location_operational_impact(
                agent.location_id
            )
        )

        # Modify decision context based on intelligence
        enhanced_context = decision_context.copy()
        enhanced_context["threat_level"] = location_impact["threat_level"]
        enhanced_context["operational_restrictions"] = location_impact[
            "operational_restrictions"
        ]
        enhanced_context["intelligence_warnings"] = location_impact.get(
            "threat_warnings", []
        )

        # Adjust agent behavior based on threat level
        if location_impact["threat_level"] in ["high", "critical", "imminent"]:
            # Increase caution in high-threat areas
            enhanced_context["risk_tolerance"] = (
                enhanced_context.get("risk_tolerance", 0.5) * 0.7
            )
            enhanced_context["prefer_safe_actions"] = True

        # Make decision with enhanced context
        return agent_autonomy_system.make_autonomous_decision(agent, enhanced_context)

    return intelligence_informed_decisions
