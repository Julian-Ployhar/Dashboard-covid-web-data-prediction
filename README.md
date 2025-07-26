# COVID-19 Data Prediction Dashboard

### Original Analysis originally conducted July 2020 by Northwell Health nyc

This repository hosts a COVID-19 case prediction system that analyzes the relationship between web traffic data and COVID-19 case surges. The program includes a full course meal including data cleaning, analysis, and an interactive dashboard.

It was built using Northwell healths Covid-web-data-prediction as the template for the idea structure and logic. 
NOTE the Northwell CSV metric data was unavailable so a different set of hospital data was utilized in its place this is not directly representative of Northwell healths data as this program is a proof of concept.

### Option 1: One-Click Launch (Windows)
1. **Double-click** `run_dashboard.bat`
2. **Wait** for the setup to complete
3. **Dashboard opens** automatically in your browser

###Command Line
1. **obligitory virtual environment activation**:
   venv\Scripts\activate

2. **Run the complete setup in bash script**:
   python setup_and_run.py


3. **Dashboard opens** at `http://localhost:8501`

---

## if doing manual setup >>>

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
# assuming bash is used for the terminal in these cases unless stated otherwise
   python -m venv venv
   venv\Scripts\activate  # On Windows

3. **Install dependencies**
   pip install -r requirements.txt
4. **Create sample data** (if you don't have your own data)
   python create_sample_data.py
5. **Clean and prepare the data**
   python datacleaner.py
6. **Launch the dashboard**
   streamlit run covidDashboard.py
   The dashboard will open at `http://localhost:8501`

##
- `setup_and_run.py` - **Complete setup and launch script** (recommended)
- `run_dashboard.bat` - **Windows one-click launcher**
- `covidDashboard.py` - Streamlit dashboard with interactive graphs
- `datacleaner.py` - Data cleaning and prepping
- `create_sample_data.py` - Generates sample data
- `covid-web-data-predictor-notebook.ipynb` - Jupyter notebook for analysis this should mostly be untouched from the original
- `requirements.txt` - dependencies
- `web_input_data_v3_from_BQ.sql` - SQL query for BigQuery

##

### Input Files used
- `cases.csv` - COVID case data with columns: `date`, `cases`
- `web_metrics.csv` - Web traffic data with columns: `date` and various metrics

### output
- `cleaned_merged_data.csv` - Processed data ready for analysis
- `merged_data_raw.csv` - Backup of raw merged data

### Dashboardfunctionality
- **Time Series Visualization**: Daily COVID case counts over time
- **Interactive Metrics**: Select web metrics to compare with cases
- **Correlation Analysis**: See how web interactions relate to case surges
- **Data Exploration**: Raw data viewer and distribution plots

### Data Analysis
- Open `covid-web-data-predictor-notebook.ipynb` for detailed analysis
- Includes statistical modeling and predictive analytics

### troubleshooting protocol because sometimes things don't work out like you planned at first

**"File not found" errors**
- Run `python setup_and_run.py` to create all required files
- Or manually run: `python create_sample_data.py` then `python datacleaner.py`

**Import error**
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt`

**Dashboard unfunctional**
- Use `streamlit run covidDashboard.py` (not `python covidDashboard.py`)
- Or use the simplified `python setup_and_run.py`

**Port in use**
- Try a different port: `streamlit run covidDashboard.py --server.port 8502`
