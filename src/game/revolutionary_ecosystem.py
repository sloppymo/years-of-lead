"""
Revolutionary Ecosystem - ITERATION 021

Multi-faction revolutionary environment where AI-controlled factions operate independently
alongside the player, creating a dynamic ecosystem of competing resistance movements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import random


class FactionIdeology(Enum):
    """Core ideological orientations of revolutionary factions"""
    SOCIALIST = "socialist"                 # Worker-focused revolutionary socialism
    ANARCHIST = "anarchist"                # Anti-state anarchist collective
    NATIONALIST = "nationalist"            # Ethnic/national liberation movement
    RELIGIOUS = "religious"                # Faith-based resistance movement
    LIBERAL_DEMOCRATIC = "liberal_democratic"  # Democratic reform movement
    MILITANT_COMMUNIST = "militant_communist"  # Hardline communist revolution
    SEPARATIST = "separatist"              # Regional independence movement


class FactionActivityType(Enum):
    """Types of activities AI factions can engage in"""
    PASSIVE_RECRUITMENT = "passive_recruitment"     # Building support quietly
    PROPAGANDA_CAMPAIGN = "propaganda_campaign"     # Media and messaging operations
    SABOTAGE_OPERATION = "sabotage_operation"      # Infrastructure attacks
    ASSASSINATION_ATTEMPT = "assassination_attempt" # Targeting officials
    MASS_DEMONSTRATION = "mass_demonstration"       # Public protest organization
    UNDERGROUND_ORGANIZING = "underground_organizing" # Cell network building
    RIVAL_CONFRONTATION = "rival_confrontation"     # Fighting other factions
    COOPERATION_MISSION = "cooperation_mission"     # Joint operations
    
    # Rivalry & Splinter Activities - ITERATION 022
    PROPAGANDA_WAR = "propaganda_war"              # Media campaign against rival faction
    INFILTRATION_OPERATION = "infiltration_operation" # Infiltrating rival faction
    DEFECTION_CAMPAIGN = "defection_campaign"      # Encouraging rival defections
    IDEOLOGICAL_PURGE = "ideological_purge"       # Internal faction purification


class JointActivityType(Enum):
    """Types of joint activities between allied factions - ITERATION 023"""
    COOP_PROPAGANDA = "coop_propaganda"            # Joint propaganda campaign
    JOINT_DEMONSTRATION = "joint_demonstration"    # Coordinated public demonstration
    COMBINED_OPERATION = "combined_operation"      # Joint military/sabotage operation
    SHARED_RECRUITMENT = "shared_recruitment"      # Cooperative recruitment drive
    ALLIANCE_SUMMIT = "alliance_summit"           # Strategic planning meeting
    RESOURCE_SHARING = "resource_sharing"         # Sharing funds, safe houses, intel


class FactionConflictType(Enum):
    """Types of inter-faction conflicts"""
    FRACTURE_REVOLUTION = "fracture_revolution"    # Major ideological split
    MARTYR_SPLIT = "martyr_split"                 # Split over martyrdom interpretation
    COVERT_RIVALRY = "covert_rivalry"             # Hidden competition
    DOCTRINAL_DOMINATION = "doctrinal_domination" # One faction claiming ideological supremacy
    TERRITORIAL_DISPUTE = "territorial_dispute"    # Fighting over territory
    RESOURCE_COMPETITION = "resource_competition"  # Competing for funding/recruits
    BETRAYAL_EXPOSURE = "betrayal_exposure"       # Revealing faction betrayals
    
    # Additional conflict types for rivalry resolution - ITERATION 022
    PROPAGANDA_WAR = "propaganda_war"             # Media campaign between factions
    DEFECTION_CAMPAIGN = "defection_campaign"     # Encouraging rival defections
    
    # Alliance conflict types - ITERATION 023
    ALLIANCE_BETRAYAL = "alliance_betrayal"       # Breaking alliance for personal gain
    COOPERATION_FAILURE = "cooperation_failure"   # Joint operation failure causing tension
    
    # Propaganda narrative conflicts - ITERATION 024
    NARRATIVE_WAR = "narrative_war"               # Public propaganda battle over alliance/betrayal


class PropagandaTone(Enum):
    """Propaganda narrative tones for alliance events - ITERATION 024"""
    UNITY_AGAINST_OPPRESSION = "unity_against_oppression"    # Positive alliance spin
    BETRAYAL_OF_CAUSE = "betrayal_of_cause"                 # Anti-betrayer narrative
    HEROIC_COOPERATION = "heroic_cooperation"               # Joint success celebration
    ALLIANCE_NECESSITY = "alliance_necessity"               # Strategic alliance justification
    TRAITOR_EXPOSURE = "traitor_exposure"                   # Denouncing former allies


@dataclass
class FactionRelationship:
    """Bi-directional relationship between two factions"""
    faction_a: str  # Faction name
    faction_b: str  # Faction name
    trust_rating: float = 0.0           # -100 to +100, trust/hostility level
    rivalry_intensity: float = 0.0      # 0-100, how intense their rivalry is
    cooperation_cooldown: int = 0       # Days until they can cooperate again
    sabotage_penalties: float = 0.0     # Accumulated sabotage damage
    
    # Historical tracking
    major_conflicts: List[str] = field(default_factory=list)
    cooperation_history: List[str] = field(default_factory=list)
    last_interaction_date: Optional[datetime] = None
    
    def adjust_trust(self, change: float, reason: str) -> None:
        """Adjust trust rating with bounds checking"""
        old_trust = self.trust_rating
        self.trust_rating = max(-100.0, min(100.0, self.trust_rating + change))
        
        # Log significant changes
        if abs(change) > 10.0:
            interaction_record = f"{reason}: {old_trust:.1f} → {self.trust_rating:.1f}"
            if change > 0:
                self.cooperation_history.append(interaction_record)
            else:
                self.major_conflicts.append(interaction_record)
        
        self.last_interaction_date = datetime.now()
    
    def escalate_rivalry(self, intensity_increase: float, conflict_type: str) -> None:
        """Escalate rivalry between factions"""
        self.rivalry_intensity = min(100.0, self.rivalry_intensity + intensity_increase)
        self.major_conflicts.append(f"{conflict_type}_{datetime.now().strftime('%Y%m%d')}")
        
        # Rivalry reduces trust
        trust_damage = intensity_increase * 0.5
        self.adjust_trust(-trust_damage, f"Rivalry escalation: {conflict_type}")


@dataclass
class FactionConflictEvent:
    """Dynamic faction conflict event with narrative consequences"""
    conflict_type: FactionConflictType
    primary_faction: str
    target_faction: str
    trigger_date: datetime
    description: str
    intensity: float = 1.0              # 0-3, how severe the conflict is
    
    # Outcome tracking
    winner: Optional[str] = None
    consequences: Dict[str, Any] = field(default_factory=dict)
    momentum_impact: float = 0.0
    public_attention: float = 0.0       # How much public notice this gets
    
    def resolve_conflict(self, primary_faction_obj: 'RevolutionaryFaction',
                        target_faction_obj: 'RevolutionaryFaction',
                        ecosystem: 'RevolutionaryEcosystem') -> Dict[str, Any]:
        """Resolve the faction conflict and apply consequences"""
        resolution_results = {
            'conflict_type': self.conflict_type.value,
            'primary_faction': self.primary_faction,
            'target_faction': self.target_faction,
            'winner': None,
            'consequences': [],
            'momentum_impact': 0.0
        }
        
        if self.conflict_type == FactionConflictType.PROPAGANDA_WAR:
            # Media war between factions
            primary_media_power = primary_faction_obj.media_reach * primary_faction_obj.public_support
            target_media_power = target_faction_obj.media_reach * target_faction_obj.public_support
            
            if primary_media_power > target_media_power * 1.3:
                # Primary faction wins decisively
                self.winner = self.primary_faction
                primary_faction_obj.public_support += 5.0
                target_faction_obj.public_support -= 8.0
                primary_faction_obj.media_reach = min(1.0, primary_faction_obj.media_reach + 0.1)
                resolution_results['consequences'].append(f"{self.primary_faction} dominates media narrative")
                self.momentum_impact = 2.0
            elif primary_media_power > target_media_power:
                # Narrow victory
                self.winner = self.primary_faction
                primary_faction_obj.public_support += 2.0
                target_faction_obj.public_support -= 3.0
                resolution_results['consequences'].append(f"{self.primary_faction} wins media battle")
                self.momentum_impact = 1.0
            else:
                # Target faction resists or wins
                target_faction_obj.public_support += 3.0
                primary_faction_obj.public_support -= 2.0
                resolution_results['consequences'].append(f"{self.target_faction} successfully defends against propaganda")
                self.momentum_impact = -1.0
        
        elif self.conflict_type == FactionConflictType.TERRITORIAL_DISPUTE:
            # Fighting over territory control
            primary_strength = primary_faction_obj.operational_capacity * primary_faction_obj.aggression
            target_strength = target_faction_obj.operational_capacity * target_faction_obj.aggression
            
            if primary_strength > target_strength * 1.5:
                # Primary faction takes territory
                self.winner = self.primary_faction
                if target_faction_obj.territory_zones:
                    seized_territory = random.choice(target_faction_obj.territory_zones)
                    target_faction_obj.territory_zones.remove(seized_territory)
                    primary_faction_obj.territory_zones.append(seized_territory)
                    primary_faction_obj.territories_gained.append(seized_territory)
                    target_faction_obj.territories_lost.append(seized_territory)
                    resolution_results['consequences'].append(f"{self.primary_faction} seizes {seized_territory}")
                    self.momentum_impact = 3.0
            elif random.random() < 0.3:  # 30% chance of casualties in territorial disputes
                # Bloody stalemate with martyrs
                primary_casualties = random.randint(1, 2)
                target_casualties = random.randint(1, 2)
                
                for _ in range(primary_casualties):
                    primary_faction_obj.martyrs_created.append(f"territorial_martyr_{datetime.now().strftime('%Y%m%d')}")
                for _ in range(target_casualties):
                    target_faction_obj.martyrs_created.append(f"territorial_martyr_{datetime.now().strftime('%Y%m%d')}")
                
                # Martyrs boost support but reduce operational capacity
                primary_faction_obj.public_support += primary_casualties * 4.0
                target_faction_obj.public_support += target_casualties * 4.0
                primary_faction_obj.operational_capacity = max(0.3, primary_faction_obj.operational_capacity - 0.1)
                target_faction_obj.operational_capacity = max(0.3, target_faction_obj.operational_capacity - 0.1)
                
                resolution_results['consequences'].append(f"Bloody territorial clash: {primary_casualties + target_casualties} martyrs created")
                self.momentum_impact = 2.5  # Martyrs create momentum
        
        elif self.conflict_type == FactionConflictType.DEFECTION_CAMPAIGN:
            # Attempting to encourage defections
            defection_appeal = primary_faction_obj.cooperation * (100 - target_faction_obj.public_support) / 100
            
            if defection_appeal > 0.6 and random.random() < 0.4:
                # Successful defection campaign
                self.winner = self.primary_faction
                support_transfer = random.uniform(3.0, 8.0)
                primary_faction_obj.public_support += support_transfer
                target_faction_obj.public_support -= support_transfer * 1.2  # Defections hurt more than they help
                resolution_results['consequences'].append(f"Defection campaign draws {support_transfer:.1f}% support away from {self.target_faction}")
                self.momentum_impact = 1.5
            else:
                # Failed defection campaign backfires
                primary_faction_obj.public_support -= 2.0
                target_faction_obj.public_support += 1.0  # Unity against external pressure
                resolution_results['consequences'].append(f"Failed defection campaign strengthens {self.target_faction} unity")
                self.momentum_impact = -0.5
        
        # Apply momentum impact
        resolution_results['momentum_impact'] = self.momentum_impact
        self.consequences = resolution_results['consequences']
        
        return resolution_results


@dataclass
class FactionAlliance:
    """Formal alliance between revolutionary factions - ITERATION 023"""
    alliance_name: str
    member_factions: List[str] = field(default_factory=list)
    formation_date: datetime = field(default_factory=datetime.now)
    trust_level: float = 50.0               # 0-100, overall alliance cohesion
    cooperation_momentum: float = 0.0       # -50 to +50, recent cooperation success
    
    # Joint activities
    joint_operations: List[str] = field(default_factory=list)
    shared_victories: int = 0
    cooperation_failures: int = 0
    
    # Stability tracking
    betrayal_risk: float = 0.1             # 0-1, chance of betrayal per turn
    alliance_strength: float = 1.0         # 0-2, effectiveness multiplier for joint ops
    last_joint_activity: Optional[datetime] = None
    
    def calculate_betrayal_risk(self, faction_relationships: Dict[str, 'FactionRelationship']) -> float:
        """Calculate current risk of alliance betrayal"""
        base_risk = 0.1
        
        # Low trust increases betrayal risk
        if self.trust_level < 30.0:
            base_risk += 0.3
        
        # Cooperation failures increase risk
        if self.cooperation_failures > self.shared_victories:
            base_risk += 0.2
        
        # Check individual faction relationships within alliance
        worst_relationship_trust = 100.0
        for i, faction_a in enumerate(self.member_factions):
            for j, faction_b in enumerate(self.member_factions):
                if i < j:
                    relationship_key = f"{faction_a}_{faction_b}"
                    alt_key = f"{faction_b}_{faction_a}"
                    relationship = faction_relationships.get(relationship_key) or faction_relationships.get(alt_key)
                    if relationship:
                        worst_relationship_trust = min(worst_relationship_trust, relationship.trust_rating)
        
        if worst_relationship_trust < 0:
            base_risk += 0.4  # Hostile members make alliance unstable
        
        # Positive momentum reduces risk
        if self.cooperation_momentum > 20.0:
            base_risk -= 0.2
        
        return max(0.0, min(1.0, base_risk))
    
    def execute_joint_activity(self, activity_type: JointActivityType, 
                             participating_factions: List['RevolutionaryFaction'],
                             faction_relationships: Dict[str, 'FactionRelationship']) -> Dict[str, Any]:
        """Execute a joint activity between alliance members"""
        results = {
            'activity_type': activity_type.value,
            'participants': [f.name for f in participating_factions],
            'success': False,
            'outcomes': [],
            'trust_change': 0.0,
            'momentum_impact': 0.0
        }
        
        # Calculate joint effectiveness
        combined_capacity = sum(f.operational_capacity for f in participating_factions)
        combined_support = sum(f.public_support for f in participating_factions) / len(participating_factions)
        
        # Activity-specific execution
        if activity_type == JointActivityType.COOP_PROPAGANDA:
            combined_media = sum(f.media_reach for f in participating_factions)
            success_chance = min(0.9, (combined_media + combined_support / 100) / 2)
            
            if random.random() < success_chance:
                results['success'] = True
                support_boost = random.uniform(3.0, 8.0) * len(participating_factions) * 0.5
                for faction in participating_factions:
                    faction.public_support += support_boost
                    faction.media_reach = min(1.0, faction.media_reach + 0.05)
                
                results['outcomes'].append(f"Joint propaganda campaign boosts support by {support_boost:.1f}% each")
                results['trust_change'] = 5.0
                results['momentum_impact'] = 2.0
                self.shared_victories += 1
            else:
                results['outcomes'].append("Joint propaganda campaign fails to resonate")
                results['trust_change'] = -2.0
                self.cooperation_failures += 1
        
        elif activity_type == JointActivityType.COMBINED_OPERATION:
            success_chance = min(0.8, combined_capacity / len(participating_factions))
            
            if random.random() < success_chance:
                results['success'] = True
                for faction in participating_factions:
                    faction.major_operations.append(f"joint_op_{datetime.now().strftime('%Y%m%d')}")
                    faction.government_heat += 1.5
                
                results['outcomes'].append(f"Combined operation successful with {len(participating_factions)} factions")
                results['trust_change'] = 8.0
                results['momentum_impact'] = 4.0 * len(participating_factions)
                self.shared_victories += 1
            else:
                results['outcomes'].append("Combined operation fails, coordination problems")
                results['trust_change'] = -5.0
                results['momentum_impact'] = -1.0
                
                # Failed joint ops can cause casualties
                if random.random() < 0.3:
                    casualty_faction = random.choice(participating_factions)
                    casualty_faction.martyrs_created.append(f"joint_op_martyr_{datetime.now().strftime('%Y%m%d')}")
                    results['outcomes'].append(f"{casualty_faction.name} suffers casualties in failed operation")
        
        elif activity_type == JointActivityType.JOINT_DEMONSTRATION:
            demo_power = combined_support * len(participating_factions) * 0.8
            
            if demo_power > 60.0:
                results['success'] = True
                for faction in participating_factions:
                    faction.public_support += 2.0
                
                results['outcomes'].append(f"Massive joint demonstration with {demo_power:.0f} participation power")
                results['trust_change'] = 4.0
                results['momentum_impact'] = 3.0
                self.shared_victories += 1
            else:
                results['outcomes'].append("Joint demonstration poorly attended")
                results['trust_change'] = -1.0
                results['momentum_impact'] = -1.0
                self.cooperation_failures += 1
        
        # Update alliance metrics
        self.trust_level = max(0.0, min(100.0, self.trust_level + results['trust_change']))
        self.cooperation_momentum += results['momentum_impact']
        self.cooperation_momentum = max(-50.0, min(50.0, self.cooperation_momentum))
        self.last_joint_activity = datetime.now()
        
        # Update betrayal risk
        self.betrayal_risk = self.calculate_betrayal_risk(faction_relationships)
        
        return results


@dataclass
class RevolutionaryFaction:
    """AI-controlled revolutionary faction operating independently"""
    name: str
    ideology: FactionIdeology
    
    # Core attributes
    aggression: float = 0.5        # 0-1, likelihood of violent/confrontational actions
    cooperation: float = 0.5       # 0-1, willingness to work with other factions
    public_support: float = 25.0   # 0-100, popular support level
    media_reach: float = 0.3       # 0-1, ability to influence public opinion
    
    # Territory and influence
    territory_zones: List[str] = field(default_factory=list)  # Cities of primary influence
    secondary_presence: List[str] = field(default_factory=list)  # Cities with minor presence
    
    # Current status
    current_activity: FactionActivityType = FactionActivityType.PASSIVE_RECRUITMENT
    activity_start_date: datetime = field(default_factory=datetime.now)
    activity_duration_days: int = 7  # How long current activity lasts
    
    # Relationships with player faction
    player_relationship: str = "neutral"  # "ally", "rival", "neutral", "hostile"
    cooperation_willingness: float = 0.5  # 0-1, specific to player faction
    sabotage_risk: float = 0.1            # 0-1, chance of undermining player operations
    
    # Historical tracking
    major_operations: List[str] = field(default_factory=list)
    martyrs_created: List[str] = field(default_factory=list)
    territories_gained: List[str] = field(default_factory=list)
    territories_lost: List[str] = field(default_factory=list)
    
    # Resources and capabilities
    operational_capacity: float = 1.0     # 0-2, ability to execute complex operations
    funding_level: float = 0.5           # 0-1, financial resources
    government_heat: float = 5.0         # 0-10, government attention/pressure
    
    # Faction Rivalry & Splinter System - ITERATION 022
    internal_divergence: float = 0.0      # 0-1, internal ideological disagreement
    faction_unity: float = 1.0           # 0-1, how cohesive the faction is
    split_threshold: float = 0.7         # When internal_divergence exceeds this, faction may split
    rivalry_targets: Set[str] = field(default_factory=set)  # Faction names we actively rival
    
    # Alliance tracking - ITERATION 023
    alliance_memberships: List[str] = field(default_factory=list)  # Names of alliances joined
    alliance_cooldown: Dict[str, datetime] = field(default_factory=dict)  # Faction -> last betrayal time
    preferred_alliance_partners: List[str] = field(default_factory=list)  # Faction names
    joint_operation_experience: int = 0         # Number of joint ops participated in
    factional_trust: float = 50.0               # 0-100, trust in other factions
    
    # Splinter tracking
    is_splinter_faction: bool = False
    parent_faction: Optional[str] = None
    splinter_date: Optional[datetime] = None
    inherited_support: float = 0.0       # Support inherited from parent faction

    def can_form_alliance_with(self, other_faction: 'RevolutionaryFaction', 
                              relationship: Optional['FactionRelationship'] = None) -> Tuple[bool, str]:
        """Check if this faction can form an alliance with another - ITERATION 023"""
        reasons = []
        
        # Cooldown check
        if other_faction.name in self.alliance_cooldown:
            cooldown_end = self.alliance_cooldown[other_faction.name] + timedelta(days=30)
            if datetime.now() < cooldown_end:
                return False, f"Alliance cooldown with {other_faction.name} still active"
        
        # Trust requirements
        if relationship:
            if relationship.trust_rating < 20.0:
                return False, "Insufficient trust for alliance formation"
            
            if relationship.rivalry_intensity > 70.0:
                return False, "Too much hostility for alliance"
        
        # Basic compatibility
        if self.factional_trust < 30.0:
            return False, "This faction has low general trust in alliances"
        
        if len(self.rivalry_targets) > 2:
            return False, "This faction is too hostile for cooperation"
        
        # Strategic alignment
        shared_enemies = False
        if self.government_heat > 6.0 and other_faction.government_heat > 6.0:
            shared_enemies = True
            reasons.append("Both factions face high government pressure")
        
        if self.public_support + other_faction.public_support < 40.0:
            reasons.append("Combined support creates strategic necessity")
            shared_enemies = True
        
        if shared_enemies or self.cooperation > 0.6:
            return True, f"Alliance viable: {', '.join(reasons)}"
        
        return False, "No compelling strategic reason for alliance"

    def calculate_alliance_value(self, other_faction: 'RevolutionaryFaction') -> float:
        """Calculate the strategic value of allying with another faction - ITERATION 023"""
        value = 0.0
        
        # Complementary strengths
        if other_faction.operational_capacity > self.operational_capacity:
            value += 20.0  # They bring operational expertise
        
        if other_faction.media_reach > self.media_reach:
            value += 15.0  # They bring media access
        
        if other_faction.public_support > self.public_support:
            value += 10.0  # They bring popular support
        
        # Resource synergy
        combined_resources = self.funding_level + other_faction.funding_level
        if combined_resources > 1.5:
            value += 15.0  # Strong resource base
        
        # Strategic necessity
        if self.government_heat > 6.0:
            value += 25.0  # Need allies when under pressure
        
        if self.public_support < 20.0:
            value += 20.0  # Need allies when unpopular
        
        # Experience factor
        if other_faction.joint_operation_experience > 2:
            value += 10.0  # They're good alliance partners
        
        return min(100.0, value)

    def execute_turn_activity(self, ecosystem: 'RevolutionaryEcosystem') -> Dict[str, any]:
        """Execute this faction's activity for the current turn"""
        activity_results = {
            'faction_name': self.name,
            'activity_type': self.current_activity.value,
            'outcomes': [],
            'city_effects': {},
            'narrative_events': []
        }
        
        # Check for faction split before other activities
        split_result = self.check_faction_split(ecosystem)
        if split_result:
            activity_results['faction_split'] = split_result
            return activity_results  # Faction split interrupts normal activity
        
        # Check if current activity is complete
        if (datetime.now() - self.activity_start_date).days >= self.activity_duration_days:
            # Complete current activity and choose new one
            completion_results = self._complete_current_activity(ecosystem)
            activity_results['outcomes'].extend(completion_results)
            
            # Choose new activity
            self._choose_next_activity(ecosystem)
            activity_results['new_activity'] = self.current_activity.value
        
        # Execute ongoing effects of current activity
        ongoing_effects = self._apply_ongoing_activity_effects(ecosystem)
        activity_results['ongoing_effects'] = ongoing_effects
        
        # Update internal divergence based on activities and outcomes
        self._update_internal_divergence(ecosystem)
        
        return activity_results
    
    def check_faction_split(self, ecosystem: 'RevolutionaryEcosystem') -> Optional[Dict[str, Any]]:
        """Check if faction should split due to internal divergence - ITERATION 022"""
        if self.internal_divergence < self.split_threshold:
            return None
        
        # Additional split conditions
        split_probability = (self.internal_divergence - self.split_threshold) * 2.0
        
        # Factors that increase split probability
        if self.faction_unity < 0.4:
            split_probability += 0.3
        
        if len(self.martyrs_created) >= 3:  # Many martyrs can cause ideological splits
            split_probability += 0.2
        
        if self.public_support < 20.0:  # Low support increases internal stress
            split_probability += 0.2
        
        # Random chance of split
        if random.random() < split_probability:
            return self._execute_faction_split(ecosystem)
        
        return None
    
    def _execute_faction_split(self, ecosystem: 'RevolutionaryEcosystem') -> Dict[str, Any]:
        """Execute a faction split - ITERATION 022"""
        split_results = {
            'event_type': 'faction_split',
            'parent_faction': self.name,
            'split_reason': '',
            'new_faction_name': '',
            'support_division': {},
            'territory_division': {}
        }
        
        # Determine split type and reason
        if len(self.martyrs_created) >= 2:
            split_type = FactionConflictType.MARTYR_SPLIT
            split_results['split_reason'] = "Disagreement over martyrdom tactics and commemoration"
            splinter_suffix = "Memorial Brigade"
        elif self.ideology == FactionIdeology.SOCIALIST and random.random() < 0.6:
            split_type = FactionConflictType.FRACTURE_REVOLUTION  
            split_results['split_reason'] = "Ideological fracture over revolutionary methods"
            splinter_suffix = "Revolutionary Guard"
        else:
            split_type = FactionConflictType.DOCTRINAL_DOMINATION
            split_results['split_reason'] = "Doctrinal disagreement leading to faction purge"
            splinter_suffix = "Liberation Front"
        
        # Create splinter faction
        splinter_name = f"{self.name.split()[0]} {splinter_suffix}"
        split_results['new_faction_name'] = splinter_name
        
        # Determine support and territory division
        splinter_support_ratio = random.uniform(0.2, 0.4)  # Splinter gets 20-40% of original support
        original_support = self.public_support
        
        splinter_support = original_support * splinter_support_ratio
        remaining_support = original_support * (1 - splinter_support_ratio) * 0.8  # Some support lost in split
        
        # Create splinter faction
        splinter_faction = RevolutionaryFaction(
            name=splinter_name,
            ideology=self.ideology,  # Same ideology but different interpretation
            aggression=min(1.0, self.aggression + random.uniform(-0.2, 0.3)),  # Slightly different aggression
            cooperation=max(0.0, self.cooperation - 0.2),  # Less cooperative after split
            public_support=splinter_support,
            media_reach=self.media_reach * 0.6,  # Reduced media reach
            is_splinter_faction=True,
            parent_faction=self.name,
            splinter_date=datetime.now(),
            inherited_support=splinter_support
        )
        
        # Divide territories
        if len(self.territory_zones) > 1:
            territories_to_split = random.sample(self.territory_zones, 
                                               len(self.territory_zones) // 2)
            for territory in territories_to_split:
                self.territory_zones.remove(territory)
                splinter_faction.territory_zones.append(territory)
            
            split_results['territory_division'] = {
                'original_keeps': self.territory_zones,
                'splinter_gets': splinter_faction.territory_zones
            }
        
        # Update original faction
        self.public_support = remaining_support
        self.faction_unity = 0.3  # Low unity after split
        self.internal_divergence = 0.1  # Reset divergence
        self.operational_capacity = max(0.4, self.operational_capacity - 0.3)  # Reduced capacity
        
        # Add rivalry between original and splinter
        self.rivalry_targets.add(splinter_name)
        splinter_faction.rivalry_targets.add(self.name)
        
        # Add splinter faction to ecosystem
        ecosystem.active_factions.append(splinter_faction)
        
        # Create faction relationship with immediate hostility
        relationship_key = f"{self.name}_{splinter_name}"
        ecosystem.faction_relationships[relationship_key] = FactionRelationship(
            faction_a=self.name,
            faction_b=splinter_name,
            trust_rating=-60.0,  # Immediate hostility after split
            rivalry_intensity=40.0
        )
        
        split_results['support_division'] = {
            'original_faction': remaining_support,
            'splinter_faction': splinter_support,
            'support_lost': original_support - remaining_support - splinter_support
        }
        
        return split_results
    
    def _update_internal_divergence(self, ecosystem: 'RevolutionaryEcosystem') -> None:
        """Update internal ideological divergence based on faction activities and outcomes"""
        # Base divergence change
        divergence_change = 0.0
        
        # Failed operations increase divergence
        recent_failures = len([op for op in self.major_operations[-3:] if 'failed' in op.lower()])
        divergence_change += recent_failures * 0.05
        
        # High government heat increases internal stress
        if self.government_heat > 7.0:
            divergence_change += 0.02
        
        # Rivalry with other factions can cause internal disagreement
        if len(self.rivalry_targets) > 1:
            divergence_change += 0.03
        
        # Low unity accelerates divergence
        if self.faction_unity < 0.5:
            divergence_change += 0.04
        
        # High aggression factions are more prone to splits
        if self.aggression > 0.7:
            divergence_change += 0.02
        
        # Success and good leadership reduce divergence
        if self.public_support > 40.0:
            divergence_change -= 0.02
        
        if self.operational_capacity > 1.5:
            divergence_change -= 0.03
        
        # Apply change with bounds
        self.internal_divergence = max(0.0, min(1.0, self.internal_divergence + divergence_change))
        
        # Unity tends to correlate inversely with divergence
        self.faction_unity = max(0.1, min(1.0, 1.0 - self.internal_divergence * 0.8))
    
    def initiate_rivalry_action(self, target_faction: 'RevolutionaryFaction',
                              ecosystem: 'RevolutionaryEcosystem') -> Optional[FactionConflictEvent]:
        """Initiate a rivalry action against another faction - ITERATION 022"""
        if target_faction.name not in self.rivalry_targets:
            return None
        
        # Determine conflict type based on faction characteristics
        possible_conflicts = []
        
        if self.media_reach > 0.4:
            possible_conflicts.append(FactionConflictType.PROPAGANDA_WAR)
        
        if any(city in target_faction.territory_zones for city in self.territory_zones):
            possible_conflicts.append(FactionConflictType.TERRITORIAL_DISPUTE)
        
        if self.cooperation > 0.3:  # Paradoxically, cooperative factions can run defection campaigns
            possible_conflicts.append(FactionConflictType.DEFECTION_CAMPAIGN)
        
        if not possible_conflicts:
            possible_conflicts.append(FactionConflictType.COVERT_RIVALRY)
        
        conflict_type = random.choice(possible_conflicts)
        
        # Create conflict event
        conflict_event = FactionConflictEvent(
            conflict_type=conflict_type,
            primary_faction=self.name,
            target_faction=target_faction.name,
            trigger_date=datetime.now(),
            description=f"{self.name} initiates {conflict_type.value} against {target_faction.name}",
            intensity=random.uniform(1.0, 2.5)
        )
        
        return conflict_event
    
    def _complete_current_activity(self, ecosystem: 'RevolutionaryEcosystem') -> List[str]:
        """Complete current activity and apply its effects"""
        outcomes = []
        
        if self.current_activity == FactionActivityType.PROPAGANDA_CAMPAIGN:
            # Increase public support and media reach
            support_gain = random.uniform(2.0, 8.0) * self.media_reach
            self.public_support = min(100.0, self.public_support + support_gain)
            outcomes.append(f"Propaganda campaign increased support by {support_gain:.1f}")
            
            # Affect cities in territory
            for city in self.territory_zones:
                if city in ecosystem.city_reputations:
                    city_rep = ecosystem.city_reputations[city]
                    city_rep.reputation_score += support_gain * 0.5
                    city_rep.popular_support += support_gain * 0.01
        
        elif self.current_activity == FactionActivityType.SABOTAGE_OPERATION:
            # Execute sabotage with success based on operational capacity
            success_chance = self.operational_capacity * 0.7
            if random.random() < success_chance:
                target_city = random.choice(self.territory_zones) if self.territory_zones else "unknown"
                self.major_operations.append(f"sabotage_{target_city}_{datetime.now().strftime('%Y%m%d')}")
                outcomes.append(f"Successful sabotage operation in {target_city}")
                
                # Increase government heat
                self.government_heat = min(10.0, self.government_heat + 2.0)
                
                # Affect city if tracked
                if target_city in ecosystem.city_reputations:
                    city_rep = ecosystem.city_reputations[target_city]
                    city_rep.government_heat += 1.5
                    city_rep.reputation_score += 5.0  # Sabotage can boost reputation
            else:
                outcomes.append("Sabotage operation failed")
                self.government_heat += 1.0
        
        elif self.current_activity == FactionActivityType.MASS_DEMONSTRATION:
            # Organize public demonstration
            demo_size = self.public_support * random.uniform(0.5, 1.5)
            if demo_size > 30.0:  # Successful demonstration
                outcomes.append(f"Large demonstration with {demo_size:.0f}% participation equivalent")
                self.media_reach = min(1.0, self.media_reach + 0.1)
                
                # Government response based on aggression
                if self.aggression > 0.7:
                    # Aggressive faction likely to have violent clashes
                    if random.random() < 0.4:
                        casualties = random.randint(1, 3)
                        self.martyrs_created.append(f"demo_martyr_{datetime.now().strftime('%Y%m%d')}")
                        outcomes.append(f"Demonstration turned violent, {casualties} martyrs created")
                        self.public_support += casualties * 3.0  # Martyrdom boosts support
            else:
                outcomes.append("Small demonstration with limited impact")
        
        elif self.current_activity == FactionActivityType.RIVAL_CONFRONTATION:
            # Confront rival faction
            target_faction = self._select_rival_faction(ecosystem)
            if target_faction:
                confrontation_result = self._resolve_faction_confrontation(target_faction)
                outcomes.append(f"Confrontation with {target_faction.name}: {confrontation_result}")
        
        return outcomes
    
    def _choose_next_activity(self, ecosystem: 'RevolutionaryEcosystem') -> None:
        """Choose next activity based on faction characteristics and situation"""
        # Weight activities based on faction ideology and traits
        activity_weights = {}
        
        # Base weights
        if self.ideology == FactionIdeology.ANARCHIST:
            activity_weights[FactionActivityType.SABOTAGE_OPERATION] = 0.3
            activity_weights[FactionActivityType.MASS_DEMONSTRATION] = 0.2
        elif self.ideology == FactionIdeology.SOCIALIST:
            activity_weights[FactionActivityType.PROPAGANDA_CAMPAIGN] = 0.3
            activity_weights[FactionActivityType.UNDERGROUND_ORGANIZING] = 0.2
        elif self.ideology == FactionIdeology.MILITANT_COMMUNIST:
            activity_weights[FactionActivityType.ASSASSINATION_ATTEMPT] = 0.2
            activity_weights[FactionActivityType.RIVAL_CONFRONTATION] = 0.2
        
        # Aggression influences violent activities
        if self.aggression > 0.7:
            activity_weights[FactionActivityType.SABOTAGE_OPERATION] = activity_weights.get(FactionActivityType.SABOTAGE_OPERATION, 0) + 0.2
            activity_weights[FactionActivityType.ASSASSINATION_ATTEMPT] = activity_weights.get(FactionActivityType.ASSASSINATION_ATTEMPT, 0) + 0.15
        
        # Cooperation influences collaborative activities
        if self.cooperation > 0.6:
            activity_weights[FactionActivityType.COOPERATION_MISSION] = 0.15
        
        # Low support factions focus on recruitment
        if self.public_support < 30.0:
            activity_weights[FactionActivityType.PASSIVE_RECRUITMENT] = 0.25
            activity_weights[FactionActivityType.UNDERGROUND_ORGANIZING] = 0.2
        
        # High government heat makes factions more cautious
        if self.government_heat > 7.0:
            activity_weights[FactionActivityType.PASSIVE_RECRUITMENT] = activity_weights.get(FactionActivityType.PASSIVE_RECRUITMENT, 0) + 0.2
            # Reduce violent activities
            for violent_activity in [FactionActivityType.SABOTAGE_OPERATION, FactionActivityType.ASSASSINATION_ATTEMPT]:
                if violent_activity in activity_weights:
                    activity_weights[violent_activity] *= 0.5
        
        # Ensure all activities have some weight
        all_activities = list(FactionActivityType)
        for activity in all_activities:
            if activity not in activity_weights:
                activity_weights[activity] = 0.05
        
        # Choose weighted random activity
        activities = list(activity_weights.keys())
        weights = list(activity_weights.values())
        
        chosen_activity = random.choices(activities, weights=weights)[0]
        self.current_activity = chosen_activity
        self.activity_start_date = datetime.now()
        
        # Set duration based on activity type
        duration_map = {
            FactionActivityType.PASSIVE_RECRUITMENT: random.randint(10, 20),
            FactionActivityType.PROPAGANDA_CAMPAIGN: random.randint(5, 10),
            FactionActivityType.SABOTAGE_OPERATION: random.randint(3, 7),
            FactionActivityType.ASSASSINATION_ATTEMPT: random.randint(2, 5),
            FactionActivityType.MASS_DEMONSTRATION: random.randint(1, 3),
            FactionActivityType.UNDERGROUND_ORGANIZING: random.randint(7, 14),
            FactionActivityType.RIVAL_CONFRONTATION: random.randint(1, 4),
            FactionActivityType.COOPERATION_MISSION: random.randint(3, 8)
        }
        
        self.activity_duration_days = duration_map.get(chosen_activity, 7)
    
    def _apply_ongoing_activity_effects(self, ecosystem: 'RevolutionaryEcosystem') -> Dict[str, any]:
        """Apply ongoing effects of current activity"""
        effects = {}
        
        if self.current_activity == FactionActivityType.PASSIVE_RECRUITMENT:
            # Slowly build support and reduce government heat
            daily_support_gain = 0.3
            self.public_support = min(100.0, self.public_support + daily_support_gain)
            self.government_heat = max(0.0, self.government_heat - 0.1)
            effects['support_gain'] = daily_support_gain
            
        elif self.current_activity == FactionActivityType.UNDERGROUND_ORGANIZING:
            # Build operational capacity
            capacity_gain = 0.02
            self.operational_capacity = min(2.0, self.operational_capacity + capacity_gain)
            effects['capacity_gain'] = capacity_gain
        
        return effects
    
    def _select_rival_faction(self, ecosystem: 'RevolutionaryEcosystem') -> Optional['RevolutionaryFaction']:
        """Select a rival faction for confrontation"""
        potential_rivals = []
        for faction in ecosystem.active_factions:
            if faction != self and faction.name != self.name:
                # Ideological conflicts
                if self._are_ideologically_opposed(faction):
                    potential_rivals.append(faction)
                # Territory conflicts
                elif any(city in faction.territory_zones for city in self.territory_zones):
                    potential_rivals.append(faction)
        
        return random.choice(potential_rivals) if potential_rivals else None
    
    def _are_ideologically_opposed(self, other_faction: 'RevolutionaryFaction') -> bool:
        """Check if two factions have opposing ideologies"""
        opposition_map = {
            FactionIdeology.ANARCHIST: [FactionIdeology.MILITANT_COMMUNIST],
            FactionIdeology.NATIONALIST: [FactionIdeology.SOCIALIST, FactionIdeology.MILITANT_COMMUNIST],
            FactionIdeology.RELIGIOUS: [FactionIdeology.ANARCHIST, FactionIdeology.MILITANT_COMMUNIST],
            FactionIdeology.LIBERAL_DEMOCRATIC: [FactionIdeology.MILITANT_COMMUNIST, FactionIdeology.ANARCHIST],
            FactionIdeology.MILITANT_COMMUNIST: [FactionIdeology.ANARCHIST, FactionIdeology.NATIONALIST, FactionIdeology.RELIGIOUS, FactionIdeology.LIBERAL_DEMOCRATIC]
        }
        
        return other_faction.ideology in opposition_map.get(self.ideology, [])
    
    def _resolve_faction_confrontation(self, target_faction: 'RevolutionaryFaction') -> str:
        """Resolve confrontation between factions"""
        # Simple confrontation resolution based on operational capacity and aggression
        our_strength = self.operational_capacity * self.aggression
        their_strength = target_faction.operational_capacity * target_faction.aggression
        
        if our_strength > their_strength * 1.2:
            # We win decisively
            self.public_support += 5.0
            target_faction.public_support -= 8.0
            return "decisive victory"
        elif our_strength > their_strength:
            # We win narrowly
            self.public_support += 2.0
            target_faction.public_support -= 3.0
            return "narrow victory"
        elif their_strength > our_strength * 1.2:
            # We lose decisively
            self.public_support -= 8.0
            target_faction.public_support += 5.0
            return "decisive defeat"
        else:
            # Stalemate
            both_casualties = random.randint(0, 2)
            if both_casualties > 0:
                self.martyrs_created.append(f"confrontation_martyr_{datetime.now().strftime('%Y%m%d')}")
                target_faction.martyrs_created.append(f"confrontation_martyr_{datetime.now().strftime('%Y%m%d')}")
            return f"bloody stalemate ({both_casualties} casualties each)"


@dataclass
class UprisingClock:
    """Global timeline tracking revolutionary momentum and events"""
    current_date: datetime = field(default_factory=datetime.now)
    days_since_start: int = 0
    
    # Global revolutionary momentum
    national_uprising_momentum: float = 0.0    # 0-100, how close to national uprising
    government_stability: float = 80.0         # 0-100, regime stability
    international_attention: float = 0.0       # 0-100, global awareness
    
    # Event tracking
    major_events: List[Dict[str, any]] = field(default_factory=list)
    faction_interactions: List[Dict[str, any]] = field(default_factory=list)
    
    def advance_day(self) -> None:
        """Advance the uprising clock by one day"""
        self.current_date += timedelta(days=1)
        self.days_since_start += 1
        
        # Natural momentum decay
        self.national_uprising_momentum = max(0.0, self.national_uprising_momentum - 0.1)
    
    def record_faction_event(self, faction_name: str, event_type: str, description: str, 
                           momentum_impact: float = 0.0) -> None:
        """Record a significant faction event"""
        event = {
            'date': self.current_date,
            'faction': faction_name,
            'type': event_type,
            'description': description,
            'momentum_impact': momentum_impact
        }
        
        self.major_events.append(event)
        self.national_uprising_momentum = min(100.0, max(0.0, 
            self.national_uprising_momentum + momentum_impact))


@dataclass
class AlliancePropagandaEvent:
    """Propaganda event around alliance formation, cooperation, or betrayal - ITERATION 024"""
    event_type: str                                         # "alliance_formation", "joint_success", "betrayal"
    propaganda_tone: PropagandaTone
    initiating_faction: str
    target_factions: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Media characteristics
    media_saturation: float = 0.5                          # 0-1, how much media coverage
    public_reaction: float = 0.0                           # -1 to +1, public reception
    narrative_strength: float = 1.0                       # 0-2, effectiveness of message
    
    # Outcome tracking
    support_changes: Dict[str, float] = field(default_factory=dict)  # Faction -> support delta
    trust_impacts: Dict[str, float] = field(default_factory=dict)   # Alliance -> trust delta
    counter_narratives: List[str] = field(default_factory=list)     # Competing propaganda
    
    def execute_propaganda_campaign(self, ecosystem: 'RevolutionaryEcosystem') -> Dict[str, Any]:
        """Execute the propaganda campaign and calculate impacts"""
        results = {
            'propaganda_type': self.propaganda_tone.value,
            'initiator': self.initiating_faction,
            'media_coverage': self.media_saturation,
            'public_response': self.public_reaction,
            'support_changes': {},
            'trust_changes': {},
            'narrative_success': False
        }
        
        initiator = next((f for f in ecosystem.active_factions if f.name == self.initiating_faction), None)
        if not initiator:
            return results
        
        # Calculate propaganda effectiveness
        base_effectiveness = initiator.media_reach * self.narrative_strength
        saturation_bonus = self.media_saturation * 0.5
        total_effectiveness = min(1.0, base_effectiveness + saturation_bonus)
        
        # Apply tone-specific effects
        if self.propaganda_tone == PropagandaTone.UNITY_AGAINST_OPPRESSION:
            # Boost support for alliance members
            for faction_name in [self.initiating_faction] + self.target_factions:
                faction = next((f for f in ecosystem.active_factions if f.name == faction_name), None)
                if faction:
                    support_boost = total_effectiveness * random.uniform(2.0, 6.0)
                    faction.public_support += support_boost
                    self.support_changes[faction_name] = support_boost
                    results['support_changes'][faction_name] = support_boost
            
            # Boost trust in alliances involving these factions
            for alliance in ecosystem.active_alliances.values():
                if self.initiating_faction in alliance.member_factions:
                    trust_boost = total_effectiveness * random.uniform(3.0, 8.0)
                    alliance.trust_level = min(100.0, alliance.trust_level + trust_boost)
                    self.trust_impacts[alliance.alliance_name] = trust_boost
                    results['trust_changes'][alliance.alliance_name] = trust_boost
            
            results['narrative_success'] = total_effectiveness > 0.6
        
        elif self.propaganda_tone == PropagandaTone.BETRAYAL_OF_CAUSE:
            # Damage betrayer's support and credibility
            for target_name in self.target_factions:
                target_faction = next((f for f in ecosystem.active_factions if f.name == target_name), None)
                if target_faction:
                    support_damage = total_effectiveness * random.uniform(3.0, 10.0)
                    target_faction.public_support = max(0.0, target_faction.public_support - support_damage)
                    target_faction.factional_trust = max(0.0, target_faction.factional_trust - support_damage * 0.5)
                    self.support_changes[target_name] = -support_damage
                    results['support_changes'][target_name] = -support_damage
            
            # Boost initiator's credibility slightly
            support_boost = total_effectiveness * random.uniform(1.0, 4.0)
            initiator.public_support += support_boost
            self.support_changes[self.initiating_faction] = support_boost
            results['support_changes'][self.initiating_faction] = support_boost
            
            results['narrative_success'] = total_effectiveness > 0.5
        
        elif self.propaganda_tone == PropagandaTone.HEROIC_COOPERATION:
            # Celebrate joint successes
            involved_factions = [self.initiating_faction] + self.target_factions
            for faction_name in involved_factions:
                faction = next((f for f in ecosystem.active_factions if f.name == faction_name), None)
                if faction:
                    support_boost = total_effectiveness * random.uniform(1.5, 5.0)
                    faction.public_support += support_boost
                    faction.media_reach = min(1.0, faction.media_reach + 0.02)
                    self.support_changes[faction_name] = support_boost
                    results['support_changes'][faction_name] = support_boost
            
            results['narrative_success'] = total_effectiveness > 0.4
        
        elif self.propaganda_tone == PropagandaTone.ALLIANCE_NECESSITY:
            # Justify alliance decisions
            faction = next((f for f in ecosystem.active_factions if f.name == self.initiating_faction), None)
            if faction:
                support_boost = total_effectiveness * random.uniform(0.5, 3.0)
                faction.public_support += support_boost
                self.support_changes[self.initiating_faction] = support_boost
                results['support_changes'][self.initiating_faction] = support_boost
            
            results['narrative_success'] = total_effectiveness > 0.3
        
        elif self.propaganda_tone == PropagandaTone.TRAITOR_EXPOSURE:
            # Expose supposed traitors
            for target_name in self.target_factions:
                target_faction = next((f for f in ecosystem.active_factions if f.name == target_name), None)
                if target_faction:
                    support_damage = total_effectiveness * random.uniform(2.0, 7.0)
                    target_faction.public_support = max(0.0, target_faction.public_support - support_damage)
                    self.support_changes[target_name] = -support_damage
                    results['support_changes'][target_name] = -support_damage
            
            # Small boost for exposer
            support_boost = total_effectiveness * random.uniform(0.5, 2.0)
            initiator.public_support += support_boost
            self.support_changes[self.initiating_faction] = support_boost
            results['support_changes'][self.initiating_faction] = support_boost
            
            results['narrative_success'] = total_effectiveness > 0.4
        
        # Media saturation affects future propaganda effectiveness
        self.media_saturation = max(0.1, self.media_saturation - 0.1)  # Saturation decay
        
        return results


@dataclass
class RevolutionaryEcosystem:
    """Manages multiple revolutionary factions and their interactions"""
    active_factions: List[RevolutionaryFaction] = field(default_factory=list)
    uprising_clock: UprisingClock = field(default_factory=UprisingClock)
    city_reputations: Dict[str, any] = field(default_factory=dict)  # Reference to campaign city data
    
    # Inter-faction relationship system - ITERATION 022
    faction_relationships: Dict[str, FactionRelationship] = field(default_factory=dict)
    active_conflicts: List[FactionConflictEvent] = field(default_factory=list)
    conflict_history: List[FactionConflictEvent] = field(default_factory=list)
    
    # Alliance system - ITERATION 023
    active_alliances: Dict[str, FactionAlliance] = field(default_factory=dict)
    alliance_events: List[Dict[str, Any]] = field(default_factory=list)
    alliance_formation_threshold: float = 60.0  # Combined cooperation + trust needed
    
    # Propaganda narrative system - ITERATION 024
    propaganda_events: List[AlliancePropagandaEvent] = field(default_factory=list)
    media_saturation_level: float = 0.3  # 0-1, current media attention on alliances
    
    def trigger_propaganda_event(self, event_type: str, initiator: str, 
                                targets: List[str] = None, tone: PropagandaTone = None) -> AlliancePropagandaEvent:
        """Trigger a propaganda event around alliance activities - ITERATION 024"""
        if targets is None:
            targets = []
        
        # Auto-select propaganda tone based on event type if not specified
        if tone is None:
            if event_type == "alliance_formation":
                tone = PropagandaTone.UNITY_AGAINST_OPPRESSION
            elif event_type == "joint_success":
                tone = PropagandaTone.HEROIC_COOPERATION
            elif event_type == "betrayal":
                tone = PropagandaTone.BETRAYAL_OF_CAUSE
            else:
                tone = PropagandaTone.ALLIANCE_NECESSITY
        
        # Create propaganda event
        propaganda_event = AlliancePropagandaEvent(
            event_type=event_type,
            propaganda_tone=tone,
            initiating_faction=initiator,
            target_factions=targets,
            media_saturation=min(1.0, self.media_saturation_level + 0.2),
            narrative_strength=random.uniform(0.8, 1.5)
        )
        
        # Execute the propaganda campaign
        results = propaganda_event.execute_propaganda_campaign(self)
        
        # Store event and results
        self.propaganda_events.append(propaganda_event)
        
        # Update global media saturation
        self.media_saturation_level = min(1.0, self.media_saturation_level + 0.1)
        
        return propaganda_event
    
    def execute_narrative_wars(self) -> List[Dict[str, Any]]:
        """Execute propaganda narrative wars between factions - ITERATION 024"""
        narrative_results = []
        
        # Check for counter-propaganda opportunities
        for faction in self.active_factions:
            if faction.media_reach > 0.4 and random.random() < 0.3:  # 30% chance if high media reach
                
                # Look for recent propaganda to counter
                recent_propaganda = [p for p in self.propaganda_events[-3:] 
                                   if faction.name not in [p.initiating_faction] + p.target_factions]
                
                if recent_propaganda:
                    target_propaganda = recent_propaganda[-1]  # Counter most recent
                    
                    # Determine counter-narrative tone
                    if target_propaganda.propaganda_tone == PropagandaTone.UNITY_AGAINST_OPPRESSION:
                        counter_tone = PropagandaTone.BETRAYAL_OF_CAUSE
                        targets = [target_propaganda.initiating_faction]
                    elif target_propaganda.propaganda_tone == PropagandaTone.BETRAYAL_OF_CAUSE:
                        counter_tone = PropagandaTone.UNITY_AGAINST_OPPRESSION
                        targets = target_propaganda.target_factions
                    else:
                        counter_tone = PropagandaTone.TRAITOR_EXPOSURE
                        targets = [target_propaganda.initiating_faction]
                    
                    # Launch counter-propaganda
                    counter_event = self.trigger_propaganda_event(
                        "counter_narrative", faction.name, targets, counter_tone
                    )
                    
                    narrative_results.append({
                        'type': 'counter_propaganda',
                        'initiator': faction.name,
                        'targets': targets,
                        'tone': counter_tone.value,
                        'effectiveness': counter_event.narrative_strength
                    })
        
        # Media saturation decay
        self.media_saturation_level = max(0.1, self.media_saturation_level - 0.05)
        
        return narrative_results

    def initialize_default_factions(self) -> None:
        """Initialize 2-3 default AI factions for testing"""
        # Socialist Workers' Movement
        socialist_faction = RevolutionaryFaction(
            name="People's Liberation Front",
            ideology=FactionIdeology.SOCIALIST,
            aggression=0.4,
            cooperation=0.7,
            public_support=35.0,
            media_reach=0.4,
            territory_zones=["Industrial District", "Port City"],
            player_relationship="neutral",
            cooperation_willingness=0.6
        )
        
        # Anarchist Collective
        anarchist_faction = RevolutionaryFaction(
            name="Black Flag Collective",
            ideology=FactionIdeology.ANARCHIST,
            aggression=0.8,
            cooperation=0.3,
            public_support=20.0,
            media_reach=0.2,
            territory_zones=["University Quarter"],
            player_relationship="neutral",
            cooperation_willingness=0.3,
            sabotage_risk=0.2
        )
        
        # Nationalist Movement
        nationalist_faction = RevolutionaryFaction(
            name="National Liberation Army",
            ideology=FactionIdeology.NATIONALIST,
            aggression=0.6,
            cooperation=0.4,
            public_support=45.0,
            media_reach=0.5,
            territory_zones=["Border Region", "Mountain Towns"],
            player_relationship="neutral",
            cooperation_willingness=0.4
        )
        
        self.active_factions = [socialist_faction, anarchist_faction, nationalist_faction]
        
        # Initialize inter-faction relationships - ITERATION 022
        self._initialize_faction_relationships()
    
    def _initialize_faction_relationships(self) -> None:
        """Initialize relationships between all factions"""
        for i, faction_a in enumerate(self.active_factions):
            for j, faction_b in enumerate(self.active_factions):
                if i < j:  # Avoid duplicate relationships
                    relationship_key = f"{faction_a.name}_{faction_b.name}"
                    
                    # Calculate initial trust based on ideological compatibility
                    initial_trust = self._calculate_initial_trust(faction_a, faction_b)
                    
                    relationship = FactionRelationship(
                        faction_a=faction_a.name,
                        faction_b=faction_b.name,
                        trust_rating=initial_trust
                    )
                    
                    self.faction_relationships[relationship_key] = relationship
                    
                    # Set up initial rivalries for opposing ideologies
                    if initial_trust < -20.0:
                        faction_a.rivalry_targets.add(faction_b.name)
                        faction_b.rivalry_targets.add(faction_a.name)
                        relationship.rivalry_intensity = 20.0
    
    def _calculate_initial_trust(self, faction_a: RevolutionaryFaction, 
                               faction_b: RevolutionaryFaction) -> float:
        """Calculate initial trust between two factions based on ideology"""
        # Base compatibility
        if faction_a.ideology == faction_b.ideology:
            base_trust = 30.0  # Same ideology = positive start
        elif faction_a._are_ideologically_opposed(faction_b):
            base_trust = -40.0  # Opposing ideologies = hostility
        else:
            base_trust = 0.0  # Neutral ideologies
        
        # Cooperation levels affect trust
        cooperation_factor = (faction_a.cooperation + faction_b.cooperation) * 15.0
        
        # Aggression differences create tension
        aggression_difference = abs(faction_a.aggression - faction_b.aggression)
        aggression_penalty = aggression_difference * -20.0
        
        # Territory overlap creates tension
        territory_overlap = len(set(faction_a.territory_zones) & set(faction_b.territory_zones))
        territory_penalty = territory_overlap * -15.0
        
        final_trust = base_trust + cooperation_factor + aggression_penalty + territory_penalty
        return max(-100.0, min(100.0, final_trust))
    
    def simulate_ecosystem_turn(self) -> Dict[str, any]:
        """Simulate one turn of the revolutionary ecosystem"""
        turn_results = {
            'date': self.uprising_clock.current_date,
            'faction_activities': [],
            'major_events': [],
            'faction_conflicts': [],
            'faction_splits': [],
            'alliance_activities': {},  # ITERATION 023: Alliance activities
            'ecosystem_changes': {}
        }
        
        # Advance the clock
        self.uprising_clock.advance_day()
        
        # Each faction executes their turn
        for faction in self.active_factions[:]:  # Use slice to allow list modification
            faction_results = faction.execute_turn_activity(self)
            turn_results['faction_activities'].append(faction_results)
            
            # Handle faction splits
            if 'faction_split' in faction_results:
                turn_results['faction_splits'].append(faction_results['faction_split'])
                self.uprising_clock.record_faction_event(
                    faction.name,
                    "faction_split",
                    f"Faction split: {faction_results['faction_split']['split_reason']}",
                    -5.0  # Splits generally hurt momentum
                )
            
            # Record significant events
            if faction_results['outcomes']:
                for outcome in faction_results['outcomes']:
                    momentum_impact = self._calculate_momentum_impact(faction, outcome)
                    self.uprising_clock.record_faction_event(
                        faction.name, 
                        faction.current_activity.value,
                        outcome,
                        momentum_impact
                    )
        
        # Process alliance activities - ITERATION 023
        alliance_turn_results = self.simulate_alliance_turn()
        turn_results['alliance_activities'] = alliance_turn_results
        
        # Record alliance events in uprising clock
        for joint_op in alliance_turn_results.get('joint_operations', []):
            if joint_op['success']:
                momentum_impact = joint_op.get('momentum_impact', 0.0)
                self.uprising_clock.record_faction_event(
                    joint_op['alliance_name'],
                    "joint_operation",
                    f"Successful {joint_op['activity_type']}: {'; '.join(joint_op['outcomes'])}",
                    momentum_impact
                )
        
        # Process inter-faction rivalries and conflicts
        rivalry_conflicts = self._process_faction_rivalries()
        turn_results['faction_conflicts'] = rivalry_conflicts
        
        # Resolve active conflicts
        resolved_conflicts = self._resolve_active_conflicts()
        if resolved_conflicts:
            turn_results['major_events'].extend(resolved_conflicts)
        
        # Check for ecosystem-wide events
        ecosystem_events = self._check_ecosystem_events()
        turn_results['major_events'].extend(ecosystem_events)
        
        return turn_results
    
    def _process_faction_rivalries(self) -> List[Dict[str, Any]]:
        """Process rivalry actions between factions - ITERATION 022"""
        rivalry_events = []
        
        for faction in self.active_factions:
            if faction.rivalry_targets and random.random() < 0.3:  # 30% chance of rivalry action
                # Select a random rival
                target_name = random.choice(list(faction.rivalry_targets))
                target_faction = next((f for f in self.active_factions if f.name == target_name), None)
                
                if target_faction:
                    conflict_event = faction.initiate_rivalry_action(target_faction, self)
                    if conflict_event:
                        self.active_conflicts.append(conflict_event)
                        rivalry_events.append({
                            'initiator': faction.name,
                            'target': target_faction.name,
                            'conflict_type': conflict_event.conflict_type.value,
                            'description': conflict_event.description
                        })
        
        return rivalry_events
    
    def _resolve_active_conflicts(self) -> List[str]:
        """Resolve active faction conflicts and return narrative results"""
        resolved_events = []
        
        for conflict in self.active_conflicts[:]:  # Use slice to allow list modification
            # Find the faction objects
            primary_faction = next((f for f in self.active_factions if f.name == conflict.primary_faction), None)
            target_faction = next((f for f in self.active_factions if f.name == conflict.target_faction), None)
            
            if primary_faction and target_faction:
                resolution = conflict.resolve_conflict(primary_faction, target_faction, self)
                
                # Update faction relationship
                relationship = self._get_faction_relationship(conflict.primary_faction, conflict.target_faction)
                if relationship:
                    if conflict.winner == conflict.primary_faction:
                        relationship.adjust_trust(-10.0, f"Lost {conflict.conflict_type.value}")
                        relationship.escalate_rivalry(5.0, conflict.conflict_type.value)
                    elif conflict.winner == conflict.target_faction:
                        relationship.adjust_trust(-5.0, f"Failed {conflict.conflict_type.value}")
                        relationship.escalate_rivalry(3.0, conflict.conflict_type.value)
                    else:
                        relationship.escalate_rivalry(2.0, conflict.conflict_type.value)
                
                # Create narrative event
                consequence_text = "; ".join(resolution['consequences'])
                event_description = f"{conflict.conflict_type.value.replace('_', ' ').title()}: {consequence_text}"
                resolved_events.append(event_description)
                
                # Record in uprising clock
                self.uprising_clock.record_faction_event(
                    conflict.primary_faction,
                    conflict.conflict_type.value,
                    event_description,
                    conflict.momentum_impact
                )
                
                # Move to history
                self.conflict_history.append(conflict)
            
            # Remove from active conflicts
            self.active_conflicts.remove(conflict)
        
        return resolved_events
    
    def _get_faction_relationship(self, faction_a_name: str, faction_b_name: str) -> Optional[FactionRelationship]:
        """Get relationship between two factions (order independent)"""
        key1 = f"{faction_a_name}_{faction_b_name}"
        key2 = f"{faction_b_name}_{faction_a_name}"
        
        return self.faction_relationships.get(key1) or self.faction_relationships.get(key2)
    
    def get_faction_relationship_summary(self) -> Dict[str, Any]:
        """Get summary of all faction relationships"""
        summary = {
            'total_relationships': len(self.faction_relationships),
            'hostile_relationships': 0,
            'neutral_relationships': 0,
            'friendly_relationships': 0,
            'active_rivalries': 0,
            'relationship_details': []
        }
        
        for relationship in self.faction_relationships.values():
            trust = relationship.trust_rating
            
            if trust < -20.0:
                summary['hostile_relationships'] += 1
                status = "HOSTILE"
            elif trust > 20.0:
                summary['friendly_relationships'] += 1
                status = "FRIENDLY"
            else:
                summary['neutral_relationships'] += 1
                status = "NEUTRAL"
            
            if relationship.rivalry_intensity > 30.0:
                summary['active_rivalries'] += 1
            
            summary['relationship_details'].append({
                'factions': f"{relationship.faction_a} ↔ {relationship.faction_b}",
                'trust': trust,
                'status': status,
                'rivalry_intensity': relationship.rivalry_intensity,
                'major_conflicts': len(relationship.major_conflicts)
            })
        
        return summary
    
    def _calculate_momentum_impact(self, faction: RevolutionaryFaction, outcome: str) -> float:
        """Calculate how faction activity affects national uprising momentum"""
        base_impact = 0.0
        
        if "successful" in outcome.lower() or "victory" in outcome.lower():
            base_impact = 2.0
        elif "failed" in outcome.lower() or "defeat" in outcome.lower():
            base_impact = -1.0
        elif "martyr" in outcome.lower():
            base_impact = 3.0  # Martyrs create significant momentum
        
        # Factor in faction support and media reach
        impact_multiplier = (faction.public_support / 100.0) * faction.media_reach
        
        return base_impact * impact_multiplier
    
    def _check_ecosystem_events(self) -> List[str]:
        """Check for ecosystem-wide events triggered by faction activities"""
        events = []
        
        # Check for coordinated uprising potential
        total_momentum = sum(f.public_support for f in self.active_factions)
        if total_momentum > 200.0 and self.uprising_clock.national_uprising_momentum > 50.0:
            if random.random() < 0.1:  # 10% chance
                events.append("NATIONWIDE COORDINATION: Revolutionary factions showing signs of coordination")
                self.uprising_clock.national_uprising_momentum += 10.0
        
        # Check for government crackdown
        total_heat = sum(f.government_heat for f in self.active_factions)
        if total_heat > 25.0:
            if random.random() < 0.15:  # 15% chance
                events.append("GOVERNMENT CRACKDOWN: Increased security operations against all factions")
                for faction in self.active_factions:
                    faction.government_heat += 1.0
                    faction.operational_capacity = max(0.3, faction.operational_capacity - 0.1)
        
        return events

    def evaluate_alliance_opportunities(self) -> List[Tuple[str, str, float]]:
        """Find potential alliance opportunities between factions - ITERATION 023"""
        opportunities = []
        faction_names = [f.name for f in self.active_factions]
        
        for i, faction_a_name in enumerate(faction_names):
            for j, faction_b_name in enumerate(faction_names):
                if i < j:  # Avoid duplicate pairs
                    faction_a = next(f for f in self.active_factions if f.name == faction_a_name)
                    faction_b = next(f for f in self.active_factions if f.name == faction_b_name)
                    
                    # Skip if already in alliance together
                    shared_alliances = set(faction_a.alliance_memberships) & set(faction_b.alliance_memberships)
                    if shared_alliances:
                        continue
                    
                    # Get relationship
                    relationship_key = f"{faction_a_name}_{faction_b_name}"
                    alt_key = f"{faction_b_name}_{faction_a_name}"
                    relationship = self.faction_relationships.get(relationship_key) or self.faction_relationships.get(alt_key)
                    
                    # Check basic alliance possibility
                    can_ally_a, reason_a = faction_a.can_form_alliance_with(faction_b, relationship)
                    can_ally_b, reason_b = faction_b.can_form_alliance_with(faction_a, relationship)
                    
                    if can_ally_a and can_ally_b:
                        # Calculate combined alliance motivation
                        value_a = faction_a.calculate_alliance_value(faction_b)
                        value_b = faction_b.calculate_alliance_value(faction_a)
                        combined_value = (value_a + value_b) / 2
                        
                        if relationship:
                            trust_bonus = max(0, relationship.trust_rating - 50) * 0.5
                            cooperation_bonus = max(0, len(relationship.cooperation_history) - 2) * 5
                            combined_value += trust_bonus + cooperation_bonus
                        
                        if combined_value > self.alliance_formation_threshold:
                            opportunities.append((faction_a_name, faction_b_name, combined_value))
        
        return sorted(opportunities, key=lambda x: x[2], reverse=True)

    def form_alliance(self, faction_names: List[str], alliance_name: str = None) -> Optional[FactionAlliance]:
        """Form a new alliance between specified factions - ITERATION 023"""
        if len(faction_names) < 2:
            return None
        
        # Generate alliance name if not provided
        if not alliance_name:
            alliance_name = f"{'_'.join(sorted(faction_names))}_alliance"
        
        # Check if all factions can join
        participating_factions = []
        for name in faction_names:
            faction = next((f for f in self.active_factions if f.name == name), None)
            if not faction:
                return None
            participating_factions.append(faction)
        
        # Create alliance
        alliance = FactionAlliance(
            alliance_name=alliance_name,
            member_factions=faction_names.copy(),
            trust_level=50.0,
            cooperation_momentum=10.0  # Initial optimism
        )
        
        # Add factions to alliance
        for faction in participating_factions:
            faction.alliance_memberships.append(alliance_name)
        
        self.active_alliances[alliance_name] = alliance
        
        # Log alliance formation
        alliance_event = {
            'type': 'alliance_formation',
            'alliance_name': alliance_name,
            'members': faction_names,
            'timestamp': datetime.now(),
            'initial_trust': alliance.trust_level
        }
        self.alliance_events.append(alliance_event)
        
        # Trigger propaganda event for alliance formation - ITERATION 024
        propaganda_initiator = random.choice(faction_names)  # Random faction leads propaganda
        other_members = [name for name in faction_names if name != propaganda_initiator]
        self.trigger_propaganda_event("alliance_formation", propaganda_initiator, other_members)
        
        print(f"🤝 ALLIANCE FORMED: {alliance_name} between {', '.join(faction_names)}")
        
        return alliance

    def execute_alliance_betrayal(self, alliance_name: str, betraying_faction: str) -> bool:
        """Execute betrayal of an alliance by one member - ITERATION 023"""
        alliance = self.active_alliances.get(alliance_name)
        if not alliance or betraying_faction not in alliance.member_factions:
            return False
        
        betrayer = next((f for f in self.active_factions if f.name == betraying_faction), None)
        if not betrayer:
            return False
            
        remaining_members = [name for name in alliance.member_factions if name != betraying_faction]
        
        # Remove betrayer from alliance
        alliance.member_factions.remove(betraying_faction)
        betrayer.alliance_memberships.remove(alliance_name)
        
        # Set cooldowns and relationship damage
        for member_name in remaining_members:
            betrayer.alliance_cooldown[member_name] = datetime.now()
            
            # Damage relationships with betrayed factions
            relationship_key = f"{betraying_faction}_{member_name}"
            alt_key = f"{member_name}_{betraying_faction}"
            relationship = self.faction_relationships.get(relationship_key) or self.faction_relationships.get(alt_key)
            
            if relationship:
                relationship.trust_rating = max(-50.0, relationship.trust_rating - 30.0)
                relationship.rivalry_intensity = min(100.0, relationship.rivalry_intensity + 25.0)
        
        # Trigger propaganda campaigns around betrayal - ITERATION 024
        # Betrayed factions launch "betrayal of cause" propaganda
        if remaining_members:
            victim_spokesman = random.choice(remaining_members)
            self.trigger_propaganda_event("betrayal", victim_spokesman, [betraying_faction], 
                                         PropagandaTone.BETRAYAL_OF_CAUSE)
        
        # Betrayer may launch defensive propaganda
        if random.random() < 0.6:  # 60% chance of defensive response
            self.trigger_propaganda_event("betrayal_defense", betraying_faction, remaining_members,
                                         PropagandaTone.ALLIANCE_NECESSITY)
        
        # Log betrayal event
        betrayal_event = {
            'type': 'alliance_betrayal',
            'alliance_name': alliance_name,
            'betrayer': betraying_faction,
            'victims': remaining_members,
            'timestamp': datetime.now(),
            'impact': 'severe_trust_damage'
        }
        self.alliance_events.append(betrayal_event)
        
        # Create conflict event
        conflict = FactionConflictEvent(
            conflict_type=FactionConflictType.ALLIANCE_BETRAYAL,
            primary_faction=betraying_faction,
            target_faction=remaining_members[0] if remaining_members else "",
            trigger_date=datetime.now(),
            description=f"{betraying_faction} betrays {alliance_name}, breaking alliance",
            intensity=0.8,
            momentum_impact=-15.0
        )
        self.active_conflicts.append(conflict)
        
        # Disband alliance if too few members remain
        if len(alliance.member_factions) < 2:
            del self.active_alliances[alliance_name]
            for member_name in alliance.member_factions:
                member = next((f for f in self.active_factions if f.name == member_name), None)
                if member and alliance_name in member.alliance_memberships:
                    member.alliance_memberships.remove(alliance_name)
        
        print(f"💀 BETRAYAL: {betraying_faction} betrays {alliance_name}!")
        
        return True

    def execute_joint_operations(self) -> List[Dict[str, Any]]:
        """Execute joint operations for all active alliances - ITERATION 023"""
        joint_operation_results = []
        
        for alliance_name, alliance in list(self.active_alliances.items()):  # Use list() to avoid iteration issues
            # Skip if alliance too weak or recent failure
            if alliance.trust_level < 25.0 or alliance.cooperation_momentum < -20.0:
                continue
            
            # Choose operation type based on alliance characteristics
            member_factions = [next(f for f in self.active_factions if f.name == name) for name in alliance.member_factions]
            
            # High operational capacity favors combined operations
            avg_capacity = sum(f.operational_capacity for f in member_factions) / len(member_factions)
            if avg_capacity > 1.2 and random.random() < 0.4:
                activity_type = JointActivityType.COMBINED_OPERATION
            elif sum(f.public_support for f in member_factions) > 100.0:
                activity_type = JointActivityType.JOINT_DEMONSTRATION
            else:
                activity_type = JointActivityType.COOP_PROPAGANDA
            
            # Execute the joint activity
            results = alliance.execute_joint_activity(activity_type, member_factions, self.faction_relationships)
            results['alliance_name'] = alliance_name
            
            # Update faction experience
            for faction in member_factions:
                faction.joint_operation_experience += 1
            
            # Trigger propaganda events based on operation results - ITERATION 024
            if results['success']:
                # Successful joint operations trigger celebratory propaganda
                propaganda_leader = random.choice(alliance.member_factions)
                other_members = [name for name in alliance.member_factions if name != propaganda_leader]
                propaganda_event = self.trigger_propaganda_event(
                    "joint_success", propaganda_leader, other_members, PropagandaTone.HEROIC_COOPERATION
                )
                results['propaganda_event'] = {
                    'type': 'success_celebration',
                    'leader': propaganda_leader,
                    'tone': propaganda_event.propaganda_tone.value,
                    'media_coverage': propaganda_event.media_saturation
                }
            elif alliance.cooperation_failures > alliance.shared_victories:
                # Multiple failures may trigger blame propaganda
                if random.random() < 0.4:  # 40% chance of internal blame
                    scapegoat = random.choice(alliance.member_factions)
                    accusers = [name for name in alliance.member_factions if name != scapegoat]
                    if accusers:
                        accuser = random.choice(accusers)
                        propaganda_event = self.trigger_propaganda_event(
                            "operation_failure", accuser, [scapegoat], PropagandaTone.TRAITOR_EXPOSURE
                        )
                        results['propaganda_event'] = {
                            'type': 'failure_blame',
                            'accuser': accuser,
                            'scapegoat': scapegoat,
                            'tone': propaganda_event.propaganda_tone.value
                        }
            
            joint_operation_results.append(results)
            
            # Check for betrayal after joint operations
            alliance.betrayal_risk = alliance.calculate_betrayal_risk(self.faction_relationships)
            if random.random() < alliance.betrayal_risk:
                # Random faction betrays
                betrayer_name = random.choice(alliance.member_factions)
                self.execute_alliance_betrayal(alliance_name, betrayer_name)
        
        return joint_operation_results

    def simulate_alliance_turn(self) -> Dict[str, Any]:
        """Simulate alliance activities for one turn - ITERATION 023"""
        alliance_results = {
            'alliance_opportunities': [],
            'new_alliances': [],
            'joint_operations': [],
            'betrayals': [],
            'propaganda_wars': [],  # ITERATION 024: Add propaganda tracking
            'alliance_summary': {}
        }
        
        # Check for new alliance formation opportunities
        opportunities = self.evaluate_alliance_opportunities()
        alliance_results['alliance_opportunities'] = opportunities
        
        # Attempt to form new alliances (30% chance for top opportunity)
        if opportunities and random.random() < 0.3:
            faction_a, faction_b, value = opportunities[0]
            new_alliance = self.form_alliance([faction_a, faction_b])
            if new_alliance:
                alliance_results['new_alliances'].append({
                    'alliance_name': new_alliance.alliance_name,
                    'members': new_alliance.member_factions,
                    'formation_value': value
                })
        
        # Execute joint operations for existing alliances
        joint_ops = self.execute_joint_operations()
        alliance_results['joint_operations'] = joint_ops
        
        # Execute propaganda narrative wars - ITERATION 024
        narrative_wars = self.execute_narrative_wars()
        alliance_results['propaganda_wars'] = narrative_wars
        
        # Create alliance summary
        alliance_results['alliance_summary'] = {
            'active_alliances': len(self.active_alliances),
            'total_alliance_events': len(self.alliance_events),
            'propaganda_events': len(self.propaganda_events),  # ITERATION 024
            'media_saturation': self.media_saturation_level,    # ITERATION 024
            'alliance_details': []
        }
        
        for alliance_name, alliance in self.active_alliances.items():
            alliance_results['alliance_summary']['alliance_details'].append({
                'name': alliance_name,
                'members': alliance.member_factions,
                'trust_level': alliance.trust_level,
                'cooperation_momentum': alliance.cooperation_momentum,
                'shared_victories': alliance.shared_victories,
                'cooperation_failures': alliance.cooperation_failures,
                'betrayal_risk': alliance.betrayal_risk
            })
        
        return alliance_results