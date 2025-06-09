# Years of Lead

> A sophisticated insurgency simulator that puts you in command of a resistance movement fighting against an oppressive regime.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)](https://github.com/yourusername/years-of-lead)

## 🎯 Overview

Years of Lead is a text-based strategy game that simulates the complex dynamics of running an underground resistance movement. You'll create characters, plan missions, gather intelligence, and make difficult moral choices in a world where every decision has consequences.

### Key Features

- **Deep Character Creation**: Create operatives with unique backgrounds, personalities, and trauma
- **Strategic Mission Planning**: Plan operations with comprehensive risk assessment and team coordination
- **Intelligence Network**: Gather and analyze intelligence to stay ahead of government forces
- **Moral Complexity**: Navigate the difficult choices of revolutionary violence and its consequences
- **Dynamic World**: Experience a living world that reacts to your actions and decisions

## 🚀 Recent Updates (v1.0.1)

### ✅ Character Creation Improvements
- **Confirmation prompts** for all character choices
- **Hidden name input** for security
- **Detailed mechanical and narrative explanations** for every choice
- **Realistic funding** (multiplied by 100 for realism)

### ✅ Mission Planning System
- **Comprehensive location information** with security levels and local support
- **Procedural flavor text** for atmospheric immersion
- **Risk assessment** and success probability calculation
- **Narrative consequences** and action opportunities

### ✅ Intelligence System
- **Detailed event information** with mechanical effects
- **Pattern detection** and threat assessment
- **Action opportunities** based on intelligence gathered
- **Real-time analysis** and situation reports

## 🎮 Gameplay

### Character Creation
Create operatives from diverse backgrounds:
- **Military**: Combat veterans with tactical expertise
- **Academic**: Researchers and intellectuals
- **Criminal**: Street-smart operatives with underworld connections
- **Corporate**: Business professionals with access to resources
- **Medical**: Healthcare workers with healing skills
- **Technical**: IT professionals and hackers
- **Journalist**: Media professionals with communication skills
- **Religious**: Faith leaders with community connections
- **Activist**: Political organizers with protest experience
- **Laborer**: Working-class operatives with industrial knowledge

Each background provides unique skills, resources, and narrative consequences.

### Mission Planning
Plan operations across different districts:
- **Government Quarter**: High-security government district
- **University District**: Academic area with student population
- **Industrial Zone**: Factory district with worker population
- **Old Town Market**: Historic district with markets
- **Suburban Residential**: Middle-class residential area
- **Downtown Commercial**: Business district with offices

Each location has different security levels, surveillance, and local support.

### Intelligence Gathering
Monitor government activities through:
- **Government Movement**: Track official activities and meetings
- **Security Changes**: Monitor new surveillance and security measures
- **Economic Data**: Analyze financial manipulation and economic trends
- **Social Unrest**: Track protest movements and civil unrest
- **Military Activity**: Monitor military movements and equipment
- **Corporate Activity**: Watch business and corporate developments
- **Media Analysis**: Analyze news and propaganda
- **Infrastructure**: Monitor critical infrastructure changes
- **Personnel Movements**: Track key personnel and officials
- **Communications**: Intercept and analyze communications

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/years-of-lead.git
cd years-of-lead

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python play_years_of_lead.py
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python test_improvements.py

# Run linting
flake8 src/
```

## 📁 Project Structure

```
years-of-lead/
├── src/
│   └── game/
│       ├── character_creation.py      # Character creation system
│       ├── character_creation_ui.py   # Character creation interface
│       ├── mission_planning.py        # Mission planning system
│       ├── intelligence_system.py     # Intelligence gathering
│       ├── emotional_state.py         # Emotional state management
│       ├── core.py                    # Core game engine
│       ├── engine.py                  # Game engine
│       ├── events.py                  # Event system
│       ├── factions.py                # Faction system
│       └── state.py                   # Game state management
├── tests/                             # Test files
├── docs/                              # Documentation
├── assets/                            # Game assets
├── requirements.txt                   # Python dependencies
├── play_years_of_lead.py             # Main game launcher
└── README.md                          # This file
```

## 🎯 Core Systems

### Character System
- **Background Types**: 10 different backgrounds with unique bonuses
- **Personality Traits**: 16 personality traits affecting gameplay
- **Skill System**: 8 skill categories (Combat, Stealth, Hacking, etc.)
- **Trauma System**: Psychological trauma affecting character behavior
- **Emotional State**: Dynamic emotional states influencing decisions

### Mission System
- **Mission Types**: 8 mission types (Propaganda, Sabotage, Recruitment, etc.)
- **Risk Assessment**: Comprehensive risk calculation based on multiple factors
- **Team Coordination**: Character skills affect mission success
- **Consequences**: Long-term effects of mission outcomes

### Intelligence System
- **Event Types**: 10 intelligence event types
- **Source Reliability**: Different intelligence sources have varying reliability
- **Pattern Detection**: Automatic analysis of intelligence patterns
- **Threat Assessment**: Dynamic threat level calculation

## 🔧 Configuration

### Game Settings
The game can be configured through environment variables or configuration files:

```bash
# Set game difficulty
export YEARS_OF_LEAD_DIFFICULTY=medium

# Enable debug mode
export YEARS_OF_LEAD_DEBUG=true

# Set save directory
export YEARS_OF_LEAD_SAVE_DIR=./saves
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_improvements.py
```

The test suite covers:
- Character creation improvements
- Mission planning system
- Intelligence system
- System integration

## 📚 Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Improvements Summary](IMPROVEMENTS_SUMMARY.md)
- [To-Do List](TODO.md)
- [Maintenance Guide](MAINTENANCE_GUIDE.md)
- [Technical Documentation](docs/technical/)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for all classes and methods
- Include tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by classic strategy games and political simulations
- Built with modern Python best practices
- Community feedback and testing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/years-of-lead/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/years-of-lead/discussions)
- **Email**: support@years-of-lead.com

## 🗺️ Roadmap

See our [To-Do List](TODO.md) for detailed development plans.

### Upcoming Features (v1.1)
- Character relationships system
- Advanced trauma mechanics
- Mission execution phase
- Real-time intelligence

### Future Releases
- Resource management system
- Enhanced faction dynamics
- Combat mechanics
- Multiplayer support

---

**Years of Lead** - Where every choice matters, and the revolution never sleeps.

*"The price of freedom is eternal vigilance."*
