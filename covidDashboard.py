import streamlit as st
import pandas as pd
import plotly.express as px

# Load data sets from the csv file
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_merged_data.csv", parse_dates=["date"])
    return df

df = load_data()

st.title("🦠 COVID-19 Case Prediction Dashboard")
st.markdown("Analyze how web interactions relate to COVID case surges.")

# showcases the raw data
with st.expander("See raw data"):
    st.dataframe(df)

# Time series of cases
st.subheader("Daily COVID Case Counts")
fig = px.line(df, x='date', y='cases', title="COVID Cases Over Time")
st.plotly_chart(fig)

# Select a metric
metric = st.selectbox("Choose a Web Interaction Metric", df.columns.drop(['date', 'cases']))

# Correlation between the cases and the metric
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
