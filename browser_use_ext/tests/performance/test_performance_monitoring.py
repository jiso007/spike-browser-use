"""
Performance monitoring tests to catch regressions in test execution time.

These tests help ensure the test suite remains fast and reliable.
"""

import time
import pytest
import sys
import os
from pathlib import Path

# Performance budgets (in seconds)
PERFORMANCE_BUDGETS = {
    'unit_test_suite': 5.0,      # All unit tests should complete in 5 seconds
    'integration_test_suite': 3.0,  # All integration tests should complete in 3 seconds
    'single_unit_test': 1.0,     # Any single unit test should complete in 1 second
    'single_integration_test': 2.0,  # Any single integration test should complete in 2 seconds
}

def run_test_suite(test_pattern: str) -> float:
    """Run a test suite and return execution time in seconds."""
    import subprocess
    
    start_time = time.time()
    
    # Run tests with minimal output
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 
        test_pattern,
        '--tb=no',      # No traceback
        '--quiet',      # Minimal output
        '--disable-warnings'  # No warnings
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent.parent)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    if result.returncode != 0:
        pytest.fail(f"Test suite {test_pattern} failed:\n{result.stdout}\n{result.stderr}")
    
    return execution_time

@pytest.mark.performance
def test_unit_test_performance():
    """Ensure unit tests complete within performance budget."""
    test_pattern = "browser_use_ext/tests/unit/javascript/"
    execution_time = run_test_suite(test_pattern)
    
    budget = PERFORMANCE_BUDGETS['unit_test_suite']
    assert execution_time <= budget, (
        f"Unit test suite took {execution_time:.2f}s, "
        f"exceeding budget of {budget}s"
    )
    
    print(f"✅ Unit tests completed in {execution_time:.2f}s (budget: {budget}s)")

@pytest.mark.performance  
def test_integration_test_performance():
    """Ensure integration tests complete within performance budget."""
    test_pattern = "browser_use_ext/tests/integration/javascript/"
    execution_time = run_test_suite(test_pattern)
    
    budget = PERFORMANCE_BUDGETS['integration_test_suite']
    assert execution_time <= budget, (
        f"Integration test suite took {execution_time:.2f}s, "
        f"exceeding budget of {budget}s"
    )
    
    print(f"✅ Integration tests completed in {execution_time:.2f}s (budget: {budget}s)")

@pytest.mark.performance
def test_individual_test_performance():
    """Check for any individual tests that are too slow."""
    # This would require more sophisticated test result parsing
    # For now, we'll just validate that the concept works
    
    # Example: Test that a specific slow test stays within budget
    test_pattern = "browser_use_ext/tests/unit/javascript/content_test.js"
    execution_time = run_test_suite(test_pattern)
    
    budget = PERFORMANCE_BUDGETS['single_unit_test']
    assert execution_time <= budget, (
        f"Individual test took {execution_time:.2f}s, "
        f"exceeding budget of {budget}s"
    )
    
    print(f"✅ Individual test completed in {execution_time:.2f}s (budget: {budget}s)")

@pytest.mark.performance
def test_test_suite_scalability():
    """Ensure test suite scales reasonably with number of tests."""
    # Run full Jest test suite
    test_pattern = "browser_use_ext/tests/"
    execution_time = run_test_suite(test_pattern)
    
    # For 76 tests, should complete well under 10 seconds
    max_allowed_time = 10.0
    assert execution_time <= max_allowed_time, (
        f"Full test suite took {execution_time:.2f}s, "
        f"exceeding maximum of {max_allowed_time}s"
    )
    
    print(f"✅ Full test suite completed in {execution_time:.2f}s (max: {max_allowed_time}s)")

def test_performance_budget_report():
    """Generate a performance report showing all test timing."""
    print("\n" + "="*60)
    print("📊 PERFORMANCE BUDGET REPORT")
    print("="*60)
    
    test_suites = {
        "Unit Tests": "browser_use_ext/tests/unit/javascript/",
        "Integration Tests": "browser_use_ext/tests/integration/javascript/",
    }
    
    for suite_name, pattern in test_suites.items():
        try:
            execution_time = run_test_suite(pattern)
            print(f"{suite_name:20} | {execution_time:6.2f}s")
        except Exception as e:
            print(f"{suite_name:20} | ERROR: {e}")
    
    print("="*60)
    print("Budget Guidelines:")
    for budget_name, budget_time in PERFORMANCE_BUDGETS.items():
        print(f"  {budget_name:25} | {budget_time:6.1f}s")
    print("="*60)

# Run performance tests with:
# poetry run pytest browser_use_ext/tests/performance/ -v -m performance