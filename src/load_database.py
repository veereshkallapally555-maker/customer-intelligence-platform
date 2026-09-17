from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///data/db/customer_intelligence.db")

print("Database connection created!")

customers = pd.read_csv("data/cleaned/customers.csv")

customers.to_sql(
    "customers",
    engine,
    if_exists="replace",
    index=False
)

print("Customers table loaded!")

products = pd.read_csv("data/cleaned/products.csv")

products.to_sql(
    "products",
    engine,
    if_exists="replace",
    index=False
)

print("Products table loaded!")

orders = pd.read_csv("data/cleaned/orders.csv")

orders.to_sql(
    "orders",
    engine,
    if_exists="replace",
    index=False
)

print("Orders table loaded!")

from sqlalchemy import inspect

inspector = inspect(engine)

print("\nDatabase tables:")
print(inspector.get_table_names())

with engine.connect() as connection:
    for table in ["customers", "products", "orders"]:
        count = connection.exec_driver_sql(
            f"SELECT COUNT(*) FROM {table}"
        ).scalar()

        print(f"{table}: {count} rows")