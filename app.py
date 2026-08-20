import streamlit as st
import database as db
from groq_client import ask_health_assistant

st.set_page_config(
    page_title="KidsCare Profiles",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .block-container { padding-top: 2rem; max-width: 900px; }
    [data-testid="stSidebar"] { background-color: #202123; }
    [data-testid="stSidebar"] * { color: #ececf1 !important; }
    h1, h2, h3 { color: #202123 !important; font-weight: 600 !important; }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background-color: #10a37f !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: #0d8c6d !important;
    }
    .stButton > button { border-radius: 8px !important; border: 1px solid #d9d9e3 !important; }
    .profile-card {
        background: #f7f7f8;
        border: 1px solid #ececf1;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }
    .profile-card h4 { margin: 0 0 0.3rem 0; color: #202123; font-size: 1.05rem; }
    .profile-card p { margin: 0; color: #6e6e80; font-size: 0.875rem; }
    .badge {
        display: inline-block;
        background: #10a37f;
        color: white;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
    }
    .chat-user {
        background: #f7f7f8;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin: 0.5rem 0;
        border: 1px solid #ececf1;
    }
    .chat-assistant {
        background: #ffffff;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin: 0.5rem 0;
        border: 1px solid #ececf1;
    }
    .chat-label { font-size: 0.75rem; font-weight: 600; color: #10a37f; margin-bottom: 0.3rem; }
    .chat-label-user { color: #202123; }
    .info-box {
        background: #f0faf7;
        border-left: 4px solid #10a37f;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        color: #202123;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

db.init_db()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_profile_id" not in st.session_state:
    st.session_state.selected_profile_id = None
if "edit_profile_id" not in st.session_state:
    st.session_state.edit_profile_id = None


def profile_form(defaults=None, key_prefix="new"):
    defaults = defaults or {}
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *", value=defaults.get("name", ""), key=f"{key_prefix}_name")
        age = st.number_input(
            "Age (3–15) *", min_value=3, max_value=15,
            value=defaults.get("age", 5), key=f"{key_prefix}_age"
        )
        gender = st.selectbox(
            "Gender *", ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(defaults.get("gender", "Male")),
            key=f"{key_prefix}_gender"
        )
        blood_options = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        blood_group = st.selectbox(
            "Blood Group", blood_options,
            index=blood_options.index(defaults.get("blood_group", "")) if defaults.get("blood_group", "") in blood_options else 0,
            key=f"{key_prefix}_blood"
        )
    with col2:
        emergency_contact = st.text_input(
            "Emergency Contact Name", value=defaults.get("emergency_contact", ""),
            key=f"{key_prefix}_ec_name"
        )
        emergency_phone = st.text_input(
            "Emergency Phone", value=defaults.get("emergency_phone", ""),
            key=f"{key_prefix}_ec_phone"
        )

    allergies = st.text_area("Allergies", value=defaults.get("allergies", ""), key=f"{key_prefix}_allergies")
    medical_conditions = st.text_area("Medical Conditions", value=defaults.get("medical_conditions", ""), key=f"{key_prefix}_conditions")
    medications = st.text_area("Current Medications", value=defaults.get("medications", ""), key=f"{key_prefix}_meds")
    notes = st.text_area("Additional Notes", value=defaults.get("notes", ""), key=f"{key_prefix}_notes")

    return {
        "name": name.strip(),
        "age": int(age),
        "gender": gender,
        "blood_group": blood_group,
        "allergies": allergies.strip(),
        "medical_conditions": medical_conditions.strip(),
        "medications": medications.strip(),
        "emergency_contact": emergency_contact.strip(),
        "emergency_phone": emergency_phone.strip(),
        "notes": notes.strip(),
    }


def render_profile_card(profile):
    blood = f'<span class="badge">{profile["blood_group"]}</span>' if profile.get("blood_group") else ""
    st.markdown(f"""
    <div class="profile-card">
        <h4>{profile['name']} {blood}</h4>
        <p>Age {profile['age']} · {profile['gender']} · Updated {profile['updated_at'][:10]}</p>
    </div>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 🩺 KidsCare")
    st.markdown("*Pediatric Health Profiles*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📋 All Profiles", "➕ New Profile", "💬 Health Assistant"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("For children aged 3–15 yrs. Not a substitute for professional medical advice.")


if page == "📋 All Profiles":
    st.title("Child Health Profiles")
    st.markdown('<div class="info-box">Manage medical profiles for children aged 3 to 15 years.</div>', unsafe_allow_html=True)

    profiles = db.get_all_profiles()
    if not profiles:
        st.info("No profiles yet. Go to **New Profile** to create one.")
    else:
        for profile in profiles:
            render_profile_card(profile)
            col1, col2, _ = st.columns([1, 1, 4])
            with col1:
                if st.button("View", key=f"view_{profile['id']}"):
                    st.session_state.selected_profile_id = profile["id"]
                    st.session_state.edit_profile_id = None
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"del_{profile['id']}"):
                    db.delete_profile(profile["id"])
                    if st.session_state.selected_profile_id == profile["id"]:
                        st.session_state.selected_profile_id = None
                    st.rerun()

        if st.session_state.selected_profile_id:
            st.markdown("---")
            profile = db.get_profile(st.session_state.selected_profile_id)
            if profile:
                if st.session_state.edit_profile_id == profile["id"]:
                    st.subheader(f"Edit — {profile['name']}")
                    data = profile_form(defaults=profile, key_prefix=f"edit_{profile['id']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save Changes", type="primary"):
                            if not data["name"]:
                                st.error("Name is required.")
                            else:
                                db.update_profile(profile["id"], data)
                                st.session_state.edit_profile_id = None
                                st.success("Profile updated!")
                                st.rerun()
                    with col2:
                        if st.button("Cancel"):
                            st.session_state.edit_profile_id = None
                            st.rerun()
                else:
                    st.subheader(profile["name"])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Age:** {profile['age']} years")
                        st.markdown(f"**Gender:** {profile['gender']}")
                        st.markdown(f"**Blood Group:** {profile.get('blood_group') or '—'}")
                        st.markdown(f"**Allergies:** {profile.get('allergies') or 'None'}")
                        st.markdown(f"**Conditions:** {profile.get('medical_conditions') or 'None'}")
                    with col2:
                        st.markdown(f"**Medications:** {profile.get('medications') or 'None'}")
                        st.markdown(f"**Emergency Contact:** {profile.get('emergency_contact') or '—'}")
                        st.markdown(f"**Emergency Phone:** {profile.get('emergency_phone') or '—'}")
                        st.markdown(f"**Notes:** {profile.get('notes') or '—'}")
                    if st.button("Edit Profile", type="primary"):
                        st.session_state.edit_profile_id = profile["id"]
                        st.rerun()

elif page == "➕ New Profile":
    st.title("Create New Profile")
    st.markdown('<div class="info-box">Fill in the health details for a child (age 3–15).</div>', unsafe_allow_html=True)
    data = profile_form(key_prefix="new")
    if st.button("Save Profile", type="primary"):
        if not data["name"]:
            st.error("Please enter the child's name.")
        else:
            profile_id = db.create_profile(data)
            st.success(f"Profile for **{data['name']}** saved successfully!")
            st.session_state.selected_profile_id = profile_id
            st.balloons()

else:
    st.title("Health Assistant")
    st.markdown(
        '<div class="info-box">Ask general health questions. The AI uses the selected child\'s profile for context. '
        'Always consult a doctor for medical decisions.</div>',
        unsafe_allow_html=True,
    )

    profiles = db.get_all_profiles()
    if not profiles:
        st.warning("Create a child profile first before using the assistant.")
    else:
        profile_options = {p["id"]: p["name"] for p in profiles}
        default_id = st.session_state.selected_profile_id or list(profile_options.keys())[0]
        selected_id = st.selectbox(
            "Select Child Profile",
            options=list(profile_options.keys()),
            format_func=lambda x: profile_options[x],
            index=list(profile_options.keys()).index(default_id) if default_id in profile_options else 0,
        )
        st.session_state.selected_profile_id = selected_id
        profile = db.get_profile(selected_id)

        st.markdown(f"**Chatting about:** {profile['name']} (Age {profile['age']})")
        st.markdown("---")

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-user"><div class="chat-label chat-label-user">You</div>{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="chat-assistant"><div class="chat-label">KidsCare AI</div>{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

        user_input = st.chat_input("Ask a health question about this child...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                try:
                    response = ask_health_assistant(profile, user_input, st.session_state.chat_history[:-1])
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Sorry, I couldn't process that. Error: {e}",
                    })
            st.rerun()

        if st.session_state.chat_history and st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
