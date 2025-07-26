import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load data
@st.cache_data
def load_data():
    try:
        # Try with default engine first
        df = pd.read_csv("cleaned_merged_data.csv", parse_dates=["date"])
        return df
    except pd.errors.ParserError:
        try:
            # Fallback to python engine for problematic CSV files
            df = pd.read_csv("cleaned_merged_data.csv", parse_dates=["date"], engine='python')
            return df
        except Exception as e:
            st.error(f"❌ **Error parsing CSV file**: {str(e)}")
            st.error("The CSV file may be corrupted or have formatting issues.")
            st.stop()
    except FileNotFoundError:
        st.error("""
        ❌ **Data file not found!**
        
        The file `cleaned_merged_data.csv` is missing. Please:
        
        1. **Create sample data**: Run `python create_sample_data.py`
        2. **Clean the data**: Run `python datacleaner.py`
        3. **Then restart this dashboard**: `streamlit run covidDashboard.py`
        
        **Or use the simplified setup**: `python setup_and_run.py`
        """)
        st.stop()
    except Exception as e:
        st.error(f"❌ **Error loading data**: {str(e)}")
        st.error("Please check that the CSV file exists and is properly formatted.")
        st.stop()

df = load_data()

st.title("🦠 COVID-19 Case Prediction Dashboard")
st.markdown("Analyze how web interactions relate to COVID case surges.")

# Show raw data
with st.expander("See raw data"):
    st.dataframe(df)

# Time series of cases
st.subheader("Daily COVID Case Counts")
fig = px.line(df, x='date', y='cases', title="COVID Cases Over Time")
st.plotly_chart(fig)

# Select a metric
metric = st.selectbox("Choose a Web Interaction Metric", df.columns.drop(['date', 'cases']))

# Correlation
corr = df['cases'].corr(df[metric])
st.metric(label=f"Correlation with Cases", value=f"{corr:.2f}")

# Scatter plot of metric vs cases
st.subheader(f"{metric} vs COVID Cases")
scatter = px.scatter(df, x=metric, y="cases", trendline="ols", title=f"{metric} vs COVID Cases")
st.plotly_chart(scatter)

# Optional: histogram of cases
st.subheader("Case Count Distribution")
hist = px.histogram(df, x="cases", nbins=30)
st.plotly_chart(hist)
