"""
Unit tests for the reputation system

Tests the reputation loops, memory systems, and political simulation integration.
"""

import pytest

from datetime import date

from game.reputation_system import (
    FameType,
    MediaTone,
    EncounterTone,
    GovernmentResponse,
    MediaMention,
    PublicSentiment,
    PublicReputation,
    NPCMemory,
    PoliticalSimulationState,
    ReputationSystem,
)


class TestMediaMention:
    """Test media mention functionality"""

    def test_reputation_impact_calculation(self):
        """Test reputation impact calculation based on tone and circulation"""
        # Test sympathetic media with high circulation
        mention = MediaMention(
            headline="Hero of the People",
            source="Underground Press",
            tone=MediaTone.SYMPATHETIC,
            date=date.today(),
            impact_score=1.0,
            circulation=15000,
        )

        impact = mention.get_reputation_impact()
        assert impact > 0  # Should be positive for sympathetic coverage
        assert impact <= 0.15  # Should be capped by circulation factor

        # Test hostile media
        hostile_mention = MediaMention(
            headline="Dangerous Agitator",
            source="State News",
            tone=MediaTone.HOSTILE,
            date=date.today(),
            impact_score=1.0,
            circulation=5000,
        )

        hostile_impact = hostile_mention.get_reputation_impact()
        assert hostile_impact < 0  # Should be negative for hostile coverage


class TestPublicSentiment:
    """Test public sentiment functionality"""

    def test_dominant_sentiment(self):
        """Test dominant sentiment calculation"""
        sentiment = PublicSentiment(
            support_rating=0.4,
            fear_rating=0.3,
            confusion_rating=0.1,
            admiration_rating=0.1,
            hatred_rating=0.1,
        )

        dominant = sentiment.get_dominant_sentiment()
        assert dominant == "support"

    def test_sentiment_normalization(self):
        """Test sentiment normalization"""
        sentiment = PublicSentiment(
            support_rating=0.8,
            fear_rating=0.4,
            confusion_rating=0.2,
            admiration_rating=0.3,
            hatred_rating=0.1,
        )

        sentiment.normalize()
        total = (
            sentiment.support_rating
            + sentiment.fear_rating
            + sentiment.confusion_rating
            + sentiment.admiration_rating
            + sentiment.hatred_rating
        )

        assert abs(total - 1.0) < 0.001  # Should sum to 1.0


class TestPublicReputation:
    """Test public reputation functionality"""

    def test_reputation_creation(self):
        """Test basic reputation creation"""
        reputation = PublicReputation(agent_id="test_agent")

        assert reputation.agent_id == "test_agent"
        assert reputation.notoriety_score == 0.0
        assert reputation.fame_type == FameType.NONE
        assert len(reputation.reputation_tags) == 0

    def test_media_update(self):
        """Test reputation update from media coverage"""
        reputation = PublicReputation(agent_id="test_agent")

        mention = MediaMention(
            headline="Test Headline",
            source="Test Source",
            tone=MediaTone.SYMPATHETIC,
            date=date.today(),
            impact_score=1.0,
        )

        reputation.update_from_media(mention)

        assert reputation.notoriety_score > 0.0
        assert len(reputation.media_mentions) == 1
        assert reputation.public_sentiment.support_rating > 0.0

    def test_reputation_tags(self):
        """Test reputation tag system"""
        reputation = PublicReputation(agent_id="test_agent")

        reputation.add_reputation_tag("escaped_multiple")
        assert "escaped_multiple" in reputation.reputation_tags
        assert reputation.fame_type == FameType.MARTYR

        reputation.add_reputation_tag("inspired_riot")
        assert reputation.fame_type == FameType.AGITATOR  # Should override

    def test_search_modifier(self):
        """Test search frequency modifier calculation"""
        reputation = PublicReputation(agent_id="test_agent")
        reputation.notoriety_score = 0.8
        reputation.fame_type = FameType.AGITATOR
        reputation.region_visibility["test_region"] = 0.6

        modifier = reputation.get_search_modifier("test_region")
        assert modifier > 0.0
        assert modifier <= 1.0

    def test_political_pressure(self):
        """Test political pressure calculation"""
        reputation = PublicReputation(agent_id="test_agent")
        reputation.notoriety_score = 0.7
        reputation.public_sentiment.support_rating = 0.6

        pressure = reputation.get_political_pressure()
        assert pressure > 0.0
        assert pressure <= 1.0

    def test_reputation_decay(self):
        """Test reputation decay over time"""
        reputation = PublicReputation(agent_id="test_agent")
        reputation.notoriety_score = 0.8
        reputation.region_visibility["test_region"] = 0.6

        initial_notoriety = reputation.notoriety_score
        initial_visibility = reputation.region_visibility["test_region"]

        reputation.apply_decay(days_passed=5)

        assert reputation.notoriety_score < initial_notoriety
        assert reputation.region_visibility["test_region"] < initial_visibility

    def test_serialization(self):
        """Test reputation serialization and deserialization"""
        reputation = PublicReputation(agent_id="test_agent")
        reputation.notoriety_score = 0.5
        reputation.fame_type = FameType.MARTYR
        reputation.add_reputation_tag("test_tag")

        data = reputation.as_dict()
        reconstructed = PublicReputation.from_dict(data)

        assert reconstructed.agent_id == reputation.agent_id
        assert reconstructed.notoriety_score == reputation.notoriety_score
        assert reconstructed.fame_type == reputation.fame_type
        assert "test_tag" in reconstructed.reputation_tags


class TestNPCMemory:
    """Test NPC memory functionality"""

    def test_memory_creation(self):
        """Test basic memory creation"""
        memory = NPCMemory()

        assert memory.encounter_tone == EncounterTone.NEUTRAL
        assert len(memory.remembered_traits) == 0
        assert memory.encounter_count == 0

    def test_encounter_update(self):
        """Test memory update from encounter"""
        memory = NPCMemory()

        memory.update_from_encounter(
            location="checkpoint_alpha",
            tone=EncounterTone.HOSTILE,
            traits=["carried_contraband", "refused_compliance"],
            emotional_impact={"resentment": 0.5, "fear": 0.2},
        )

        assert memory.last_location == "checkpoint_alpha"
        assert memory.encounter_tone == EncounterTone.HOSTILE
        assert "carried_contraband" in memory.remembered_traits
        assert memory.emotional_reaction["resentment"] == 0.5
        assert memory.encounter_count == 1

    def test_search_rigor_modifier(self):
        """Test search rigor modifier calculation"""
        memory = NPCMemory()
        memory.dialogue_bias["search_rigor_bonus"] = 0.3
        memory.remembered_traits = ["escaped_search", "carried_contraband"]

        modifier = memory.get_search_rigor_modifier()
        assert modifier > 0.0
        assert modifier <= 1.0

    def test_dialogue_modifier(self):
        """Test dialogue politeness modifier"""
        memory = NPCMemory()
        memory.dialogue_bias["politeness_penalty"] = -0.3

        modifier = memory.get_dialogue_modifier()
        assert modifier == -0.3

    def test_memory_decay(self):
        """Test memory decay over time"""
        memory = NPCMemory()
        memory.emotional_reaction["resentment"] = 0.8
        memory.dialogue_bias["politeness_penalty"] = -0.4

        memory.apply_decay(days_passed=3)

        assert memory.emotional_reaction["resentment"] < 0.8
        assert memory.dialogue_bias["politeness_penalty"] > -0.4

    def test_serialization(self):
        """Test memory serialization and deserialization"""
        memory = NPCMemory()
        memory.update_from_encounter(
            location="test_location",
            tone=EncounterTone.DEFIANT,
            traits=["test_trait"],
            emotional_impact={"test_emotion": 0.5},
        )

        data = memory.as_dict()
        reconstructed = NPCMemory.from_dict(data)

        assert reconstructed.last_location == memory.last_location
        assert reconstructed.encounter_tone == memory.encounter_tone
        assert "test_trait" in reconstructed.remembered_traits


class TestPoliticalSimulationState:
    """Test political simulation functionality"""

    def test_government_response_update(self):
        """Test government response updates based on reputation"""
        political_state = PoliticalSimulationState()
        reputation = PublicReputation(agent_id="test_agent")
        reputation.notoriety_score = 0.8
        reputation.public_sentiment.support_rating = 0.6

        political_state.update_government_response(
            reputation, reputation.public_sentiment, recent_arrests=5
        )

        assert "response_mode" in political_state.government_policy
        assert len(political_state.policy_change_log) > 0

    def test_search_intensity(self):
        """Test search intensity calculation"""
        political_state = PoliticalSimulationState()
        political_state.heat_map["test_region"] = 0.7
        political_state.crackdown_zones = ["test_region"]
        political_state.government_policy[
            "response_mode"
        ] = GovernmentResponse.ANTI_INSURGENCY_ACT.value

        intensity = political_state.get_search_intensity("test_region")
        assert intensity > 0.0
        assert intensity <= 1.0

    def test_heat_map_update(self):
        """Test heat map updates"""
        political_state = PoliticalSimulationState()

        political_state.update_heat_map("test_region", 0.8)
        assert political_state.heat_map["test_region"] == 0.8
        assert "test_region" in political_state.crackdown_zones  # Should auto-add

    def test_serialization(self):
        """Test political state serialization"""
        political_state = PoliticalSimulationState()
        political_state.heat_map["test_region"] = 0.5
        political_state.crackdown_zones = ["test_region"]

        data = political_state.as_dict()
        reconstructed = PoliticalSimulationState.from_dict(data)

        assert reconstructed.heat_map["test_region"] == 0.5
        assert "test_region" in reconstructed.crackdown_zones


class TestReputationSystem:
    """Test the main reputation system integration"""

    def test_system_creation(self):
        """Test reputation system initialization"""
        system = ReputationSystem()

        assert len(system.public_reputations) == 0
        assert len(system.npc_memories) == 0
        assert isinstance(system.political_state, PoliticalSimulationState)

    def test_reputation_creation(self):
        """Test automatic reputation creation"""
        system = ReputationSystem()

        reputation = system.get_or_create_reputation("test_agent")
        assert reputation.agent_id == "test_agent"

        # Should return the same instance
        reputation2 = system.get_or_create_reputation("test_agent")
        assert reputation is reputation2

    def test_npc_memory_creation(self):
        """Test automatic NPC memory creation"""
        system = ReputationSystem()

        memory = system.get_or_create_npc_memory("npc_1", "agent_1")
        assert memory.encounter_tone == EncounterTone.NEUTRAL

        # Should return the same instance
        memory2 = system.get_or_create_npc_memory("npc_1", "agent_1")
        assert memory is memory2

    def test_encounter_recording(self):
        """Test encounter recording and reputation updates"""
        system = ReputationSystem()

        system.record_encounter(
            npc_id="officer_korrin",
            agent_id="agent_046",
            location="checkpoint_alpha",
            tone=EncounterTone.DEFIANT,
            traits=["refused_compliance"],
            emotional_impact={"resentment": 0.6},
        )

        # Check NPC memory was updated
        memory = system.get_or_create_npc_memory("officer_korrin", "agent_046")
        assert "refused_compliance" in memory.remembered_traits
        assert memory.emotional_reaction["resentment"] == 0.6

        # Check reputation was updated
        reputation = system.get_or_create_reputation("agent_046")
        assert "checkpoint_alpha" in reputation.region_visibility
        assert reputation.region_visibility["checkpoint_alpha"] > 0.0

    def test_media_event_generation(self):
        """Test media event generation and political updates"""
        system = ReputationSystem()

        system.generate_media_event(
            agent_id="agent_046",
            headline="Mysterious Figure Evades Capture",
            source="State News",
            tone=MediaTone.FEARFUL,
            impact_score=1.0,
        )

        # Check reputation was updated
        reputation = system.get_or_create_reputation("agent_046")
        assert len(reputation.media_mentions) == 1
        assert (
            reputation.media_mentions[0].headline == "Mysterious Figure Evades Capture"
        )
        assert reputation.notoriety_score > 0.0

    def test_search_probability_calculation(self):
        """Test search probability calculation"""
        system = ReputationSystem()

        # Set up reputation and memory
        reputation = system.get_or_create_reputation("agent_046")
        reputation.notoriety_score = 0.7
        reputation.fame_type = FameType.AGITATOR
        reputation.region_visibility["sector_alpha"] = 0.8

        memory = system.get_or_create_npc_memory("officer_korrin", "agent_046")
        memory.remembered_traits = ["escaped_search"]

        # Set up political state
        system.political_state.heat_map["sector_alpha"] = 0.6
        system.political_state.government_policy[
            "response_mode"
        ] = GovernmentResponse.ANTI_INSURGENCY_ACT.value

        probability = system.calculate_search_probability(
            agent_id="agent_046", region="sector_alpha", npc_id="officer_korrin"
        )

        assert probability > 0.0
        assert probability <= 1.0

    def test_dialogue_modifier(self):
        """Test dialogue modifier retrieval"""
        system = ReputationSystem()

        memory = system.get_or_create_npc_memory("npc_1", "agent_1")
        memory.dialogue_bias["politeness_penalty"] = -0.3

        modifier = system.get_dialogue_modifier("npc_1", "agent_1")
        assert modifier == -0.3

    def test_daily_decay(self):
        """Test daily decay application"""
        system = ReputationSystem()

        # Set up reputation and memory with high values
        reputation = system.get_or_create_reputation("agent_1")
        reputation.notoriety_score = 0.8
        reputation.region_visibility["test_region"] = 0.6

        memory = system.get_or_create_npc_memory("npc_1", "agent_1")
        memory.emotional_reaction["resentment"] = 0.8
        memory.dialogue_bias["politeness_penalty"] = -0.4

        initial_notoriety = reputation.notoriety_score
        initial_visibility = reputation.region_visibility["test_region"]
        initial_resentment = memory.emotional_reaction["resentment"]

        system.apply_daily_decay()

        assert reputation.notoriety_score < initial_notoriety
        assert reputation.region_visibility["test_region"] < initial_visibility
        assert memory.emotional_reaction["resentment"] < initial_resentment

    def test_system_serialization(self):
        """Test full system serialization and deserialization"""
        system = ReputationSystem()

        # Add some data
        system.record_encounter(
            npc_id="npc_1",
            agent_id="agent_1",
            location="test_location",
            tone=EncounterTone.HOSTILE,
            traits=["test_trait"],
            emotional_impact={"test": 0.5},
        )

        system.generate_media_event(
            agent_id="agent_1",
            headline="Test",
            source="Test",
            tone=MediaTone.NEUTRAL,
            impact_score=1.0,
        )

        # Serialize and deserialize
        data = system.serialize()
        reconstructed = ReputationSystem.deserialize(data)

        # Check that data was preserved
        assert "agent_1" in reconstructed.public_reputations
        assert "npc_1" in reconstructed.npc_memories
        assert "agent_1" in reconstructed.npc_memories["npc_1"]


class TestReputationLoops:
    """Test the reputation feedback loops"""

    def test_reputation_to_search_loop(self):
        """Test how reputation affects search probability"""
        system = ReputationSystem()

        # High notoriety should increase search probability
        reputation = system.get_or_create_reputation("agent_1")
        reputation.notoriety_score = 0.9
        reputation.fame_type = FameType.AGITATOR

        high_prob = system.calculate_search_probability("agent_1", "test_region")

        # Low notoriety should decrease search probability
        reputation.notoriety_score = 0.1
        reputation.fame_type = FameType.NONE

        low_prob = system.calculate_search_probability("agent_1", "test_region")

        assert high_prob > low_prob

    def test_npc_memory_to_dialogue_loop(self):
        """Test how NPC memory affects dialogue"""
        system = ReputationSystem()

        # Hostile encounter should affect dialogue
        system.record_encounter(
            npc_id="npc_1",
            agent_id="agent_1",
            location="test",
            tone=EncounterTone.HOSTILE,
            traits=[],
            emotional_impact={},
        )

        modifier = system.get_dialogue_modifier("npc_1", "agent_1")
        assert modifier < 0  # Should be negative for hostile encounters

    def test_media_to_political_loop(self):
        """Test how media events affect political pressure"""
        system = ReputationSystem()

        # Generate sympathetic media coverage
        system.generate_media_event(
            agent_id="agent_1",
            headline="Hero of the People",
            source="Underground Press",
            tone=MediaTone.SYMPATHETIC,
            impact_score=1.0,
        )

        reputation = system.get_or_create_reputation("agent_1")
        pressure = reputation.get_political_pressure()

        assert pressure > 0.0  # Should generate some political pressure


if __name__ == "__main__":
    pytest.main([__file__])
