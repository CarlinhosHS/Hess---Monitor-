import requests
import pandas as pd

def get_data():
    url = "https://services.swpc.noaa.gov/experimental/json/geoelectric/geoelectric_scatterplots.json"
    response = requests.get(url)
    data = response.json()

    valores = []

    for item in data:
        if "value" in item:
            valores.append(item["value"])

    df = pd.DataFrame({
        "tempo": range(len(valores)),
        "x_t": valores
    })
    return df

    k = 1.5
    df["tau"] = mediana + k * mad

    df["anomalia_hess"] = (df["delta_H"] > df["tau"]).astype(int)

    return df
