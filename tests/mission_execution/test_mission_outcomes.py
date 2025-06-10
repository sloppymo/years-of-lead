"""
Test suite for the Years of Lead mission execution system
Tests phase-based resolution, psychological integration, and emergent narrative events
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
from src.game.mission_execution import (
    MissionExecutor, MissionPhase, ActionType, MissionOutcome,
    ComplicationSeverity, MissionAction, MissionComplication,
    AgentPerformance, MissionReport, NarrativeGenerator
)
from src.game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait
from src.game.emotional_state import EmotionalState, TraumaTriggerType, TraumaMemory
from src.game.relationship_system import RelationshipManager, RelationshipType, RelationshipMetrics
from src.game.legal_system import LegalSystem, CrimeType
from src.game.intelligence_system import IntelligenceDatabase


class TestMissionAction:
    """Test mission action tracking"""
    
    def test_action_creation(self):
        """Test creating a mission action"""
        action = MissionAction(
            phase=MissionPhase.EXECUTION,
            agent_id="agent1",
            action_type=ActionType.COMBAT,
            timestamp=datetime.now(),
            success=True,
            details={"weapon": "rifle"},
            narrative="Agent successfully engages target"
        )
        
        assert action.phase == MissionPhase.EXECUTION
        assert action.agent_id == "agent1"
        assert action.success is True
        assert "weapon" in action.details
    
    def test_action_to_log_entry(self):
        """Test converting action to log entry"""
        action = MissionAction(
            phase=MissionPhase.INFILTRATION,
            agent_id="agent1",
            action_type=ActionType.STEALTH,
            timestamp=datetime.now(),
            success=False,
            details={},
            narrative="Agent spotted by guard"
        )
        
        log_entry = action.to_log_entry()
        assert "[INFILTRATION]" in log_entry
        assert "✗" in log_entry  # Failed action
        assert "Agent spotted by guard" in log_entry


class TestMissionComplication:
    """Test mission complications"""
    
    def test_complication_creation(self):
        """Test creating a complication"""
        comp = MissionComplication(
            phase=MissionPhase.EXECUTION,
            severity=ComplicationSeverity.MAJOR,
            description="Unexpected police patrol",
            affected_agents=["agent1", "agent2"],
            resolution_required=True,
            narrative_hook="Sirens wail in the distance"
        )
        
        assert comp.severity == ComplicationSeverity.MAJOR
        assert len(comp.affected_agents) == 2
        assert comp.resolution_required
    
    def test_generate_narrative(self):
        """Test narrative generation for complications"""
        comp = MissionComplication(
            phase=MissionPhase.EXTRACTION,
            severity=ComplicationSeverity.CATASTROPHIC,
            description="Exit route compromised",
            affected_agents=["agent1"],
            resolution_required=True,
            narrative_hook="All escape routes blocked"
        )
        
        narrative = comp.generate_narrative()
        assert "complete disaster" in narrative
        assert "Exit route compromised" in narrative


class TestAgentPerformance:
    """Test agent performance tracking"""
    
    def test_performance_initialization(self):
        """Test initializing agent performance"""
        perf = AgentPerformance(
            agent_id="agent1",
            actions_taken=[],
            stress_gained=0.0,
            trauma_triggered=False,
            relationships_affected={},
            betrayal_attempted=False,
            heroic_moment=False,
            panic_episodes=0,
            disobedience_count=0,
            crimes_committed=[]
        )
        
        assert perf.agent_id == "agent1"
        assert perf.calculate_performance_score() == 0.5  # No actions = neutral score
    
    def test_performance_score_calculation(self):
        """Test performance score calculation with various modifiers"""
        # Create successful actions
        actions = [
            MissionAction(MissionPhase.EXECUTION, "agent1", ActionType.COMBAT,
                         datetime.now(), True, {}, "Success"),
            MissionAction(MissionPhase.EXECUTION, "agent1", ActionType.STEALTH,
                         datetime.now(), True, {}, "Success"),
            MissionAction(MissionPhase.EXTRACTION, "agent1", ActionType.ESCAPE,
                         datetime.now(), False, {}, "Failed")
        ]
        
        perf = AgentPerformance(
            agent_id="agent1",
            actions_taken=actions,
            stress_gained=0.2,
            trauma_triggered=False,
            relationships_affected={},
            betrayal_attempted=False,
            heroic_moment=True,  # Heroic bonus
            panic_episodes=1,     # Panic penalty
            disobedience_count=0,
            crimes_committed=[]
        )
        
        score = perf.calculate_performance_score()
        # 2/3 success rate = 0.67 + 0.2 heroic - 0.1 panic = 0.77
        assert 0.7 < score < 0.8
    
    def test_betrayal_performance_penalty(self):
        """Test that betrayal severely impacts performance score"""
        perf = AgentPerformance(
            agent_id="traitor",
            actions_taken=[],
            stress_gained=0.0,
            trauma_triggered=False,
            relationships_affected={},
            betrayal_attempted=True,
            heroic_moment=False,
            panic_episodes=0,
            disobedience_count=0,
            crimes_committed=[]
        )
        
        score = perf.calculate_performance_score()
        assert score < 0.1  # Betrayal should tank the score


class TestMissionReport:
    """Test mission report generation"""
    
    def test_report_creation(self):
        """Test creating a mission report"""
        report = MissionReport(
            mission_id="mission001",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=30),
            phases_completed=[MissionPhase.PLANNING, MissionPhase.INFILTRATION],
            outcome=MissionOutcome.PARTIAL_SUCCESS,
            action_log=[],
            complications=[],
            agent_performance={},
            objectives_completed=["sabotage"],
            objectives_failed=["escape_undetected"],
            casualties=[],
            captured_agents=["agent2"],
            heat_generated=15,
            public_opinion_shift=0.02,
            resources_gained={"intel": 3},
            resources_lost={"equipment": 2},
            narrative_summary="Mixed results with one capture",
            memorable_moments=["Agent1's daring escape"],
            propaganda_value=0.4,
            symbolic_impact="A costly but symbolic victory"
        )
        
        assert report.mission_id == "mission001"
        assert report.outcome == MissionOutcome.PARTIAL_SUCCESS
        assert len(report.captured_agents) == 1
        assert report.heat_generated == 15
    
    def test_full_report_generation(self):
        """Test generating a full narrative report"""
        # Create sample performance data
        perf = AgentPerformance(
            agent_id="agent1",
            actions_taken=[],
            stress_gained=0.1,
            trauma_triggered=False,
            relationships_affected={},
            betrayal_attempted=False,
            heroic_moment=True,
            panic_episodes=0,
            disobedience_count=0,
            crimes_committed=[]
        )
        
        report = MissionReport(
            mission_id="mission001",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=45),
            phases_completed=list(MissionPhase),
            outcome=MissionOutcome.SUCCESS,
            action_log=[],
            complications=[],
            agent_performance={"agent1": perf},
            objectives_completed=["primary"],
            objectives_failed=[],
            casualties=[],
            captured_agents=[],
            heat_generated=10,
            public_opinion_shift=0.03,
            resources_gained={},
            resources_lost={},
            narrative_summary="Successful operation with minimal complications",
            memorable_moments=["Agent1's heroic moment"],
            propaganda_value=0.6,
            symbolic_impact="A victory for the resistance"
        )
        
        full_report = report.generate_full_report()
        
        assert "MISSION REPORT: mission001" in full_report
        assert "SUCCESS" in full_report
        assert "Duration: 45.0 minutes" in full_report
        assert "⭐ Displayed exceptional heroism" in full_report
        assert "Heat Generated: +10" in full_report


class TestMissionExecutor:
    """Test the main mission executor"""
    
    @pytest.fixture
    def mock_systems(self):
        """Create mock game systems"""
        legal_system = Mock(spec=LegalSystem)
        intelligence_system = Mock(spec=IntelligenceDatabase)
        relationship_manager = Mock(spec=RelationshipManager)
        
        return legal_system, intelligence_system, relationship_manager
    
    @pytest.fixture
    def executor(self, mock_systems):
        """Create a mission executor with mocked systems"""
        legal, intel, relations = mock_systems
        return MissionExecutor(legal, intel, relations)
    
    @pytest.fixture
    def test_agents(self):
        """Create test agents"""
        creator = CharacterCreator()
        
        agents = []
        # Leader
        leader = creator.create_character(
            "Squad Leader",
            BackgroundType.MILITARY,
            PersonalityTrait.LEADER,
            PersonalityTrait.METHODICAL
        )
        agents.append(leader)
        
        # Specialist
        specialist = creator.create_character(
            "Tech Specialist",
            BackgroundType.TECHNICAL,
            PersonalityTrait.ANALYTICAL,
            PersonalityTrait.CAUTIOUS
        )
        agents.append(specialist)
        
        # Potentially unstable member
        unstable = creator.create_character(
            "Rookie",
            BackgroundType.CRIMINAL,
            PersonalityTrait.RECKLESS,
            PersonalityTrait.OPPORTUNISTIC
        )
        # Add trauma
        unstable.emotional_state.apply_trauma(
            trauma_intensity=0.7,
            event_type="violence_witnessed",
            triggers=[TraumaTriggerType.VIOLENCE, TraumaTriggerType.LOUD_NOISES]
        )
        agents.append(unstable)
        
        return agents
    
    @pytest.fixture
    def mock_mission(self):
        """Create a mock mission"""
        mission = Mock()
        mission.id = "test_mission_001"
        mission.primary_objective = "sabotage_communications"
        mission.required_skills = ["technical", "stealth"]
        mission.faction_id = "resistance"
        mission.mission_type = "sabotage"
        return mission
    
    @pytest.fixture
    def mock_location(self):
        """Create a mock location"""
        location = Mock()
        location.id = "downtown"
        location.security_level = 7
        return location
    
    def test_executor_initialization(self, mock_systems):
        """Test creating a mission executor"""
        legal, intel, relations = mock_systems
        executor = MissionExecutor(legal, intel, relations)
        
        assert executor.legal_system == legal
        assert executor.intelligence_system == intel
        assert executor.relationship_manager == relations
        assert executor.narrative_generator is not None
    
    def test_planning_phase_with_conflicts(self, executor, test_agents, mock_mission):
        """Test planning phase with relationship conflicts"""
        # Set up relationship conflict
        executor.relationship_manager.get_relationship.return_value = Mock(
            metrics=Mock(trust=-0.6)  # Very low trust
        )
        
        report = MissionReport(
            mission_id="test",
            start_time=datetime.now(),
            end_time=datetime.now(),
            phases_completed=[],
            outcome=MissionOutcome.FAILURE,
            action_log=[],
            complications=[],
            agent_performance={agent.id: executor._init_agent_performance(agent.id) for agent in test_agents},
            objectives_completed=[],
            objectives_failed=[],
            casualties=[],
            captured_agents=[],
            heat_generated=0,
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        result = executor._execute_planning_phase(mock_mission, test_agents, report)
        
        # Should have complications from trust issues
        assert len(report.complications) > 0
        comp = report.complications[0]
        assert comp.severity == ComplicationSeverity.MODERATE
        assert "refuses to work with" in comp.description
    
    def test_infiltration_phase_trauma_trigger(self, executor, test_agents, mock_mission, mock_location):
        """Test infiltration phase with trauma triggers"""
        report = MissionReport(
            mission_id="test",
            start_time=datetime.now(),
            end_time=datetime.now(),
            phases_completed=[],
            outcome=MissionOutcome.FAILURE,
            action_log=[],
            complications=[],
            agent_performance={agent.id: executor._init_agent_performance(agent.id) for agent in test_agents},
            objectives_completed=[],
            objectives_failed=[],
            casualties=[],
            captured_agents=[],
            heat_generated=0,
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        result = executor._execute_infiltration_phase(mock_mission, test_agents, mock_location, report)
        
        # Check for trauma triggers (unstable agent has trauma)
        unstable_perf = next(p for p in report.agent_performance.values() 
                            if p.agent_id == test_agents[2].id)
        
        # Agent with trauma should have issues
        assert any("traumatic memories" in action.narrative for action in report.action_log)
    
    def test_execution_phase_betrayal(self, executor, test_agents, mock_mission, mock_location):
        """Test betrayal during execution phase"""
        # Mock betrayal check to always betray
        with patch.object(executor, '_check_for_betrayal') as mock_betrayal:
            mock_betrayal.return_value = {
                "betrayal_occurred": True,
                "reason": "overwhelming fear"
            }
            
            report = MissionReport(
                mission_id="test",
                start_time=datetime.now(),
                end_time=datetime.now(),
                phases_completed=[],
                outcome=MissionOutcome.FAILURE,
                action_log=[],
                complications=[],
                agent_performance={agent.id: executor._init_agent_performance(agent.id) for agent in test_agents},
                objectives_completed=[],
                objectives_failed=[],
                casualties=[],
                captured_agents=[],
                heat_generated=0,
                public_opinion_shift=0.0,
                resources_gained={},
                resources_lost={},
                narrative_summary="",
                memorable_moments=[],
                propaganda_value=0.0,
                symbolic_impact=""
            )
            
            result = executor._execute_execution_phase(mock_mission, test_agents, mock_location, {}, report)
            
            # Should abort mission due to betrayal
            assert result["abort_mission"] is True
            
            # Check for catastrophic complication
            catastrophic = [c for c in report.complications if c.severity == ComplicationSeverity.CATASTROPHIC]
            assert len(catastrophic) > 0
            assert "Betrayal" in catastrophic[0].description
    
    def test_extraction_phase_casualties(self, executor, test_agents, mock_mission, mock_location):
        """Test extraction phase with potential casualties"""
        report = MissionReport(
            mission_id="test",
            start_time=datetime.now(),
            end_time=datetime.now(),
            phases_completed=[],
            outcome=MissionOutcome.FAILURE,
            action_log=[],
            complications=[],
            agent_performance={agent.id: executor._init_agent_performance(agent.id) for agent in test_agents},
            objectives_completed=[],
            objectives_failed=["primary"],  # Failed mission = harder extraction
            casualties=[],
            captured_agents=[],
            heat_generated=25,  # High heat = harder extraction
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        # Mock random to force some captures/casualties
        with patch('random.random') as mock_random:
            # First agent escapes, second captured, third varies
            mock_random.side_effect = [0.1, 0.9, 0.9, 0.7]  # escape check, capture/kill check
            
            result = executor._execute_extraction_phase(mock_mission, test_agents, mock_location, report)
            
            # Should have some agents captured or killed
            assert len(report.captured_agents) > 0 or len(report.casualties) > 0
    
    def test_skill_check_with_traits(self, executor):
        """Test skill checks are modified by traits"""
        # Create methodical agent (bonus to success)
        creator = CharacterCreator()
        methodical = creator.create_character(
            "Methodical Agent",
            BackgroundType.TECHNICAL,
            PersonalityTrait.METHODICAL,
            PersonalityTrait.ANALYTICAL
        )
        
        # Create reckless agent (penalty to success)
        reckless = creator.create_character(
            "Reckless Agent",
            BackgroundType.CRIMINAL,
            PersonalityTrait.RECKLESS,
            PersonalityTrait.OPPORTUNISTIC
        )
        
        # Set similar skill levels
        methodical.skills.technical = 5
        reckless.skills.technical = 5
        
        # Perform skill checks
        methodical_check = executor._perform_skill_check(methodical, ["technical"])
        reckless_check = executor._perform_skill_check(reckless, ["technical"])
        
        # Methodical should have better chance
        assert methodical_check["details"]["chance"] > reckless_check["details"]["chance"]
    
    def test_cascade_failure_detection(self, executor, test_agents):
        """Test detection of cascading mission failure"""
        report = MissionReport(
            mission_id="test",
            start_time=datetime.now(),
            end_time=datetime.now(),
            phases_completed=[],
            outcome=MissionOutcome.FAILURE,
            action_log=[],
            complications=[],
            agent_performance={agent.id: executor._init_agent_performance(agent.id) for agent in test_agents},
            objectives_completed=[],
            objectives_failed=[],
            casualties=[],
            captured_agents=[],
            heat_generated=0,
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        # Test 1: All agents panicking
        for perf in report.agent_performance.values():
            perf.panic_episodes = 2
        
        assert executor._check_cascade_failure(test_agents, report) is True
        
        # Test 2: All agents captured/killed
        report.casualties = [test_agents[0].id]
        report.captured_agents = [test_agents[1].id, test_agents[2].id]
        
        assert executor._check_cascade_failure(test_agents, report) is True
        
        # Test 3: Multiple catastrophic complications
        report.complications = [
            MissionComplication(MissionPhase.EXECUTION, ComplicationSeverity.CATASTROPHIC,
                              "Betrayal", [], True, ""),
            MissionComplication(MissionPhase.EXTRACTION, ComplicationSeverity.CATASTROPHIC,
                              "Ambush", [], True, "")
        ]
        
        assert executor._check_cascade_failure(test_agents, report) is True
    
    def test_propaganda_value_calculation(self, executor):
        """Test propaganda value calculation"""
        # Successful mission with heroics
        report1 = MissionReport(
            mission_id="test1",
            start_time=datetime.now(),
            end_time=datetime.now(),
            phases_completed=list(MissionPhase),
            outcome=MissionOutcome.SUCCESS,
            action_log=[],
            complications=[],
            agent_performance={
                "hero": AgentPerformance("hero", [], 0, False, {}, False, True, 0, 0, [])
            },
            objectives_completed=["primary"],
            objectives_failed=[],
            casualties=[],
            captured_agents=[],
            heat_generated=10,
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        value1 = executor._calculate_propaganda_value(report1)
        assert value1 > 0.5  # Success + heroics = good propaganda
        
        # Failed mission with betrayal
        report2 = MissionReport(
            mission_id="test2",
            start_time=datetime.now(),
            end_time=datetime.now(),
            phases_completed=list(MissionPhase),
            outcome=MissionOutcome.FAILURE,
            action_log=[],
            complications=[],
            agent_performance={
                "traitor": AgentPerformance("traitor", [], 0, False, {}, True, False, 0, 0, [])
            },
            objectives_completed=[],
            objectives_failed=["primary"],
            casualties=[],
            captured_agents=[],
            heat_generated=30,  # High heat
            public_opinion_shift=0.0,
            resources_gained={},
            resources_lost={},
            narrative_summary="",
            memorable_moments=[],
            propaganda_value=0.0,
            symbolic_impact=""
        )
        
        value2 = executor._calculate_propaganda_value(report2)
        assert value2 < 0.2  # Failure + betrayal + high heat = bad propaganda
    
    def test_complete_mission_execution(self, executor, test_agents, mock_mission, mock_location):
        """Test executing a complete mission"""
        equipment = {"rifles": 3, "explosives": 2}
        
        # Execute mission
        report = executor.execute_mission(mock_mission, test_agents, mock_location, equipment)
        
        # Verify report structure
        assert report.mission_id == "test_mission_001"
        assert len(report.phases_completed) > 0
        assert report.outcome in list(MissionOutcome)
        assert report.narrative_summary != ""
        assert report.propaganda_value >= 0.0
        assert report.symbolic_impact != ""
        
        # Verify all agents have performance records
        for agent in test_agents:
            assert agent.id in report.agent_performance
            perf = report.agent_performance[agent.id]
            assert isinstance(perf, AgentPerformance)


class TestNarrativeGenerator:
    """Test narrative generation"""
    
    def test_mission_summary_generation(self):
        """Test generating mission summaries for different outcomes"""
        generator = NarrativeGenerator()
        
        # Critical success
        report1 = Mock(
            outcome=MissionOutcome.CRITICAL_SUCCESS,
            agent_performance={},
            casualties=[],
            captured_agents=[],
            complications=[],
            propaganda_value=0.8
        )
        summary1 = generator.generate_mission_summary(report1)
        assert "stunning display" in summary1
        assert "turning point" in summary1
        
        # Disaster with betrayal
        report2 = Mock(
            outcome=MissionOutcome.DISASTER,
            agent_performance={
                "traitor": Mock(betrayal_attempted=True)
            },
            casualties=["agent1", "agent2"],
            captured_agents=["agent3"],
            complications=[Mock(severity=ComplicationSeverity.CATASTROPHIC)],
            propaganda_value=0.1
        )
        summary2 = generator.generate_mission_summary(report2)
        assert "chaos and tragedy" in summary2
        assert "betrayal" in summary2
        assert "2 brave souls" in summary2


class TestIntegrationScenarios:
    """Test complete mission scenarios"""
    
    @pytest.fixture
    def full_setup(self):
        """Create a complete test setup"""
        legal = LegalSystem()
        intel = IntelligenceDatabase()
        relations = RelationshipManager()
        executor = MissionExecutor(legal, intel, relations)
        
        # Create a team
        creator = CharacterCreator()
        team = [
            creator.create_character("Leader", BackgroundType.MILITARY,
                                   PersonalityTrait.LEADER, PersonalityTrait.LOYAL),
            creator.create_character("Hacker", BackgroundType.TECHNICAL,
                                   PersonalityTrait.ANALYTICAL, PersonalityTrait.CAUTIOUS),
            creator.create_character("Fighter", BackgroundType.CRIMINAL,
                                   PersonalityTrait.RECKLESS, PersonalityTrait.AGGRESSIVE)
        ]
        
        # Set up relationships
        for i, agent1 in enumerate(team):
            for j, agent2 in enumerate(team):
                if i != j:
                    relations.create_relationship(
                        agent1.id, agent2.id,
                        RelationshipType.COMRADE,
                        RelationshipMetrics(trust=0.5, loyalty=0.6)
                    )
        
        return executor, team, legal, intel, relations
    
    def test_successful_stealth_mission(self, full_setup):
        """Test a successful stealth mission"""
        executor, team, legal, intel, relations = full_setup
        
        # Create stealth mission
        mission = Mock()
        mission.id = "stealth_001"
        mission.primary_objective = "steal_documents"
        mission.required_skills = ["stealth", "hacking"]
        mission.faction_id = "resistance"
        mission.mission_type = "theft"
        
        location = Mock()
        location.id = "corporate_hq"
        location.security_level = 5  # Medium security
        
        equipment = {"lockpicks": 2, "hacking_device": 1}
        
        # Execute mission
        report = executor.execute_mission(mission, team, location, equipment)
        
        # Mission should have reasonable chance of success
        assert report.outcome in [
            MissionOutcome.SUCCESS,
            MissionOutcome.CRITICAL_SUCCESS,
            MissionOutcome.PARTIAL_SUCCESS
        ]
        
        # Check for appropriate crimes if caught
        for agent_id in report.captured_agents:
            perf = report.agent_performance[agent_id]
            assert CrimeType.GRAND_THEFT in perf.crimes_committed or CrimeType.BURGLARY in perf.crimes_committed
    
    def test_high_stakes_combat_mission(self, full_setup):
        """Test a high-risk combat mission"""
        executor, team, legal, intel, relations = full_setup
        
        # Add combat trauma to one agent
        team[2].emotional_state.apply_trauma(
            trauma_intensity=0.8,
            event_type="violence_witnessed",
            triggers=[TraumaTriggerType.VIOLENCE]
        )
        
        # Create combat mission
        mission = Mock()
        mission.id = "assault_001"
        mission.primary_objective = "eliminate_target"
        mission.required_skills = ["combat", "survival"]
        mission.faction_id = "resistance"
        mission.mission_type = "assault"
        
        location = Mock()
        location.id = "military_base"
        location.security_level = 9  # Very high security
        
        equipment = {"rifles": 3, "body_armor": 3, "grenades": 6}
        
        # Execute mission
        report = executor.execute_mission(mission, team, location, equipment)
        
        # High security should make mission difficult
        assert report.heat_generated > 15
        
        # Combat mission should trigger trauma
        traumatized_perf = report.agent_performance[team[2].id]
        assert traumatized_perf.trauma_triggered or traumatized_perf.panic_episodes > 0
        
        # Check narrative captures the intensity
        assert any(moment for moment in report.memorable_moments)
    
    def test_betrayal_cascade_scenario(self, full_setup):
        """Test how betrayal affects mission and team dynamics"""
        executor, team, legal, intel, relations = full_setup
        
        # Corrupt one agent's relationships
        traitor = team[2]
        for other in team:
            if other.id != traitor.id:
                rel = relations.get_relationship(traitor.id, other.id)
                if rel:
                    rel.metrics.trust = -0.8
                    rel.metrics.loyalty = 0.1
                    rel.metrics.ideological_proximity = 0.2
        
        # Make traitor opportunistic and fearful
        traitor.emotional_state.fear = 0.8
        traitor.traits.primary_trait = PersonalityTrait.OPPORTUNISTIC
        
        mission = Mock()
        mission.id = "sabotage_001"
        mission.primary_objective = "destroy_equipment"
        mission.required_skills = ["technical", "stealth"]
        mission.faction_id = "resistance"
        mission.mission_type = "sabotage"
        
        location = Mock()
        location.id = "power_plant"
        location.security_level = 7
        
        equipment = {"explosives": 5, "timers": 3}
        
        # Execute mission multiple times to test betrayal probability
        betrayal_occurred = False
        for _ in range(10):
            report = executor.execute_mission(mission, team, location, equipment)
            if any(p.betrayal_attempted for p in report.agent_performance.values()):
                betrayal_occurred = True
                
                # Check consequences
                assert report.outcome in [MissionOutcome.ABORTED, MissionOutcome.DISASTER]
                assert any("Betrayal" in c.description for c in report.complications)
                assert any("betrayal" in moment.lower() for moment in report.memorable_moments)
                break
        
        # With these conditions, betrayal should be likely
        assert betrayal_occurred


@pytest.mark.integration
class TestEndToEndMissionFlow:
    """Test complete mission flow with all systems integrated"""
    
    def test_mission_affects_all_systems(self):
        """Test that mission outcomes properly affect all game systems"""
        # Create real systems
        legal = LegalSystem()
        intel = IntelligenceDatabase()
        relations = RelationshipManager()
        executor = MissionExecutor(legal, intel, relations)
        
        # Create team
        creator = CharacterCreator()
        team = [
            creator.create_character("Agent1", BackgroundType.ACTIVIST,
                                   PersonalityTrait.IDEALISTIC, PersonalityTrait.LOYAL),
            creator.create_character("Agent2", BackgroundType.MILITARY,
                                   PersonalityTrait.PRAGMATIC, PersonalityTrait.METHODICAL)
        ]
        
        # Set up initial relationship
        relations.create_relationship(
            team[0].id, team[1].id,
            RelationshipType.COMRADE,
            RelationshipMetrics(trust=0.6, loyalty=0.7)
        )
        
        # Mission setup
        mission = Mock()
        mission.id = "integrated_test_001"
        mission.primary_objective = "hack_database"
        mission.required_skills = ["hacking", "stealth"]
        mission.faction_id = "resistance"
        mission.mission_type = "infiltration"
        
        location = Mock()
        location.id = "data_center"
        location.security_level = 6
        
        equipment = {"laptop": 1, "usb_drives": 5}
        
        # Execute mission
        initial_trust = relations.get_relationship(team[0].id, team[1].id).metrics.trust
        initial_stress_1 = team[0].get_stress_level()
        initial_stress_2 = team[1].get_stress_level()
        
        report = executor.execute_mission(mission, team, location, equipment)
        
        # Check emotional state changes
        final_stress_1 = team[0].get_stress_level()
        final_stress_2 = team[1].get_stress_level()
        
        # Stress should increase from mission
        assert final_stress_1 >= initial_stress_1
        assert final_stress_2 >= initial_stress_2
        
        # Check relationship changes
        final_trust = relations.get_relationship(team[0].id, team[1].id).metrics.trust
        
        if report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.CRITICAL_SUCCESS]:
            # Success should improve trust
            assert final_trust >= initial_trust
        
        # Check legal consequences for captured agents
        for agent_id in report.captured_agents:
            # Legal system should have crimes recorded
            # (Would check actual legal system records here)
            pass
        
        # Check intelligence events generated
        # (Would verify intelligence system received appropriate events)
        
        # Verify narrative coherence
        assert report.narrative_summary
        assert len(report.narrative_summary) > 50  # Meaningful narrative
        assert report.symbolic_impact
        assert 0.0 <= report.propaganda_value <= 1.0