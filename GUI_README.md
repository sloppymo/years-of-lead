# Years of Lead - GUI Implementation

## Overview

This document describes the desktop GUI implementation for **Years of Lead**, converting the terminal-based insurgency simulation game into a modern desktop application using Python and Tkinter.

## Features

### 🎮 Core Interface
- **Dark Theme**: Modern dark interface with blue/orange accent colors
- **Multi-Panel Layout**: Organized display with status, narrative, and detail panels
- **Real-time Updates**: Live game state updates with 1-second refresh rate
- **Responsive Design**: Adapts to different window sizes

### 📊 Visual Elements
- **Emotional State Visualization**: Bar charts showing agent emotions
- **Status Icons**: Color-coded indicators for agent status (🟢 Active, 🔴 Captured, etc.)
- **Faction Resources**: Visual display of money, personnel, and influence
- **Location Security**: Security and unrest level indicators

### 🎯 Game Controls
- **Turn Advancement**: Manual and automatic turn progression
- **Agent Management**: View, select, and manage individual agents
- **Mission System**: Create and assign missions to agents
- **Save/Load**: Game state persistence

### 📝 Information Display
- **Narrative Panel**: Scrollable text area for game narrative
- **Event Log**: Recent events and location-specific activities
- **Agent Details**: Comprehensive agent information display
- **Location Status**: Security levels and agent distribution

## Architecture

### File Structure
```
src/gui/
├── __init__.py          # Package initialization
├── main_gui.py          # Main GUI application class
└── components.py        # Reusable GUI components
```

### Key Classes

#### `YearsOfLeadGUI`
Main application class that orchestrates the entire interface:
- Manages game state integration
- Handles UI updates and event binding
- Coordinates between different panels

#### `StatusPanel`
Displays current game status:
- Day counter and phase indicator
- Active agent count
- Faction resource overview

#### `NarrativePanel`
Handles narrative text display:
- Scrollable text area for game narrative
- Event log with recent activities
- Auto-scroll to latest content

#### `AgentDetailPanel`
Shows detailed agent information:
- Personal details and statistics
- Skills and equipment lists
- Relationship information

#### `EmotionalVisualization`
Canvas-based emotion display:
- Bar charts for emotional states
- Color-coded emotion types
- Real-time emotion updates

## Installation

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually included with Python)

### Setup
1. Install GUI dependencies:
   ```bash
   pip install -r requirements-gui.txt
   ```

2. Run the GUI:
   ```bash
   python main.py --mode gui
   ```

### Alternative Launch Methods
```bash
# Direct GUI launch
python src/gui/main_gui.py

# CLI mode (fallback)
python main.py --mode cli

# Legacy compatibility
python main.py --no-ui
```

## Usage

### Basic Controls
- **Spacebar**: Advance turn
- **Ctrl+S**: Save game
- **Ctrl+Q**: Quit application

### Interface Navigation
1. **Left Panel**: Faction status and agent list
2. **Center Panel**: Narrative and recent events
3. **Right Panel**: Agent details and location info
4. **Bottom Panel**: Action buttons and controls

### Agent Management
1. Select an agent from the left panel
2. View details in the right panel
3. Use action buttons to manage the agent
4. Monitor emotional state visualization

### Game Progression
1. Review current game state
2. Assign missions or move agents
3. Click "Advance Turn" or use auto-play
4. Read narrative updates and events

## Customization

### Theme Colors
Modify the `colors` dictionary in `main_gui.py`:
```python
self.colors = {
    'bg_primary': '#1a1a1a',      # Main background
    'bg_secondary': '#2d2d2d',    # Secondary background
    'accent_blue': '#4a9eff',     # Primary accent
    'accent_green': '#6dd400',    # Success/positive
    'accent_red': '#ff4757',      # Danger/negative
    # ... more colors
}
```

### Layout Adjustments
- Modify panel sizes in `setup_middle_panel()`
- Adjust font sizes and styles
- Change update frequency in `update_display()`

### Adding New Features
1. Create new component classes in `components.py`
2. Integrate into main GUI in `main_gui.py`
3. Add event handlers and update logic
4. Test with `test_gui.py`

## Development

### Testing
Run the GUI test suite:
```bash
python test_gui.py
```

### Debugging
- Enable debug logging in the main application
- Use print statements for development
- Check console output for errors

### Packaging
Create standalone executable:
```bash
# Using PyInstaller
pyinstaller --onefile --windowed src/gui/main_gui.py

# Using Briefcase
briefcase new
briefcase dev
briefcase build
briefcase run
```

## Integration with Game Logic

### Adapter Pattern
The GUI uses an adapter pattern to interface with existing game logic:
- GUI events → Game state updates
- Game state changes → UI updates
- No modification of core game logic required

### State Synchronization
- Real-time updates via `update_display()` loop
- Event-driven updates for user actions
- Automatic refresh on game state changes

### Error Handling
- Graceful fallback to CLI mode
- User-friendly error messages
- Automatic recovery from common issues

## Future Enhancements

### Planned Features
- **Advanced Charts**: Faction influence radar charts
- **Voice Synthesis**: Narrator text-to-speech
- **Animations**: Smooth transitions and effects
- **Multiplayer**: Network-based multiplayer support

### Optional Components
- **Plotly Integration**: Interactive data visualizations
- **Kivy Alternative**: Mobile-compatible interface
- **Web Interface**: Browser-based version

## Troubleshooting

### Common Issues

#### GUI Won't Launch
- Check Python version (3.8+ required)
- Verify Tkinter installation
- Try CLI mode as fallback

#### Import Errors
- Ensure `src/` directory is in Python path
- Check all required modules are installed
- Verify file structure is correct

#### Performance Issues
- Reduce update frequency in `update_display()`
- Limit number of displayed agents/events
- Optimize canvas redraw operations

#### Styling Problems
- Check ttk style configuration
- Verify color definitions
- Test on different platforms

### Getting Help
1. Check console output for error messages
2. Run `test_gui.py` for diagnostic information
3. Verify game logic is working in CLI mode
4. Check system requirements and dependencies

## Contributing

### Development Guidelines
1. Follow existing code style and structure
2. Add comprehensive error handling
3. Include docstrings for all new methods
4. Test on multiple platforms
5. Update documentation for new features

### Code Organization
- Keep GUI logic separate from game logic
- Use component-based architecture
- Maintain consistent naming conventions
- Add type hints for better IDE support

---

**Years of Lead GUI** - Bringing the insurgency simulation to the desktop with style and functionality.
