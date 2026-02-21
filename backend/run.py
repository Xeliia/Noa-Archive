"""
Run script for the chatbot backend with optional ngrok tunnel.

Usage:
    python run.py              # Run locally only
    python run.py --ngrok      # Run with ngrok tunnel
    python run.py --ngrok-auth YOUR_AUTH_TOKEN  # First time ngrok setup
"""

import argparse
import uvicorn
from config import get_settings


def main():
    parser = argparse.ArgumentParser(description="Run the chatbot backend")
    parser.add_argument("--ngrok", action="store_true", help="Enable ngrok tunnel")
    parser.add_argument("--ngrok-auth", type=str, help="Set ngrok auth token (one-time setup)")
    args = parser.parse_args()
    
    settings = get_settings()
    
    # Handle ngrok auth token setup
    if args.ngrok_auth:
        from pyngrok import ngrok
        ngrok.set_auth_token(args.ngrok_auth)
        print(f"✓ ngrok auth token saved")
    
    # Start ngrok tunnel if requested
    if args.ngrok:
        from pyngrok import ngrok
        
        # Create tunnel
        tunnel = ngrok.connect(settings.port, "http")
        public_url = tunnel.public_url
        
        print("\n" + "=" * 50)
        print("🚀 ngrok tunnel active!")
        print(f"   Public URL: {public_url}")
        print(f"   API endpoint: {public_url}/chat")
        print("=" * 50 + "\n")
        print(f"⚠️  Don't forget to update your frontend with this URL")
        print(f"   and include the API key in Authorization header:\n")
        print(f'   Authorization: Bearer {settings.api_key}\n')
    
    print(f"🤖 LLM Backend: {settings.llm_backend_url}")
    print(f"📦 Model: {settings.llm_model}\n")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True  # Auto-reload on code changes (dev mode)
    )


if __name__ == "__main__":
    main()
