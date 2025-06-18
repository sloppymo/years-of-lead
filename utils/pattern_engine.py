"""
Pattern Engine for SYLVA - Phase 2 Enhanced
Analyzes emotional patterns in user interactions using keyword-to-emotion mapping.

Provides symbolic analysis of emotional frequencies for trauma-safe reflection
without clinical interpretation or advice-giving.

Phase 2 Features:
- Emotion frequency tracking (7/30/90 day summaries)
- Subsystem tension mapping (🔥/🌳/🌙 balance analysis)
- Ritual closure intensity scaling (light/medium/heavy endings)
- Drift-aware pattern summaries ("You have left the mountain path...")
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class PatternEngine:
    """
    Analyzes emotional patterns in user interactions through keyword mapping.
    Returns frequency data for symbolic reflection while maintaining trauma-safe boundaries.

    Phase 2 Enhanced Features:
    - Multi-timeframe emotion tracking
    - Subsystem balance analysis
    - Adaptive ritual closure intensity
    - Drift detection and symbolic guidance
    """

    def __init__(self):
        """Initialize the pattern engine with emotion-to-keyword mappings and Phase 2 enhancements."""
        self.emotion_keywords = {
            "sadness": [
                "sad",
                "depressed",
                "hurt",
                "crying",
                "tears",
                "grief",
                "mourning",
                "despair",
                "defeated",
                "hopeless",
                "empty",
                "broken",
                "tired",
                "loss",
            ],
            "anger": [
                "hate",
                "rage",
                "furious",
                "bitter",
                "angry",
                "mad",
                "irritated",
                "frustrated",
                "annoyed",
                "outraged",
                "livid",
                "seething",
                "hostile",
                "resentful",
                "vengeful",
                "aggressive",
                "violent",
                "explosive",
            ],
            "anxiety": [
                "panic",
                "nervous",
                "worry",
                "anxious",
                "jittery",
                "restless",
                "uneasy",
                "apprehensive",
                "dread",
                "horror",
                "paralyzed",
                "frozen",
                "stressed",
                "tense",
            ],
            "shame": [
                "ashamed",
                "embarrassed",
                "dirty",
                "guilt",
                "shameful",
                "disgusting",
                "unworthy",
                "defective",
                "damaged",
                "tainted",
                "contaminated",
                "impure",
                "sinful",
                "bad",
                "wrong",
                "inadequate",
                "worthless",
            ],
            "overwhelm": [
                "too much",
                "can't breathe",
                "drowning",
                "suffocating",
                "crushed",
                "buried",
                "trapped",
                "stuck",
                "numb",
                "disconnected",
                "spaced out",
                "overwhelmed",
                "exhausted",
                "drained",
            ],
            "grief": [
                "missing",
                "gone",
                "died",
                "death",
                "bereaved",
                "grieving",
                "heartbroken",
                "devastated",
                "destroyed",
                "shattered",
                "void",
                "hollow",
                "left behind",
            ],
            "fear": [
                "afraid",
                "scared",
                "terrified",
                "horrified",
                "petrified",
                "frightened",
                "intimidated",
                "threatened",
                "vulnerable",
                "exposed",
                "unsafe",
                "dangerous",
                "risky",
                "threatening",
                "hostile",
                "danger",
            ],
            "loneliness": [
                "alone",
                "lonely",
                "isolated",
                "separated",
                "disconnected",
                "abandoned",
                "rejected",
                "excluded",
                "left out",
                "ignored",
                "invisible",
                "unseen",
                "unheard",
                "forgotten",
                "deserted",
                "stranded",
            ],
        }

        # Create reverse mapping for efficient lookup
        self.keyword_to_emotion = {}
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                self.keyword_to_emotion[keyword] = emotion

        # Phase 2: Ritual closure intensity templates
        self.ritual_closures = {
            "light": [
                "That's enough for now.",
                "We'll build from that ember.",
                "Let it be named and left.",
            ],
            "medium": [
                "The container holds what needs holding. That's enough for now.",
                "What has been witnessed can rest here. We'll build from that ember.",
                "The boundary honors what is needed. Let it be named and left.",
            ],
            "heavy": [
                "The deep systems have witnessed this. The container holds what needs holding. That's enough for now.",
                "What the spiral teaches, the ember remembers. What has been witnessed can rest here. We'll build from that ember.",
                "The sacred boundary protects what is most tender. The boundary honors what is needed. Let it be named and left.",
            ],
        }

        # Phase 2: Drift detection patterns
        self.drift_patterns = {
            "mountain_path": "You have left the mountain path - the patterns show movement away from grounding.",
            "ember_cooling": "The ember grows distant - less fire in recent exchanges.",
            "tide_receding": "The tide has receded - boundary work has shifted.",
            "spiral_ascending": "The spiral moves upward - transformation patterns emerging.",
            "forest_thinning": "The forest grows sparse - connection patterns changing.",
            "well_deepening": "The well deepens - more profound currents flowing.",
        }

    def analyze_emotion_frequencies(
        self, memory_entries: List[Dict], timeframes: List[int] = [7, 30, 90]
    ) -> Dict[str, Dict[str, int]]:
        """
        Analyze emotion frequencies across multiple timeframes.

        Args:
            memory_entries: List of memory entry dictionaries with timestamps
            timeframes: List of days to analyze (default: 7, 30, 90 days)

        Returns:
            Dictionary with emotion frequencies for each timeframe
        """
        now = datetime.now()
        results = {}

        for days in timeframes:
            cutoff_date = now - timedelta(days=days)

            # Filter entries within timeframe
            timeframe_entries = []
            for entry in memory_entries:
                try:
                    entry_date = datetime.fromisoformat(entry.get("timestamp", ""))
                    if entry_date >= cutoff_date:
                        user_input = entry.get("user_input", "")
                        if user_input and not user_input.startswith(
                            "/"
                        ):  # Skip commands
                            timeframe_entries.append(user_input)
                except (ValueError, TypeError):
                    continue

            # Analyze emotions for this timeframe
            emotion_counts = self.analyze_emotions(timeframe_entries)
            results[f"{days}_days"] = emotion_counts

        return results

    def analyze_subsystem_tension(
        self, memory_entries: List[Dict], days: int = 30
    ) -> Dict[str, any]:
        """
        Analyze subsystem balance and tension patterns.

        Args:
            memory_entries: List of memory entry dictionaries
            days: Number of days to analyze

        Returns:
            Dictionary with subsystem tension analysis
        """
        now = datetime.now()
        cutoff_date = now - timedelta(days=days)

        subsystem_counts = {"MARROW": 0, "ROOT": 0, "AURA": 0}
        subsystem_emotions = {"MARROW": [], "ROOT": [], "AURA": []}

        # Collect subsystem activity and associated emotions
        for entry in memory_entries:
            try:
                entry_date = datetime.fromisoformat(entry.get("timestamp", ""))
                if entry_date >= cutoff_date:
                    subsystem = entry.get("subsystem", "ROOT")
                    emotion = entry.get("emotion")

                    if subsystem in subsystem_counts:
                        subsystem_counts[subsystem] += 1
                        if emotion:
                            subsystem_emotions[subsystem].append(emotion)
            except (ValueError, TypeError):
                continue

        total_activity = sum(subsystem_counts.values())
        if total_activity == 0:
            return {
                "balance": "equilibrium",
                "tension_level": "minimal",
                "dominant_subsystem": None,
            }

        # Calculate balance ratios
        balance_ratios = {k: v / total_activity for k, v in subsystem_counts.items()}

        # Determine tension level and dominant subsystem
        dominant_subsystem = max(balance_ratios.items(), key=lambda x: x[1])[0]
        max_ratio = balance_ratios[dominant_subsystem]

        if max_ratio > 0.6:
            tension_level = "high"
            balance_state = f"{dominant_subsystem.lower()}_dominant"
        elif max_ratio > 0.45:
            tension_level = "moderate"
            balance_state = f"{dominant_subsystem.lower()}_leading"
        else:
            tension_level = "low"
            balance_state = "balanced"

        return {
            "balance": balance_state,
            "tension_level": tension_level,
            "dominant_subsystem": dominant_subsystem,
            "ratios": balance_ratios,
            "subsystem_emotions": subsystem_emotions,
            "total_activity": total_activity,
        }

    def determine_ritual_intensity(
        self, emotion_counts: Dict[str, int], subsystem_tension: Dict[str, any]
    ) -> str:
        """
        Determine appropriate ritual closure intensity based on emotional load and subsystem tension.

        Args:
            emotion_counts: Dictionary of emotion frequencies
            subsystem_tension: Subsystem tension analysis

        Returns:
            Intensity level: "light", "medium", or "heavy"
        """
        if not emotion_counts:
            return "light"

        total_emotions = sum(emotion_counts.values())
        tension_level = subsystem_tension.get("tension_level", "low")

        # Check for high-intensity emotions
        intense_emotions = ["shame", "grief", "overwhelm", "fear"]
        intense_count = sum(
            emotion_counts.get(emotion, 0) for emotion in intense_emotions
        )

        # Determine intensity
        if intense_count >= 3 or tension_level == "high" or total_emotions >= 8:
            return "heavy"
        elif intense_count >= 1 or tension_level == "moderate" or total_emotions >= 4:
            return "medium"
        else:
            return "light"

    def detect_drift_patterns(
        self, memory_entries: List[Dict], comparison_days: Tuple[int, int] = (7, 30)
    ) -> Optional[str]:
        """
        Detect drift in emotional or subsystem patterns.

        Args:
            memory_entries: List of memory entry dictionaries
            comparison_days: Tuple of (recent_days, comparison_days) for drift detection

        Returns:
            Drift pattern description or None if no significant drift detected
        """
        recent_days, comparison_days = comparison_days

        # Analyze recent vs. historical patterns
        recent_analysis = self.analyze_subsystem_tension(memory_entries, recent_days)
        historical_analysis = self.analyze_subsystem_tension(
            memory_entries, comparison_days
        )

        recent_dominant = recent_analysis.get("dominant_subsystem")
        historical_dominant = historical_analysis.get("dominant_subsystem")

        recent_ratios = recent_analysis.get("ratios", {})
        historical_ratios = historical_analysis.get("ratios", {})

        # Detect significant shifts
        if recent_dominant != historical_dominant:
            if recent_dominant == "ROOT" and historical_dominant in ["MARROW", "AURA"]:
                return self.drift_patterns["mountain_path"]
            elif recent_dominant == "AURA" and historical_dominant == "MARROW":
                return self.drift_patterns["ember_cooling"]
            elif recent_dominant == "ROOT" and historical_dominant == "AURA":
                return self.drift_patterns["tide_receding"]

        # Detect intensity shifts
        recent_marrow = recent_ratios.get("MARROW", 0)
        historical_marrow = historical_ratios.get("MARROW", 0)

        if recent_marrow > historical_marrow + 0.2:
            return self.drift_patterns["spiral_ascending"]
        elif recent_marrow < historical_marrow - 0.2:
            return self.drift_patterns["well_deepening"]

        return None

    def generate_ritual_closure(self, intensity: str) -> str:
        """
        Generate appropriate ritual closure based on intensity level.

        Args:
            intensity: Intensity level ("light", "medium", "heavy")

        Returns:
            Ritual closure string
        """
        import random

        closures = self.ritual_closures.get(intensity, self.ritual_closures["light"])
        return random.choice(closures)
