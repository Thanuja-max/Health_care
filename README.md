# KidsCare — Pediatric Health Profiles

A simple Streamlit app to build and manage medical profiles for children aged **3 to 15 years**. Uses a local SQLite database and Groq AI for a health assistant.

## Features

- Create, view, edit, and delete child health profiles
- Store allergies, conditions, medications, and emergency contacts
- AI Health Assistant powered by Groq (uses profile context)
- ChatGPT-inspired clean UI

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**

   Create a `.env` file in the project root:

   ```
   groq_api_key=your_groq_api_key_here
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

## Project Structure

```
Health_care/
├── app.py           # Streamlit UI
├── database.py      # SQLite CRUD operations
├── groq_client.py   # Groq AI integration
├── data/
│   └── profiles.db  # Local database (auto-created)
├── requirements.txt
└── .env             # Your Groq API key (not committed)
```

## Profile Fields

| Field | Description |
|---|---|
| Name | Child's full name |
| Age | 3–15 years |
| Gender | Male / Female / Other |
| Blood Group | A+, B-, etc. |
| Allergies | Known allergies |
| Medical Conditions | Existing conditions |
| Medications | Current medications |
| Emergency Contact | Contact person name |
| Emergency Phone | Contact phone number |
| Notes | Additional health notes |

## Disclaimer

This app is for profile management and general health information only. It is **not** a substitute for professional medical advice. Always consult a qualified pediatrician for medical decisions.
