import duckdb

def run_leakage_checks(con):
    results = {}

    # 1. Misapplied Discounts (unit_price < 50% of MRP)
    q1 = """
        SELECT 
            t.order_id, t.product_id, t.unit_price, t.mrp, t.quantity,
            (t.mrp - t.unit_price) * t.quantity AS discount_loss
        FROM transactions_base t
        WHERE t.unit_price < t.mrp * 0.5
    """
    results["misapplied_discounts"] = con.execute(q1).df()

    # 2. Negative or Zero Order Totals
    q2 = """
        SELECT order_id, customer_id, order_total
        FROM orders
        WHERE order_total <= 0
    """
    results["invalid_order_totals"] = con.execute(q2).df()

    # 3. Duplicate Orders (same customer, same amount, same day)
    q3 = """
        SELECT customer_id, order_date, order_total, COUNT(*) as duplicate_count
        FROM orders
        GROUP BY customer_id, order_date, order_total
        HAVING COUNT(*) > 1
    """
    results["duplicate_orders"] = con.execute(q3).df()

    # 4. Inventory Shrinkage (damaged stock > 20% of received)
    q4 = """
        SELECT product_id, date, stock_received, damaged_stock,
               damaged_stock * 1.0 / NULLIF(stock_received,0) AS shrinkage_ratio
        FROM inventory
        WHERE stock_received > 0 
          AND damaged_stock > stock_received * 0.2
    """
    results["inventory_shrinkage"] = con.execute(q4).df()

    # 5. Delayed Deliveries (actual_time > promised_time)
    q5 = """
        SELECT order_id, promised_time, actual_time, delivery_time_minutes, reasons_if_delayed
        FROM delivery_performance
        WHERE actual_time > promised_time
    """
    results["delayed_deliveries"] = con.execute(q5).df()

    return results


if __name__ == "__main__":
    con = duckdb.connect("blinkit.duckdb")
    findings = run_leakage_checks(con)

    print("\n=== Revenue Leakage Findings ===\n")
    for rule, df in findings.items():
        print(f"\n--- {rule} ---")
        if df.empty:
            print("No issues found")
        else:
            print(df.head(10))  # show first 10 for preview
