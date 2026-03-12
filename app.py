import streamlit as st
from views.predict_view import show_predict_page
from views.history_view import show_history_page
from views.dashboard_view import show_dashboard_page
from models.db import DatabaseConnection


st.set_page_config(
    page_title="Bank Churn Prediction System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def initialize_database():
    """Initialize database and tables on app startup"""
    db = DatabaseConnection()
    db.create_database()
    db.create_table()
    return db


try:
    initialize_database()
except Exception as e:
    st.warning(f"Database initialization warning: {e}")


st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title(" Bank Churn System")
st.sidebar.markdown("---")


page = st.sidebar.radio(
    "Navigation",
    [" Dashboard", " Predict Churn", " Prediction History"],
    key="nav_radio"
)

st.sidebar.markdown("---")


if page == " Dashboard":
    show_dashboard_page()
elif page == " Predict Churn":
    show_predict_page()
elif page == " Prediction History":
    show_history_page()