"""
Enhanced Equipment System for Years of Lead - Phase 1 Implementation

This module extends the base equipment system with:
1. Equipment variety expansion (20+ new items)
2. Quality & durability system
3. Equipment effects & bonuses
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
from .equipment_system import (
    EquipmentCategory,
    LegalStatus,
    EquipmentProfile,
)


class EquipmentQuality(Enum):
    """Equipment quality levels"""

    BROKEN = 0.0
    POOR = 0.25
    FAIR = 0.5
    GOOD = 0.75
    EXCELLENT = 1.0


@dataclass
class EquipmentDurability:
    """Equipment durability and condition tracking"""

    condition: float = 1.0  # 0.0 = broken, 1.0 = perfect
    reliability: float = 0.8  # Success chance modifier
    maintenance_required: bool = False
    degradation_rate: float = 0.01  # Per use
    repair_cost: float = 0.0  # Cost to repair
    max_repairs: int = 3  # Maximum repair attempts
    repair_count: int = 0  # Current number of repairs
    last_maintenance: int = 0  # Turn of last maintenance

    def use_equipment(self, intensity: float = 1.0) -> bool:
        """Use equipment and apply degradation"""
        if self.condition <= 0.0:
            return False  # Equipment is broken

        # Apply degradation
        degradation = self.degradation_rate * intensity
        self.condition = max(0.0, self.condition - degradation)

        # Check if maintenance is needed
        if self.condition < 0.5:
            self.maintenance_required = True

        return True

    def repair_equipment(self, quality: float = 1.0) -> bool:
        """Repair equipment"""
        if self.repair_count >= self.max_repairs:
            return False  # Cannot repair further

        if self.condition >= 1.0:
            return False  # Already in perfect condition

        # Repair based on quality
        repair_amount = quality * 0.3  # 30% repair per attempt
        self.condition = min(1.0, self.condition + repair_amount)
        self.repair_count += 1
        self.maintenance_required = False

        return True

    def get_effectiveness_modifier(self) -> float:
        """Get effectiveness modifier based on condition"""
        if self.condition <= 0.0:
            return 0.0  # Broken equipment is useless
        elif self.condition < 0.3:
            return 0.3  # Poor condition
        elif self.condition < 0.6:
            return 0.6  # Fair condition
        elif self.condition < 0.9:
            return 0.9  # Good condition
        else:
            return 1.0  # Excellent condition


@dataclass
class EquipmentEffects:
    """Equipment effects and bonuses"""

    skill_bonuses: Dict[str, float] = field(default_factory=dict)
    mission_modifiers: Dict[str, float] = field(default_factory=dict)
    emotional_effects: Dict[str, float] = field(default_factory=dict)
    social_effects: Dict[str, float] = field(default_factory=dict)
    concealment_bonuses: Dict[str, float] = field(default_factory=dict)
    detection_penalties: Dict[str, float] = field(default_factory=dict)

    def get_total_skill_bonus(self, skill: str) -> float:
        """Get total bonus for a specific skill"""
        return self.skill_bonuses.get(skill, 0.0)

    def get_mission_modifier(self, mission_type: str) -> float:
        """Get modifier for a specific mission type"""
        return self.mission_modifiers.get(mission_type, 0.0)

    def get_emotional_effect(self, emotion: str) -> float:
        """Get emotional effect modifier"""
        return self.emotional_effects.get(emotion, 0.0)

    def get_social_effect(self, context: str) -> float:
        """Get social effect modifier"""
        return self.social_effects.get(context, 0.0)


@dataclass
class EnhancedEquipmentProfile(EquipmentProfile):
    """Enhanced equipment profile with quality and effects"""

    durability: EquipmentDurability = field(default_factory=EquipmentDurability)
    effects: EquipmentEffects = field(default_factory=EquipmentEffects)
    signature_properties: Dict[str, Any] = field(default_factory=dict)
    faction_affiliation: Optional[str] = None
    rarity: float = 0.5  # 0.0 = common, 1.0 = legendary

    def get_effective_concealment(
        self,
        container_present: bool = False,
        equipment_flags: Set[str] = None,
        context: Dict[str, Any] = None,
    ) -> float:
        """Calculate effective concealment with quality and effects"""
        base_concealment = super().get_effective_concealment(
            container_present, equipment_flags
        )

        # Apply quality modifier
        quality_modifier = self.durability.get_effectiveness_modifier()
        base_concealment *= quality_modifier

        # Apply concealment bonuses from effects
        if context:
            for context_type, bonus in self.effects.concealment_bonuses.items():
                if context.get(context_type, False):
                    base_concealment += bonus

        return min(1.0, max(0.0, base_concealment))

    def use_equipment(self, intensity: float = 1.0) -> bool:
        """Use equipment and apply degradation"""
        return self.durability.use_equipment(intensity)

    def get_skill_bonus(self, skill: str) -> float:
        """Get skill bonus for this equipment"""
        return self.effects.get_total_skill_bonus(skill)

    def get_mission_bonus(self, mission_type: str) -> float:
        """Get mission bonus for this equipment"""
        return self.effects.get_mission_modifier(mission_type)


class EnhancedEquipmentManager:
    """Manager for enhanced equipment system"""

    def __init__(self):
        self.equipment_registry: Dict[str, EnhancedEquipmentProfile] = {}
        self.initialize_enhanced_equipment()

    def register_equipment(self, equipment: EnhancedEquipmentProfile):
        """Register enhanced equipment"""
        self.equipment_registry[equipment.item_id] = equipment
        logger.info(
            f"Registered enhanced equipment: {equipment.name} ({equipment.item_id})"
        )

    def get_equipment(self, item_id: str) -> Optional[EnhancedEquipmentProfile]:
        """Get equipment by ID"""
        return self.equipment_registry.get(item_id)

    def initialize_enhanced_equipment(self):
        """Initialize all enhanced equipment items"""

        # === WEAPONS ===

        # Assault Rifle
        assault_rifle = EnhancedEquipmentProfile(
            item_id="wpn_002",
            name="assault rifle",
            category=EquipmentCategory.WEAPON,
            concealable=False,
            concealment_rating=0.1,
            legal_status=LegalStatus.PROHIBITED,
            description="Military-grade automatic rifle",
            weight=3.5,
            bulk=2.0,
            value=2500,
            rarity=0.7,
            durability=EquipmentDurability(
                condition=0.9, reliability=0.85, degradation_rate=0.02, repair_cost=500
            ),
            effects=EquipmentEffects(
                skill_bonuses={"combat": 0.4, "intimidation": 0.3},
                mission_modifiers={"sabotage": 0.2, "propaganda": -0.1},
                emotional_effects={"fear": 0.2, "confidence": 0.3},
                social_effects={"military": 0.2, "civilian": -0.3},
            ),
        )
        self.register_equipment(assault_rifle)

        # Silenced Pistol
        silenced_pistol = EnhancedEquipmentProfile(
            item_id="wpn_005",
            name="silenced pistol",
            category=EquipmentCategory.WEAPON,
            concealable=True,
            concealment_rating=0.8,
            container_bonus=0.2,
            legal_status=LegalStatus.PROHIBITED,
            description="Compact pistol with integrated suppressor",
            weight=1.0,
            bulk=0.6,
            value=1800,
            rarity=0.8,
            durability=EquipmentDurability(
                condition=0.95, reliability=0.9, degradation_rate=0.015, repair_cost=300
            ),
            effects=EquipmentEffects(
                skill_bonuses={"combat": 0.2, "stealth": 0.4},
                mission_modifiers={"intelligence": 0.3, "sabotage": 0.1},
                emotional_effects={"confidence": 0.2},
                concealment_bonuses={"stealth_mission": 0.2},
            ),
        )
        self.register_equipment(silenced_pistol)

        # Combat Knife
        combat_knife = EnhancedEquipmentProfile(
            item_id="wpn_006",
            name="combat knife",
            category=EquipmentCategory.WEAPON,
            concealable=True,
            concealment_rating=0.9,
            container_bonus=0.1,
            legal_status=LegalStatus.RESTRICTED,
            description="Military combat knife",
            weight=0.3,
            bulk=0.2,
            value=150,
            rarity=0.4,
            durability=EquipmentDurability(
                condition=0.98, reliability=0.95, degradation_rate=0.005, repair_cost=50
            ),
            effects=EquipmentEffects(
                skill_bonuses={"combat": 0.15, "stealth": 0.2},
                mission_modifiers={"intelligence": 0.1},
                emotional_effects={"confidence": 0.1},
            ),
        )
        self.register_equipment(combat_knife)

        # === ELECTRONICS ===

        # Laptop Computer
        laptop = EnhancedEquipmentProfile(
            item_id="elc_002",
            name="laptop computer",
            category=EquipmentCategory.ELECTRONIC,
            concealable=True,
            concealment_rating=0.6,
            container_bonus=0.1,
            legal_status=LegalStatus.LEGAL,
            description="High-performance laptop for hacking and intelligence",
            weight=2.5,
            bulk=1.5,
            value=1200,
            rarity=0.6,
            durability=EquipmentDurability(
                condition=0.85, reliability=0.8, degradation_rate=0.01, repair_cost=200
            ),
            effects=EquipmentEffects(
                skill_bonuses={"hacking": 0.5, "intelligence": 0.3},
                mission_modifiers={"intelligence": 0.4, "propaganda": 0.2},
                emotional_effects={"confidence": 0.1},
                social_effects={"corporate": 0.1},
            ),
        )
        self.register_equipment(laptop)

        # Signal Jammer
        signal_jammer = EnhancedEquipmentProfile(
            item_id="elc_004",
            name="signal jammer",
            category=EquipmentCategory.ELECTRONIC,
            concealable=True,
            concealment_rating=0.7,
            container_bonus=0.15,
            legal_status=LegalStatus.PROHIBITED,
            description="Portable signal jamming device",
            weight=1.8,
            bulk=1.2,
            value=800,
            rarity=0.7,
            durability=EquipmentDurability(
                condition=0.8, reliability=0.75, degradation_rate=0.02, repair_cost=150
            ),
            effects=EquipmentEffects(
                skill_bonuses={"hacking": 0.3, "stealth": 0.2},
                mission_modifiers={"sabotage": 0.3, "intelligence": 0.2},
                emotional_effects={"anxiety": 0.1},
            ),
        )
        self.register_equipment(signal_jammer)

        # === TOOLS ===

        # Lockpick Set
        lockpicks = EnhancedEquipmentProfile(
            item_id="tool_001",
            name="lockpick set",
            category=EquipmentCategory.TOOL,
            concealable=True,
            concealment_rating=0.95,
            container_bonus=0.05,
            legal_status=LegalStatus.RESTRICTED,
            description="Professional lockpicking tools",
            weight=0.2,
            bulk=0.1,
            value=200,
            rarity=0.5,
            durability=EquipmentDurability(
                condition=0.9, reliability=0.85, degradation_rate=0.008, repair_cost=30
            ),
            effects=EquipmentEffects(
                skill_bonuses={"stealth": 0.4, "infiltration": 0.3},
                mission_modifiers={"intelligence": 0.3, "sabotage": 0.2},
                emotional_effects={"confidence": 0.1},
            ),
        )
        self.register_equipment(lockpicks)

        # Demolition Kit
        demo_kit = EnhancedEquipmentProfile(
            item_id="tool_002",
            name="demolition kit",
            category=EquipmentCategory.TOOL,
            concealable=False,
            concealment_rating=0.3,
            container_bonus=0.2,
            legal_status=LegalStatus.PROHIBITED,
            description="Professional demolition equipment",
            weight=4.0,
            bulk=2.5,
            value=1500,
            rarity=0.8,
            durability=EquipmentDurability(
                condition=0.85, reliability=0.8, degradation_rate=0.025, repair_cost=400
            ),
            effects=EquipmentEffects(
                skill_bonuses={"demolitions": 0.6, "engineering": 0.3},
                mission_modifiers={"sabotage": 0.5},
                emotional_effects={"fear": 0.2, "confidence": 0.3},
            ),
        )
        self.register_equipment(demo_kit)

        # Disguise Kit
        disguise_kit = EnhancedEquipmentProfile(
            item_id="tool_004",
            name="disguise kit",
            category=EquipmentCategory.TOOL,
            concealable=True,
            concealment_rating=0.8,
            container_bonus=0.1,
            legal_status=LegalStatus.LEGAL,
            description="Professional disguise and makeup kit",
            weight=1.5,
            bulk=1.0,
            value=300,
            rarity=0.6,
            durability=EquipmentDurability(
                condition=0.9, reliability=0.85, degradation_rate=0.01, repair_cost=80
            ),
            effects=EquipmentEffects(
                skill_bonuses={"stealth": 0.3, "social": 0.2},
                mission_modifiers={"intelligence": 0.3, "recruitment": 0.2},
                emotional_effects={"confidence": 0.2},
                concealment_bonuses={"identity_concealment": 0.3},
            ),
        )
        self.register_equipment(disguise_kit)

        # === ARMOR ===

        # Bulletproof Vest
        bulletproof_vest = EnhancedEquipmentProfile(
            item_id="arm_001",
            name="bulletproof vest",
            category=EquipmentCategory.ARMOR,
            concealable=False,
            concealment_rating=0.2,
            legal_status=LegalStatus.RESTRICTED,
            description="Military-grade body armor",
            weight=3.0,
            bulk=2.0,
            value=800,
            rarity=0.6,
            durability=EquipmentDurability(
                condition=0.9, reliability=0.9, degradation_rate=0.015, repair_cost=200
            ),
            effects=EquipmentEffects(
                skill_bonuses={"combat": 0.2, "survival": 0.3},
                mission_modifiers={"sabotage": 0.1},
                emotional_effects={"confidence": 0.3, "fear": -0.1},
                social_effects={"military": 0.2, "civilian": -0.2},
            ),
        )
        self.register_equipment(bulletproof_vest)

        # === MEDICAL ===

        # Advanced Medical Kit
        advanced_medkit = EnhancedEquipmentProfile(
            item_id="med_002",
            name="advanced medical kit",
            category=EquipmentCategory.MEDICAL,
            concealable=False,
            concealment_rating=0.3,
            legal_status=LegalStatus.LEGAL,
            description="Comprehensive field medical equipment",
            weight=2.0,
            bulk=1.5,
            value=600,
            rarity=0.5,
            durability=EquipmentDurability(
                condition=0.95, reliability=0.9, degradation_rate=0.005, repair_cost=100
            ),
            effects=EquipmentEffects(
                skill_bonuses={"medical": 0.5, "survival": 0.2},
                mission_modifiers={"intelligence": 0.1, "recruitment": 0.1},
                emotional_effects={"confidence": 0.1, "fear": -0.1},
                social_effects={"medical": 0.3, "civilian": 0.1},
            ),
        )
        self.register_equipment(advanced_medkit)

        # === DOCUMENTS ===

        # Corporate ID
        corporate_id = EnhancedEquipmentProfile(
            item_id="doc_002",
            name="corporate identification",
            category=EquipmentCategory.DOCUMENT,
            concealable=True,
            concealment_rating=0.95,
            container_bonus=0.02,
            legal_status=LegalStatus.LEGAL,
            description="Legitimate corporate identification",
            weight=0.1,
            bulk=0.05,
            value=50,
            rarity=0.3,
            durability=EquipmentDurability(
                condition=0.98, reliability=0.95, degradation_rate=0.001, repair_cost=10
            ),
            effects=EquipmentEffects(
                skill_bonuses={"social": 0.2},
                mission_modifiers={"intelligence": 0.2, "recruitment": 0.1},
                emotional_effects={"confidence": 0.1},
                social_effects={"corporate": 0.4, "official": 0.2},
            ),
        )
        self.register_equipment(corporate_id)

        # === COMMUNICATION ===

        # Burner Phone
        burner_phone = EnhancedEquipmentProfile(
            item_id="com_001",
            name="burner phone",
            category=EquipmentCategory.COMMUNICATION,
            concealable=True,
            concealment_rating=0.9,
            container_bonus=0.05,
            legal_status=LegalStatus.LEGAL,
            description="Disposable mobile phone",
            weight=0.2,
            bulk=0.1,
            value=30,
            rarity=0.2,
            durability=EquipmentDurability(
                condition=0.9, reliability=0.8, degradation_rate=0.01, repair_cost=5
            ),
            effects=EquipmentEffects(
                skill_bonuses={"communication": 0.2},
                mission_modifiers={"intelligence": 0.1, "recruitment": 0.1},
                emotional_effects={"confidence": 0.05},
                concealment_bonuses={"communication_security": 0.3},
            ),
        )
        self.register_equipment(burner_phone)

        # === CURRENCY ===

        # Cash Bundle
        cash_bundle = EnhancedEquipmentProfile(
            item_id="cur_001",
            name="cash bundle",
            category=EquipmentCategory.CURRENCY,
            concealable=True,
            concealment_rating=0.8,
            container_bonus=0.1,
            legal_status=LegalStatus.LEGAL,
            description="Large bundle of cash",
            weight=0.5,
            bulk=0.3,
            value=5000,
            rarity=0.7,
            durability=EquipmentDurability(
                condition=0.95, reliability=1.0, degradation_rate=0.001, repair_cost=0
            ),
            effects=EquipmentEffects(
                skill_bonuses={"persuasion": 0.3},
                mission_modifiers={"recruitment": 0.4, "financing": 0.5},
                emotional_effects={"confidence": 0.2},
                social_effects={"criminal": 0.2},
            ),
        )
        self.register_equipment(cash_bundle)

        # === EXPLOSIVES ===

        # Improvised Explosive
        improvised_explosive = EnhancedEquipmentProfile(
            item_id="exp_001",
            name="improvised explosive device",
            category=EquipmentCategory.EXPLOSIVE,
            concealable=True,
            concealment_rating=0.6,
            container_bonus=0.2,
            legal_status=LegalStatus.CONTRABAND,
            description="Homemade explosive device",
            weight=1.5,
            bulk=1.0,
            value=200,
            rarity=0.8,
            durability=EquipmentDurability(
                condition=0.7, reliability=0.6, degradation_rate=0.03, repair_cost=100
            ),
            effects=EquipmentEffects(
                skill_bonuses={"demolitions": 0.4},
                mission_modifiers={"sabotage": 0.6},
                emotional_effects={"fear": 0.4, "anxiety": 0.3},
                social_effects={"criminal": 0.4},
            ),
        )
        self.register_equipment(improvised_explosive)

    def get_equipment_by_category(
        self, category: EquipmentCategory
    ) -> List[EnhancedEquipmentProfile]:
        """Get all equipment in a specific category"""
        return [
            eq for eq in self.equipment_registry.values() if eq.category == category
        ]

    def get_equipment_by_rarity(
        self, min_rarity: float = 0.0, max_rarity: float = 1.0
    ) -> List[EnhancedEquipmentProfile]:
        """Get equipment within a rarity range"""
        return [
            eq
            for eq in self.equipment_registry.values()
            if min_rarity <= eq.rarity <= max_rarity
        ]

    def get_equipment_summary(self) -> Dict[str, Any]:
        """Get summary of all registered equipment"""
        categories = {}
        for category in EquipmentCategory:
            category_items = self.get_equipment_by_category(category)
            categories[category.value] = {
                "count": len(category_items),
                "items": [item.name for item in category_items],
            }

        return {
            "total_equipment": len(self.equipment_registry),
            "categories": categories,
            "rarity_distribution": {
                "common": len(self.get_equipment_by_rarity(0.0, 0.3)),
                "uncommon": len(self.get_equipment_by_rarity(0.3, 0.6)),
                "rare": len(self.get_equipment_by_rarity(0.6, 0.8)),
                "legendary": len(self.get_equipment_by_rarity(0.8, 1.0)),
            },
        }


# Global instance
enhanced_equipment_manager = EnhancedEquipmentManager()
