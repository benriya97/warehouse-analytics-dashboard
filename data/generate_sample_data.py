import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

dates = [datetime(2024, 1, 1) + timedelta(days=x) for x in range(180)]
warehouses = ['WH-Paris', 'WH-Lyon', 'WH-Marseille', 'WH-Lille', 'WH-Toulouse']
products = ['Product-A', 'Product-B', 'Product-C', 'Product-D', 'Product-E']
statuses = ['Delivered', 'In Transit', 'Pending', 'Delayed', 'Cancelled']

records = []
for i in range(1000):
    ship_date = random.choice(dates)
    
    # 5% of shipments take >45 days (intentional outliers)
    if random.random() < 0.05:
        delivery_date = ship_date + timedelta(days=random.randint(46, 60))
    else:
        delivery_date = ship_date + timedelta(days=random.randint(1, 45))
    
    record = {
        'shipment_id': f'SHIP-{i+1000}',
        'warehouse': random.choice(warehouses),
        'product': random.choice(products),
        'quantity': random.randint(1, 500),
        'ship_date': ship_date,
        'delivery_date': delivery_date,
        'status': random.choice(statuses),
        'delivery_country': random.choice(['FR', 'DE', 'IT', 'ES', 'BE']),
        'system_inventory': random.randint(0, 1000),
        'physical_count': random.randint(0, 1000)
    }
    records.append(record)

df = pd.DataFrame(records)
df.to_csv('data/shipments.csv', index=False)
print(f'✓ Generated {len(df)} synthetic shipping records (with ~5% outliers)')
