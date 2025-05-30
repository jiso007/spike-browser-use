#!/usr/bin/env python3
"""
Comprehensive test runner for the browser-use extension project.

This script demonstrates the complete testing strategy:
1. Unit tests (Jest + Python)
2. Integration tests (Jest + Python) 
3. Performance monitoring
4. E2E tests (optional, requires browser setup)

Usage:
    python run_all_tests.py                    # Run all tests except E2E
    python run_all_tests.py --include-e2e      # Run all tests including E2E
    python run_all_tests.py --only-jest        # Run only Jest tests
    python run_all_tests.py --only-python      # Run only Python tests
    python run_all_tests.py --performance      # Run only performance tests
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

def run_command(cmd: List[str], description: str) -> Tuple[bool, float]:
    """Run a command and return (success, execution_time)."""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    execution_time = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED ({execution_time:.2f}s)")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return True, execution_time
    else:
        print(f"❌ {description} - FAILED ({execution_time:.2f}s)")
        if result.stderr.strip():
            print(f"Error: {result.stderr.strip()}")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return False, execution_time

def main():
    parser = argparse.ArgumentParser(description="Run browser-use extension tests")
    parser.add_argument("--include-e2e", action="store_true", 
                       help="Include E2E tests (requires manual browser setup)")
    parser.add_argument("--only-jest", action="store_true",
                       help="Run only Jest (JavaScript) tests")
    parser.add_argument("--only-python", action="store_true", 
                       help="Run only Python tests")
    parser.add_argument("--performance", action="store_true",
                       help="Run only performance monitoring tests")
    
    args = parser.parse_args()
    
    # Change to project directory
    project_root = Path(__file__).parent
    print(f"🏠 Project root: {project_root}")
    
    results = []
    total_start_time = time.time()
    
    print("\n" + "="*60)
    print("🧪 BROWSER-USE EXTENSION TEST SUITE")
    print("="*60)
    
    # Performance tests only
    if args.performance:
        print("\n📊 Running Performance Monitoring Tests...")
        success, exec_time = run_command([
            "poetry", "run", "pytest", 
            "browser_use_ext/tests/performance/",
            "-v", "-m", "performance"
        ], "Performance Tests")
        results.append(("Performance Tests", success, exec_time))
    
    # Jest tests only
    elif args.only_jest:
        print("\n🟨 Running Jest (JavaScript) Tests...")
        success, exec_time = run_command([
            "npm", "test"
        ], "Jest Tests (Unit + Integration)")
        results.append(("Jest Tests", success, exec_time))
    
    # Python tests only
    elif args.only_python:
        print("\n🐍 Running Python Tests...")
        
        # Python unit tests
        success, exec_time = run_command([
            "poetry", "run", "pytest",
            "browser_use_ext/tests/unit/python/",
            "-v"
        ], "Python Unit Tests")
        results.append(("Python Unit Tests", success, exec_time))
        
        # Python integration tests
        success, exec_time = run_command([
            "poetry", "run", "pytest",
            "browser_use_ext/tests/integration/python/", 
            "-v"
        ], "Python Integration Tests")
        results.append(("Python Integration Tests", success, exec_time))
    
    # Full test suite
    else:
        print("\n🟨 Running Jest (JavaScript) Tests...")
        success, exec_time = run_command([
            "npm", "test"
        ], "Jest Tests (Unit + Integration)")
        results.append(("Jest Tests", success, exec_time))
        
        print("\n🐍 Running Python Tests...")
        
        # Python unit tests
        success, exec_time = run_command([
            "poetry", "run", "pytest",
            "browser_use_ext/tests/unit/python/",
            "-v"
        ], "Python Unit Tests")
        results.append(("Python Unit Tests", success, exec_time))
        
        # Python integration tests  
        success, exec_time = run_command([
            "poetry", "run", "pytest",
            "browser_use_ext/tests/integration/python/",
            "-v"
        ], "Python Integration Tests")
        results.append(("Python Integration Tests", success, exec_time))
        
        # E2E tests (optional)
        if args.include_e2e:
            print("\n🌐 Running E2E Tests...")
            print("⚠️  E2E tests require manual browser setup:")
            print("   1. Open Chrome browser")
            print("   2. Load extension from browser_use_ext/extension/")
            print("   3. Ensure WS_URL points to ws://localhost:8766")
            print("   4. Open at least one tab")
            
            input("Press Enter when browser is ready, or Ctrl+C to skip...")
            
            success, exec_time = run_command([
                "poetry", "run", "pytest",
                "browser_use_ext/tests/e2e/python/test_extension_basic_e2e.py",
                "-v", "-m", "e2e"
            ], "E2E Tests (Basic)")
            results.append(("E2E Tests", success, exec_time))
    
    # Summary
    total_time = time.time() - total_start_time
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    passed_count = 0
    failed_count = 0
    
    for test_name, success, exec_time in results:
        status = "✅ PASS" if success else "❌ FAIL" 
        print(f"{test_name:25} | {status} | {exec_time:6.2f}s")
        if success:
            passed_count += 1
        else:
            failed_count += 1
    
    print("-" * 60)
    print(f"Total Tests Run: {len(results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print(f"Total Time: {total_time:.2f}s")
    
    if failed_count == 0:
        print("\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n💥 {failed_count} TEST SUITE(S) FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()