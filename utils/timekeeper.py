from datetime import datetime

def get_protocol_state() -> str:
    """Returns SYLVA's symbolic safety protocol state based on the current hour."""
    hour = datetime.now().hour
    if 22 <= hour <= 23 or 0 <= hour < 2:
        return "moonlight"
    elif 2 <= hour < 6:
        return "deep_moonlight"
    return "standard"

def is_moonlight_active() -> bool:
    """Returns True if any moonlight protocol is currently active."""
    return get_protocol_state() in ["moonlight", "deep_moonlight"]

def get_time_context() -> dict:
    """Returns detailed time context for symbolic response adaptation."""
    state = get_protocol_state()
    hour = datetime.now().hour
    
    return {
        "protocol_state": state,
        "hour": hour,
        "is_night": is_moonlight_active(),
        "symbolic_tone": _get_symbolic_tone(state),
        "ritual_style": _get_ritual_style(state)
    }

def _get_symbolic_tone(state: str) -> str:
    """Returns the appropriate symbolic tone for the current protocol state."""
    tones = {
        "standard": "daylight",
        "moonlight": "twilight", 
        "deep_moonlight": "shadow"
    }
    return tones.get(state, "daylight")

def _get_ritual_style(state: str) -> str:
    """Returns the ritual closure style for the current protocol state."""
    styles = {
        "standard": "standard",
        "moonlight": "gentle",
        "deep_moonlight": "whispered"
    }
    return styles.get(state, "standard") 