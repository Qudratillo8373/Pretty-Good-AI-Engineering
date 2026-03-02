# 🎙️ Pretty Good AI — Voice Bot Engineering Challenge

Automated **AI Patient Voice Bot** built in Python to test the Pretty Good AI phone agent by simulating real patient conversations, recording calls, generating transcripts, and identifying conversational bugs.

---

# ✅ Project Status

✔ Automated outbound calling
✔ Scenario-based patient simulation
✔ Voice recording
✔ Transcription pipeline
✔ AI response generation
✔ Bug detection system
✔ Secure environment configuration

---

# 🧠 Architecture Overview

This system acts as a **synthetic patient tester**.

**Flow**

1. Voice bot initiates call using Twilio
2. Bot speaks generated patient scenario
3. Pretty Good AI agent responds
4. Audio is recorded
5. Audio is transcribed
6. Transcript analyzed for bugs
7. Results stored as reports

The design prioritizes:

* simplicity
* real working calls
* modular components
* secure credentials

---

# 📂 Project Structure

```
Pretty-Good-AI-Engineering/
│
├── .env                     # Secrets (NOT committed)
├── .gitignore
├── README.md
├── requirements.txt
├── LICENSE
│
├── main.py                  # Entry point
├── voice_bot.py             # Bot orchestration
├── caller.py                # Twilio call handler
├── recorder.py              # Call recording logic
├── transcriber.py           # Speech → text
├── response_generator.py    # Patient dialogue generator
├── scenarios.py             # Test scenarios
├── bug_detector.py          # Bug analysis engine
├── simple_bot.py            # Basic fallback bot
│
├── transcripts/
└── bug_reports/
```

---

# 🧰 Technologies Used

* Python 3.9+
* Twilio Voice API
* OpenAI API
* Deepgram (Speech-to-Text)
* ElevenLabs (Text-to-Speech)
* python-dotenv

---

# ⚙️ Prerequisites

Install:

### Python

```
python3 --version
```

### Git

```
git --version
```

Create accounts:

* Twilio
* OpenAI
* Deepgram
* ElevenLabs

---

# 📦 Installation

Clone repository:

```
git clone https://github.com/YOUR_USERNAME/Pretty-Good-AI-Engineering.git
cd Pretty-Good-AI-Engineering
```

Create virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# 📄 requirements.txt

```
twilio
openai
python-dotenv
requests
deepgram-sdk
elevenlabs
```

---

# 🔐 Environment Configuration

Create environment file:

```
touch .env
```

Add:

```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

OPENAI_API_KEY=
DEEPGRAM_API_KEY=
ELEVENLABS_API_KEY=
```

---

# 🧾 .env.example

```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

OPENAI_API_KEY=
DEEPGRAM_API_KEY=
ELEVENLABS_API_KEY=
```

---

# 🚫 .gitignore

```
.env
.venv/
__pycache__/
*.pyc
```

---

# 🔧 Configuration

Environment variables are loaded through:

```
config/settings.py
```

Key configuration:

* Target Test Number → `+18054398008`
* Max Call Duration → 180 seconds
* Minimum Valid Call → 60 seconds

---

# ▶️ Running the Voice Bot

Activate environment:

```
source .venv/bin/activate
```

Run:

```
python main.py
```

The bot will:

1. Generate a patient scenario
2. Call the Pretty Good AI test number
3. Speak automatically
4. Record interaction
5. Save transcript
6. Analyze bugs

---

# ☎️ Call Scenarios

Implemented scenarios include:

* Appointment scheduling
* Rescheduling
* Medication refill
* Insurance questions
* Office hours inquiries
* Interruptions
* Confusing requests
* Edge-case stress tests

Minimum required: **10 full conversations**

---

# 📝 Transcripts

Saved automatically:

```
transcripts/transcript-01.txt
```

Format:

```
Patient:
Agent:
Patient:
Agent:
```

---

# 🐞 Bug Detection

Example bug report:

```
Bug: Appointment scheduled outside office hours
Severity: High
Call: transcript-07.txt
Timestamp: 01:23

Agent confirmed Sunday appointment despite clinic closure.
Expected behavior: Offer next weekday availability.
```

Reports saved in:

```
bug_reports/
```

---

# 🎥 Loom Walkthrough (Required Deliverable)

Record a ≤5 minute video explaining:

* Architecture decisions
* Call flow
* Bugs discovered
* Iteration improvements
* Engineering reasoning

---

# 🔒 Security

Never commit:

* API keys
* Tokens
* `.env` file

GitHub push protection will block exposed credentials.

---

# 🚀 Development Workflow

```
git add .
git commit -m "update"
git push origin main
```

---

# ⭐ Standout Improvements Implemented

* Modular micro-service design
* Automated bug discovery
* AI patient simulation
* Real telephony testing
* Secure environment loading
* Extensible architecture

---

# 📬 Submission

Send email to:

[kevin@prettygoodai.com](mailto:kevin@prettygoodai.com)

Include:

* GitHub repository link
* Loom walkthrough link
* Bot phone number (E.164 format)

Subject:

```
PGA I BUILT IT: Kudratillo Saydaliev +1XXXXXXXXXX
```

---

# 👨‍💻 Author

**Kudratillo Saydaliev**

DevOps Engineer | Cloud Engineer | Platform Engineer
AWS • GCP • Kubernetes • Terraform • AI Systems

---
