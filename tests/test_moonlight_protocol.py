import pytest
from unittest.mock import patch
from datetime import datetime
import sys
import os

# Add utils to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))

from timekeeper import (
    get_protocol_state, 
    is_moonlight_active, 
    get_time_context,
    _get_symbolic_tone,
    _get_ritual_style
)

class TestMoonlightProtocol:
    """Test suite for SYLVA's Moonlight Protocol time-aware safety layer."""
    
    @pytest.mark.parametrize("hour,expected_state", [
        # Standard daylight hours
        (6, "standard"), (12, "standard"), (18, "standard"), (21, "standard"),
        # Moonlight hours (22-01:59)
        (22, "moonlight"), (23, "moonlight"), (0, "moonlight"), (1, "moonlight"),
        # Deep moonlight hours (02-05:59)
        (2, "deep_moonlight"), (3, "deep_moonlight"), (4, "deep_moonlight"), (5, "deep_moonlight")
    ])
    def test_protocol_state_detection(self, hour, expected_state):
        """Test that protocol states are correctly detected for all hours."""
        with patch('timekeeper.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, hour, 0, 0)
            assert get_protocol_state() == expected_state
    
    @pytest.mark.parametrize("hour,expected_active", [
        # Standard hours should not be moonlight active
        (6, False), (12, False), (18, False), (21, False),
        # Moonlight and deep moonlight should be active
        (22, True), (23, True), (0, True), (1, True), (2, True), (3, True), (4, True), (5, True)
    ])
    def test_moonlight_active_detection(self, hour, expected_active):
        """Test moonlight activity detection across all hours."""
        with patch('timekeeper.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, hour, 0, 0)
            assert is_moonlight_active() == expected_active
    
    def test_time_context_structure(self):
        """Test that time context returns proper structure."""
        with patch('timekeeper.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 23, 30, 0)
            
            context = get_time_context()
            
            # Verify all required keys are present
            required_keys = ["protocol_state", "hour", "is_night", "symbolic_tone", "ritual_style"]
            for key in required_keys:
                assert key in context
            
            # Verify values are correct for moonlight hour
            assert context["protocol_state"] == "moonlight"
            assert context["hour"] == 23
            assert context["is_night"] == True
            assert context["symbolic_tone"] == "twilight"
            assert context["ritual_style"] == "gentle"
    
    @pytest.mark.parametrize("state,expected_tone", [
        ("standard", "daylight"),
        ("moonlight", "twilight"),
        ("deep_moonlight", "shadow")
    ])
    def test_symbolic_tone_mapping(self, state, expected_tone):
        """Test symbolic tone mapping for all protocol states."""
        assert _get_symbolic_tone(state) == expected_tone
    
    @pytest.mark.parametrize("state,expected_style", [
        ("standard", "standard"),
        ("moonlight", "gentle"),
        ("deep_moonlight", "whispered")
    ])
    def test_ritual_style_mapping(self, state, expected_style):
        """Test ritual closure style mapping for all protocol states."""
        assert _get_ritual_style(state) == expected_style
    
    def test_edge_case_boundary_times(self):
        """Test boundary conditions at protocol transition times."""
        boundary_tests = [
            (21, 59, "standard"),  # Just before moonlight
            (22, 0, "moonlight"),   # Start of moonlight
            (1, 59, "moonlight"),   # End of moonlight
            (2, 0, "deep_moonlight"), # Start of deep moonlight
            (5, 59, "deep_moonlight"), # End of deep moonlight
            (6, 0, "standard")      # Return to standard
        ]
        
        for hour, minute, expected_state in boundary_tests:
            with patch('timekeeper.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 1, hour, minute, 0)
                assert get_protocol_state() == expected_state
    
    def test_protocol_consistency(self):
        """Test that protocol state and activity detection are consistent."""
        for hour in range(24):
            with patch('timekeeper.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 1, hour, 0, 0)
                
                state = get_protocol_state()
                is_active = is_moonlight_active()
                
                # If moonlight is active, state should be moonlight or deep_moonlight
                if is_active:
                    assert state in ["moonlight", "deep_moonlight"]
                else:
                    assert state == "standard"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 