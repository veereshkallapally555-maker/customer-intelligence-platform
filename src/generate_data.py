import pandas as pd
import numpy as np

customers = pd.DataFrame({
    "customer_id": [f"C{i:04d}" for i in range(1, 501)],
    "name": [f"Customer {i}" for i in range(1, 501)],
    "city": np.random.choice(
        ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai"],
        500
    ),
    "email": [f"customer{i}@example.com" for i in range(1, 501)],
    "signup_date": pd.date_range(
        start="2025-01-01",
        periods=500,
        freq="D"
    )
})

customers.to_csv("data/raw/customers.csv", index=False)

print(customers.head())

products = pd.DataFrame({
    "product_id": [f"P{i:04d}" for i in range(1, 101)],
    "product_name": [f"Product {i}" for i in range(1, 101)],
    "category": np.random.choice(
        ["Electronics", "Clothing", "Home", "Beauty", "Sports"],
        100
    ),
    "price": np.random.randint(500, 10000, 100),
    "cost": np.random.randint(200, 7000, 100)
})

products.to_csv("data/raw/products.csv", index=False)

print(products.head())

orders = pd.DataFrame({
    "order_id": [f"O{i:05d}" for i in range(1, 5001)],
    "customer_id": np.random.choice(customers["customer_id"], 5000),
    "product_id": np.random.choice(products["product_id"], 5000),
    "order_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2025-01-01", "2026-06-30"),
            5000
        )
    ),
    "quantity": np.random.randint(1, 5, 5000),
    "discount": np.random.choice(
        [0, 0.05, 0.10, 0.15, 0.20],
        5000
    )
})

orders.to_csv("data/raw/orders.csv", index=False)

print(orders.head())