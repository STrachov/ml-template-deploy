import requests
import streamlit as st
import logging
from datetime import datetime, timezone
from streamlit_cookies_manager import EncryptedCookieManager
import jwt

logger = logging.getLogger(__name__)


def is_token_valid():
    TEST_TOKEN_URL = "http://localhost:8080/api/v1/login/test-token"
    token = st.session_state.get("access_token")

    if not token:
        return False

    try:
        response = requests.post(
            TEST_TOKEN_URL, headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def check_login(cookie_manager: EncryptedCookieManager):

    if not cookie_manager.ready():
        st.stop()

    # Check if the user is logged in
    if "access_token" in cookie_manager and len(cookie_manager["access_token"]) > 1:
        if test_token(cookie_manager["access_token"]):
            return True  # User is already logged in
        else:
            cookie_manager["access_token"] = ""  # Token has expired - clear cookies
            return False
    else:
        return False


def redirect_to_login():
    st.warning("Session expired or not logged in. Please log in again.")
    st.session_state.clear()
    st.rerun()


def log_out(cookie_manager: EncryptedCookieManager):
    if not cookie_manager.ready():
        st.warning("Session cookie manager not ready.")
        st.stop()

    logger.info(f"logout: access_token before logout: {cookie_manager['access_token']}")

    # Delete cookies
    cookie_manager["access_token"] = ""
    # cookie_manager.save()

    logger.info(
        f"logout: access_token after logout: {cookie_manager.get('access_token', 'deleted')}"
    )

    # Rerun the app to reflect the changes
    st.rerun()


def test_token(token: str):

    payload = jwt.decode(token, options={"verify_signature": False})
    expiration_time = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
    logger.info(f"test_token expiration_time: {expiration_time}")
    current_time = datetime.now(timezone.utc)
    logger.info(f"test_token current_time: {current_time}")
    return expiration_time > current_time
