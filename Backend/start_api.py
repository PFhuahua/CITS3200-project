#!/usr/bin/env python3
"""
Startup script for the Census PDF Finder API
"""

import uvicorn
from backend.api  import app

if __name__ == "__main__":
    print("Starting Census PDF Finder API...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "backend.api:app",  # Import string format to avoid warning
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
 