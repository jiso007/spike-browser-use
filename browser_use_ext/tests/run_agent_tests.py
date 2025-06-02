#!/usr/bin/env python3
"""
Test runner for agent integration tests.
Runs all unit and integration tests related to the agent functionality.
"""

import subprocess
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def run_python_tests():
    """Run Python unit and integration tests."""
    print("\n" + "="*60)
    print("Running Python Agent Tests")
    print("="*60 + "\n")
    
    test_files = [
        # Unit tests
        "browser_use_ext/tests/unit/python/test_extension_interface_agent.py",
        "browser_use_ext/tests/unit/python/test_llm_initialization.py",
        
        # Integration tests
        "browser_use_ext/tests/integration/python/test_agent_task_execution.py",
    ]
    
    failed_tests = []
    
    for test_file in test_files:
        print(f"\n{'='*40}")
        print(f"Running: {test_file}")
        print('='*40)
        
        result = subprocess.run(
            ["pytest", "-v", test_file],
            capture_output=False
        )
        
        if result.returncode != 0:
            failed_tests.append(test_file)
    
    return failed_tests


def run_javascript_tests():
    """Run JavaScript unit tests."""
    print("\n" + "="*60)
    print("Running JavaScript Agent Tests")
    print("="*60 + "\n")
    
    test_file = "browser_use_ext/tests/unit/javascript/test_user_task_submission_unit.js"
    
    print(f"Running: {test_file}")
    
    result = subprocess.run(
        ["npm", "test", "--", test_file],
        capture_output=False
    )
    
    return result.returncode != 0


def run_all_tests():
    """Run all agent-related tests."""
    print("\n🧪 Agent Integration Test Suite")
    print("================================\n")
    
    # Check for required environment
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: No LLM API keys found. Some tests may be skipped.")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY for full test coverage.\n")
    
    # Run Python tests
    python_failures = run_python_tests()
    
    # Run JavaScript tests
    js_failed = run_javascript_tests()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    total_failures = len(python_failures) + (1 if js_failed else 0)
    
    if total_failures == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ {total_failures} test suite(s) failed:")
        
        for test in python_failures:
            print(f"   - {test}")
        
        if js_failed:
            print("   - JavaScript tests")
    
    return total_failures


def run_coverage_report():
    """Run tests with coverage report."""
    print("\n📊 Running Tests with Coverage")
    print("="*60 + "\n")
    
    subprocess.run([
        "pytest",
        "--cov=browser_use_ext.extension_interface",
        "--cov=browser_use_ext.agent",
        "--cov-report=html",
        "--cov-report=term",
        "browser_use_ext/tests/unit/python/test_extension_interface_agent.py",
        "browser_use_ext/tests/unit/python/test_llm_initialization.py",
        "browser_use_ext/tests/integration/python/test_agent_task_execution.py"
    ])
    
    print("\n📁 Coverage report generated in htmlcov/index.html")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run agent integration tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--python-only", action="store_true", help="Run only Python tests")
    parser.add_argument("--js-only", action="store_true", help="Run only JavaScript tests")
    
    args = parser.parse_args()
    
    if args.coverage:
        run_coverage_report()
    elif args.python_only:
        failures = run_python_tests()
        sys.exit(len(failures))
    elif args.js_only:
        sys.exit(1 if run_javascript_tests() else 0)
    else:
        failures = run_all_tests()
        sys.exit(failures)