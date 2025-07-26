import pandas as pd

def load_public_data(path="data/public_nyc_cases_mobility.csv"):
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.rename(columns={"cases_new": "cases"})  # Match existing structure
    return df
