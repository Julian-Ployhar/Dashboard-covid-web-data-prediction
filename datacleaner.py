import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

class DataProcessor:
    """Handles data processing and cleaning operations"""
    
    def __init__(self):
        self.required_files = ["cases.csv", "web_metrics.csv"]
        self.output_files = ["merged_data_raw.csv", "cleaned_merged_data.csv"]
    
    def verify_file_exists(self, file_name):
        """Check if a required file exists in the current directory"""
        if not os.path.exists(file_name):
            print(f"Error: {file_name} not found!")
            print(f"   Please make sure {file_name} is in the current directory.")
            print(f"   If you don't have this file, run: python create_sample_data.py")
            return False
        return True
    
    def validate_input_files(self):
        """Validate that all required input files exist"""
        for file_name in self.required_files:
            if not self.verify_file_exists(file_name):
                return False
        return True
    
    def load_datasets(self):
        """Load and return the COVID cases and web metrics datasets"""
        print("Loading data files...")
        covid_cases = pd.read_csv("cases.csv", parse_dates=["date"])
        web_traffic = pd.read_csv("web_metrics.csv", parse_dates=["date"])
        
        print(f"   Loaded cases.csv: {len(covid_cases)} rows")
        print(f"   Loaded web_metrics.csv: {len(web_traffic)} rows")
        
        return covid_cases, web_traffic
    
    def merge_datasets(self, covid_cases, web_traffic):
        """Merge COVID cases and web traffic datasets"""
        print("Merging datasets...")
        merged_data = pd.merge(web_traffic, covid_cases, on="date", how="inner")
        print(f"   Merged data: {len(merged_data)} rows")
        return merged_data
    
    def clean_dataset(self, merged_data):
        """Remove rows with missing data"""
        print("Cleaning data...")
        initial_row_count = len(merged_data)
        cleaned_data = merged_data.dropna()
        removed_rows = initial_row_count - len(cleaned_data)
        print(f"   Removed {removed_rows} rows with missing data")
        return cleaned_data
    
    def standardize_features(self, cleaned_data):
        """Apply Z-score standardization to features"""
        print("Standardizing features...")
        feature_columns = cleaned_data.drop(columns=['date', 'cases'])
        scaler = StandardScaler()
        standardized_features = scaler.fit_transform(feature_columns)
        
        # Convert back to DataFrame
        standardized_df = pd.DataFrame(standardized_features, columns=feature_columns.columns)
        
        # Combine with date and cases
        final_dataset = pd.concat([cleaned_data['date'], standardized_df, cleaned_data['cases']], axis=1)
        return final_dataset
    
    def save_processed_data(self, merged_data, final_dataset):
        """Save both raw merged and cleaned datasets"""
        # Save raw merged for backup
        merged_data.to_csv("merged_data_raw.csv", index=False, encoding='utf-8')
        print("   Saved merged_data_raw.csv")
        
        # Export final cleaned dataset
        final_dataset.to_csv("cleaned_merged_data.csv", index=False, encoding='utf-8', float_format='%.6f')
        print("Successfully created cleaned_merged_data.csv")
        print(f"   Final dataset: {len(final_dataset)} rows, {len(final_dataset.columns)} columns")
    
    def process_data(self):
        """Main method to process and clean the data"""
        try:
            # Validate input files
            if not self.validate_input_files():
                return False
            
            # Load datasets
            covid_cases, web_traffic = self.load_datasets()
            
            # Merge datasets
            merged_data = self.merge_datasets(covid_cases, web_traffic)
            
            # Clean data
            cleaned_data = self.clean_dataset(merged_data)
            
            # Standardize features
            final_dataset = self.standardize_features(cleaned_data)
            
            # Save results
            self.save_processed_data(merged_data, final_dataset)
            
            print("\nData cleaning complete! You can now run:")
            print("   streamlit run covidDashboard.py")
            return True
            
        except Exception as error:
            print(f"Error during data cleaning: {str(error)}")
            print("   Please check your input files and try again.")
            return False

# Main execution
if __name__ == "__main__":
    processor = DataProcessor()
    processor.process_data()
