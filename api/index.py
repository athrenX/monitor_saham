from app_simple import app

# Vercel serverless function handler
def handler(event, context):
    return app(event, context)
