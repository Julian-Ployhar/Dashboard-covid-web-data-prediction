# COVID-19 Web Data Prediction Dashboard

### Analysis originally conducted July 2020

This repository hosts a COVID-19 case prediction system that analyzes the relationship between web traffic data and COVID-19 case surges. The system includes data cleaning, analysis, and an interactive dashboard.

## 🚀 Quick Start (Simplified)

### Option 1: One-Click Launch (Windows)
1. **Double-click** `run_dashboard.bat`
2. **Wait** for the setup to complete
3. **Dashboard opens** automatically in your browser

### Option 2: Command Line
1. **Activate your virtual environment**:
   ```bash
   venv\Scripts\activate
   ```

2. **Run the complete setup**:
   ```bash
   python setup_and_run.py
   ```

3. **Dashboard opens** at `http://localhost:8501`

---

## 🔧 Manual Setup (If Needed)

### Prerequisites
- Python 3.10 or 3.11 (for best compatibility)
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Dashboard-covid-web-data-prediction
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create sample data** (if you don't have your own data)
   ```bash
   python create_sample_data.py
   ```

5. **Clean and prepare the data**
   ```bash
   python datacleaner.py
   ```

6. **Launch the dashboard**
   ```bash
   streamlit run covidDashboard.py
   ```

   The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

- `setup_and_run.py` - **Complete setup and launch script** (recommended)
- `run_dashboard.bat` - **Windows one-click launcher**
- `covidDashboard.py` - Interactive Streamlit dashboard
- `datacleaner.py` - Data cleaning and preprocessing script
- `create_sample_data.py` - Generates sample data for testing
- `covid-web-data-predictor-notebook.ipynb` - Jupyter notebook for analysis
- `requirements.txt` - Python dependencies
- `web_input_data_v3_from_BQ.sql` - SQL query for BigQuery data extraction

## 📊 Data Requirements

### Input Files (if using your own data)
- `cases.csv` - COVID case data with columns: `date`, `cases`
- `web_metrics.csv` - Web traffic data with columns: `date` and various metrics

### Output Files
- `cleaned_merged_data.csv` - Processed data ready for analysis
- `merged_data_raw.csv` - Backup of raw merged data

## 🔧 Usage

### Dashboard Features
- **Time Series Visualization**: Daily COVID case counts over time
- **Interactive Metrics**: Select web metrics to compare with cases
- **Correlation Analysis**: See how web interactions relate to case surges
- **Data Exploration**: Raw data viewer and distribution plots

### Data Analysis
- Open `covid-web-data-predictor-notebook.ipynb` for detailed analysis
- Includes statistical modeling and predictive analytics

## 🛠️ Troubleshooting

### Common Issues

**"File not found" errors**
- Run `python setup_and_run.py` to create all required files
- Or manually run: `python create_sample_data.py` then `python datacleaner.py`

**Import errors**
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt`

**Dashboard won't start**
- Use `streamlit run covidDashboard.py` (not `python covidDashboard.py`)
- Or use the simplified `python setup_and_run.py`

**Port already in use**
- Try a different port: `streamlit run covidDashboard.py --server.port 8502`

## 📝 Notes

- **Data Source**: Northwell Health uses Google Analytics data sent to BigQuery
- **Case Data**: COVID positive diagnoses identified by ICD-10 codes
- **Model**: Logistic Regression model created in Google ML
- **Deployment**: Results available in BigQuery for BI tools (Tableau, Data Studio)

## 🤝 Contributing

This repository is meant to be a starting point for other health systems. The main customization needed is feature engineering of URL patterns to categorize web traffic into predictive categories.

## 📄 License

See LICENSE file for details.
