"""
Dynamic Narrative Tone System for Years of Lead

This module implements a system that dynamically shapes the tone of narrative dialog
based on both predefined filters and player-authored contributions, integrating with
SYLVA/WREN-style emotional tagging for enhanced storytelling.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import random
import json
import re
from loguru import logger


class EmotionalTone(Enum):
    """Core emotional tones for narrative filtering"""
    WRY = "wry"
    TRAGIC = "tragic"
    REBELLIOUS = "rebellious"
    SARDONIC = "sardonic"
    NOSTALGIC = "nostalgic"
    DEFIANT = "defiant"
    MELANCHOLIC = "melancholic"
    HOPEFUL = "hopeful"
    BITTER = "bitter"
    ROMANTIC = "romantic"
    CYNICAL = "cynical"
    IDEALISTIC = "idealistic"


class SymbolicElement(Enum):
    """Symbolic elements that can influence narrative generation"""
    SMALL_OBJECTS = "small objects"
    GRAFFITI = "graffiti"
    GHOST_SPACES = "ghost spaces"
    BROKEN_GLASS = "broken glass"
    CIGARETTES = "cigarettes"
    COFFEE = "coffee"
    FLOWERS = "flowers"
    STATUES = "statues"
    SHADOWS = "shadows"
    RAIN = "rain"
    MUSIC = "music"
    PHOTOGRAPHS = "photographs"


class NarrativeStyle(Enum):
    """Style characteristics for voice generation"""
    ONE_LINERS = "likes one-liners"
    SARCASM_COPING = "uses sarcasm to cope"
    BEAUTY_IN_DESTRUCTION = "notices beauty in destruction"
    DRY_HUMOR = "dry humor"
    POETIC_LANGUAGE = "poetic language"
    SHORT_SENTENCES = "prefers short sentences"
    METAPHORICAL = "speaks metaphorically"
    DIRECT_SPEECH = "direct and blunt"
    INTROSPECTIVE = "tends to introspect"
    OBSERVATIONAL = "notices small details"


@dataclass
class PlayerAuthoredLine:
    """A single line authored by the player to influence future narrative"""
    content: str
    emotional_tone: Optional[EmotionalTone] = None
    symbolic_elements: Set[SymbolicElement] = field(default_factory=set)
    style_markers: Set[NarrativeStyle] = field(default_factory=set)
    usage_count: int = 0
    created_turn: int = 0
    effectiveness_rating: float = 1.0  # How well this line influences generation

    def analyze_line(self):
        """Automatically analyze the line for emotional tone, symbols, and style"""
        content_lower = self.content.lower()

        # Detect symbolic elements
        symbol_keywords = {
            SymbolicElement.SMALL_OBJECTS: ["coin", "key", "button", "ring", "lighter"],
            SymbolicElement.GRAFFITI: ["wall", "spray", "paint", "mark", "tag"],
            SymbolicElement.GHOST_SPACES: ["empty", "abandoned", "silence", "echo"],
            SymbolicElement.BROKEN_GLASS: ["glass", "shatter", "fragment", "shard"],
            SymbolicElement.CIGARETTES: ["smoke", "tobacco", "ash", "cigarette"],
            SymbolicElement.COFFEE: ["coffee", "brew", "cup", "steam"],
            SymbolicElement.FLOWERS: ["flower", "petal", "bloom", "wilt"],
            SymbolicElement.STATUES: ["statue", "monument", "stone", "marble"],
            SymbolicElement.SHADOWS: ["shadow", "dark", "silhouette"],
            SymbolicElement.RAIN: ["rain", "wet", "drip", "storm"],
            SymbolicElement.MUSIC: ["song", "melody", "rhythm", "tune"],
            SymbolicElement.PHOTOGRAPHS: ["photo", "picture", "image", "memory"]
        }

        for symbol, keywords in symbol_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                self.symbolic_elements.add(symbol)

        # Detect style markers
        if len([s for s in self.content.split('.') if s.strip()]) == 1 and len(self.content) < 50:
            self.style_markers.add(NarrativeStyle.ONE_LINERS)

        if any(word in content_lower for word in ["beauty", "beautiful", "broken", "ruin"]):
            self.style_markers.add(NarrativeStyle.BEAUTY_IN_DESTRUCTION)

        if self.content.count('.') >= 2 and "." in self.content[:-1]:
            self.style_markers.add(NarrativeStyle.SHORT_SENTENCES)

        # Detect emotional tone patterns
        if any(word in content_lower for word in ["mistake", "wrong", "again"]):
            self.emotional_tone = EmotionalTone.WRY
        elif any(word in content_lower for word in ["carnation", "red", "regime"]):
            self.emotional_tone = EmotionalTone.SARDONIC
        elif any(word in content_lower for word in ["beauty", "right", "squint"]):
            self.emotional_tone = EmotionalTone.MELANCHOLIC


@dataclass
class VoiceConfiguration:
    """Complete voice configuration for a character's narrative generation"""
    character_id: str
    emotional_tones: List[EmotionalTone] = field(default_factory=list)
    symbolic_preferences: List[SymbolicElement] = field(default_factory=list)
    style_notes: List[NarrativeStyle] = field(default_factory=list)
    player_authored_lines: List[PlayerAuthoredLine] = field(default_factory=list)

    # Advanced settings
    tone_consistency_weight: float = 0.7  # How strongly to maintain consistent tone
    player_line_influence: float = 0.5    # How much player lines influence generation
    symbolic_density: float = 0.3         # How often to include symbolic elements

    # Learning parameters
    successful_patterns: Dict[str, int] = field(default_factory=dict)
    avoided_patterns: Dict[str, int] = field(default_factory=dict)

    def add_player_line(self, content: str, turn: int = 0) -> PlayerAuthoredLine:
        """Add a new player-authored line and analyze it"""
        line = PlayerAuthoredLine(content=content, created_turn=turn)
        line.analyze_line()
        self.player_authored_lines.append(line)

        # Update preferences based on the new line
        if line.emotional_tone:
            if line.emotional_tone not in self.emotional_tones:
                self.emotional_tones.append(line.emotional_tone)

        for symbol in line.symbolic_elements:
            if symbol not in self.symbolic_preferences:
                self.symbolic_preferences.append(symbol)

        for style in line.style_markers:
            if style not in self.style_notes:
                self.style_notes.append(style)

        logger.info(f"Added player line for {self.character_id}: {content[:50]}...")
        return line

    def get_recent_lines(self, count: int = 5) -> List[PlayerAuthoredLine]:
        """Get the most recently added player lines"""
        return sorted(self.player_authored_lines,
                     key=lambda x: x.created_turn, reverse=True)[:count]

    def get_effective_lines(self, min_rating: float = 0.7) -> List[PlayerAuthoredLine]:
        """Get player lines that have been effective at influencing generation"""
        return [line for line in self.player_authored_lines
                if line.effectiveness_rating >= min_rating]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize voice configuration to dictionary"""
        return {
            "character_id": self.character_id,
            "emotional_tones": [tone.value for tone in self.emotional_tones],
            "symbolic_preferences": [symbol.value for symbol in self.symbolic_preferences],
            "style_notes": [style.value for style in self.style_notes],
            "player_authored_lines": [
                {
                    "content": line.content,
                    "emotional_tone": line.emotional_tone.value if line.emotional_tone else None,
                    "symbolic_elements": [elem.value for elem in line.symbolic_elements],
                    "style_markers": [style.value for style in line.style_markers],
                    "usage_count": line.usage_count,
                    "created_turn": line.created_turn,
                    "effectiveness_rating": line.effectiveness_rating
                }
                for line in self.player_authored_lines
            ],
            "tone_consistency_weight": self.tone_consistency_weight,
            "player_line_influence": self.player_line_influence,
            "symbolic_density": self.symbolic_density,
            "successful_patterns": self.successful_patterns,
            "avoided_patterns": self.avoided_patterns
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceConfiguration':
        """Deserialize voice configuration from dictionary"""
        config = cls(character_id=data["character_id"])

        config.emotional_tones = [EmotionalTone(tone) for tone in data.get("emotional_tones", [])]
        config.symbolic_preferences = [SymbolicElement(symbol) for symbol in data.get("symbolic_preferences", [])]
        config.style_notes = [NarrativeStyle(style) for style in data.get("style_notes", [])]

        config.tone_consistency_weight = data.get("tone_consistency_weight", 0.7)
        config.player_line_influence = data.get("player_line_influence", 0.5)
        config.symbolic_density = data.get("symbolic_density", 0.3)
        config.successful_patterns = data.get("successful_patterns", {})
        config.avoided_patterns = data.get("avoided_patterns", {})

        # Reconstruct player lines
        for line_data in data.get("player_authored_lines", []):
            line = PlayerAuthoredLine(
                content=line_data["content"],
                emotional_tone=EmotionalTone(line_data["emotional_tone"]) if line_data["emotional_tone"] else None,
                symbolic_elements=set(SymbolicElement(elem) for elem in line_data.get("symbolic_elements", [])),
                style_markers=set(NarrativeStyle(style) for style in line_data.get("style_markers", [])),
                usage_count=line_data.get("usage_count", 0),
                created_turn=line_data.get("created_turn", 0),
                effectiveness_rating=line_data.get("effectiveness_rating", 1.0)
            )
            config.player_authored_lines.append(line)

        return config


class DynamicNarrativeToneEngine:
    """Engine for generating narrative content with dynamic tone based on voice configuration"""

    def __init__(self):
        self.voice_configurations: Dict[str, VoiceConfiguration] = {}
        self.tone_templates: Dict[EmotionalTone, List[str]] = self._initialize_tone_templates()
        self.style_patterns: Dict[NarrativeStyle, List[str]] = self._initialize_style_patterns()
        self.symbol_templates: Dict[SymbolicElement, List[str]] = self._initialize_symbol_templates()

    def _initialize_tone_templates(self) -> Dict[EmotionalTone, List[str]]:
        """Initialize base templates for different emotional tones"""
        return {
            EmotionalTone.WRY: [
                "You {action}. {observation}. Of course.",
                "The {object} {state}. You're not surprised.",
                "{action_result}. That figures.",
                "You {action}. Wrong again."
            ],
            EmotionalTone.TRAGIC: [
                "You {action}, remembering {memory}.",
                "The {object} reminds you of what's lost.",
                "{action_result}, like everything else.",
                "You {action}, feeling the weight of {emotion}."
            ],
            EmotionalTone.REBELLIOUS: [
                "You {action} despite {authority}.",
                "The {object} represents everything wrong with {system}.",
                "You {action}. They can't stop you.",
                "Let them try to {threat}. You {action} anyway."
            ],
            EmotionalTone.SARDONIC: [
                "You {action}. How {adjective}.",
                "The {object} {state}. Perfect, just perfect.",
                "{action_result}. What else is new?",
                "You {action}. The irony isn't lost on you."
            ],
            EmotionalTone.MELANCHOLIC: [
                "You {action}, thinking of {past}.",
                "The {object} holds echoes of {memory}.",
                "{action_result}, like autumn leaves.",
                "You {action} with the weight of {emotion}."
            ]
        }

    def _initialize_style_patterns(self) -> Dict[NarrativeStyle, List[str]]:
        """Initialize patterns for different narrative styles"""
        return {
            NarrativeStyle.ONE_LINERS: [
                "{simple_statement}.",
                "{observation}.",
                "{action_result}."
            ],
            NarrativeStyle.SHORT_SENTENCES: [
                "{action}. {observation}. {consequence}.",
                "{statement}. {reaction}. {outcome}.",
                "{event}. {feeling}. {decision}."
            ],
            NarrativeStyle.BEAUTY_IN_DESTRUCTION: [
                "The broken {object} catches light beautifully.",
                "There's something lovely about the way {destruction} spreads.",
                "You find beauty in the {damaged_thing}'s fractures."
            ],
            NarrativeStyle.SARCASM_COPING: [
                "You {action}. How delightfully {ironic_adjective}.",
                "Oh wonderful, {situation}. Just what you needed.",
                "Perfect. {problem}. Your day is complete."
            ]
        }

    def _initialize_symbol_templates(self) -> Dict[SymbolicElement, List[str]]:
        """Initialize templates that incorporate symbolic elements"""
        return {
            SymbolicElement.SMALL_OBJECTS: [
                "A {small_object} catches your eye.",
                "You pocket the {small_object}. It might matter later.",
                "The {small_object} reminds you of {association}."
            ],
            SymbolicElement.GRAFFITI: [
                "Someone has spray-painted {message} on the wall.",
                "The graffiti tells a story: {narrative}.",
                "New tags appear overnight. The city speaks."
            ],
            SymbolicElement.GHOST_SPACES: [
                "The empty {space} echoes with {memory}.",
                "This place used to {past_activity}. Now silence.",
                "You walk through where {people} once {activity}."
            ],
            SymbolicElement.CIGARETTES: [
                "You share your last cigarette with {person}.",
                "Smoke rises, carrying {metaphor}.",
                "The ash falls like {comparison}."
            ],
            SymbolicElement.COFFEE: [
                "The coffee smells like {association}.",
                "Real coffee. A small luxury in these times.",
                "You savor the warmth, the normalcy."
            ]
        }

    def register_voice_configuration(self, config: VoiceConfiguration):
        """Register a voice configuration for a character"""
        self.voice_configurations[config.character_id] = config
        logger.info(f"Registered voice configuration for character {config.character_id}")

    def get_voice_configuration(self, character_id: str) -> Optional[VoiceConfiguration]:
        """Get voice configuration for a character"""
        return self.voice_configurations.get(character_id)

    def generate_narrative_with_voice(self, character_id: str, base_event: str,
                                    context: Dict[str, Any] = None) -> str:
        """Generate narrative content using the character's voice configuration"""
        if context is None:
            context = {}

        config = self.voice_configurations.get(character_id)
        if not config:
            # No voice configuration, return base event
            return base_event

        # Start with base event
        narrative = base_event

        # Apply tone filtering
        narrative = self._apply_tone_filtering(narrative, config, context)

        # Incorporate player-authored influences
        narrative = self._incorporate_player_influences(narrative, config, context)

        # Add symbolic elements
        narrative = self._add_symbolic_elements(narrative, config, context)

        # Apply style modifications
        narrative = self._apply_style_modifications(narrative, config, context)

        # Learn from generation
        self._update_learning_patterns(config, narrative, context)

        return narrative

    def _apply_tone_filtering(self, narrative: str, config: VoiceConfiguration,
                            context: Dict[str, Any]) -> str:
        """Apply emotional tone filtering to the narrative"""
        if not config.emotional_tones:
            return narrative

        # Choose tone based on context and preferences
        primary_tone = random.choice(config.emotional_tones)

        # Get tone-specific templates
        templates = self.tone_templates.get(primary_tone, [])
        if not templates:
            return narrative

        # Apply tone weighting
        tone_weight = config.tone_consistency_weight
        if random.random() < tone_weight:
            # Use tone template
            template = random.choice(templates)
            # Fill template with context or keep original
            if any(placeholder in template for placeholder in ["{action}", "{object}", "{observation}"]):
                # Try to extract meaningful elements from original narrative
                enhanced = self._fill_tone_template(template, narrative, context)
                return enhanced if enhanced else narrative

        return narrative

    def _incorporate_player_influences(self, narrative: str, config: VoiceConfiguration,
                                     context: Dict[str, Any]) -> str:
        """Incorporate patterns and styles from player-authored lines"""
        if not config.player_authored_lines:
            return narrative

        influence_weight = config.player_line_influence
        if random.random() > influence_weight:
            return narrative

        # Get effective player lines
        effective_lines = config.get_effective_lines()
        if not effective_lines:
            effective_lines = config.get_recent_lines(3)

        if not effective_lines:
            return narrative

        # Choose a line to emulate
        reference_line = random.choice(effective_lines)

        # Apply line's style patterns
        enhanced_narrative = self._mirror_line_patterns(narrative, reference_line, context)

        # Update usage tracking
        reference_line.usage_count += 1

        return enhanced_narrative

    def _mirror_line_patterns(self, narrative: str, reference_line: PlayerAuthoredLine,
                            context: Dict[str, Any]) -> str:
        """Mirror the patterns found in a player-authored line"""

        # Extract structural patterns from reference line
        ref_sentences = reference_line.content.split('.')
        ref_sentence_count = len([s for s in ref_sentences if s.strip()])

        # Apply sentence structure patterns
        if NarrativeStyle.SHORT_SENTENCES in reference_line.style_markers:
            # Break narrative into shorter sentences
            narrative = self._break_into_short_sentences(narrative)

        if NarrativeStyle.ONE_LINERS in reference_line.style_markers:
            # Condense to single impactful sentence
            narrative = self._condense_to_one_liner(narrative)

        # Apply emotional tone patterns
        if reference_line.emotional_tone:
            tone_words = self._get_tone_vocabulary(reference_line.emotional_tone)
            narrative = self._enhance_with_tone_words(narrative, tone_words)

        # Apply symbolic element patterns
        for symbol in reference_line.symbolic_elements:
            if random.random() < 0.3:  # 30% chance to incorporate symbol
                narrative = self._add_symbolic_reference(narrative, symbol)

        return narrative

    def _add_symbolic_elements(self, narrative: str, config: VoiceConfiguration,
                             context: Dict[str, Any]) -> str:
        """Add symbolic elements based on character preferences"""
        if not config.symbolic_preferences:
            return narrative

        if random.random() > config.symbolic_density:
            return narrative

        # Choose a symbolic element
        symbol = random.choice(config.symbolic_preferences)

        # Add symbolic reference
        return self._add_symbolic_reference(narrative, symbol)

    def _add_symbolic_reference(self, narrative: str, symbol: SymbolicElement) -> str:
        """Add a reference to a symbolic element"""
        templates = self.symbol_templates.get(symbol, [])
        if not templates:
            return narrative

        template = random.choice(templates)

        # Simple template filling for symbols
        symbol_line = template.replace("{small_object}", random.choice(["coin", "key", "button"]))
        symbol_line = symbol_line.replace("{space}", random.choice(["room", "street", "building"]))
        symbol_line = symbol_line.replace("{message}", random.choice(["'RESIST'", "'HOPE'", "'REMEMBER'"]))

        # Append to narrative
        return f"{narrative} {symbol_line}"

    def _apply_style_modifications(self, narrative: str, config: VoiceConfiguration,
                                 context: Dict[str, Any]) -> str:
        """Apply style modifications based on configuration"""
        for style in config.style_notes:
            if style == NarrativeStyle.SHORT_SENTENCES:
                narrative = self._break_into_short_sentences(narrative)
            elif style == NarrativeStyle.ONE_LINERS:
                narrative = self._condense_to_one_liner(narrative)
            elif style == NarrativeStyle.DRY_HUMOR:
                narrative = self._add_dry_humor(narrative)

        return narrative

    def _break_into_short_sentences(self, narrative: str) -> str:
        """Break narrative into shorter, punchier sentences"""
        # Simple implementation - break long sentences
        sentences = narrative.split('.')
        result = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # If sentence is long, try to break it
            if len(sentence) > 60:
                # Look for conjunctions to break on
                for conjunction in [', and ', ', but ', ', so ', ' because ']:
                    if conjunction in sentence:
                        parts = sentence.split(conjunction, 1)
                        result.append(parts[0].strip())
                        result.append(parts[1].strip())
                        break
                else:
                    result.append(sentence)
            else:
                result.append(sentence)

        return '. '.join(result) + '.'

    def _condense_to_one_liner(self, narrative: str) -> str:
        """Condense narrative to a single impactful line"""
        # Extract the most important sentence
        sentences = [s.strip() for s in narrative.split('.') if s.strip()]
        if not sentences:
            return narrative

        # Prefer shorter, more impactful sentences
        best_sentence = min(sentences, key=len)
        return best_sentence + '.'

    def _add_dry_humor(self, narrative: str) -> str:
        """Add elements of dry humor to the narrative"""
        dry_additions = [
            " Naturally.",
            " Of course.",
            " How typical.",
            " Perfect.",
            " Wonderful."
        ]

        if random.random() < 0.3:
            return narrative + random.choice(dry_additions)

        return narrative

    def _get_tone_vocabulary(self, tone: EmotionalTone) -> List[str]:
        """Get vocabulary words associated with an emotional tone"""
        vocabulary = {
            EmotionalTone.WRY: ["naturally", "of course", "typical", "figures"],
            EmotionalTone.SARDONIC: ["perfect", "wonderful", "delightful", "charming"],
            EmotionalTone.MELANCHOLIC: ["faded", "distant", "echoes", "shadows"],
            EmotionalTone.REBELLIOUS: ["despite", "anyway", "still", "nevertheless"],
            EmotionalTone.TRAGIC: ["lost", "broken", "memory", "weight"]
        }
        return vocabulary.get(tone, [])

    def _enhance_with_tone_words(self, narrative: str, tone_words: List[str]) -> str:
        """Enhance narrative with tone-appropriate vocabulary"""
        if not tone_words or random.random() > 0.4:
            return narrative

        tone_word = random.choice(tone_words)

        # Simple insertion at the end
        if narrative.endswith('.'):
            return f"{narrative[:-1]}, {tone_word}."
        else:
            return f"{narrative} {tone_word}."

    def _fill_tone_template(self, template: str, original: str, context: Dict[str, Any]) -> Optional[str]:
        """Fill a tone template with context information"""
        # Simple template filling - in a full implementation, this would be more sophisticated
        filled = template

        # Replace common placeholders with defaults or context
        replacements = {
            "{action}": context.get("action", "act"),
            "{object}": context.get("object", "situation"),
            "{observation}": context.get("observation", "things happen"),
            "{action_result}": context.get("result", "it happens"),
            "{adjective}": context.get("adjective", "typical"),
            "{authority}": "the system",
            "{system}": "this place",
            "{threat}": "stop you",
            "{memory}": "the past",
            "{emotion}": "everything",
            "{past}": "better times"
        }

        for placeholder, default in replacements.items():
            filled = filled.replace(placeholder, default)

        return filled if filled != template else None

    def _update_learning_patterns(self, config: VoiceConfiguration, generated: str,
                                context: Dict[str, Any]):
        """Update learning patterns based on successful generation"""
        # Extract patterns from successful generation
        if len(generated.split('.')) <= 2:
            config.successful_patterns["short_sentences"] = config.successful_patterns.get("short_sentences", 0) + 1

        # Track symbolic element usage
        for symbol in config.symbolic_preferences:
            if symbol.value.lower() in generated.lower():
                config.successful_patterns[f"symbol_{symbol.value}"] = config.successful_patterns.get(f"symbol_{symbol.value}", 0) + 1

    def create_voice_command_handler(self) -> 'VoiceCommandHandler':
        """Create a command handler for managing voice configurations"""
        return VoiceCommandHandler(self)


class VoiceCommandHandler:
    """Handles player commands for managing voice configuration"""

    def __init__(self, engine: DynamicNarrativeToneEngine):
        self.engine = engine

    def handle_voice_config_command(self, character_id: str, command: str,
                                  args: List[str]) -> str:
        """Handle voice configuration commands"""
        config = self.engine.get_voice_configuration(character_id)
        if not config:
            config = VoiceConfiguration(character_id=character_id)
            self.engine.register_voice_configuration(config)

        if command == "add_line":
            content = " ".join(args)
            line = config.add_player_line(content)
            return f"Added voice line: '{content}'. Detected tone: {line.emotional_tone.value if line.emotional_tone else 'neutral'}"

        elif command == "set_tone":
            try:
                tone = EmotionalTone(args[0])
                if tone not in config.emotional_tones:
                    config.emotional_tones.append(tone)
                return f"Added emotional tone: {tone.value}"
            except ValueError:
                available = [t.value for t in EmotionalTone]
                return f"Invalid tone. Available: {', '.join(available)}"

        elif command == "set_symbol":
            try:
                symbol = SymbolicElement(args[0])
                if symbol not in config.symbolic_preferences:
                    config.symbolic_preferences.append(symbol)
                return f"Added symbolic preference: {symbol.value}"
            except ValueError:
                available = [s.value for s in SymbolicElement]
                return f"Invalid symbol. Available: {', '.join(available)}"

        elif command == "set_style":
            try:
                style = NarrativeStyle(args[0])
                if style not in config.style_notes:
                    config.style_notes.append(style)
                return f"Added style note: {style.value}"
            except ValueError:
                available = [s.value for s in NarrativeStyle]
                return f"Invalid style. Available: {', '.join(available)}"

        elif command == "show_config":
            return self._format_voice_config(config)

        elif command == "clear_lines":
            config.player_authored_lines.clear()
            return "Cleared all player-authored lines"

        else:
            return self._get_help_text()

    def _format_voice_config(self, config: VoiceConfiguration) -> str:
        """Format voice configuration for display"""
        result = f"Voice Configuration for {config.character_id}:\n"
        result += f"Emotional Tones: {', '.join(t.value for t in config.emotional_tones)}\n"
        result += f"Symbolic Preferences: {', '.join(s.value for s in config.symbolic_preferences)}\n"
        result += f"Style Notes: {', '.join(s.value for s in config.style_notes)}\n"
        result += f"Player Lines ({len(config.player_authored_lines)}):\n"

        for i, line in enumerate(config.player_authored_lines[-5:], 1):
            result += f"  {i}. '{line.content}' (used {line.usage_count} times)\n"

        return result

    def _get_help_text(self) -> str:
        """Get help text for voice commands"""
        return """Voice Configuration Commands:
/voice add_line <text> - Add a line that influences your character's voice
/voice set_tone <tone> - Add an emotional tone preference
/voice set_symbol <symbol> - Add a symbolic element preference
/voice set_style <style> - Add a style preference
/voice show_config - Show current voice configuration
/voice clear_lines - Clear all player-authored lines

Examples:
/voice add_line You mistake gunfire for fireworks. Again.
/voice set_tone wry
/voice set_symbol broken_glass
/voice set_style one_liners
"""


# Example usage and integration helpers
def create_default_voice_configurations() -> Dict[str, VoiceConfiguration]:
    """Create some default voice configurations for testing"""
    configs = {}

    # Cynical resistance fighter
    cynical_config = VoiceConfiguration("cynical_fighter")
    cynical_config.emotional_tones = [EmotionalTone.WRY, EmotionalTone.SARDONIC]
    cynical_config.symbolic_preferences = [SymbolicElement.CIGARETTES, SymbolicElement.BROKEN_GLASS]
    cynical_config.style_notes = [NarrativeStyle.SARCASM_COPING, NarrativeStyle.SHORT_SENTENCES]
    cynical_config.add_player_line("You mistake gunfire for fireworks. Again.")
    cynical_config.add_player_line("There's beauty in broken glass if you squint just right.")
    configs["cynical_fighter"] = cynical_config

    # Idealistic student
    idealistic_config = VoiceConfiguration("idealistic_student")
    idealistic_config.emotional_tones = [EmotionalTone.HOPEFUL, EmotionalTone.REBELLIOUS]
    idealistic_config.symbolic_preferences = [SymbolicElement.GRAFFITI, SymbolicElement.FLOWERS]
    idealistic_config.style_notes = [NarrativeStyle.POETIC_LANGUAGE, NarrativeStyle.METAPHORICAL]
    idealistic_config.add_player_line("The regime sends flowers now. Carnations. Red, of course.")
    configs["idealistic_student"] = idealistic_config

    return configs