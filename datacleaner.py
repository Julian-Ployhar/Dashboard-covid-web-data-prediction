import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load data
cases = pd.read_csv("cases.csv", parse_dates=["date"])
web = pd.read_csv("web_metrics.csv", parse_dates=["date"])

# Merge
df = pd.merge(web, cases, on="date", how="inner")

# Drop rows with missing data
df.dropna(inplace=True)

# Save raw merged for backup
df.to_csv("merged_data_raw.csv", index=False)

# Z-score standardize all features except 'date' and 'cases'
features = df.drop(columns=['date', 'cases'])
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Convert back to DataFrame
features_scaled_df = pd.DataFrame(features_scaled, columns=features.columns)

# Final clean DataFrame
cleaned = pd.concat([df['date'], features_scaled_df, df['cases']], axis=1)

# Export to CSV
cleaned.to_csv("cleaned_merged_data.csv", index=False)
print("✅ Saved cleaned_merged_data.csv")
