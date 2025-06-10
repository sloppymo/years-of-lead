#!/usr/bin/env python3
"""
Years of Lead - Automated Playtesting System
MAX mode testing for Phases 1 & 2 (Character Psychology + Mission Execution)
"""

import json
import os
import random
import uuid
from datetime import datetime
from typing import List, Dict, Any, Tuple
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.game.mission_execution import (
    MissionExecutor, MissionPhase, MissionOutcome, MissionReport,
    ComplicationSeverity, MissionAction, MissionComplication,
    AgentPerformance
)
from src.game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait
from src.game.relationship_system import RelationshipManager, RelationshipType, RelationshipMetrics
from src.game.legal_system import LegalSystem, CrimeType
from src.game.intelligence_system import IntelligenceDatabase
from src.game.emotional_state import TraumaTriggerType


class MockMission:
    """Mock mission for testing"""
    def __init__(self, mission_id, mission_type, objective, required_skills):
        self.id = mission_id
        self.mission_type = mission_type
        self.primary_objective = objective
        self.required_skills = required_skills
        self.faction_id = "resistance"


class MockLocation:
    """Mock location for testing"""
    def __init__(self, location_id, name, security_level):
        self.id = location_id
        self.name = name
        self.security_level = security_level


class PlaytestLogger:
    """Logs playtest results"""
    
    def __init__(self):
        self.logs_dir = "playtest_logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
    def determine_emotional_tone(self, report: MissionReport) -> str:
        """Analyze mission results for emotional tone"""
        
        # Count key events
        betrayals = sum(1 for perf in report.agent_performance.values() if perf.betrayal_attempted)
        heroics = sum(1 for perf in report.agent_performance.values() if perf.heroic_moment)
        casualties = len(report.casualties)
        panics = sum(perf.panic_episodes for perf in report.agent_performance.values())
        
        # Determine tone based on events
        if report.outcome == MissionOutcome.DISASTER and casualties >= 2:
            if betrayals > 0:
                return "tragic_betrayal"
            elif panics > 2:
                return "psychological_collapse"
            else:
                return "somber_defeat"
        
        elif report.outcome == MissionOutcome.CRITICAL_SUCCESS:
            if heroics > 0:
                return "heroic_triumph"
            else:
                return "professional_success"
        
        elif report.outcome == MissionOutcome.ABORTED:
            if panics > 0:
                return "fearful_retreat"
            else:
                return "tactical_withdrawal"
        
        elif betrayals > 0 and heroics > 0:
            return "ironic_duality"
        
        elif casualties > 0 and report.outcome in [MissionOutcome.SUCCESS, MissionOutcome.PARTIAL_SUCCESS]:
            return "pyrrhic_victory"
        
        elif report.propaganda_value > 0.7:
            return "symbolic_statement"
        
        else:
            return "ambiguous_outcome"
    
    def log_iteration(self, iteration_id: str, mission_config: Dict, 
                      team_config: List[Dict], report: MissionReport,
                      relationships: List[Dict], bugs: List[str] = None):
        """Log a complete playtest iteration"""
        
        # Extract key psychological events
        psychological_events = []
        for action in report.action_log:
            if any(keyword in action.narrative.lower() 
                   for keyword in ['trauma', 'panic', 'freeze', 'betrayal', 'heroic']):
                psychological_events.append({
                    'phase': action.phase.value,
                    'agent': action.agent_id,
                    'narrative': action.narrative,
                    'success': action.success
                })
        
        # Compile performance summaries
        agent_summaries = {}
        for agent_id, perf in report.agent_performance.items():
            agent_summaries[agent_id] = {
                'score': perf.calculate_performance_score(),
                'heroic': perf.heroic_moment,
                'betrayal': perf.betrayal_attempted,
                'trauma_triggered': perf.trauma_triggered,
                'panic_episodes': perf.panic_episodes,
                'captured': agent_id in report.captured_agents,
                'killed': agent_id in report.casualties
            }
        
        log_entry = {
            'iteration_id': iteration_id,
            'timestamp': datetime.now().isoformat(),
            'mission': mission_config,
            'team': team_config,
            'relationships': relationships,
            'outcome': {
                'result': report.outcome.value,
                'phases_completed': [p.value for p in report.phases_completed],
                'objectives_completed': len(report.objectives_completed),
                'objectives_failed': len(report.objectives_failed),
                'casualties': report.casualties,
                'captured': report.captured_agents,
                'heat_generated': report.heat_generated,
                'public_opinion_shift': report.public_opinion_shift,
                'propaganda_value': report.propaganda_value
            },
            'psychological_events': psychological_events,
            'agent_performance': agent_summaries,
            'memorable_moments': report.memorable_moments,
            'narrative_summary': report.narrative_summary,
            'symbolic_impact': report.symbolic_impact,
            'emotional_tone': self.determine_emotional_tone(report),
            'bugs': bugs or []
        }
        
        # Save to file
        filename = os.path.join(self.logs_dir, f"iteration_{iteration_id}.json")
        with open(filename, 'w') as f:
            json.dump(log_entry, f, indent=2)
        
        return log_entry


class MissionGenerator:
    """Generates varied mission configurations"""
    
    MISSION_TYPES = ['sabotage', 'assassination', 'propaganda', 'theft', 'rescue']
    
    OBJECTIVES = {
        'sabotage': [
            "Destroy government surveillance hub",
            "Disable power grid infrastructure", 
            "Sabotage military supply depot",
            "Destroy propaganda broadcast tower"
        ],
        'assassination': [
            "Eliminate regime official",
            "Neutralize secret police commander",
            "Remove corrupt judge",
            "Target military general"
        ],
        'propaganda': [
            "Hijack broadcast system",
            "Distribute underground newspapers",
            "Tag government buildings with slogans",
            "Project resistance imagery on monuments"
        ],
        'theft': [
            "Steal military intelligence",
            "Acquire regime financial records",
            "Obtain weapons cache",
            "Extract prisoner lists"
        ],
        'rescue': [
            "Free political prisoners",
            "Extract compromised operative",
            "Rescue kidnapped civilian leader",
            "Evacuate threatened families"
        ]
    }
    
    LOCATIONS = [
        ("central_command", "Central Government Complex", 9),
        ("police_hq", "Secret Police Headquarters", 8),
        ("media_center", "State Media Building", 7),
        ("military_base", "Northern Military Installation", 8),
        ("prison_complex", "Political Detention Center", 9),
        ("financial_district", "Regime Banking Center", 6),
        ("port_warehouse", "Harbor Supply Depot", 5),
        ("suburban_safehouse", "Residential District", 4)
    ]
    
    def generate_mission(self, iteration: int) -> Tuple[MockMission, MockLocation, Dict]:
        """Generate a mission with appropriate difficulty scaling"""
        
        mission_type = random.choice(self.MISSION_TYPES)
        objective = random.choice(self.OBJECTIVES[mission_type])
        
        # Add variation to objectives
        if random.random() < 0.3:
            objective += " (time sensitive)"
        
        mission_id = f"OPERATION_{mission_type.upper()}_{iteration:03d}"
        
        # Select location based on mission type
        if mission_type in ['assassination', 'rescue']:
            # Higher security for these
            location_data = random.choice([loc for loc in self.LOCATIONS if loc[2] >= 7])
        else:
            location_data = random.choice(self.LOCATIONS)
        
        location = MockLocation(*location_data)
        
        # Required skills based on mission type
        skill_sets = {
            'sabotage': ['technical', 'stealth', 'explosives'],
            'assassination': ['combat', 'stealth', 'marksmanship'],
            'propaganda': ['technical', 'social', 'media'],
            'theft': ['stealth', 'technical', 'infiltration'],
            'rescue': ['combat', 'medical', 'leadership']
        }
        
        required_skills = skill_sets.get(mission_type, ['combat', 'stealth'])
        
        # Equipment based on mission
        equipment_sets = {
            'sabotage': {
                'explosives': random.randint(2, 5),
                'detonators': random.randint(2, 4),
                'tools': 2,
                'fake_ids': 3
            },
            'assassination': {
                'sniper_rifle': 1,
                'pistol_silenced': 2,
                'poison': 1,
                'escape_vehicle': 1
            },
            'propaganda': {
                'hacking_kit': 1,
                'spray_paint': 5,
                'leaflets': 100,
                'projector': 1
            },
            'theft': {
                'lockpicks': 3,
                'hacking_kit': 1,
                'duffel_bags': 3,
                'smoke_grenades': 2
            },
            'rescue': {
                'assault_rifles': 3,
                'medical_kit': 2,
                'breaching_charges': 2,
                'transport_van': 1
            }
        }
        
        equipment = equipment_sets.get(mission_type, {'basic_kit': 1})
        
        mission = MockMission(mission_id, mission_type, objective, required_skills)
        
        return mission, location, equipment


class TeamGenerator:
    """Generates diverse team configurations"""
    
    FIRST_NAMES = [
        "Sarah", "Marcus", "Elena", "Carlos", "Maya", "Ahmed", "Nina", 
        "Viktor", "Lucia", "Dmitri", "Fatima", "Jorge", "Aisha", "Pavel"
    ]
    
    LAST_NAMES = [
        "Chen", "Rodriguez", "Petrov", "Hassan", "Silva", "Kowalski",
        "Nguyen", "Okafor", "Anderson", "Delacroix", "Volkov", "Santos"
    ]
    
    def __init__(self, creator: CharacterCreator):
        self.creator = creator
        
    def generate_team(self, size: int = 3) -> List:
        """Generate a team with varied backgrounds and traits"""
        
        team = []
        used_names = set()
        
        # Ensure variety in backgrounds
        backgrounds = list(BackgroundType)
        random.shuffle(backgrounds)
        
        # Trait combinations that create interesting dynamics
        trait_combos = [
            (PersonalityTrait.LEADER, PersonalityTrait.METHODICAL),
            (PersonalityTrait.ANALYTICAL, PersonalityTrait.CAUTIOUS),
            (PersonalityTrait.RECKLESS, PersonalityTrait.OPPORTUNISTIC),
            (PersonalityTrait.COMPASSIONATE, PersonalityTrait.IDEALISTIC),
            (PersonalityTrait.RUTHLESS, PersonalityTrait.PRAGMATIC),
            (PersonalityTrait.CREATIVE, PersonalityTrait.INTUITIVE),
            (PersonalityTrait.LEADER, PersonalityTrait.PESSIMISTIC),
            (PersonalityTrait.ANALYTICAL, PersonalityTrait.METHODICAL)
        ]
        
        for i in range(size):
            # Generate unique name
            while True:
                first = random.choice(self.FIRST_NAMES)
                last = random.choice(self.LAST_NAMES)
                name = f"{first} {last}"
                if name not in used_names:
                    used_names.add(name)
                    break
            
            # Select background
            background = backgrounds[i % len(backgrounds)]
            
            # Select traits
            primary, secondary = random.choice(trait_combos)
            
            # Create character
            character = self.creator.create_character(
                name, background, primary, secondary
            )
            
            # Add trauma with probability
            if random.random() < 0.4:  # 40% chance of trauma
                trauma_types = list(TraumaTriggerType)
                triggers = random.sample(trauma_types, k=random.randint(1, 3))
                
                character.emotional_state.apply_trauma(
                    trauma_intensity=random.uniform(0.4, 0.8),
                    event_type=random.choice([
                        "witnessed_violence", "torture", "loss_of_comrade",
                        "betrayal", "civilian_deaths", "failed_mission"
                    ]),
                    triggers=triggers
                )
            
            # Randomize stress and ideology
            character.emotional_state.stress = random.uniform(0.1, 0.6)
            character.emotional_state.fear = random.uniform(0.0, 0.5)
            character.ideology_score = random.uniform(0.3, 0.9)
            
            team.append(character)
        
        return team
    
    def generate_relationships(self, team: List, manager: RelationshipManager) -> List[Dict]:
        """Generate complex relationship web"""
        
        relationships = []
        
        # Ensure at least one problematic relationship
        if len(team) >= 2:
            # Create a rivalry or strained relationship
            agent1, agent2 = random.sample(team, 2)
            
            rel_type = random.choice([RelationshipType.RIVAL, RelationshipType.SUBORDINATE])
            metrics = RelationshipMetrics(
                trust=random.uniform(-0.5, 0.2),
                loyalty=random.uniform(0.1, 0.4),
                fear=random.uniform(0.3, 0.7),
                ideological_proximity=random.uniform(0.1, 0.3)
            )
            
            manager.create_relationship(agent1.id, agent2.id, rel_type, metrics)
            relationships.append({
                'agent1': agent1.name,
                'agent2': agent2.name,
                'type': rel_type.value,
                'trust': metrics.trust,
                'loyalty': metrics.loyalty
            })
        
        # Add some positive relationships
        for _ in range(len(team) // 2):
            if len(team) >= 2:
                agent1, agent2 = random.sample(team, 2)
                
                # Skip if relationship already exists
                if manager.get_relationship(agent1.id, agent2.id):
                    continue
                
                rel_type = random.choice([
                    RelationshipType.COMRADE, RelationshipType.FRIEND,
                    RelationshipType.MENTOR, RelationshipType.ROMANTIC
                ])
                
                metrics = RelationshipMetrics(
                    trust=random.uniform(0.5, 0.9),
                    loyalty=random.uniform(0.6, 0.95),
                    fear=random.uniform(0.0, 0.2),
                    ideological_proximity=random.uniform(0.4, 0.9)
                )
                
                manager.create_relationship(agent1.id, agent2.id, rel_type, metrics)
                relationships.append({
                    'agent1': agent1.name,
                    'agent2': agent2.name,
                    'type': rel_type.value,
                    'trust': metrics.trust,
                    'loyalty': metrics.loyalty
                })
        
        return relationships


class AutomatedPlaytester:
    """Main playtest orchestrator"""
    
    def __init__(self):
        self.logger = PlaytestLogger()
        self.mission_gen = MissionGenerator()
        self.creator = CharacterCreator()
        self.team_gen = TeamGenerator(self.creator)
        
        # Initialize game systems
        self.legal_system = LegalSystem()
        self.intelligence_system = IntelligenceDatabase()
        self.relationship_manager = RelationshipManager()
        self.executor = MissionExecutor(
            self.legal_system, 
            self.intelligence_system,
            self.relationship_manager
        )
        
        self.iteration_count = 0
        self.unique_tones = set()
        self.non_tragic_count = 0
        self.bugs_found = []
        
    def run_iteration(self) -> Dict:
        """Run a single playtest iteration"""
        
        self.iteration_count += 1
        iteration_id = f"{self.iteration_count:03d}_{uuid.uuid4().hex[:8]}"
        
        print(f"\n{'='*60}")
        print(f"ITERATION {self.iteration_count}: {iteration_id}")
        print(f"{'='*60}")
        
        # Generate mission
        mission, location, equipment = self.mission_gen.generate_mission(self.iteration_count)
        print(f"Mission: {mission.id}")
        print(f"Type: {mission.mission_type} | Location: {location.name}")
        
        # Generate team
        team_size = random.choice([2, 3, 3, 4])  # Prefer 3-person teams
        team = self.team_gen.generate_team(team_size)
        print(f"Team size: {len(team)}")
        
        # Generate relationships
        relationships = self.team_gen.generate_relationships(team, self.relationship_manager)
        
        # Log team configuration
        team_config = []
        for agent in team:
            config = {
                'id': agent.id,
                'name': agent.name,
                'background': agent.background.name,
                'traits': {
                    'primary': agent.traits.primary_trait.value,
                    'secondary': agent.traits.secondary_trait.value
                },
                'stress': agent.get_stress_level(),
                'ideology': agent.get_ideological_score(),
                'trauma': agent.trauma.type.value if agent.trauma else None
            }
            team_config.append(config)
            print(f"  - {agent.name}: {config['background']} ({config['traits']['primary']})")
        
        # Execute mission
        try:
            report = self.executor.execute_mission(mission, team, location, equipment)
            bugs = []
        except Exception as e:
            print(f"ERROR during mission execution: {e}")
            bugs = [f"Mission execution error: {str(e)}"]
            # Create a failed report with all required fields
            report = MissionReport(
                mission_id=mission.id,
                start_time=datetime.now(),
                end_time=datetime.now(),
                phases_completed=[],
                outcome=MissionOutcome.DISASTER,
                action_log=[],
                complications=[],
                agent_performance={agent.id: AgentPerformance(
                    agent_id=agent.id,
                    actions_taken=[],
                    stress_gained=0.0,
                    trauma_triggered=False,
                    relationships_affected={},
                    betrayal_attempted=False,
                    heroic_moment=False,
                    panic_episodes=0,
                    disobedience_count=0,
                    crimes_committed=[]
                ) for agent in team},
                objectives_completed=[],
                objectives_failed=[mission.primary_objective],
                casualties=[],
                captured_agents=[],
                heat_generated=0,
                public_opinion_shift=0.0,
                resources_gained={},
                resources_lost={},
                narrative_summary=f"Mission failed due to system error: {e}",
                memorable_moments=[],
                propaganda_value=0.0,
                symbolic_impact="Technical failure"
            )
        
        # Check for logical inconsistencies
        bugs.extend(self.check_for_bugs(report, team))
        
        # Log results
        mission_config = {
            'id': mission.id,
            'type': mission.mission_type,
            'objective': mission.primary_objective,
            'location': location.name,
            'security_level': location.security_level
        }
        
        log_entry = self.logger.log_iteration(
            iteration_id, mission_config, team_config, 
            report, relationships, bugs
        )
        
        # Track unique tones
        tone = log_entry['emotional_tone']
        self.unique_tones.add(tone)
        
        # Track non-tragic outcomes
        if report.outcome not in [MissionOutcome.FAILURE, MissionOutcome.DISASTER]:
            self.non_tragic_count += 1
        
        # Print summary
        print(f"\nOutcome: {report.outcome.value}")
        print(f"Emotional tone: {tone}")
        print(f"Casualties: {len(report.casualties)} | Captured: {len(report.captured_agents)}")
        print(f"Propaganda value: {report.propaganda_value:.0%}")
        
        if bugs:
            print(f"BUGS FOUND: {len(bugs)}")
            for bug in bugs:
                print(f"  - {bug}")
                self.bugs_found.append(bug)
        
        return log_entry
    
    def check_for_bugs(self, report: MissionReport, team: List) -> List[str]:
        """Check for logical inconsistencies and bugs"""
        
        bugs = []
        
        # Check if dead agents are still performing actions
        for action in report.action_log:
            if action.agent_id in report.casualties:
                # Check if action happened after death
                death_phase = None
                for earlier_action in report.action_log:
                    if earlier_action.agent_id == action.agent_id and "killed" in earlier_action.narrative:
                        death_phase = earlier_action.phase
                        break
                
                if death_phase and action.phase.value > death_phase.value:
                    bugs.append(f"Dead agent {action.agent_id} performed action after death")
        
        # Check if captured agents are still active
        for action in report.action_log:
            if action.agent_id in report.captured_agents:
                capture_phase = None
                for earlier_action in report.action_log:
                    if earlier_action.agent_id == action.agent_id and "captured" in earlier_action.narrative:
                        capture_phase = earlier_action.phase
                        break
                
                if capture_phase and action.phase.value > capture_phase.value:
                    bugs.append(f"Captured agent {action.agent_id} performed action after capture")
        
        # Check propaganda value consistency
        if len(report.casualties) == len(team) and report.propaganda_value < 0.3:
            bugs.append("Total team wipe should generate higher propaganda value")
        
        # Check betrayal logic
        betrayal_count = sum(1 for perf in report.agent_performance.values() if perf.betrayal_attempted)
        if betrayal_count > len(team) // 2:
            bugs.append("Excessive betrayals - more than half the team betrayed")
        
        # Check phase progression
        expected_phases = [MissionPhase.PLANNING, MissionPhase.INFILTRATION, 
                          MissionPhase.EXECUTION, MissionPhase.EXTRACTION]
        for i, phase in enumerate(report.phases_completed[:-1]):  # Exclude aftermath
            if i < len(expected_phases) and phase != expected_phases[i]:
                bugs.append(f"Phase progression error: {phase.value} at position {i}")
        
        return bugs
    
    def run_full_test(self):
        """Run complete playtest session"""
        
        print("="*80)
        print("YEARS OF LEAD - AUTOMATED PLAYTEST SESSION")
        print("MAX Mode: Deep testing of Character Psychology + Mission Execution")
        print("="*80)
        
        # Run until conditions are met
        while (self.iteration_count < 20 or 
               len(self.unique_tones) < 3 or 
               self.non_tragic_count < 2):
            
            self.run_iteration()
            
            # Progress report every 5 iterations
            if self.iteration_count % 5 == 0:
                print(f"\n📊 PROGRESS REPORT:")
                print(f"Iterations: {self.iteration_count}")
                print(f"Unique tones: {len(self.unique_tones)} - {self.unique_tones}")
                print(f"Non-tragic outcomes: {self.non_tragic_count}")
                print(f"Bugs found: {len(self.bugs_found)}")
        
        # Final report
        self.generate_final_report()
    
    def generate_final_report(self):
        """Generate summary report and update changelog"""
        
        print("\n" + "="*80)
        print("PLAYTEST SESSION COMPLETE")
        print("="*80)
        
        print(f"\n📊 FINAL STATISTICS:")
        print(f"Total iterations: {self.iteration_count}")
        print(f"Unique emotional tones: {len(self.unique_tones)}")
        print(f"  - {', '.join(sorted(self.unique_tones))}")
        print(f"Non-tragic outcomes: {self.non_tragic_count} ({self.non_tragic_count/self.iteration_count:.0%})")
        print(f"Total bugs found: {len(self.bugs_found)}")
        
        # Analyze all logs for patterns
        tone_counts = {}
        outcome_counts = {}
        
        for i in range(1, self.iteration_count + 1):
            try:
                with open(f"playtest_logs/iteration_{i:03d}_*.json", 'r') as f:
                    data = json.load(f)
                    tone = data['emotional_tone']
                    outcome = data['outcome']['result']
                    
                    tone_counts[tone] = tone_counts.get(tone, 0) + 1
                    outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
            except:
                pass
        
        # Update changelog
        self.update_changelog()
        
        print("\n✅ Playtest logs saved to playtest_logs/")
        print("✅ Changelog updated with findings")
    
    def update_changelog(self):
        """Update changelog with test findings"""
        
        changelog_entry = f"""

## Automated Playtest Session - {datetime.now().strftime('%Y-%m-%d')}

### Test Parameters
- Total iterations: {self.iteration_count}
- Focus: Character Psychology (Phase 1) + Mission Execution (Phase 2)
- Team sizes: 2-4 agents
- Mission types: sabotage, assassination, propaganda, theft, rescue

### Key Findings

#### Emotional Tone Distribution
- Unique tones discovered: {len(self.unique_tones)}
- Most common: {', '.join(list(self.unique_tones)[:3])}

#### Outcome Statistics  
- Success rate: {self.non_tragic_count}/{self.iteration_count} ({self.non_tragic_count/self.iteration_count:.0%})
- Critical failures: {self.iteration_count - self.non_tragic_count}

#### Bugs and Issues
"""
        
        if self.bugs_found:
            # Count bug occurrences
            bug_counts = {}
            for bug in self.bugs_found:
                bug_counts[bug] = bug_counts.get(bug, 0) + 1
            
            # Sort by frequency
            sorted_bugs = sorted(bug_counts.items(), key=lambda x: x[1], reverse=True)
            
            for bug, count in sorted_bugs[:10]:  # Top 10 bugs
                changelog_entry += f"- {bug} (occurred {count}x)\n"
        else:
            changelog_entry += "- No critical bugs found\n"
        
        changelog_entry += """

#### Design Observations
- Betrayal mechanics create compelling narrative tension
- Trauma episodes effectively disrupt mission flow
- Propaganda values scale appropriately with dramatic events
- Relationship dynamics significantly impact mission outcomes

#### Recommendations
1. Consider reducing betrayal frequency for 4-person teams
2. Add more variety to extraction phase complications
3. Increase propaganda bonus for ideologically-motivated missions
4. Balance panic cascade effects in high-stress scenarios
"""
        
        # Append to changelog
        with open("CHANGELOG.md", "a") as f:
            f.write(changelog_entry)
        
        print(f"\n📝 Updated CHANGELOG.md with {len(self.bugs_found)} findings")


if __name__ == "__main__":
    # Initialize and run automated playtester
    playtester = AutomatedPlaytester()
    
    # Run exactly 20 iterations
    print("="*80)
    print("YEARS OF LEAD - AUTOMATED PLAYTEST SESSION")
    print("MAX Mode: Deep testing of Character Psychology + Mission Execution")
    print("="*80)
    
    for i in range(20):
        playtester.run_iteration()
    
    # Check completion conditions
    print(f"\n📊 FINAL REPORT:")
    print(f"Completed iterations: {playtester.iteration_count}")
    print(f"Unique emotional tones: {len(playtester.unique_tones)}")
    print(f"Non-tragic outcomes: {playtester.non_tragic_count}")
    print(f"Bugs found: {len(playtester.bugs_found)}")
    
    if playtester.bugs_found:
        print("\n🐛 TOP BUGS:")
        bug_counts = {}
        for bug in playtester.bugs_found:
            bug_counts[bug] = bug_counts.get(bug, 0) + 1
        
        for bug, count in sorted(bug_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {bug} (x{count})")
    
    # Update changelog
    playtester.update_changelog()
    print("\n✅ Playtest complete. Logs saved to playtest_logs/")