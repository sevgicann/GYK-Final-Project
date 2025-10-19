#!/usr/bin/env python3
"""Script to create database tables"""

from app import app, db
from flask import current_app

def create_tables():
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("✅ Tables created successfully!")
            
            # List all tables
            result = db.engine.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            tables = [row[0] for row in result]
            print(f"Created tables: {tables}")
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()