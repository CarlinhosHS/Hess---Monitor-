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
ai_model.py
from sklearn.ensemble import IsolationForest

def aplicar_ia(df):
    model = IsolationForest(contamination=0.05)

    df["anomalia_ia"] = model.fit_predict(df[["x_t"]])
    df["anomalia_ia"] = df["anomalia_ia"].apply(lambda x: 1 if x == -1 else 0)

    return df
