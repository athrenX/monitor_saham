import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app_simple import app

# Export app for Vercel
# Vercel will automatically detect this as the WSGI app
application = app
