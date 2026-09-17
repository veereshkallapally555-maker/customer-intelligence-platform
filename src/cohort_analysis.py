import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

engine = create_engine("sqlite:///data/db/customer_intelligence.db")

query = """
WITH customer_cohorts AS (
    SELECT
        customer_id,
        strftime('%Y-%m', MIN(order_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
)

SELECT
    orders.customer_id,
    customer_cohorts.cohort_month,
    strftime('%Y-%m', orders.order_date) AS activity_month
FROM orders
JOIN customer_cohorts
    ON orders.customer_id = customer_cohorts.customer_id
"""

df = pd.read_sql(query, engine)

df = df.drop_duplicates()

retention = pd.crosstab(
    df["cohort_month"],
    df["activity_month"]
)

cohort_sizes = retention.max(axis=1)

retention_rate = retention.div(
    cohort_sizes,
    axis=0
) * 100

print(retention_rate.round(2))

plt.figure(figsize=(14, 8))

sns.heatmap(
    retention_rate,
    annot=True,
    fmt=".1f"
)

plt.title("Customer Cohort Retention (%)")
plt.xlabel("Activity Month")
plt.ylabel("Cohort Month")
plt.tight_layout()

plt.show()