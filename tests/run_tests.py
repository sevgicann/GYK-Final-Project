#!/usr/bin/env python3
"""
Test Runner for TerraMind Project

Bu script TerraMind projesinin tüm testlerini çalıştırmak için kullanılır.
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


def run_backend_tests(test_type=None, coverage=False, verbose=False):
    """Run backend tests."""
    print("=" * 60)
    print("Running Backend Tests")
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
    
    cmd_parts.append("../tests/")
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_frontend_tests(test_type=None, coverage=False, verbose=False):
    """Run frontend tests."""
    print("=" * 60)
    print("Running Frontend Tests")
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
    
    command = " ".join(cmd_parts)
    
    success = run_command(command)
    
    # Change back to root directory
    os.chdir("..")
    
    return success


def run_all_tests(test_type=None, coverage=False, verbose=False):
    """Run all tests."""
    print("=" * 60)
    print("Running All Tests")
    print("=" * 60)
    
    backend_success = run_backend_tests(test_type, coverage, verbose)
    frontend_success = run_frontend_tests(test_type, coverage, verbose)
    
    return backend_success and frontend_success


def run_unit_tests(coverage=False, verbose=False):
    """Run unit tests only."""
    print("=" * 60)
    print("Running Unit Tests")
    print("=" * 60)
    
    backend_success = run_backend_tests("unit", coverage, verbose)
    frontend_success = run_frontend_tests("unit", coverage, verbose)
    
    return backend_success and frontend_success


def run_integration_tests(coverage=False, verbose=False):
    """Run integration tests only."""
    print("=" * 60)
    print("Running Integration Tests")
    print("=" * 60)
    
    backend_success = run_backend_tests("integration", coverage, verbose)
    # Frontend integration tests would be here if needed
    
    return backend_success


def run_security_tests(coverage=False, verbose=False):
    """Run security tests only."""
    print("=" * 60)
    print("Running Security Tests")
    print("=" * 60)
    
    backend_success = run_backend_tests("security", coverage, verbose)
    # Frontend security tests would be here if needed
    
    return backend_success


def install_test_dependencies():
    """Install test dependencies."""
    print("=" * 60)
    print("Installing Test Dependencies")
    print("=" * 60)
    
    # Install backend test dependencies
    backend_dir = Path("backend")
    if backend_dir.exists():
        os.chdir(backend_dir)
        success = run_command("pip install -r requirements-dev.txt")
        os.chdir("..")
        
        if not success:
            print("Failed to install backend test dependencies!")
            return False
    
    # Install frontend test dependencies
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        os.chdir(frontend_dir)
        success = run_command("flutter pub get")
        os.chdir("..")
        
        if not success:
            print("Failed to install frontend test dependencies!")
            return False
    
    return True


def generate_test_report():
    """Generate test report."""
    print("=" * 60)
    print("Generating Test Report")
    print("=" * 60)
    
    # Generate backend coverage report
    backend_dir = Path("backend")
    if backend_dir.exists():
        os.chdir(backend_dir)
        run_command("python -m pytest --cov=. --cov-report=html --cov-report=xml ../tests/")
        os.chdir("..")
        print("Backend coverage report generated in backend/htmlcov/")
    
    # Generate frontend coverage report
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        os.chdir(frontend_dir)
        run_command("flutter test --coverage")
        os.chdir("..")
        print("Frontend coverage report generated in frontend/coverage/")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="TerraMind Test Runner")
    parser.add_argument("--type", choices=["unit", "integration", "security", "all"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--backend-only", action="store_true", 
                       help="Run only backend tests")
    parser.add_argument("--frontend-only", action="store_true", 
                       help="Run only frontend tests")
    parser.add_argument("--coverage", action="store_true", 
                       help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--install-deps", action="store_true", 
                       help="Install test dependencies")
    parser.add_argument("--report", action="store_true", 
                       help="Generate test report")
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_test_dependencies():
            sys.exit(1)
    
    # Run tests
    success = True
    
    if args.backend_only:
        if args.type == "unit":
            success = run_unit_tests(args.coverage, args.verbose)
        elif args.type == "integration":
            success = run_integration_tests(args.coverage, args.verbose)
        elif args.type == "security":
            success = run_security_tests(args.coverage, args.verbose)
        else:
            success = run_backend_tests(coverage=args.coverage, verbose=args.verbose)
    elif args.frontend_only:
        success = run_frontend_tests(coverage=args.coverage, verbose=args.verbose)
    else:
        if args.type == "unit":
            success = run_unit_tests(args.coverage, args.verbose)
        elif args.type == "integration":
            success = run_integration_tests(args.coverage, args.verbose)
        elif args.type == "security":
            success = run_security_tests(args.coverage, args.verbose)
        else:
            success = run_all_tests(coverage=args.coverage, verbose=args.verbose)
    
    # Generate report if requested
    if args.report:
        generate_test_report()
    
    # Print results
    print("=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
