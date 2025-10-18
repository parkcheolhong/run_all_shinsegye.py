#!/usr/bin/env python3
"""
Simple test suite for run_all_shinsegye.py
"""

import subprocess
import sys
import os

def run_test(description, command, expected_exit_code=0):
    """Run a test and report result."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    
    success = result.returncode == expected_exit_code
    status = "✓ PASS" if success else "✗ FAIL"
    
    print(f"Exit code: {result.returncode} (expected: {expected_exit_code})")
    print(f"Status: {status}")
    
    if result.stdout:
        print(f"\nOutput:\n{result.stdout[:200]}")
    
    if result.stderr and not success:
        print(f"\nError:\n{result.stderr[:200]}")
    
    return success

def main():
    """Run all tests."""
    print("="*60)
    print("run_all_shinsegye.py Test Suite")
    print("="*60)
    
    os.chdir("/home/runner/work/run_all_shinsegye.py/run_all_shinsegye.py")
    
    tests = [
        ("Help output", "python run_all_shinsegye.py --help", 0),
        ("Single command", "python run_all_shinsegye.py --command 'echo test'", 0),
        ("Run Python script", "python run_all_shinsegye.py --script example_scripts/example_script1.py", 0),
        ("Run commands from file", "python run_all_shinsegye.py --file example_commands.txt", 0),
        ("Run all scripts in directory", "python run_all_shinsegye.py --directory example_scripts", 0),
        ("Verbose mode", "python run_all_shinsegye.py --command 'echo verbose' --verbose", 0),
        ("No arguments (should fail)", "python run_all_shinsegye.py", 1),
    ]
    
    results = []
    for description, command, expected_exit_code in tests:
        results.append(run_test(description, command, expected_exit_code))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"Total tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"{'='*60}\n")
    
    if failed > 0:
        print("Some tests failed!")
        sys.exit(1)
    else:
        print("All tests passed! 🎉")
        sys.exit(0)

if __name__ == '__main__':
    main()
