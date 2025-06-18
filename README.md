![License](https://img.shields.io/badge/license-Forest%20Within%20Proprietary-blueviolet?style=flat-square)

> © 2025 Forest Within Therapeutic Services PC.
> [Custom Symbolic License](./LICENSE.txt) — All rights reserved.
> For licensing inquiries, contact: [your.email@example.com]

# Years of Lead v1.0.0

> An advanced psychological insurgency simulator featuring autonomous agent decision-making, enhanced mission execution, real-time intelligence systems, deep agent relationships, emotional modeling, emergent narrative generation, and sophisticated reputation systems through complex social network dynamics.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0.0-brightgreen.svg)](VERSION)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-Enabled-brightgreen.svg)](.pre-commit-config.yaml)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/ci-cd.yml)

## ✨ Overview

**Years of Lead v1.0.0** is a sophisticated political insurgency simulation that combines advanced AI agent autonomy, enhanced mission execution systems, real-time intelligence gathering, and deep psychological modeling. This release represents a complete core simulation with autonomous agents that make independent decisions based on their emotional states, trauma levels, faction loyalty, and mission priorities.

The simulation features 15 autonomous action types, enhanced mission outcomes with multi-agent collaboration effects, real-time intelligence systems with counter-intelligence operations, and pattern analysis capabilities. Every agent relationship, emotional state, and reputation consequence drives emergent gameplay where stories develop naturally from complex agent interactions.

### 🧠 Core Philosophy
- **Autonomous Agent Intelligence**: Agents make independent decisions based on psychological states
- **Enhanced Mission Execution**: Multi-layered outcomes with emotional and collaboration factors
- **Real-time Intelligence Systems**: Continuous gathering, analysis, and counter-intelligence operations
- **Trauma-Informed Design**: Respectful modeling of psychological complexity and emotional states
- **Emergent Narratives**: Stories emerge from agent interactions rather than scripted events
- **Social Network Realism**: Authentic relationship dynamics with trust, loyalty, and betrayal

## 🚀 Major Features (v1.0.0)

### 🤖 **Enhanced Agent Autonomy System** *(NEW in v1.0.0)*
- **15 Autonomous Action Types**:
  - Safety/Survival: `seek_safety`, `avoid_threat`, `change_location`, `seek_medical_help`
  - Social: `build_relationship`, `confide_secret`, `request_backup`
  - Mission: `gather_intelligence`, `recruit_contact`, `abandon_mission`
  - Emotional: `emotional_breakdown`, `seek_revenge`
  - Loyalty: `betray_target`, `desert_faction`, `self_sacrifice`

- **Advanced Decision Engine**:
  - Emotional state-driven decisions (fear triggers safety-seeking, anger drives revenge)
  - Risk assessment with 5-level system (minimal to extreme)
  - Agent autonomy profiles with customizable risk tolerance and emotional stability
  - Learning system that updates profiles based on decision outcomes

- **Psychological Integration**:
  - Trauma levels affect decision-making (>0.6 trauma triggers help-seeking)
  - Stress thresholds influence autonomous actions (>70% stress triggers mission abandonment)
  - Faction loyalty crisis detection (<30% loyalty triggers desertion consideration)

### 🎯 **Enhanced Mission Execution System** *(NEW in v1.0.0)*
- **14 Enhanced Outcome Types**:
  - Success Variants: `perfect_success`, `success_with_complications`, `tragic_success`, `pyrrhic_victory`
  - Failure Types: `failure_with_intel`, `beneficial_failure`, `catastrophic_failure`
  - Special Outcomes: `betrayal_revealed`, `sabotaged_mission`, `unintended_consequences`

- **Multi-Agent Collaboration Analysis**:
  - Trust synergy bonuses between agents
  - Skill complementarity assessment
  - Communication efficiency factors
  - Leadership effectiveness evaluation
  - Emotional contagion effects across team

- **Enhanced Consequence System**:
  - Per-agent emotional impacts from mission outcomes
  - Relationship changes based on shared mission experience
  - Delayed effects and recovery time mechanics
  - Escalation potential tracking

### 🕵️ **Real-time Intelligence System** *(NEW in v1.0.0)*
- **Continuous Intelligence Gathering**:
  - Agent network intelligence (30% base chance, modified by skills/emotions)
  - Technical surveillance (satellite, electronic, communication intercepts)
  - Human assets (government insiders, military contacts, civilian informants)
  - Signal intelligence (radio intercepts, phone taps, encryption breaking)

- **Advanced Pattern Analysis**:
  - Type clustering detection (3+ events of same type)
  - Location-based activity patterns (4+ events in same area)
  - Temporal pattern recognition (rapid event sequences)
  - Cross-source correlation and verification

- **Counter-Intelligence Operations**:
  - Surveillance detection and evasion
  - Disinformation campaigns
  - Security audits and mole hunts
  - Communication security enhancement
  - Double agent management

### 🧠 **Agent Psychological Complexity**
- **Emotional State Modeling**: Plutchik's 8-emotion model with trauma integration
- **Dynamic Personality Evolution**: Agents change based on experiences and relationships
- **Stress Response Systems**: Dynamic stress accumulation affecting all decisions
- **Memory-Driven Behavior**: Past experiences shape future choices
- **Adaptive Learning**: Success/failure rates influence future autonomous decisions

### 🕸️ **Advanced Social Networks**
- **Bidirectional Relationship Graphs**: Complex social connections with influence mapping
- **Multi-Dimensional Metrics**: Trust (0.0-1.0), Loyalty (0.0-1.0), Affinity (-100 to +100)
- **Relationship Evolution**: Mission experiences and autonomous actions affect relationships
- **Social Circle Analysis**: Filter by bond type, influence radius, faction membership
- **Emotional Contagion**: Emotions spread through positive relationships over time

### 🏆 **Reputation & Public Perception**
- **Multi-Layer Reputation System**: Fame, infamy, and public sentiment tracking
- **Media Influence Mechanics**: News coverage affects public opinion and operations
- **Government Response Modeling**: State reactions to resistance activities
- **Dynamic Threat Assessment**: Location-based threat levels with intelligence integration
- **Political Pressure Dynamics**: Reputation affects search probability and dialogue

### 🤐 **Secrets & Information Warfare**
- **6 Secret Categories**: Personal, Operational, Political, Criminal, Emotional, Strategic
- **Network-Based Propagation**: Rumor spreading with success probability modeling
- **Strategic Information Use**: Emotional blackmail and tactical advantage
- **Discovery Events**: Dynamic revelation with relationship consequences
- **Intelligence Network Topology**: Flow analysis and vulnerability mapping

### 📝 **Memory & Trauma Systems**
- **Emotional Memory Logs**: Persistent journals with emotional impact scoring
- **Time-Based Decay**: Memory fading with trauma persistence mechanics
- **Narrative Integration**: Past experiences influence future story generation
- **Shared Memory Networks**: Collective memories affecting group dynamics
- **Recovery Systems**: Therapy, safe environments, and healing mechanics

## 🧬 Architecture & Systems

### 📁 **Enhanced Core Structure**
```
src/
├── game/
│   ├── core.py                          # Main simulation engine
│   ├── entities.py                      # Base dataclasses and game state
│   ├── enhanced_agent_autonomy.py       # NEW: Autonomous decision system
│   ├── enhanced_mission_system.py       # NEW: Advanced mission execution
│   ├── enhanced_intelligence_system.py  # NEW: Real-time intelligence
│   ├── relationships.py                 # Social network management
│   ├── advanced_relationships.py        # Secrets, betrayal, memory systems
│   ├── emotional_state.py               # Psychological modeling
│   ├── narrative_engine.py              # Dynamic story generation
│   └── reputation_system.py             # Public perception tracking
├── gui/                                 # Desktop interface
├── ui/                                  # Web interface (React)
├── api/                                 # REST API backend
├── models/                              # Data models
├── services/                            # Business logic
└── utils/                               # Utility functions
```

### 🧪 **Comprehensive Testing**
```
tests/
├── unit/                    # Unit tests for all components
├── integration/             # Cross-system testing
├── maintenance/             # System health validation
├── e2e/                    # End-to-end simulation testing
└── gui/                    # Interface testing
```

### 📊 **Quality Assurance & Monitoring**
- **Automated Testing**: GitHub Actions CI/CD pipeline
- **Code Quality**: Pre-commit hooks with Black, Ruff, and comprehensive linting
- **Performance Monitoring**: Real-time system health metrics
- **Memory Management**: Efficient large-scale agent simulation handling
- **Error Recovery**: Robust error handling with graceful degradation

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12 or higher
- Node.js 16+ (for web UI)
- Git for version control

### Quick Start
```bash
# Clone the repository
git clone https://github.com/sloppymo/years-of-lead.git
cd years-of-lead

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run the simulation
python play_years_of_lead.py
```

### Web UI Setup
```bash
# Navigate to web UI directory
cd src/ui

# Install Node.js dependencies
npm install

# Start development server
npm start
```

### Desktop GUI Setup
```bash
# Install GUI dependencies
pip install -r requirements-gui.txt

# Run desktop interface
python -m gui.main_gui
```

## 🎮 Usage Examples

### Basic Simulation
```python
from src.game.core import GameState

# Initialize complete simulation
game_state = GameState()
game_state.initialize_game()

# Process one turn with all systems
results = game_state.advance_turn()

print(f"Autonomous decisions: {len(results['autonomous_decisions'])}")
print(f"Mission outcomes: {len(results['mission_results'])}")
print(f"Intelligence events: {len(results['intelligence_updates'])}")
```

### Advanced Agent Autonomy
```python
from src.game.enhanced_agent_autonomy import EnhancedAgentAutonomySystem

# Initialize autonomy system
autonomy_system = EnhancedAgentAutonomySystem(game_state)

# Process autonomous decisions
decisions = autonomy_system.process_autonomous_decisions()

# Analyze decision patterns
for decision in decisions['decisions_made']:
    print(f"Agent {decision.agent_id}: {decision.action_type.value}")
    print(f"Emotional driver: {decision.emotional_driver}")
    print(f"Risk level: {decision.risk_level:.2f}")
```

### Enhanced Mission Execution
```python
from src.game.enhanced_mission_system import EnhancedMissionExecutor

# Execute mission with enhanced outcomes
mission_executor = EnhancedMissionExecutor(game_state)
result = mission_executor.execute_enhanced_mission(
    mission={"type": "sabotage", "difficulty": "high"},
    agents=[agent_1, agent_2, agent_3],
    location=target_location,
    resources=available_resources
)

print(f"Outcome: {result['outcome'].value}")
print(f"Collaboration score: {result['collaboration_analysis'].group_cohesion:.2f}")
print(f"Emotional impacts: {result['emotional_impacts']}")
```

### Real-time Intelligence
```python
from src.game.enhanced_intelligence_system import EnhancedIntelligenceSystem

# Process intelligence gathering
intel_system = EnhancedIntelligenceSystem(game_state)
intel_results = intel_system.process_real_time_intelligence()

print(f"New intelligence: {len(intel_results['new_intelligence'])}")
print(f"Patterns detected: {len(intel_results['patterns_detected'])}")
print(f"Threat assessments: {intel_results['threat_assessments']}")
```

## 📈 System Performance

### Key Metrics (v1.0.0)
- **Agent Autonomy**: 15 decision types with 70%+ success rate
- **Mission Enhancement**: 14 outcome types with collaboration factors
- **Intelligence Processing**: Real-time pattern detection and counter-ops
- **Emotional Modeling**: Plutchik 8-emotion system with trauma persistence
- **Relationship Tracking**: Efficient multi-agent social network management
- **Narrative Generation**: 50+ templates with anti-repetition logic

### Performance Benchmarks
- **Agent Processing**: 100+ agents per turn with autonomous decisions
- **Memory Efficiency**: Optimized relationship and emotional state tracking
- **Intelligence Analysis**: Real-time pattern detection on 100+ events
- **Mission Execution**: Multi-agent collaboration with complex outcome calculation
- **Code Quality**: 100% pre-commit hook compliance

## 🚀 What's New in v1.0.0

### ✅ **Phase 1: Agent Autonomy Enhancement** - COMPLETED
- Autonomous decision-making based on emotional states and trauma
- 15 action types from safety-seeking to faction desertion
- Risk assessment and agent learning systems
- Integration with existing psychological modeling

### ✅ **Phase 2: Mission Outcome Enhancement** - COMPLETED
- 14 enhanced outcome types including tragic success and pyrrhic victory
- Multi-agent collaboration analysis with trust and skill synergy
- Enhanced consequence system with emotional and relationship impacts
- Mission-based relationship evolution

### ✅ **Phase 3: Real-time Intelligence Systems** - COMPLETED
- Continuous intelligence gathering from multiple sources
- Advanced pattern analysis and threat assessment
- Counter-intelligence operations and security measures
- Intelligence-driven mission planning and execution

### ✅ **Phase 4: Enhanced CLI Navigation** - COMPLETED
- Dwarf Fortress-inspired command center interface with 5-star navigation efficiency
- Arrow key navigation for menu selection and interaction
- Mouse click support for intuitive point-and-click interface
- Combined navigation methods for accessibility and user preference
- Visual selection indicators and context-sensitive help
- Victory/defeat conditions with game over screens and statistics
- Enhanced save/load system with rich metadata and autosave functionality

### 🔄 **Upcoming Enhancements**
- **Phase 5**: Dynamic Narrative Generation expansion
- **Phase 6**: Advanced Trauma and Psychological Impact systems
- Enhanced web UI with real-time intelligence dashboards
- Multi-player faction competition modes

## 🤝 Contributing

We welcome contributions to the Years of Lead project! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development workflow and coding standards
- Testing requirements and quality gates
- Pull request process and review guidelines
- Community guidelines and code of conduct

### Development Commands
```bash
# Run comprehensive tests
python -m pytest tests/ -v --cov=src

# Format and lint code
pre-commit run --all-files

# Run specific system tests
python test_relationship_system.py
python test_dynamic_narrative_tone.py
python test_equipment_search_system.py

# System health check
python run_maintenance.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Advanced AI Systems**: Built with sophisticated agent autonomy and decision-making
- **Psychological Modeling**: Trauma-informed design with respectful complexity
- **Open Source Community**: Leveraging community contributions and feedback
- **Academic Research**: Informed by psychology, sociology, and game theory

---

**Years of Lead v1.0.0** - Complete core simulation with autonomous agents, enhanced missions, and real-time intelligence. Where every decision matters, every relationship evolves, and the revolution is deeply personal.

*"The simulation is no longer just about what you plan—it's about what your agents decide to do when plans fall apart, trust breaks down, and survival becomes personal."*

---

**Release Notes v1.0.0**:
- ✅ **Enhanced Agent Autonomy**: Complete autonomous decision-making system
- ✅ **Advanced Mission Execution**: Multi-layered outcomes with collaboration effects
- ✅ **Real-time Intelligence**: Continuous gathering and counter-intelligence operations
- ✅ **Enhanced CLI Navigation**: Arrow keys, mouse support, and DF-style interface
- ✅ **Game Flow Completion**: Victory/defeat conditions and enhanced save system
- ✅ **Code Quality**: Full pre-commit hook implementation and CI/CD pipeline
- ✅ **Documentation**: Comprehensive API documentation and usage examples
- ✅ **Testing**: Complete test coverage with unit, integration, and E2E tests
- ✅ **Performance**: Optimized for large-scale multi-agent simulations
