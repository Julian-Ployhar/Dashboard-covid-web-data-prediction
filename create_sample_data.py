import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample COVID cases data
start_date = datetime(2020, 3, 1)
end_date = datetime(2020, 8, 31)
dates = pd.date_range(start_date, end_date, freq='D')

# Generate realistic COVID case data with some seasonality and trends
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

# Create sample web metrics data
web_metrics = pd.DataFrame({
    'date': dates,
    'page_views': np.random.poisson(1000, len(dates)) + 500,
    'unique_visitors': np.random.poisson(800, len(dates)) + 300,
    'search_queries': np.random.poisson(200, len(dates)) + 100,
    'covid_symptom_searches': np.random.poisson(50, len(dates)) + 20,
    'appointment_requests': np.random.poisson(30, len(dates)) + 10
})

# Save the files
cases_df.to_csv('cases.csv', index=False)
web_metrics.to_csv('web_metrics.csv', index=False)

print("✅ Created sample data files:")
print("   - cases.csv")
print("   - web_metrics.csv")
print("\nNow run: python datacleaner.py") 