from app.core.utils import check_login, redirect_to_login
import streamlit as st
import requests


def home_page():

    st.title("Home")

    st.write(f"**Title**: ")
    st.write(f"**Description**: ")
    st.write(f"**Posted**: ")
    st.write(f"**Budget**: ")
    st.write("---")
