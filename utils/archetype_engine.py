"""
Archetype Engine for SYLVA - Phase 2 User Modeling
Tracks user archetype preferences, session typing, symbolic arc detection, and memory weight scoring as part of Phase 2 v2.3.0 features.

Provides trauma-safe user modeling through symbolic archetypes and patterns
without clinical profiling or diagnostic categorization.

Phase 2 Features:
- Archetype preference tracking (e.g. river vs. ember)
- Session typing: emergent / reflective / dispersive
- Symbolic arc detection (beginning, middle, closure identification)
- Memory weight scoring (emotional gravity per entry)
"""

from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import json
from pathlib import Path

class ArchetypeEngine:
    """
    Models user symbolic preferences and patterns through archetype analysis.
    Maintains trauma-safe boundaries while providing personalized symbolic responses.
    
    Phase 2 Features:
    - Archetype preference learning
    - Session pattern recognition
    - Symbolic arc tracking
    - Emotional gravity scoring
    """
    
    def __init__(self, user_profile_path: Optional[str] = None):
        """Initialize the archetype engine with user modeling capabilities."""
        
        # Archetype definitions by subsystem
        self.archetypes = {
            "MARROW": {
                "the_ember": {
                    "keywords": ["fire", "burn", "flame", "spark", "heat", "glow", "warmth"],
                    "themes": ["transformation", "inner_fire", "passion", "core_energy"],
                    "responses": ["The ember holds steady in the wind.", "What burns within cannot be extinguished."]
                },
                "the_spiral": {
                    "keywords": ["spiral", "cycle", "turn", "twist", "wind", "coil", "circle"],
                    "themes": ["transformation", "cycles", "depth", "evolution"],
                    "responses": ["The spiral has its own wisdom.", "Each turn reveals new depths."]
                },
                "the_cave": {
                    "keywords": ["cave", "dark", "deep", "hidden", "shelter", "protect", "inside"],
                    "themes": ["protection", "inner_work", "gestation", "safety"],
                    "responses": ["The cave protects what is growing in the dark.", "Deep places hold deep wisdom."]
                },
                "the_seed": {
                    "keywords": ["seed", "grow", "plant", "root", "sprout", "potential", "begin"],
                    "themes": ["potential", "growth", "beginning", "life_force"],
                    "responses": ["The seed knows its season.", "What is planted in darkness grows toward light."]
                },
                "the_well": {
                    "keywords": ["well", "deep", "water", "source", "draw", "depth", "spring"],
                    "themes": ["depth", "source", "wisdom", "nourishment"],
                    "responses": ["The well runs deeper than you know.", "Ancient waters flow in deep places."]
                }
            },
            "ROOT": {
                "the_mountain": {
                    "keywords": ["mountain", "peak", "high", "solid", "stone", "rock", "steady"],
                    "themes": ["stability", "endurance", "perspective", "strength"],
                    "responses": ["The mountain stands, regardless of storms.", "High places offer wide views."]
                },
                "the_forest": {
                    "keywords": ["forest", "tree", "wood", "branch", "leaf", "grow", "green"],
                    "themes": ["growth", "community", "interconnection", "life"],
                    "responses": ["The forest grows in its own time.", "Each tree supports the whole."]
                },
                "the_river": {
                    "keywords": ["river", "flow", "water", "stream", "current", "move", "path"],
                    "themes": ["flow", "movement", "persistence", "adaptation"],
                    "responses": ["The river finds its way.", "Water shapes stone through patience."]
                },
                "the_bridge": {
                    "keywords": ["bridge", "cross", "connect", "span", "link", "join", "between"],
                    "themes": ["connection", "transition", "linking", "passage"],
                    "responses": ["The bridge connects what was separate.", "Crossing requires courage."]
                }
            },
            "AURA": {
                "the_mask": {
                    "keywords": ["mask", "face", "hide", "show", "protect", "cover", "reveal"],
                    "themes": ["protection", "identity", "boundaries", "presentation"],
                    "responses": ["The mask protects what is tender.", "What is hidden has its reasons."]
                },
                "the_tide": {
                    "keywords": ["tide", "wave", "ocean", "ebb", "flow", "rhythm", "cycle"],
                    "themes": ["cycles", "boundaries", "rhythm", "natural_flow"],
                    "responses": ["The tide knows its own timing.", "What recedes will return."]
                },
                "the_moon": {
                    "keywords": ["moon", "night", "phase", "cycle", "light", "dark", "change"],
                    "themes": ["cycles", "mystery", "reflection", "phases"],
                    "responses": ["The moon shows all its faces in time.", "Night wisdom differs from day wisdom."]
                },
                "the_mirror": {
                    "keywords": ["mirror", "reflect", "see", "show", "image", "truth", "surface"],
                    "themes": ["reflection", "truth", "seeing", "clarity"],
                    "responses": ["The mirror shows what is, without commentary.", "Reflection reveals what was always there."]
                }
            }
        }
        
        # Session type patterns
        self.session_types = {
            "emergent": {
                "indicators": ["new", "sudden", "unexpected", "surprise", "emerge", "arise", "appear"],
                "characteristics": "New patterns or insights arising"
            },
            "reflective": {
                "indicators": ["think", "consider", "reflect", "ponder", "wonder", "contemplate", "examine"],
                "characteristics": "Deep contemplation and processing"
            },
            "dispersive": {
                "indicators": ["scattered", "everywhere", "all over", "confused", "mixed", "chaotic", "unclear"],
                "characteristics": "Energy scattered, seeking integration"
            }
        }
        
        # User profile path
        if user_profile_path:
            self.profile_path = Path(user_profile_path)
        else:
            self.profile_path = Path(__file__).parent.parent / "memory" / "user_archetype_profile.json"
        
        # Initialize user profile
        self.user_profile = self._load_user_profile()
    
    def _load_user_profile(self) -> Dict:
        """Load or initialize user archetype profile."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Initialize new profile
        return {
            "created": datetime.now().isoformat(),
            "version": "2.0",
            "archetype_preferences": {subsystem: {} for subsystem in self.archetypes.keys()},
            "session_patterns": {"emergent": 0, "reflective": 0, "dispersive": 0},
            "symbolic_arcs": [],
            "total_interactions": 0,
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_user_profile(self):
        """Save user profile to disk."""
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        self.user_profile["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.user_profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save user profile: {e}")
    
    def track_archetype_preference(self, user_input: str, subsystem: str, archetype_used: str):
        """
        Track user's archetype preferences based on responses and usage.
        
        Args:
            user_input: User's input text
            subsystem: Active subsystem (MARROW/ROOT/AURA)
            archetype_used: Archetype that was used in response
        """
        if subsystem not in self.user_profile["archetype_preferences"]:
            self.user_profile["archetype_preferences"][subsystem] = {}
        
        # Increment usage count for this archetype
        archetype_prefs = self.user_profile["archetype_preferences"][subsystem]
        archetype_prefs[archetype_used] = archetype_prefs.get(archetype_used, 0) + 1
        
        # Check if user input contains keywords that align with specific archetypes
        user_lower = user_input.lower()
        for archetype_name, archetype_data in self.archetypes.get(subsystem, {}).items():
            keyword_matches = sum(1 for keyword in archetype_data["keywords"] if keyword in user_lower)
            if keyword_matches > 0:
                archetype_prefs[archetype_name] = archetype_prefs.get(archetype_name, 0) + keyword_matches
        
        self.user_profile["total_interactions"] += 1
        self._save_user_profile()
    
    def detect_session_type(self, session_inputs: List[str]) -> str:
        """
        Detect the type of session based on user inputs.
        
        Args:
            session_inputs: List of user inputs from current session
            
        Returns:
            Session type: "emergent", "reflective", or "dispersive"
        """
        if not session_inputs:
            return "reflective"
        
        combined_text = " ".join(session_inputs).lower()
        type_scores = {}
        
        for session_type, data in self.session_types.items():
            score = sum(1 for indicator in data["indicators"] if indicator in combined_text)
            type_scores[session_type] = score
        
        # Determine session type
        if not any(type_scores.values()):
            return "reflective"  # Default
        
        detected_type = max(type_scores.items(), key=lambda x: x[1])[0]
        
        # Update session pattern tracking
        self.user_profile["session_patterns"][detected_type] += 1
        self._save_user_profile()
        
        return detected_type
    
    def detect_symbolic_arc(self, memory_entries: List[Dict], session_threshold: int = 5) -> Optional[Dict]:
        """
        Detect symbolic arcs in user's journey (beginning, middle, closure patterns).
        
        Args:
            memory_entries: List of memory entries
            session_threshold: Minimum interactions to consider an arc
            
        Returns:
            Dictionary describing the detected arc or None
        """
        if len(memory_entries) < session_threshold:
            return None
        
        # Analyze recent entries for arc patterns
        recent_entries = memory_entries[-session_threshold:]
        
        # Extract emotions and subsystems
        emotions = [entry.get("emotion") for entry in recent_entries if entry.get("emotion")]
        subsystems = [entry.get("subsystem") for entry in recent_entries if entry.get("subsystem")]
        
        if not emotions or not subsystems:
            return None
        
        # Detect arc patterns
        arc_type = None
        arc_description = ""
        
        # Beginning pattern: high intensity emotions, mixed subsystems
        if len(set(emotions)) >= 3 and len(set(subsystems)) >= 2:
            arc_type = "beginning"
            arc_description = "Multiple currents converging - a new chapter begins"
        
        # Middle pattern: sustained engagement with one subsystem
        elif len(subsystems) >= 3 and subsystems.count(max(set(subsystems), key=subsystems.count)) >= 3:
            dominant_subsystem = max(set(subsystems), key=subsystems.count)
            arc_type = "middle"
            arc_description = f"Deep work in {dominant_subsystem} - the middle passage unfolds"
        
        # Closure pattern: decreasing emotional intensity, movement toward AURA
        elif subsystems[-2:].count("AURA") >= 1 and len(emotions) >= 2:
            arc_type = "closure"
            arc_description = "Boundary work emerging - patterns seeking completion"
        
        if arc_type:
            arc_data = {
                "type": arc_type,
                "description": arc_description,
                "timestamp": datetime.now().isoformat(),
                "entries_analyzed": len(recent_entries),
                "dominant_emotions": list(Counter(emotions).most_common(2)),
                "subsystem_flow": subsystems
            }
            
            # Store arc in profile
            self.user_profile["symbolic_arcs"].append(arc_data)
            # Keep only last 10 arcs
            self.user_profile["symbolic_arcs"] = self.user_profile["symbolic_arcs"][-10:]
            self._save_user_profile()
            
            return arc_data
        
        return None
    
    def calculate_memory_weight(self, user_input: str, emotion: Optional[str], subsystem: str) -> float:
        """
        Calculate emotional gravity/weight of a memory entry.
        
        Args:
            user_input: User's input text
            emotion: Detected emotion
            subsystem: Active subsystem
            
        Returns:
            Weight score (0.0 to 1.0)
        """
        weight = 0.0
        
        # Base weight from emotion intensity
        emotion_weights = {
            "shame": 0.9,
            "grief": 0.8,
            "overwhelm": 0.8,
            "fear": 0.7,
            "anger": 0.6,
            "anxiety": 0.6,
            "sadness": 0.5,
            "loneliness": 0.5
        }
        
        if emotion:
            weight += emotion_weights.get(emotion, 0.3)
        
        # Subsystem weight modifiers
        subsystem_weights = {"MARROW": 0.3, "ROOT": 0.1, "AURA": 0.2}
        weight += subsystem_weights.get(subsystem, 0.1)
        
        # Text intensity indicators
        intensity_keywords = [
            "always", "never", "everything", "nothing", "completely", "totally",
            "destroyed", "shattered", "broken", "hopeless", "desperate"
        ]
        
        text_lower = user_input.lower()
        intensity_count = sum(1 for keyword in intensity_keywords if keyword in text_lower)
        weight += min(intensity_count * 0.1, 0.2)
        
        # Length factor (longer expressions often carry more weight)
        if len(user_input) > 100:
            weight += 0.1
        
        return min(weight, 1.0)
    
    def get_preferred_archetype(self, subsystem: str) -> Optional[str]:
        """
        Get user's preferred archetype for a given subsystem.
        
        Args:
            subsystem: Subsystem to check (MARROW/ROOT/AURA)
            
        Returns:
            Preferred archetype name or None
        """
        prefs = self.user_profile["archetype_preferences"].get(subsystem, {})
        if not prefs:
            return None
        
        return max(prefs.items(), key=lambda x: x[1])[0]
    
    def get_user_summary(self) -> Dict:
        """
        Generate a summary of user's archetype profile.
        
        Returns:
            Dictionary with user modeling summary
        """
        # Calculate preferred archetypes
        preferred_archetypes = {}
        for subsystem in self.archetypes.keys():
            preferred = self.get_preferred_archetype(subsystem)
            if preferred:
                preferred_archetypes[subsystem] = preferred
        
        # Calculate dominant session type
        session_patterns = self.user_profile["session_patterns"]
        dominant_session_type = max(session_patterns.items(), key=lambda x: x[1])[0] if any(session_patterns.values()) else "balanced"
        
        # Recent arc analysis
        recent_arcs = self.user_profile["symbolic_arcs"][-3:] if self.user_profile["symbolic_arcs"] else []
        
        return {
            "total_interactions": self.user_profile["total_interactions"],
            "preferred_archetypes": preferred_archetypes,
            "dominant_session_type": dominant_session_type,
            "session_distribution": session_patterns,
            "recent_symbolic_arcs": recent_arcs,
            "profile_age_days": self._calculate_profile_age(),
            "last_updated": self.user_profile["last_updated"]
        }
    
    def _calculate_profile_age(self) -> int:
        """Calculate age of user profile in days."""
        try:
            created_date = datetime.fromisoformat(self.user_profile["created"])
            return (datetime.now() - created_date).days
        except (ValueError, KeyError):
            return 0 