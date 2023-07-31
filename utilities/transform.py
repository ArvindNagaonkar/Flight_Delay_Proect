import joblib
import pandas as pd
import os

base_directory = "Models/data_transform"

Market_file = os.path.join(base_directory, "Marketing_Airline_Network")
ArrTime_file = os.path.join(base_directory, "CRSArrTimeHourDis")
DepTime_file = os.path.join(base_directory, "CRSDepTimeHourDis")
TDest_file = os.path.join(base_directory, "DestCityName")
TOrigin_file = os.path.join(base_directory, "OriginCityName")
wheelsOff_file = os.path.join(base_directory, "WheelsOffHourDis")
wheelsOn_file = os.path.join(base_directory, "WheelsOnHourDis")


Market = joblib.load(Market_file)
ArrTime = joblib.load(ArrTime_file)
DepTime = joblib.load(DepTime_file)
TDest = joblib.load(TDest_file)
TOrigin = joblib.load(TOrigin_file)
wheelsOff = joblib.load(wheelsOff_file)
wheelsOn = joblib.load(wheelsOn_file)


def TimeDis(Hour):
    ranges = [
        (3, 5, "EarlyMorning"),
        (6, 11, "Morning"),
        (12, 16, "Afternoon"),
        (17, 21, "Evening"),
    ]
    for min_range, max_range, group_label in ranges:
        if min_range <= Hour <= max_range:
            return group_label
    return "Night"


def DistanceG(dist):
    ranges = [
        (0, 250, 1),
        (251, 500, 2),
        (501, 750, 3),
        (751, 1000, 4),
        (1001, 1250, 5),
        (1251, 1500, 6),
        (1501, 1750, 7),
        (1751, 2000, 8),
        (2001, 2250, 9),
        (2251, 2500, 10),
    ]

    for min_range, max_range, group_label in ranges:
        if min_range <= dist <= max_range:
            return group_label
    return 11


def ElapsedGroup(t):
    ranges = [
        (0, 50, 1),
        (51, 100, 2),
        (101, 150, 3),
        (151, 200, 4),
        (201, 250, 5),
        (251, 300, 6),
        (301, 350, 7),
        (351, 400, 8),
        (401, 450, 9),
        (451, 500, 10),
    ]

    for min_range, max_range, group_label in ranges:
        if min_range <= t <= max_range:
            return group_label
    return 11


def transfrom(
    FlightDate,
    Origin,
    CRSDepTime,
    FTaxiOut,
    WheelsOff,
    FCRSElapsedTime,
    Marketing_AirN,
    Destination,
    CRSArrTime,
    FTaxiIn,
    WheelsOn,
    FDistance,
):
    Year = FlightDate.year
    Month = FlightDate.month
    DayofMonth = FlightDate.day
    DayofWeek = FlightDate.weekday()

    Marketing_Airline_Network = Market.transform([Marketing_AirN])[0]
    CRSDepTimeHour = int(str(CRSDepTime).split(":")[0])
    CRSDepTimeMinute = int(str(CRSDepTime).split(":")[1])
    TaxiIn = float(FTaxiIn)

    WheelsOnHour = int(str(WheelsOn).split(":")[0])
    WheelsOnMinute = int(str(WheelsOn).split(":")[1])
    CRSElapsedTime = float(FCRSElapsedTime)

    OriginCityName = TOrigin.transform([Origin])[0]
    DestCityName = TDest.transform([Destination])[0]

    CRSArrTimeHour = int(str(CRSArrTime).split(":")[0])
    CRSArrTimeMinute = int(str(CRSArrTime).split(":")[1])

    TaxiOut = float(FTaxiOut)

    WheelsOffHour = int(str(WheelsOff).split(":")[0])
    WheelsOffMinute = int(str(WheelsOff).split(":")[1])

    Distance = float(FDistance)

    DistanceGroup = DistanceG(Distance)

    CRSDepTimeHourDis = DepTime.transform([TimeDis(CRSDepTimeHour)])[0]
    WheelsOffHourDis = wheelsOff.transform([TimeDis(WheelsOffHour)])[0]
    CRSArrTimeHourDis = ArrTime.transform([TimeDis(CRSArrTimeHour)])[0]
    WheelsOnHourDis = wheelsOn.transform([TimeDis(WheelsOnHour)])[0]

    CRSElapsedTimeGorup = ElapsedGroup(CRSElapsedTime)

    data = [
        Year,
        Month,
        DayofMonth,
        Marketing_Airline_Network,
        OriginCityName,
        DestCityName,
        TaxiOut,
        TaxiIn,
        CRSElapsedTime,
        Distance,
        DistanceGroup,
        DayofWeek,
        CRSDepTimeMinute,
        CRSDepTimeHour,
        WheelsOffMinute,
        WheelsOffHour,
        CRSArrTimeMinute,
        CRSArrTimeHour,
        WheelsOnMinute,
        WheelsOnHour,
        CRSDepTimeHourDis,
        WheelsOffHourDis,
        CRSArrTimeHourDis,
        WheelsOnHourDis,
        CRSElapsedTimeGorup,
    ]

    columns_names = [
        "Year",
        "Month",
        "DayofMonth",
        "Marketing_Airline_Network",
        "OriginCityName",
        "DestCityName",
        "TaxiOut",
        "TaxiIn",
        "CRSElapsedTime",
        "Distance",
        "DistanceGroup",
        "DayofWeek",
        "CRSDepTimeMinute",
        "CRSDepTimeHour",
        "WheelsOffMinute",
        "WheelsOffHour",
        "CRSArrTimeMinute",
        "CRSArrTimeHour",
        "WheelsOnMinute",
        "WheelsOnHour",
        "CRSDepTimeHourDis",
        "WheelsOffHourDis",
        "CRSArrTimeHourDis",
        "WheelsOnHourDis",
        "CRSElapsedTimeGorup",
    ]

    return pd.DataFrame(data=[data], columns=columns_names)
