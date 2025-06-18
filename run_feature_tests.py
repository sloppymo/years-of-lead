#!/usr/bin/env python3
"""
Test runner for Years of Lead feature tests.
This script runs all tests for the enhanced navigation, save/load system, and victory/defeat conditions.
"""

import unittest
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()

    # Discover all tests in the tests/unit directory
    test_loader = unittest.TestLoader()
    feature_tests = test_loader.discover("tests/unit", pattern="test_enhanced_*.py")
    test_suite.addTests(feature_tests)

    # Add specific test modules
    test_suite.addTests(
        test_loader.loadTestsFromName("tests.unit.test_save_load_system")
    )
    test_suite.addTests(
        test_loader.loadTestsFromName("tests.unit.test_victory_defeat_conditions")
    )
    test_suite.addTests(
        test_loader.loadTestsFromName("tests.unit.test_integrated_features")
    )

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n=== Test Summary ===")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    # Exit with appropriate code
    if result.wasSuccessful():
        print("\nAll tests passed! ✅")
        sys.exit(0)
    else:
        print("\nSome tests failed! ❌")
        sys.exit(1)
