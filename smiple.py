# !/usr/bin/env python3
"""
Simple Voice Bot Tester - Runner
"""

import os
import time
import sys
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('.') / '.env'
print(f"Loading .env from: {env_path.absolute()}")
load_dotenv(dotenv_path=env_path, override=True)

# Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
TARGET_NUMBER = os.environ.get('TARGET_NUMBER', '+18054398008')

# Debug print
print("\n=== Configuration Check ===")
print(f"TWILIO_ACCOUNT_SID: {'✓' if TWILIO_ACCOUNT_SID else '✗'}")
print(f"TWILIO_AUTH_TOKEN: {'✓' if TWILIO_AUTH_TOKEN else '✗'}")
print(f"TWILIO_PHONE_NUMBER: {TWILIO_PHONE_NUMBER or '✗ MISSING'}")
print(f"OPENAI_API_KEY: {'✓' if OPENAI_API_KEY else '✗'}")
print(f"TARGET_NUMBER: {TARGET_NUMBER}")
print("==========================\n")

# Check required variables
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OPENAI_API_KEY]):
    print("ERROR: Missing required environment variables!")
    sys.exit(1)

# Initialize Twilio
try:
    from twilio.rest import Client
    from twilio.twiml.voice_response import VoiceResponse, Gather

    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✓ Twilio client initialized")
except Exception as e:
    print(f"✗ Error initializing Twilio: {e}")
    sys.exit(1)

# Test scenarios
SCENARIOS = [
    {
        "name": "New Patient Scheduling",
        "opening": "Hi, I'm a new patient and would like to schedule an appointment.",
    },
    {
        "name": "Medication Refill",
        "opening": "Hello, I need to request a refill for my blood pressure medication.",
    },
    {
        "name": "Sunday Appointment",
        "opening": "Hi, I need to schedule an appointment. I can only come in on Sundays.",
    },
    {
        "name": "Cancel Appointment",
        "opening": "I need to cancel my appointment for next week.",
    },
    {
        "name": "Insurance Question",
        "opening": "Do you accept Blue Cross insurance? I'm thinking of switching.",
    }
]


def make_test_call(scenario, call_number):
    """Make a single test call"""
    print(f"\n[{call_number}/5] Testing: {scenario['name']}")
    print(f"  From: {TWILIO_PHONE_NUMBER}")
    print(f"  To: {TARGET_NUMBER}")

    try:
        # Create TwiML
        response = VoiceResponse()
        response.say(scenario['opening'])
        response.pause(length=2)
        response.say("Thank you. Goodbye.")

        # Make the call
        call = twilio_client.calls.create(
            twiml=str(response),
            to=TARGET_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            timeout=30
        )

        print(f"  ✓ Call initiated!")
        print(f"  Call SID: {call.sid}")
        print(f"  Status: {call.status}")

        return {
            'success': True,
            'call_sid': call.sid,
            'scenario': scenario['name'],
            'status': call.status
        }

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return {
            'success': False,
            'scenario': scenario['name'],
            'error': str(e)
        }


def save_transcript(call_data, filename):
    """Save call information"""
    os.makedirs("transcripts", exist_ok=True)

    with open(f"transcripts/{filename}", 'w') as f:
        f.write(f"CALL TRANSCRIPT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Scenario: {call_data['scenario']}\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if call_data.get('call_sid'):
            f.write(f"Call SID: {call_data['call_sid']}\n")
        f.write(f"Status: {call_data.get('status', 'Failed')}\n")
        f.write("=" * 50 + "\n\n")


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("STARTING TEST CALLS")
    print("=" * 60)
    print(f"Making {len(SCENARIOS)} calls to {TARGET_NUMBER}")
    print("This will take a few minutes...")
    print("=" * 60)

    results = []

    for i, scenario in enumerate(SCENARIOS, 1):
        result = make_test_call(scenario, i)
        results.append(result)

        # Save transcript
        filename = f"transcript-{i:02d}.txt"
        save_transcript(result, filename)
        print(f"  Saved: transcripts/{filename}")

        # Wait between calls (except after last)
        if i < len(SCENARIOS):
            print("  Waiting 30 seconds before next call...")
            time.sleep(30)

    # Summary
    print("\n" + "=" * 60)
    print("CALL SUMMARY")
    print("=" * 60)
    successful = sum(1 for r in results if r['success'])
    print(f"Total calls: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    if successful > 0:
        print("\n✓ Calls have been initiated!")
        print("  Check your Twilio console for call details:")
        print(f"  https://console.twilio.com/?frameUrl=/console/phone-calls/logs/{TWILIO_ACCOUNT_SID}")
    else:
        print("\n✗ No successful calls. Check the errors above.")

    print("=" * 60)


# THIS IS THE IMPORTANT PART - make sure main() is called
if __name__ == "__main__":
    print("\n🚀 Starting voice bot tester...")
    main()
