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

class DashboardOrchestrator:
    """Orchestrates the complete setup and launch of the COVID dashboard"""
    
    def __init__(self):
        self.project_files = {
            'input_files': ['cases.csv', 'web_metrics.csv'],
            'output_files': ['cleaned_merged_data.csv', 'merged_data_raw.csv'],
            'main_dashboard': 'covidDashboard.py'
        }
    
    def print_step_header(self, step_number, description):
        """Print a formatted step message"""
        print(f"\n{'='*60}")
        print(f"STEP {step_number}: {description}")
        print(f"{'='*60}")
    
    def create_sample_datasets(self):
        """Create realistic sample data files"""
        self.print_step_header(1, "Creating Sample Data Files")
        
        # Create sample COVID cases data
        start_date = datetime(2020, 3, 1)
        end_date = datetime(2020, 8, 31)
        date_range = pd.date_range(start_date, end_date, freq='D')
        
        # Generate realistic COVID case data with trends and seasonality
        np.random.seed(42)  # For reproducible results
        base_case_count = 50
        trend_component = np.linspace(0, 100, len(date_range))  # Upward trend
        seasonal_component = 20 * np.sin(2 * np.pi * np.arange(len(date_range)) / 30)  # Monthly seasonality
        noise_component = np.random.normal(0, 15, len(date_range))  # Random noise
        case_counts = np.maximum(0, base_case_count + trend_component + seasonal_component + noise_component).astype(int)
        
        covid_cases_df = pd.DataFrame({
            'date': date_range,
            'cases': case_counts
        })
        
        # Create sample web metrics data with correlation to cases
        # Add some correlation between web activity and cases
        case_influence = case_counts * 0.1  # Web activity influenced by cases
        web_traffic_metrics = pd.DataFrame({
            'date': date_range,
            'page_views': np.random.poisson(1000, len(date_range)) + 500 + case_influence,
            'unique_visitors': np.random.poisson(800, len(date_range)) + 300 + case_influence * 0.8,
            'search_queries': np.random.poisson(200, len(date_range)) + 100 + case_influence * 0.5,
            'covid_symptom_searches': np.random.poisson(50, len(date_range)) + 20 + case_influence * 0.3,
            'appointment_requests': np.random.poisson(30, len(date_range)) + 10 + case_influence * 0.2
        })
        
        # Save the files
        covid_cases_df.to_csv('cases.csv', index=False)
        web_traffic_metrics.to_csv('web_metrics.csv', index=False)
        
        print("Created sample data files:")
        print(f"   cases.csv: {len(covid_cases_df)} rows")
        print(f"   web_metrics.csv: {len(web_traffic_metrics)} rows")
        print("   Data includes realistic trends and correlations")
    
    def process_and_clean_data(self):
        """Run the data cleaning process"""
        self.print_step_header(2, "Cleaning and Processing Data")
        
        try:
            # Import and run the data cleaning logic
            import pandas as pd
            from sklearn.preprocessing import StandardScaler
            
            print("Loading data files...")
            covid_cases = pd.read_csv("cases.csv", parse_dates=["date"])
            web_traffic = pd.read_csv("web_metrics.csv", parse_dates=["date"])
            
            print(f"   Loaded cases.csv: {len(covid_cases)} rows")
            print(f"   Loaded web_metrics.csv: {len(web_traffic)} rows")

            # Merge
            print("Merging datasets...")
            merged_dataset = pd.merge(web_traffic, covid_cases, on="date", how="inner")
            print(f"   Merged data: {len(merged_dataset)} rows")

            # Drop rows with missing data
            print("Cleaning data...")
            initial_row_count = len(merged_dataset)
            merged_dataset.dropna(inplace=True)
            print(f"   Removed {initial_row_count - len(merged_dataset)} rows with missing data")

            # Save raw merged for backup
            merged_dataset.to_csv("merged_data_raw.csv", index=False)
            print("   Saved merged_data_raw.csv")

            # Z-score standardize all features except 'date' and 'cases'
            print("Standardizing features...")
            feature_columns = merged_dataset.drop(columns=['date', 'cases'])
            scaler = StandardScaler()
            standardized_features = scaler.fit_transform(feature_columns)

            # Convert back to DataFrame
            standardized_df = pd.DataFrame(standardized_features, columns=feature_columns.columns)

            # Final clean DataFrame
            cleaned_dataset = pd.concat([merged_dataset['date'], standardized_df, merged_dataset['cases']], axis=1)

            # Export to CSV
            cleaned_dataset.to_csv("cleaned_merged_data.csv", index=False)
            print("Successfully created cleaned_merged_data.csv")
            print(f"   Final dataset: {len(cleaned_dataset)} rows, {len(cleaned_dataset.columns)} columns")
            
        except Exception as error:
            print(f"Error during data cleaning: {str(error)}")
            sys.exit(1)
    
    def verify_required_files(self):
        """Verify all required files exist"""
        self.print_step_header(3, "Verifying Files")
        
        all_required_files = self.project_files['input_files'] + self.project_files['output_files']
        
        all_files_present = True
        for file_name in all_required_files:
            if os.path.exists(file_name):
                file_size = os.path.getsize(file_name)
                print(f"   {file_name} ({file_size:,} bytes)")
            else:
                print(f"   {file_name} - MISSING")
                all_files_present = False
        
        if not all_files_present:
            print("\nSome required files are missing!")
            sys.exit(1)
        
        print("\nAll required files are present and ready!")
    
    def launch_dashboard_interface(self):
        """Launch the Streamlit dashboard"""
        self.print_step_header(4, "Launching Dashboard")
        
        print("Starting Streamlit dashboard...")
        print("   The dashboard will open in your browser at http://localhost:8501")
        print("   Press Ctrl+C to stop the dashboard when you're done")
        print("\n" + "="*60)
        
        try:
            # Launch streamlit with kebab-case configuration
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "covidDashboard.py",
                "--server.headless", "false",
                "--server.port", "8501"
            ], check=True)
        except KeyboardInterrupt:
            print("\n\nDashboard stopped by user")
        except subprocess.CalledProcessError as error:
            print(f"\nError launching dashboard: {error}")
            print("   Try running manually: streamlit run covidDashboard.py")
        except FileNotFoundError:
            print("\nStreamlit not found!")
            print("   Install it with: pip install streamlit")
    
    def setup_and_launch(self):
        """Main setup and run function"""
        print("COVID-19 Dashboard Setup and Launch")
        print("This script will set up everything and launch your dashboard.")
        
        # Check if we're in the right directory
        if not os.path.exists(self.project_files['main_dashboard']):
            print("Error: covidDashboard.py not found!")
            print("   Please run this script from the project directory.")
            sys.exit(1)
        
        # Create data if it doesn't exist
        input_files_exist = all(os.path.exists(f) for f in self.project_files['input_files'])
        if not input_files_exist:
            self.create_sample_datasets()
        else:
            print("Sample data files already exist, skipping creation...")
        
        # Clean data if needed
        output_files_exist = all(os.path.exists(f) for f in self.project_files['output_files'])
        if not output_files_exist:
            self.process_and_clean_data()
        else:
            print("Cleaned data already exists, skipping cleaning...")
        
        # Verify everything
        self.verify_required_files()
        
        # Launch dashboard
        self.launch_dashboard_interface()

# Main execution
if __name__ == "__main__":
    orchestrator = DashboardOrchestrator()
    orchestrator.setup_and_launch() 