from streamlit_cookies_manager import EncryptedCookieManager

from app.core.utils import check_login, redirect_to_login
import streamlit as st
import requests


def job_analyzer_page(cookie_manager: EncryptedCookieManager):
    BACKEND_API_URL = "http://localhost:8080/api/v1"

    st.title("Job Offer Analyzer for Upwork")

    with st.form("upwork_form"):
        username = st.text_input("Upwork Username or Email")
        password = st.text_input("Upwork Password", type="password")
        submitted = st.form_submit_button("Analyze Job Offers")

    if submitted:
        if not username or not password:
            st.error("Please provide both username and password.")
        else:
            credentials = {
                "username": username,
                "password": password,
            }

            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}

            try:
                response = requests.post(
                    f"{BACKEND_API_URL}/actions/analyze-job-offers",
                    json=credentials,
                    headers=headers,
                )
                response.raise_for_status()

                job_analysis = response.json()
                st.write("## Analysis Results")
                for job in job_analysis.get("related_jobs", []):
                    st.write(f"**Title**: {job['title']}")
                    st.write(f"**Description**: {job['description']}")
                    st.write(f"**Posted**: {job['posted_date']}")
                    st.write(f"**Budget**: {job['budget']}")
                    st.write("---")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to analyze job offers: {e}")
