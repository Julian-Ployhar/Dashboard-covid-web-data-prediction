import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def check_file_exists(filename):
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found!")
        print(f"   Please make sure {filename} is in the current directory.")
        print(f"   If you don't have this file, run: python create_sample_data.py")
        return False
    return True

# Check if required files exist
if not check_file_exists("cases.csv") or not check_file_exists("web_metrics.csv"):
    exit(1)

try:
    # Load data
    print("📊 Loading data files...")
    cases = pd.read_csv("cases.csv", parse_dates=["date"])
    web = pd.read_csv("web_metrics.csv", parse_dates=["date"])
    
    print(f"   ✅ Loaded cases.csv: {len(cases)} rows")
    print(f"   ✅ Loaded web_metrics.csv: {len(web)} rows")

    # Merge
    print("🔗 Merging datasets...")
    df = pd.merge(web, cases, on="date", how="inner")
    print(f"   ✅ Merged data: {len(df)} rows")

    # Drop rows with missing data
    print("🧹 Cleaning data...")
    initial_rows = len(df)
    df.dropna(inplace=True)
    print(f"   ✅ Removed {initial_rows - len(df)} rows with missing data")

    # Save raw merged for backup
    df.to_csv("merged_data_raw.csv", index=False, encoding='utf-8')
    print("   ✅ Saved merged_data_raw.csv")

    # Z-score standardize all features except 'date' and 'cases'
    print("📏 Standardizing features...")
    features = df.drop(columns=['date', 'cases'])
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Convert back to DataFrame
    features_scaled_df = pd.DataFrame(features_scaled, columns=features.columns)

    # Final clean DataFrame
    cleaned = pd.concat([df['date'], features_scaled_df, df['cases']], axis=1)

    # Export to CSV with proper formatting
    cleaned.to_csv("cleaned_merged_data.csv", index=False, encoding='utf-8', float_format='%.6f')
    print("✅ Successfully created cleaned_merged_data.csv")
    print(f"   📈 Final dataset: {len(cleaned)} rows, {len(cleaned.columns)} columns")
    print("\n🎉 Data cleaning complete! You can now run:")
    print("   streamlit run covidDashboard.py")

except Exception as e:
    print(f"❌ Error during data cleaning: {str(e)}")
    print("   Please check your input files and try again.")
