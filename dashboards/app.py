import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(page_title="Warehouse Analytics", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/logistics.db')
    df = pd.read_sql_query("SELECT * FROM shipments", conn)
    conn.close()
    
    # Convert date columns
    df['ship_date'] = pd.to_datetime(df['ship_date'])
    df['delivery_date'] = pd.to_datetime(df['delivery_date'])
    
    # Recreate calculated columns
    df['days_in_transit'] = (df['delivery_date'] - df['ship_date']).dt.days
    df['is_outlier'] = df['days_in_transit'] > 45
    df['inventory_variance'] = abs(df['system_inventory'] - df['physical_count'])
    df['has_variance'] = df['inventory_variance'] > 50
    
    return df

df = load_data()

# ===== HEADER =====
st.title("📦 Warehouse & Shipping Analytics Dashboard")
st.markdown("Real-time operational insights for logistics optimization")

# ===== KEY METRICS =====
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_shipments = len(df)
    st.metric("Total Shipments", f"{total_shipments:,}", "All time")

with col2:
    on_time = (df['days_in_transit'] <= 30).sum()
    on_time_pct = (on_time / len(df) * 100)
    st.metric("On-Time Delivery %", f"{on_time_pct:.1f}%", f"{on_time:,} shipments")

with col3:
    data_quality = ((~df['is_outlier']) & (~df['has_variance'])).sum() / len(df) * 100
    st.metric("Data Quality Score", f"{data_quality:.1f}%", "Clean records")

with col4:
    avg_transit = df['days_in_transit'].mean()
    st.metric("Avg Transit Time", f"{avg_transit:.1f} days", "All routes")

st.divider()

# ===== TAB 1: SHIPPING PERFORMANCE =====
st.subheader("📊 Shipping Performance Analysis")

tab1, tab2, tab3 = st.tabs(["Performance Trends", "Warehouse Analysis", "Data Quality Issues"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Days in transit distribution
        fig1 = px.histogram(df, x='days_in_transit', nbins=30, 
                           title="Distribution of Transit Times",
                           labels={'days_in_transit': 'Days', 'count': 'Number of Shipments'},
                           color_discrete_sequence=['#1f77b4'])
        fig1.add_vline(x=30, line_dash="dash", line_color="red", 
                      annotation_text="Target: 30 days", annotation_position="top right")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # On-time delivery by country
        delivery_country_perf = df.groupby('delivery_country').apply(
            lambda x: ((x['days_in_transit'] <= 30).sum() / len(x) * 100)
        ).sort_values(ascending=False)
        
        fig2 = px.bar(x=delivery_country_perf.index, y=delivery_country_perf.values,
                     title="On-Time Delivery % by Country",
                     labels={'x': 'Country', 'y': 'On-Time %'},
                     color=delivery_country_perf.values,
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # Warehouse performance
    warehouse_stats = df.groupby('warehouse').agg({
        'shipment_id': 'count',
        'days_in_transit': 'mean',
        'is_outlier': lambda x: (x).sum()
    }).rename(columns={
        'shipment_id': 'Total Shipments',
        'days_in_transit': 'Avg Transit (days)',
        'is_outlier': 'Outlier Shipments'
    }).sort_values('Total Shipments', ascending=False)
    
    st.dataframe(warehouse_stats, use_container_width=True)
    
    # Warehouse outliers chart
    fig3 = px.bar(warehouse_stats, x=warehouse_stats.index, y='Outlier Shipments',
                 title="Outlier Shipments by Warehouse",
                 color='Outlier Shipments',
                 color_continuous_scale='Reds')
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("⚠️ Data Quality Issues Found")
    
    # Create tabs for different issue types
    issue1, issue2, issue3 = st.columns(3)
    
    with issue1:
        outlier_count = df['is_outlier'].sum()
        st.metric("Outlier Shipments", f"{outlier_count}", ">45 days transit")
    
    with issue2:
        variance_count = df['has_variance'].sum()
        st.metric("Stock Variances", f"{variance_count}", ">50 units discrepancy")
    
    with issue3:
        cancelled_count = (df['status'] == 'Cancelled').sum()
        st.metric("Cancelled Orders", f"{cancelled_count}", "Requires investigation")
    
    st.divider()
    
    # Show outlier shipments table
    st.subheader("🚨 Outlier Shipments (>45 days)")
    outlier_df = df[df['is_outlier']][['shipment_id', 'warehouse', 'delivery_country', 
                                        'days_in_transit']].head(10)
    st.dataframe(outlier_df, use_container_width=True)
    
    # Show stock variance issues
    st.subheader("📦 Warehouse Stock Variance Issues")
    variance_df = df[df['has_variance']][['warehouse', 'product', 'system_inventory', 
                                          'physical_count', 'inventory_variance']].head(10)
    st.dataframe(variance_df, use_container_width=True)

st.divider()

# ===== FOOTER =====
st.subheader("📈 How This Data Is Used")
st.info("""
**Operational Decisions:**
- Identify warehouses with poor on-time delivery → Resource allocation
- Find stock variance issues → Inventory control improvements
- Detect outlier shipments → Customer communication & claims processing
- Track data quality → Improve system reliability

**For Stakeholders:**
- Operations: Optimize delivery routes & warehouse processes
- Finance: Forecast shipping costs & claim reserves
- Leadership: Strategic capacity planning across regions
""")

st.caption(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
