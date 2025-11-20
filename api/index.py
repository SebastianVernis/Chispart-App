#!/usr/bin/env python3
"""
Vercel Serverless Entry Point for Blackbox Hybrid Tool
Adapts the FastAPI application for serverless deployment
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import main app
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app from main.py
from main import app

# Import Mangum for ASGI to AWS Lambda/Vercel adapter
from mangum import Mangum

# Configure for serverless environment
# Vercel uses /tmp for writable storage
os.environ.setdefault("WRITE_ROOT", "/tmp")

# Disable auto-snapshot in serverless environment (read-only filesystem except /tmp)
os.environ.setdefault("AUTO_SNAPSHOT", "false")

# Ensure config file path is correct
config_path = Path(__file__).parent.parent / "config" / "models.json"
if config_path.exists():
    os.environ.setdefault("CONFIG_FILE", str(config_path))

# Create Mangum handler for Vercel
handler = Mangum(app, lifespan="off")

# Export handler for Vercel
def lambda_handler(event, context):
    """
    AWS Lambda/Vercel handler function
    """
    return handler(event, context)
