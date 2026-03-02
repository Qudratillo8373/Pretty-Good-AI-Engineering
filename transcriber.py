# analysis/transcriber.py
import openai
from typing import List, Dict
import json


class ConversationTranscriber:
    """Transcribes and analyzes conversations"""

    def __init__(self, api_key: str):
        openai.api_key = api_key

    def transcribe_audio(self, audio_file: str) -> str:
        """Transcribe audio file using Whisper API"""
        with open(audio_file, "rb") as f:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=f
            )
        return transcript.text

    def separate_speakers(self, transcript: str, num_speakers=2) -> List[Dict]:
        """Attempt to separate speakers in transcript"""
        # This is simplified - in production you'd use speaker diarization
        # For this challenge, manual separation might be acceptable

        prompt = f"""
        Separate this conversation transcript into speakers.
        The speakers are: Patient (your bot) and Agent (the AI being tested).

        Format as JSON array with each entry having 'speaker' and 'text' fields.

        Transcript: {transcript}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        try:
            return json.loads(response.choices[0].message.content)
        except:
            # Fallback - return as single speaker
            return [{"speaker": "unknown", "text": transcript}]

    def save_transcript(self, call_sid: str, conversation: List[Dict],
                        metadata: Dict, filename: str):
        """Save transcript to file"""
        with open(filename, 'w') as f:
            f.write(f"Call SID: {call_sid}\n")
            f.write(f"Scenario: {metadata.get('scenario', 'unknown')}\n")
            f.write(f"Edge Case: {metadata.get('edge_case', False)}\n")
            f.write(f"Timestamp: {metadata.get('timestamp', 'unknown')}\n")
            f.write("-" * 50 + "\n\n")

            for exchange in conversation:
                f.write(f"{exchange['speaker'].upper()}: {exchange['text']}\n\n")
