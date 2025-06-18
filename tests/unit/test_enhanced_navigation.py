import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import MenuItem, GameCLI

class TestEnhancedNavigation(unittest.TestCase):
    """Tests for the enhanced navigation features"""
    
    def setUp(self):
        """Set up test environment"""
        self.cli = GameCLI()
        # Create test menu items
        self.cli.current_menu_items = [
            MenuItem("a", "advance", "Advance Turn", lambda: "advance"),
            MenuItem("g", "agents", "Show Agents", lambda: "agents"),
            MenuItem("q", "quit", "Quit Game", lambda: "quit")
        ]
        self.cli.selected_index = 0
        self.cli.current_menu_items[0].selected = True
        
    def test_menu_item_initialization(self):
        """Test that MenuItem objects are initialized correctly"""
        item = MenuItem("t", "test", "Test Item", lambda: "test")
        self.assertEqual(item.key, "t")
        self.assertEqual(item.label, "test")
        self.assertEqual(item.description, "Test Item")
        self.assertFalse(item.selected)
        self.assertEqual(item.position, (0, 0))
        
    def test_arrow_key_navigation_down(self):
        """Test arrow key navigation - move down"""
        result = self.cli._handle_arrow_key("down")
        
        # Check that selection moved to the second item
        self.assertFalse(self.cli.current_menu_items[0].selected)
        self.assertTrue(self.cli.current_menu_items[1].selected)
        self.assertEqual(self.cli.selected_index, 1)
        self.assertEqual(result, "navigation")
        
    def test_arrow_key_navigation_up(self):
        """Test arrow key navigation - move up"""
        # Start with second item selected
        self.cli.current_menu_items[0].selected = False
        self.cli.selected_index = 1
        self.cli.current_menu_items[1].selected = True
        
        result = self.cli._handle_arrow_key("up")
        
        # Check that selection moved to the first item
        self.assertTrue(self.cli.current_menu_items[0].selected)
        self.assertFalse(self.cli.current_menu_items[1].selected)
        self.assertEqual(self.cli.selected_index, 0)
        self.assertEqual(result, "navigation")
        
    def test_arrow_key_navigation_wrap_down(self):
        """Test arrow key navigation - wrap from bottom to top"""
        # Start with last item selected
        self.cli.current_menu_items[0].selected = False
        self.cli.selected_index = 2
        self.cli.current_menu_items[2].selected = True
        
        result = self.cli._handle_arrow_key("down")
        
        # Check that selection wrapped to the first item
        self.assertTrue(self.cli.current_menu_items[0].selected)
        self.assertFalse(self.cli.current_menu_items[2].selected)
        self.assertEqual(self.cli.selected_index, 0)
        self.assertEqual(result, "navigation")
        
    def test_arrow_key_navigation_wrap_up(self):
        """Test arrow key navigation - wrap from top to bottom"""
        result = self.cli._handle_arrow_key("up")
        
        # Check that selection wrapped to the last item
        self.assertFalse(self.cli.current_menu_items[0].selected)
        self.assertTrue(self.cli.current_menu_items[2].selected)
        self.assertEqual(self.cli.selected_index, 2)
        self.assertEqual(result, "navigation")
        
    def test_arrow_key_enter(self):
        """Test arrow key navigation - press enter to execute"""
        result = self.cli._handle_arrow_key("enter")
        
        # Check that the action was executed
        self.assertEqual(result, "advance")
        
    def test_mouse_click_selection(self):
        """Test mouse click selection"""
        # Set up positions for menu items
        self.cli.current_menu_items[0].position = (4, 2)
        self.cli.current_menu_items[1].position = (5, 2)
        self.cli.current_menu_items[2].position = (6, 2)
        
        # Click on the second item
        result = self.cli._handle_mouse_click(2, 5)
        
        # Check that selection changed to the second item
        self.assertFalse(self.cli.current_menu_items[0].selected)
        self.assertTrue(self.cli.current_menu_items[1].selected)
        self.assertEqual(self.cli.selected_index, 1)
        self.assertEqual(result, "agents")
        
    def test_mouse_click_outside_menu(self):
        """Test mouse click outside menu area"""
        # Set up positions for menu items
        self.cli.current_menu_items[0].position = (4, 2)
        self.cli.current_menu_items[1].position = (5, 2)
        self.cli.current_menu_items[2].position = (6, 2)
        
        # Click outside menu area
        result = self.cli._handle_mouse_click(20, 20)
        
        # Check that selection didn't change
        self.assertTrue(self.cli.current_menu_items[0].selected)
        self.assertEqual(self.cli.selected_index, 0)
        self.assertIsNone(result)
        
    def test_run_with_arrow_navigation(self):
        """Test run method with arrow key navigation"""
        # Mock input to simulate arrow key navigation
        inputs = ["arrow:down", "arrow:enter", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'show_agent_details') as mock_show_agents:
                            self.cli.run()
                            
                            # Check that show_agent_details was called
                            mock_show_agents.assert_called_once()
                            
    def test_run_with_mouse_navigation(self):
        """Test run method with mouse navigation"""
        # Set up positions for menu items
        self.cli.current_menu_items[0].position = (4, 2)
        self.cli.current_menu_items[1].position = (5, 2)
        self.cli.current_menu_items[2].position = (6, 2)
        
        # Mock input to simulate mouse navigation
        inputs = ["mouse:2,5", "q"]
        
        with patch('builtins.input', side_effect=inputs):
            with patch.object(self.cli, 'display_header'):
                with patch.object(self.cli, 'display_current_status'):
                    with patch.object(self.cli, 'display_menu'):
                        with patch.object(self.cli, 'show_agent_details') as mock_show_agents:
                            self.cli.run()
                            
                            # Check that show_agent_details was called
                            mock_show_agents.assert_called_once()

if __name__ == "__main__":
    unittest.main() 