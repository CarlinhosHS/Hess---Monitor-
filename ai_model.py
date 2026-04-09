from sklearn.ensemble import IsolationForest

def aplicar_ia(df):
    model = IsolationForest(
        contamination=0.03,
        random_state=42
    )

    df["anomalia_ia"] = model.fit_predict(df[["x_t"]])
    df["anomalia_ia"] = df["anomalia_ia"].apply(lambda x: 1 if x == -1 else 0)

    return df
