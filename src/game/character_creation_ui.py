"""
Years of Lead - Character Creation UI

Interactive character creation interface that integrates with the existing
Years of Lead menu system and game state.
"""

import os
import sys
import getpass
from typing import List, Tuple, Optional, Dict, Any
from .character_creation import (
    CharacterCreator, Character, BackgroundType, PersonalityTrait,
    SkillCategory, CharacterSkills, CharacterTraits, CharacterMotivation
)


class CharacterCreationUI:
    """Interactive character creation interface"""

    def __init__(self):
        self.creator = CharacterCreator()
        self.current_character = None
        self.creation_steps = [
            "name",
            "background",
            "primary_trait",
            "secondary_trait",
            "skills",
            "review"
        ]
        self.current_step = 0
        self.character_data = {}

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_banner(self):
        """Print the character creation banner"""
        print("=" * 80)
        print("""
 ██████╗██╗  ██╗ █████╗ ██████╗ ███████╗ █████╗  ██████╗ ████████╗███████╗██████╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔══██╗
██║     ███████║███████║██████╔╝█████╗  ███████║██║   ██║   ██║   █████╗  ██████╔╝
██║     ██╔══██║██╔══██║██╔══██╗██╔══╝  ██╔══██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
╚██████╗██║  ██║██║  ██║██║  ██║███████╗██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝

                           Character Creation System
""")
        print("=" * 80)

    def print_progress(self):
        """Print creation progress"""
        step_names = {
            "name": "Character Name",
            "background": "Background Selection",
            "primary_trait": "Primary Personality",
            "secondary_trait": "Secondary Personality",
            "skills": "Skill Allocation",
            "review": "Final Review"
        }

        current_step_name = step_names.get(self.creation_steps[self.current_step], "Unknown")
        print(f"\nStep {self.current_step + 1} of {len(self.creation_steps)}: {current_step_name}")
        print("-" * 50)

    def confirm_choice(self, prompt: str, choice: str) -> bool:
        """Ask user to confirm their choice"""
        print(f"\n{'-' * 60}")
        print(f"CONFIRMATION: {prompt}")
        print(f"Your choice: {choice}")
        print(f"{'-' * 60}")

        while True:
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def get_name_input(self) -> str:
        """Get character name from user with confirmation"""
        while True:
            print("\nEnter your character's name:")
            print("(The name will be hidden as you type for security)")
            name = getpass.getpass("Name: ").strip()

            if not name:
                print("Name cannot be empty. Please try again.")
                continue

            # Show the name and confirm
            print(f"\nYou entered: {name}")
            if self.confirm_choice("Character Name", name):
                return name
            else:
                print("Let's try again...")

    def get_background_details(self, bg_type: BackgroundType) -> Dict[str, Any]:
        """Get detailed information about a background"""
        background = self.creator.backgrounds[bg_type]

        details = {
            "name": background.name,
            "description": background.description,
            "story": background.get_background_story("Your Character"),
            "skill_bonuses": background.skill_bonuses,
            "starting_resources": background.starting_resources,
            "connections": background.connections,
            "trauma_risk": background.trauma_risk,
            "mechanical_effects": self._get_background_mechanics(bg_type),
            "narrative_consequences": self._get_background_narrative(bg_type)
        }

        return details

    def _get_background_mechanics(self, bg_type: BackgroundType) -> Dict[str, str]:
        """Get mechanical effects of background choices"""
        mechanics = {
            BackgroundType.MILITARY: {
                "combat_bonus": "+2 Combat, +1 Survival",
                "resource_bonus": "Access to military equipment",
                "special_ability": "Can train other operatives in combat",
                "heat_penalty": "Higher suspicion from authorities"
            },
            BackgroundType.TECHNICAL: {
                "technical_bonus": "+2 Technical, +1 Hacking",
                "resource_bonus": "Access to technical equipment",
                "special_ability": "Can hack security systems",
                "heat_penalty": "Monitored by tech companies"
            },
            BackgroundType.MEDICAL: {
                "medical_bonus": "+2 Medical, +1 Intelligence",
                "resource_bonus": "Access to medical supplies",
                "special_ability": "Can heal injured operatives",
                "heat_penalty": "Monitored by health authorities"
            },
            BackgroundType.CRIMINAL: {
                "stealth_bonus": "+2 Stealth, +1 Social",
                "resource_bonus": "Access to black market",
                "special_ability": "Can gather intelligence from criminal networks",
                "heat_penalty": "Already known to police"
            },
            BackgroundType.ACADEMIC: {
                "intelligence_bonus": "+2 Intelligence, +1 Technical",
                "resource_bonus": "Access to research facilities",
                "special_ability": "Can analyze complex information",
                "heat_penalty": "Monitored by academic institutions"
            },
            BackgroundType.CORPORATE: {
                "social_bonus": "+2 Social, +1 Intelligence",
                "resource_bonus": "Access to corporate resources",
                "special_ability": "Can infiltrate corporate targets",
                "heat_penalty": "Monitored by corporate security"
            },
            BackgroundType.JOURNALIST: {
                "social_bonus": "+2 Social, +1 Intelligence",
                "resource_bonus": "Access to media contacts",
                "special_ability": "Can spread propaganda effectively",
                "heat_penalty": "Monitored by media companies"
            },
            BackgroundType.RELIGIOUS: {
                "social_bonus": "+2 Social, +1 Medical",
                "resource_bonus": "Access to community networks",
                "special_ability": "Can recruit from religious communities",
                "heat_penalty": "Monitored by religious authorities"
            },
            BackgroundType.ACTIVIST: {
                "social_bonus": "+2 Social, +1 Stealth",
                "resource_bonus": "Access to activist networks",
                "special_ability": "Can organize protests and demonstrations",
                "heat_penalty": "Already on watch lists"
            },
            BackgroundType.LABORER: {
                "survival_bonus": "+2 Survival, +1 Technical",
                "resource_bonus": "Access to industrial areas",
                "special_ability": "Can sabotage industrial targets",
                "heat_penalty": "Monitored by labor unions"
            }
        }

        return mechanics.get(bg_type, {})

    def _get_background_narrative(self, bg_type: BackgroundType) -> Dict[str, str]:
        """Get narrative consequences of background choices"""
        narrative = {
            BackgroundType.MILITARY: {
                "personal_conflicts": "Struggles with following orders vs. personal morality",
                "relationships": "May have former comrades who could help or betray",
                "psychological_impact": "Combat experience affects decision-making",
                "future_opportunities": "Can access military intelligence and equipment"
            },
            BackgroundType.TECHNICAL: {
                "personal_conflicts": "Balancing technical solutions with human costs",
                "relationships": "Network of tech professionals and hackers",
                "psychological_impact": "Analytical thinking may override emotional concerns",
                "future_opportunities": "Can develop advanced surveillance and communication systems"
            },
            BackgroundType.MEDICAL: {
                "personal_conflicts": "Hippocratic oath vs. revolutionary violence",
                "relationships": "Network of medical professionals and patients",
                "psychological_impact": "Deep empathy may lead to hesitation in violent situations",
                "future_opportunities": "Can provide medical support and access to restricted areas"
            },
            BackgroundType.CRIMINAL: {
                "personal_conflicts": "Criminal past vs. revolutionary ideals",
                "relationships": "Complex network of criminals, some trustworthy, some not",
                "psychological_impact": "Street-smart but may struggle with trust",
                "future_opportunities": "Can access black market and criminal intelligence"
            },
            BackgroundType.ACADEMIC: {
                "personal_conflicts": "Intellectual analysis vs. direct action",
                "relationships": "Network of academics and researchers",
                "psychological_impact": "May overthink situations and hesitate",
                "future_opportunities": "Can access research facilities and academic networks"
            },
            BackgroundType.CORPORATE: {
                "personal_conflicts": "Corporate success vs. revolutionary goals",
                "relationships": "Network of business contacts and former colleagues",
                "psychological_impact": "May be accustomed to working within systems",
                "future_opportunities": "Can infiltrate corporate targets and access resources"
            },
            BackgroundType.JOURNALIST: {
                "personal_conflicts": "Objectivity vs. advocacy for the cause",
                "relationships": "Network of media contacts and sources",
                "psychological_impact": "May feel compelled to document everything",
                "future_opportunities": "Can spread propaganda and gather intelligence"
            },
            BackgroundType.RELIGIOUS: {
                "personal_conflicts": "Religious faith vs. revolutionary violence",
                "relationships": "Network of religious community members",
                "psychological_impact": "May seek divine guidance in difficult decisions",
                "future_opportunities": "Can recruit from religious communities and access facilities"
            },
            BackgroundType.ACTIVIST: {
                "personal_conflicts": "Peaceful protest vs. armed resistance",
                "relationships": "Network of activists and community organizers",
                "psychological_impact": "May be idealistic but inexperienced with violence",
                "future_opportunities": "Can organize mass actions and recruit from activist circles"
            },
            BackgroundType.LABORER: {
                "personal_conflicts": "Working class solidarity vs. individual survival",
                "relationships": "Network of workers and union members",
                "psychological_impact": "May be practical and focused on immediate needs",
                "future_opportunities": "Can access industrial areas and organize workers"
            }
        }

        return narrative.get(bg_type, {})

    def display_background_details(self, bg_type: BackgroundType):
        """Display detailed background information"""
        details = self.get_background_details(bg_type)

        print(f"\n{'=' * 60}")
        print(f"BACKGROUND: {details['name'].upper()}")
        print(f"{'=' * 60}")

        print(f"\n📖 DESCRIPTION:")
        print(f"{details['description']}")

        print(f"\n📚 PERSONAL STORY:")
        print(f"{details['story']}")

        print(f"\n⚔️  MECHANICAL EFFECTS:")
        mechanics = details['mechanical_effects']
        for key, value in mechanics.items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")

        print(f"\n🎭 NARRATIVE CONSEQUENCES:")
        narrative = details['narrative_consequences']
        for key, value in narrative.items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")

        print(f"\n💰 STARTING RESOURCES:")
        for resource, amount in details['starting_resources'].items():
            print(f"  • {resource.title()}: {amount}")

        print(f"\n🔗 CONNECTIONS:")
        for connection in details['connections']:
            print(f"  • {connection}")

        print(f"\n⚠️  TRAUMA RISKS:")
        for trauma in details['trauma_risk']:
            print(f"  • {trauma.value.replace('_', ' ').title()}")

    def select_background(self) -> BackgroundType:
        """Interactive background selection with detailed information"""
        backgrounds = list(BackgroundType)
        selected = None

        while selected is None:
            print("\nSelect your character's background:")
            print("-" * 40)

            for i, bg_type in enumerate(backgrounds, 1):
                background = self.creator.backgrounds[bg_type]
                print(f"{i:2d}. {background.name}")

            print(f"\n{len(backgrounds) + 1:2d}. View detailed information")
            print(" 0. Back to previous step")

            try:
                choice = int(input(f"\nEnter choice (0-{len(backgrounds) + 1}): "))

                if choice == 0:
                    return None  # Go back
                elif 1 <= choice <= len(backgrounds):
                    bg_type = backgrounds[choice - 1]
                    background = self.creator.backgrounds[bg_type]

                    if self.confirm_choice("Background Selection", background.name):
                        selected = bg_type
                    else:
                        print("Let's try again...")

                elif choice == len(backgrounds) + 1:
                    # Show detailed information
                    print("\nWhich background would you like to learn more about?")
                    for i, bg_type in enumerate(backgrounds, 1):
                        background = self.creator.backgrounds[bg_type]
                        print(f"{i:2d}. {background.name}")

                    try:
                        detail_choice = int(input(f"\nEnter choice (1-{len(backgrounds)}): "))
                        if 1 <= detail_choice <= len(backgrounds):
                            self.display_background_details(backgrounds[detail_choice - 1])
                            input("\nPress Enter to continue...")
                            self.clear_screen()
                            self.print_banner()
                            self.print_progress()
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Please enter a valid number.")

                else:
                    print(f"Please enter a number between 0 and {len(backgrounds) + 1}")
            except ValueError:
                print("Please enter a valid number")

        return selected

    def get_trait_details(self, trait: PersonalityTrait) -> Dict[str, str]:
        """Get detailed information about a personality trait"""
        details = {
            PersonalityTrait.IDEALISTIC: {
                "description": "Driven by strong moral convictions and principles",
                "mechanical_effects": "+2 to recruitment rolls, -1 to pragmatic decisions",
                "narrative_impact": "May refuse morally questionable missions",
                "relationships": "Inspires others but may be seen as naive",
                "conflicts": "Struggles with necessary compromises"
            },
            PersonalityTrait.PRAGMATIC: {
                "description": "Focused on practical results over ideology",
                "mechanical_effects": "+2 to survival rolls, -1 to morale checks",
                "narrative_impact": "Willing to make hard choices for the cause",
                "relationships": "Respected for effectiveness but may seem cold",
                "conflicts": "May alienate more idealistic comrades"
            },
            PersonalityTrait.CAUTIOUS: {
                "description": "Careful and methodical in approach",
                "mechanical_effects": "+2 to stealth rolls, -1 to initiative",
                "narrative_impact": "Prefers planning over direct action",
                "relationships": "Trusted for reliability but may seem slow",
                "conflicts": "May miss opportunities due to over-planning"
            },
            PersonalityTrait.RECKLESS: {
                "description": "Willing to take bold risks",
                "mechanical_effects": "+2 to combat rolls, -1 to stealth",
                "narrative_impact": "May charge into dangerous situations",
                "relationships": "Inspiring in combat but may endanger others",
                "conflicts": "May put comrades at unnecessary risk"
            },
            PersonalityTrait.COMPASSIONATE: {
                "description": "Deeply concerned with others' welfare",
                "mechanical_effects": "+2 to medical rolls, -1 to ruthless decisions",
                "narrative_impact": "May hesitate to harm enemies",
                "relationships": "Beloved by comrades but may be exploited",
                "conflicts": "Struggles with necessary violence"
            },
            PersonalityTrait.RUTHLESS: {
                "description": "Willing to make hard choices",
                "mechanical_effects": "+2 to intimidation rolls, -1 to trust",
                "narrative_impact": "May use extreme methods",
                "relationships": "Feared and respected but not loved",
                "conflicts": "May alienate more compassionate comrades"
            },
            PersonalityTrait.ANALYTICAL: {
                "description": "Thinks through problems systematically",
                "mechanical_effects": "+2 to intelligence rolls, -1 to social",
                "narrative_impact": "May overthink situations",
                "relationships": "Valued for planning but may seem cold",
                "conflicts": "May miss emotional aspects of situations"
            },
            PersonalityTrait.INTUITIVE: {
                "description": "Relies on gut feelings and instincts",
                "mechanical_effects": "+2 to surprise rolls, -1 to planning",
                "narrative_impact": "May make snap decisions",
                "relationships": "Trusted instincts but may seem unpredictable",
                "conflicts": "May ignore logical planning"
            },
            PersonalityTrait.LOYAL: {
                "description": "Devoted to comrades and cause",
                "mechanical_effects": "+2 to morale rolls, -1 to betrayal resistance",
                "narrative_impact": "May be too trusting of allies",
                "relationships": "Beloved by comrades but vulnerable to betrayal",
                "conflicts": "May ignore warning signs about allies"
            },
            PersonalityTrait.OPPORTUNISTIC: {
                "description": "Adapts quickly to changing situations",
                "mechanical_effects": "+2 to flexibility rolls, -1 to consistency",
                "narrative_impact": "May change plans frequently",
                "relationships": "Valued for adaptability but may seem unreliable",
                "conflicts": "May seem inconsistent to comrades"
            },
            PersonalityTrait.LEADER: {
                "description": "Naturally takes charge in groups",
                "mechanical_effects": "+2 to leadership rolls, -1 to following orders",
                "narrative_impact": "May challenge authority",
                "relationships": "Natural leader but may conflict with other leaders",
                "conflicts": "May struggle with being subordinate"
            },
            PersonalityTrait.FOLLOWER: {
                "description": "Prefers to support others' leadership",
                "mechanical_effects": "+2 to teamwork rolls, -1 to initiative",
                "narrative_impact": "May hesitate to take charge",
                "relationships": "Reliable team player but may lack initiative",
                "conflicts": "May not step up when needed"
            },
            PersonalityTrait.OPTIMISTIC: {
                "description": "Maintains hope even in dark times",
                "mechanical_effects": "+2 to morale rolls, -1 to realistic assessment",
                "narrative_impact": "May underestimate dangers",
                "relationships": "Inspiring to others but may seem naive",
                "conflicts": "May ignore warning signs"
            },
            PersonalityTrait.PESSIMISTIC: {
                "description": "Prepares for the worst outcomes",
                "mechanical_effects": "+2 to survival rolls, -1 to morale",
                "narrative_impact": "May be overly cautious",
                "relationships": "Valued for realism but may be depressing",
                "conflicts": "May demoralize comrades"
            },
            PersonalityTrait.CREATIVE: {
                "description": "Finds innovative solutions to problems",
                "mechanical_effects": "+2 to problem-solving rolls, -1 to routine tasks",
                "narrative_impact": "May prefer unconventional approaches",
                "relationships": "Valued for ideas but may seem impractical",
                "conflicts": "May ignore proven methods"
            },
            PersonalityTrait.METHODICAL: {
                "description": "Follows established procedures",
                "mechanical_effects": "+2 to technical rolls, -1 to improvisation",
                "narrative_impact": "May be slow to adapt",
                "relationships": "Reliable but may seem rigid",
                "conflicts": "May miss creative opportunities"
            }
        }

        return details.get(trait, {})

    def display_trait_details(self, trait: PersonalityTrait):
        """Display detailed trait information"""
        details = self.get_trait_details(trait)

        print(f"\n{'=' * 60}")
        print(f"PERSONALITY TRAIT: {trait.value.replace('_', ' ').upper()}")
        print(f"{'=' * 60}")

        print(f"\n📖 DESCRIPTION:")
        print(f"{details['description']}")

        print(f"\n⚔️  MECHANICAL EFFECTS:")
        print(f"{details['mechanical_effects']}")

        print(f"\n🎭 NARRATIVE IMPACT:")
        print(f"{details['narrative_impact']}")

        print(f"\n👥 RELATIONSHIPS:")
        print(f"{details['relationships']}")

        print(f"\n⚔️  POTENTIAL CONFLICTS:")
        print(f"{details['conflicts']}")

    def select_trait(self, trait_type: str, exclude_trait: Optional[PersonalityTrait] = None) -> PersonalityTrait:
        """Interactive trait selection with detailed information"""
        traits = list(PersonalityTrait)
        if exclude_trait:
            traits = [t for t in traits if t != exclude_trait]

        selected = None

        while selected is None:
            print(f"\nSelect your character's {trait_type} personality trait:")
            print("-" * 50)

            for i, trait in enumerate(traits, 1):
                trait_desc = trait.value.replace('_', ' ').title()
                print(f"{i:2d}. {trait_desc}")

            print(f"\n{len(traits) + 1:2d}. View detailed information")
            print(" 0. Back to previous step")

            try:
                choice = int(input(f"\nEnter choice (0-{len(traits) + 1}): "))

                if choice == 0:
                    return None  # Go back
                elif 1 <= choice <= len(traits):
                    trait = traits[choice - 1]
                    trait_desc = trait.value.replace('_', ' ').title()

                    if self.confirm_choice(f"{trait_type} Personality Trait", trait_desc):
                        selected = trait
                    else:
                        print("Let's try again...")

                elif choice == len(traits) + 1:
                    # Show detailed information
                    print(f"\nWhich {trait_type.lower()} trait would you like to learn more about?")
                    for i, trait in enumerate(traits, 1):
                        trait_desc = trait.value.replace('_', ' ').title()
                        print(f"{i:2d}. {trait_desc}")

                    try:
                        detail_choice = int(input(f"\nEnter choice (1-{len(traits)}): "))
                        if 1 <= detail_choice <= len(traits):
                            self.display_trait_details(traits[detail_choice - 1])
                            input("\nPress Enter to continue...")
                            self.clear_screen()
                            self.print_banner()
                            self.print_progress()
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Please enter a valid number.")

                else:
                    print(f"Please enter a number between 0 and {len(traits) + 1}")
            except ValueError:
                print("Please enter a valid number")

        return selected

    def allocate_skills(self) -> Dict[str, int]:
        """Interactive skill allocation with detailed explanations"""
        max_points = 20
        remaining_points = max_points
        skills = {
            'combat': 1, 'stealth': 1, 'hacking': 1, 'social': 1,
            'technical': 1, 'medical': 1, 'survival': 1, 'intelligence': 1
        }

        # Apply background bonuses first
        background = self.creator.backgrounds[self.character_data['background']]
        for skill_category, bonus in background.skill_bonuses.items():
            skills[skill_category.value] += bonus

        skill_descriptions = {
            'combat': "Fighting, weapons, tactical combat",
            'stealth': "Sneaking, hiding, avoiding detection",
            'hacking': "Computer systems, digital security, cyber warfare",
            'social': "Persuasion, recruitment, public speaking",
            'technical': "Engineering, mechanics, technical problem-solving",
            'medical': "Healing, first aid, medical knowledge",
            'survival': "Wilderness survival, resourcefulness, adaptability",
            'intelligence': "Analysis, research, strategic thinking"
        }

        print(f"\nSkill Allocation - {remaining_points} points remaining")
        print("Skills start at level 1. Maximum level is 10.")
        print("-" * 50)

        while remaining_points > 0:
            # Display current skills
            print("\nCurrent Skills:")
            for skill_name, level in skills.items():
                desc = skill_descriptions[skill_name]
                print(f"  {skill_name.title():12}: {level}/10 - {desc}")

            print(f"\nPoints remaining: {remaining_points}")

            # Get skill to increase
            skill_names = list(skills.keys())
            print("\nSkills to increase:")
            for i, skill_name in enumerate(skills.keys(), 1):
                current_level = skills[skill_name]
                if current_level < 10:
                    print(f"{i:2d}. {skill_name.title()} (currently {current_level})")

            print(f"\n{len(skill_names) + 1:2d}. View skill descriptions")
            print(" 0. Finish allocation")

            try:
                choice = int(input(f"\nSelect option (0-{len(skill_names) + 1}): "))

                if choice == 0:
                    if remaining_points > 0:
                        print(f"\nYou still have {remaining_points} points remaining.")
                        continue_choice = input("Are you sure you want to finish? (y/n): ").strip().lower()
                        if continue_choice in ['y', 'yes']:
                            break
                        else:
                            continue
                    else:
                        break

                elif 1 <= choice <= len(skill_names):
                    skill_name = skill_names[choice - 1]
                    current_level = skills[skill_name]

                    if current_level >= 10:
                        print(f"{skill_name.title()} is already at maximum level!")
                        continue

                    # Get number of points to invest
                    max_invest = min(remaining_points, 10 - current_level)
                    if max_invest == 1:
                        points_to_invest = 1
                    else:
                        points_input = input(f"How many points to invest in {skill_name.title()}? (1-{max_invest}): ")
                        try:
                            points_to_invest = int(points_input)
                            if not (1 <= points_to_invest <= max_invest):
                                print(f"Please enter a number between 1 and {max_invest}")
                                continue
                        except ValueError:
                            print("Please enter a valid number")
                            continue

                    skills[skill_name] += points_to_invest
                    remaining_points -= points_to_invest

                    print(f"\n✅ {skill_name.title()} increased to {skills[skill_name]}/10")

                    if remaining_points == 0:
                        print("\nAll points allocated!")
                        break

                elif choice == len(skill_names) + 1:
                    # Show skill descriptions
                    print(f"\n{'=' * 60}")
                    print("SKILL DESCRIPTIONS")
                    print(f"{'=' * 60}")
                    for skill_name, desc in skill_descriptions.items():
                        print(f"\n{skill_name.title()}: {desc}")
                    input("\nPress Enter to continue...")
                    self.clear_screen()
                    self.print_banner()
                    self.print_progress()

                else:
                    print(f"Please enter a number between 0 and {len(skill_names) + 1}")
            except ValueError:
                print("Please enter a valid number")

        return skills

    def review_character(self) -> bool:
        """Review character and confirm creation"""
        print("\n" + "=" * 60)
        print("CHARACTER REVIEW")
        print("=" * 60)

        # Create temporary character for review
        temp_character = self.create_character_from_data()

        # Display character summary
        print(temp_character.get_character_summary())

        print("\n" + "=" * 60)
        print("FINAL CONFIRMATION")
        print("=" * 60)

        while True:
            confirm = input("\nAre you satisfied with this character? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def create_character_from_data(self) -> Character:
        """Create character from collected data"""
        return self.creator.create_character(
            name=self.character_data['name'],
            background_type=self.character_data['background'],
            primary_trait=self.character_data['primary_trait'],
            secondary_trait=self.character_data['secondary_trait']
        )

    def run_character_creation(self) -> Optional[Character]:
        """Run the complete character creation process"""
        self.clear_screen()
        self.print_banner()

        while self.current_step < len(self.creation_steps):
            self.print_progress()

            step = self.creation_steps[self.current_step]

            if step == "name":
                name = self.get_name_input()
                if name is None:
                    continue
                self.character_data['name'] = name
                self.current_step += 1

            elif step == "background":
                background = self.select_background()
                if background is None:
                    if self.current_step > 0:
                        self.current_step -= 1
                    continue
                self.character_data['background'] = background
                self.current_step += 1

            elif step == "primary_trait":
                trait = self.select_trait("Primary")
                if trait is None:
                    if self.current_step > 0:
                        self.current_step -= 1
                    continue
                self.character_data['primary_trait'] = trait
                self.current_step += 1

            elif step == "secondary_trait":
                trait = self.select_trait("Secondary", self.character_data.get('primary_trait'))
                if trait is None:
                    if self.current_step > 0:
                        self.current_step -= 1
                    continue
                self.character_data['secondary_trait'] = trait
                self.current_step += 1

            elif step == "skills":
                skills = self.allocate_skills()
                self.character_data['skills'] = skills
                self.current_step += 1

            elif step == "review":
                if self.review_character():
                    self.current_step += 1
                else:
                    # Go back to previous step
                    self.current_step -= 1
                    continue

        # Create final character
        if self.current_step >= len(self.creation_steps):
            character = self.create_character_from_data()
            print(f"\n🎉 Character '{character.name}' created successfully!")
            return character

        return None

    def quick_create_character(self, name: str = None) -> Character:
        """Quick character creation for testing"""
        if name is None:
            name = input("Enter character name: ").strip()

        return self.creator.create_character(
            name=name,
            background_type=BackgroundType.MILITARY,
            primary_trait=PersonalityTrait.LOYAL,
            secondary_trait=PersonalityTrait.PRAGMATIC
        )


class CharacterManagementUI:
    """Character management interface"""

    def __init__(self):
        self.characters = []

    def add_character(self, character: Character):
        """Add a character to the roster"""
        self.characters.append(character)

    def list_characters(self):
        """List all characters"""
        if not self.characters:
            print("No characters in roster.")
            return

        print("\nCHARACTER ROSTER")
        print("=" * 50)
        for i, character in enumerate(self.characters, 1):
            print(f"{i:2d}. {character.name} - {character.background.name}")
            print(f"    {character.traits.get_trait_description()}")
            print()

    def view_character(self, character_index: int):
        """View detailed character information"""
        if 1 <= character_index <= len(self.characters):
            character = self.characters[character_index - 1]
            print(character.get_character_summary())
        else:
            print("Invalid character index.")

    def select_character(self) -> Optional[Character]:
        """Select a character from the roster"""
        if not self.characters:
            print("No characters available.")
            return None

        self.list_characters()

        while True:
            try:
                choice = int(input(f"\nSelect character (1-{len(self.characters)}): "))
                if 1 <= choice <= len(self.characters):
                    return self.characters[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(self.characters)}")
            except ValueError:
                print("Please enter a valid number")


def integrate_with_main_menu():
    """Integration function for main menu"""

    def character_creation_menu():
        """Character creation menu option"""
        creator = CharacterCreationUI()
        character = creator.run_character_creation()

        if character:
            manager = CharacterManagementUI()
            manager.add_character(character)
            print(f"\nCharacter '{character.name}' added to roster!")

        return character

    return character_creation_menu


if __name__ == "__main__":
    # Test the character creation system
    print("Testing Character Creation UI")
    print("=" * 50)

    # Test quick creation
    ui = CharacterCreationUI()
    character = ui.quick_create_character("Test Character")
    print(character.get_character_summary())

    # Test management
    mgmt = CharacterManagementUI()
    mgmt.add_character(character)
    mgmt.list_characters()