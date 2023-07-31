import streamlit as st
import pandas as pd
from utilities.transform import transfrom
from utilities.helpers import pred_section, insights_section

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("# Navigation")
    selected_section = st.radio(
        "Navigate:", ("Prediction", "Insights"), label_visibility="hidden"
    )

if selected_section == "Prediction":
    pred_section(transfrom)
elif selected_section == "Insights":
    insights_section()
