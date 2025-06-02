#!/usr/bin/env python3
"""
E2E Test Runner for Browser-Use Extension

This script runs different types of E2E tests:
1. WebSocket-based E2E tests (no browser required)
2. Agent pipeline E2E tests (mock browser)
3. Full browser E2E tests (requires Playwright - optional)

Usage:
    python run_e2e_tests.py                    # Run all available E2E tests
    python run_e2e_tests.py --websocket-only   # Run only WebSocket E2E tests
    python run_e2e_tests.py --pipeline-only    # Run only pipeline E2E tests
    python run_e2e_tests.py --browser-only     # Run only browser E2E tests (requires Playwright)
    python run_e2e_tests.py --mock-only        # Run WebSocket + Pipeline tests (no browser)
"""

import subprocess
import sys
import argparse
import time
from pathlib import Path

def run_command(command, description, timeout=120):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🏃 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(command)}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent.parent.parent  # Project root
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED ({elapsed:.2f}s)")
            if result.stdout.strip():
                print(f"\nOutput:\n{result.stdout}")
            return True
        else:
            print(f"❌ {description} - FAILED ({elapsed:.2f}s)")
            if result.stderr.strip():
                print(f"\nError:\n{result.stderr}")
            if result.stdout.strip():
                print(f"\nOutput:\n{result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT ({timeout}s)")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False

def check_playwright_available():
    """Check if Playwright browsers are available."""
    try:
        result = subprocess.run(
            ["python", "-c", "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description="Run E2E tests for browser-use extension")
    parser.add_argument("--websocket-only", action="store_true", help="Run only WebSocket E2E tests")
    parser.add_argument("--pipeline-only", action="store_true", help="Run only pipeline E2E tests")
    parser.add_argument("--browser-only", action="store_true", help="Run only browser E2E tests")
    parser.add_argument("--mock-only", action="store_true", help="Run WebSocket + Pipeline tests (no browser)")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout per test suite in seconds")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose pytest output")
    
    args = parser.parse_args()
    
    # Set up pytest command base
    pytest_base = ["python", "-m", "pytest"]
    if args.verbose:
        pytest_base.append("-v")
    
    # Check Poetry availability
    poetry_available = False
    try:
        result = subprocess.run(["poetry", "--version"], capture_output=True, timeout=5)
        poetry_available = result.returncode == 0
    except:
        pass
    
    if poetry_available:
        pytest_cmd = ["poetry", "run"] + pytest_base
        print("📦 Using Poetry for test execution")
    else:
        pytest_cmd = pytest_base
        print("🐍 Using system Python for test execution")
    
    # Test configurations
    tests = []
    
    if args.websocket_only or args.mock_only or not any([args.websocket_only, args.pipeline_only, args.browser_only, args.mock_only]):
        tests.append({
            "name": "WebSocket E2E Tests",
            "command": pytest_cmd + ["browser_use_ext/tests/e2e/python/test_agent_websocket_e2e.py"],
            "description": "WebSocket-based E2E tests (agent + extension communication)"
        })
    
    if args.pipeline_only or args.mock_only or not any([args.websocket_only, args.pipeline_only, args.browser_only, args.mock_only]):
        tests.append({
            "name": "Simple E2E Tests", 
            "command": pytest_cmd + ["browser_use_ext/tests/e2e/python/test_simple_agent_e2e.py"],
            "description": "Simple agent E2E tests (core functionality)"
        })
    
    if args.browser_only or not any([args.websocket_only, args.pipeline_only, args.browser_only, args.mock_only]):
        # Check if Playwright is available
        playwright_available = check_playwright_available()
        
        if playwright_available:
            tests.append({
                "name": "Browser E2E Tests",
                "command": pytest_cmd + ["browser_use_ext/tests/e2e/python/test_extension_basic_e2e.py"],
                "description": "Full browser E2E tests (requires Playwright)"
            })
        else:
            print("⚠️  Playwright browsers not available - skipping browser E2E tests")
            print("   To install: poetry run playwright install chromium")
    
    if not tests:
        print("❌ No tests selected or available to run")
        return 1
    
    # Run tests
    print(f"🧪 Running {len(tests)} E2E test suite(s)")
    print(f"⏱️  Timeout: {args.timeout}s per suite")
    
    results = []
    total_start_time = time.time()
    
    for test in tests:
        success = run_command(
            test["command"],
            test["description"], 
            timeout=args.timeout
        )
        results.append({
            "name": test["name"],
            "success": success
        })
    
    total_elapsed = time.time() - total_start_time
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 E2E TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{result['name']:<30} | {status}")
    
    print(f"{'-'*60}")
    print(f"Total Tests Run: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total Time: {total_elapsed:.2f}s")
    
    if failed > 0:
        print(f"\n💥 {failed} E2E TEST SUITE(S) FAILED!")
        return 1
    else:
        print(f"\n🎉 ALL {passed} E2E TEST SUITES PASSED!")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)