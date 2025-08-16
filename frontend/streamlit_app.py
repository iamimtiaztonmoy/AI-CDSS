"""
Streamlit frontend for the comprehensive CDSS.

This app provides two modes of interaction:

1. **Structured Recommendation** – Users enter patient demographics and a list of symptoms.  The app calls the backend `/recommendation` endpoint and displays a guideline snippet along with an explanation.
2. **Chat** – Users can ask free‑form questions about the guidelines.  Messages persist across interactions using `st.session_state` so the conversation history is visible.  Each user query is sent to the backend `/chat` endpoint and the retrieved snippet is returned as the assistant's reply.

To run the app locally without Docker, ensure that the backend is accessible at `http://localhost:8000` or adjust the `BACKEND_URL` constant below.
"""

import requests
import streamlit as st

# Configure backend URL.  When using docker-compose the hostname is `backend`.  If
# running manually, change this to "http://localhost:8000".
BACKEND_URL = "http://backend:8000"

st.set_page_config(page_title="Comprehensive Clinical Decision Support")
st.title("Comprehensive AI Clinical Decision Support System")

# Sidebar selection for mode
mode = st.sidebar.selectbox(
    "Select Mode",
    ["Structured Recommendation", "Chat about Guidelines"],
)


def call_recommendation_api(payload: dict) -> dict:
    resp = requests.post(f"{BACKEND_URL}/recommendation", json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()


def call_chat_api(query: str) -> str:
    resp = requests.post(f"{BACKEND_URL}/chat", json={"query": query}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return data.get("answer", "")


def structured_recommendation_view() -> None:
    """
    Render the structured recommendation form and handle submission.
    """
    st.header("Get a Guideline Recommendation")
    with st.form("patient_form"):
        patient_id = st.text_input("Patient ID", value="anon")
        age = st.number_input("Age", min_value=0, max_value=120, value=50, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        symptoms_input = st.text_area(
            "Symptoms (comma‑separated)",
            placeholder="shortness of breath, fatigue, swelling",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            symptoms = [s.strip() for s in symptoms_input.split(",") if s.strip()]
            if not symptoms:
                st.error("Please enter at least one symptom.")
            else:
                payload = {
                    "patient_id": patient_id,
                    "age": int(age),
                    "gender": gender,
                    "symptoms": symptoms,
                }
                with st.spinner("Retrieving recommendation..."):
                    try:
                        data = call_recommendation_api(payload)
                        st.subheader("Guideline Recommendation")
                        st.write(data["snippet"])
                        st.markdown(f"**Explanation:** {data['explanation']}")
                    except Exception as e:
                        st.error(f"Error retrieving recommendation: {e}")


def chat_view() -> None:
    """
    Render the chat interface and handle user messages.
    """
    st.header("Ask Questions about the Guideline")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []  # type: ignore
    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    # Chat input
    prompt = st.chat_input("Ask a question…")
    if prompt:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})  # type: ignore
        # Call backend
        with st.spinner("Retrieving answer..."):
            try:
                answer = call_chat_api(prompt)
            except Exception as e:
                answer = f"Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": answer})  # type: ignore
        # Rerender to show the new messages
        st.experimental_rerun()


# Render the selected mode
if mode == "Structured Recommendation":
    structured_recommendation_view()
else:
    chat_view()
