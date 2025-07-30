import pandas as pd

def merge_and_save():
    # NYC case data
    cases_url = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/cases-by-day.csv"
    cases = pd.read_csv(cases_url, parse_dates=["date"])
    cases = cases.rename(columns={"cases": "cases_new"})

    # Mobility data (Google via Opportunity Insights)
    mob_url = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Google%20Mobility%20-%20State%20-%20Daily.csv"
    mob = pd.read_csv(mob_url, parse_dates=["date"])
    mob = mob[mob["state"] == "New York"]

    cols = [
        "retail_and_recreation_percent_change_from_baseline",
        "grocery_and_pharmacy_percent_change_from_baseline",
        "transit_stations_percent_change_from_baseline",
        "workplaces_percent_change_from_baseline",
        "residential_percent_change_from_baseline",
    ]
    mob = mob[["date"] + cols]
    mob.columns = ["date"] + [col.replace("_percent_change_from_baseline", "_change") for col in cols]

    df = pd.merge(cases[["date", "cases_new"]], mob, on="date", how="inner")
    df.to_csv("data/public_nyc_cases_mobility.csv", index=False)
    print("✅ Data saved to data/public_nyc_cases_mobility.csv")

if __name__ == "__main__":
    merge_and_save()
