# main.py
import streamlit as st
import sys
from pathlib import Path

from streamlit_cookies_manager import EncryptedCookieManager

# Add the parent directory of 'strm' to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import inner_pages
from app.core.utils import check_login, log_out
import logging
from datetime import datetime

# Logging setup
log_file = Path(__file__).resolve().parent.parent / "frontend.log"
logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Cookies Manager
cookie_manager = EncryptedCookieManager(
    password="12345678",
    prefix=f"unique_key_{st.session_state.get('page_name', 'default')}",
)

# Ensure cookie manager is ready
if not cookie_manager.ready():
    st.stop()

# Define pages
PAGES_FOR_LOGGED_IN = {
    "Home": inner_pages.home_page,
    "Job Analyzer": lambda: inner_pages.job_analyzer_page(
        cookie_manager=cookie_manager
    ),
    "Logout page": lambda: inner_pages.logout_page(cookie_manager=cookie_manager),
}
PAGES_FOR_NOT_LOGGED_IN = {
    "Home": inner_pages.home_page,
    "Login": lambda: inner_pages.login_page(cookie_manager=cookie_manager),
}
is_logged_in = check_login(cookie_manager=cookie_manager)
PAGES = PAGES_FOR_LOGGED_IN if is_logged_in else PAGES_FOR_NOT_LOGGED_IN

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", list(PAGES.keys()), label_visibility="hidden")
st.session_state.current_page = page

PAGES[page]()

# Log current page
logger.info(f"Current page: {st.session_state.current_page}")
