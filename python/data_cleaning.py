import pandas as pd
import sqlite3
from datetime import datetime

print("=" * 60)
print("DATA CLEANING PIPELINE")
print("=" * 60)

# Load data
df = pd.read_csv('data/shipments.csv')
print(f"\n1. Loaded {len(df)} raw records")

# Clean: Remove exact duplicates
df_clean = df.drop_duplicates(subset=['shipment_id'])
duplicates_removed = len(df) - len(df_clean)
print(f"2. Removed {duplicates_removed} duplicate shipment records")

# Clean: Fix date format
df_clean['ship_date'] = pd.to_datetime(df_clean['ship_date'])
df_clean['delivery_date'] = pd.to_datetime(df_clean['delivery_date'])

# Validate: Flag invalid dates
invalid_mask = df_clean['delivery_date'] < df_clean['ship_date']
invalid_count = invalid_mask.sum()
print(f"3. Flagged {invalid_count} records with invalid dates")

# Remove invalid records
df_clean = df_clean[~invalid_mask]

# Create calculated field: Days in transit
df_clean['days_in_transit'] = (df_clean['delivery_date'] - df_clean['ship_date']).dt.days

# Flag outliers (>45 days) for investigation
df_clean['is_outlier'] = df_clean['days_in_transit'] > 45
outliers_flagged = df_clean['is_outlier'].sum()
print(f"4. Flagged {outliers_flagged} shipments as outliers (>45 days transit)")

# Calculate inventory variance
df_clean['inventory_variance'] = abs(df_clean['system_inventory'] - df_clean['physical_count'])
df_clean['has_variance'] = df_clean['inventory_variance'] > 50
variance_count = df_clean['has_variance'].sum()
print(f"5. Identified {variance_count} warehouse records with stock variance >50 units")

# Save cleaned data
df_clean.to_csv('data/shipments_cleaned.csv', index=False)
print(f"\n✓ Saved cleaned dataset: {len(df_clean)} records")

# Load into SQLite for dashboard queries
conn = sqlite3.connect('data/logistics.db')
df_clean.to_sql('shipments', conn, if_exists='replace', index=False)
conn.close()

print("✓ Loaded cleaned data into SQLite database")
print("=" * 60)
