"""
Equipment Profile and Search System for Years of Lead

This module implements equipment profiles with concealment mechanics, legal status tracking,
and search encounter systems for realistic item detection gameplay.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import random
from loguru import logger


class EquipmentCategory(Enum):
    """Categories of equipment with different rules"""

    WEAPON = "weapon"
    ARMOR = "armor"
    ELECTRONIC = "electronic"
    MEDICAL = "medical"
    DOCUMENT = "document"
    TOOL = "tool"
    CONTRABAND = "contraband"
    CURRENCY = "currency"
    COMMUNICATION = "communication"
    EXPLOSIVE = "explosive"


class LegalStatus(Enum):
    """Legal status classifications for equipment"""

    LEGAL = "legal"
    RESTRICTED = "restricted"  # Legal with permit
    PROHIBITED = "prohibited"  # Illegal to possess
    CONTRABAND = "contraband"  # Extremely illegal


class ConsequenceType(Enum):
    """Types of consequences when equipment is discovered"""

    IGNORE = "ignore"
    CONFISCATE_AND_WARN = "confiscate_and_warn"
    CONFISCATE_AND_FINE = "confiscate_and_fine"
    INTERROGATION_AND_CONFISCATION = "interrogation_and_confiscation"
    ARREST = "arrest"
    ARREST_AND_FLAG = "arrest_and_flag"
    IMMEDIATE_DETENTION = "immediate_detention"
    MILD_SUSPICION_ONLY = "mild_suspicion_only"
    ITEM_LOGGED_BUT_RELEASED = "item_logged_but_released"


class PlayerUniformType(Enum):
    """Types of uniforms that affect search outcomes"""

    CIVILIAN = "civilian"
    MEDICAL = "medical"
    MAINTENANCE = "maintenance"
    DELIVERY = "delivery"
    PRESS = "press"
    OFFICIAL = "official"
    SECURITY = "security"


@dataclass
class EquipmentFlag:
    """Flags that modify equipment behavior and detection"""

    flag_id: str
    name: str
    description: str
    concealment_modifier: float = 0.0  # Positive makes harder to detect
    suspicion_modifier: float = 0.0  # Positive increases suspicion
    consequence_modifier: str = ""  # Changes consequence type


@dataclass
class ConsequenceRule:
    """Rules for consequences based on conditions"""

    condition: str  # e.g., "no_permit", "has_permit", "player_uniformed"
    consequence: ConsequenceType
    description: str = ""
    additional_effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EquipmentProfile:
    """Complete equipment profile with concealment and legal mechanics"""

    item_id: str
    name: str
    category: EquipmentCategory

    # Concealment properties
    concealable: bool = True
    concealment_rating: float = (
        0.5  # 0.0 = impossible to hide, 1.0 = perfect concealment
    )
    container_bonus: float = 0.0  # Additional concealment when in containers

    # Legal properties
    legal_status: LegalStatus = LegalStatus.LEGAL
    detected_if_searched: bool = True

    # Consequence system
    consequence_rules: Dict[str, ConsequenceRule] = field(default_factory=dict)

    # Equipment flags
    associated_flags: Set[str] = field(default_factory=set)

    # Metadata
    description: str = ""
    weight: float = 1.0
    bulk: float = 1.0
    value: int = 0

    def __post_init__(self):
        """Initialize default consequence rules if none provided"""
        if not self.consequence_rules:
            self._create_default_consequences()

    def _create_default_consequences(self):
        """Create default consequence rules based on legal status"""
        if self.legal_status == LegalStatus.LEGAL:
            self.consequence_rules["default"] = ConsequenceRule(
                condition="default",
                consequence=ConsequenceType.MILD_SUSPICION_ONLY,
                description="Legal item causes minimal concern",
            )
        elif self.legal_status == LegalStatus.RESTRICTED:
            self.consequence_rules["default"] = ConsequenceRule(
                condition="no_permit",
                consequence=ConsequenceType.INTERROGATION_AND_CONFISCATION,
                description="Restricted item without permit",
            )
            self.consequence_rules["has_permit"] = ConsequenceRule(
                condition="has_permit",
                consequence=ConsequenceType.ITEM_LOGGED_BUT_RELEASED,
                description="Restricted item with valid permit",
            )
        elif self.legal_status == LegalStatus.PROHIBITED:
            self.consequence_rules["default"] = ConsequenceRule(
                condition="default",
                consequence=ConsequenceType.ARREST,
                description="Prohibited item possession",
            )
        elif self.legal_status == LegalStatus.CONTRABAND:
            self.consequence_rules["default"] = ConsequenceRule(
                condition="default",
                consequence=ConsequenceType.ARREST_AND_FLAG,
                description="Contraband possession - serious offense",
            )

    def get_effective_concealment(
        self, container_present: bool = False, equipment_flags: Set[str] = None
    ) -> float:
        """Calculate effective concealment rating with modifiers"""
        if not self.concealable:
            return 0.0

        base_concealment = self.concealment_rating

        # Container bonus
        if container_present:
            base_concealment += self.container_bonus

        # Flag modifiers
        if equipment_flags:
            # Note: Flag effects would be handled by the SearchEncounterManager
            # This is a simplified version for equipment profile calculation
            pass

        return min(1.0, max(0.0, base_concealment))

    def get_consequence(self, player_context: Dict[str, Any]) -> ConsequenceRule:
        """Determine appropriate consequence based on player context"""

        # Check for uniform-specific rules
        if player_context.get("uniformed", False):
            uniform_type = player_context.get(
                "uniform_type", PlayerUniformType.CIVILIAN
            )
            uniform_rule_key = f"if_player_{uniform_type.value}"
            if uniform_rule_key in self.consequence_rules:
                return self.consequence_rules[uniform_rule_key]

        # Check for permit
        if self.legal_status == LegalStatus.RESTRICTED:
            has_permit = player_context.get("has_permit", False)
            if has_permit and "has_permit" in self.consequence_rules:
                return self.consequence_rules["has_permit"]

        # Default consequence
        return self.consequence_rules.get(
            "default",
            ConsequenceRule(
                condition="default",
                consequence=ConsequenceType.CONFISCATE_AND_WARN,
                description="Standard procedure",
            ),
        )


class SearchRigor(Enum):
    """Search thoroughness levels"""

    CURSORY = 0.2  # Quick pat-down
    STANDARD = 0.4  # Normal search
    THOROUGH = 0.6  # Detailed search
    INTENSIVE = 0.8  # Full strip search
    FORENSIC = 1.0  # Complete forensic examination


class NPCDisposition(Enum):
    """NPC attitudes affecting search behavior"""

    RELAXED = "relaxed"  # -0.1 to search rigor
    PROFESSIONAL = "professional"  # No modifier
    SUSPICIOUS = "suspicious"  # +0.1 to search rigor
    PARANOID = "paranoid"  # +0.2 to search rigor
    HOSTILE = "hostile"  # +0.3 to search rigor


@dataclass
class NPCProfile:
    """Profile for search NPCs"""

    search_rigor: float = 0.5
    tech_bonus: float = 0.0  # Technology assistance bonus
    disposition: NPCDisposition = NPCDisposition.PROFESSIONAL
    experience_level: float = 0.5  # 0.0 = rookie, 1.0 = expert
    corruption_level: float = 0.0  # 0.0 = incorruptible, 1.0 = easily bribed

    def get_effective_search_rating(self) -> float:
        """Calculate effective search rating with all modifiers"""
        base_rating = self.search_rigor

        # Disposition modifier
        disposition_modifiers = {
            NPCDisposition.RELAXED: -0.1,
            NPCDisposition.PROFESSIONAL: 0.0,
            NPCDisposition.SUSPICIOUS: 0.1,
            NPCDisposition.PARANOID: 0.2,
            NPCDisposition.HOSTILE: 0.3,
        }

        base_rating += disposition_modifiers.get(self.disposition, 0.0)
        base_rating += self.tech_bonus
        base_rating += (self.experience_level - 0.5) * 0.2  # Experience modifier

        return min(1.0, max(0.0, base_rating))


@dataclass
class PlayerResponse:
    """Player response option during search encounter"""

    response_id: str
    text: str
    outcome: str
    suspicion_modifier: float = 0.0
    skill_check: Optional[str] = None  # e.g., "social", "stealth"
    difficulty: float = 0.5
    consequences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchTrigger:
    """Conditions that trigger a search encounter"""

    zone: str = "any"
    curfew_active: bool = False
    player_flagged: bool = False
    check_probability: float = 0.3
    time_of_day: Optional[str] = None  # "morning", "afternoon", "evening", "night"
    location_specific: bool = False

    def should_trigger(self, game_context: Dict[str, Any]) -> bool:
        """Determine if search should trigger based on context"""

        # Zone check
        if self.zone != "any" and game_context.get("current_zone") != self.zone:
            return False

        # Curfew check
        if self.curfew_active and not game_context.get("curfew_active", False):
            return False

        # Player flagging check
        if self.player_flagged and not game_context.get("player_flagged", False):
            return False

        # Time check
        if self.time_of_day and game_context.get("time_of_day") != self.time_of_day:
            return False

        # Probability check
        return random.random() < self.check_probability


@dataclass
class SearchEncounter:
    """Complete search encounter definition"""

    encounter_id: str
    location: str
    description: str
    trigger: SearchTrigger
    npc_profile: NPCProfile
    player_response_options: List[PlayerResponse] = field(default_factory=list)

    # Detection formula parameters
    base_detection_threshold: float = 0.5
    random_variance: float = 0.2

    def __post_init__(self):
        """Initialize default player responses if none provided"""
        if not self.player_response_options:
            self._create_default_responses()

    def _create_default_responses(self):
        """Create default player response options"""
        self.player_response_options = [
            PlayerResponse(
                response_id="comply",
                text="You open your bag and remain silent.",
                outcome="begin_item_reveal",
                suspicion_modifier=0.0,
            ),
            PlayerResponse(
                response_id="deflect",
                text="Do you really need to do this? I'm just trying to get home.",
                outcome="suspicion_roll",
                suspicion_modifier=0.2,
                skill_check="social",
                difficulty=0.6,
            ),
            PlayerResponse(
                response_id="resist",
                text="You step back and prepare to run.",
                outcome="combat_or_pursuit_triggered",
                suspicion_modifier=0.8,
                skill_check="stealth",
                difficulty=0.8,
            ),
        ]

    def calculate_detection_probability(
        self, equipment: EquipmentProfile, player_context: Dict[str, Any]
    ) -> float:
        """Calculate probability of detecting specific equipment"""

        # Get effective ratings
        search_rating = self.npc_profile.get_effective_search_rating()
        concealment_rating = equipment.get_effective_concealment(
            container_present=player_context.get("has_container", False),
            equipment_flags=player_context.get("equipment_flags", set()),
        )

        # Player bonuses (skills, etc.)
        player_bonus = player_context.get("concealment_bonus", 0.0)

        # Detection formula: search_rating + random - (concealment + player_bonus)
        detection_score = (
            search_rating
            + random.uniform(-self.random_variance, self.random_variance)
            - (concealment_rating + player_bonus)
        )

        # Convert to probability (0.0 to 1.0)
        return min(1.0, max(0.0, detection_score))

    def execute_search(
        self, player_inventory: List[EquipmentProfile], player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute complete search encounter"""

        results = {
            "encounter_id": self.encounter_id,
            "location": self.location,
            "detected_items": [],
            "missed_items": [],
            "consequences": [],
            "narrative": "",
            "suspicion_level": 0.0,
        }

        logger.info(
            f"Executing search encounter {self.encounter_id} at {self.location}"
        )

        # Process each item in inventory
        for equipment in player_inventory:
            if not equipment.detected_if_searched:
                continue

            detection_prob = self.calculate_detection_probability(
                equipment, player_context
            )

            if random.random() < detection_prob:
                # Item detected
                results["detected_items"].append(equipment)
                consequence_rule = equipment.get_consequence(player_context)
                results["consequences"].append(
                    {
                        "item": equipment.name,
                        "consequence": consequence_rule.consequence.value,
                        "description": consequence_rule.description,
                    }
                )
                logger.info(
                    f"Detected {equipment.name}: {consequence_rule.consequence.value}"
                )
            else:
                # Item missed
                results["missed_items"].append(equipment)
                logger.debug(
                    f"Missed {equipment.name} (concealment: {equipment.concealment_rating})"
                )

        # Calculate overall suspicion
        suspicion_factors = [
            len(results["detected_items"]) * 0.2,
            player_context.get("base_suspicion", 0.0),
            self._get_disposition_suspicion_modifier(),
        ]
        results["suspicion_level"] = min(1.0, sum(suspicion_factors))

        # Generate narrative
        results["narrative"] = self._generate_search_narrative(results, player_context)

        return results

    def _get_disposition_suspicion_modifier(self) -> float:
        """Get suspicion modifier based on NPC disposition"""
        modifiers = {
            NPCDisposition.RELAXED: -0.1,
            NPCDisposition.PROFESSIONAL: 0.0,
            NPCDisposition.SUSPICIOUS: 0.1,
            NPCDisposition.PARANOID: 0.2,
            NPCDisposition.HOSTILE: 0.3,
        }
        return modifiers.get(self.npc_profile.disposition, 0.0)

    def _generate_search_narrative(
        self, results: Dict[str, Any], player_context: Dict[str, Any]
    ) -> str:
        """Generate narrative description of search encounter"""

        narrative_parts = []

        # Opening
        disposition_text = {
            NPCDisposition.RELAXED: "The guard approaches casually",
            NPCDisposition.PROFESSIONAL: "The officer conducts a professional search",
            NPCDisposition.SUSPICIOUS: "The guard eyes you suspiciously",
            NPCDisposition.PARANOID: "The officer searches with intense scrutiny",
            NPCDisposition.HOSTILE: "The guard searches aggressively",
        }

        opening = disposition_text.get(
            self.npc_profile.disposition, "The search begins"
        )
        narrative_parts.append(f"{opening} at {self.location}.")

        # Detection results
        if results["detected_items"]:
            detected_names = [item.name for item in results["detected_items"]]
            narrative_parts.append(f"They discover: {', '.join(detected_names)}.")

        if results["missed_items"]:
            narrative_parts.append("Some items remain undetected.")

        # Consequences
        if results["consequences"]:
            consequence_texts = []
            for cons in results["consequences"]:
                if cons["consequence"] == "arrest":
                    consequence_texts.append("You are placed under arrest.")
                elif cons["consequence"] == "confiscate_and_warn":
                    consequence_texts.append(
                        f"Your {cons['item']} is confiscated with a warning."
                    )
                elif cons["consequence"] == "interrogation_and_confiscation":
                    consequence_texts.append(
                        f"You are questioned about your {cons['item']}."
                    )

            narrative_parts.extend(consequence_texts)

        # Closing
        if not results["detected_items"]:
            closing_texts = {
                NPCDisposition.RELAXED: "Alright, you're good to go.",
                NPCDisposition.PROFESSIONAL: "Move along. Have a safe day.",
                NPCDisposition.SUSPICIOUS: "I've got my eye on you. Move along.",
                NPCDisposition.PARANOID: "Don't test me next time. Keep moving.",
                NPCDisposition.HOSTILE: "Get out of here before I change my mind.",
            }
            closing = closing_texts.get(
                self.npc_profile.disposition, "You may proceed."
            )
            narrative_parts.append(f'"{closing}"')

        return " ".join(narrative_parts)


class SearchEncounterManager:
    """Manages search encounters and equipment detection"""

    def __init__(self):
        self.encounters: Dict[str, SearchEncounter] = {}
        self.equipment_registry: Dict[str, EquipmentProfile] = {}
        self.flag_registry: Dict[str, EquipmentFlag] = {}
        self.active_encounters: List[str] = []

        # Initialize with default content
        self._initialize_default_equipment()
        self._initialize_default_encounters()
        self._initialize_equipment_flags()

    def register_equipment(self, equipment: EquipmentProfile):
        """Register equipment profile"""
        self.equipment_registry[equipment.item_id] = equipment
        logger.info(f"Registered equipment: {equipment.name} ({equipment.item_id})")

    def register_encounter(self, encounter: SearchEncounter):
        """Register search encounter"""
        self.encounters[encounter.encounter_id] = encounter
        logger.info(f"Registered search encounter: {encounter.encounter_id}")

    def register_flag(self, flag: EquipmentFlag):
        """Register equipment flag"""
        self.flag_registry[flag.flag_id] = flag
        logger.info(f"Registered equipment flag: {flag.name}")

    def check_for_encounters(
        self, game_context: Dict[str, Any]
    ) -> Optional[SearchEncounter]:
        """Check if any encounters should trigger"""

        for encounter in self.encounters.values():
            if encounter.trigger.should_trigger(game_context):
                logger.info(f"Triggered search encounter: {encounter.encounter_id}")
                return encounter

        return None

    def execute_encounter(
        self,
        encounter_id: str,
        player_inventory: List[str],
        player_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a search encounter with player inventory"""

        if encounter_id not in self.encounters:
            raise ValueError(f"Unknown encounter: {encounter_id}")

        encounter = self.encounters[encounter_id]

        # Convert item IDs to equipment profiles
        equipment_list = []
        for item_id in player_inventory:
            if item_id in self.equipment_registry:
                equipment_list.append(self.equipment_registry[item_id])

        return encounter.execute_search(equipment_list, player_context)

    def get_equipment_concealment_rating(
        self, item_id: str, context: Dict[str, Any] = None
    ) -> float:
        """Get effective concealment rating for an item"""
        if context is None:
            context = {}

        if item_id not in self.equipment_registry:
            return 0.0

        equipment = self.equipment_registry[item_id]
        return equipment.get_effective_concealment(
            container_present=context.get("has_container", False),
            equipment_flags=context.get("equipment_flags", set()),
        )

    def _initialize_default_equipment(self):
        """Initialize default equipment profiles"""

        # Weapons
        compact_pistol = EquipmentProfile(
            item_id="wpn_001",
            name="compact pistol",
            category=EquipmentCategory.WEAPON,
            concealable=True,
            concealment_rating=0.7,
            container_bonus=0.1,
            legal_status=LegalStatus.RESTRICTED,
            detected_if_searched=True,
            associated_flags={"unregistered_serial", "smuggled"},
            description="Small, easily concealed handgun",
            weight=1.2,
            bulk=0.8,
        )

        # Add uniform-specific consequence
        compact_pistol.consequence_rules["if_player_uniformed"] = ConsequenceRule(
            condition="if_player_uniformed",
            consequence=ConsequenceType.CONFISCATE_AND_WARN,
            description="Weapon confiscated from uniformed personnel",
        )

        self.register_equipment(compact_pistol)

        # Electronics
        encrypted_phone = EquipmentProfile(
            item_id="elc_001",
            name="encrypted communication device",
            category=EquipmentCategory.ELECTRONIC,
            concealable=True,
            concealment_rating=0.8,
            container_bonus=0.2,
            legal_status=LegalStatus.PROHIBITED,
            associated_flags={"military_encryption", "foreign_made"},
            description="Military-grade encrypted communicator",
        )

        self.register_equipment(encrypted_phone)

        # Documents
        fake_id = EquipmentProfile(
            item_id="doc_001",
            name="forged identification papers",
            category=EquipmentCategory.DOCUMENT,
            concealable=True,
            concealment_rating=0.9,
            container_bonus=0.05,
            legal_status=LegalStatus.CONTRABAND,
            associated_flags={"professional_forgery", "government_seal"},
            description="High-quality forged identification documents",
        )

        self.register_equipment(fake_id)

        # Medical supplies
        medical_kit = EquipmentProfile(
            item_id="med_001",
            name="field medical kit",
            category=EquipmentCategory.MEDICAL,
            concealable=False,
            concealment_rating=0.2,
            legal_status=LegalStatus.LEGAL,
            description="Professional medical supplies",
        )

        self.register_equipment(medical_kit)

    def _initialize_default_encounters(self):
        """Initialize default search encounters"""

        # Checkpoint Alpha - High security
        checkpoint_alpha = SearchEncounter(
            encounter_id="search_chkpt_alpha",
            location="Checkpoint Alpha",
            description="Heavily fortified military checkpoint",
            trigger=SearchTrigger(
                zone="occupied",
                curfew_active=True,
                player_flagged=True,
                check_probability=0.55,
            ),
            npc_profile=NPCProfile(
                search_rigor=0.6,
                tech_bonus=0.3,
                disposition=NPCDisposition.PARANOID,
                experience_level=0.8,
            ),
        )

        self.register_encounter(checkpoint_alpha)

        # Random street patrol
        street_patrol = SearchEncounter(
            encounter_id="search_street_patrol",
            location="Street Patrol",
            description="Routine police patrol stop",
            trigger=SearchTrigger(zone="any", check_probability=0.2),
            npc_profile=NPCProfile(
                search_rigor=0.4,
                tech_bonus=0.1,
                disposition=NPCDisposition.PROFESSIONAL,
                experience_level=0.5,
            ),
        )

        self.register_encounter(street_patrol)

        # Metro station security
        metro_security = SearchEncounter(
            encounter_id="search_metro_station",
            location="Metro Security Checkpoint",
            description="Transit authority security screening",
            trigger=SearchTrigger(
                zone="transit", check_probability=0.8, location_specific=True
            ),
            npc_profile=NPCProfile(
                search_rigor=0.7,
                tech_bonus=0.4,
                disposition=NPCDisposition.SUSPICIOUS,
                experience_level=0.6,
            ),
        )

        self.register_encounter(metro_security)

    def _initialize_equipment_flags(self):
        """Initialize equipment flags"""

        flags = [
            EquipmentFlag(
                flag_id="unregistered_serial",
                name="Unregistered Serial Number",
                description="Item has filed-off or altered serial number",
                concealment_modifier=0.0,
                suspicion_modifier=0.3,
            ),
            EquipmentFlag(
                flag_id="smuggled",
                name="Smuggled Item",
                description="Item was illegally imported",
                concealment_modifier=-0.1,
                suspicion_modifier=0.2,
            ),
            EquipmentFlag(
                flag_id="military_encryption",
                name="Military Encryption",
                description="Uses military-grade encryption protocols",
                concealment_modifier=0.1,
                suspicion_modifier=0.4,
            ),
            EquipmentFlag(
                flag_id="professional_forgery",
                name="Professional Forgery",
                description="High-quality forged document",
                concealment_modifier=0.2,
                suspicion_modifier=-0.1,
            ),
        ]

        for flag in flags:
            self.register_flag(flag)

    def get_encounter_summary(self) -> Dict[str, Any]:
        """Get summary of all registered encounters and equipment"""
        return {
            "total_encounters": len(self.encounters),
            "total_equipment": len(self.equipment_registry),
            "total_flags": len(self.flag_registry),
            "encounter_ids": list(self.encounters.keys()),
            "equipment_categories": {
                category.value: len(
                    [
                        e
                        for e in self.equipment_registry.values()
                        if e.category == category
                    ]
                )
                for category in EquipmentCategory
            },
        }


# Utility functions for integration
def get_equipment_flag(flag_id: str) -> Optional[EquipmentFlag]:
    """Get equipment flag by ID - for use in other modules"""
    # This integrates with the SearchEncounterManager flag registry
    manager = SearchEncounterManager()
    return manager.flag_registry.get(flag_id)


def create_custom_equipment(item_data: Dict[str, Any]) -> EquipmentProfile:
    """Create equipment profile from dictionary data"""
    return EquipmentProfile(
        item_id=item_data["item_id"],
        name=item_data["name"],
        category=EquipmentCategory(item_data["category"]),
        concealable=item_data.get("concealable", True),
        concealment_rating=item_data.get("concealment_rating", 0.5),
        container_bonus=item_data.get("container_bonus", 0.0),
        legal_status=LegalStatus(item_data.get("legal_status", "legal")),
        detected_if_searched=item_data.get("detected_if_searched", True),
        associated_flags=set(item_data.get("associated_flags", [])),
        description=item_data.get("description", ""),
        weight=item_data.get("weight", 1.0),
        bulk=item_data.get("bulk", 1.0),
        value=item_data.get("value", 0),
    )


def create_custom_encounter(encounter_data: Dict[str, Any]) -> SearchEncounter:
    """Create search encounter from dictionary data"""
    trigger_data = encounter_data["trigger"]
    npc_data = encounter_data["npc_profile"]

    trigger = SearchTrigger(
        zone=trigger_data.get("zone", "any"),
        curfew_active=trigger_data.get("curfew_active", False),
        player_flagged=trigger_data.get("player_flagged", False),
        check_probability=trigger_data.get("check_probability", 0.3),
        time_of_day=trigger_data.get("time_of_day"),
        location_specific=trigger_data.get("location_specific", False),
    )

    npc_profile = NPCProfile(
        search_rigor=npc_data.get("search_rigor", 0.5),
        tech_bonus=npc_data.get("tech_bonus", 0.0),
        disposition=NPCDisposition(npc_data.get("disposition", "professional")),
        experience_level=npc_data.get("experience_level", 0.5),
        corruption_level=npc_data.get("corruption_level", 0.0),
    )

    # Create player responses if provided
    responses = []
    for resp_data in encounter_data.get("player_response_options", []):
        responses.append(
            PlayerResponse(
                response_id=resp_data["id"],
                text=resp_data["text"],
                outcome=resp_data["outcome"],
                suspicion_modifier=resp_data.get("suspicion_modifier", 0.0),
                skill_check=resp_data.get("skill_check"),
                difficulty=resp_data.get("difficulty", 0.5),
            )
        )

    return SearchEncounter(
        encounter_id=encounter_data["encounter_id"],
        location=encounter_data["location"],
        description=encounter_data.get("description", ""),
        trigger=trigger,
        npc_profile=npc_profile,
        player_response_options=responses,
    )
