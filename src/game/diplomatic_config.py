"""
Years of Lead - Diplomatic & Covert Operations Configuration

Configuration constants for diplomatic channels, alliances, espionage,
and covert operations to centralize hard-coded values.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class DiplomaticConstants:
    """Configuration constants for diplomatic systems"""

    # Secret Diplomatic Channel Constants
    BASE_TRUST_LEVEL: float = 0.5
    MAX_TRUST_LEVEL: float = 1.0
    MIN_TRUST_LEVEL: float = 0.0

    # Encryption & Security
    BASE_ENCRYPTION_STRENGTH: float = 0.7
    ENCRYPTION_DECAY_RATE: float = 0.05  # Per turn
    ENCRYPTION_UPGRADE_COST: int = 50

    # Leak Risk Constants
    BASE_LEAK_CHANCE: float = 0.1  # 10% base chance
    TRUST_LEAK_MODIFIER: float = -0.05  # Higher trust reduces leak chance
    ENCRYPTION_LEAK_MODIFIER: float = -0.08  # Better encryption reduces leaks
    SURVEILLANCE_HEAT_MODIFIER: float = 0.2  # Higher heat increases leaks

    # Alliance Constants
    SECRET_ALLIANCE_DISCOVERY_CHANCE: float = 0.05  # 5% per turn
    PUBLIC_ALLIANCE_STABILITY_BONUS: float = 0.2
    COERCED_ALLIANCE_INSTABILITY: float = 0.3

    # Betrayal Constants
    BETRAYAL_TRUST_THRESHOLD: float = 0.3  # Below this, betrayal becomes likely
    BETRAYAL_BASE_CHANCE: float = 0.15
    BETRAYAL_DESPERATION_MODIFIER: float = 0.1  # Per desperation level
    BETRAYAL_SCANDAL_MULTIPLIER: float = 2.0  # Scandal impact

    # Support & Resource Modifiers
    COVERT_SUPPORT_EFFICIENCY: float = 0.8  # 80% efficiency vs direct support
    JOINT_OPERATION_BONUS: float = 0.25  # 25% bonus for joint operations
    SECRET_FUNDING_DISCOUNT: float = 0.9  # 10% discount on secret funding

    # False Flag Operations
    FALSE_FLAG_BASE_SUCCESS: float = 0.6
    FALSE_FLAG_DETECTION_CHANCE: float = 0.25
    FALSE_FLAG_BLOWBACK_MULTIPLIER: float = 1.5

    # Double Agent Constants
    DOUBLE_AGENT_CONVERSION_CHANCE: float = 0.1
    DOUBLE_AGENT_EXPOSURE_CHANCE: float = 0.08
    DOUBLE_AGENT_INTELLIGENCE_BONUS: float = 0.4

    # Propaganda & Media Constants
    SCANDAL_MEDIA_SATURATION_THRESHOLD: int = 3  # Number of scandals for saturation
    BETRAYAL_TONE_DECAY_RATE: float = 0.1  # Per turn
    MEDIA_EXPOSURE_HEAT_MULTIPLIER: float = 1.2

    # Surveillance & Heat Constants
    DIPLOMATIC_ACTIVITY_HEAT_GAIN: int = 2
    LEAKED_OPERATION_HEAT_GAIN: int = 15
    EXPOSED_ALLIANCE_HEAT_GAIN: int = 25
    COUNTERINTELLIGENCE_ALERT_THRESHOLD: int = 30

    # Momentum & Clock Constants
    BETRAYAL_MOMENTUM_LOSS: int = 10
    ALLIANCE_DISCOVERY_MOMENTUM_LOSS: int = 5
    SUCCESSFUL_COVERT_OP_MOMENTUM_GAIN: int = 8

    # Memory & History Constants
    BETRAYAL_MEMORY_DURATION: int = 20  # Turns remembered
    ALLIANCE_HISTORY_WEIGHT: float = 0.3  # Weight in future decisions
    TRUST_REPAIR_RATE: float = 0.05  # Per turn for trust recovery

    # Mission & Operation Constants
    INFILTRATION_DISCOVERY_CHANCE: float = 0.12
    EXFILTRATION_FAILURE_PENALTIES: Dict[str, int] = field(
        default_factory=lambda: {"heat": 20, "exposure": 1, "trust_loss": 0.2}
    )

    # Character Development Constants
    ESPIONAGE_EXPERIENCE_GAIN: int = 15
    DIPLOMATIC_SKILL_BONUS: float = 0.1
    BETRAYAL_TRAUMA_PENALTY: float = -0.15


# Global instance
DIPLOMATIC_CONFIG = DiplomaticConstants()


class OperationalConstants:
    """Constants for specific operational types"""

    OPERATION_TYPES = {
        "INTELLIGENCE_SHARING": {
            "base_cost": 25,
            "trust_requirement": 0.6,
            "success_rate": 0.85,
            "heat_gain": 3,
        },
        "JOINT_SABOTAGE": {
            "base_cost": 75,
            "trust_requirement": 0.7,
            "success_rate": 0.75,
            "heat_gain": 12,
        },
        "COORDINATED_PROPAGANDA": {
            "base_cost": 40,
            "trust_requirement": 0.5,
            "success_rate": 0.90,
            "heat_gain": 5,
        },
        "RESOURCE_TRANSFER": {
            "base_cost": 15,
            "trust_requirement": 0.4,
            "success_rate": 0.95,
            "heat_gain": 1,
        },
        "FALSE_FLAG": {
            "base_cost": 100,
            "trust_requirement": 0.8,
            "success_rate": 0.60,
            "heat_gain": 25,
            "detection_chance": 0.30,
        },
    }

    SURVEILLANCE_THRESHOLDS = {
        "LOW": {"min_heat": 0, "detection_modifier": 0.0},
        "MEDIUM": {"min_heat": 20, "detection_modifier": 0.15},
        "HIGH": {"min_heat": 50, "detection_modifier": 0.30},
        "CRITICAL": {"min_heat": 80, "detection_modifier": 0.50},
    }


# Global instance
OPERATIONAL_CONFIG = OperationalConstants()
