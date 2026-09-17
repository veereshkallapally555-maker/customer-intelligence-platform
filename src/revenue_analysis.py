import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/db/customer_intelligence.db")

city_query = """
SELECT
    customers.city,
    SUM(
        products.price
        * orders.quantity
        * (1 - orders.discount)
    ) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
JOIN customers
    ON orders.customer_id = customers.customer_id
GROUP BY customers.city
ORDER BY revenue DESC
"""

city_df = pd.read_sql(city_query, engine)

print("\nRevenue by city:")
print(city_df)

plt.figure(figsize=(10, 6))

plt.bar(
    city_df["city"],
    city_df["revenue"]
)

plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig("reports/charts/revenue_by_city.png")

plt.show()

customer_query = """
SELECT
    customers.customer_id,
    customers.name,
    SUM(
        products.price
        * orders.quantity
        * (1 - orders.discount)
    ) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
JOIN customers
    ON orders.customer_id = customers.customer_id
GROUP BY
    customers.customer_id,
    customers.name
ORDER BY revenue DESC
LIMIT 10
"""

customer_df = pd.read_sql(customer_query, engine)

print("\nTop 10 customers by revenue:")
print(customer_df)

plt.figure(figsize=(10, 6))

plt.bar(
    customer_df["name"],
    customer_df["revenue"]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("reports/charts/top_10_customers_revenue.png")

plt.show()

customer_summary_query = """
SELECT
    customers.customer_id,
    customers.name,

    COUNT(DISTINCT orders.order_id) AS total_orders,

    COUNT(
    DISTINCT CASE
        WHEN products.product_id IS NOT NULL
        THEN orders.order_id
    END
) AS orders_with_valid_products,

    ROUND(
        SUM(
            products.price
            * orders.quantity
            * (1 - orders.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            products.price
            * orders.quantity
            * (1 - orders.discount)
        )
        /
        NULLIF(
            COUNT(
                DISTINCT CASE
                    WHEN products.product_id IS NOT NULL
                    THEN orders.order_id
                END
            ),
            0
        ),
        2
    ) AS average_order_value

FROM customers

LEFT JOIN orders
    ON customers.customer_id = orders.customer_id

LEFT JOIN products
    ON orders.product_id = products.product_id

GROUP BY
    customers.customer_id,
    customers.name

ORDER BY total_revenue DESC
"""

customer_summary_df = pd.read_sql(
    customer_summary_query,
    engine
)

pd.set_option("display.max_columns", None)
print("\nCustomer order summary:")
print(customer_summary_df.head(10))

customer_summary_df.to_csv(
    "reports/customer_summary.csv",
    index=False
)

product_query = """
SELECT
    products.product_id,
    products.product_name,
    products.category,
    SUM(orders.quantity) AS units_sold,
    ROUND(
        SUM(
            products.price
            * orders.quantity
            * (1 - orders.discount)
        ),
        2
    ) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
GROUP BY
    products.product_id,
    products.product_name,
    products.category
ORDER BY revenue DESC
LIMIT 10
"""

product_df = pd.read_sql(
    product_query,
    engine
)

print("\nTop 10 products by revenue:")
print(product_df)

product_df.to_csv(
    "reports/product_performance.csv",
    index=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    product_df["product_name"],
    product_df["revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "reports/charts/top_10_products_revenue.png"
)

plt.show()

kpi_query = """
SELECT
    COUNT(DISTINCT orders.order_id) AS total_orders,

    ROUND(
        SUM(
            products.price
            * orders.quantity
            * (1 - orders.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            products.price
            * orders.quantity
            * (1 - orders.discount)
        )
        / COUNT(DISTINCT orders.order_id),
        2
    ) AS average_order_value

FROM orders
JOIN products
    ON orders.product_id = products.product_id
"""

kpi_df = pd.read_sql(
    kpi_query,
    engine
)

print("\nBusiness KPIs:")
print(kpi_df)

kpi_df.to_csv(
    "reports/business_kpis.csv",
    index=False
)