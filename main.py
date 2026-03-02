import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config.settings import Config
    print("✓ Successfully imported Config")
    print(f"  Target number: {Config.TARGET_NUMBER}")
    print("  Other settings loaded successfully")
except Exception as e:
    print(f"✗ Error importing Config: {e}")
    print("\nTroubleshooting steps:")
    print("1. Make sure you're in the correct directory:")
    print("   pwd  # Should show /Users/kudratillosaydaliev/PycharmProjects/PythonProject/pgai-voicebot")
    print("2. Check if config/settings.py exists:")
    print("   ls -la config/")
    print("3. Check if config/__init__.py exists:")
    print("   ls -la config/__init__.py")
    print("4. Make sure you have a .env file:")
    print("   ls -la .env")
