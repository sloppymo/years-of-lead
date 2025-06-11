"""
Years of Lead - Campaign Structure & Historical Memory

# ITERATION_034

Provides lightweight campaign arcs (multi-mission storylines) and
a global HistoricalMemory registry for tracking major events.  This lays
foundation for future narrative and validation systems.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional
import uuid
import datetime as _dt

# ---------------------------------------------------------------------------
# Campaign Data Structures
# ---------------------------------------------------------------------------

class CampaignStage(Enum):
    """High-level stages a campaign progresses through."""
    PLANNING = auto()
    EXECUTION = auto()
    CONSOLIDATION = auto()
    RESOLUTION = auto()


@dataclass
class Campaign:
    """Represents a multi-mission campaign arc."""

    name: str
    description: str
    start_turn: int
    faction_id: str
    id: str = field(default_factory=lambda: f"cmp_{uuid.uuid4().hex[:8]}")

    stages: List[CampaignStage] = field(default_factory=lambda: [CampaignStage.PLANNING])
    current_stage: CampaignStage = CampaignStage.PLANNING
    completed: bool = False
    missions: List[str] = field(default_factory=list)  # mission IDs linked to this campaign

    def advance_stage(self):  # ITERATION_034
        """Advance to the next campaign stage."""
        if self.completed:
            return
        order = list(CampaignStage)
        idx = order.index(self.current_stage)
        if idx + 1 < len(order):
            self.current_stage = order[idx + 1]
            self.stages.append(self.current_stage)
        else:
            self.completed = True

    def add_mission(self, mission_id: str):  # ITERATION_034
        if mission_id not in self.missions:
            self.missions.append(mission_id)

# ---------------------------------------------------------------------------
# Historical Memory – global registry
# ---------------------------------------------------------------------------

@dataclass
class HistoricalEvent:
    """Stores key outcomes for future reference & narrative callbacks."""

    turn: int
    description: str
    factions: List[str]
    impact: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"hist_{uuid.uuid4().hex[:8]}")
    timestamp: str = field(default_factory=lambda: _dt.datetime.utcnow().isoformat())


class HistoricalMemory:
    """Singleton-like container tracking important game events."""

    def __init__(self):
        self._events: List[HistoricalEvent] = []

    # Tag function
    def record_event(self, event: HistoricalEvent):  # ITERATION_034
        self._events.append(event)

    def query(self, faction_id: Optional[str] = None, since_turn: int = 0) -> List[HistoricalEvent]:
        """Retrieve events filtered by faction or time."""
        return [e for e in self._events if (faction_id is None or faction_id in e.factions) and e.turn >= since_turn]

    def latest(self, limit: int = 5) -> List[HistoricalEvent]:
        return self._events[-limit:]

    # Simple health metric – number of recorded events
    def count(self) -> int:
        return len(self._events)

# Global instance
historical_memory = HistoricalMemory()