"""
Test suite for the Years of Lead relationship system
Tests relationship tracking, loyalty, betrayal, and trauma integration
"""

import pytest
from datetime import datetime, timedelta
from src.game.relationship_system import (
    RelationshipType, RelationshipEvent, RelationshipMetrics,
    RelationshipHistory, Relationship, RelationshipManager,
    create_initial_cell_relationships
)
from src.game.emotional_state import EmotionalState, TraumaTriggerType, TherapyType
from src.game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait


class TestRelationshipMetrics:
    """Test relationship metrics and calculations"""
    
    def test_metrics_initialization(self):
        """Test that metrics initialize within valid ranges"""
        metrics = RelationshipMetrics()
        
        assert -1.0 <= metrics.admiration <= 1.0
        assert 0.0 <= metrics.fear <= 1.0
        assert -1.0 <= metrics.trust <= 1.0
        assert 0.0 <= metrics.ideological_proximity <= 1.0
        assert 0.0 <= metrics.loyalty <= 1.0
        assert 0.0 <= metrics.betrayal_potential <= 1.0
        assert -1.0 <= metrics.emotional_bond <= 1.0
        assert metrics.shared_experiences == 0
    
    def test_metrics_clamping(self):
        """Test that values are properly clamped"""
        metrics = RelationshipMetrics(
            admiration=2.0,
            fear=-0.5,
            trust=1.5,
            betrayal_potential=2.0
        )
        
        assert metrics.admiration == 1.0
        assert metrics.fear == 0.0
        assert metrics.trust == 1.0
        assert metrics.betrayal_potential == 1.0
    
    def test_relationship_strength_calculation(self):
        """Test overall relationship strength calculation"""
        # Strong positive relationship
        positive_metrics = RelationshipMetrics(
            admiration=0.8,
            trust=0.9,
            loyalty=0.8,
            emotional_bond=0.7,
            fear=0.1,
            betrayal_potential=0.1,
            ideological_proximity=0.9
        )
        strength = positive_metrics.calculate_overall_relationship_strength()
        assert strength > 0.5
        
        # Negative relationship
        negative_metrics = RelationshipMetrics(
            admiration=-0.5,
            trust=-0.8,
            loyalty=0.2,
            emotional_bond=-0.6,
            fear=0.8,
            betrayal_potential=0.7,
            ideological_proximity=0.2
        )
        strength = negative_metrics.calculate_overall_relationship_strength()
        assert strength < -0.3
    
    def test_betrayal_potential_update(self):
        """Test betrayal potential calculation"""
        metrics = RelationshipMetrics(
            trust=0.3,
            loyalty=0.4,
            fear=0.7,
            ideological_proximity=0.3,
            emotional_bond=-0.2
        )
        
        # High trauma and external pressure should increase betrayal potential
        potential = metrics.update_betrayal_potential(
            character_trauma=0.8,
            external_pressure=0.6
        )
        
        assert potential > 0.5
        assert metrics.last_betrayal_check is not None


class TestRelationshipHistory:
    """Test relationship history tracking"""
    
    def test_event_tracking(self):
        """Test that events are properly recorded"""
        history = RelationshipHistory()
        
        # Add various events
        history.add_event(RelationshipEvent.MISSION_SUCCESS)
        history.add_event(RelationshipEvent.MISSION_FAILURE)
        history.add_event(RelationshipEvent.SAVED_LIFE)
        history.add_event(RelationshipEvent.ABANDONED)
        
        assert len(history.events) == 4
        assert history.shared_successes == 1
        assert history.shared_failures == 1
        assert history.times_saved_by == 1
        assert history.times_abandoned_by == 1
    
    def test_betrayal_history_detection(self):
        """Test detection of betrayal history"""
        history = RelationshipHistory()
        
        # No betrayal initially
        assert not history.has_betrayal_history()
        
        # Add betrayal event
        history.add_event(RelationshipEvent.BETRAYAL)
        assert history.has_betrayal_history()
        
        # Trust broken also counts
        history2 = RelationshipHistory()
        history2.add_event(RelationshipEvent.TRUST_BROKEN)
        assert history2.has_betrayal_history()
    
    def test_metric_tracking(self):
        """Test metric trajectory tracking"""
        history = RelationshipHistory()
        
        history.track_metric("trust", 0.5)
        history.track_metric("trust", 0.6)
        history.track_metric("loyalty", 0.7)
        
        assert len(history.trust_trajectory) == 2
        assert len(history.loyalty_trajectory) == 1
        assert history.trust_trajectory[-1][1] == 0.6


class TestRelationship:
    """Test individual relationship mechanics"""
    
    def test_relationship_creation(self):
        """Test basic relationship creation"""
        metrics = RelationshipMetrics(trust=0.5, loyalty=0.6)
        history = RelationshipHistory()
        
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=metrics,
            history=history
        )
        
        assert rel.character_id == "char1"
        assert rel.target_id == "char2"
        assert rel.relationship_type == RelationshipType.COMRADE
        assert rel.metrics.trust == 0.5
    
    def test_mission_success_event(self):
        """Test mission success impact on relationship"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(trust=0.5),
            history=RelationshipHistory()
        )
        
        initial_trust = rel.metrics.trust
        changes = rel.apply_event(RelationshipEvent.MISSION_SUCCESS, intensity=1.0)
        
        assert rel.metrics.trust > initial_trust
        assert "trust" in changes
        assert rel.metrics.shared_experiences == 1
        assert rel.history.shared_successes == 1
    
    def test_betrayal_event(self):
        """Test betrayal impact on relationship"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(
                trust=0.8,
                loyalty=0.7,
                admiration=0.6,
                emotional_bond=0.5,
                fear=0.1
            ),
            history=RelationshipHistory()
        )
        
        # Apply betrayal
        changes = rel.apply_event(RelationshipEvent.BETRAYAL, intensity=1.0)
        
        # Check severe negative impacts
        assert rel.metrics.trust < 0.0  # Should be severely negative
        assert rel.metrics.loyalty < 0.2
        assert rel.metrics.fear > 0.3
        assert rel.metrics.betrayal_potential > 0.4
        assert rel.history.has_betrayal_history()
    
    def test_saved_life_event(self):
        """Test life-saving event impact"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(fear=0.5),
            history=RelationshipHistory()
        )
        
        initial_fear = rel.metrics.fear
        changes = rel.apply_event(RelationshipEvent.SAVED_LIFE)
        
        assert rel.metrics.trust > 0.3
        assert rel.metrics.admiration > 0.3
        assert rel.metrics.loyalty > 0.3
        assert rel.metrics.fear < initial_fear  # Fear should reduce
        assert rel.history.times_saved_by == 1
    
    def test_romantic_advance(self):
        """Test romantic advance handling"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.FRIEND,
            metrics=RelationshipMetrics(),
            history=RelationshipHistory()
        )
        
        # Accepted advance
        changes = rel.apply_event(
            RelationshipEvent.ROMANTIC_ADVANCE,
            details={"accepted": True}
        )
        
        assert rel.relationship_type == RelationshipType.ROMANTIC
        assert rel.metrics.emotional_bond > 0.3
        assert rel.metrics.trust > 0.1
    
    def test_time_decay(self):
        """Test relationship decay over time"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(
                admiration=0.8,
                emotional_bond=0.7,
                fear=0.6,
                betrayal_potential=0.5
            ),
            history=RelationshipHistory()
        )
        
        initial_admiration = rel.metrics.admiration
        initial_fear = rel.metrics.fear
        initial_betrayal = rel.metrics.betrayal_potential
        
        # Apply time decay
        rel.apply_time_decay(days_passed=5.0)
        
        # Relationships drift toward neutral
        assert rel.metrics.admiration < initial_admiration
        assert rel.metrics.fear < initial_fear
        # Betrayal potential decreases without negative events
        assert rel.metrics.betrayal_potential < initial_betrayal
    
    def test_betrayal_check(self):
        """Test betrayal probability calculation"""
        # High loyalty should prevent betrayal
        loyal_rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(loyalty=0.9, trust=0.8),
            history=RelationshipHistory()
        )
        
        _, probability, _ = loyal_rel.check_for_betrayal()
        assert probability < 0.2
        
        # High fear and low trust increases betrayal
        fearful_rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(
                loyalty=0.3,
                trust=-0.5,
                fear=0.8,
                ideological_proximity=0.2
            ),
            history=RelationshipHistory()
        )
        
        _, probability, _ = fearful_rel.check_for_betrayal(external_pressure=0.7)
        assert probability > 0.5
    
    def test_relationship_summary_generation(self):
        """Test narrative summary generation"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.LEADER,
            metrics=RelationshipMetrics(
                trust=0.8,
                loyalty=0.9,
                admiration=0.7,
                emotional_bond=0.6
            ),
            history=RelationshipHistory()
        )
        
        # Add some history
        rel.history.times_saved_by = 2
        
        summary = rel.generate_relationship_summary()
        assert "very strong" in summary.lower() or "positive" in summary.lower()
        assert "trust" in summary.lower()
        assert "saved" in summary
    
    def test_serialization(self):
        """Test relationship serialization"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(trust=0.5),
            history=RelationshipHistory()
        )
        
        # Add some events
        rel.apply_event(RelationshipEvent.MISSION_SUCCESS)
        
        # Serialize
        data = rel.serialize()
        
        assert data["character_id"] == "char1"
        assert data["target_id"] == "char2"
        assert data["relationship_type"] == "comrade"
        assert data["metrics"]["trust"] == 0.5
        assert len(data["history"]["events"]) > 0


class TestRelationshipManager:
    """Test relationship management system"""
    
    def test_manager_creation(self):
        """Test manager initialization"""
        manager = RelationshipManager()
        assert isinstance(manager.relationships, dict)
    
    def test_create_relationship(self):
        """Test relationship creation through manager"""
        manager = RelationshipManager()
        
        rel = manager.create_relationship(
            "char1", "char2",
            RelationshipType.COMRADE
        )
        
        assert rel is not None
        assert manager.get_relationship("char1", "char2") == rel
        assert manager.get_relationship("char2", "char1") is None  # Not bidirectional by default
    
    def test_group_event_application(self):
        """Test applying events to group relationships"""
        manager = RelationshipManager()
        participants = ["char1", "char2", "char3"]
        
        # Create relationships
        for i, char_id in enumerate(participants):
            for j, target_id in enumerate(participants):
                if i != j:
                    manager.create_relationship(
                        char_id, target_id,
                        RelationshipType.COMRADE
                    )
        
        # Apply group event
        manager.apply_group_event(
            participants,
            RelationshipEvent.MISSION_SUCCESS,
            intensity=0.8
        )
        
        # Check all relationships were affected
        for char_id in participants:
            relationships = manager.get_all_relationships(char_id)
            for rel in relationships.values():
                assert rel.history.shared_successes == 1
    
    def test_group_cohesion_analysis(self):
        """Test group cohesion calculation"""
        manager = RelationshipManager()
        group = ["char1", "char2", "char3"]
        
        # Create strong relationships
        for i, char_id in enumerate(group):
            for j, target_id in enumerate(group):
                if i != j:
                    manager.create_relationship(
                        char_id, target_id,
                        RelationshipType.COMRADE,
                        RelationshipMetrics(
                            trust=0.7,
                            loyalty=0.8,
                            admiration=0.6,
                            emotional_bond=0.5
                        )
                    )
        
        cohesion = manager.check_group_cohesion(group)
        
        assert cohesion["average_strength"] > 0.3
        assert cohesion["cohesion_rating"] in ["Excellent", "Good"]
        assert len(cohesion["high_betrayal_risks"]) == 0
    
    def test_initial_cell_creation(self):
        """Test initial cell relationship creation"""
        members = ["leader", "member1", "member2", "member3"]
        
        manager = create_initial_cell_relationships(
            members,
            leader_id="leader"
        )
        
        # Check leader relationships
        leader_rels = manager.get_all_relationships("leader")
        for rel in leader_rels.values():
            assert rel.relationship_type == RelationshipType.LEADER
        
        # Check member relationships to leader
        member_rels = manager.get_all_relationships("member1")
        leader_rel = member_rels.get("leader")
        assert leader_rel is not None
        assert leader_rel.relationship_type == RelationshipType.SUBORDINATE
        
        # Check relationships between members
        member_to_member = member_rels.get("member2")
        assert member_to_member is not None
        assert member_to_member.relationship_type == RelationshipType.COMRADE


class TestIntegrationWithEmotionalState:
    """Test integration between relationships and emotional states"""
    
    def test_trauma_affects_betrayal(self):
        """Test that trauma increases betrayal potential"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(trust=0.5, loyalty=0.5),
            history=RelationshipHistory()
        )
        
        # Check betrayal with low trauma
        _, low_trauma_prob, _ = rel.check_for_betrayal(character_trauma=0.2)
        
        # Check betrayal with high trauma
        _, high_trauma_prob, _ = rel.check_for_betrayal(character_trauma=0.8)
        
        assert high_trauma_prob > low_trauma_prob
    
    def test_shared_trauma_event(self):
        """Test shared trauma strengthens bonds"""
        rel = Relationship(
            character_id="char1",
            target_id="char2",
            relationship_type=RelationshipType.COMRADE,
            metrics=RelationshipMetrics(),
            history=RelationshipHistory()
        )
        
        initial_bond = rel.metrics.emotional_bond
        rel.apply_event(RelationshipEvent.SHARED_TRAUMA)
        
        assert rel.metrics.emotional_bond > initial_bond
        assert rel.metrics.trust > 0
    
    def test_therapy_recommendation_with_relationships(self):
        """Test that relationship issues can indicate need for therapy"""
        # Create character with relationship trauma
        creator = CharacterCreator()
        char = creator.create_character(
            name="Test Agent",
            background_type=BackgroundType.MILITARY,
            primary_trait=PersonalityTrait.LOYAL,
            secondary_trait=PersonalityTrait.CAUTIOUS,
            has_trauma=True
        )
        
        # Apply betrayal trauma
        char.emotional_state.apply_trauma(
            trauma_intensity=0.8,
            event_type="betrayal",
            triggers=[TraumaTriggerType.BETRAYAL]
        )
        
        needs_therapy, reasons = char.needs_therapy()
        assert needs_therapy
    
    def test_relationship_affects_character_effectiveness(self):
        """Test that poor relationships affect character performance"""
        creator = CharacterCreator()
        char = creator.create_character(
            name="Test Agent",
            background_type=BackgroundType.ACTIVIST,
            primary_trait=PersonalityTrait.IDEALISTIC,
            secondary_trait=PersonalityTrait.COMPASSIONATE
        )
        
        # Create relationship manager
        manager = RelationshipManager()
        char.relationships_manager = manager
        
        # Add a very negative relationship
        manager.create_relationship(
            char.id, "enemy",
            RelationshipType.ENEMY,
            RelationshipMetrics(
                trust=-0.9,
                fear=0.8,
                admiration=-0.7,
                betrayal_potential=0.9
            )
        )
        
        # High stress from bad relationships should affect stability
        stress = char.get_stress_level()
        assert stress > 0  # Should have some baseline stress


@pytest.mark.integration
class TestFullScenarios:
    """Test complete scenarios involving relationships"""
    
    def test_betrayal_cascade(self):
        """Test how betrayal affects a whole cell"""
        # Create a cell
        members = ["leader", "loyal", "wavering", "traitor"]
        manager = create_initial_cell_relationships(members, "leader")
        
        # Make one member more likely to betray
        traitor_rels = manager.get_all_relationships("traitor")
        for rel in traitor_rels.values():
            rel.metrics.loyalty = 0.2
            rel.metrics.ideological_proximity = 0.2
            rel.metrics.fear = 0.8
        
        # Simulate betrayal event
        manager.apply_group_event(
            ["loyal", "wavering"],
            RelationshipEvent.BETRAYAL,
            details={"betrayer": "traitor"}
        )
        
        # Check impact on remaining members
        loyal_rels = manager.get_all_relationships("loyal")
        for rel in loyal_rels.values():
            # Trust should be damaged even toward others
            assert rel.metrics.trust < 0.5
            assert rel.metrics.betrayal_potential > 0
    
    def test_successful_mission_strengthens_bonds(self):
        """Test how success improves group cohesion"""
        members = ["char1", "char2", "char3"]
        manager = create_initial_cell_relationships(members)
        
        # Record initial cohesion
        initial_cohesion = manager.check_group_cohesion(members)
        
        # Multiple successful missions
        for _ in range(3):
            manager.apply_group_event(
                members,
                RelationshipEvent.MISSION_SUCCESS
            )
        
        # Check improved cohesion
        final_cohesion = manager.check_group_cohesion(members)
        
        assert final_cohesion["average_strength"] > initial_cohesion["average_strength"]
        assert len(final_cohesion["high_betrayal_risks"]) <= len(initial_cohesion["high_betrayal_risks"])