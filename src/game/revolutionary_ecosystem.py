"""
Revolutionary Ecosystem - ITERATION 021

Multi-faction revolutionary environment where AI-controlled factions operate independently
alongside the player, creating a dynamic ecosystem of competing resistance movements.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
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
    
    def execute_turn_activity(self, ecosystem: 'RevolutionaryEcosystem') -> Dict[str, any]:
        """Execute this faction's activity for the current turn"""
        activity_results = {
            'faction_name': self.name,
            'activity_type': self.current_activity.value,
            'outcomes': [],
            'city_effects': {},
            'narrative_events': []
        }
        
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
        
        return activity_results
    
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
class RevolutionaryEcosystem:
    """Manages multiple revolutionary factions and their interactions"""
    active_factions: List[RevolutionaryFaction] = field(default_factory=list)
    uprising_clock: UprisingClock = field(default_factory=UprisingClock)
    city_reputations: Dict[str, any] = field(default_factory=dict)  # Reference to campaign city data
    
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
    
    def simulate_ecosystem_turn(self) -> Dict[str, any]:
        """Simulate one turn of the revolutionary ecosystem"""
        turn_results = {
            'date': self.uprising_clock.current_date,
            'faction_activities': [],
            'major_events': [],
            'ecosystem_changes': {}
        }
        
        # Advance the clock
        self.uprising_clock.advance_day()
        
        # Each faction executes their turn
        for faction in self.active_factions:
            faction_results = faction.execute_turn_activity(self)
            turn_results['faction_activities'].append(faction_results)
            
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
        
        # Check for ecosystem-wide events
        ecosystem_events = self._check_ecosystem_events()
        turn_results['major_events'] = ecosystem_events
        
        return turn_results
    
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