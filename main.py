import streamlit as st
import pandas as pd
from utilities.transform import transfrom
from utilities.helpers import pred_section, insights_section
from streamlit_lottie import st_lottie
import os
import json
import time

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
base_directory = "animation"
path = os.path.join(base_directory, "animation1.json")
with open(path, "r") as file:
    animation = json.load(file)

with st.sidebar:
    st_lottie(
        animation,
        reverse=True,
        height=100,
        width=200,
        speed=1,
        loop=True,
        quality="high",
        key="flight",
    )
    st.markdown("# Navigation")
    selected_section = st.radio(
        "Navigate:", ("Prediction", "Insights"), label_visibility="hidden"
    )

if selected_section == "Prediction":
    pred_section(transfrom)
elif selected_section == "Insights":
    insights_section()
