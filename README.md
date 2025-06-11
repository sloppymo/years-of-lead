# Years of Lead

> An advanced psychological insurgency simulator featuring deep agent relationships, emotional modeling, and emergent narrative generation through sophisticated social network dynamics.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Alpha%20v0.4.0-orange.svg)](https://github.com/yourusername/years-of-lead)
[![Tests](https://img.shields.io/badge/Tests-47/47%20Passing-brightgreen.svg)](tests/)

## ✨ Overview

**Years of Lead** is a high-complexity insurgency simulation that models human psychology, social networks, and emergent storytelling through sophisticated agent interactions. Built with trauma-informed design principles and integrated with symbolic narrative logic, the system creates authentic relationship dynamics where trust, loyalty, betrayal, and emotional contagion drive emergent gameplay.

The simulation combines advanced psychological modeling with political insurgency mechanics, creating stories that emerge naturally from agent relationships rather than scripted events. Every interaction matters, every secret has consequences, and every betrayal reshapes the social fabric of the resistance.

### 🧠 Core Philosophy
- **Trauma-Informed Design**: Respectful modeling of psychological complexity and emotional states
- **Emergent Narratives**: Stories emerge from agent interactions rather than scripted events  
- **Social Network Realism**: Authentic relationship dynamics with trust, loyalty, and betrayal
- **Symbolic Integration**: SYLVA/WREN compatible for therapeutic and educational applications

## 🚀 Features

### 🕸️ **Dynamic Social Networks**
- **Bidirectional Relationship Graphs**: Complex social connections with influence mapping
- **Multi-Dimensional Metrics**: Trust (0.0-1.0), Loyalty (0.0-1.0), Affinity (-100 to +100)
- **Relationship Decay**: Natural drift toward neutrality unless actively reinforced
- **Social Circle Analysis**: Filter relationships by bond type, influence radius, and faction membership

### 🤐 **Secrets & Information Warfare**
- **6 Secret Categories**: Personal, Operational, Political, Criminal, Emotional, Strategic
- **Rumor Propagation**: Network-based secret spreading with success probability modeling
- **Emotional Blackmail**: Strategic weaponization of secrets with resistance mechanics
- **Discovery Events**: Dynamic revelation systems with relationship consequences

### 🎭 **Persona Masks & Deception**
- **Strategic Mask Systems**: Agents hide true feelings behind calculated personas
- **Empathy-Based Detection**: Skill-based mask penetration with relationship strength factors
- **Social Manipulation**: Deliberate relationship deception for tactical advantage
- **Betrayal Integration**: Persona mechanics feed directly into betrayal planning systems

### 📝 **Memory & Emotional Journaling**
- **Emotional Memory Logs**: Persistent journals of impactful events with emotional scoring
- **Time-Based Memory Decay**: Configurable fading rates with trauma persistence
- **Narrative Memory Integration**: Past experiences influence future relationship events
- **Shared Memory Networks**: Collective memories affecting group dynamics

### 🏛️ **Political Fracture Mechanics**
- **Real-Time Cohesion Monitoring**: Continuous faction internal stability measurement
- **Automatic Fracture Triggers**: Splinter cell generation when cohesion drops below 0.3
- **Agent Migration Systems**: Defectors form new factions with resource reallocation
- **Ideological Drift Tracking**: 6-dimensional belief evolution through social exposure

### 🔀 **Betrayal Planning Engine**
- **Multi-Factor Triggers**: Trust thresholds, stress levels, ideological distance, faction loyalty
- **Co-conspirator Networks**: Identification of potential betrayal allies through relationship analysis
- **Strategic Timing**: Preferred betrayal moments (immediate, during mission, post-success)
- **Continuous Activation Monitoring**: Real-time evaluation of betrayal plan viability

## 🧠 Agent Simulation

### 👥 **Sophisticated Agent Modeling**
- **10+ Background Types**: Veteran, Student, Journalist, Worker, Organizer, Insider, Academic, Artist, Exile, Militant
- **8 Skill Categories**: Combat, Stealth, Hacking, Persuasion, Intelligence, Demolitions, Medical, Leadership
- **Plutchik Emotion Model**: 8 basic emotions (joy, trust, fear, surprise, sadness, disgust, anger, anticipation)
- **6-Dimensional Ideology**: Radical, Pacifist, Individualist, Traditional, Nationalist, Materialist vectors

### 🧬 **Psychological Complexity**
- **Emotional Contagion**: Emotions spread through positive relationships over time
- **Trauma Integration**: Persistent traumatic memories with special decay resistance
- **Stress Response Systems**: Dynamic stress accumulation affecting decision-making
- **Social Tag Inheritance**: Background and faction-based personality markers

### 📊 **Behavioral Dynamics**
- **Trust Evolution**: Dynamic trust building and erosion through interactions
- **Loyalty Shifts**: Faction loyalty influenced by relationships and ideological alignment
- **Memory-Driven Decisions**: Past experiences shape future behavioral choices
- **Persona Management**: Strategic emotional presentation for social advantage

## 📚 Narrative Engine

### 🎬 **Hybrid Template System**
- **50+ Narrative Templates**: Comprehensive event coverage with variable substitution
- **Advanced Context Resolution**: Agent names, emotions, locations dynamically filled
- **Anti-Repetition Logic**: Template usage tracking ensures narrative variety
- **Hierarchical Fallbacks**: Graceful degradation when specific contexts unavailable

### 📖 **Dynamic Story Generation**
- **Relationship-Driven Events**: Narratives emerge from current agent social dynamics
- **Emotional Context Integration**: Story tone matches agent emotional states
- **Memory-Influenced Narratives**: Past events affect future story generation
- **Cross-System Integration**: Secrets, betrayals, and memories create narrative hooks

### 🎭 **Event Categories**
- **Relationship Events**: Trust building, loyalty tests, emotional bonding
- **Secret Revelation**: Discovery mechanics with relationship consequences  
- **Betrayal Narratives**: Planning, execution, and aftermath storytelling
- **Memory Formation**: Significant event recording with emotional impact
- **Ideological Conflict**: Belief system clashes and evolution stories

## 🧬 Symbolic Systems

### 🔗 **SYLVA/WREN Integration Hooks**
- **Symbolic Narrative Enhancement**: Prepared integration points for symbolic logic
- **Therapeutic Framework Stubs**: Mental health application connection points
- **Emotional Regulation Modeling**: Healthy coping mechanism simulation
- **Dream Logic Integration**: Subconscious narrative element support

### 🌐 **Network Analysis Systems**
- **Social Graph Algorithms**: Influence mapping and cluster detection
- **Emotional Flow Analysis**: Contagion pattern recognition and prediction
- **Secret Network Topology**: Information flow and vulnerability analysis
- **Memory Network Mapping**: Shared experience connection visualization

### 🔮 **Emergent Pattern Recognition**
- **Relationship Trend Analysis**: Historical evolution tracking and prediction
- **Faction Health Monitoring**: Early warning systems for instability
- **Betrayal Risk Assessment**: Multi-factor loyalty breakdown probability
- **Narrative Quality Metrics**: Story coherence and engagement scoring

## 📈 Faction Dynamics

### 🏛️ **Multi-Faction Politics**
- **Complex Inter-Faction Relationships**: Dynamic alliances and hostilities
- **Resource Competition**: Money, influence, and personnel management
- **Public Opinion Integration**: Sentiment tracking affecting faction power
- **Coalition Formation**: Temporary alliances based on shared interests

### 📊 **Internal Faction Management**
- **Cohesion Monitoring**: Real-time internal relationship strength measurement
- **Leadership Dynamics**: Authority structures and succession planning
- **Ideological Coherence**: Belief system alignment within factions
- **Defection Risk Assessment**: Early warning for agent loyalty breakdown

### 🔄 **Dynamic Faction Evolution**
- **Automatic Fracture Mechanics**: Splinter groups form when cohesion drops
- **Agent Migration Systems**: Organic movement between factions
- **Resource Reallocation**: Economic consequences of faction changes
- **Narrative Faction Events**: Story-driven faction relationship evolution

## 🔧 Architecture

### 📁 **Core Module Structure**
```
src/game/
├── entities.py                 # Base dataclasses (Agent, GameState, Faction, Relationship)
├── core.py                     # Main simulation engine and turn processing
├── relationships.py            # Social network graph and basic relationship logic
├── advanced_relationships.py   # 6 advanced relationship systems (secrets, betrayal, etc.)
├── emotional_state.py          # Plutchik emotion model with trauma integration
├── narrative_engine.py         # Hybrid template system with variable substitution
└── events.py                   # Event system with contextual narrative modification
```

### 🧪 **Testing & Quality Assurance**
```
tests/
├── unit/                       # Comprehensive unit tests (47/47 passing)
├── maintenance/                # Scenario-based system integrity validation
├── integration/               # Cross-system interaction testing
└── e2e/                       # End-to-end simulation testing
```

### 📊 **Performance & Monitoring**
- **Health Metrics**: Automated system stability assessment (Δ > +0.2)
- **Emotional Drift Optimization**: ≤0.01 per turn for realistic psychological change
- **Trauma Persistence**: 0.5+ accumulation factor for meaningful impact
- **Narrative Variety**: >0.7 uniqueness score preventing repetition

### 🔗 **Integration Architecture**
- **Entity-Component-System**: Maximum modularity and extensibility
- **Event-Driven Design**: Relationship changes trigger narrative updates
- **SYLVA/WREN Stubs**: Symbolic and therapeutic integration points
- **Circular Import Resolution**: Clean dependency management via entities.py

## 🛠️ Getting Started

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Quick Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/years-of-lead.git
cd years-of-lead

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Simulation
```bash
# Run the main simulation
python play_years_of_lead.py

# Test relationship systems
python test_relationship_system.py

# Run comprehensive test suite
python -m pytest tests/ -v

# Run specific advanced relationship tests
python -m pytest tests/unit/test_advanced_relationships.py -v
```

### Basic Usage Example
```python
from src.game.core import GameState
from src.game.advanced_relationships import AdvancedRelationshipManager

# Initialize sophisticated simulation
game_state = GameState()
game_state.initialize_game()

# Process advanced relationship mechanics
game_state.advance_turn()

# Generate context-aware narratives
agent_a = game_state.agents["agent_maria"]
agent_b = game_state.agents["agent_sofia"]
narrative = game_state.narrative_engine.generate_advanced_narrative(agent_a, agent_b)
print(narrative)

# Analyze social network dynamics
relationship_manager = game_state.relationship_manager
cohesion = relationship_manager.calculate_faction_cohesion("the_resistance")
secrets = relationship_manager.get_active_secrets()
betrayal_risks = relationship_manager.assess_betrayal_risks()
```

### Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with debugging
python debug_new_features.py

# Monitor system health
python run_maintenance.py

# Format code
pre-commit run --all-files
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Years of Lead** - Where every relationship matters, every secret has power, and the revolution is deeply personal.

*"In the end, it's not about ideology or tactics—it's about the people who stand with you when trust breaks down and the masks come off."*
