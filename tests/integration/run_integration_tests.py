#!/usr/bin/env python3
"""
Integration Test Runner for TerraMind Project

Bu script TerraMind projesinin entegrasyon testlerini çalıştırmak için kullanılır.
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


def run_backend_integration_tests(test_type=None, coverage=False, verbose=False):
    """Run backend integration tests."""
    print("=" * 60)
    print("Running Backend Integration Tests")
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
    
    cmd_parts.append("../tests/integration/backend/")
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_frontend_integration_tests(test_type=None, coverage=False, verbose=False):
    """Run frontend integration tests."""
    print("=" * 60)
    print("Running Frontend Integration Tests")
    print("=" * 60)
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("Frontend directory not found!")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Build flutter test command
    cmd_parts = ["flutter", "test"]
    
    if test_type:
        cmd_parts.extend(["--name", test_type])
    
    if verbose:
        cmd_parts.append("--verbose")
    
    # Add coverage if requested
    if coverage:
        cmd_parts.extend(["--coverage", "--coverage-path=coverage/lcov.info"])
    
    # Test integration directory
    cmd_parts.append("test/integration/")
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_cross_platform_integration_tests(coverage=False, verbose=False):
    """Run cross-platform integration tests."""
    print("=" * 60)
    print("Running Cross-Platform Integration Tests")
    print("=" * 60)
    
    backend_success = run_backend_integration_tests("cross_platform", coverage, verbose)
    frontend_success = run_frontend_integration_tests("cross_platform", coverage, verbose)
    
    return backend_success and frontend_success


def run_api_integration_tests(coverage=False, verbose=False):
    """Run API integration tests."""
    print("=" * 60)
    print("Running API Integration Tests")
    print("=" * 60)
    
    backend_success = run_backend_integration_tests("api", coverage, verbose)
    frontend_success = run_frontend_integration_tests("api", coverage, verbose)
    
    return backend_success and frontend_success


def run_ml_integration_tests(coverage=False, verbose=False):
    """Run ML integration tests."""
    print("=" * 60)
    print("Running ML Integration Tests")
    print("=" * 60)
    
    backend_success = run_backend_integration_tests("ml", coverage, verbose)
    
    return backend_success


def run_database_integration_tests(coverage=False, verbose=False):
    """Run database integration tests."""
    print("=" * 60)
    print("Running Database Integration Tests")
    print("=" * 60)
    
    backend_success = run_backend_integration_tests("database", coverage, verbose)
    
    return backend_success


def run_all_integration_tests(coverage=False, verbose=False):
    """Run all integration tests."""
    print("=" * 60)
    print("Running All Integration Tests")
    print("=" * 60)
    
    api_success = run_api_integration_tests(coverage, verbose)
    ml_success = run_ml_integration_tests(coverage, verbose)
    database_success = run_database_integration_tests(coverage, verbose)
    cross_platform_success = run_cross_platform_integration_tests(coverage, verbose)
    
    return api_success and ml_success and database_success and cross_platform_success


def generate_integration_report():
    """Generate integration test report."""
    print("=" * 60)
    print("Generating Integration Test Report")
    print("=" * 60)
    
    # Generate backend coverage report
    backend_dir = Path("backend")
    if backend_dir.exists():
        os.chdir(backend_dir)
        run_command("python -m pytest --cov=. --cov-report=html --cov-report=xml ../tests/integration/")
        os.chdir("..")
        print("Backend integration coverage report generated in backend/htmlcov/")
    
    # Generate frontend coverage report
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        os.chdir(frontend_dir)
        run_command("flutter test --coverage test/integration/")
        os.chdir("..")
        print("Frontend integration coverage report generated in frontend/coverage/")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="TerraMind Integration Test Runner")
    parser.add_argument("--type", choices=["api", "ml", "database", "cross_platform", "all"], 
                       default="all", help="Type of integration tests to run")
    parser.add_argument("--backend-only", action="store_true", 
                       help="Run only backend integration tests")
    parser.add_argument("--frontend-only", action="store_true", 
                       help="Run only frontend integration tests")
    parser.add_argument("--coverage", action="store_true", 
                       help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--report", action="store_true", 
                       help="Generate integration test report")
    
    args = parser.parse_args()
    
    # Run tests
    success = True
    
    if args.backend_only:
        if args.type == "api":
            success = run_backend_integration_tests("api", args.coverage, args.verbose)
        elif args.type == "ml":
            success = run_backend_integration_tests("ml", args.coverage, args.verbose)
        elif args.type == "database":
            success = run_backend_integration_tests("database", args.coverage, args.verbose)
        elif args.type == "cross_platform":
            success = run_backend_integration_tests("cross_platform", args.coverage, args.verbose)
        else:
            success = run_backend_integration_tests(coverage=args.coverage, verbose=args.verbose)
    elif args.frontend_only:
        if args.type == "api":
            success = run_frontend_integration_tests("api", args.coverage, args.verbose)
        elif args.type == "cross_platform":
            success = run_frontend_integration_tests("cross_platform", args.coverage, args.verbose)
        else:
            success = run_frontend_integration_tests(coverage=args.coverage, verbose=args.verbose)
    else:
        if args.type == "api":
            success = run_api_integration_tests(args.coverage, args.verbose)
        elif args.type == "ml":
            success = run_ml_integration_tests(args.coverage, args.verbose)
        elif args.type == "database":
            success = run_database_integration_tests(args.coverage, args.verbose)
        elif args.type == "cross_platform":
            success = run_cross_platform_integration_tests(args.coverage, args.verbose)
        else:
            success = run_all_integration_tests(args.coverage, args.verbose)
    
    # Generate report if requested
    if args.report:
        generate_integration_report()
    
    # Print results
    print("=" * 60)
    if success:
        print("✅ All integration tests passed!")
    else:
        print("❌ Some integration tests failed!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
