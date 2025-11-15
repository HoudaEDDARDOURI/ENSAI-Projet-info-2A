import streamlit as st
from pages.user_page import users_page
from pages.activite_page import activites_page
from pages.statistique_page import statistiques_page
from pages.feed_page import feed_page
from pages.parcours_page import parcours_page


st.set_page_config(page_title="Sport App", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = None

st.sidebar.title("Menu")
page = st.sidebar.radio("Navigation", ["Utilisateurs", "Activités", "Statistiques","Parcours"])

if page == "Utilisateurs":
    users_page()
elif page == "Statistiques":
    statistiques_page()
elif page == "Activités":
    activites_page()
elif page == "Parcours": 
    parcours_page()
else:
    feed_page()
