#!/usr/bin/env python3
"""
Database initialization script
Creates all tables if they don't exist
"""
import time
import sys
from sqlalchemy import create_engine, text
from db import models
from db.db import engine, DATABASE_URL

def wait_for_db(max_retries=30, delay=2):
    """Wait for database to be ready"""
    print("Waiting for database to be ready...")
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Database is ready!")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"  Attempt {i+1}/{max_retries}: Database not ready yet, waiting {delay}s...")
                time.sleep(delay)
            else:
                print(f"✗ Failed to connect to database after {max_retries} attempts")
                print(f"  Error: {e}")
                return False
    return False

def init_database():
    """Initialize database tables"""
    print("\n" + "="*60)
    print("DATABASE INITIALIZATION")
    print("="*60)
    print(f"Database URL: {DATABASE_URL}")
    
    if not wait_for_db():
        print("\n✗ Database initialization failed - database not available")
        sys.exit(1)
    
    try:
        print("\nCreating database tables...")
        models.Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"\n✓ Tables in database: {', '.join(tables)}")
        
        print("\n" + "="*60)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database()
