import streamlit as st
import pandas as pd
import datetime
import plotly.figure_factory as ff
import plotly.express as px
import joblib
import os
from utilities.transform import transfrom
from utilities.variables import (
    OriginCityName,
    DestCityName,
    Marketing_AN,
)

from utilities.plots import (
    flights_dist,
    AVG_Depdelay_per_month_plot,
    DayDist_plot,
    DepDelay_Ariline,
    ArrDelay_Ariline,
    DelayTypesbyAirline,
    DelayTypesbyTimeofDay_plot,
    TopCities_with_highest_Avg_Departure_delay_plot,
    TopCities_with_highest_Avg_TaxiIn_plot,
    TopCities_with_highest_Avg_Arrival_delay_plot,
    TopCities_with_highest_Avg_TaxiOut_plot,
    scatter_Dist_Delay,
    scatter_Dep_Arr,
)

# from streamlit_lottie import st_lottie
import json

"""
Depature Models
"""
base_directory_Dep = "Models/Dep"

DepRf = joblib.load(os.path.join(base_directory_Dep, "RandomForestRegressor"))
DepCb = joblib.load(os.path.join(base_directory_Dep, "CatBoostRegressor"))
DepXb = joblib.load(os.path.join(base_directory_Dep, "XGBRegressor"))


"""
Arrival Models
"""

base_directory_Arr = "Models/Arr"

ArrRf = joblib.load(os.path.join(base_directory_Arr, "RandomForestRegressor"))
ArrCb = joblib.load(os.path.join(base_directory_Arr, "CatBoostRegressor"))
ArrXb = joblib.load(os.path.join(base_directory_Arr, "XGBRegressor"))


def navigation_bar():
    st.markdown(
        """
    <style>
        .navbar {
            display: flex;
            padding: 0.4rem;
            background-color: #333;
            color: white;
            font-size: 18px;
            font-weight: bold;
        }
        .navbar-item {
            margin-right: 1rem;
        }
    </style>
    <div class="navbar">
        <div class="navbar-item">Prediction</div>
        <div class="navbar-item">Insights</div>
        <div class="navbar-item">Analysis</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def pred(arr_input):
    DepDelay = (
        (DepRf.predict(arr_input) * 0.3333)
        + (DepCb.predict(arr_input) * 0.3333)
        + (DepXb.predict(arr_input) * 0.3333)
    )
    ArrDelay = (
        (ArrRf.predict(arr_input) * 0.3333)
        + (ArrCb.predict(arr_input) * 0.3333)
        + (ArrXb.predict(arr_input) * 0.3333)
    )
    return DepDelay[0], ArrDelay[0]


def text_animation(Text):
    st.markdown(
        """
        <style>
        .wrapper {
            place-items: center;
            }

        .animated-text {
            width: 65ch;
            animation: typing 6s steps(65), blink .5s step-end infinite alternate;
            white-space: nowrap;
            overflow: hidden;
            border-right: 3px solid;
            font-family: monospace;
            font-size: 1.3em;
            }

        @keyframes typing {
            from {
                width: 0
            }
        }
                
        @keyframes blink {
            50% {
                border-color: transparent
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="wrapper">
            <div class="animated-text">
                {Text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pred_section(transfrom):
    st.header("Flight Delay Prediction")
    # st_lottie(lottie_load, speed=1, loop=True, quality="low", height=None)
    col1, col2 = st.columns(2)

    with col1:
        FlightDate = st.date_input("FlightDate", datetime.date.today())
        Origin = st.selectbox("OriginCityName:", OriginCityName)
        CRSDepTime = st.time_input("Expected Departure Time", datetime.time(8, 45))
        TaxiOut = st.number_input("Expected TaxiOut in Minutes:")
        WheelsOn = st.time_input("Expected WheelsOn Time", datetime.time(8, 45))
        CRSElapsedTime = st.number_input("Expected Total Flight Time:")

    with col2:
        Marketing_AirN = st.selectbox("Marketing_Airline_Network:", Marketing_AN)
        Destination = st.selectbox("DestCityName:", DestCityName)
        CRSArrTime = st.time_input("Expected Arrival Time:", datetime.time(8, 45))
        TaxiIn = st.number_input("Expected TaxiIn in Minutes:")
        WheelsOff = st.time_input("Expected WheelsOff Time:", datetime.time(8, 45))
        Distance = st.number_input("Distance:")

    if st.button("Predict"):
        input = transfrom(
            FlightDate,
            Origin,
            CRSDepTime,
            TaxiOut,
            WheelsOff,
            CRSElapsedTime,
            Marketing_AirN,
            Destination,
            CRSArrTime,
            TaxiIn,
            WheelsOn,
            Distance,
        )
        DepDelay, ArrDelay = pred(input)

        DepDelayMinutes = (f"{DepDelay:.2f}").split(".")[0]
        DepDelaySec = (f"{DepDelay:.2f}").split(".")[1]
        ArrDelayMinutes = (f"{ArrDelay:.2f}").split(".")[0]
        ArrDelaySec = (f"{ArrDelay:.2f}").split(".")[1]

        out1 = f"The Predicted Departure Delay is {DepDelayMinutes} Minutes and {DepDelaySec} seconds."
        out2 = f"The Predicted Arrival Delay is {ArrDelayMinutes} Minutes and {ArrDelaySec} seconds."
        text_animation(out1)
        text_animation(out2)


def insights_section():
    st.header("Flight Delays Analysis")
    st.write("")
    base_path = "data"
    df = pd.read_parquet(os.path.join(base_path, "analysis_data.parquet"))

    """
    Weekly Flights: How each no. of flights get SCHEDULED for week and in sigle day
    """
    st.markdown("### 1. Weekly Flights:")
    st.plotly_chart(flights_dist, use_container_width=True)

    """
    Flight Delays by months
    """
    st.markdown("### 2. Flight Delays by Month:")
    st.plotly_chart(AVG_Depdelay_per_month_plot, use_container_width=True)

    """
    Flight Delays by Daytime
    """
    st.markdown("### 3. Flight Delays by Daytime:")
    st.plotly_chart(DayDist_plot, use_container_width=True)

    """
    Average Departure Delay by Airline
    """
    st.markdown("### 4. Average Departure Delay by Airline:")
    st.plotly_chart(DepDelay_Ariline, use_container_width=True)

    """
    Average Arrival Delay by Airline
    """
    st.markdown("### 5. Average Arrival Delay by Airline:")
    st.plotly_chart(ArrDelay_Ariline, use_container_width=True)

    """
    Stack Bar Plot - Delay Types by Airline
    """
    st.markdown("###  6. Delay Types by Airline:")
    st.plotly_chart(DelayTypesbyAirline, use_container_width=True)

    """
    line Plot - Delay Types by Time of Day
    """
    st.markdown("###  7. Delay Types by Time of Day:")
    st.plotly_chart(DelayTypesbyTimeofDay_plot, use_container_width=True)

    """
    Top 10 Cities with Highest Average Departure Delay
    """
    st.markdown("### 8. Top 10 Cities with Highest Average Departure Delay:")
    st.plotly_chart(
        TopCities_with_highest_Avg_Departure_delay_plot, use_container_width=True
    )

    """
    Top 10 Cites with Highets Average TaxiIn(minutes) time
    """
    st.markdown("### 9. Top 10 Cites with Highets Average TaxiIn(minutes) time:")
    st.plotly_chart(TopCities_with_highest_Avg_TaxiIn_plot, use_container_width=True)

    """
    Top 10 Cities with Highest Average Arrival Delay
    """
    st.markdown("### 10. Top 10 Cities with Highest Average Arrival Delay:")
    st.plotly_chart(
        TopCities_with_highest_Avg_Arrival_delay_plot, use_container_width=True
    )

    """
    Top 10 Cites with Highets Average TaxiOut(minutes) time
    """
    st.markdown("### 11. Top 10 Cites with Highets Average TaxiOut(minutes) time:")
    st.plotly_chart(TopCities_with_highest_Avg_TaxiOut_plot, use_container_width=True)

    """
    Scatter Plot - Delay vs. Distance
    """
    st.markdown("###  12. Scatter Plot - Delay vs. Distance:")
    st.plotly_chart(scatter_Dist_Delay, use_container_width=True)

    """
    Scatter Plot - Departure Delay vs. Arrival Delay
    """
    st.markdown("###  13. Scatter Plot - Departure Delay vs. Arrival Delay:")
    st.plotly_chart(scatter_Dep_Arr, use_container_width=True)
