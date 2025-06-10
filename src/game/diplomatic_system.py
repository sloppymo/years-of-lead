"""
Years of Lead - Diplomatic System

Revolutionary simulation game diplomatic system with secret alliances,
covert operations, dynamic trust, and scandal-driven narratives.
"""

import uuid
import random
from datetime import datetime, timedelta
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from loguru import logger

from .diplomatic_config import DIPLOMATIC_CONFIG, OPERATIONAL_CONFIG


class AllianceType(Enum):
    """Types of faction alliances"""
    PUBLIC = "public"
    SECRET = "secret"
    COERCED = "coerced"


class CovertOperationType(Enum):
    """Types of covert operations"""
    INTELLIGENCE_SHARING = "intelligence_sharing"
    JOINT_SABOTAGE = "joint_sabotage"
    COORDINATED_PROPAGANDA = "coordinated_propaganda"
    RESOURCE_TRANSFER = "resource_transfer"
    COVERT_SUPPORT = "covert_support"
    FALSE_FLAG = "false_flag"
    DOUBLE_AGENT_DEPLOYMENT = "double_agent_deployment"
    COUNTER_INTELLIGENCE = "counter_intelligence"


class DiplomaticEventType(Enum):
    """Types of diplomatic events for narrative tracking"""
    ALLIANCE_FORMED = "alliance_formed"
    ALLIANCE_BROKEN = "alliance_broken"
    BETRAYAL_DISCOVERED = "betrayal_discovered"
    OPERATION_LEAKED = "operation_leaked"
    TRUST_GAINED = "trust_gained"
    TRUST_LOST = "trust_lost"
    SCANDAL_ERUPTED = "scandal_erupted"
    DOUBLE_AGENT_EXPOSED = "double_agent_exposed"
    FALSE_FLAG_DISCOVERED = "false_flag_discovered"


class AgentStatus(Enum):
    """Status types for double agents"""
    LOYAL = "loyal"
    DOUBLE_AGENT = "double_agent"
    EXPOSED = "exposed"
    TURNED = "turned"


@dataclass
class SecretDiplomaticChannel:  # ITERATION_031
    """Secure communication channel between factions"""
    id: str
    faction_a: str
    faction_b: str
    trust_level: float = DIPLOMATIC_CONFIG.BASE_TRUST_LEVEL
    encryption_strength: float = DIPLOMATIC_CONFIG.BASE_ENCRYPTION_STRENGTH
    established_turn: int = 0
    last_used_turn: int = 0
    
    # Security metrics
    leak_incidents: int = 0
    successful_communications: int = 0
    failed_communications: int = 0
    
    # Activity tracking
    message_history: List[Dict[str, Any]] = field(default_factory=list)
    operation_history: List[str] = field(default_factory=list)
    
    def calculate_leak_risk(self, current_heat: int = 0) -> float:  # ITERATION_031
        """Calculate current leak risk based on trust, encryption, and heat"""
        base_risk = DIPLOMATIC_CONFIG.BASE_LEAK_CHANCE
        
        # Trust modifier (higher trust = lower risk)
        trust_modifier = self.trust_level * DIPLOMATIC_CONFIG.TRUST_LEAK_MODIFIER
        
        # Encryption modifier (better encryption = lower risk)
        encryption_modifier = self.encryption_strength * DIPLOMATIC_CONFIG.ENCRYPTION_LEAK_MODIFIER
        
        # Heat modifier (higher surveillance = higher risk)
        heat_modifier = (current_heat / 100.0) * DIPLOMATIC_CONFIG.SURVEILLANCE_HEAT_MODIFIER
        
        # Historical incidents increase risk
        incident_modifier = self.leak_incidents * 0.02
        
        total_risk = base_risk + trust_modifier + encryption_modifier + heat_modifier + incident_modifier
        
        # Apply minimum risk only for active channels
        if self.last_used_turn > 0:
            total_risk = max(0.01, total_risk)
        
        return max(0.0, min(1.0, total_risk))
    
    def update_trust(self, change: float, reason: str = ""):
        """Update trust level with bounds checking and logging"""
        old_trust = self.trust_level
        self.trust_level = max(
            DIPLOMATIC_CONFIG.MIN_TRUST_LEVEL,
            min(DIPLOMATIC_CONFIG.MAX_TRUST_LEVEL, self.trust_level + change)
        )
        
        if abs(change) > 0.05:  # Log significant changes
            logger.info(f"Diplomatic trust between {self.faction_a} and {self.faction_b} "
                       f"changed from {old_trust:.2f} to {self.trust_level:.2f}. Reason: {reason}")
    
    def degrade_encryption(self):
        """Natural encryption degradation over time"""
        self.encryption_strength = max(0.1, 
            self.encryption_strength - DIPLOMATIC_CONFIG.ENCRYPTION_DECAY_RATE)
    
    def upgrade_encryption(self, cost_paid: int) -> bool:
        """Upgrade encryption if cost is sufficient"""
        if cost_paid >= DIPLOMATIC_CONFIG.ENCRYPTION_UPGRADE_COST:
            self.encryption_strength = min(1.0, self.encryption_strength + 0.2)
            return True
        return False
    
    def send_message(self, sender: str, content: str, operation_type: Optional[str] = None) -> bool:
        """Send a message through the channel and check for leaks"""
        leak_risk = self.calculate_leak_risk()
        leaked = random.random() < leak_risk
        
        message = {
            "id": str(uuid.uuid4()),
            "sender": sender,
            "content": content,
            "operation_type": operation_type,
            "timestamp": datetime.now(),
            "leaked": leaked,
            "leak_risk": leak_risk
        }
        
        self.message_history.append(message)
        self.last_used_turn += 1
        
        if leaked:
            self.leak_incidents += 1
            self.failed_communications += 1
            self.update_trust(-0.1, f"Communication leaked: {content[:50]}...")
            logger.warning(f"LEAK: Communication between {self.faction_a} and {self.faction_b} leaked!")
            return False
        else:
            self.successful_communications += 1
            return True


@dataclass
class FactionAlliance:
    """Alliance between two or more factions"""
    id: str
    name: str
    alliance_type: AllianceType
    member_factions: Set[str] = field(default_factory=set)
    leader_faction: Optional[str] = None
    
    # Alliance metrics
    stability: float = 0.7
    public_support: float = 0.5
    formed_turn: int = 0
    
    # Operational capabilities
    shared_resources: Dict[str, int] = field(default_factory=dict)
    joint_operations: List[str] = field(default_factory=list)
    active_channels: Dict[str, str] = field(default_factory=dict)  # faction_pair -> channel_id
    
    # History and narrative
    betrayal_history: List[Dict[str, Any]] = field(default_factory=list)
    major_events: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_member(self, faction_id: str) -> bool:
        """Add a faction to the alliance"""
        if faction_id not in self.member_factions:
            self.member_factions.add(faction_id)
            self._update_stability(-0.05)  # New members slightly destabilize
            return True
        return False
    
    def remove_member(self, faction_id: str, reason: str = "withdrawal") -> bool:
        """Remove a faction from the alliance"""
        if faction_id in self.member_factions:
            self.member_factions.remove(faction_id)
            self.betrayal_history.append({
                "faction": faction_id,
                "reason": reason,
                "turn": 0,  # Will be set by caller
                "stability_impact": -0.3
            })
            self._update_stability(-0.3)
            return True
        return False
    
    def _update_stability(self, change: float):
        """Update alliance stability with bounds"""
        self.stability = max(0.0, min(1.0, self.stability + change))
        
    def calculate_discovery_chance(self) -> float:
        """Calculate chance of secret alliance being discovered"""
        if self.alliance_type != AllianceType.SECRET:
            return 0.0
        
        base_chance = DIPLOMATIC_CONFIG.SECRET_ALLIANCE_DISCOVERY_CHANCE
        
        # More members = higher chance of discovery
        member_modifier = (len(self.member_factions) - 2) * 0.02
        
        # Lower stability = higher chance of leaks
        stability_modifier = (1.0 - self.stability) * 0.1
        
        # Recent operations increase visibility
        activity_modifier = min(len(self.joint_operations), 5) * 0.01
        
        return min(1.0, base_chance + member_modifier + stability_modifier + activity_modifier)
    
    def get_operational_bonus(self) -> float:
        """Get bonus for joint operations based on alliance type and stability"""
        base_bonus = DIPLOMATIC_CONFIG.JOINT_OPERATION_BONUS
        
        type_modifier = {
            AllianceType.PUBLIC: 1.0,
            AllianceType.SECRET: 0.8,  # Secret alliances are less efficient
            AllianceType.COERCED: 0.6  # Coerced alliances are least efficient
        }
        
        return base_bonus * type_modifier[self.alliance_type] * self.stability


@dataclass
class DoubleAgent:  # ITERATION_031
    """Agent working for multiple factions"""
    agent_id: str
    primary_faction: str
    secondary_factions: Set[str] = field(default_factory=set)
    exposure_risk: float = DIPLOMATIC_CONFIG.DOUBLE_AGENT_EXPOSURE_CHANCE
    intelligence_value: float = DIPLOMATIC_CONFIG.DOUBLE_AGENT_INTELLIGENCE_BONUS
    
    # Status tracking
    status: AgentStatus = AgentStatus.DOUBLE_AGENT
    last_report_turn: int = 0
    successful_missions: int = 0
    failed_missions: int = 0
    
    def update_exposure_risk(self, mission_result: bool):  # ITERATION_031
        """Update exposure risk based on mission outcomes"""
        if mission_result:
            self.successful_missions += 1
            # Success slightly reduces risk
            self.exposure_risk = max(0.02, self.exposure_risk - 0.01)
        else:
            self.failed_missions += 1
            # Failure increases risk
            self.exposure_risk = min(0.5, self.exposure_risk + 0.03)
    
    def check_exposure(self) -> bool:
        """Check if agent is exposed this turn"""
        # Only check exposure if agent has been active
        if self.last_report_turn == 0:
            return False
        
        # Update last report turn to simulate activity
        self.last_report_turn += 1
        return random.random() < self.exposure_risk


@dataclass
class DiplomaticEvent:
    """Diplomatic event for history and narrative tracking"""
    id: str
    event_type: DiplomaticEventType
    factions_involved: List[str]
    turn_occurred: int
    description: str
    narrative_impact: Dict[str, Any] = field(default_factory=dict)
    mechanical_effects: Dict[str, Any] = field(default_factory=dict)
    
    # Scandal and media tracking
    media_coverage: int = 0  # 0-10 scale
    public_awareness: float = 0.0  # 0-1 scale
    heat_generated: int = 0


class DiplomaticSystem:
    """Main diplomatic system managing all faction relationships and covert operations"""
    
    def __init__(self):
        self.channels: Dict[str, SecretDiplomaticChannel] = {}
        self.alliances: Dict[str, FactionAlliance] = {}
        self.double_agents: Dict[str, DoubleAgent] = {}
        self.diplomatic_events: List[DiplomaticEvent] = []
        
        # System state tracking
        self.current_turn: int = 0
        self.global_heat: int = 0
        self.media_saturation: int = 0
        self.scandal_count: int = 0
        
        # Faction relationship matrix
        self.faction_relationships: Dict[str, Dict[str, float]] = {}
        self.betrayal_memory: Dict[str, Dict[str, int]] = {}  # faction -> betrayer -> turns_remembered
        
        logger.info("Diplomatic system initialized")
    
    def establish_channel(self, faction_a: str, faction_b: str) -> str:
        """Establish a secret diplomatic channel between two factions"""
        channel_id = f"channel_{faction_a}_{faction_b}_{self.current_turn}"
        
        channel = SecretDiplomaticChannel(
            id=channel_id,
            faction_a=faction_a,
            faction_b=faction_b,
            established_turn=self.current_turn
        )
        
        self.channels[channel_id] = channel
        self.global_heat += DIPLOMATIC_CONFIG.DIPLOMATIC_ACTIVITY_HEAT_GAIN
        
        # Log establishment
        event = DiplomaticEvent(
            id=str(uuid.uuid4()),
            event_type=DiplomaticEventType.TRUST_GAINED,
            factions_involved=[faction_a, faction_b],
            turn_occurred=self.current_turn,
            description=f"Secret diplomatic channel established between {faction_a} and {faction_b}",
            heat_generated=DIPLOMATIC_CONFIG.DIPLOMATIC_ACTIVITY_HEAT_GAIN
        )
        self.diplomatic_events.append(event)
        
        logger.info(f"Established diplomatic channel between {faction_a} and {faction_b}")
        return channel_id
    
    def form_alliance(self, factions: List[str], alliance_type: AllianceType, 
                     name: str, leader: Optional[str] = None) -> str:
        """Form an alliance between multiple factions"""
        alliance_id = f"alliance_{name.lower().replace(' ', '_')}_{self.current_turn}"
        
        alliance = FactionAlliance(
            id=alliance_id,
            name=name,
            alliance_type=alliance_type,
            member_factions=set(factions),
            leader_faction=leader,
            formed_turn=self.current_turn
        )
        
        self.alliances[alliance_id] = alliance
        
        # Establish channels between all members if secret alliance
        if alliance_type == AllianceType.SECRET:
            for i, faction_a in enumerate(factions):
                for faction_b in factions[i+1:]:
                    channel_id = self.establish_channel(faction_a, faction_b)
                    alliance.active_channels[f"{faction_a}_{faction_b}"] = channel_id
        
        # Update heat based on alliance type
        heat_gain = {
            AllianceType.PUBLIC: 5,
            AllianceType.SECRET: 2,
            AllianceType.COERCED: 10
        }
        self.global_heat += heat_gain[alliance_type]
        
        # Create diplomatic event
        event = DiplomaticEvent(
            id=str(uuid.uuid4()),
            event_type=DiplomaticEventType.ALLIANCE_FORMED,
            factions_involved=factions,
            turn_occurred=self.current_turn,
            description=f"{alliance_type.value.title()} alliance '{name}' formed between {', '.join(factions)}",
            heat_generated=heat_gain[alliance_type]
        )
        self.diplomatic_events.append(event)
        
        logger.info(f"Formed {alliance_type.value} alliance '{name}' with factions: {factions}")
        return alliance_id
    
    def execute_covert_operation(self, operation_type: CovertOperationType, 
                                executing_faction: str, target_faction: Optional[str] = None,
                                allied_factions: Optional[List[str]] = None,
                                operation_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a covert operation with full consequences"""
        operation_id = str(uuid.uuid4())
        results = {
            "operation_id": operation_id,
            "success": False,
            "leaked": False,
            "discovered": False,
            "narrative": "",
            "heat_gain": 0,
            "trust_changes": {},
            "resource_changes": {},
            "scandal_generated": False
        }
        
        # Get operation configuration
        operation_config = OPERATIONAL_CONFIG.OPERATION_TYPES.get(operation_type.value, {})
        base_success_rate = operation_config.get("success_rate", 0.7)
        base_heat_gain = operation_config.get("heat_gain", 5)
        
        # Calculate success based on various factors
        success_chance = self._calculate_operation_success(
            operation_type, executing_faction, allied_factions, operation_config
        )
        
        results["success"] = random.random() < success_chance
        
        # Handle specific operation types
        if operation_type == CovertOperationType.FALSE_FLAG:
            return self._execute_false_flag(executing_faction, target_faction, results, operation_data)
        elif operation_type == CovertOperationType.DOUBLE_AGENT_DEPLOYMENT:
            return self._execute_double_agent_deployment(executing_faction, target_faction, results, operation_data)
        elif operation_type == CovertOperationType.COVERT_SUPPORT:
            return self._execute_covert_support(executing_faction, target_faction, results, operation_data)
        elif operation_type == CovertOperationType.COUNTER_INTELLIGENCE:
            return self._execute_counter_intelligence(executing_faction, target_faction, results, operation_data)
        else:
            # Handle other operation types
            results["success"] = False
            results["leaked"] = True
            results["discovered"] = False
            results["narrative"] = f"Operation type '{operation_type.value}' not implemented."
            results["heat_gain"] = 0
            results["trust_changes"] = {}
            results["resource_changes"] = {}
            results["scandal_generated"] = False
        
        return results 
    
    def _calculate_operation_success(self, operation_type: CovertOperationType,  # ITERATION_031
                                   executing_faction: str, allied_factions: Optional[List[str]] = None,
                                   operation_config: Optional[Dict[str, Any]] = None) -> float:
        """Calculate success chance for a covert operation"""
        base_success = operation_config.get("success_rate", 0.7) if operation_config else 0.7
        
        # Alliance bonuses
        alliance_bonus = 0.0
        if allied_factions:
            for alliance in self.alliances.values():
                if executing_faction in alliance.member_factions:
                    alliance_bonus += alliance.get_operational_bonus()
        
        # Trust bonuses from channels
        trust_bonus = 0.0
        for channel in self.channels.values():
            if executing_faction in [channel.faction_a, channel.faction_b]:
                trust_bonus += channel.trust_level * 0.1
        
        # Heat penalties
        heat_penalty = (self.global_heat / 100.0) * 0.2
        
        success_chance = base_success + alliance_bonus + trust_bonus - heat_penalty
        return max(0.1, min(0.95, success_chance))
    
    def _execute_false_flag(self, executing_faction: str, target_faction: str, 
                           results: Dict[str, Any], operation_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a false flag operation"""
        detection_chance = DIPLOMATIC_CONFIG.FALSE_FLAG_DETECTION_CHANCE
        
        if random.random() < detection_chance:
            results["discovered"] = True
            results["narrative"] = f"False flag operation by {executing_faction} against {target_faction} was discovered!"
            results["heat_gain"] = DIPLOMATIC_CONFIG.LEAKED_OPERATION_HEAT_GAIN
            results["scandal_generated"] = True
        else:
            results["success"] = True
            results["narrative"] = f"False flag operation successfully framed {target_faction}"
            results["heat_gain"] = 5
        
        return results
    
    def _execute_double_agent_deployment(self, executing_faction: str, target_faction: str,
                                        results: Dict[str, Any], operation_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a double agent deployment"""
        agent_id = operation_data.get("agent_id", f"agent_{random.randint(1000, 9999)}")
        
        double_agent = DoubleAgent(
            agent_id=agent_id,
            primary_faction=executing_faction,
            secondary_factions={target_faction}
        )
        
        self.double_agents[agent_id] = double_agent
        results["success"] = True
        results["narrative"] = f"Double agent {agent_id} deployed to {target_faction}"
        results["heat_gain"] = 3
        
        return results
    
    def _execute_covert_support(self, executing_faction: str, target_faction: str,
                               results: Dict[str, Any], operation_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute covert support operation"""
        results["success"] = True
        results["narrative"] = f"{executing_faction} provided covert support to {target_faction}"
        results["heat_gain"] = 2
        results["resource_changes"] = {target_faction: {"support": 10}}
        
        return results
    
    def _execute_counter_intelligence(self, executing_faction: str, target_faction: str,
                                     results: Dict[str, Any], operation_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute counter-intelligence operation"""
        results["success"] = True
        results["narrative"] = f"{executing_faction} conducted counter-intelligence against {target_faction}"
        results["heat_gain"] = 4
        
        return results
    
    def process_turn(self, turn_number: int, faction_states: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:  # ITERATION_031
        """Process diplomatic events for a turn"""
        self.current_turn = turn_number
        results = {
            "events": [],
            "heat_changes": 0,
            "alliance_changes": [],
            "betrayals": []
        }
        
        # Process alliance discoveries
        for alliance in self.alliances.values():
            if alliance.alliance_type == AllianceType.SECRET:
                discovery_chance = alliance.calculate_discovery_chance()
                if random.random() < discovery_chance:
                    results["events"].append(f"Secret alliance '{alliance.name}' discovered!")
                    results["heat_changes"] += DIPLOMATIC_CONFIG.EXPOSED_ALLIANCE_HEAT_GAIN
                    results["alliance_changes"].append({
                        "alliance_id": alliance.id,
                        "type": "discovered",
                        "heat_gain": DIPLOMATIC_CONFIG.EXPOSED_ALLIANCE_HEAT_GAIN
                    })
        
        # Process double agent exposures
        exposed_agents = []
        for agent_id, agent in self.double_agents.items():
            if agent.check_exposure():
                exposed_agents.append(agent_id)
                results["events"].append(f"Double agent {agent_id} exposed!")
                results["heat_changes"] += 10
        
        # Remove exposed agents
        for agent_id in exposed_agents:
            del self.double_agents[agent_id]
        
        # Update global heat
        self.global_heat += results["heat_changes"]
        
        return results
    
    def _execute_betrayal(self, betraying_faction: str, alliance: FactionAlliance,  # ITERATION_031
                         faction_states: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a betrayal within an alliance"""
        results = {
            "betraying_faction": betraying_faction,
            "alliance_id": alliance.id,
            "success": False,
            "narrative": "",
            "consequences": {}
        }
        
        # Check if betrayal is successful
        betrayal_chance = DIPLOMATIC_CONFIG.BETRAYAL_BASE_CHANCE
        
        # Desperation increases betrayal chance
        if betraying_faction in faction_states:
            desperation = faction_states[betraying_faction].get("desperation", 0)
            betrayal_chance += desperation * DIPLOMATIC_CONFIG.BETRAYAL_DESPERATION_MODIFIER
        
        if random.random() < betrayal_chance:
            results["success"] = True
            results["narrative"] = f"{betraying_faction} betrayed alliance '{alliance.name}'"
            
            # Record betrayal in memory
            if betraying_faction not in self.betrayal_memory:
                self.betrayal_memory[betraying_faction] = {}
            
            for faction in alliance.member_factions:
                if faction != betraying_faction:
                    self.betrayal_memory[betraying_faction][faction] = DIPLOMATIC_CONFIG.BETRAYAL_MEMORY_DURATION
            
            # Remove from alliance
            alliance.remove_member(betraying_faction, "betrayal")
            
            # Generate scandal
            results["consequences"]["scandal"] = True
            results["consequences"]["heat_gain"] = DIPLOMATIC_CONFIG.BETRAYAL_MOMENTUM_LOSS
        
        return results
    
    def get_recent_scandals(self, turns_back: int = 5) -> List[DiplomaticEvent]:
        """Get recent scandal events"""
        recent_scandals = []
        cutoff_turn = self.current_turn - turns_back
        
        for event in self.diplomatic_events:
            if (event.event_type == DiplomaticEventType.SCANDAL_ERUPTED and 
                event.turn_occurred >= cutoff_turn):
                recent_scandals.append(event)
        
        return recent_scandals 