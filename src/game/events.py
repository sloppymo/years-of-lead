"""
Event management system for Years of Lead
Handles event dispatching, listeners, and event processing
"""

from typing import Dict, List, Any, Callable, Optional
import time
from loguru import logger


class EventManager:
    """
    Event manager for the game engine

    Provides a publish-subscribe pattern for game events,
    allowing components to listen for and react to events
    generated during gameplay.
    """

    def __init__(self):
        """Initialize event manager"""
        self.listeners = {}
        self.event_history = []
        self.max_history = 1000  # Maximum number of events to keep in history

    def register(self, event_type: str, listener: Callable) -> None:
        """
        Register a listener function for a specific event type

        Args:
            event_type: The type of event to listen for
            listener: Function to call when the event occurs
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []

        self.listeners[event_type].append(listener)
        logger.debug(f"Registered listener for event type: {event_type}")

    def unregister(self, event_type: str, listener: Callable) -> bool:
        """
        Unregister a listener function for a specific event type

        Args:
            event_type: The event type to unregister from
            listener: The listener function to remove

        Returns:
            bool: True if listener was removed, False otherwise
        """
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)
            logger.debug(f"Unregistered listener for event type: {event_type}")
            return True
        return False

    def trigger(self, event_type: str, data: Dict[str, Any] = None) -> None:
        """
        Trigger an event, notifying all listeners

        Args:
            event_type: The type of event to trigger
            data: Event data to pass to listeners
        """
        event_data = data or {}
        event_time = time.time()

        # Create event record
        event = {"type": event_type, "timestamp": event_time, "data": event_data}

        # Add to history
        self.event_history.append(event)

        # Trim history if necessary
        if len(self.event_history) > self.max_history:
            self.event_history = self.event_history[-self.max_history :]

        # Notify listeners
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    listener(event_data)
                except Exception as e:
                    logger.error(f"Error in event listener for {event_type}: {e}")

        # Special case for wildcard listeners
        if "*" in self.listeners:
            for listener in self.listeners["*"]:
                try:
                    listener({"type": event_type, **event_data})
                except Exception as e:
                    logger.error(
                        f"Error in wildcard event listener for {event_type}: {e}"
                    )

        logger.debug(f"Triggered event: {event_type}")

    def get_events(
        self, event_type: str = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get events from history, optionally filtered by type

        Args:
            event_type: Optional filter for event type
            limit: Maximum number of events to return

        Returns:
            List of event records
        """
        if event_type is None:
            return self.event_history[-limit:]

        filtered_events = [e for e in self.event_history if e["type"] == event_type]
        return filtered_events[-limit:]

    def clear_history(self) -> None:
        """Clear event history"""
        self.event_history = []
        logger.debug("Event history cleared")


class GameEvent:
    """Base class for structured game events"""

    def __init__(self, event_type: str, data: Dict[str, Any] = None):
        """
        Initialize a game event

        Args:
            event_type: The type of event
            data: Event data
        """
        self.type = event_type
        self.data = data or {}
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation"""
        return {"type": self.type, "timestamp": self.timestamp, "data": self.data}


# Predefined event types
class EventTypes:
    """Constants for common event types"""

    # Game flow events
    GAME_STARTED = "game.started"
    GAME_ENDED = "game.ended"
    GAME_PAUSED = "game.paused"
    GAME_RESUMED = "game.resumed"
    GAME_SAVED = "game.saved"
    GAME_LOADED = "game.loaded"

    # Turn events
    TURN_START = "turn.start"
    TURN_END = "turn.end"

    # Action events
    PLAYER_ACTION = "player.action"
    FACTION_ACTION = "faction.action"

    # Resource events
    RESOURCE_CHANGED = "resource.changed"
    RESOURCE_DEPLETED = "resource.depleted"

    # Faction events
    FACTION_CREATED = "faction.created"
    FACTION_DESTROYED = "faction.destroyed"
    FACTION_RELATIONSHIP_CHANGED = "faction.relationship.changed"

    # District events
    DISTRICT_CONTROL_CHANGED = "district.control.changed"
    DISTRICT_HEAT_CHANGED = "district.heat.changed"

    # Cell events
    CELL_CREATED = "cell.created"
    CELL_COMPROMISED = "cell.compromised"
    CELL_DISBANDED = "cell.disbanded"

    # Operation events
    OPERATION_STARTED = "operation.started"
    OPERATION_COMPLETED = "operation.completed"
    OPERATION_FAILED = "operation.failed"

    # SYLVA/WREN integration events
    EMOTIONAL_STATE_CHANGED = "emotional.state.changed"
    NARRATIVE_BRANCH_CREATED = "narrative.branch.created"
    SYMBOLIC_PATTERN_DETECTED = "symbolic.pattern.detected"


class EventSystem:
    """
    Narrative event generation system for Years of Lead.

    Generates contextual events with descriptions and emotional impacts
    for the game world and agent interactions.
    """

    def __init__(self, game_state=None):
        """Initialize the event system"""
        self.game_state = game_state
        self.event_templates = self._initialize_event_templates()
        self.recent_events = []
        self.recently_used_templates = (
            []
        )  # Track recently used templates to avoid repetition
        self.max_recent_templates = 5  # Don't reuse the same template for 5 events

        # Variable substitution system
        self.variable_resolvers = {
            "agent_name": self._resolve_agent_name,
            "cell_leader": self._resolve_cell_leader,
            "safehouse": self._resolve_safehouse,
            "location": self._resolve_location,
            "faction_name": self._resolve_faction_name,
            "resource_type": self._resolve_resource_type,
            "destination": self._resolve_destination,
            "hiding_place": self._resolve_hiding_place,
            "relative": self._resolve_relative,
            "district": self._resolve_district,
            "contact_name": self._resolve_contact_name,
            "city": self._resolve_city,
            "traitor_name": self._resolve_traitor_name,
            "trainer_name": self._resolve_trainer_name,
        }

        # Fallback values for common variables
        self.fallbacks = {
            "agent_name": ["an operative", "a resistance member", "one of your agents"],
            "location": ["the safehouse", "the hideout", "your base"],
            "faction_name": ["the government", "the authorities", "security forces"],
            "resource_type": ["supplies", "equipment", "materials"],
            "destination": [
                "the government facility",
                "the checkpoint",
                "the warehouse",
            ],
            "hiding_place": ["a basement", "an abandoned building", "a secret cache"],
            "relative": ["family", "a loved one", "someone from home"],
            "district": [
                "the city center",
                "the industrial zone",
                "the residential area",
            ],
            "contact_name": ["a trusted source", "an informant", "a fellow operative"],
            "city": ["the city", "this place", "your home"],
            "traitor_name": ["a trusted ally", "someone close", "a fellow operative"],
            "trainer_name": ["a veteran", "an experienced agent", "your mentor"],
        }

    def _initialize_event_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize event templates for different contexts"""
        return {
            "daily_life": [
                {
                    "description": "You wake up to the sound of helicopters circling overhead",
                    "emotional_impact": {"fear": 0.2, "anticipation": 0.1},
                    "consequences": {"time_of_day": "morning", "location": "bedroom"},
                },
                {
                    "description": "The morning news reports another crackdown in the university district",
                    "emotional_impact": {"anger": 0.3, "sadness": 0.2},
                    "consequences": {"unrest_level": 6},
                },
                {
                    "description": "You prepare a simple breakfast while checking for surveillance",
                    "emotional_impact": {"anticipation": 0.1},
                    "consequences": {"location": "kitchen", "time_of_day": "morning"},
                },
                {
                    "description": "Neighbors whisper anxiously about the increased patrols",
                    "emotional_impact": {"fear": 0.2, "trust": -0.1},
                    "consequences": {"social_tension": "high"},
                },
                {
                    "description": "You receive a coded message from a fellow resistance member",
                    "emotional_impact": {"anticipation": 0.3, "trust": 0.2},
                    "consequences": {"has_message": True},
                },
                {
                    "description": "The local market buzzes with rumors of government infiltrators",
                    "emotional_impact": {"fear": 0.3, "anger": 0.1},
                    "consequences": {"location": "market", "paranoia_level": "high"},
                },
                {
                    "description": "You notice unfamiliar faces watching from across the street",
                    "emotional_impact": {"fear": 0.4, "surprise": 0.2},
                    "consequences": {"surveillance_risk": "high"},
                },
                {
                    "description": "A childhood friend mentions seeing you in an old photograph",
                    "emotional_impact": {"joy": 0.3, "sadness": 0.1},
                    "consequences": {"nostalgia_triggered": True},
                },
                {
                    "description": "The power cuts out suddenly, leaving the block in darkness",
                    "emotional_impact": {"surprise": 0.3, "fear": 0.2},
                    "consequences": {"power_status": "off", "vulnerability": "high"},
                },
                {
                    "description": "You discover a hidden cache of supplies in an abandoned building",
                    "emotional_impact": {"joy": 0.4, "anticipation": 0.2},
                    "consequences": {"supplies_found": True, "hope_level": "increased"},
                },
                {
                    "description": "A stray cat follows you home, reminding you of simpler times",
                    "emotional_impact": {"joy": 0.2, "sadness": 0.1},
                    "consequences": {"companion_found": True},
                },
                {
                    "description": "You overhear a conversation about the resistance in a crowded café",
                    "emotional_impact": {"anticipation": 0.2, "fear": 0.1},
                    "consequences": {"intelligence_gathered": True},
                },
                {
                    "description": "The smell of fresh bread from a local bakery brings comfort",
                    "emotional_impact": {"joy": 0.1, "trust": 0.1},
                    "consequences": {"comfort_found": True},
                },
                {
                    "description": "You find an old resistance pamphlet hidden in a library book",
                    "emotional_impact": {"anticipation": 0.3, "trust": 0.2},
                    "consequences": {"intelligence_found": True},
                },
                {
                    "description": "A street musician plays a familiar revolutionary song",
                    "emotional_impact": {"joy": 0.2, "anticipation": 0.2},
                    "consequences": {"morale_boosted": True},
                },
                {
                    "description": "You witness a small act of kindness between strangers",
                    "emotional_impact": {"joy": 0.2, "trust": 0.2},
                    "consequences": {"hope_restored": True},
                },
                {
                    "description": "The sound of distant explosions echoes through the night",
                    "emotional_impact": {"fear": 0.3, "anger": 0.2},
                    "consequences": {"violence_nearby": True},
                },
                {
                    "description": "You find graffiti supporting the resistance on a wall",
                    "emotional_impact": {"joy": 0.2, "anticipation": 0.2},
                    "consequences": {"resistance_visible": True},
                },
                {
                    "description": "A child asks you about the meaning of freedom",
                    "emotional_impact": {"joy": 0.3, "sadness": 0.1},
                    "consequences": {"teaching_moment": True},
                },
                {
                    "description": "You discover a secret passage in an old building",
                    "emotional_impact": {"anticipation": 0.4, "fear": 0.1},
                    "consequences": {"escape_route_found": True},
                },
                {
                    "description": "A radio broadcast crackles with static, then suddenly clears to reveal a resistance message",
                    "emotional_impact": {"anticipation": 0.3, "joy": 0.2},
                    "consequences": {"communication_established": True},
                },
                {
                    "description": "You find an old photograph hidden in a book, showing happier times before the occupation",
                    "emotional_impact": {"sadness": 0.3, "joy": 0.2},
                    "consequences": {"memory_triggered": True},
                },
                {
                    "description": "A neighbor leaves a small package on your doorstep, a silent gesture of solidarity",
                    "emotional_impact": {"trust": 0.3, "joy": 0.2},
                    "consequences": {"community_support": True},
                },
                {
                    "description": "The sound of distant church bells echoes through the empty streets, a reminder of normalcy",
                    "emotional_impact": {"sadness": 0.2, "hope": 0.1},
                    "consequences": {"nostalgia_triggered": True},
                },
                {
                    "description": "A black cat crosses your path. Most forboding.",
                    "emotional_impact": {"fear": 0.2, "anticipation": 0.2},
                    "consequences": {"omen_seen": True},
                },
                {
                    "description": "You help an unhoused man pick up his belongings after a cop scattered them. You feel like a damn superhero.",
                    "emotional_impact": {"pride": 0.3, "anger": 0.2},
                    "consequences": {
                        "dignity_defended": True,
                        "cop_abuse_witnessed": True,
                    },
                },
                {
                    "description": 'You see "ACAB" written on a bus bench. Very based.',
                    "emotional_impact": {"defiance": 0.3, "solidarity": 0.2},
                    "consequences": {"radical_message_seen": True},
                },
                {
                    "description": "You watch a child give their snack to someone hungrier than them.",
                    "emotional_impact": {"hope": 0.4, "tenderness": 0.3},
                    "consequences": {"solidarity_witnessed": True},
                },
                {
                    "description": "You hear a siren and instinctively duck into an alley. Old reflexes, never dead.",
                    "emotional_impact": {"fear": 0.3, "alertness": 0.2},
                    "consequences": {"paranoia_triggered": True},
                },
                {
                    "description": "Someone slides a zine into your bag. Later, you read about prison abolition.",
                    "emotional_impact": {"curiosity": 0.3, "inspiration": 0.2},
                    "consequences": {"radicalized_further": True},
                },
                {
                    "description": "The cafe you're in gives away yesterday's bread to those in need.",
                    "emotional_impact": {"trust": 0.3, "warmth": 0.2},
                    "consequences": {"community_support_seen": True},
                },
                {
                    "description": "You find a patch on the ground: a red star with faded threads.",
                    "emotional_impact": {"nostalgia": 0.2, "respect": 0.3},
                    "consequences": {"symbol_found": True},
                },
                {
                    "description": 'A teen tags "No Justice, No Peace" in chalk on a school wall.',
                    "emotional_impact": {"pride": 0.3, "hope": 0.2},
                    "consequences": {"youth_resistance_seen": True},
                },
                {
                    "description": "You notice two plainclothes officers tailing someone down the street.",
                    "emotional_impact": {"suspicion": 0.4, "anger": 0.2},
                    "consequences": {"surveillance_detected": True},
                },
                {
                    "description": "A memorial candle flickers on a sidewalk corner. Someone remembers the fallen.",
                    "emotional_impact": {"sadness": 0.3, "resolve": 0.2},
                    "consequences": {"martyr_recognized": True},
                },
                {
                    "description": "Your neighbor knocks to share soup. No words exchanged, just survival.",
                    "emotional_impact": {"trust": 0.4, "peace": 0.2},
                    "consequences": {"mutual_aid": True},
                },
                {
                    "description": "You spot a drone scanning faces at the market. Nobody reacts.",
                    "emotional_impact": {"dread": 0.3, "resignation": 0.2},
                    "consequences": {"surveillance_normalized": True},
                },
                {
                    "description": "You catch your own reflection in a shattered shop window. You look… changed.",
                    "emotional_impact": {"reflection": 0.3, "dissociation": 0.2},
                    "consequences": {"self_awareness_shifted": True},
                },
                {
                    "description": "A flute plays softly in a metro tunnel, briefly turning ruin into ritual.",
                    "emotional_impact": {"beauty": 0.3, "melancholy": 0.2},
                    "consequences": {"art_encountered": True},
                },
                {
                    "description": 'A flyer flutters onto your boot: "The people will not forget." You take it with you.',
                    "emotional_impact": {"anticipation": 0.3, "solidarity": 0.2},
                    "consequences": {"propaganda_found": True},
                },
                {
                    "description": "You notice a building wall now blank where a mural once stood. Censored, scrubbed.",
                    "emotional_impact": {"sadness": 0.3, "anger": 0.2},
                    "consequences": {"art_destroyed": True},
                },
                {
                    "description": "A kid asks if you're a freedom fighter. You don't know how to answer.",
                    "emotional_impact": {"uncertainty": 0.3, "pride": 0.2},
                    "consequences": {"identity_questioned": True},
                },
                {
                    "description": "Two friends hold hands walking past a checkpoint. No one dares stop them.",
                    "emotional_impact": {"joy": 0.2, "defiance": 0.3},
                    "consequences": {"love_visible": True},
                },
                {
                    "description": 'Someone tucks a pack of cigarettes into your hand—"For the long night."',
                    "emotional_impact": {"trust": 0.2, "dread": 0.2},
                    "consequences": {"gift_received": True},
                },
                {
                    "description": "The city smells like smoke today. No fires in sight.",
                    "emotional_impact": {"foreboding": 0.3, "confusion": 0.2},
                    "consequences": {"unseen_threat": True},
                },
                {
                    "description": "You watch pigeons settle on a statue missing its head.",
                    "emotional_impact": {"absurdity": 0.2, "nostalgia": 0.2},
                    "consequences": {"history_cracked": True},
                },
                {
                    "description": "A stranger nods to you in a crowd. No words, but you understand.",
                    "emotional_impact": {"connection": 0.3, "anticipation": 0.2},
                    "consequences": {"contact_made": True},
                },
                {
                    "description": "You walk past a shuttered bookstore. Its window holds a single banned title.",
                    "emotional_impact": {"curiosity": 0.2, "loss": 0.3},
                    "consequences": {"resistance_signal": True},
                },
                {
                    "description": "Someone's dog barks at a patrol vehicle, refusing to be silenced.",
                    "emotional_impact": {"humor": 0.2, "resistance": 0.2},
                    "consequences": {"animal_rebellion": True},
                },
                {
                    "description": "You see someone take off their ID badge and toss it in the gutter.",
                    "emotional_impact": {"liberation": 0.3, "shock": 0.2},
                    "consequences": {"resignation_witnessed": True},
                },
                {
                    "description": "A street artist paints over an old billboard with revolutionary colors.",
                    "emotional_impact": {"joy": 0.2, "inspiration": 0.3},
                    "consequences": {"art_created": True},
                },
                {
                    "description": "The wind carries someone's chant down the avenue, far from the protest site.",
                    "emotional_impact": {"hope": 0.2, "resolve": 0.3},
                    "consequences": {"chant_heard": True},
                },
                {
                    "description": 'A message scratched into a doorframe: "Still here."',
                    "emotional_impact": {"solidarity": 0.3, "grit": 0.2},
                    "consequences": {"survivor_mark": True},
                },
                {
                    "description": "Someone leaves a loaf of bread wrapped in a scarf on a stoop. No note.",
                    "emotional_impact": {"kindness": 0.3, "mystery": 0.2},
                    "consequences": {"aid_received": True},
                },
                {
                    "description": "You see an officer trip and drop his baton. The silence is loaded.",
                    "emotional_impact": {"schadenfreude": 0.3, "tension": 0.2},
                    "consequences": {"power_slipped": True},
                },
                {
                    "description": "A pigeon wears a tiny red ribbon around its leg. You wonder who trained it.",
                    "emotional_impact": {"curiosity": 0.4},
                    "consequences": {"signal_seen": True},
                },
                {
                    "description": "You notice fresh tire tracks near a known activist's hideout.",
                    "emotional_impact": {"worry": 0.3, "alertness": 0.2},
                    "consequences": {"pursuit_implied": True},
                },
                {
                    "description": "A grandmother slaps a cop's hand away from her produce basket. The crowd erupts.",
                    "emotional_impact": {"joy": 0.2, "empowerment": 0.4},
                    "consequences": {"elder_defiance": True},
                },
                {
                    "description": 'You stop in front of a public mirror tagged with "You are needed."',
                    "emotional_impact": {"motivation": 0.3, "reflection": 0.2},
                    "consequences": {"call_to_action": True},
                },
            ],
            "resistance_operations": [
                {
                    "description": "Your cell successfully distributes propaganda leaflets across the district",
                    "emotional_impact": {"joy": 0.4, "anticipation": 0.3},
                    "consequences": {"operation_success": True, "influence": 5},
                },
                {
                    "description": "Government forces raid a safe house, but find it already evacuated",
                    "emotional_impact": {"relief": 0.3, "fear": 0.2},
                    "consequences": {"safe_house_status": "compromised"},
                },
                {
                    "description": "A new recruit shows promising skills in stealth operations",
                    "emotional_impact": {"hope": 0.3, "trust": 0.2},
                    "consequences": {"recruitment_success": True},
                },
                {
                    "description": "Intelligence suggests government forces are planning a major sweep",
                    "emotional_impact": {"fear": 0.4, "anticipation": 0.3},
                    "consequences": {"threat_level": "high", "planning_required": True},
                },
            ],
            "trauma_events": [
                {
                    "description": "You witness government forces brutally dispersing peaceful protesters",
                    "emotional_impact": {"fear": 0.7, "anger": 0.6, "sadness": 0.5},
                    "type": "violence_witnessed",
                    "severity": 0.8,
                    "consequences": {"trauma_witnessed": True, "trust_in_system": -0.8},
                },
                {
                    "description": "A trusted comrade is arrested and doesn't return from interrogation",
                    "emotional_impact": {"sadness": 0.8, "fear": 0.6, "anger": 0.7},
                    "type": "loss_of_comrade",
                    "severity": 0.9,
                    "consequences": {
                        "comrade_lost": True,
                        "operation_compromised": True,
                    },
                },
                {
                    "description": "You discover that someone you trusted has been informing the authorities",
                    "emotional_impact": {"anger": 0.8, "trust": -0.9, "sadness": 0.4},
                    "type": "betrayal",
                    "severity": 0.8,
                    "consequences": {
                        "trust_betrayed": True,
                        "network_compromised": True,
                    },
                },
            ],
            "covert_operations": [
                {
                    "description": "{agent_name} intercepts a government transmission, revealing their next move. The information is rushed to {cell_leader}, who immediately calls for a midnight meeting at {safehouse}.",
                    "emotional_impact": {"anticipation": 0.3, "trust": 0.2},
                    "consequences": {"intel_gathered": True},
                },
                {
                    "description": "A coded message arrives at {location}, instructing your team to sabotage a key power relay. The operation must be completed before dawn, or the opportunity will be lost.",
                    "emotional_impact": {"anticipation": 0.4, "fear": 0.2},
                    "consequences": {"mission_timer": "urgent"},
                },
            ],
            "public_unrest": [
                {
                    "description": "A spontaneous protest erupts in {location}, drawing a heavy response from {faction_name}. The crowd's chants echo through the streets long after the last demonstrator is dragged away.",
                    "emotional_impact": {"anger": 0.3, "sadness": 0.2},
                    "consequences": {"unrest_level": "increased"},
                },
                {
                    "description": "Striking workers block the main avenue, demanding justice for recent arrests. Police form a barricade, and tension mounts as the standoff drags on.",
                    "emotional_impact": {"fear": 0.2, "anticipation": 0.3},
                    "consequences": {"strike": True},
                },
            ],
            "resource_management": [
                {
                    "description": "A shipment of {resource_type} is intercepted by your operatives before it reaches {destination}. The crates are hidden in {hiding_place}, destined for families in need.",
                    "emotional_impact": {"joy": 0.3, "trust": 0.2},
                    "consequences": {"resources_gained": True},
                },
                {
                    "description": "Supplies run dangerously low in {location}, forcing your cell to ration food and medicine. Morale suffers as agents debate how to stretch the dwindling stockpile.",
                    "emotional_impact": {"sadness": 0.3, "fear": 0.2},
                    "consequences": {"morale": "decreased"},
                },
            ],
            "agent_personal_life": [
                {
                    "description": "{agent_name} receives a letter from {relative}, rekindling memories of a peaceful past. The words bring both comfort and a sharp pang of longing for what's been lost.",
                    "emotional_impact": {"joy": 0.2, "sadness": 0.3},
                    "consequences": {"memory_triggered": True},
                },
                {
                    "description": "Rumors spread that {agent_name} has been seen meeting with a mysterious stranger. Some in the cell grow suspicious, while others urge trust and patience.",
                    "emotional_impact": {"trust": -0.2, "anticipation": 0.2},
                    "consequences": {"suspicion": True},
                },
            ],
            "government_actions": [
                {
                    "description": "The government imposes a curfew in {district}, restricting movement after dark. Patrols double in number, and the city's nightlife vanishes overnight.",
                    "emotional_impact": {"fear": 0.3, "anger": 0.2},
                    "consequences": {"curfew": True},
                },
                {
                    "description": "A new propaganda campaign floods the airwaves, painting the resistance as criminals. Some citizens begin to question their loyalties, while others grow more defiant.",
                    "emotional_impact": {"anger": 0.3, "trust": -0.2},
                    "consequences": {"public_opinion": "shifted"},
                },
            ],
            "underground_network": [
                {
                    "description": "A coded message leads you to a hidden safehouse beneath {location}. Inside, {contact_name} waits with news that could change the course of the resistance.",
                    "emotional_impact": {"anticipation": 0.3, "trust": 0.2},
                    "consequences": {"intel_gathered": True},
                },
                {
                    "description": "A secret meeting is held in the back room of {location}, where plans for the next operation are drawn up. The air is thick with tension and hope.",
                    "emotional_impact": {"anticipation": 0.3, "joy": 0.2},
                    "consequences": {"plans_made": True},
                },
            ],
            "international_affairs": [
                {
                    "description": "A foreign journalist publishes a report on the resistance in {city}, drawing global attention to your struggle. The government scrambles to control the narrative, but whispers of support begin to cross the border.",
                    "emotional_impact": {"hope": 0.3, "anticipation": 0.2},
                    "consequences": {"international_attention": True},
                },
                {
                    "description": "An aid package arrives from abroad, smuggled in under the cover of night. The supplies are a lifeline, but also draw the suspicion of local authorities.",
                    "emotional_impact": {"joy": 0.3, "fear": 0.2},
                    "consequences": {"resources_gained": True, "risk_increased": True},
                },
            ],
            "morale_and_hope": [
                {
                    "description": "A small victory inspires hope among the resistance fighters in {safehouse}. For the first time in weeks, laughter and song fill the air.",
                    "emotional_impact": {"joy": 0.3, "hope": 0.3},
                    "consequences": {"morale": "increased"},
                },
                {
                    "description": "A respected leader delivers a rousing speech, reminding everyone what they're fighting for. Spirits lift as agents rededicate themselves to the cause.",
                    "emotional_impact": {"hope": 0.4, "trust": 0.2},
                    "consequences": {"morale": "increased"},
                },
            ],
            "betrayal_and_intrigue": [
                {
                    "description": "A trusted ally, {traitor_name}, is revealed to be a government informant, sending shockwaves through your ranks. Paranoia spreads as everyone wonders who might be next.",
                    "emotional_impact": {"anger": 0.4, "trust": -0.5},
                    "consequences": {"trust_betrayed": True},
                },
                {
                    "description": "A coded warning arrives just in time, allowing your cell to avoid a deadly ambush. The source remains unknown, fueling both gratitude and suspicion.",
                    "emotional_impact": {"relief": 0.3, "anticipation": 0.2},
                    "consequences": {"danger_avoided": True},
                },
            ],
            "training_and_recruitment": [
                {
                    "description": "A group of new recruits completes their first training mission under {trainer_name}, their faces a mix of pride and exhaustion. {cell_leader} nods approvingly, already planning their next assignment.",
                    "emotional_impact": {"joy": 0.2, "anticipation": 0.2},
                    "consequences": {"recruits_trained": True},
                },
                {
                    "description": "A veteran agent shares hard-won lessons with the younger members of the cell. The stories are sobering, but everyone leaves the session better prepared for what lies ahead.",
                    "emotional_impact": {"trust": 0.2, "anticipation": 0.2},
                    "consequences": {"training_complete": True},
                },
            ],
        }

    def generate_event(
        self, event_category: str, context: Dict[str, Any] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a contextual event based on category and current context.

        Args:
            event_category: Category of event to generate ('daily_life', 'resistance_operations', etc.)
            context: Current game context to influence event selection

        Returns:
            Generated event with description, emotional impact, and consequences
        """
        if event_category not in self.event_templates:
            return None

        context = context or {}
        templates = self.event_templates[event_category]

        # Filter out recently used templates to ensure variety
        available_templates = []
        for i, template in enumerate(templates):
            if i not in self.recently_used_templates:
                available_templates.append((i, template))

        # If all templates have been recently used, reset the tracking
        if not available_templates:
            self.recently_used_templates = []
            available_templates = [
                (i, template) for i, template in enumerate(templates)
            ]

        # Select a template that hasn't been recently used
        import random

        selected_index, template = random.choice(available_templates)

        # Track this template as recently used
        self.recently_used_templates.append(selected_index)
        if len(self.recently_used_templates) > self.max_recent_templates:
            self.recently_used_templates.pop(0)

        # Create event from template
        event = {
            "category": event_category,
            "description": self._substitute_variables(template["description"], context),
            "emotional_impact": template.get("emotional_impact", {}),
            "consequences": template.get("consequences", {}),
            "type": template.get("type", "general"),
            "severity": template.get("severity", 0.3),
            "context": context,
        }

        # Apply context-based modifications
        event = self._apply_context_modifications(event, context)

        # Store in recent events
        self.recent_events.append(event)
        if len(self.recent_events) > 50:  # Keep only recent events
            self.recent_events = self.recent_events[-50:]

        return event

    def _apply_context_modifications(
        self, event: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply context-based modifications to generated events.
        This allows events to be influenced by current game state.
        """
        # Modify emotional impact based on context
        if context.get("time_of_day") == "night":
            # Night events are more fearful
            if "fear" in event["emotional_impact"]:
                event["emotional_impact"]["fear"] *= 1.2

        if context.get("location") == "government_quarter":
            # Events in government quarter are more tense
            event["emotional_impact"]["fear"] = (
                event["emotional_impact"].get("fear", 0) + 0.1
            )
            event["emotional_impact"]["anticipation"] = (
                event["emotional_impact"].get("anticipation", 0) + 0.1
            )

        # Modify consequences based on context
        if context.get("recent_events"):
            # If recent events included violence, increase fear in current event
            recent_violence = any(
                "violence" in str(recent_event).lower()
                for recent_event in context["recent_events"]
            )
            if recent_violence:
                event["emotional_impact"]["fear"] = (
                    event["emotional_impact"].get("fear", 0) + 0.2
                )

        return event

    def get_recent_events(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent events for context"""
        return self.recent_events[-count:] if self.recent_events else []

    def _resolve_agent_name(self, context: Dict[str, Any]) -> str:
        """Resolve agent name with fallbacks"""
        if self.game_state and self.game_state.agents:
            # Try to get a random active agent
            active_agents = [
                agent
                for agent in self.game_state.agents.values()
                if agent.status.value == "active"
            ]
            if active_agents:
                import random

                return random.choice(active_agents).name

        # Fallback to context or default
        return context.get("agent_name", self._get_random_fallback("agent_name"))

    def _resolve_cell_leader(self, context: Dict[str, Any]) -> str:
        """Resolve cell leader with fallbacks"""
        if self.game_state and self.game_state.agents:
            # Look for agents with leadership roles or high skills
            potential_leaders = []
            for agent in self.game_state.agents.values():
                if (
                    agent.status.value == "active"
                    and hasattr(agent.skills, "get")
                    and agent.skills.get("persuasion", 0).level > 2
                ):
                    potential_leaders.append(agent.name)

            if potential_leaders:
                import random

                return random.choice(potential_leaders)

        return context.get("cell_leader", "your cell leader")

    def _resolve_safehouse(self, context: Dict[str, Any]) -> str:
        """Resolve safehouse with fallbacks"""
        if self.game_state and self.game_state.locations:
            # Look for locations with low security (potential safehouses)
            safe_locations = []
            for location in self.game_state.locations.values():
                if location.security_level < 4:  # Low security = safer
                    safe_locations.append(location.name)

            if safe_locations:
                import random

                return random.choice(safe_locations)

        return context.get("safehouse", self._get_random_fallback("location"))

    def _resolve_location(self, context: Dict[str, Any]) -> str:
        """Resolve location with fallbacks"""
        if self.game_state and self.game_state.locations:
            import random

            return random.choice(list(self.game_state.locations.values())).name

        return context.get("location", self._get_random_fallback("location"))

    def _resolve_faction_name(self, context: Dict[str, Any]) -> str:
        """Resolve faction name with fallbacks"""
        if self.game_state and self.game_state.factions:
            import random

            return random.choice(list(self.game_state.factions.values())).name

        return context.get("faction_name", self._get_random_fallback("faction_name"))

    def _resolve_resource_type(self, context: Dict[str, Any]) -> str:
        """Resolve resource type with fallbacks"""
        resource_types = [
            "medical supplies",
            "weapons",
            "food",
            "communications equipment",
            "explosives",
            "intelligence documents",
            "money",
            "clothing",
        ]
        import random

        return context.get("resource_type", random.choice(resource_types))

    def _resolve_destination(self, context: Dict[str, Any]) -> str:
        """Resolve destination with fallbacks"""
        destinations = [
            "the government facility",
            "the military checkpoint",
            "the police station",
            "the warehouse district",
            "the port",
            "the airport",
        ]
        import random

        return context.get("destination", random.choice(destinations))

    def _resolve_hiding_place(self, context: Dict[str, Any]) -> str:
        """Resolve hiding place with fallbacks"""
        hiding_places = [
            "a basement",
            "an abandoned building",
            "a secret cache",
            "a tunnel",
            "a rooftop",
            "a sewer",
            "an attic",
            "a cellar",
        ]
        import random

        return context.get("hiding_place", random.choice(hiding_places))

    def _resolve_relative(self, context: Dict[str, Any]) -> str:
        """Resolve relative with fallbacks"""
        relatives = [
            "family",
            "a loved one",
            "someone from home",
            "an old friend",
            "a childhood companion",
            "a distant relative",
        ]
        import random

        return context.get("relative", random.choice(relatives))

    def _resolve_district(self, context: Dict[str, Any]) -> str:
        """Resolve district with fallbacks"""
        districts = [
            "the city center",
            "the industrial zone",
            "the residential area",
            "the university district",
            "the old town",
            "the suburbs",
        ]
        import random

        return context.get("district", random.choice(districts))

    def _resolve_contact_name(self, context: Dict[str, Any]) -> str:
        """Resolve contact name with fallbacks"""
        if self.game_state and self.game_state.agents:
            import random

            return random.choice(list(self.game_state.agents.values())).name

        return context.get("contact_name", self._get_random_fallback("contact_name"))

    def _resolve_city(self, context: Dict[str, Any]) -> str:
        """Resolve city with fallbacks"""
        cities = [
            "the city",
            "this place",
            "your home",
            "the capital",
            "the metropolis",
        ]
        import random

        return context.get("city", random.choice(cities))

    def _resolve_traitor_name(self, context: Dict[str, Any]) -> str:
        """Resolve traitor name with fallbacks"""
        if self.game_state and self.game_state.agents:
            import random

            return random.choice(list(self.game_state.agents.values())).name

        return context.get("traitor_name", self._get_random_fallback("traitor_name"))

    def _resolve_trainer_name(self, context: Dict[str, Any]) -> str:
        """Resolve trainer name with fallbacks"""
        if self.game_state and self.game_state.agents:
            # Look for experienced agents
            experienced_agents = []
            for agent in self.game_state.agents.values():
                if agent.status.value == "active":
                    total_skill = sum(skill.level for skill in agent.skills.values())
                    if total_skill > 10:  # Experienced agent
                        experienced_agents.append(agent.name)

            if experienced_agents:
                import random

                return random.choice(experienced_agents)

        return context.get("trainer_name", "a veteran agent")

    def _get_random_fallback(self, variable_name: str) -> str:
        """Get a random fallback value for a variable"""
        if variable_name in self.fallbacks:
            import random

            return random.choice(self.fallbacks[variable_name])
        return f"{{{variable_name}}}"

    def _substitute_variables(self, template: str, context: Dict[str, Any]) -> str:
        """Substitute variables in a template string with robust fallbacks"""
        try:
            # Find all variables in the template
            import re

            variable_pattern = r"\{([^}]+)\}"
            variables = re.findall(variable_pattern, template)

            # Build substitution dictionary
            substitutions = {}
            for var_name in variables:
                if var_name in self.variable_resolvers:
                    substitutions[var_name] = self.variable_resolvers[var_name](context)
                else:
                    # Unknown variable, use context or fallback
                    substitutions[var_name] = context.get(var_name, f"{{{var_name}}}")

            # Perform substitution with error handling
            try:
                return template.format(**substitutions)
            except (KeyError, ValueError):
                # If substitution fails, try with safe fallbacks
                safe_substitutions = {}
                for var_name in variables:
                    safe_substitutions[var_name] = substitutions.get(
                        var_name, f"{{{var_name}}}"
                    )

                try:
                    return template.format(**safe_substitutions)
                except (KeyError, ValueError):
                    # Last resort: replace with generic text
                    return template.replace("{", "").replace("}", "")

        except Exception:
            # If all else fails, return the original template
            return template
