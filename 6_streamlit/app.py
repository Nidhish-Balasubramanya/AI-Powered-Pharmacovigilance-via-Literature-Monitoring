import streamlit as st
import requests
import json
import os

st.set_option('server.maxUploadSize', 20)  # limit to 20 MB

API_URL = os.environ.get("API_URL", "http://localhost:8000")


st.set_page_config(page_title="AI-Powered Pharmacovigilance", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar Navigation ---
st.sidebar.title("AI-Powered Pharmacovigilance")
module = st.sidebar.selectbox(
    "Go to",
    [
        "Home",
        "📤 Case Upload & Extraction",
        "📝 Narrative by Case ID",
        "💬 Feedback",
        "📂 Retrieve Case JSON"
    ]
)

# --- Home Page ---
if module == "Home":
    st.title("AI-Powered Pharmacovigilance")
    st.markdown("""
    Welcome to the AI-Powered Pharmacovigilance system.

    This web application automates the extraction and analysis of Adverse Event Reports (AER) from pharmaceutical literature using advanced AI and NLP.

    **Features:**
    - Upload pharma documents and extract structured case data
    - Generate regulatory-ready case narratives
    - Retrieve or download case information by ID
    - Submit feedback on any case or narrative

    Use the sidebar to navigate between modules.
    """)
    
# --- Module 1: Case Upload & Extraction ---
elif module == "📤 Case Upload & Extraction":
    st.title("📤 Case Upload & Extraction")
    uploaded_file = st.file_uploader("Upload document (PDF/Image/TXT)", type=["pdf", "png", "jpg", "jpeg", "txt"])
    if 'case_id' not in st.session_state:
        st.session_state.case_id = None
    if 'case_json' not in st.session_state:
        st.session_state.case_json = None
    if 'narrative' not in st.session_state:
        st.session_state.narrative = None

    if st.button("Process Case") and uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            response = requests.post(f"{API_URL}/upload", files=files)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Case processed successfully!")
                st.session_state.case_id = result["case_id"]
                st.session_state.case_json = result["case_json"]
                st.session_state.narrative = None
            else:
                st.error(f"❌ Error: {response.json()['detail']}")
                st.session_state.case_id = None
                st.session_state.case_json = None
                st.session_state.narrative = None
        except Exception as e:
            st.error(f"🚨 Connection error: {str(e)}")
            st.session_state.case_id = None
            st.session_state.case_json = None
            st.session_state.narrative = None
    if st.session_state.case_id:
        st.info(f"Case ID: `{st.session_state.case_id}`")
    if st.session_state.case_json:
        with st.expander("View Extracted JSON", expanded=True):
            st.json(st.session_state.case_json)
        st.download_button(
            label="Download Case JSON",
            data=json.dumps(st.session_state.case_json, indent=2),
            file_name=f"case_{st.session_state.case_id}.json",
            mime="application/json",
            key="download_json"
        )

    if st.session_state.case_id:
        if st.button("Generate Narrative"):
            try:
                response = requests.post(
                    f"{API_URL}/narrative",
                    params={"case_id": st.session_state.case_id}
                )
                if response.status_code == 200:
                    narrative = response.json()["narrative"]
                    # Remove preamble if present
                    lines = narrative.strip().split('\n')
                    if lines and ("draft" in lines[0].lower() or "narrative" in lines[0].lower()):
                        lines = lines[1:]
                    narrative = "\n".join(lines).strip()
                    st.session_state.narrative = narrative
                else:
                    st.error(f"❌ Narrative error: {response.json()['detail']}")
                    st.session_state.narrative = None
            except Exception as e:
                st.error(f"🚨 Connection error: {str(e)}")
                st.session_state.narrative = None

    if st.session_state.narrative:
        st.subheader("AI-Generated Narrative")
        for para in st.session_state.narrative.split('\n\n'):
            st.markdown(para)
        st.download_button(
            label="Download Narrative",
            data=st.session_state.narrative,
            file_name=f"narrative_{st.session_state.case_id}.txt",
            mime="text/plain",
            key="download_narrative"
        )

# --- Module 2: Narrative by Case ID ---
elif module == "📝 Narrative by Case ID":
    st.title("📝 Generate Narrative by Case ID")
    narrative_case_id = st.text_input("Enter Case ID for narrative generation:")
    if st.button("Get Narrative"):
        if narrative_case_id:
            try:
                response = requests.post(
                    f"{API_URL}/narrative",
                    params={"case_id": narrative_case_id}
                )
                if response.status_code == 200:
                    narrative = response.json()["narrative"]
                    # Remove preamble if present
                    lines = narrative.strip().split('\n')
                    if lines and ("draft" in lines[0].lower() or "narrative" in lines[0].lower()):
                        lines = lines[1:]
                    narrative = "\n".join(lines).strip()
                    st.session_state.narrative_by_id = narrative
                    st.success("Narrative generated!")
                else:
                    st.error(f"❌ Narrative error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"🚨 Connection error: {str(e)}")
        else:
            st.warning("Please enter a valid Case ID.")

    if st.session_state.get("narrative_by_id"):
        st.subheader("Narrative")
        for para in st.session_state.narrative_by_id.split('\n\n'):
            st.markdown(para)
        st.download_button(
            label="Download Narrative",
            data=st.session_state.narrative_by_id,
            file_name=f"narrative_{narrative_case_id}.txt",
            mime="text/plain",
            key="download_narrative_by_id"
        )

# --- Module 3: Feedback ---
elif module == "💬 Feedback":
    st.title("💬 Submit Feedback")
    feedback_case_id = st.text_input("Enter Case ID for feedback:")
    feedback_text = st.text_area("Your feedback on this case/narrative:")
    if st.button("Submit Feedback"):
        if feedback_case_id and feedback_text.strip():
            try:
                response = requests.post(
                    f"{API_URL}/validate",
                    data={"case_id": feedback_case_id, "feedback": feedback_text}
                )
                # Accept any response as success for feedback
                st.success("Thank you for your feedback!")
            except Exception as e:
                st.error(f"🚨 Connection error: {str(e)}")
        else:
            st.warning("Enter both Case ID and feedback.")

# --- Module 4: Retrieve Case JSON ---
elif module == "📂 Retrieve Case JSON":
    st.title("📂 Retrieve Case JSON by ID")
    get_case_id = st.text_input("Enter Case ID to fetch JSON:")
    if st.button("Get Case JSON"):
        if get_case_id:
            try:
                response = requests.get(f"{API_URL}/case/{get_case_id}")
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.retrieved_case_json = result
                    st.success("Case loaded!")
                    with st.expander("View Extracted JSON", expanded=True):
                        st.json(result)
                    st.download_button(
                        label="Download Case JSON",
                        data=json.dumps(result, indent=2),
                        file_name=f"case_{get_case_id}.json",
                        mime="application/json",
                        key="download_json_by_id"
                    )
                else:
                    st.error(f"❌ Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"🚨 Connection error: {str(e)}")
        else:
            st.warning("Please enter a valid Case ID.")

st.markdown("---")
st.caption("Powered by Streamlit & FastAPI | All rights reserved.")
