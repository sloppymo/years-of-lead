#!/usr/bin/env python3
"""
Years of Lead - Character Integration Demo

This demonstrates how to create characters using the character creation system
and integrate them into the main Years of Lead game.
"""

import sys
import os
import random

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game.character_creation_ui import CharacterCreationUI
from game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait
from game.core import GameState, Agent
from game.entities import SkillType, Skill
from game.emotional_state import EmotionalState


class CharacterGameIntegrator:
    """Integrates character creation system with main game"""
    
    def __init__(self):
        self.character_creator = CharacterCreationUI()
        self.game_state = GameState()
        self.game_state.initialize_game()
    
    def convert_character_to_agent(self, character, faction_id="resistance", location_id="university"):
        """Convert a Character from character creation to an Agent for the main game"""
        
        # Create the agent with basic info
        agent = Agent(
            id=character.id,
            name=character.name,
            faction_id=faction_id,
            location_id=location_id,
            background=character.background.type.value,
            loyalty=int(character.motivation.ideological_commitment * 100),
            stress=max(0, int(character.emotional_state.trauma_level * 100))
        )
        
        # Convert character skills to agent skills
        skill_mapping = {
            'combat': SkillType.COMBAT,
            'stealth': SkillType.STEALTH,
            'hacking': SkillType.HACKING,
            'social': SkillType.PERSUASION,  # Map social to persuasion
            'technical': SkillType.DEMOLITIONS,  # Map technical to demolitions
            'medical': SkillType.INTELLIGENCE,  # Map medical to intelligence (closest match)
            'survival': SkillType.STEALTH,  # Map survival to stealth (closest match)
            'intelligence': SkillType.INTELLIGENCE
        }
        
        # Add skills to agent
        for char_skill, agent_skill in skill_mapping.items():
            skill_level = getattr(character.skills, char_skill, 1)
            agent.skills[agent_skill] = Skill(level=skill_level)
        
        # Copy emotional state
        agent.emotional_state = character.emotional_state
        agent.emotion_state = {
            'trust': character.emotional_state.trust,
            'anticipation': character.emotional_state.anticipation, 
            'joy': character.emotional_state.joy,
            'anger': character.emotional_state.anger,
            'fear': character.emotional_state.fear,
            'sadness': character.emotional_state.sadness,
            'surprise': character.emotional_state.surprise,
            'disgust': character.emotional_state.disgust
        }
        
        # Add character-specific traits as tags
        agent.social_tags = []
        for trait in character.traits.get_all_traits():
            agent.social_tags.append(trait.value)
        
        # Add trauma information if exists
        if character.trauma:
            agent.trauma_level = character.trauma.severity
            agent.social_tags.append(f"trauma_{character.trauma.type.value}")
        
        # Set ideology based on background and traits
        agent.ideology_vector = self._create_ideology_from_character(character)
        
        # Copy voice configuration for narrative
        if character.voice_config:
            agent.voice_config = character.voice_config
        
        return agent
    
    def _create_ideology_from_character(self, character):
        """Create ideology vector based on character background and traits"""
        ideology = {
            'radical': 0.5,
            'pacifist': 0.5,
            'individualist': 0.5,
            'traditional': 0.5,
            'nationalist': 0.3,  # Most resistance members are less nationalist
            'materialist': 0.5
        }
        
        # Adjust based on background
        background_modifiers = {
            BackgroundType.ACADEMIC: {'radical': 0.2, 'individualist': 0.3, 'traditional': -0.2},
            BackgroundType.MILITARY: {'traditional': 0.4, 'radical': -0.2, 'pacifist': -0.4},
            BackgroundType.CRIMINAL: {'individualist': 0.4, 'traditional': -0.3, 'materialist': 0.3},
            BackgroundType.CORPORATE: {'materialist': 0.4, 'individualist': 0.3, 'radical': -0.2},
            BackgroundType.MEDICAL: {'pacifist': 0.4, 'traditional': 0.2, 'radical': -0.1},
            BackgroundType.TECHNICAL: {'individualist': 0.3, 'radical': 0.2, 'traditional': -0.2},
            BackgroundType.JOURNALIST: {'radical': 0.3, 'individualist': 0.2, 'traditional': -0.2},
            BackgroundType.RELIGIOUS: {'traditional': 0.5, 'pacifist': 0.3, 'materialist': -0.4},
            BackgroundType.ACTIVIST: {'radical': 0.5, 'pacifist': 0.2, 'individualist': -0.2},
            BackgroundType.LABORER: {'materialist': 0.3, 'traditional': 0.2, 'radical': 0.2}
        }
        
        if character.background.type in background_modifiers:
            for key, modifier in background_modifiers[character.background.type].items():
                ideology[key] = max(-1.0, min(1.0, ideology[key] + modifier))
        
        # Adjust based on personality traits
        trait_modifiers = {
            PersonalityTrait.IDEALISTIC: {'radical': 0.3, 'pacifist': 0.2},
            PersonalityTrait.PRAGMATIC: {'radical': -0.2, 'materialist': 0.2},
            PersonalityTrait.CAUTIOUS: {'radical': -0.3, 'traditional': 0.2},
            PersonalityTrait.RECKLESS: {'radical': 0.4, 'individualist': 0.2},
            PersonalityTrait.COMPASSIONATE: {'pacifist': 0.4, 'materialist': -0.2},
            PersonalityTrait.RUTHLESS: {'pacifist': -0.4, 'radical': 0.3},
            PersonalityTrait.LEADER: {'individualist': 0.2, 'radical': 0.2},
            PersonalityTrait.FOLLOWER: {'traditional': 0.3, 'individualist': -0.2}
        }
        
        for trait in character.traits.get_all_traits():
            if trait in trait_modifiers:
                for key, modifier in trait_modifiers[trait].items():
                    ideology[key] = max(-1.0, min(1.0, ideology[key] + modifier))
        
        return ideology
    
    def add_character_to_game(self, character, faction_id="resistance", location_id="university_district"):
        """Add a character to the active game"""
        
        # Convert character to agent
        agent = self.convert_character_to_agent(character, faction_id, location_id)
        
        # Add to game state
        self.game_state.add_agent(agent)
        
        # Generate welcome narrative
        welcome_message = f"{character.name} joins the resistance as a {character.background.name.lower()}."
        self.game_state.recent_narrative.append(welcome_message)
        
        # Add character story to narrative
        if character.trauma:
            trauma_message = f"{character.name} carries the scars of {character.trauma.type.value.replace('_', ' ').lower()}."
            self.game_state.recent_narrative.append(trauma_message)
        
        return agent
    
    def demonstrate_integration(self):
        """Run a complete integration demonstration"""
        
        print("🎮 YEARS OF LEAD - CHARACTER INTEGRATION DEMO")
        print("=" * 60)
        
        # Show initial game state
        print("\n📊 INITIAL GAME STATE:")
        print(f"Active Agents: {len(self.game_state.agents)}")
        for agent_id, agent in self.game_state.agents.items():
            print(f"  • {agent.name} ({agent.background}) - Faction: {agent.faction_id}")
        
        print("\n🎭 Creating Custom Character...")
        
        # Create a custom character
        custom_char = self.character_creator.quick_create_character("Alex Rivera")
        
        print(f"\n✅ Character Created: {custom_char.name}")
        print(f"Background: {custom_char.background.name}")
        print(f"Personality: {custom_char.traits.get_trait_description()}")
        print(f"Primary Skills: Combat({custom_char.skills.combat}) Social({custom_char.skills.social}) Stealth({custom_char.skills.stealth})")
        
        # Add character to game
        print(f"\n🔗 Adding {custom_char.name} to the game...")
        
        agent = self.add_character_to_game(custom_char, "resistance", "university_district")
        
        print(f"✅ {custom_char.name} successfully integrated!")
        
        # Show updated game state
        print("\n📊 UPDATED GAME STATE:")
        print(f"Active Agents: {len(self.game_state.agents)}")
        for agent_id, agent in self.game_state.agents.items():
            if agent.id == custom_char.id:
                print(f"  🆕 {agent.name} ({agent.background}) - Faction: {agent.faction_id} [NEW!]")
            else:
                print(f"     {agent.name} ({agent.background}) - Faction: {agent.faction_id}")
        
        # Show character's skills integrated into game
        print(f"\n🛠️  {custom_char.name}'s Skills in Game:")
        for skill_type, skill in agent.skills.items():
            print(f"  • {skill_type.value.title()}: Level {skill.level}")
        
        # Show emotional state
        print(f"\n💭 {custom_char.name}'s Emotional State:")
        for emotion, value in agent.emotion_state.items():
            print(f"  • {emotion.title()}: {value:.2f}")
        
        # Show ideology
        print(f"\n🎯 {custom_char.name}'s Ideology:")
        for ideology, value in agent.ideology_vector.items():
            print(f"  • {ideology.title()}: {value:.2f}")
        
        # Show recent narrative including the character
        print(f"\n📖 Recent Game Narrative:")
        for narrative in self.game_state.recent_narrative[-5:]:
            if custom_char.name in narrative:
                print(f"  🆕 {narrative}")
            else:
                print(f"     {narrative}")
        
        # Demonstrate character in action
        print(f"\n⚡ Simulating {custom_char.name} in Action...")
        
        # Advance one turn to see character participate
        original_turn = self.game_state.turn_number
        self.game_state.advance_turn()
        
        print(f"✅ Turn advanced from {original_turn} to {self.game_state.turn_number}")
        
        # Show how the character participated
        print(f"\n📋 Turn {self.game_state.turn_number} Results:")
        for narrative in self.game_state.recent_narrative[-3:]:
            print(f"  • {narrative}")
        
        return agent


def main():
    """Main demonstration function"""
    
    print("Choose integration demo:")
    print("1. Quick Integration Demo (Automated)")
    print("2. Create Custom Character + Integrate") 
    print("3. Multiple Character Integration")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    integrator = CharacterGameIntegrator()
    
    if choice == "1":
        # Quick automated demo
        integrator.demonstrate_integration()
        
    elif choice == "2":
        # Interactive character creation + integration
        print("\n🎭 Starting Interactive Character Creation...")
        character = integrator.character_creator.run_character_creation()
        
        if character:
            print(f"\n🔗 Integrating {character.name} into the game...")
            agent = integrator.add_character_to_game(character)
            
            print("\n✅ Integration Complete!")
            print(character.get_character_summary())
            
            # Show in-game status
            print(f"\n🎮 {character.name} is now active in the game!")
            print(f"Faction: {agent.faction_id}")
            print(f"Location: {agent.location_id}")
            print(f"Stress Level: {agent.stress}")
            print(f"Loyalty: {agent.loyalty}")
        
    elif choice == "3":
        # Multiple character integration
        print("\n🎭 Creating Multiple Characters...")
        
        characters = []
        names = ["Elena Vasquez", "Marcus Johnson", "Sofia Chen"]
        
        for name in names:
            char = integrator.character_creator.quick_create_character(name)
            characters.append(char)
            print(f"✅ Created {char.name} ({char.background.name})")
        
        print(f"\n🔗 Integrating {len(characters)} characters into game...")
        
        factions = ["resistance", "urban_liberation", "underground"]
        
        for i, character in enumerate(characters):
            faction = factions[i % len(factions)]
            agent = integrator.add_character_to_game(character, faction)
            print(f"✅ {character.name} joined {faction}")
        
        print(f"\n📊 Final Game State: {len(integrator.game_state.agents)} agents")
        
    elif choice == "4":
        print("👋 Goodbye!")
        return
    
    else:
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main() 