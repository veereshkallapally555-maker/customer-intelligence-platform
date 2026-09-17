import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")

print("Data loaded successfully!")

print("\nCustomer missing values:")
print(customers.isna().sum())

print("\nProduct missing values:")
print(products.isna().sum())

print("\nOrder missing values:")
print(orders.isna().sum())

print("\nCustomer duplicates:", customers.duplicated().sum())
print("Product duplicates:", products.duplicated().sum())
print("Order duplicates:", orders.duplicated().sum())

print(
    "\nInvalid customer IDs:",
    (~orders["customer_id"].isin(customers["customer_id"])).sum()
)

print(
    "Invalid product IDs:",
    (~orders["product_id"].isin(products["product_id"])).sum()
)

print(
    "\nInvalid quantities:",
    (orders["quantity"] <= 0).sum()
)

print(
    "\nInvalid discounts:",
    ((orders["discount"] < 0) | (orders["discount"] > 0.20)).sum()
)

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

print(
    "\nInvalid emails:",
    (~customers["email"].str.contains("@", na=False)).sum()
)