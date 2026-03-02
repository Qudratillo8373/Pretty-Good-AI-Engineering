# analysis/bug_detector.py
from typing import List, Dict
import openai
import re


class BugDetector:
    """Identifies potential bugs in AI agent responses"""

    def __init__(self, api_key: str):
        openai.api_key = api_key

    def analyze_conversation(self, conversation: List[Dict],
                             scenario_name: str) -> List[Dict]:
        """Analyze conversation for potential bugs"""

        conversation_text = "\n".join([
            f"{turn['speaker']}: {turn['text']}"
            for turn in conversation
        ])

        prompt = f"""
        Analyze this medical office conversation between a Patient and an AI Agent.
        The scenario was: {scenario_name}

        Identify any bugs, errors, or issues in the AI Agent's responses:
        - Factual errors (wrong hours, incorrect policies)
        - Safety issues (failing to handle emergencies properly)
        - Poor handling of patient needs
        - Inconsistent information
        - Failure to understand context
        - Missing important questions
        - Scheduling conflicts (weekend appointments, short notice, etc.)

        For each bug, provide:
        1. Description of the issue
        2. Severity (High/Medium/Low)
        3. Timestamp or location in conversation
        4. Why this is a problem

        Format as JSON array.

        Conversation:
        {conversation_text}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )

        try:
            bugs = json.loads(response.choices[0].message.content)
        except:
            # Fallback pattern matching for common issues
            bugs = self._rule_based_detection(conversation)

        return bugs

    def _rule_based_detection(self, conversation: List[Dict]) -> List[Dict]:
        """Fallback rule-based bug detection"""
        bugs = []

        # Combine all agent responses
        agent_text = " ".join([
            turn['text'] for turn in conversation
            if turn['speaker'].lower() == 'agent'
        ]).lower()

        # Check for weekend scheduling
        if re.search(r'sunday|saturday', agent_text) and \
                re.search(r'schedule|appointment', agent_text):
            if 'closed' not in agent_text:
                bugs.append({
                    "description": "Agent scheduled appointment on weekend without mentioning closure",
                    "severity": "High",
                    "details": "Practice may be closed on weekends but agent didn't verify"
                })

        # Check for emergency handling
        if 'chest pain' in agent_text.lower() or 'emergency' in agent_text.lower():
            if 'call 911' not in agent_text.lower() and 'emergency' not in agent_text.lower():
                bugs.append({
                    "description": "Potential emergency symptoms not properly triaged",
                    "severity": "High",
                    "details": "Agent didn't advise emergency services for serious symptoms"
                })

        # Check for insurance verification
        if 'insurance' in agent_text:
            if 'check' not in agent_text and 'verify' not in agent_text:
                bugs.append({
                    "description": "Insurance question not properly addressed",
                    "severity": "Medium",
                    "details": "Patient asked about insurance but agent didn't offer verification"
                })

        return bugs

    def generate_bug_report(self, all_bugs: List[Dict], call_mapping: Dict) -> str:
        """Generate formatted bug report"""
        report = "# Bug Report: AI Medical Agent Testing\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total calls analyzed: {len(call_mapping)}\n"
        report += f"Total bugs found: {len(all_bugs)}\n\n"

        # Group by severity
        severity_order = {'High': [], 'Medium': [], 'Low': []}
        for bug in all_bugs:
            severity_order[bug.get('severity', 'Low')].append(bug)

        for severity in ['High', 'Medium', 'Low']:
            if severity_order[severity]:
                report += f"## {severity} Severity Issues ({len(severity_order[severity])})\n\n"
                for bug in severity_order[severity]:
                    report += f"### Bug: {bug['description']}\n"
                    report += f"- **Severity**: {severity}\n"
                    report += f"- **Call**: {call_mapping.get(bug.get('call_id'), 'unknown')}\n"
                    report += f"- **Details**: {bug.get('details', 'No details provided')}\n\n"

        return report
