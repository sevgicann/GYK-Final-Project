#!/usr/bin/env python3
"""
Accessibility Test Runner for TerraMind Project

Bu script TerraMind projesinin erişilebilirlik testlerini çalıştırmak için kullanılır.
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


def run_backend_accessibility_tests(test_type=None, coverage=False, verbose=False):
    """Run backend accessibility tests."""
    print("=" * 60)
    print("Running Backend Accessibility Tests")
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
    
    cmd_parts.append("../tests/accessibility/backend/")
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_frontend_accessibility_tests(test_type=None, coverage=False, verbose=False):
    """Run frontend accessibility tests."""
    print("=" * 60)
    print("Running Frontend Accessibility Tests")
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
    
    # Test accessibility directory
    cmd_parts.append("test/accessibility/")
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_location_tests(coverage=False, verbose=False):
    """Run location accessibility tests."""
    print("=" * 60)
    print("Running Location Accessibility Tests")
    print("=" * 60)
    
    backend_success = run_backend_accessibility_tests("location", coverage, verbose)
    frontend_success = run_frontend_accessibility_tests("location", coverage, verbose)
    
    return backend_success and frontend_success


def run_network_tests(coverage=False, verbose=False):
    """Run network accessibility tests."""
    print("=" * 60)
    print("Running Network Accessibility Tests")
    print("=" * 60)
    
    backend_success = run_backend_accessibility_tests("network", coverage, verbose)
    frontend_success = run_frontend_accessibility_tests("network", coverage, verbose)
    
    return backend_success and frontend_success


def run_gps_tests(coverage=False, verbose=False):
    """Run GPS accessibility tests."""
    print("=" * 60)
    print("Running GPS Accessibility Tests")
    print("=" * 60)
    
    backend_success = run_backend_accessibility_tests("gps", coverage, verbose)
    frontend_success = run_frontend_accessibility_tests("gps", coverage, verbose)
    
    return backend_success and frontend_success


def run_offline_tests(coverage=False, verbose=False):
    """Run offline accessibility tests."""
    print("=" * 60)
    print("Running Offline Accessibility Tests")
    print("=" * 60)
    
    backend_success = run_backend_accessibility_tests("offline", coverage, verbose)
    frontend_success = run_frontend_accessibility_tests("offline", coverage, verbose)
    
    return backend_success and frontend_success


def run_all_accessibility_tests(coverage=False, verbose=False):
    """Run all accessibility tests."""
    print("=" * 60)
    print("Running All Accessibility Tests")
    print("=" * 60)
    
    location_success = run_location_tests(coverage, verbose)
    network_success = run_network_tests(coverage, verbose)
    gps_success = run_gps_tests(coverage, verbose)
    offline_success = run_offline_tests(coverage, verbose)
    
    return location_success and network_success and gps_success and offline_success


def generate_accessibility_report():
    """Generate accessibility test report."""
    print("=" * 60)
    print("Generating Accessibility Test Report")
    print("=" * 60)
    
    # Generate backend coverage report
    backend_dir = Path("backend")
    if backend_dir.exists():
        os.chdir(backend_dir)
        run_command("python -m pytest --cov=. --cov-report=html --cov-report=xml ../tests/accessibility/")
        os.chdir("..")
        print("Backend accessibility coverage report generated in backend/htmlcov/")
    
    # Generate frontend coverage report
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        os.chdir(frontend_dir)
        run_command("flutter test --coverage test/accessibility/")
        os.chdir("..")
        print("Frontend accessibility coverage report generated in frontend/coverage/")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="TerraMind Accessibility Test Runner")
    parser.add_argument("--type", choices=["location", "network", "gps", "offline", "all"], 
                       default="all", help="Type of accessibility tests to run")
    parser.add_argument("--backend-only", action="store_true", 
                       help="Run only backend accessibility tests")
    parser.add_argument("--frontend-only", action="store_true", 
                       help="Run only frontend accessibility tests")
    parser.add_argument("--coverage", action="store_true", 
                       help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--report", action="store_true", 
                       help="Generate accessibility test report")
    
    args = parser.parse_args()
    
    # Run tests
    success = True
    
    if args.backend_only:
        if args.type == "location":
            success = run_backend_accessibility_tests("location", args.coverage, args.verbose)
        elif args.type == "network":
            success = run_backend_accessibility_tests("network", args.coverage, args.verbose)
        elif args.type == "gps":
            success = run_backend_accessibility_tests("gps", args.coverage, args.verbose)
        elif args.type == "offline":
            success = run_backend_accessibility_tests("offline", args.coverage, args.verbose)
        else:
            success = run_backend_accessibility_tests(coverage=args.coverage, verbose=args.verbose)
    elif args.frontend_only:
        if args.type == "location":
            success = run_frontend_accessibility_tests("location", args.coverage, args.verbose)
        elif args.type == "network":
            success = run_frontend_accessibility_tests("network", args.coverage, args.verbose)
        elif args.type == "gps":
            success = run_frontend_accessibility_tests("gps", args.coverage, args.verbose)
        elif args.type == "offline":
            success = run_frontend_accessibility_tests("offline", args.coverage, args.verbose)
        else:
            success = run_frontend_accessibility_tests(coverage=args.coverage, verbose=args.verbose)
    else:
        if args.type == "location":
            success = run_location_tests(args.coverage, args.verbose)
        elif args.type == "network":
            success = run_network_tests(args.coverage, args.verbose)
        elif args.type == "gps":
            success = run_gps_tests(args.coverage, args.verbose)
        elif args.type == "offline":
            success = run_offline_tests(args.coverage, args.verbose)
        else:
            success = run_all_accessibility_tests(args.coverage, args.verbose)
    
    # Generate report if requested
    if args.report:
        generate_accessibility_report()
    
    # Print results
    print("=" * 60)
    if success:
        print("✅ All accessibility tests passed!")
    else:
        print("❌ Some accessibility tests failed!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
