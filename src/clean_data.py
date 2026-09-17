import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")

print("Raw data loaded successfully!")

orders["order_date"] = pd.to_datetime(orders["order_date"])
customers["signup_date"] = pd.to_datetime(customers["signup_date"])

order_check = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id"
)

invalid_orders = order_check["order_date"] < order_check["signup_date"]

orders = orders.loc[~invalid_orders].copy()

print("Invalid orders removed:", invalid_orders.sum())
print("Remaining orders:", len(orders))

invalid_products = products["cost"] > products["price"]

products = products.loc[~invalid_products].copy()

print("Invalid products removed:", invalid_products.sum())
print("Remaining products:", len(products))

customers = customers.drop_duplicates()
products = products.drop_duplicates()
orders = orders.drop_duplicates()

print("Duplicates removed.")

customers.to_csv("data/cleaned/customers.csv", index=False)
products.to_csv("data/cleaned/products.csv", index=False)
orders.to_csv("data/cleaned/orders.csv", index=False)

print("Cleaned data saved successfully!")

print("\nCleaned data shapes:")
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)

clean_order_check = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id"
)

print(
    "\nInvalid orders after cleaning:",
    (clean_order_check["order_date"] < clean_order_check["signup_date"]).sum()
)

print(
    "Invalid products after cleaning:",
    (products["cost"] > products["price"]).sum()
)

print(
    "Duplicate customers:",
    customers.duplicated().sum()
)

print(
    "Duplicate products:",
    products.duplicated().sum()
)

print(
    "Duplicate orders:",
    orders.duplicated().sum()
)