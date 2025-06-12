"""
Years of Lead - City Reputation & Location-Based Influence System

# ITERATION_032

This module extends the symbolic geography system with city-wide reputation tracking,
location-based influence mechanics, and dynamic neighborhood control systems.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from .geography import SymbolicLocation


class InfluenceType(Enum):
    """Types of influence factions can exert in locations"""

    POLITICAL = "political"
    ECONOMIC = "economic"
    CULTURAL = "cultural"
    CRIMINAL = "criminal"
    SURVEILLANCE = "surveillance"


class ReputationEvent(Enum):
    """Events that affect faction reputation in locations"""

    SUCCESSFUL_OPERATION = "successful_operation"
    FAILED_OPERATION = "failed_operation"
    CIVILIAN_CASUALTIES = "civilian_casualties"
    COMMUNITY_SUPPORT = "community_support"
    BETRAYAL_EXPOSED = "betrayal_exposed"
    ALLIANCE_FORMED = "alliance_formed"
    PROPAGANDA_CAMPAIGN = "propaganda_campaign"
    POLICE_CRACKDOWN = "police_crackdown"


@dataclass
class LocationInfluence:
    """Tracks faction influence in a specific location"""

    faction_id: str
    location_id: str
    influence_types: Dict[InfluenceType, float] = field(default_factory=dict)
    reputation_score: float = 0.5  # 0.0 = despised, 1.0 = beloved
    control_percentage: float = 0.0  # 0-100% control
    established_turn: int = 0

    # Activity tracking
    recent_operations: List[str] = field(default_factory=list)
    reputation_events: List[Dict[str, Any]] = field(default_factory=list)

    def get_total_influence(self) -> float:
        """Calculate total influence across all types"""
        return sum(self.influence_types.values())

    def get_dominant_influence_type(self) -> Optional[InfluenceType]:
        """Get the type of influence this faction has most of"""
        if not self.influence_types:
            return None
        return max(self.influence_types.items(), key=lambda x: x[1])[0]

    def update_reputation(self, event: ReputationEvent, magnitude: float = 0.1):
        """Update reputation based on events"""
        event_modifiers = {
            ReputationEvent.SUCCESSFUL_OPERATION: 0.05,
            ReputationEvent.FAILED_OPERATION: -0.03,
            ReputationEvent.CIVILIAN_CASUALTIES: -0.15,
            ReputationEvent.COMMUNITY_SUPPORT: 0.12,
            ReputationEvent.BETRAYAL_EXPOSED: -0.20,
            ReputationEvent.ALLIANCE_FORMED: 0.08,
            ReputationEvent.PROPAGANDA_CAMPAIGN: 0.06,
            ReputationEvent.POLICE_CRACKDOWN: -0.10,
        }

        modifier = event_modifiers.get(event, 0.0) * magnitude
        old_reputation = self.reputation_score
        self.reputation_score = max(0.0, min(1.0, self.reputation_score + modifier))

        # Record the event
        self.reputation_events.append(
            {
                "event": event.value,
                "modifier": modifier,
                "old_reputation": old_reputation,
                "new_reputation": self.reputation_score,
                "turn": 0,  # Will be set by caller
            }
        )


@dataclass
class CityLocation(SymbolicLocation):
    """Extended location with city reputation mechanics"""

    population: int = 1000
    affluence_level: float = 0.5  # 0.0 = poor, 1.0 = wealthy
    security_level: float = 0.5  # 0.0 = no security, 1.0 = high security
    media_attention: float = 0.3  # 0.0 = ignored, 1.0 = heavily watched

    # Influence tracking
    faction_influences: Dict[str, LocationInfluence] = field(default_factory=dict)
    dominant_faction: Optional[str] = None
    contested: bool = False

    # Location-specific modifiers
    operation_difficulty_modifier: float = 0.0
    narrative_tone_modifier: Dict[str, float] = field(default_factory=dict)

    def add_faction_influence(
        self,
        faction_id: str,
        influence_type: InfluenceType,
        initial_strength: float = 0.1,
        turn: int = 0,
    ) -> LocationInfluence:
        """Add or update faction influence in this location"""
        if faction_id not in self.faction_influences:
            self.faction_influences[faction_id] = LocationInfluence(
                faction_id=faction_id, location_id=self.id, established_turn=turn
            )

        influence = self.faction_influences[faction_id]
        current_strength = influence.influence_types.get(influence_type, 0.0)
        influence.influence_types[influence_type] = min(
            1.0, current_strength + initial_strength
        )

        self._update_control_dynamics()
        return influence

    def get_faction_reputation(self, faction_id: str) -> float:
        """Get faction's reputation in this location"""
        if faction_id in self.faction_influences:
            return self.faction_influences[faction_id].reputation_score
        return 0.5  # Neutral for unknown factions

    def get_operation_modifier(self, faction_id: str, operation_type: str) -> float:
        """Calculate operation difficulty modifier based on faction reputation and location"""
        base_modifier = self.operation_difficulty_modifier

        # Reputation modifier
        reputation = self.get_faction_reputation(faction_id)
        reputation_modifier = (reputation - 0.5) * 0.3  # -0.15 to +0.15

        # Security modifier
        security_modifier = self.security_level * 0.2

        # Archetype modifier
        archetype_modifier = 0.0
        if operation_type == "stealth" and self.archetype in ["sanctuary", "ghetto"]:
            archetype_modifier = -0.1  # Easier stealth in these areas
        elif operation_type == "public" and self.archetype in ["market", "university"]:
            archetype_modifier = -0.05  # Easier public operations
        elif self.archetype == "government":
            archetype_modifier = 0.15  # All operations harder in government areas

        return (
            base_modifier + reputation_modifier + security_modifier + archetype_modifier
        )

    def _update_control_dynamics(self):
        """Update which faction dominates this location"""
        if not self.faction_influences:
            self.dominant_faction = None
            self.contested = False
            return

        # Calculate total influence for each faction
        faction_totals = {
            faction_id: influence.get_total_influence()
            for faction_id, influence in self.faction_influences.items()
        }

        # Find dominant faction
        if faction_totals:
            dominant_faction = max(faction_totals.items(), key=lambda x: x[1])[0]
            dominant_strength = faction_totals[dominant_faction]

            # Check if actually dominant (>40% stronger than next best)
            other_factions = {
                k: v for k, v in faction_totals.items() if k != dominant_faction
            }
            if other_factions:
                second_best = max(other_factions.values())
                if dominant_strength > second_best * 1.4:
                    self.dominant_faction = dominant_faction
                    self.contested = False
                else:
                    self.dominant_faction = None
                    self.contested = True
            else:
                self.dominant_faction = dominant_faction
                self.contested = False

            # Update control percentage for dominant faction
            if self.dominant_faction:
                total_influence = sum(faction_totals.values())
                if total_influence > 0:
                    control_pct = (dominant_strength / total_influence) * 100
                    self.faction_influences[
                        self.dominant_faction
                    ].control_percentage = control_pct


class CityReputationSystem:
    """Manages city-wide reputation and location-based influence"""

    def __init__(self):
        self.locations: Dict[str, CityLocation] = {}
        self.reputation_events: List[Dict[str, Any]] = []
        self.current_turn: int = 0

        # Global city metrics
        self.overall_stability: float = 0.7
        self.media_heat: int = 0
        self.civilian_morale: float = 0.6

    def create_location(
        self,
        name: str,
        archetype: str = "neutral",
        population: int = 1000,
        affluence: float = 0.5,
        security: float = 0.5,
    ) -> str:
        """Create a new city location"""
        location_id = f"location_{name.lower().replace(' ', '_')}_{len(self.locations)}"

        location = CityLocation(
            id=location_id,
            name=name,
            archetype=archetype,
            population=population,
            affluence_level=affluence,
            security_level=security,
        )

        self.locations[location_id] = location
        return location_id

    def establish_influence(
        self,
        faction_id: str,
        location_id: str,
        influence_type: InfluenceType,
        strength: float = 0.1,
    ) -> bool:
        """Establish faction influence in a location"""
        if location_id not in self.locations:
            return False

        location = self.locations[location_id]
        location.add_faction_influence(
            faction_id, influence_type, strength, self.current_turn
        )

        # Record establishment event
        self.reputation_events.append(
            {
                "type": "influence_established",
                "faction": faction_id,
                "location": location_id,
                "influence_type": influence_type.value,
                "strength": strength,
                "turn": self.current_turn,
            }
        )

        return True

    def process_operation_impact(
        self,
        faction_id: str,
        location_id: str,
        operation_type: str,
        success: bool,
        civilian_impact: bool = False,
    ) -> Dict[str, Any]:
        """Process the reputation impact of an operation"""
        if location_id not in self.locations:
            return {"error": "Location not found"}

        location = self.locations[location_id]
        results = {
            "reputation_changes": {},
            "influence_changes": {},
            "narrative_impact": "",
        }

        # Determine reputation event
        if civilian_impact:
            event = ReputationEvent.CIVILIAN_CASUALTIES
        elif success:
            event = ReputationEvent.SUCCESSFUL_OPERATION
        else:
            event = ReputationEvent.FAILED_OPERATION

        # Update faction reputation
        if faction_id in location.faction_influences:
            influence = location.faction_influences[faction_id]
            old_reputation = influence.reputation_score
            influence.update_reputation(event)
            influence.reputation_events[-1]["turn"] = self.current_turn

            results["reputation_changes"][faction_id] = {
                "old": old_reputation,
                "new": influence.reputation_score,
                "change": influence.reputation_score - old_reputation,
            }

        # Update city-wide metrics
        if civilian_impact:
            self.civilian_morale = max(0.0, self.civilian_morale - 0.05)
            self.media_heat += 10
            results[
                "narrative_impact"
            ] = f"Civilian casualties in {location.name} sparked outrage"
        elif success:
            if location.archetype in ["sanctuary", "university"]:
                self.civilian_morale = min(1.0, self.civilian_morale + 0.02)
            results[
                "narrative_impact"
            ] = f"Successful operation in {location.name} builds {faction_id} reputation"

        # Record global event
        self.reputation_events.append(
            {
                "type": "operation_impact",
                "faction": faction_id,
                "location": location_id,
                "operation_type": operation_type,
                "success": success,
                "civilian_impact": civilian_impact,
                "reputation_change": results["reputation_changes"].get(faction_id, {}),
                "turn": self.current_turn,
            }
        )

        return results

    def get_faction_city_reputation(self, faction_id: str) -> Dict[str, float]:
        """Get faction's reputation across all city locations"""
        reputation_map = {}
        for location_id, location in self.locations.items():
            reputation_map[location_id] = location.get_faction_reputation(faction_id)
        return reputation_map

    def get_location_control_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of faction control across all locations"""
        summary = {}
        for location_id, location in self.locations.items():
            summary[location_id] = {
                "name": location.name,
                "archetype": location.archetype,
                "dominant_faction": location.dominant_faction,
                "contested": location.contested,
                "faction_influences": {
                    faction_id: {
                        "total_influence": influence.get_total_influence(),
                        "reputation": influence.reputation_score,
                        "control_percentage": influence.control_percentage,
                    }
                    for faction_id, influence in location.faction_influences.items()
                },
            }
        return summary

    def process_turn(self, turn_number: int) -> Dict[str, Any]:
        """Process turn-based reputation and influence changes"""
        self.current_turn = turn_number
        results = {"reputation_shifts": [], "control_changes": [], "city_events": []}

        # Gradual reputation decay/recovery
        for location_id, location in self.locations.items():
            for faction_id, influence in location.faction_influences.items():
                # Reputation naturally drifts toward neutral (0.5) over time
                decay_rate = 0.01
                if influence.reputation_score > 0.5:
                    influence.reputation_score = max(
                        0.5, influence.reputation_score - decay_rate
                    )
                elif influence.reputation_score < 0.5:
                    influence.reputation_score = min(
                        0.5, influence.reputation_score + decay_rate
                    )

        # Media heat decay
        self.media_heat = max(0, self.media_heat - 2)

        # Check for significant control shifts
        for location_id, location in self.locations.items():
            old_dominant = location.dominant_faction
            location._update_control_dynamics()
            if location.dominant_faction != old_dominant:
                results["control_changes"].append(
                    {
                        "location": location_id,
                        "old_dominant": old_dominant,
                        "new_dominant": location.dominant_faction,
                        "contested": location.contested,
                    }
                )

        return results


# Global system instance for easy access
city_reputation_system = CityReputationSystem()
