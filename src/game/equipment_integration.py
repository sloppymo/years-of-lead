"""
Equipment Integration System for Years of Lead

This module integrates the Phase 1 enhanced equipment system with:
1. Mission execution engine
2. Agent loadout management
3. Pre-mission planning
4. Equipment durability tracking
5. Equipment effects application
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from .equipment_enhanced import (
    EnhancedEquipmentProfile,
    EnhancedEquipmentManager,
)
from .equipment_system import EquipmentCategory, LegalStatus


class LoadoutSlot(Enum):
    """Equipment loadout slots"""

    PRIMARY_WEAPON = "primary_weapon"
    SECONDARY_WEAPON = "secondary_weapon"
    TOOL = "tool"
    ELECTRONIC = "electronic"
    CONTAINER = "container"
    DISGUISE = "disguise"
    MEDICAL = "medical"
    DOCUMENT = "document"
    EXPLOSIVE = "explosive"
    SPECIAL = "special"


@dataclass
class AgentLoadout:
    """Agent equipment loadout"""

    agent_id: str
    equipment: Dict[LoadoutSlot, EnhancedEquipmentProfile] = field(default_factory=dict)
    total_weight: float = 0.0
    total_bulk: float = 0.0
    concealment_rating: float = 0.0
    legal_risk: float = 0.0
    equipment_bonuses: Dict[str, float] = field(default_factory=dict)
    mission_modifiers: Dict[str, float] = field(default_factory=dict)
    emotional_effects: Dict[str, float] = field(default_factory=dict)
    social_effects: Dict[str, float] = field(default_factory=dict)

    def add_equipment(
        self, slot: LoadoutSlot, equipment: EnhancedEquipmentProfile
    ) -> bool:
        """Add equipment to loadout"""
        if slot in self.equipment:
            return False  # Slot already occupied

        self.equipment[slot] = equipment
        self._recalculate_loadout_stats()
        return True

    def remove_equipment(self, slot: LoadoutSlot) -> Optional[EnhancedEquipmentProfile]:
        """Remove equipment from loadout"""
        if slot not in self.equipment:
            return None

        equipment = self.equipment.pop(slot)
        self._recalculate_loadout_stats()
        return equipment

    def get_equipment(self, slot: LoadoutSlot) -> Optional[EnhancedEquipmentProfile]:
        """Get equipment in slot"""
        return self.equipment.get(slot)

    def _recalculate_loadout_stats(self):
        """Recalculate loadout statistics"""
        self.total_weight = 0.0
        self.total_bulk = 0.0
        self.concealment_rating = 0.0
        self.legal_risk = 0.0

        # Reset bonuses
        self.equipment_bonuses = {}
        self.mission_modifiers = {}
        self.emotional_effects = {}
        self.social_effects = {}

        # Calculate stats from all equipment
        for equipment in self.equipment.values():
            # Weight and bulk
            self.total_weight += equipment.weight
            self.total_bulk += equipment.bulk

            # Legal risk
            if equipment.legal_status == LegalStatus.PROHIBITED:
                self.legal_risk += 0.3
            elif equipment.legal_status == LegalStatus.RESTRICTED:
                self.legal_risk += 0.1

            # Concealment (average of all equipment)
            concealment = equipment.get_effective_concealment()
            self.concealment_rating = (self.concealment_rating + concealment) / 2

            # Equipment bonuses
            for skill, bonus in equipment.effects.skill_bonuses.items():
                self.equipment_bonuses[skill] = (
                    self.equipment_bonuses.get(skill, 0.0) + bonus
                )

            # Mission modifiers
            for mission_type, modifier in equipment.effects.mission_modifiers.items():
                self.mission_modifiers[mission_type] = (
                    self.mission_modifiers.get(mission_type, 0.0) + modifier
                )

            # Emotional effects
            for emotion, effect in equipment.effects.emotional_effects.items():
                self.emotional_effects[emotion] = (
                    self.emotional_effects.get(emotion, 0.0) + effect
                )

            # Social effects
            for context, effect in equipment.effects.social_effects.items():
                self.social_effects[context] = (
                    self.social_effects.get(context, 0.0) + effect
                )

    def get_skill_bonus(self, skill: str) -> float:
        """Get total skill bonus from loadout"""
        return self.equipment_bonuses.get(skill, 0.0)

    def get_mission_modifier(self, mission_type: str) -> float:
        """Get total mission modifier from loadout"""
        return self.mission_modifiers.get(mission_type, 0.0)

    def get_emotional_effect(self, emotion: str) -> float:
        """Get total emotional effect from loadout"""
        return self.emotional_effects.get(emotion, 0.0)

    def get_social_effect(self, context: str) -> float:
        """Get total social effect from loadout"""
        return self.social_effects.get(context, 0.0)

    def use_equipment_in_mission(
        self, mission_intensity: float = 1.0
    ) -> Dict[str, Any]:
        """Use all equipment in mission and return degradation results"""
        degradation_results = {}

        for slot, equipment in self.equipment.items():
            # Calculate intensity based on slot and mission type
            slot_intensity = self._calculate_slot_intensity(slot, mission_intensity)

            # Use equipment
            success = equipment.use_equipment(slot_intensity)

            degradation_results[slot.value] = {
                "equipment_id": equipment.item_id,
                "equipment_name": equipment.name,
                "success": success,
                "condition_before": equipment.durability.condition,
                "condition_after": equipment.durability.condition,
                "degradation": equipment.durability.condition
                - equipment.durability.condition,
                "maintenance_required": equipment.durability.maintenance_required,
                "broken": equipment.durability.condition <= 0.0,
            }

        return degradation_results

    def _calculate_slot_intensity(
        self, slot: LoadoutSlot, mission_intensity: float
    ) -> float:
        """Calculate equipment usage intensity for a slot"""
        base_intensity = mission_intensity

        # Adjust intensity based on slot type
        slot_multipliers = {
            LoadoutSlot.PRIMARY_WEAPON: 1.2,
            LoadoutSlot.SECONDARY_WEAPON: 0.8,
            LoadoutSlot.TOOL: 1.0,
            LoadoutSlot.ELECTRONIC: 1.1,
            LoadoutSlot.CONTAINER: 0.5,
            LoadoutSlot.DISGUISE: 0.7,
            LoadoutSlot.MEDICAL: 0.6,
            LoadoutSlot.DOCUMENT: 0.3,
            LoadoutSlot.EXPLOSIVE: 1.3,
            LoadoutSlot.SPECIAL: 1.0,
        }

        return base_intensity * slot_multipliers.get(slot, 1.0)


@dataclass
class MissionEquipmentAnalysis:
    """Analysis of equipment suitability for a mission"""

    mission_type: str
    recommended_equipment: Dict[LoadoutSlot, List[EnhancedEquipmentProfile]]
    equipment_scores: Dict[str, float]
    loadout_suggestions: List[Dict[str, Any]]
    risk_assessment: Dict[str, float]
    success_probability_boost: float
    concealment_rating: float
    legal_risk_level: float


class EquipmentIntegrationManager:
    """Manager for equipment integration with game systems"""

    def __init__(self, equipment_manager: EnhancedEquipmentManager):
        self.equipment_manager = equipment_manager
        self.agent_loadouts: Dict[str, AgentLoadout] = {}
        self.mission_equipment_history: List[Dict[str, Any]] = []

    def create_agent_loadout(self, agent_id: str) -> AgentLoadout:
        """Create a new loadout for an agent"""
        loadout = AgentLoadout(agent_id=agent_id)
        self.agent_loadouts[agent_id] = loadout
        return loadout

    def get_agent_loadout(self, agent_id: str) -> Optional[AgentLoadout]:
        """Get agent's current loadout"""
        return self.agent_loadouts.get(agent_id)

    def analyze_mission_equipment(
        self,
        mission: Dict[str, Any],
        available_equipment: List[EnhancedEquipmentProfile],
    ) -> MissionEquipmentAnalysis:
        """Analyze equipment suitability for a mission"""

        mission_type = mission.get("type", "propaganda")
        location = mission.get("location", {})
        difficulty = mission.get("difficulty", 0.5)

        # Categorize available equipment
        equipment_by_category = self._categorize_equipment(available_equipment)

        # Score equipment for mission
        equipment_scores = self._score_equipment_for_mission(
            available_equipment, mission_type, location, difficulty
        )

        # Generate recommendations
        recommended_equipment = self._generate_equipment_recommendations(
            equipment_by_category, equipment_scores, mission_type
        )

        # Create loadout suggestions
        loadout_suggestions = self._create_loadout_suggestions(
            recommended_equipment, mission_type, difficulty
        )

        # Assess risks
        risk_assessment = self._assess_equipment_risks(
            recommended_equipment, location, mission_type
        )

        # Calculate success probability boost
        success_boost = self._calculate_success_boost(
            recommended_equipment, mission_type
        )

        # Calculate concealment and legal risk
        concealment_rating = self._calculate_concealment_rating(recommended_equipment)
        legal_risk_level = self._calculate_legal_risk(recommended_equipment)

        return MissionEquipmentAnalysis(
            mission_type=mission_type,
            recommended_equipment=recommended_equipment,
            equipment_scores=equipment_scores,
            loadout_suggestions=loadout_suggestions,
            risk_assessment=risk_assessment,
            success_probability_boost=success_boost,
            concealment_rating=concealment_rating,
            legal_risk_level=legal_risk_level,
        )

    def _categorize_equipment(
        self, equipment_list: List[EnhancedEquipmentProfile]
    ) -> Dict[EquipmentCategory, List[EnhancedEquipmentProfile]]:
        """Categorize equipment by type"""
        categorized = {}
        for equipment in equipment_list:
            category = equipment.category
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(equipment)
        return categorized

    def _score_equipment_for_mission(
        self,
        equipment_list: List[EnhancedEquipmentProfile],
        mission_type: str,
        location: Dict[str, Any],
        difficulty: float,
    ) -> Dict[str, float]:
        """Score equipment suitability for mission"""
        scores = {}

        for equipment in equipment_list:
            score = 0.0

            # Base mission modifier
            mission_modifier = equipment.get_mission_bonus(mission_type)
            score += mission_modifier * 0.4

            # Quality/condition bonus
            quality_bonus = equipment.durability.get_effectiveness_modifier()
            score += quality_bonus * 0.2

            # Rarity bonus
            score += equipment.rarity * 0.1

            # Concealment bonus for stealth missions
            if mission_type in ["intelligence", "sabotage"]:
                concealment = equipment.get_effective_concealment()
                score += concealment * 0.2

            # Combat bonus for violent missions
            if mission_type in ["assassination", "rescue"]:
                combat_bonus = equipment.get_skill_bonus("combat")
                score += combat_bonus * 0.3

            # Technical bonus for complex missions
            if mission_type in ["intelligence", "sabotage"]:
                tech_bonus = equipment.get_skill_bonus(
                    "hacking"
                ) + equipment.get_skill_bonus("intelligence")
                score += tech_bonus * 0.2

            scores[equipment.item_id] = max(0.0, min(1.0, score))

        return scores

    def _generate_equipment_recommendations(
        self,
        equipment_by_category: Dict[EquipmentCategory, List[EnhancedEquipmentProfile]],
        equipment_scores: Dict[str, float],
        mission_type: str,
    ) -> Dict[LoadoutSlot, List[EnhancedEquipmentProfile]]:
        """Generate equipment recommendations by slot"""
        recommendations = {}

        # Map categories to loadout slots (using correct categories)
        category_to_slot = {
            EquipmentCategory.WEAPON: [
                LoadoutSlot.PRIMARY_WEAPON,
                LoadoutSlot.SECONDARY_WEAPON,
            ],
            EquipmentCategory.TOOL: [LoadoutSlot.TOOL],
            EquipmentCategory.ELECTRONIC: [LoadoutSlot.ELECTRONIC],
            EquipmentCategory.ARMOR: [
                LoadoutSlot.DISGUISE
            ],  # Map armor to disguise slot
            EquipmentCategory.MEDICAL: [LoadoutSlot.MEDICAL],
            EquipmentCategory.DOCUMENT: [LoadoutSlot.DOCUMENT],
            EquipmentCategory.EXPLOSIVE: [LoadoutSlot.EXPLOSIVE],
            EquipmentCategory.COMMUNICATION: [
                LoadoutSlot.ELECTRONIC
            ],  # Map communication to electronic
            EquipmentCategory.CURRENCY: [
                LoadoutSlot.SPECIAL
            ],  # Map currency to special
            EquipmentCategory.CONTRABAND: [
                LoadoutSlot.SPECIAL
            ],  # Map contraband to special
        }

        for category, equipment_list in equipment_by_category.items():
            if category in category_to_slot:
                slots = category_to_slot[category]

                # Sort equipment by score
                sorted_equipment = sorted(
                    equipment_list,
                    key=lambda e: equipment_scores.get(e.item_id, 0.0),
                    reverse=True,
                )

                # Assign to slots
                for i, slot in enumerate(slots):
                    if i < len(sorted_equipment):
                        if slot not in recommendations:
                            recommendations[slot] = []
                        recommendations[slot].extend(
                            sorted_equipment[:3]
                        )  # Top 3 options

        return recommendations

    def _create_loadout_suggestions(
        self,
        recommended_equipment: Dict[LoadoutSlot, List[EnhancedEquipmentProfile]],
        mission_type: str,
        difficulty: float,
    ) -> List[Dict[str, Any]]:
        """Create specific loadout suggestions"""
        suggestions = []

        # Create different loadout strategies
        strategies = [
            {
                "name": "Stealth",
                "focus": "concealment",
                "slots": [
                    LoadoutSlot.TOOL,
                    LoadoutSlot.ELECTRONIC,
                    LoadoutSlot.DISGUISE,
                ],
            },
            {
                "name": "Combat",
                "focus": "combat",
                "slots": [
                    LoadoutSlot.PRIMARY_WEAPON,
                    LoadoutSlot.SECONDARY_WEAPON,
                    LoadoutSlot.MEDICAL,
                ],
            },
            {
                "name": "Technical",
                "focus": "intelligence",
                "slots": [
                    LoadoutSlot.ELECTRONIC,
                    LoadoutSlot.TOOL,
                    LoadoutSlot.DOCUMENT,
                ],
            },
            {
                "name": "Balanced",
                "focus": "balanced",
                "slots": [
                    LoadoutSlot.PRIMARY_WEAPON,
                    LoadoutSlot.ELECTRONIC,
                    LoadoutSlot.TOOL,
                ],
            },
        ]

        for strategy in strategies:
            suggestion = {
                "strategy": strategy["name"],
                "focus": strategy["focus"],
                "equipment": {},
                "total_weight": 0.0,
                "concealment_rating": 0.0,
                "legal_risk": 0.0,
                "success_boost": 0.0,
            }

            for slot in strategy["slots"]:
                if slot in recommended_equipment and recommended_equipment[slot]:
                    best_equipment = recommended_equipment[slot][0]
                    suggestion["equipment"][slot.value] = {
                        "item_id": best_equipment.item_id,
                        "name": best_equipment.name,
                        "condition": best_equipment.durability.condition,
                        "weight": best_equipment.weight,
                    }
                    suggestion["total_weight"] += best_equipment.weight

            suggestions.append(suggestion)

        return suggestions

    def _assess_equipment_risks(
        self,
        recommended_equipment: Dict[LoadoutSlot, List[EnhancedEquipmentProfile]],
        location: Dict[str, Any],
        mission_type: str,
    ) -> Dict[str, float]:
        """Assess risks associated with equipment choices"""
        risks = {
            "detection_risk": 0.0,
            "legal_risk": 0.0,
            "equipment_failure_risk": 0.0,
            "maintenance_risk": 0.0,
        }

        for slot, equipment_list in recommended_equipment.items():
            if equipment_list:
                equipment = equipment_list[0]

                # Detection risk based on concealment
                concealment = equipment.get_effective_concealment()
                risks["detection_risk"] += (1.0 - concealment) * 0.1

                # Legal risk
                if equipment.legal_status == LegalStatus.PROHIBITED:
                    risks["legal_risk"] += 0.3
                elif equipment.legal_status == LegalStatus.RESTRICTED:
                    risks["legal_risk"] += 0.1

                # Equipment failure risk
                condition = equipment.durability.condition
                risks["equipment_failure_risk"] += (1.0 - condition) * 0.2

                # Maintenance risk
                if equipment.durability.maintenance_required:
                    risks["maintenance_risk"] += 0.2

        # Normalize risks
        for risk_type in risks:
            risks[risk_type] = min(1.0, risks[risk_type])

        return risks

    def _calculate_success_boost(
        self,
        recommended_equipment: Dict[LoadoutSlot, List[EnhancedEquipmentProfile]],
        mission_type: str,
    ) -> float:
        """Calculate success probability boost from equipment"""
        boost = 0.0

        for slot, equipment_list in recommended_equipment.items():
            if equipment_list:
                equipment = equipment_list[0]

                # Mission modifier
                boost += equipment.get_mission_bonus(mission_type)

                # Quality modifier
                boost += equipment.durability.get_effectiveness_modifier() * 0.1

        return min(0.5, max(-0.2, boost))  # Cap between -20% and +50%

    def _calculate_concealment_rating(
        self, recommended_equipment: Dict[LoadoutSlot, List[EnhancedEquipmentProfile]]
    ) -> float:
        """Calculate overall concealment rating"""
        total_concealment = 0.0
        count = 0

        for slot, equipment_list in recommended_equipment.items():
            if equipment_list:
                equipment = equipment_list[0]
                concealment = equipment.get_effective_concealment()
                total_concealment += concealment
                count += 1

        return total_concealment / max(1, count)

    def _calculate_legal_risk(
        self, recommended_equipment: Dict[LoadoutSlot, List[EnhancedEquipmentProfile]]
    ) -> float:
        """Calculate overall legal risk"""
        risk = 0.0

        for slot, equipment_list in recommended_equipment.items():
            if equipment_list:
                equipment = equipment_list[0]
                if equipment.legal_status == LegalStatus.PROHIBITED:
                    risk += 0.3
                elif equipment.legal_status == LegalStatus.RESTRICTED:
                    risk += 0.1

        return min(1.0, risk)

    def apply_equipment_effects_to_mission(
        self,
        mission: Dict[str, Any],
        agents: List[Dict[str, Any]],
        loadouts: Dict[str, AgentLoadout],
    ) -> Dict[str, Any]:
        """Apply equipment effects to mission execution"""

        equipment_effects = {
            "success_modifier": 0.0,
            "skill_bonuses": {},
            "emotional_effects": {},
            "concealment_rating": 0.0,
            "legal_risk": 0.0,
            "equipment_degradation": {},
            "narrative_elements": [],
        }

        mission_type = mission.get("type", "propaganda")

        for agent in agents:
            agent_id = agent.get("id")
            loadout = loadouts.get(agent_id)

            if loadout:
                # Apply loadout effects
                equipment_effects["success_modifier"] += loadout.get_mission_modifier(
                    mission_type
                )

                # Skill bonuses
                for skill, bonus in loadout.equipment_bonuses.items():
                    if skill not in equipment_effects["skill_bonuses"]:
                        equipment_effects["skill_bonuses"][skill] = 0.0
                    equipment_effects["skill_bonuses"][skill] += bonus

                # Emotional effects
                for emotion, effect in loadout.emotional_effects.items():
                    if emotion not in equipment_effects["emotional_effects"]:
                        equipment_effects["emotional_effects"][emotion] = 0.0
                    equipment_effects["emotional_effects"][emotion] += effect

                # Concealment and legal risk
                equipment_effects["concealment_rating"] = max(
                    equipment_effects["concealment_rating"], loadout.concealment_rating
                )
                equipment_effects["legal_risk"] = max(
                    equipment_effects["legal_risk"], loadout.legal_risk
                )

                # Equipment degradation
                mission_intensity = mission.get("difficulty", 0.5)
                degradation = loadout.use_equipment_in_mission(mission_intensity)
                equipment_effects["equipment_degradation"][agent_id] = degradation

                # Generate narrative elements
                narrative_elements = self._generate_equipment_narrative(
                    loadout, mission_type, degradation
                )
                equipment_effects["narrative_elements"].extend(narrative_elements)

        return equipment_effects

    def _generate_equipment_narrative(
        self, loadout: AgentLoadout, mission_type: str, degradation: Dict[str, Any]
    ) -> List[str]:
        """Generate narrative elements based on equipment usage"""
        narrative_elements = []

        for slot, result in degradation.items():
            equipment_name = result["equipment_name"]

            if result["broken"]:
                narrative_elements.append(
                    f"The {equipment_name} failed catastrophically during the mission."
                )
            elif result["maintenance_required"]:
                narrative_elements.append(
                    f"The {equipment_name} showed signs of wear and needs maintenance."
                )
            elif result["degradation"] < -0.1:
                narrative_elements.append(
                    f"The {equipment_name} suffered significant damage during use."
                )

        # Add equipment-specific narrative
        for slot, equipment in loadout.equipment.items():
            if equipment.durability.condition < 0.3:
                narrative_elements.append(
                    f"The {equipment.name} is in poor condition and may fail soon."
                )

        return narrative_elements

    def get_equipment_maintenance_report(self) -> Dict[str, Any]:
        """Generate maintenance report for all equipment"""
        maintenance_report = {
            "broken_equipment": [],
            "maintenance_required": [],
            "repair_costs": 0,
            "total_equipment": 0,
        }

        for loadout in self.agent_loadouts.values():
            for slot, equipment in loadout.equipment.items():
                maintenance_report["total_equipment"] += 1

                if equipment.durability.condition <= 0.0:
                    maintenance_report["broken_equipment"].append(
                        {
                            "agent_id": loadout.agent_id,
                            "slot": slot.value,
                            "equipment": equipment.name,
                            "repair_cost": equipment.durability.repair_cost,
                        }
                    )
                    maintenance_report[
                        "repair_costs"
                    ] += equipment.durability.repair_cost

                elif equipment.durability.maintenance_required:
                    maintenance_report["maintenance_required"].append(
                        {
                            "agent_id": loadout.agent_id,
                            "slot": slot.value,
                            "equipment": equipment.name,
                            "condition": equipment.durability.condition,
                        }
                    )

        return maintenance_report
