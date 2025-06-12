from game.emotional_state import EmotionalState


def test_emotional_drift_reduces_extreme_values():
    """EmotionalState.apply_drift should move emotions toward neutral over time."""
    # Start with extreme positive and negative emotions
    state = EmotionalState(fear=0.8, joy=-0.7, anger=0.9, trust=-0.6, trauma_level=0.2)

    # Capture initial magnitudes
    initial_values = {
        "fear": state.fear,
        "joy": state.joy,
        "anger": state.anger,
        "trust": state.trust,
    }

    # Apply drift for ten time-steps
    for _ in range(10):
        state.apply_drift(time_delta=1.0)

    # After drift, magnitudes should be strictly closer to zero
    assert abs(state.fear) < abs(initial_values["fear"])
    assert abs(state.joy) < abs(initial_values["joy"])
    assert abs(state.anger) < abs(initial_values["anger"])
    assert abs(state.trust) < abs(initial_values["trust"])

    # Trauma should not have increased during passive drift
    assert state.trauma_level <= 0.2 + 1e-6
