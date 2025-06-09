# Years of Lead

A complex turn-based insurgency simulator with narrative complexity, inspired by Liberal Crime Squad and Dwarf Fortress, integrated with SYLVA & WREN emotional wellness systems.

## Project Overview

**Years of Lead** simulates revolutionary resistance with deep factional nuance and emotional dynamics. The game features procedural storytelling, emergent complexity, and moral dimensions that challenge players to navigate the complicated world of political movements and insurgency tactics.

## Technology Stack

- **Backend**: Python (FastAPI), PostgreSQL, MongoDB
- **Frontend**: React
- **AI Integration**: SYLVA & WREN APIs for emotional modeling and narrative generation
- **Containerization**: Docker & Docker Compose

## Project Structure

```
years-of-lead/
├── src/                  # Source code
│   ├── api/              # API endpoints and routes
│   ├── core/             # Core configuration and utilities
│   ├── game/             # Game engine, state management, and logic
│   ├── ui/               # React frontend application
│   ├── utils/            # Utility functions and helpers
│   └── main.py           # Application entry point
├── tests/                # Test code
├── docs/                 # Documentation
├── assets/               # Game assets
├── config/               # Configuration files
├── deployment/           # Deployment scripts and configurations
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration for backend
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # Project documentation
```

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL 14+
- MongoDB 5+

### Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd years-of-lead
   ```

2. Create and activate a Python virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env file with appropriate values
   ```

5. Set up the frontend:
   ```
   cd src/ui
   npm install
   ```

### Running with Docker

1. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

2. Access the application:
   - Backend API: http://localhost:8000
   - Frontend UI: http://localhost:3000

### Running Development Servers

1. Start the backend server:
   ```
   source venv/bin/activate
   cd src
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```
   cd src/ui
   npm start
   ```

## AI Integration

### SYLVA Integration

SYLVA (Symbolic Yield Logic & Variant Architecture) provides emotional regulation modeling and symbolic interpretation of player decisions. The integration includes:

- Emotional regulation engine
- Symbolic feedback mechanisms
- Narrative AI layer with symbolic mapping

### WREN Integration

WREN (Worldbuilding Reflective Engine for Narrative) handles reflective narrative scaffolding and character growth loops:

- Therapeutic character arc system
- Emotional resonance feedback loops
- Adaptive storytelling responses

## Implementation Roadmap

See [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) for a detailed breakdown of the development phases.

## Gameplay Mechanics

Core gameplay mechanics include:

1. **Faction System**: Diverse factions with asymmetric goals and diplomacy
2. **Cell Management**: Underground operations, heat tracking, sleeper agents
3. **Protest Engineering**: Procedural protest building with crowd psychology
4. **Information Warfare**: Meme warfare, hacking, and disinformation
5. **Narrative AI**: Procedural storytelling with ethical and emotional depth

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## License

This project is proprietary and confidential. All rights reserved by Windsurf.
