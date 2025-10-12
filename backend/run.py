#!/usr/bin/env python3
"""
Terramind Backend API Runner
"""

import os
from app import app

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Starting Terramind API server...")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Server: http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Health check: http://{host}:{port}/health")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )
