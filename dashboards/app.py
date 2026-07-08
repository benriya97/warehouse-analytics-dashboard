import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta
import os
import random
import numpy as np

st.set_page_config(page_title="Warehouse Analytics", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    db_path = 'data/logistics.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        # Generate synthetic data
        np.random.seed(42)
        random.seed(42)
        
        dates = [datetime(2024, 1, 1) + timedelta(days=x) for x in range(180)]
        warehouses = ['WH-Paris', 'WH-Lyon', 'WH-Marseille', 'WH-Lille', 'WH-Toulouse']
        products = ['Product-A', 'Product-B', 'Product-C', 'Product-D', 'Product-E']
        statuses = ['Delivered', 'In Transit', 'Pending', 'Delayed', 'Cancelled']
        
        records = []
        for i in range(1000):
            ship_date = random.choice(dates)
            if random.random() < 0.05:
                delivery_date = ship_date + timedelta(days=random.randint(46, 60))
            else:
                delivery_date = ship_date + timedelta(days=random.randint(1, 45))
            
            record = {
                'shipment_id': f'SHIP-{i+1000}',
                'warehouse': random.choice(warehouses),
                'product': random.choice(products),
                'quantity': random.randint(1, 500),
                'ship_date': ship_date.isoformat(),
                'delivery_date': delivery_date.isoformat(),
                'status': random.choice(statuses),
                'delivery_country': random.choice(['FR', 'DE', 'IT', 'ES', 'BE']),
                'system_inventory': random.randint(0, 1000),
                'physical_count': random.randint(0, 1000)
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        conn = sqlite3.connect(db_path)
        df.to_sql('shipments', conn, if_exists='replace', index=False)
        conn.close()
    
    # Load from database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM shipments", conn)
    conn.close()
    
    # Convert and calculate
    df['ship_date'] = pd.to_datetime(df['ship_date'])
    df['delivery_date'] = pd.to_datetime(df['delivery_date'])
    df['days_in_transit'] = (df['delivery_date'] - df['ship_date']).dt.days
    df['is_outlier'] = df['days_in_transit'] > 45
    df['inventory_variance'] = abs(df['system_inventory'] - df['physical_count'])
    df['has_variance'] = df['inventory_variance'] > 50
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# HEADER
st.title("📦 Warehouse & Shipping Analytics Dashboard")
st.markdown("Real-time operational insights for logistics optimization")

# KEY METRICS
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Shipments", f"{len(df):,}", "All time")
with col2:
    on_time_pct = (df['days_in_transit'] <= 30).sum() / len(df) * 100
    st.metric("On-Time Delivery %", f"{on_time_pct:.1f}%")
with col3:
    quality = ((~df['is_outlier']) & (~df['has_variance'])).sum() / len(df) * 100
    st.metric("Data Quality Score", f"{quality:.1f}%")
with col4:
    st.metric("Avg Transit Time", f"{df['days_in_transit'].mean():.1f} days")

st.divider()

st.subheader("📊 Shipping Performance Analysis")
tab1, tab2, tab3 = st.tabs(["Performance Trends", "Warehouse Analysis", "Data Quality Issues"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.histogram(df, x='days_in_transit', nbins=30, 
                           title="Distribution of Transit Times",
                           color_discrete_sequence=['#1f77b4'])
        fig1.add_vline(x=30, line_dash="dash", line_color="red")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        country_perf = df.groupby('delivery_country').apply(
            lambda x: ((x['days_in_transit'] <= 30).sum() / len(x) * 100)
        ).sort_values(ascending=False)
        fig2 = px.bar(x=country_perf.index, y=country_perf.values,
                     title="On-Time Delivery % by Country",
                     color=country_perf.values,
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    warehouse_stats = df.groupby('warehouse').agg({
        'shipment_id': 'count',
        'days_in_transit': 'mean',
        'is_outlier': 'sum'
    }).rename(columns={
        'shipment_id': 'Total Shipments',
        'days_in_transit': 'Avg Transit (days)',
        'is_outlier': 'Outlier Shipments'
    }).sort_values('Total Shipments', ascending=False)
    
    st.dataframe(warehouse_stats, use_container_width=True)
    
    fig3 = px.bar(warehouse_stats, x=warehouse_stats.index, y='Outlier Shipments',
                 title="Outlier Shipments by Warehouse",
                 color='Outlier Shipments',
                 color_continuous_scale='Reds')
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("⚠️ Data Quality Issues Found")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Outlier Shipments", f"{df['is_outlier'].sum()}", ">45 days")
    with col2:
        st.metric("Stock Variances", f"{df['has_variance'].sum()}", ">50 units")
    with col3:
        st.metric("Cancelled Orders", f"{(df['status'] == 'Cancelled').sum()}")
    
    st.divider()
    
    st.subheader("🚨 Outlier Shipments (>45 days)")
    outlier_df = df[df['is_outlier']][['shipment_id', 'warehouse', 'delivery_country', 'days_in_transit']].head(10)
    st.dataframe(outlier_df, use_container_width=True)
    
    st.subheader("📦 Warehouse Stock Variance Issues")
    variance_df = df[df['has_variance']][['warehouse', 'product', 'system_inventory', 'physical_count', 'inventory_variance']].head(10)
    st.dataframe(variance_df, use_container_width=True)

st.divider()
st.subheader("📈 How This Data Is Used")
st.info("""
**Operational Decisions:**
- Identify warehouses with poor on-time delivery → Resource allocation
- Find stock variance issues → Inventory control improvements
- Detect outlier shipments → Customer communication & claims processing
""")
st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
