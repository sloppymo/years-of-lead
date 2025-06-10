"""
Years of Lead - Therapy Module

# ITERATION_033

Implements agent-level therapy sessions and outcome logic.
"""

from __future__ import annotations
import uuid
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional
from .emotional_state import EmotionalState
from .support_networks import SupportNetwork


class TherapyType(Enum):
    """Enumerates available therapy modalities."""
    INDIVIDUAL = "individual"
    GROUP = "group"
    MEDICATION = "medication"
    # More types can be added in future iterations


@dataclass
class TherapyOutcome:
    """Container for session results."""
    success: bool
    relapse: bool
    recovery_score: float
    narrative: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TherapySession:
    """Represents a single therapy session for an agent."""

    agent_id: str
    therapy_type: TherapyType
    duration_hours: int = 1
    base_effectiveness: float = 0.2  # Baseline recovery score (0–1)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def _calculate_recovery(self, emotional_state: EmotionalState, support: Optional[SupportNetwork]) -> float:
        """Compute recovery score based on therapy type and modifiers."""
        effectiveness = self.base_effectiveness

        # Therapy-specific modifiers
        if self.therapy_type == TherapyType.GROUP:
            effectiveness += 0.05  # peer empathy
        elif self.therapy_type == TherapyType.MEDICATION:
            effectiveness += 0.1  # faster chemical relief

        # Diminishing returns for low trauma
        if emotional_state.trauma_level < 0.2:
            effectiveness *= 0.5

        # Support network bonus
        if support:
            effectiveness += support.get_resilience_modifier() * 0.5

        # Clamp
        return max(0.0, min(1.0, effectiveness))

    def conduct(self, emotional_state: EmotionalState, support: Optional[SupportNetwork] = None) -> TherapyOutcome:
        """Run the therapy session, mutating the emotional state and returning outcome."""
        recovery_score = self._calculate_recovery(emotional_state, support)
        emotional_state.apply_therapy_effect(recovery_score)

        # Relapse check (lower base chance right after therapy)
        relapse = emotional_state.check_relapse(base_chance=0.05, resilience_modifier=support.get_resilience_modifier() if support else 0.0)

        narrative = ""
        if relapse:
            narrative = "Relapse occurred despite therapy; emotions destabilised."
        else:
            narrative = "Therapy helped alleviate trauma and improve outlook."

        return TherapyOutcome(
            success=not relapse,
            relapse=relapse,
            recovery_score=recovery_score,
            narrative=narrative,
            details={
                "therapy_type": self.therapy_type.value,
                "support_bonus": support.get_resilience_modifier() if support else 0.0,
            }
        ) 