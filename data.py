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
hess.py
import numpy as np

def aplicar_hess(df):
    df["H"] = df["x_t"]

    df["H1"] = df["H"].shift(1)
    df["H2"] = df["H"].shift(2)

    df["media"] = (df["H1"] + df["H2"]) / 2
    df["delta_H"] = abs(df["H"] - df["media"])

    window = 20

    mediana = df["H"].rolling(window).median()
    mad = df["H"].rolling(window).apply(lambda x: np.median(abs(x - np.median(x))))

    k = 1.5
    df["tau"] = mediana + k * mad

    df["anomalia_hess"] = (df["delta_H"] > df["tau"]).astype(int)

    return df
