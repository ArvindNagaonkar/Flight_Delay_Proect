import pandas as pd
import plotly.express as px
import os

base_path = "data"
df = pd.read_parquet(os.path.join(base_path, "analysis_data.parquet"))

"""
Weekly Flights: How each no. of flights get SCHEDULED for week and in sigle day
"""

flights = (
    pd.DataFrame(
        df[["DayofWeek", "CRSArrTimeHourDis", "ArrDelay"]]
        .groupby(["DayofWeek", "CRSArrTimeHourDis"])["ArrDelay"]
        .median()
    )
    .rename({"ArrDelay": "counts"}, axis=1)
    .reset_index()
)

flights_dist = px.histogram(
    flights,
    x="DayofWeek",
    y="counts",
    color="CRSArrTimeHourDis",
    barmode="group",
    height=400,
)

"""
Flight Delays by months
"""
AVG_Depdelay_per_month = pd.DataFrame(
    df[["DepDelayMinutes", "Month"]].groupby("Month")["DepDelayMinutes"].mean()
).reset_index()

AVG_Depdelay_per_month_plot = px.bar(
    AVG_Depdelay_per_month,
    x="Month",
    y="DepDelayMinutes",
    labels={"DepDelay": "Departure Delay (Minutes)"},
    height=400,
)

"""
Flight Delays by Daytime
"""
DayDist = pd.DataFrame(
    df[["CRSDepTimeHourDis", "DepDelay"]]
    .groupby("CRSDepTimeHourDis")["DepDelay"]
    .mean()
).reset_index()

DayDist_plot = px.bar(
    DayDist,
    x="CRSDepTimeHourDis",
    y="DepDelay",
    labels={"DepDelay": "Departure Delay (Minutes)"},
    height=400,
)

"""
Average Departure Delay by Airline
"""
Ariline_delays = (
    df[["Marketing_Airline_Network", "DepDelay", "ArrDelay"]]
    .groupby("Marketing_Airline_Network")[["DepDelay", "ArrDelay"]]
    .mean()
    .reset_index()
)
DepDelay_Ariline = px.bar(
    Ariline_delays,
    x="Marketing_Airline_Network",
    y="DepDelay",
    color="DepDelay",
    labels={"DepDelay": "Departure Delay (Minutes)"},
    height=400,
)

"""
Average Arrival Delay by Airline
"""
ArrDelay_Ariline = px.bar(
    Ariline_delays,
    x="Marketing_Airline_Network",
    y="ArrDelay",
    color="ArrDelay",
    labels={"ArrDelay": "Arrival Delay (Minutes)"},
    height=400,
)

"""
Stack Bar Plot - Delay Types by Airline
"""
Rdelays = (
    df[
        [
            "Marketing_Airline_Network",
            "CarrierDelay",
            "WeatherDelay",
            "NASDelay",
            "SecurityDelay",
            "LateAircraftDelay",
        ]
    ]
    .groupby("Marketing_Airline_Network")[
        [
            "CarrierDelay",
            "WeatherDelay",
            "NASDelay",
            "SecurityDelay",
            "LateAircraftDelay",
        ]
    ]
    .mean()
    .reset_index()
)

DelayTypesbyAirline = px.bar(
    Rdelays,
    x="Marketing_Airline_Network",
    y=[
        "CarrierDelay",
        "WeatherDelay",
        "NASDelay",
        "SecurityDelay",
        "LateAircraftDelay",
    ],
    labels={"value": "Delay (Minutes)"},
)

"""
line Plot - Delay Types by Time of Day
"""
DelayTypesbyTimeofDay = (
    df[
        [
            "CRSArrTimeHourDis",
            "CarrierDelay",
            "WeatherDelay",
            "NASDelay",
            "SecurityDelay",
            "LateAircraftDelay",
        ]
    ]
    .groupby("CRSArrTimeHourDis")[
        [
            "CarrierDelay",
            "WeatherDelay",
            "NASDelay",
            "SecurityDelay",
            "LateAircraftDelay",
        ]
    ]
    .mean()
    .reset_index()
)

DelayTypesbyTimeofDay_plot = px.line(
    DelayTypesbyTimeofDay,
    x="CRSArrTimeHourDis",
    y=[
        "CarrierDelay",
        "WeatherDelay",
        "NASDelay",
        "SecurityDelay",
        "LateAircraftDelay",
    ],
    markers=True,
    labels={"value": "Delay (Minutes)"},
)


"""
Top 10 Cities with Highest Average Departure Delay
"""
TopCities_with_highest_Avg_Departure_delay = (
    pd.DataFrame(
        df[["OriginCityName", "DepDelayMinutes"]]
        .groupby("OriginCityName")["DepDelayMinutes"]
        .mean()
    )
    .reset_index()
    .sort_values("DepDelayMinutes")
    .head(10)
)
TopCities_with_highest_Avg_Departure_delay_plot = px.bar(
    TopCities_with_highest_Avg_Departure_delay,
    x="DepDelayMinutes",
    y="OriginCityName",
    labels={"DepDelay": "Departure Delay (Minutes)"},
    # orientation="h",
    height=400,
)

"""
Top 10 Cites with Highets Average TaxiIn(minutes) time
"""
TopCities_with_highest_Avg_TaxiIn = (
    pd.DataFrame(
        df[["DestCityName", "TaxiIn"]].groupby("DestCityName")["TaxiIn"].mean()
    )
    .reset_index()
    .sort_values("TaxiIn")
    .head(10)
)

TopCities_with_highest_Avg_TaxiIn_plot = px.bar(
    TopCities_with_highest_Avg_TaxiIn,
    x="TaxiIn",
    y="DestCityName",
    labels={"TaxiIn": "TaxiIn (Minutes)"},
    # orientation="h",
    height=400,
)

"""
Top 10 Cities with Highest Average Arrival Delay
"""
TopCities_with_highest_Avg_Arrival_delay = (
    pd.DataFrame(
        df[["DestCityName", "ArrDelayMinutes"]]
        .groupby("DestCityName")["ArrDelayMinutes"]
        .mean()
    )
    .reset_index()
    .sort_values("ArrDelayMinutes")
    .head(10)
)
TopCities_with_highest_Avg_Arrival_delay_plot = px.bar(
    TopCities_with_highest_Avg_Arrival_delay,
    x="ArrDelayMinutes",
    y="DestCityName",
    labels={"DepDelay": "Departure Delay (Minutes)"},
    # orientation="h",
    height=400,
)

"""
Top 10 Cites with Highets Average TaxiOut(minutes) time
"""
TopCities_with_highest_Avg_TaxiOut = (
    pd.DataFrame(
        df[["OriginCityName", "TaxiOut"]].groupby("OriginCityName")["TaxiOut"].mean()
    )
    .reset_index()
    .sort_values("TaxiOut")
    .head(10)
)

TopCities_with_highest_Avg_TaxiOut_plot = px.bar(
    TopCities_with_highest_Avg_TaxiOut,
    x="TaxiOut",
    y="OriginCityName",
    labels={"TaxiOut": "TaxiOut (Minutes)"},
    # orientation="h",
    height=400,
)

"""
Scatter Plot - Delay vs. Distance
"""
scatter_Dist_Delay = px.scatter(df, x="ArrDelay", y="Distance", color="Holidays")

"""
Scatter Plot - Departure Delay vs. Arrival Delay
"""
scatter_Dep_Arr = px.scatter(df, x="DepDelay", y="ArrDelay", color="Holidays")
