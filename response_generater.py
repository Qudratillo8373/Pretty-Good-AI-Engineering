# bot/response_generator.py
import openai
from typing import List, Dict
from .scenarios import PatientScenario


class PatientResponseGenerator:
    """Generates realistic patient responses based on scenario"""

    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.conversation_history = []

    def generate_response(self, agent_message: str, scenario: PatientScenario) -> str:
        """Generate patient's next response based on scenario and conversation"""

        system_prompt = f"""
        You are a patient in a medical office phone conversation. 
        Your scenario: {scenario.context}
        Your goals: {', '.join(scenario.goals)}
        Your personality: {scenario.personality}

        Respond naturally to the AI agent's questions and statements.
        Stay in character and work toward your goals.
        Keep responses brief and conversational (1-2 sentences typically).
        """

        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history[-6:],  # Keep last few exchanges for context
            {"role": "user", "content": agent_message}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-3.5-turbo for cost efficiency
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )

        patient_response = response.choices[0].message.content
        self.conversation_history.append({"role": "user", "content": agent_message})
        self.conversation_history.append({"role": "assistant", "content": patient_response})

        return patient_response

    def reset_conversation(self):
        """Reset for new call"""
        self.conversation_history = []
