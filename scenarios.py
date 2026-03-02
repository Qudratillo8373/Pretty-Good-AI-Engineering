# bot/scenarios.py
from enum import Enum
from typing import Dict, List, Optional
import random


class PatientScenario:
    """Defines different patient scenarios for testing"""

    def __init__(self, name: str, context: str, goals: List[str],
                 personality: str = "cooperative", edge_case: bool = False):
        self.name = name
        self.context = context  # Patient history/background
        self.goals = goals  # What the patient wants to accomplish
        self.personality = personality  # cooperative, confused, frustrated, etc.
        self.edge_case = edge_case


class ScenarioGenerator:
    """Generates realistic patient scenarios"""

    BASE_SCENARIOS = [
        PatientScenario(
            name="New Patient Scheduling",
            context="New to the area, looking for a primary care physician",
            goals=["Schedule first appointment", "Ask about insurance acceptance"],
            personality="cooperative"
        ),
        PatientScenario(
            name="Medication Refill",
            context="Existing patient, needs blood pressure medication refill",
            goals=["Request refill", "Ask about pickup time"],
            personality="cooperative"
        ),
        PatientScenario(
            name="Sunday Appointment Request",
            context="Works weekdays, can only do weekends",
            goals=["Schedule weekend appointment", "Express frustration if not available"],
            personality="frustrated",
            edge_case=True  # Testing weekend scheduling logic
        ),
        PatientScenario(
            name="Multiple Issues",
            context="Has several questions and needs",
            goals=["Ask about test results", "Schedule follow-up", "Request referral"],
            personality="anxious",
            edge_case=True  # Testing multi-topic handling
        ),
        PatientScenario(
            name="Vague Symptoms",
            context="Not sure what's wrong but feels unwell",
            goals=["Describe vague symptoms", "Get appointment", "Ask about urgent care"],
            personality="confused"
        ),
        PatientScenario(
            name="Cancel and Reschedule",
            context="Has existing appointment next week but needs to change",
            goals=["Cancel current appointment", "Find new time next month"],
            personality="apologetic"
        ),
        PatientScenario(
            name="Insurance Question",
            context="Considering switching insurance plans",
            goals=["Verify insurance acceptance", "Ask about coverage details"],
            personality="detailed",
            edge_case=True  # Testing detailed insurance knowledge
        ),
        PatientScenario(
            name="Interruption Test",
            context="Tends to interrupt and talk over the agent",
            goals=["Schedule appointment", "Keep interrupting with additional details"],
            personality="interrupting",
            edge_case=True  # Testing interruption handling
        ),
        PatientScenario(
            name="Hearing Difficulty",
            context="Elderly patient with hearing issues",
            goals=["Ask for repetition", "Confirm understanding slowly"],
            personality="hard_of_hearing",
            edge_case=True  # Testing clear communication
        ),
        PatientScenario(
            name="Emergency vs Non-emergency",
            context="Has chest pain but not sure if emergency",
            goals=["Describe symptoms", "Get guidance on urgency"],
            personality="worried",
            edge_case=True  # Testing triage handling
        ),
        PatientScenario(
            name="Language Barrier",
            context="Non-native English speaker, simple vocabulary",
            goals=["Simple appointment request", "Basic medication questions"],
            personality="simple_language"
        ),
        PatientScenario(
            name="Angry Patient",
            context="Had bad experience with billing",
            goals=["Complain about bill", "Demand explanation", "Still need appointment"],
            personality="angry",
            edge_case=True
        )
    ]

    @classmethod
    def get_scenario(cls, scenario_name: Optional[str] = None) -> PatientScenario:
        """Get a specific scenario or random one"""
        if scenario_name:
            for scenario in cls.BASE_SCENARIOS:
                if scenario.name == scenario_name:
                    return scenario
        return random.choice(cls.BASE_SCENARIOS)

    @classmethod
    def get_edge_cases(cls) -> List[PatientScenario]:
        """Get all edge case scenarios"""
        return [s for s in cls.BASE_SCENARIOS if s.edge_case]
