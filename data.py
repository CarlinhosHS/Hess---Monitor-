import pandas as pd
import requests

def get_data():
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data)

    df["tempo"] = pd.to_datetime(df["time_tag"])
    df["x_t"] = df["kp_index"]

    return df.tail(200)
