"""
Years of Lead - Support Networks Module

# ITERATION_033

Provides lightweight modelling of informal/organizational support structures
that buffer agents against trauma and improve therapy outcomes.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid


@dataclass
class SupportNetwork:
    """Represents a support network of peers, therapists, or mentors."""

    name: str
    faction_id: Optional[str] = None
    members: List[str] = field(default_factory=list)
    resilience_bonus: float = 0.1  # 0.0–0.3 typical range
    passive_recovery: float = 0.01  # Trauma reduction per turn

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def add_member(self, agent_id: str):
        """Add an agent to the network"""
        if agent_id not in self.members:
            self.members.append(agent_id)

    def remove_member(self, agent_id: str):
        """Remove an agent from the network"""
        if agent_id in self.members:
            self.members.remove(agent_id)

    # ---------------------------------------------------------------------
    # Modifiers
    # ---------------------------------------------------------------------

    def get_resilience_modifier(self) -> float:
        """Return resilience bonus applied to relapse calculations"""
        return self.resilience_bonus

    def apply_passive_support(self, emotional_state: 'EmotionalState') -> None:  # type: ignore
        """Apply passive trauma recovery each turn."""
        emotional_state.apply_therapy_effect(self.passive_recovery)


# Registry for quick lookup in systems
_support_registry: Dict[str, SupportNetwork] = {}


def register_support_network(network: SupportNetwork):
    _support_registry[network.id] = network


def get_support_network(network_id: str) -> Optional[SupportNetwork]:
    return _support_registry.get(network_id)