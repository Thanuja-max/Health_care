import os
import pip_system_certs.wrapt_requests  # noqa: F401 — fixes SSL on Windows
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "groq/compound-mini"


def get_client():
    api_key = os.getenv("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key not found. Add groq_api_key to your .env file.")
    return Groq(api_key=api_key)


def ask_health_assistant(profile: dict, user_message: str, chat_history: list) -> str:
    client = get_client()

    profile_context = f"""
Child Profile:
- Name: {profile['name']}
- Age: {profile['age']} years
- Gender: {profile['gender']}
- Blood Group: {profile.get('blood_group') or 'Not specified'}
- Allergies: {profile.get('allergies') or 'None recorded'}
- Medical Conditions: {profile.get('medical_conditions') or 'None recorded'}
- Current Medications: {profile.get('medications') or 'None recorded'}
- Emergency Contact: {profile.get('emergency_contact') or 'Not specified'} ({profile.get('emergency_phone') or 'N/A'})
- Notes: {profile.get('notes') or 'None'}
"""

    system_prompt = f"""You are a helpful pediatric health assistant for parents and caregivers.
You provide general health information for children aged 3 to 15 years.

IMPORTANT RULES:
- Always consider the child's profile when answering.
- Never diagnose conditions or prescribe medication.
- Encourage consulting a qualified pediatrician for serious concerns.
- Be clear, caring, and easy to understand.
- If asked about emergencies, advise calling emergency services immediately.

{profile_context}"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from AI. Please try again.")
    return content
