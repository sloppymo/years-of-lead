#!/usr/bin/env python3
"""Show character creation features"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game.character_creation_ui import CharacterCreationUI
from game.character_creation import CharacterCreator, BackgroundType, PersonalityTrait

# Create a character creation UI
ui = CharacterCreationUI()

# Show what backgrounds are available
print('🎯 AVAILABLE BACKGROUNDS:')
print('=' * 50)
for i, bg_type in enumerate(BackgroundType, 1):
    bg = ui.creator.backgrounds[bg_type]
    print(f'{i:2d}. {bg.name:12s} - {bg.description}')

print('\n🎭 AVAILABLE PERSONALITY TRAITS:')
print('=' * 50)
for i, trait in enumerate(PersonalityTrait, 1):
    name = trait.value.replace('_', ' ').title()
    print(f'{i:2d}. {name}')

print('\n🛠️  CHARACTER CREATION FEATURES:')
print('=' * 50)
print('✅ 10 detailed backgrounds with unique bonuses')
print('✅ 16 personality traits that affect behavior')
print('✅ 8 skill categories (Combat, Stealth, Hacking, etc.)')
print('✅ Dynamic trauma system with 10 trauma types')
print('✅ Complex emotional state modeling')
print('✅ Voice configuration for narrative tone')
print('✅ Starting resources and connections')
print('✅ Comprehensive character backstories')
print('✅ Interactive step-by-step creation process')
print('✅ Character validation and confirmation')

print('\n📊 DETAILED BACKGROUND EXAMPLE: MILITARY')
print('=' * 50)
ui.display_background_details(BackgroundType.MILITARY) 