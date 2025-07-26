"""
Data validation utilities for the COVID dashboard
Follows proper naming conventions: camelCase for classes, snake_case for functions/variables
"""

import pandas as pd
import json
from typing import List, Dict, Any

class DataValidator:
    """Validates data files and structure for the COVID dashboard"""
    
    def __init__(self, config_file_path: str = "data-validation-config.json"):
        self.config_file_path = config_file_path
        self.validation_config = self._load_validation_config()
    
    def _load_validation_config(self) -> Dict[str, Any]:
        """Load validation configuration from JSON file"""
        try:
            with open(self.config_file_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print(f"Warning: {self.config_file_path} not found, using default validation")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default validation configuration"""
        return {
            "data-validation-settings": {
                "input-file-validation": {
                    "required-columns": ["date", "cases"],
                    "date-format": "YYYY-MM-DD",
                    "min-row-count": 10
                },
                "web-metrics-validation": {
                    "required-columns": ["date", "page_views", "unique_visitors"],
                    "numeric-columns": ["page_views", "unique_visitors", "search_queries"],
                    "min-row-count": 10
                }
            }
        }
    
    def validate_covid_cases_file(self, file_path: str) -> bool:
        """Validate COVID cases data file"""
        try:
            covid_data = pd.read_csv(file_path)
            validation_settings = self.validation_config["data-validation-settings"]["input-file-validation"]
            
            # Check required columns
            required_columns = validation_settings["required-columns"]
            missing_columns = [col for col in required_columns if col not in covid_data.columns]
            if missing_columns:
                print(f"Missing required columns in {file_path}: {missing_columns}")
                return False
            
            # Check minimum row count
            min_row_count = validation_settings["min-row-count"]
            if len(covid_data) < min_row_count:
                print(f"{file_path} has insufficient data: {len(covid_data)} rows (minimum: {min_row_count})")
                return False
            
            # Validate date column
            try:
                pd.to_datetime(covid_data['date'])
            except Exception:
                print(f"Invalid date format in {file_path}")
                return False
            
            print(f"{file_path} validation passed")
            return True
            
        except Exception as error:
            print(f"Error validating {file_path}: {str(error)}")
            return False
    
    def validate_web_metrics_file(self, file_path: str) -> bool:
        """Validate web metrics data file"""
        try:
            web_data = pd.read_csv(file_path)
            validation_settings = self.validation_config["data-validation-settings"]["web-metrics-validation"]
            
            # Check required columns
            required_columns = validation_settings["required-columns"]
            missing_columns = [col for col in required_columns if col not in web_data.columns]
            if missing_columns:
                print(f"Missing required columns in {file_path}: {missing_columns}")
                return False
            
            # Check minimum row count
            min_row_count = validation_settings["min-row-count"]
            if len(web_data) < min_row_count:
                print(f"{file_path} has insufficient data: {len(web_data)} rows (minimum: {min_row_count})")
                return False
            
            # Validate numeric columns
            numeric_columns = validation_settings["numeric-columns"]
            for column in numeric_columns:
                if column in web_data.columns:
                    if not pd.api.types.is_numeric_dtype(web_data[column]):
                        print(f"Column {column} in {file_path} is not numeric")
                        return False
            
            print(f"{file_path} validation passed")
            return True
            
        except Exception as error:
            print(f"Error validating {file_path}: {str(error)}")
            return False
    
    def validate_all_input_files(self) -> bool:
        """Validate all required input files"""
        print("Validating input files...")
        
        covid_validation_passed = self.validate_covid_cases_file("cases.csv")
        web_metrics_validation_passed = self.validate_web_metrics_file("web_metrics.csv")
        
        return covid_validation_passed and web_metrics_validation_passed

class DataQualityReporter:
    """Generates data quality reports for the COVID dashboard"""
    
    @staticmethod
    def generate_data_summary(data_frame: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """Generate a summary report for a dataset"""
        summary = {
            "dataset_name": dataset_name,
            "total_rows": len(data_frame),
            "total_columns": len(data_frame.columns),
            "missing_values": data_frame.isnull().sum().to_dict(),
            "data_types": data_frame.dtypes.astype(str).to_dict()
        }
        
        # Add numeric column statistics
        numeric_columns = data_frame.select_dtypes(include=['number']).columns
        if len(numeric_columns) > 0:
            summary["numeric_statistics"] = data_frame[numeric_columns].describe().to_dict()
        
        return summary
    
    @staticmethod
    def print_quality_report(summary: Dict[str, Any]):
        """Print a formatted quality report"""
        print(f"\nData Quality Report: {summary['dataset_name']}")
        print(f"   Total rows: {summary['total_rows']}")
        print(f"   Total columns: {summary['total_columns']}")
        
        # Show missing values
        missing_values = summary['missing_values']
        if any(missing_values.values()):
            print("   Missing values:")
            for column, missing_count in missing_values.items():
                if missing_count > 0:
                    print(f"      {column}: {missing_count}")
        else:
            print("   No missing values found")
        
        print("   Data types:")
        for column, data_type in summary['data_types'].items():
            print(f"      {column}: {data_type}")

# Example usage functions
def run_data_validation():
    """Run complete data validation for the project"""
    validator = DataValidator()
    return validator.validate_all_input_files()

def generate_quality_reports():
    """Generate quality reports for all datasets"""
    try:
        covid_data = pd.read_csv("cases.csv")
        web_data = pd.read_csv("web_metrics.csv")
        
        reporter = DataQualityReporter()
        
        covid_summary = reporter.generate_data_summary(covid_data, "COVID Cases")
        web_summary = reporter.generate_data_summary(web_data, "Web Metrics")
        
        reporter.print_quality_report(covid_summary)
        reporter.print_quality_report(web_summary)
        
    except Exception as error:
        print(f"Error generating quality reports: {str(error)}")

if __name__ == "__main__":
    print("Running data validation...")
    validation_passed = run_data_validation()
    
    if validation_passed:
        print("\nGenerating quality reports...")
        generate_quality_reports()
    else:
        print("\nData validation failed, skipping quality reports") 