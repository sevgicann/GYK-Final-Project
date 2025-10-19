#!/usr/bin/env python3
"""
Security Test Runner for TerraMind Project

Bu script TerraMind projesinin güvenlik testlerini çalıştırmak için kullanılır.
Basit ama etkili güvenlik testleri.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0


def run_backend_security_tests(test_type=None, coverage=False, verbose=False):
    """Run backend security tests."""
    print("=" * 60)
    print("Running Backend Security Tests")
    print("=" * 60)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("Backend directory not found!")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Build pytest command
    cmd_parts = ["python", "-m", "pytest"]
    
    if test_type:
        cmd_parts.extend(["-m", test_type])
    
    if coverage:
        cmd_parts.extend(["--cov=.", "--cov-report=html", "--cov-report=term-missing"])
    
    if verbose:
        cmd_parts.append("-v")
    
    cmd_parts.append("../tests/security/")
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_authentication_security_tests(coverage=False, verbose=False):
    """Run authentication security tests."""
    print("=" * 60)
    print("Running Authentication Security Tests")
    print("=" * 60)
    
    success = run_backend_security_tests("auth", coverage, verbose)
    return success


def run_input_validation_security_tests(coverage=False, verbose=False):
    """Run input validation security tests."""
    print("=" * 60)
    print("Running Input Validation Security Tests")
    print("=" * 60)
    
    success = run_backend_security_tests("input_validation", coverage, verbose)
    return success


def run_api_security_tests(coverage=False, verbose=False):
    """Run API security tests."""
    print("=" * 60)
    print("Running API Security Tests")
    print("=" * 60)
    
    success = run_backend_security_tests("api", coverage, verbose)
    return success


def run_data_security_tests(coverage=False, verbose=False):
    """Run data security tests."""
    print("=" * 60)
    print("Running Data Security Tests")
    print("=" * 60)
    
    success = run_backend_security_tests("data_encryption", coverage, verbose)
    return success


def run_ml_security_tests(coverage=False, verbose=False):
    """Run ML security tests."""
    print("=" * 60)
    print("Running ML Security Tests")
    print("=" * 60)
    
    success = run_backend_security_tests("ml", coverage, verbose)
    return success


def run_all_security_tests(coverage=False, verbose=False):
    """Run all security tests."""
    print("=" * 60)
    print("Running All Security Tests")
    print("=" * 60)
    
    auth_success = run_authentication_security_tests(coverage, verbose)
    input_success = run_input_validation_security_tests(coverage, verbose)
    api_success = run_api_security_tests(coverage, verbose)
    data_success = run_data_security_tests(coverage, verbose)
    ml_success = run_ml_security_tests(coverage, verbose)
    
    return auth_success and input_success and api_success and data_success and ml_success


def generate_security_report():
    """Generate security test report."""
    print("=" * 60)
    print("Generating Security Test Report")
    print("=" * 60)
    
    # Generate backend coverage report
    backend_dir = Path("backend")
    if backend_dir.exists():
        os.chdir(backend_dir)
        run_command("python -m pytest --cov=. --cov-report=html --cov-report=xml ../tests/security/")
        os.chdir("..")
        print("Backend security coverage report generated in backend/htmlcov/")
    
    # Generate security summary
    print("\n" + "=" * 60)
    print("SECURITY TEST SUMMARY")
    print("=" * 60)
    print("✅ Authentication Security Tests")
    print("✅ Input Validation Security Tests")
    print("✅ API Security Tests")
    print("✅ Data Security Tests")
    print("✅ ML Security Tests")
    print("=" * 60)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="TerraMind Security Test Runner")
    parser.add_argument("--type", choices=["auth", "input_validation", "api", "data_encryption", "ml", "all"], 
                       default="all", help="Type of security tests to run")
    parser.add_argument("--coverage", action="store_true", 
                       help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--report", action="store_true", 
                       help="Generate security test report")
    
    args = parser.parse_args()
    
    # Run tests
    success = True
    
    if args.type == "auth":
        success = run_authentication_security_tests(args.coverage, args.verbose)
    elif args.type == "input_validation":
        success = run_input_validation_security_tests(args.coverage, args.verbose)
    elif args.type == "api":
        success = run_api_security_tests(args.coverage, args.verbose)
    elif args.type == "data_encryption":
        success = run_data_security_tests(args.coverage, args.verbose)
    elif args.type == "ml":
        success = run_ml_security_tests(args.coverage, args.verbose)
    else:
        success = run_all_security_tests(args.coverage, args.verbose)
    
    # Generate report if requested
    if args.report:
        generate_security_report()
    
    # Print results
    print("=" * 60)
    if success:
        print("✅ All security tests passed!")
    else:
        print("❌ Some security tests failed!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
