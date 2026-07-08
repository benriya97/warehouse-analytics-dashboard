import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('data/logistics.db')

# Load your CSV into SQLite
df = pd.read_csv('data/shipments.csv')
df.to_sql('shipments', conn, if_exists='replace', index=False)

print("=" * 60)
print("DATA QUALITY VALIDATION REPORT")
print("=" * 60)

# Query 1: Missing values
result = pd.read_sql_query("""
SELECT COUNT(*) as missing_shipment_id
FROM shipments
WHERE shipment_id IS NULL
""", conn)
print(f"\n✓ Missing Shipment IDs: {result['missing_shipment_id'].values[0]}")

# Query 2: Duplicates
duplicates = pd.read_sql_query("""
SELECT COUNT(*) as duplicate_count
FROM (
    SELECT shipment_id, COUNT(*) as cnt
    FROM shipments
    GROUP BY shipment_id
    HAVING COUNT(*) > 1
)
""", conn)
print(f"⚠ Duplicate Shipments Found: {duplicates['duplicate_count'].values[0]}")

# Query 3: Invalid dates
invalid_dates = pd.read_sql_query("""
SELECT COUNT(*) as invalid_count
FROM shipments
WHERE delivery_date < ship_date
""", conn)
print(f"⚠ Invalid Dates (delivery before ship): {invalid_dates['invalid_count'].values[0]}")

# Query 4: Outlier shipments (>45 days)
outliers = pd.read_sql_query("""
SELECT COUNT(*) as outlier_count
FROM shipments
WHERE CAST((JULIANDAY(delivery_date) - JULIANDAY(ship_date)) AS INTEGER) > 45
""", conn)
print(f"⚠ Shipments Taking >45 Days: {outliers['outlier_count'].values[0]}")

# Query 5: Stock variance
variance = pd.read_sql_query("""
SELECT COUNT(*) as variance_count
FROM shipments
WHERE ABS(system_inventory - physical_count) > 50
""", conn)
print(f"⚠ Warehouse Stock Variances >50 units: {variance['variance_count'].values[0]}")

# Query 6: Cancelled orders
cancelled = pd.read_sql_query("""
SELECT warehouse, COUNT(*) as cancelled
FROM shipments
WHERE status = 'Cancelled'
GROUP BY warehouse
ORDER BY cancelled DESC
""", conn)
print(f"\n⚠ Cancelled Orders by Warehouse:")
print(cancelled.to_string(index=False))

print("\n" + "=" * 60)
print("RECOMMENDATIONS:")
print("=" * 60)
print("1. Investigate duplicate shipment IDs - may indicate system sync issues")
print("2. Validate date logic in order entry system")
print("3. Review outlier shipments - possible customs/logistics delays")
print("4. Reconcile inventory variance - check warehouse process accuracy")
print("5. Analyze cancellation patterns - focus on warehouses with high rates")

conn.close()
