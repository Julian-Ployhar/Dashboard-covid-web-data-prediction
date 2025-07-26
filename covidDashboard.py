import streamlit as st
import pandas as pd
import plotly.express as px
import os

class DataLoader:
    """Handles loading and caching the processed data for the COVID dashboard"""
    
    @staticmethod
    @st.cache_data
    def load_processed_data():
        """ processed COVID data -> cleaned and merged data set"""
        try:
            # Try with default engine first
            data_frame = pd.read_csv("cleaned_merged_data.csv", parse_dates=["date"])
            return data_frame
        except pd.errors.ParserError:
            try:
                # Fallback to python engine for problematic CSV files
                data_frame = pd.read_csv("cleaned_merged_data.csv", parse_dates=["date"], engine='python')
                return data_frame
            except Exception as error:
                st.error(f"Error parsing CSV file: {str(error)}")
                st.error("The CSV file may be corrupted or have formatting issues.")
                st.stop()
        except FileNotFoundError:
            st.error("""
            Data file not found!
            
            The file `cleaned_merged_data.csv` is missing. Please:
            
            1. Create sample data: Run `python create_sample_data.py`
            2. Clean the data: Run `python datacleaner.py`
            3. Then restart this dashboard: `streamlit run covidDashboard.py`
            
            Or use the simplified setup: `python setup_and_run.py`
            """)
            st.stop()
        except Exception as error:
            st.error(f"Error loading data: {str(error)}")
            st.error("Please check that the CSV file exists and is properly formatted.")
            st.stop()

class DashboardVisualizer:
    """Handles visualization components for the COVID dashboard"""
    
    @staticmethod
    def create_time_series_plot(data_frame):
        """Create time series plot for COVID cases"""
        return px.line(data_frame, x='date', y='cases', title="COVID Cases Over Time")
    
    @staticmethod
    def create_correlation_scatter(data_frame, selected_metric):
        """Create scatter plot with correlation line"""
        return px.scatter(data_frame, x=selected_metric, y="cases", 
                         trendline="ols", title=f"{selected_metric} vs COVID Cases")
    
    @staticmethod
    def create_distribution_histogram(data_frame):
        """Create histogram for case count distribution"""
        return px.histogram(data_frame, x="cases", nbins=30)

# Initialize data loader and load data and visualizer 
data_loader = DataLoader()
processed_data = data_loader.load_processed_data()


visualizer = DashboardVisualizer()

st.title("COVID-19 Case Prediction Dashboard")
st.markdown("Analyze how web interactions relate to COVID case surges.")

# for the "show raw data" feature
with st.expander("See raw data"):
    st.dataframe(processed_data)

# Time series of cases
st.subheader("Daily COVID Case Counts")
time_series_fig = visualizer.create_time_series_plot(processed_data)
st.plotly_chart(time_series_fig)

# Select a metric
available_metrics = processed_data.columns.drop(['date', 'cases'])
selected_metric = st.selectbox("Choose a Web Interaction Metric", available_metrics)

# correlation
correlation_value = processed_data['cases'].corr(processed_data[selected_metric])
st.metric(label=f"Correlation with Cases", value=f"{correlation_value:.2f}")

# This is a Scatter plot of metric vs cases
st.subheader(f"{selected_metric} vs COVID Cases")
scatter_fig = visualizer.create_correlation_scatter(processed_data, selected_metric)
st.plotly_chart(scatter_fig)

#histogram of cases MIGHT REMOVE IF NOT NEEDED
st.subheader("Case Count Distribution")
histogram_fig = visualizer.create_distribution_histogram(processed_data)
st.plotly_chart(histogram_fig)
