# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    TARGET_NUMBER = '+18054398008'  # The test number
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    MAX_CALL_DURATION = 180  # 3 minutes max
    MIN_CALL_DURATION = 60   # 1 minute minimum for valid calls
