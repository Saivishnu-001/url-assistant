import json
import streamlit as st
from rapidfuzz import fuzz

# ✅ Load JSON
with open("apps.json", "r") as f:
    apps = json.load(f)

# ✅ Matching Logic
def find_matches(user_input):
    user_input = user_input.lower().strip()
    matches = []

    for app_data in apps:
        best_score = 0

        for keyword in app_data["keywords"]:
            score = fuzz.token_set_ratio(user_input, keyword.lower())
            best_score = max(best_score, score)

        if best_score > 60:
            matches.append((app_data, best_score))

    return sorted(matches, key=lambda x: x[1], reverse=True)

# ✅ Session State Initialization
if "matches" not in st.session_state:
    st.session_state.matches = []

if "selected_app" not in st.session_state:
    st.session_state.selected_app = None

# ✅ Page UI
st.set_page_config(page_title="Company URL Assistant", page_icon="🔎")
st.title("🔎 Company URL Assistant")

# ✅ Reset Button
if st.session_state.selected_app:
    if st.button("🔄 New Search"):
        st.session_state.selected_app = None
        st.session_state.matches = []
        st.rerun()

# ✅ Input Handling
query = st.chat_input("Search application...")

if query:
    st.session_state.matches = find_matches(query)
    st.session_state.selected_app = None

# ✅ Multiple Matches UI
if st.session_state.matches:

    if len(st.session_state.matches) == 1:
        st.session_state.selected_app = st.session_state.matches[0][0]

    else:
        st.write("🤔 Multiple matches found. Please select:")

        for i, (app_data, score) in enumerate(st.session_state.matches):

            if st.button(
                f"{app_data['name']} ({score}%)",
                key=f"match_{i}"
            ):
                st.session_state.selected_app = app_data

# ✅ ALWAYS Render Selected App 🎯
if st.session_state.selected_app:

    app_data = st.session_state.selected_app

    st.write("═══════════════════════")
    st.write(f"🔗 **{app_data['name']}**")
    st.write(f"🌐 {app_data['url']}")
    st.write(f"🔑 Login: {app_data.get('Login', 'Not Specified')}")
    st.write(f"🔐 VPN Required: {app_data.get('VPN Required', 'NO')}")
    st.write("═══════════════════════")

    st.link_button("🌐 Open Application", app_data["url"])
