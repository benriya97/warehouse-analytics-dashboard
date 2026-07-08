-- Query 1: Find missing/null values
SELECT COUNT(*) as missing_shipment_id
FROM shipments
WHERE shipment_id IS NULL;

-- Query 2: Find duplicate shipments
SELECT shipment_id, COUNT(*) as count
FROM shipments
GROUP BY shipment_id
HAVING COUNT(*) > 1;

-- Query 3: Find invalid dates (delivery before ship)
SELECT shipment_id, ship_date, delivery_date
FROM shipments
WHERE delivery_date < ship_date;

-- Query 4: Find extreme outliers (shipments taking >45 days)
SELECT shipment_id, warehouse, delivery_country,
       CAST((JULIANDAY(delivery_date) - JULIANDAY(ship_date)) AS INTEGER) as days_in_transit
FROM shipments
WHERE CAST((JULIANDAY(delivery_date) - JULIANDAY(ship_date)) AS INTEGER) > 45;

-- Query 5: Find warehouse stock variance (system vs physical count mismatch)
SELECT warehouse, product,
       system_inventory, physical_count,
       ABS(system_inventory - physical_count) as variance
FROM shipments
WHERE ABS(system_inventory - physical_count) > 50
ORDER BY variance DESC;

-- Query 6: Find cancelled orders (potential data quality issue)
SELECT COUNT(*) as cancelled_orders, warehouse
FROM shipments
WHERE status = 'Cancelled'
GROUP BY warehouse
ORDER BY cancelled_orders DESC;
