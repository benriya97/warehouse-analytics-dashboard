# Warehouse & Shipping Analytics Dashboard

An end-to-end data analytics project demonstrating SQL, Python, and dashboard design skills.

## Project Overview

This project takes raw logistics data and transforms it into actionable business intelligence:

1. **Data Extraction:** Load shipping & warehouse data
2. **Data Validation:** Write SQL queries to identify data quality issues
   - Missing records
   - Duplicate shipments
   - Invalid dates
   - Stock variance discrepancies
   - Outlier shipments (>45 days delivery)
3. **Data Cleaning:** Python pipeline to normalize and validate data
4. **Visualization:** Interactive Streamlit dashboard showing KPIs & alerts

## Key Findings

- **904 stock variance issues** identified across warehouses
- **~50 outlier shipments** taking >45 days (vs. 30-day target)
- **~214 cancelled orders** distributed across warehouses
- **Data quality score: 91%** after cleaning

## Tech Stack

- **Data Processing:** Python, Pandas
- **Database:** SQLite, SQL
- **Visualization:** Streamlit, Plotly
- **Version Control:** GitHub

## Dashboard Features

- Real-time KPI metrics (on-time delivery %, data quality score)
- Shipping performance trends by country & warehouse
- Data quality alerts & anomaly detection
- Detailed tables for investigation & action

## How to Run Locally

\\\ash
# Clone repository
git clone https://github.com/benriya97/warehouse-analytics-dashboard.git
cd warehouse-analytics-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run data validation
python python/data_validation.py

# Run data cleaning
python python/data_cleaning.py

# Start dashboard
streamlit run dashboards/app.py
\\\

## What This Demonstrates

✓ **SQL skills:** Writing queries for data validation & discovery  
✓ **Python proficiency:** Data cleaning, transformation, automation  
✓ **Dashboard design:** Creating user-focused visualizations  
✓ **Problem-solving:** Identifying & documenting data quality issues  
✓ **End-to-end pipeline:** From raw data to actionable insights  

---

*Created as a portfolio project for Business Intelligence & Analytics roles*
