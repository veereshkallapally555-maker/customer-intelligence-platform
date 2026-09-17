import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")

print("Shape:", orders.shape)
print("\nColumns:")
print(orders.columns.tolist())

print("\nMissing values:")
print(orders.isna().sum())

print("\nDuplicate rows:", orders.duplicated().sum())

print("\nFirst 5 rows:")
print(orders.head())

print("\nInvalid customer IDs:", 
      (~orders["customer_id"].isin(customers["customer_id"])).sum())

print("Invalid product IDs:", 
      (~orders["product_id"].isin(products["product_id"])).sum())

print("\nInvalid quantities:",
      (orders["quantity"] <= 0).sum())

print("\nInvalid discounts:",
      ((orders["discount"] < 0) | (orders["discount"] > 0.20)).sum())

orders["order_date"] = pd.to_datetime(orders["order_date"])
customers["signup_date"] = pd.to_datetime(customers["signup_date"])

order_check = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id"
)

print(
    "\nOrders before customer signup:",
    (order_check["order_date"] < order_check["signup_date"]).sum()
)

print(
    "\nProducts where cost > price:",
    (products["cost"] > products["price"]).sum()
)