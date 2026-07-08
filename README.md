# Warehouse & Shipping Analytics Dashboard

An end-to-end data analytics project demonstrating SQL, Python, and dashboard design skills.

## Live Demo

**View Live Dashboard:** https://warehouse-analytics-dashboard-cnjfbkfpt5os7r9fiqv4hv.streamlit.app/

Click the link above to explore the interactive dashboard!

## Project Overview

This project takes raw logistics data and transforms it into actionable business intelligence:

1. **Data Extraction:** Load shipping & warehouse data from raw CSV
2. **Data Validation:** Write SQL queries to identify data quality issues
   - Missing records
   - Duplicate shipments
   - Invalid dates
   - Stock variance discrepancies
   - Outlier shipments (>45 days delivery)
3. **Data Cleaning:** Python pipeline to normalize and validate data
4. **Visualization:** Interactive Streamlit dashboard showing KPIs & alerts

## Key Findings

- **156 stock variance issues** identified across warehouses
- **47 outlier shipments** taking >45 days (vs. 30-day target)
- **214 cancelled orders** distributed across warehouses
- **Data quality score: 91%** after cleaning

## Tech Stack

- Data Processing: Python, Pandas
- Database: SQLite, SQL
- Visualization: Streamlit, Plotly
- Version Control: GitHub

## Dashboard Features

- Real-time KPI metrics (on-time delivery %, data quality score)
- Shipping performance trends by country & warehouse
- Data quality alerts & anomaly detection
- Detailed tables for investigation & action
- Stock variance tracking

## How to Run Locally

1. Clone repository:
   git clone https://github.com/benriya97/warehouse-analytics-dashboard.git
   cd warehouse-analytics-dashboard

2. Create virtual environment:
   python -m venv venv
   source venv/bin/activate
   (On Windows: venv\Scripts\activate)

3. Install dependencies:
   pip install -r requirements.txt

4. Run data validation:
   python python/data_validation.py

5. Run data cleaning:
   python python/data_cleaning.py

6. Start dashboard:
   streamlit run dashboards/app.py

## Project Structure

warehouse-analytics-dashboard/
├── data/
│   ├── shipments.csv (raw data)
│   ├── shipments_cleaned.csv (processed data)
│   └── logistics.db (SQLite database)
├── sql/
│   └── validation_queries.sql (data quality checks)
├── python/
│   ├── data_validation.py (SQL validation report)
│   └── data_cleaning.py (data cleaning pipeline)
├── dashboards/
│   └── app.py (Streamlit dashboard)
├── requirements.txt (dependencies)
└── README.md (this file)

## What This Demonstrates

✓ SQL skills: Writing queries for data validation & discovery
✓ Python proficiency: Data cleaning, transformation, automation
✓ Dashboard design: Creating user-focused visualizations
✓ Problem-solving: Identifying & documenting data quality issues
✓ End-to-end pipeline: From raw data to actionable insights
✓ Cloud deployment: Live Streamlit Cloud hosting

## Data Quality Issues Found

- 156 warehouse stock variances (>50 units difference)
- 47 shipments exceeding 45-day delivery window
- 214 cancelled orders (pattern analysis by warehouse)
- 0 duplicate shipments (good data integrity)
- 0 missing shipment IDs (complete records)

## Use Cases

- Operations: Optimize delivery routes & warehouse processes
- Finance: Forecast shipping costs & analyze variances
- Leadership: Strategic capacity planning across regions

---

Created as a portfolio project for Business Intelligence & Analytics roles
Author: Riya Benoy
Date: July 2026
Repository: https://github.com/benriya97/warehouse-analytics-dashboard
Live Demo: https://warehouse-analytics-dashboard-cnjfbkfpt5os7r9fiqv4hv.streamlit.app/
