#!/usr/bin/env python3
"""
Complete setup and run script for COVID Dashboard
This script handles everything from data creation to dashboard launch.
"""

import os
import sys
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def print_step(step_num, description):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*60}")

def create_sample_data():
    """Create realistic sample data files"""
    print_step(1, "Creating Sample Data Files")
    
    # Create sample COVID cases data
    start_date = datetime(2020, 3, 1)
    end_date = datetime(2020, 8, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Generate realistic COVID case data with trends and seasonality
    np.random.seed(42)  # For reproducible results
    base_cases = 50
    trend = np.linspace(0, 100, len(dates))  # Upward trend
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 30)  # Monthly seasonality
    noise = np.random.normal(0, 15, len(dates))  # Random noise
    cases = np.maximum(0, base_cases + trend + seasonal + noise).astype(int)
    
    cases_df = pd.DataFrame({
        'date': dates,
        'cases': cases
    })
    
    # Create sample web metrics data with correlation to cases
    # Add some correlation between web activity and cases
    case_influence = cases * 0.1  # Web activity influenced by cases
    web_metrics = pd.DataFrame({
        'date': dates,
        'page_views': np.random.poisson(1000, len(dates)) + 500 + case_influence,
        'unique_visitors': np.random.poisson(800, len(dates)) + 300 + case_influence * 0.8,
        'search_queries': np.random.poisson(200, len(dates)) + 100 + case_influence * 0.5,
        'covid_symptom_searches': np.random.poisson(50, len(dates)) + 20 + case_influence * 0.3,
        'appointment_requests': np.random.poisson(30, len(dates)) + 10 + case_influence * 0.2
    })
    
    # Save the files
    cases_df.to_csv('cases.csv', index=False)
    web_metrics.to_csv('web_metrics.csv', index=False)
    
    print("✅ Created sample data files:")
    print(f"   📊 cases.csv: {len(cases_df)} rows")
    print(f"   🌐 web_metrics.csv: {len(web_metrics)} rows")
    print("   📈 Data includes realistic trends and correlations")

def clean_data():
    """Run the data cleaning process"""
    print_step(2, "Cleaning and Processing Data")
    
    try:
        # Import and run the data cleaning logic
        import pandas as pd
        from sklearn.preprocessing import StandardScaler
        
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
        df.to_csv("merged_data_raw.csv", index=False)
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

        # Export to CSV
        cleaned.to_csv("cleaned_merged_data.csv", index=False)
        print("✅ Successfully created cleaned_merged_data.csv")
        print(f"   📈 Final dataset: {len(cleaned)} rows, {len(cleaned.columns)} columns")
        
    except Exception as e:
        print(f"❌ Error during data cleaning: {str(e)}")
        sys.exit(1)

def check_files():
    """Verify all required files exist"""
    print_step(3, "Verifying Files")
    
    required_files = [
        'cases.csv',
        'web_metrics.csv', 
        'cleaned_merged_data.csv',
        'merged_data_raw.csv'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ❌ {file} - MISSING")
            all_good = False
    
    if not all_good:
        print("\n❌ Some required files are missing!")
        sys.exit(1)
    
    print("\n✅ All required files are present and ready!")

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print_step(4, "Launching Dashboard")
    
    print("🚀 Starting Streamlit dashboard...")
    print("   📱 The dashboard will open in your browser at http://localhost:8501")
    print("   ⏹️  Press Ctrl+C to stop the dashboard when you're done")
    print("\n" + "="*60)
    
    try:
        # Launch streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "covidDashboard.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("   Try running manually: streamlit run covidDashboard.py")
    except FileNotFoundError:
        print("\n❌ Streamlit not found!")
        print("   Install it with: pip install streamlit")

def main():
    """Main setup and run function"""
    print("🦠 COVID-19 Dashboard Setup and Launch")
    print("This script will set up everything and launch your dashboard.")
    
    # Check if we're in the right directory
    if not os.path.exists('covidDashboard.py'):
        print("❌ Error: covidDashboard.py not found!")
        print("   Please run this script from the project directory.")
        sys.exit(1)
    
    # Create data if it doesn't exist
    if not os.path.exists('cases.csv') or not os.path.exists('web_metrics.csv'):
        create_sample_data()
    else:
        print("📁 Sample data files already exist, skipping creation...")
    
    # Clean data if needed
    if not os.path.exists('cleaned_merged_data.csv'):
        clean_data()
    else:
        print("📊 Cleaned data already exists, skipping cleaning...")
    
    # Verify everything
    check_files()
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main() 