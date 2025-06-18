#!/usr/bin/env python3
"""
Years of Lead - Character Creation Demo

Run the interactive character creation system to create custom characters
for the Years of Lead insurgency simulator.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from game.character_creation_ui import CharacterCreationUI
from game.character_creation import create_random_character


def main():
    """Run the character creation demo"""
    print("🎮 Years of Lead - Character Creation System")
    print("=" * 60)
    print()
    print("Choose an option:")
    print("1. Interactive Character Creation (Full Experience)")
    print("2. Quick Random Character Generation")
    print("3. View Random Character Examples")
    print("4. Exit")
    print()

    while True:
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            # Full interactive character creation
            ui = CharacterCreationUI()
            character = ui.run_character_creation()

            if character:
                print("\n🎉 Character Creation Complete!")
                print(character.get_character_summary())
                print("\n📖 Character Story:")
                print(character.get_character_story())

                # Ask if they want to save
                save_choice = (
                    input("\nWould you like to save this character? (y/n): ")
                    .strip()
                    .lower()
                )
                if save_choice in ["y", "yes"]:
                    # Save character (you could extend this to save to file)
                    print(f"✅ Character '{character.name}' saved successfully!")
            break

        elif choice == "2":
            # Quick character creation
            name = input("Enter character name (or press Enter for random): ").strip()
            if not name:
                name = None

            ui = CharacterCreationUI()
            character = ui.quick_create_character(name)

            print("\n🎉 Quick Character Created!")
            print(character.get_character_summary())
            print("\n📖 Character Story:")
            print(character.get_character_story())
            break

        elif choice == "3":
            # Show examples
            print("\n🎭 Generating 3 Random Character Examples:")
            print("=" * 60)

            example_names = ["Elena Rodriguez", "Marcus Chen", "Sofia Petrov"]
            for i, name in enumerate(example_names, 1):
                print(f"\n--- EXAMPLE {i}: {name.upper()} ---")
                character = create_random_character(name)
                print(f"Background: {character.background.name}")
                print(f"Personality: {character.traits.get_trait_description()}")
                print(
                    f"Primary Skills: Combat({character.skills.combat}) Social({character.skills.social}) Stealth({character.skills.stealth})"
                )
                print(f"Motivation: {character.motivation.primary_motivation}")
                if character.trauma:
                    print(
                        f"Trauma: {character.trauma.type.value.replace('_', ' ').title()}"
                    )
                print(f"Story: {character.get_character_story()[:150]}...")

            input("\nPress Enter to return to menu...")
            continue

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
