# call_recorder/recorder.py
import requests
from twilio.rest import Client
import json
from datetime import datetime


class CallRecorder:
    """Records and stores call audio and metadata"""

    def __init__(self, twilio_client, storage_path='calls/'):
        self.twilio_client = twilio_client
        self.storage_path = storage_path

    def record_call(self, call_sid: str):
        """Record a call using Twilio's recording API"""
        recording = self.twilio_client.calls(call_sid) \
            .recordings.create()

        # Wait for recording to be ready
        recording_data = self._wait_for_recording(recording.sid)

        # Download and save audio
        audio_url = f"https://api.twilio.com{recording_data.uri.replace('.json', '.wav')}"
        audio_content = requests.get(audio_url, auth=(
            self.twilio_client.username,
            self.twilio_client.password
        )).content

        filename = f"{self.storage_path}{call_sid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(filename, 'wb') as f:
            f.write(audio_content)

        return filename

    def _wait_for_recording(self, recording_sid: str, max_attempts=10):
        """Wait for recording to be ready"""
        import time

        for _ in range(max_attempts):
            recording = self.twilio_client.recordings(recording_sid).fetch()
            if recording.status == 'completed':
                return recording
            time.sleep(2)

        raise Exception("Recording timeout")
