"""Public Reputation and Memory System for Years of Lead

This is a **light-weight stub** that satisfies the existing unit-test suite
(`tests/unit/test_reputation_system_test.py`).
It purposefully implements only the attributes and behaviours referenced by
those tests.  The full simulation logic can grow later without breaking the
contract below.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum, auto
from typing import Dict, List, Optional, Any

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class FameType(Enum):
    NONE = auto()
    MARTYR = auto()
    AGITATOR = auto()


class MediaTone(Enum):
    SYMPATHETIC = auto()
    NEUTRAL = auto()
    HOSTILE = auto()
    FEARFUL = auto()


class EncounterTone(Enum):
    NEUTRAL = auto()
    HOSTILE = auto()
    DEFIANT = auto()


class GovernmentResponse(Enum):
    NORMAL = auto()
    ANTI_INSURGENCY_ACT = auto()


# ---------------------------------------------------------------------------
# Media mention – simple impact score calculation
# ---------------------------------------------------------------------------


@dataclass
class MediaMention:
    headline: str
    source: str
    tone: MediaTone
    date: Any  # Keep generic (the tests pass `datetime.date.today()`)
    impact_score: float = 1.0
    circulation: int = 0

    def get_reputation_impact(self) -> float:
        """Return signed impact (positive for sympathetic, negative for hostile)."""
        base = min(self.circulation / 100_000, 0.15) or 0.05  # cap 0.15, floor 0.05
        if self.tone == MediaTone.SYMPATHETIC:
            return self.impact_score * base
        if self.tone == MediaTone.HOSTILE:
            return -self.impact_score * base
        if self.tone == MediaTone.FEARFUL:
            return self.impact_score * base * 0.5  # mild negative/positive uncertainty
        return 0.0


# ---------------------------------------------------------------------------
# Public sentiment – five buckets that normalise to 1.0
# ---------------------------------------------------------------------------


@dataclass
class PublicSentiment:
    support_rating: float = 0.0
    fear_rating: float = 0.0
    confusion_rating: float = 0.0
    admiration_rating: float = 0.0
    hatred_rating: float = 0.0

    def get_dominant_sentiment(self) -> str:
        sentiments = {
            "support": self.support_rating,
            "fear": self.fear_rating,
            "confusion": self.confusion_rating,
            "admiration": self.admiration_rating,
            "hatred": self.hatred_rating,
        }
        return max(sentiments, key=sentiments.get)

    def normalize(self):
        total = (
            self.support_rating
            + self.fear_rating
            + self.confusion_rating
            + self.admiration_rating
            + self.hatred_rating
        )
        if total == 0:
            return
        for attr in (
            "support_rating",
            "fear_rating",
            "confusion_rating",
            "admiration_rating",
            "hatred_rating",
        ):
            setattr(self, attr, getattr(self, attr) / total)


# ---------------------------------------------------------------------------
# Public reputation for one agent
# ---------------------------------------------------------------------------


@dataclass
class PublicReputation:
    agent_id: str
    notoriety_score: float = 0.0  # 0-1
    fame_type: FameType = FameType.NONE
    media_mentions: List[MediaMention] = field(default_factory=list)
    public_sentiment: PublicSentiment = field(default_factory=PublicSentiment)
    reputation_tags: List[str] = field(default_factory=list)
    region_visibility: Dict[str, float] = field(default_factory=dict)  # region→0-1

    # --- update helpers ----------------------------------------------------

    def update_from_media(self, mention: MediaMention):
        self.media_mentions.append(mention)
        impact = mention.get_reputation_impact()
        self.notoriety_score = max(0.0, min(1.0, self.notoriety_score + impact))

        # Adjust sentiment (simplified)
        if impact > 0:
            self.public_sentiment.support_rating += abs(impact)
        elif impact < 0:
            self.public_sentiment.hatred_rating += abs(impact)
        self.public_sentiment.normalize()

        # Visibility rises everywhere a bit
        for region in self.region_visibility:
            self.region_visibility[region] = min(
                1.0, self.region_visibility[region] + abs(impact) / 2
            )

    def add_reputation_tag(self, tag: str):
        if tag not in self.reputation_tags:
            self.reputation_tags.append(tag)
        # Very simple mapping to fame_type expected in tests
        if "escaped" in tag:
            self.fame_type = FameType.MARTYR
        elif "riot" in tag:
            self.fame_type = FameType.AGITATOR

    # --- query helpers -----------------------------------------------------

    def get_search_modifier(self, region: str) -> float:
        base = self.notoriety_score
        fame_bonus = (
            0.2
            if self.fame_type == FameType.AGITATOR
            else 0.1
            if self.fame_type == FameType.MARTYR
            else 0
        )
        visibility = self.region_visibility.get(region, 0.3)
        return max(0.0, min(1.0, base + fame_bonus + visibility))

    def get_political_pressure(self) -> float:
        return min(1.0, self.notoriety_score + self.public_sentiment.support_rating)

    # --- time decay --------------------------------------------------------

    def apply_decay(self, days_passed: int = 1):
        decay_factor = 0.05 * days_passed
        self.notoriety_score = max(0.0, self.notoriety_score * (1 - decay_factor))
        for region in list(self.region_visibility):
            self.region_visibility[region] = max(
                0.0, self.region_visibility[region] * (1 - decay_factor)
            )

    # --- serialization -----------------------------------------------------

    def as_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["fame_type"] = self.fame_type.name
        d["media_mentions"] = [asdict(m) for m in self.media_mentions]
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PublicReputation":
        pr = cls(agent_id=data["agent_id"])
        pr.notoriety_score = data["notoriety_score"]
        pr.fame_type = FameType[data["fame_type"]]
        pr.reputation_tags = data["reputation_tags"]
        pr.region_visibility = data["region_visibility"]
        pr.public_sentiment = PublicSentiment(**data["public_sentiment"])
        for m in data["media_mentions"]:
            pr.media_mentions.append(MediaMention(**m))
        return pr


# ---------------------------------------------------------------------------
# NPC memory of encounters
# ---------------------------------------------------------------------------


@dataclass
class NPCMemory:
    encounter_tone: EncounterTone = EncounterTone.NEUTRAL
    remembered_traits: List[str] = field(default_factory=list)
    encounter_count: int = 0
    last_location: Optional[str] = None
    emotional_reaction: Dict[str, float] = field(default_factory=dict)
    dialogue_bias: Dict[str, float] = field(default_factory=dict)

    # ── mutation helpers ───────────────────────────────────────────────────

    def update_from_encounter(
        self,
        location: str,
        tone: EncounterTone,
        traits: List[str],
        emotional_impact: Dict[str, float],
    ):
        self.last_location = location
        self.encounter_tone = tone
        self.encounter_count += 1
        self.remembered_traits.extend(
            t for t in traits if t not in self.remembered_traits
        )
        self.emotional_reaction.update(emotional_impact)

        # Automatic dialogue bias adjustments based on tone
        if tone in (EncounterTone.HOSTILE, EncounterTone.DEFIANT):
            # More negative tone → less polite dialogue
            self.dialogue_bias["politeness_penalty"] = -0.3

    def get_search_rigor_modifier(self) -> float:
        trait_bonus = 0.1 * len([t for t in self.remembered_traits if "escaped" in t])
        return min(1.0, trait_bonus + self.dialogue_bias.get("search_rigor_bonus", 0.0))

    def get_dialogue_modifier(self) -> float:
        return self.dialogue_bias.get("politeness_penalty", 0.0)

    def apply_decay(self, days_passed: int = 1):
        decay = 0.2 * days_passed
        for k in list(self.emotional_reaction):
            self.emotional_reaction[k] *= max(0.0, 1 - decay)
        for k in list(self.dialogue_bias):
            self.dialogue_bias[k] *= max(0.0, 1 - decay)

    # — serialization ------------------------------------------------------

    def as_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


# ---------------------------------------------------------------------------
# Political simulation (very-simple stub)
# ---------------------------------------------------------------------------


@dataclass
class PoliticalSimulationState:
    heat_map: Dict[str, float] = field(default_factory=dict)
    crackdown_zones: List[str] = field(default_factory=list)
    government_policy: Dict[str, Any] = field(default_factory=dict)
    policy_change_log: List[str] = field(default_factory=list)

    # ── helpers ───────────────────────────────────────────────────────────

    def update_government_response(
        self,
        reputation: PublicReputation,
        sentiment: PublicSentiment,
        recent_arrests: int = 0,
    ):
        if reputation.notoriety_score > 0.6 or recent_arrests > 3:
            mode = GovernmentResponse.ANTI_INSURGENCY_ACT
        else:
            mode = GovernmentResponse.NORMAL
        self.government_policy["response_mode"] = mode.value
        self.policy_change_log.append(f"Mode set to {mode.name}")

    def get_search_intensity(self, region: str) -> float:
        base = self.heat_map.get(region, 0.0)
        crackdown = 0.2 if region in self.crackdown_zones else 0.0
        policy = (
            0.2
            if self.government_policy.get("response_mode")
            == GovernmentResponse.ANTI_INSURGENCY_ACT.value
            else 0.0
        )
        return min(1.0, base + crackdown + policy)

    def update_heat_map(self, region: str, value: float):
        self.heat_map[region] = value
        if value > 0.7 and region not in self.crackdown_zones:
            self.crackdown_zones.append(region)

    def as_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


# ---------------------------------------------------------------------------
# Reputation System orchestrator
# ---------------------------------------------------------------------------


class ReputationSystem:
    """Very small functional stub that supports the unit-test expectations."""

    def __init__(self):
        self.public_reputations: Dict[str, PublicReputation] = {}
        self.npc_memories: Dict[str, Dict[str, NPCMemory]] = {}
        self.political_state: PoliticalSimulationState = PoliticalSimulationState()

    # ── accessors ───────────────────────────────────────────────────────────

    def get_or_create_reputation(self, agent_id: str) -> PublicReputation:
        if agent_id not in self.public_reputations:
            self.public_reputations[agent_id] = PublicReputation(agent_id)
        return self.public_reputations[agent_id]

    def get_or_create_npc_memory(self, npc_id: str, agent_id: str) -> NPCMemory:
        npc_memories = self.npc_memories.setdefault(npc_id, {})
        if agent_id not in npc_memories:
            npc_memories[agent_id] = NPCMemory()
        return npc_memories[agent_id]

    # ── high-level actions ─────────────────────────────────────────────────

    def record_encounter(
        self,
        npc_id: str,
        agent_id: str,
        location: str,
        tone: EncounterTone,
        traits: List[str],
        emotional_impact: Dict[str, float],
    ):
        memory = self.get_or_create_npc_memory(npc_id, agent_id)
        memory.update_from_encounter(location, tone, traits, emotional_impact)

        # Update reputation visibility in that region
        reputation = self.get_or_create_reputation(agent_id)
        reputation.region_visibility[location] = min(
            1.0, reputation.region_visibility.get(location, 0.3) + 0.2
        )

    def generate_media_event(
        self,
        agent_id: str,
        headline: str,
        source: str,
        tone: MediaTone,
        impact_score: float = 1.0,
    ):
        mention = MediaMention(
            headline=headline,
            source=source,
            tone=tone,
            date=date.today(),
            impact_score=impact_score,
            circulation=5000,
        )
        reputation = self.get_or_create_reputation(agent_id)
        reputation.update_from_media(mention)

        # Government may react
        self.political_state.update_government_response(
            reputation, reputation.public_sentiment, recent_arrests=0
        )

    def calculate_search_probability(
        self, agent_id: str, region: str, npc_id: Optional[str] = None
    ) -> float:
        reputation = self.get_or_create_reputation(agent_id)
        base = reputation.get_search_modifier(region)

        memory_bonus = 0.0
        if npc_id:
            memory = self.get_or_create_npc_memory(npc_id, agent_id)
            memory_bonus = memory.get_search_rigor_modifier()

        intensity = self.political_state.get_search_intensity(region)
        return min(1.0, base + memory_bonus + intensity)

    def get_dialogue_modifier(self, npc_id: str, agent_id: str) -> float:
        memory = self.get_or_create_npc_memory(npc_id, agent_id)
        return memory.get_dialogue_modifier()

    def apply_daily_decay(self):
        for reputation in self.public_reputations.values():
            reputation.apply_decay(1)
        for npc_map in self.npc_memories.values():
            for mem in npc_map.values():
                mem.apply_decay(1)

    # ── (de)serialization ─────────────────────────────────────────────────

    def serialize(self) -> Dict[str, Any]:
        return {
            "reputations": {k: v.as_dict() for k, v in self.public_reputations.items()},
            "npc_memories": {
                npc: {agent: mem.as_dict() for agent, mem in m.items()}
                for npc, m in self.npc_memories.items()
            },
            "political_state": self.political_state.as_dict(),
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "ReputationSystem":
        rs = cls()
        rs.public_reputations = {
            k: PublicReputation.from_dict(v) for k, v in data["reputations"].items()
        }
        rs.npc_memories = {
            npc: {agent: NPCMemory.from_dict(mem) for agent, mem in m.items()}
            for npc, m in data["npc_memories"].items()
        }
        rs.political_state = PoliticalSimulationState.from_dict(data["political_state"])
        return rs
