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
    ON orders.product_id = products.product_id;