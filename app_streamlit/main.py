import streamlit as st
from pages.user_page import users_page
from pages.activite_page import activites_page

st.set_page_config(page_title="Sport App", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = None

st.sidebar.title("Menu")
page = st.sidebar.radio("Navigation", ["Utilisateurs", "Activités"])

if page == "Utilisateurs":
    users_page()
else:
    activites_page()
