"""
Mock Game class for testing purposes.
"""
from unittest.mock import MagicMock

class MockLocation:
    """Mock Location class for testing"""
    
    def __init__(self, name, controlled=False):
        """Initialize a mock location"""
        self.name = name
        self.controlled = controlled
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "name": self.name,
            "controlled": self.controlled
        }

class MockFaction:
    """Mock Faction class for testing"""
    
    def __init__(self, name, strength=30):
        """Initialize a mock faction"""
        self.name = name
        self.strength = strength
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "name": self.name,
            "strength": self.strength
        }

class MockAgent:
    """Mock Agent class for testing"""
    
    def __init__(self, name, skills=None):
        """Initialize a mock agent"""
        self.name = name
        self.skills = skills or {"combat": 3, "stealth": 2, "charisma": 4}
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "name": self.name,
            "skills": self.skills
        }

class MockGame:
    """Mock version of Game for testing"""
    
    def __init__(self):
        """Initialize the mock game"""
        self.turn = 1
        self.date = "1975-01-01"
        self.public_support = 30
        self.resources = 100
        self.agents = [
            MockAgent("Agent1"),
            MockAgent("Agent2")
        ]
        self.locations = [
            MockLocation("Milan", controlled=True),
            MockLocation("Rome", controlled=False),
            MockLocation("Turin", controlled=False),
            MockLocation("Naples", controlled=False)
        ]
        self.factions = [
            MockFaction("Police", strength=30),
            MockFaction("Military", strength=25),
            MockFaction("Government", strength=20)
        ]
        self.narrative_log = []
        
    def to_dict(self):
        """Convert game state to dictionary"""
        return {
            "turn": self.turn,
            "date": self.date,
            "public_support": self.public_support,
            "resources": self.resources,
            "agents": [agent.to_dict() for agent in self.agents],
            "locations": [location.to_dict() for location in self.locations],
            "factions": [faction.to_dict() for faction in self.factions],
            "narrative_log": self.narrative_log
        }
        
    def from_dict(self, game_state):
        """Load game state from dictionary"""
        self.turn = game_state.get("turn", 1)
        self.date = game_state.get("date", "1975-01-01")
        self.public_support = game_state.get("public_support", 30)
        self.resources = game_state.get("resources", 100)
        
        # Load agents
        self.agents = []
        for agent_data in game_state.get("agents", []):
            agent = MockAgent(agent_data.get("name", "Unknown"))
            agent.skills = agent_data.get("skills", {})
            self.agents.append(agent)
            
        # Load locations
        self.locations = []
        for location_data in game_state.get("locations", []):
            location = MockLocation(
                location_data.get("name", "Unknown"),
                controlled=location_data.get("controlled", False)
            )
            self.locations.append(location)
            
        # Load factions
        self.factions = []
        for faction_data in game_state.get("factions", []):
            faction = MockFaction(
                faction_data.get("name", "Unknown"),
                strength=faction_data.get("strength", 30)
            )
            self.factions.append(faction)
            
        # Load narrative log
        self.narrative_log = game_state.get("narrative_log", []) 