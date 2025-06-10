"""
Campaign Structure Foundations - ITERATION 020

Macro-arc scaffolding for Years of Lead campaign progression including:
- Faction reputation across cities
- Trigger conditions for turning points  
- Phase transition flags and era management
- Historical momentum and consequence propagation
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import random


class CampaignPhase(Enum):
    """Major campaign phases with distinct characteristics"""
    UNDERGROUND_FORMATION = "underground_formation"    # Building initial network
    ACTIVE_RESISTANCE = "active_resistance"           # Open operations phase
    ERA_OF_CRACKDOWN = "era_of_crackdown"            # Government response intensifies
    DAWN_OF_DEFECTION = "dawn_of_defection"          # Officials start switching sides
    FINAL_CONFRONTATION = "final_confrontation"       # Climactic phase
    LIBERATION_VICTORY = "liberation_victory"          # Victory achieved
    BRUTAL_SUPPRESSION = "brutal_suppression"         # Government victory


class TurningPointType(Enum):
    """Types of major turning points that shift campaign trajectory"""
    MASS_CASUALTY_EVENT = "mass_casualty_event"       # Major loss of life
    HISTORIC_VICTORY = "historic_victory"             # Legendary successful operation
    BETRAYAL_EXPOSURE = "betrayal_exposure"           # High-level betrayal revealed
    GOVERNMENT_ATROCITY = "government_atrocity"       # Regime brutality exposed
    POPULAR_UPRISING = "popular_uprising"             # Civilian spontaneous revolt
    INTERNATIONAL_ATTENTION = "international_attention" # Global media coverage
    INFRASTRUCTURE_COLLAPSE = "infrastructure_collapse" # Critical systems failing
    LEADER_MARTYRDOM = "leader_martyrdom"             # Iconic figure killed/captured


@dataclass
class CityReputation:
    """Faction reputation and influence in a specific city"""
    city_name: str
    reputation_score: float = 0.0         # -100 to +100, faction standing with population
    government_heat: float = 5.0          # 0-10, government attention in this city
    operational_security: float = 0.5     # 0-1, how well hidden faction operations are
    popular_support: float = 0.3          # 0-1, civilian population support
    infrastructure_control: float = 0.0   # 0-1, control over city systems
    
    # Historical events in this city
    major_victories: List[str] = field(default_factory=list)
    major_defeats: List[str] = field(default_factory=list)
    martyrs: List[str] = field(default_factory=list)
    
    # Active status
    safe_houses: int = 1
    compromised_locations: Set[str] = field(default_factory=set)
    active_cells: int = 1
    
    def apply_operation_outcome(self, operation_type: str, outcome: str, 
                              visibility: str, casualties: int = 0) -> Dict[str, float]:
        """Apply operation outcome to city reputation"""
        reputation_change = 0.0
        heat_change = 0.0
        support_change = 0.0
        
        # Base effects by outcome
        if outcome == 'critical_success':
            reputation_change = 15.0
            support_change = 0.1
            heat_change = 2.0
            self.major_victories.append(f"{operation_type}_{datetime.now().strftime('%Y%m%d')}")
        elif outcome == 'success':
            reputation_change = 8.0
            support_change = 0.05
            heat_change = 1.0
        elif outcome == 'failure':
            reputation_change = -5.0
            support_change = -0.02
            heat_change = 0.5
            self.major_defeats.append(f"{operation_type}_{datetime.now().strftime('%Y%m%d')}")
        elif outcome == 'disaster':
            reputation_change = -20.0
            support_change = -0.1
            heat_change = 3.0
            self.major_defeats.append(f"{operation_type}_{datetime.now().strftime('%Y%m%d')}")
        
        # Visibility modifiers
        visibility_multipliers = {
            'covert': 0.5,      # Hidden operations have less impact
            'public': 1.5,      # Public operations amplified
            'spectacular': 2.0   # Major spectacles get maximum impact
        }
        
        visibility_mult = visibility_multipliers.get(visibility, 1.0)
        reputation_change *= visibility_mult
        support_change *= visibility_mult
        
        # Casualty effects
        if casualties > 0:
            reputation_change -= casualties * 3.0  # Heavy penalty for casualties
            support_change -= casualties * 0.02
            heat_change += casualties * 0.5
            
            # Add martyrs for faction casualties
            if outcome in ['failure', 'disaster']:
                for _ in range(casualties):
                    self.martyrs.append(f"martyr_{len(self.martyrs)+1}_{datetime.now().strftime('%Y%m%d')}")
        
        # Apply changes with bounds
        self.reputation_score = max(-100.0, min(100.0, self.reputation_score + reputation_change))
        self.government_heat = max(0.0, min(10.0, self.government_heat + heat_change))
        self.popular_support = max(0.0, min(1.0, self.popular_support + support_change))
        
        # Heat affects operational security
        if self.government_heat > 7.0:
            self.operational_security = max(0.1, self.operational_security - 0.05)
        
        return {
            'reputation_change': reputation_change,
            'heat_change': heat_change,
            'support_change': support_change
        }
    
    def get_symbolic_status(self) -> str:
        """Get symbolic status of this city for the resistance"""
        if len(self.martyrs) >= 3:
            return "City of Martyrs"
        elif len(self.major_victories) >= 5:
            return "Liberation Stronghold"
        elif self.government_heat >= 9.0:
            return "Under Siege"
        elif self.popular_support >= 0.8:
            return "People's City"
        elif self.reputation_score >= 75.0:
            return "Resistance Capital"
        elif self.reputation_score <= -75.0:
            return "Enemy Territory"
        else:
            return "Contested Ground"


@dataclass
class TurningPoint:
    """Major campaign turning point with long-term consequences"""
    turning_point_type: TurningPointType
    trigger_date: datetime
    description: str
    consequences: Dict[str, Any] = field(default_factory=dict)
    cities_affected: List[str] = field(default_factory=list)
    phase_transition: Optional[CampaignPhase] = None
    historical_weight: float = 1.0  # How significant this event is (0.5-3.0)
    
    def apply_global_consequences(self, campaign_state: 'CampaignState') -> None:
        """Apply this turning point's consequences to the entire campaign"""
        
        if self.turning_point_type == TurningPointType.MASS_CASUALTY_EVENT:
            # Mass casualties create martyrs and increase sympathy
            for city_name in self.cities_affected:
                if city_name in campaign_state.city_reputations:
                    city = campaign_state.city_reputations[city_name]
                    city.popular_support += 0.2  # Martyrdom creates support
                    city.reputation_score += 20.0
            
            campaign_state.global_faction_reputation += 15.0
            
        elif self.turning_point_type == TurningPointType.HISTORIC_VICTORY:
            # Historic victories inspire nationwide
            for city in campaign_state.city_reputations.values():
                city.popular_support += 0.15
                city.reputation_score += 10.0
            
            campaign_state.global_faction_reputation += 25.0
            
        elif self.turning_point_type == TurningPointType.BETRAYAL_EXPOSURE:
            # Betrayals damage trust but can expose government corruption
            for city in campaign_state.city_reputations.values():
                city.popular_support -= 0.1  # Initial trust damage
                city.government_heat += 1.0  # Increased scrutiny
            
            campaign_state.global_faction_reputation -= 10.0
            
        elif self.turning_point_type == TurningPointType.GOVERNMENT_ATROCITY:
            # Government atrocities galvanize opposition
            for city in campaign_state.city_reputations.values():
                city.popular_support += 0.25
                city.reputation_score += 15.0
            
            campaign_state.global_faction_reputation += 30.0
            
        elif self.turning_point_type == TurningPointType.POPULAR_UPRISING:
            # Popular uprisings show momentum
            affected_cities = random.sample(list(campaign_state.city_reputations.keys()), 
                                           min(3, len(campaign_state.city_reputations)))
            
            for city_name in affected_cities:
                city = campaign_state.city_reputations[city_name]
                city.popular_support += 0.3
                city.infrastructure_control += 0.2
                city.government_heat += 2.0
            
            campaign_state.global_faction_reputation += 20.0


@dataclass  
class CampaignState:
    """Overall state of the resistance campaign"""
    current_phase: CampaignPhase = CampaignPhase.UNDERGROUND_FORMATION
    phase_start_date: datetime = field(default_factory=datetime.now)
    
    # Global reputation and momentum
    global_faction_reputation: float = 0.0    # -100 to +100
    international_attention: float = 0.0      # 0-100, global awareness
    government_legitimacy: float = 80.0       # 0-100, regime's perceived legitimacy
    
    # City-specific data
    city_reputations: Dict[str, CityReputation] = field(default_factory=dict)
    
    # Historical tracking
    turning_points: List[TurningPoint] = field(default_factory=list)
    phase_history: List[Tuple[CampaignPhase, datetime]] = field(default_factory=list)
    
    # Phase transition conditions
    phase_transition_thresholds: Dict[str, float] = field(default_factory=lambda: {
        'reputation_threshold': 60.0,      # Global reputation needed for advancement
        'support_threshold': 0.6,          # Average popular support needed
        'cities_controlled': 3,            # Cities with high influence needed
        'turning_points_required': 2       # Major events needed for phase change
    })
    
    def add_city(self, city_name: str) -> CityReputation:
        """Add new city to campaign tracking"""
        city = CityReputation(city_name=city_name)
        self.city_reputations[city_name] = city
        return city
    
    def trigger_turning_point(self, turning_point_type: TurningPointType, 
                            description: str, cities_affected: List[str] = None) -> TurningPoint:
        """Trigger a major campaign turning point"""
        cities_affected = cities_affected or []
        
        turning_point = TurningPoint(
            turning_point_type=turning_point_type,
            trigger_date=datetime.now(),
            description=description,
            cities_affected=cities_affected,
            historical_weight=random.uniform(1.0, 2.5)
        )
        
        # Apply consequences
        turning_point.apply_global_consequences(self)
        
        # Check for phase transition
        potential_phase = self.check_phase_transition(turning_point)
        if potential_phase:
            turning_point.phase_transition = potential_phase
            self.transition_to_phase(potential_phase)
        
        self.turning_points.append(turning_point)
        return turning_point
    
    def check_phase_transition(self, latest_turning_point: TurningPoint = None) -> Optional[CampaignPhase]:
        """Check if conditions are met for phase transition"""
        current_phase = self.current_phase
        
        # Calculate current campaign metrics
        avg_support = (sum(city.popular_support for city in self.city_reputations.values()) / 
                      len(self.city_reputations)) if self.city_reputations else 0.0
        
        controlled_cities = sum(1 for city in self.city_reputations.values() 
                               if city.infrastructure_control > 0.6)
        
        recent_turning_points = [tp for tp in self.turning_points 
                               if (datetime.now() - tp.trigger_date).days < 90]
        
        # Phase transition logic
        if current_phase == CampaignPhase.UNDERGROUND_FORMATION:
            if (self.global_faction_reputation > 30.0 and 
                avg_support > 0.4 and 
                len(recent_turning_points) >= 1):
                return CampaignPhase.ACTIVE_RESISTANCE
                
        elif current_phase == CampaignPhase.ACTIVE_RESISTANCE:
            # Could go to crackdown (if government responds) or defection (if winning)
            government_pressure = sum(city.government_heat for city in self.city_reputations.values())
            
            if government_pressure > 50.0:  # High heat triggers crackdown
                return CampaignPhase.ERA_OF_CRACKDOWN
            elif (self.global_faction_reputation > 60.0 and 
                  self.government_legitimacy < 50.0):
                return CampaignPhase.DAWN_OF_DEFECTION
                
        elif current_phase == CampaignPhase.ERA_OF_CRACKDOWN:
            # Can transition to defection if surviving crackdown well
            if (self.global_faction_reputation > 40.0 and 
                avg_support > 0.6 and
                controlled_cities >= 2):
                return CampaignPhase.DAWN_OF_DEFECTION
                
        elif current_phase == CampaignPhase.DAWN_OF_DEFECTION:
            if (controlled_cities >= 4 and 
                self.government_legitimacy < 30.0):
                return CampaignPhase.FINAL_CONFRONTATION
                
        elif current_phase == CampaignPhase.FINAL_CONFRONTATION:
            if controlled_cities >= 6:
                return CampaignPhase.LIBERATION_VICTORY
            elif self.global_faction_reputation < -50.0:
                return CampaignPhase.BRUTAL_SUPPRESSION
        
        return None
    
    def transition_to_phase(self, new_phase: CampaignPhase) -> None:
        """Transition campaign to new phase"""
        old_phase = self.current_phase
        self.phase_history.append((old_phase, self.phase_start_date))
        
        self.current_phase = new_phase
        self.phase_start_date = datetime.now()
        
        # Apply phase-specific modifiers
        self.apply_phase_effects(new_phase)
    
    def apply_phase_effects(self, phase: CampaignPhase) -> None:
        """Apply ongoing effects of current campaign phase"""
        
        if phase == CampaignPhase.ERA_OF_CRACKDOWN:
            # Crackdown increases heat and reduces operational security
            for city in self.city_reputations.values():
                city.government_heat = min(10.0, city.government_heat + 2.0)
                city.operational_security = max(0.1, city.operational_security - 0.2)
                
        elif phase == CampaignPhase.DAWN_OF_DEFECTION:
            # Defection phase - government legitimacy crumbles
            self.government_legitimacy = max(0.0, self.government_legitimacy - 10.0)
            
            # Some cities may spontaneously support resistance
            for city in self.city_reputations.values():
                if random.random() < 0.3:  # 30% chance
                    city.popular_support += 0.2
                    city.infrastructure_control += 0.1
                    
        elif phase == CampaignPhase.FINAL_CONFRONTATION:
            # High stakes - everything intensifies
            for city in self.city_reputations.values():
                city.government_heat = 10.0  # Maximum pressure
                
        elif phase == CampaignPhase.LIBERATION_VICTORY:
            # Victory achieved - resistance controls nation
            for city in self.city_reputations.values():
                city.infrastructure_control = 1.0
                city.government_heat = 0.0
                
        elif phase == CampaignPhase.BRUTAL_SUPPRESSION:
            # Defeat - resistance crushed
            for city in self.city_reputations.values():
                city.popular_support = max(0.0, city.popular_support - 0.5)
                city.operational_security = 0.1
    
    def get_campaign_summary(self) -> Dict[str, Any]:
        """Get comprehensive campaign status summary"""
        if not self.city_reputations:
            return {'status': 'no_cities_tracked'}
        
        avg_support = sum(city.popular_support for city in self.city_reputations.values()) / len(self.city_reputations)
        avg_heat = sum(city.government_heat for city in self.city_reputations.values()) / len(self.city_reputations)
        controlled_cities = sum(1 for city in self.city_reputations.values() if city.infrastructure_control > 0.6)
        
        # Identify most/least supportive cities
        most_supportive = max(self.city_reputations.values(), key=lambda c: c.popular_support)
        least_supportive = min(self.city_reputations.values(), key=lambda c: c.popular_support)
        
        return {
            'current_phase': self.current_phase.value,
            'phase_duration_days': (datetime.now() - self.phase_start_date).days,
            'global_reputation': self.global_faction_reputation,
            'government_legitimacy': self.government_legitimacy,
            'international_attention': self.international_attention,
            'average_popular_support': avg_support,
            'average_government_heat': avg_heat,
            'cities_tracked': len(self.city_reputations),
            'cities_controlled': controlled_cities,
            'turning_points_count': len(self.turning_points),
            'most_supportive_city': most_supportive.city_name,
            'least_supportive_city': least_supportive.city_name,
            'total_martyrs': sum(len(city.martyrs) for city in self.city_reputations.values()),
            'total_victories': sum(len(city.major_victories) for city in self.city_reputations.values())
        }
    
    def get_phase_transition_progress(self) -> Dict[str, float]:
        """Get progress toward next phase transition"""
        if not self.city_reputations:
            return {'no_data': True}
        
        avg_support = sum(city.popular_support for city in self.city_reputations.values()) / len(self.city_reputations)
        controlled_cities = sum(1 for city in self.city_reputations.values() if city.infrastructure_control > 0.6)
        recent_turning_points = len([tp for tp in self.turning_points if (datetime.now() - tp.trigger_date).days < 90])
        
        return {
            'reputation_progress': min(1.0, abs(self.global_faction_reputation) / self.phase_transition_thresholds['reputation_threshold']),
            'support_progress': avg_support / self.phase_transition_thresholds['support_threshold'],
            'cities_progress': controlled_cities / self.phase_transition_thresholds['cities_controlled'],
            'events_progress': recent_turning_points / self.phase_transition_thresholds['turning_points_required']
        }