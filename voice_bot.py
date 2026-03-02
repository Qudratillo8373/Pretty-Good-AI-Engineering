# bot/voice_bot.py
import time
import threading
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import base64
import json
from typing import Optional, Callable
import wave
import os


class VoiceBot:
    """Main voice bot controller"""

    def __init__(self, config, response_generator, transcriber, tts_engine):
        self.config = config
        self.twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        self.response_generator = response_generator
        self.transcriber = transcriber
        self.tts_engine = tts_engine
        self.current_call_sid = None
        self.call_status = "idle"

    def make_call(self, to_number: str, scenario, callback: Optional[Callable] = None):
        """Initiate an outbound call"""

        # Generate initial patient greeting based on scenario
        initial_message = self._generate_opening(scenario)

        # Create TwiML for the call
        response = VoiceResponse()

        # Convert initial message to speech and play
        audio_url = self._text_to_speech(initial_message)
        response.play(audio_url)

        # Set up to receive and process response
        gather = Gather(
            input='speech',
            timeout=5,
            speech_timeout='auto',
            action='/process_response',
            method='POST'
        )
        response.append(gather)

        # If no input, redirect to handle timeout
        response.redirect('/handle_timeout')

        # Make the call
        call = self.twilio_client.calls.create(
            twiml=str(response),
            to=to_number,
            from_=self.config.TWILIO_PHONE_NUMBER,
            status_callback='/call_status',
            status_callback_event=['completed'],
            timeout=30
        )

        self.current_call_sid = call.sid
        self.call_status = "in_progress"

        # Store call metadata
        self._store_call_metadata(call.sid, scenario)

        # Monitor call in background
        threading.Thread(target=self._monitor_call, args=(call.sid, callback)).start()

        return call.sid

    def _generate_opening(self, scenario) -> str:
        """Generate opening statement based on scenario"""
        openings = {
            "New Patient Scheduling": "Hi, I'm a new patient and would like to schedule an appointment.",
            "Medication Refill": "Hello, I need to request a refill for my prescription.",
            "Sunday Appointment Request": "Hi, I need to schedule an appointment. I can only come in on Sundays.",
            # ... more openings
        }

        default = f"Hello, I need help with {scenario.name.lower()}."
        return openings.get(scenario.name, default)

    def _text_to_speech(self, text: str) -> str:
        """Convert text to speech and return URL"""
        # Implementation depends on TTS service
        # Returns publicly accessible URL of audio file
        pass

    def _store_call_metadata(self, call_sid: str, scenario):
        """Store call metadata for later analysis"""
        metadata = {
            'call_sid': call_sid,
            'scenario': scenario.name,
            'personality': scenario.personality,
            'edge_case': scenario.edge_case,
            'timestamp': time.time(),
            'status': 'initiated'
        }
        # Store in database or file
        with open(f'calls/{call_sid}_metadata.json', 'w') as f:
            json.dump(metadata, f)

    def _monitor_call(self, call_sid: str, callback: Optional[Callable]):
        """Monitor call progress"""
        max_duration = self.config.MAX_CALL_DURATION
        start_time = time.time()

        while time.time() - start_time < max_duration:
            call = self.twilio_client.calls(call_sid).fetch()
            if call.status in ['completed', 'busy', 'failed', 'no-answer', 'canceled']:
                self.call_status = call.status
                break
            time.sleep(5)

        # If still in progress after max duration, end call
        if self.call_status == 'in_progress':
            self.twilio_client.calls(call_sid).update(status='completed')
            self.call_status = 'timeout'

        # Execute callback if provided
        if callback:
            callback(call_sid, self.call_status)
