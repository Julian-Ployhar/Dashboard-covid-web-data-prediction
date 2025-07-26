import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SampleDataGenerator:
    """Generates realistic sample data for COVID dashboard testing"""
    
    def __init__(self):
        self.start_date = datetime(2020, 3, 1)
        self.end_date = datetime(2020, 8, 31)
        self.random_seed = 42  # For reproducible results
        np.random.seed(self.random_seed)
    
    def generate_date_range(self):
        """Generate date range for the sample data"""
        return pd.date_range(self.start_date, self.end_date, freq='D')
    
    def create_covid_cases_data(self, date_range):
        """Create realistic COVID case data with trends and seasonality"""
        base_case_count = 50
        trend_component = np.linspace(0, 100, len(date_range))  # Upward trend
        seasonal_component = 20 * np.sin(2 * np.pi * np.arange(len(date_range)) / 30)  # Monthly seasonality
        noise_component = np.random.normal(0, 15, len(date_range))  # Random noise
        
        case_counts = np.maximum(0, base_case_count + trend_component + seasonal_component + noise_component).astype(int)
        
        return pd.DataFrame({
            'date': date_range,
            'cases': case_counts
        })
    
    def create_web_traffic_data(self, date_range):
        """Create sample web traffic metrics data"""
        # Add some correlation between web activity and cases
        case_influence = self.create_covid_cases_data(date_range)['cases'] * 0.1
        
        return pd.DataFrame({
            'date': date_range,
            'page_views': np.random.poisson(1000, len(date_range)) + 500 + case_influence,
            'unique_visitors': np.random.poisson(800, len(date_range)) + 300 + case_influence * 0.8,
            'search_queries': np.random.poisson(200, len(date_range)) + 100 + case_influence * 0.5,
            'covid_symptom_searches': np.random.poisson(50, len(date_range)) + 20 + case_influence * 0.3,
            'appointment_requests': np.random.poisson(30, len(date_range)) + 10 + case_influence * 0.2
        })
    
    def save_sample_files(self, covid_data, web_traffic_data):
        """Save the generated sample data to CSV files"""
        covid_data.to_csv('cases.csv', index=False)
        web_traffic_data.to_csv('web_metrics.csv', index=False)
        
        print("Created sample data files:")
        print(f"   cases.csv: {len(covid_data)} rows")
        print(f"   web_metrics.csv: {len(web_traffic_data)} rows")
        print("   Data includes realistic trends and correlations")
    
    def generate_all_sample_data(self):
        """Main method to generate all sample data"""
        print("Generating sample data files...")
        
        # Generate date range
        date_range = self.generate_date_range()
        
        # Create datasets
        covid_cases = self.create_covid_cases_data(date_range)
        web_metrics = self.create_web_traffic_data(date_range)
        
        # Save files
        self.save_sample_files(covid_cases, web_metrics)
        
        print("\nNow run: python datacleaner.py")

# Main execution
if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all_sample_data() 