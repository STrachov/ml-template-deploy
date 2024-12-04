import streamlit as st
from app.core.utils import log_out


def logout_page(cookie_manager):

    st.write("Are you sure you want to log out?")

    if st.button("Log out"):
        log_out(cookie_manager)
