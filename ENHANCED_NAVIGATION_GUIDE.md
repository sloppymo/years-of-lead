# Years of Lead: Enhanced Navigation Guide

## Overview

The Years of Lead CLI has been enhanced with modern navigation features while maintaining the Dwarf Fortress-inspired interface. This guide explains how to use the new arrow key and mouse click navigation alongside the existing keyboard shortcuts.

## Navigation Methods

### 1. Keyboard Shortcuts (Original)

The original single-key shortcuts remain fully functional:

- `a` - Advance Turn/Phase
- `g` - Show Agent Details
- `n` - Show Full Narrative Log
- `l` - Show Location Details
- `e` - Show Active Events
- `m` - Show Active Missions
- `p` - Show Public Opinion
- `s` - Save/Load Game
- `i` - Inventory & Storage
- `u` - Equipment Management
- `b` - Mission Briefing & Planning
- `c` - Character Creation & Management
- `r` - Agent Relationships & Network
- `y` - Dynamic Narrative System
- `d` - Search & Detection Encounters
- `v` - Show Victory Conditions
- `q` - Quit Game
- `?` - Context Help
- `*` - Toggle Query Mode

### 2. Arrow Key Navigation (New)

Arrow keys can now be used to navigate through menus:

- `↑` (Up Arrow) - Move selection up
- `↓` (Down Arrow) - Move selection down
- `Enter` - Execute the selected command
- `Esc` - Go back to previous menu (where applicable)

The currently selected menu item is highlighted with a `→` arrow indicator.

### 3. Mouse Click Navigation (New)

Mouse support has been added for point-and-click navigation:

- **Single Click** - Select a menu item
- **Double Click** - Execute the selected command
- **Click on Back/Return options** - Navigate to previous menus

## Enhanced UI Elements

### Visual Selection Indicators

- The currently selected menu item is highlighted with a `→` arrow
- The selection is visually distinct to make navigation clearer

### Navigation Help

- Navigation instructions are displayed at the bottom of menus
- Shows available navigation methods (keyboard shortcuts, arrow keys, mouse)

### Breadcrumb Navigation

- Your current location in the menu hierarchy is displayed as a path
- Example: `📍 Path: Main Menu > Missions > Planning`

### Context-Sensitive Help

- Press `?` at any time to see context-specific help for the current menu
- Shows available commands and their functions

## Navigation Examples

### Main Menu Navigation

1. **Keyboard Shortcut**: Press `g` to directly access Agent Details
2. **Arrow Keys**: Press `↓` twice to highlight "agents", then press `Enter`
3. **Mouse**: Click on the "agents" menu item

### Save/Load Menu Navigation

1. **Keyboard Shortcut**: Press `s` to access the Save/Load menu
2. **Arrow Keys**:
   - Press `↓` to highlight "Load Game"
   - Press `Enter` to see available saves
   - Use `↑`/`↓` to select a save
   - Press `Enter` to load the selected save
3. **Mouse**:
   - Click on "Load Game"
   - Click on the save you want to load

### Query Mode Navigation

1. **Keyboard Shortcut**: Press `*` to toggle Query Mode
2. **With Query Mode Active**:
   - Click on objects in the interface to inspect them
   - Type object names to get detailed information
   - Press `*` again or `Esc` to exit Query Mode

## Accessibility Benefits

- **Keyboard Power Users**: Continue using efficient single-key shortcuts
- **New Players**: Use familiar arrow keys and mouse navigation
- **Reduced Learning Curve**: Multiple navigation options for different preferences
- **Improved Discoverability**: Visual indicators help users discover features

## Demo

Run the enhanced navigation demo to see these features in action:

```bash
python demo_enhanced_navigation.py
```

The demo showcases:
- Arrow key navigation
- Mouse click support
- Combined navigation methods
- Enhanced menu interface

## Implementation Notes

- All navigation methods work simultaneously - use whichever you prefer
- The interface automatically adapts to terminal size
- Mouse support works in most terminal emulators that support mouse events
- Navigation preferences can be configured in the settings menu

---

*"Command efficiently, navigate intuitively. The resistance depends on it."*
