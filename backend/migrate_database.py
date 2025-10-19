#!/usr/bin/env python3
"""
Database migration script for Terramind
This script handles database migrations and updates
"""

import os
import sys
from datetime import datetime
from flask import Flask
from flask_migrate import Migrate, upgrade, init, migrate as flask_migrate
from app import app, db
from utils.logger import get_logger, log_info, log_error, log_success

# Initialize logger
logger = get_logger('migrate_database')

def init_migration():
    """Initialize Flask-Migrate if not already initialized"""
    try:
        log_info("Initializing Flask-Migrate...")
        init()
        log_success("Flask-Migrate initialized successfully")
        return True
    except Exception as e:
        log_error(f"Failed to initialize Flask-Migrate: {str(e)}")
        return False

def create_migration(message="Auto migration"):
    """Create a new migration"""
    try:
        log_info(f"Creating migration: {message}")
        flask_migrate(message=message)
        log_success(f"Migration created successfully: {message}")
        return True
    except Exception as e:
        log_error(f"Failed to create migration: {str(e)}")
        return False

def upgrade_database():
    """Upgrade database to latest version"""
    try:
        log_info("Upgrading database to latest version...")
        upgrade()
        log_success("Database upgraded successfully")
        return True
    except Exception as e:
        log_error(f"Failed to upgrade database: {str(e)}")
        return False

def create_tables():
    """Create all tables"""
    try:
        log_info("Creating all database tables...")
        with app.app_context():
            db.create_all()
        log_success("All tables created successfully")
        return True
    except Exception as e:
        log_error(f"Failed to create tables: {str(e)}")
        return False

def drop_tables():
    """Drop all tables (DANGEROUS!)"""
    try:
        log_info("Dropping all database tables...")
        with app.app_context():
            db.drop_all()
        log_success("All tables dropped successfully")
        return True
    except Exception as e:
        log_error(f"Failed to drop tables: {str(e)}")
        return False

def reset_database():
    """Reset database (drop and recreate all tables)"""
    try:
        log_info("Resetting database...")
        with app.app_context():
            db.drop_all()
            db.create_all()
        log_success("Database reset successfully")
        return True
    except Exception as e:
        log_error(f"Failed to reset database: {str(e)}")
        return False

def check_database_connection():
    """Check database connection"""
    try:
        log_info("Checking database connection...")
        with app.app_context():
            db.engine.execute('SELECT 1')
        log_success("Database connection successful")
        return True
    except Exception as e:
        log_error(f"Database connection failed: {str(e)}")
        return False

def show_database_info():
    """Show database information"""
    try:
        log_info("Getting database information...")
        with app.app_context():
            # Get database URL
            db_url = app.config['SQLALCHEMY_DATABASE_URI']
            log_info(f"Database URL: {db_url}")
            
            # Get table information
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            log_info(f"Tables in database: {tables}")
            
            # Get table counts
            for table in tables:
                try:
                    count = db.session.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                    log_info(f"Table '{table}': {count} records")
                except Exception as e:
                    log_error(f"Failed to get count for table '{table}': {str(e)}")
        
        return True
    except Exception as e:
        log_error(f"Failed to get database information: {str(e)}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python migrate_database.py <command>")
        print("Commands:")
        print("  init          - Initialize Flask-Migrate")
        print("  create <msg>  - Create a new migration")
        print("  upgrade       - Upgrade database to latest version")
        print("  create_tables - Create all tables")
        print("  drop_tables   - Drop all tables (DANGEROUS!)")
        print("  reset         - Reset database (drop and recreate)")
        print("  check         - Check database connection")
        print("  info          - Show database information")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        success = init_migration()
    elif command == "create":
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto migration"
        success = create_migration(message)
    elif command == "upgrade":
        success = upgrade_database()
    elif command == "create_tables":
        success = create_tables()
    elif command == "drop_tables":
        print("WARNING: This will drop all tables! Are you sure? (y/N)")
        confirm = input()
        if confirm.lower() == 'y':
            success = drop_tables()
        else:
            print("Operation cancelled.")
            success = True
    elif command == "reset":
        print("WARNING: This will reset the database! Are you sure? (y/N)")
        confirm = input()
        if confirm.lower() == 'y':
            success = reset_database()
        else:
            print("Operation cancelled.")
            success = True
    elif command == "check":
        success = check_database_connection()
    elif command == "info":
        success = show_database_info()
    else:
        print(f"Unknown command: {command}")
        success = False
    
    if success:
        print("Operation completed successfully!")
        sys.exit(0)
    else:
        print("Operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
