#!/usr/bin/env python3
"""
Run all CLI tests for Years of Lead
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_header():
    """Print the test header"""
    header = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                 YEARS OF LEAD: CLI TEST SUITE                                    ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  Running comprehensive tests for the CLI interface                               ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""
    print(header)

def run_tests():
    """Run all CLI tests"""
    test_files = [
        "tests/unit/test_cli_e2e.py",
        "tests/unit/test_cli_integration.py",
        "tests/unit/test_cli_navigation.py"  # Added the new navigation tests
    ]
    
    results = []
    
    for test_file in test_files:
        print(f"\n\n{'=' * 80}")
        print(f"Running tests in {test_file}")
        print(f"{'=' * 80}\n")
        
        start_time = time.time()
        result = subprocess.run(["pytest", "-v", test_file], capture_output=True, text=True)
        end_time = time.time()
        
        print(result.stdout)
        if result.stderr:
            print("ERRORS:")
            print(result.stderr)
        
        test_result = {
            "file": test_file,
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr,
            "time": end_time - start_time
        }
        results.append(test_result)
    
    return results

def print_summary(results):
    """Print a summary of the test results"""
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    
    print(f"\n\n{'=' * 80}")
    print(f"TEST SUMMARY")
    print(f"{'=' * 80}\n")
    
    print(f"Total test files: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED:")
        for result in results:
            if not result["success"]:
                print(f"  - {result['file']}")
    
    print("\nDetailed Results:")
    for result in results:
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"{status} - {result['file']} ({result['time']:.2f}s)")
        
        # Extract test counts from pytest output
        import re
        match = re.search(r'collected (\d+) items', result["output"])
        if match:
            test_count = match.group(1)
            print(f"       {test_count} tests")

def main():
    """Main function"""
    print_header()
    
    print("Starting CLI tests...")
    start_time = time.time()
    results = run_tests()
    end_time = time.time()
    
    print_summary(results)
    
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
    print(f"Test run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return non-zero exit code if any tests failed
    if not all(r["success"] for r in results):
        sys.exit(1)

if __name__ == "__main__":
    main() 