import os

from dotenv import load_dotenv


import streamlit as st
import requests
from sqlalchemy.orm.sync import update
from streamlit_cookies_manager import CookieManager

import logging


logger = logging.getLogger(__name__)
load_dotenv(override=True)


def login_page(cookie_manager: CookieManager):
    BACKEND_HOST = os.getenv("BACKEND_HOST")
    BACKEND_PORT = os.getenv("BACKEND_PORT")
    LOGIN_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/login/access-token"

    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        login_data = {
            "username": email,
            "password": password,
        }

        try:
            response = requests.post(LOGIN_URL, data=login_data)
            response.raise_for_status()
            token_data = response.json()
            access_token = token_data["access_token"]

            # Store token and login state
            st.session_state["access_token"] = access_token
            st.session_state["is_logged_in"] = True
            cookie_manager["access_token"] = access_token

            st.success("Login successful!")
            st.rerun()

        except requests.exceptions.RequestException as e:
            st.error("Login failed. Please check your credentials.")
            st.session_state["is_logged_in"] = False

    if "is_logged_in" in st.session_state and st.session_state["is_logged_in"]:
        st.query_params.page = "job_analyzer"
    else:
        st.session_state["is_logged_in"] = False
