import duckdb
import os
import pandas as pd

def load_data_to_duckdb(db_path="blinkit.duckdb", folder="data/blinkit_sales"):
    """
    Loads all Blinkit CSV files from folder  DuckDB file.
    Each file is stored as a table (name cleaned from filename).
    """
    con = duckdb.connect(db_path)

    for f in os.listdir(folder):
        if f.endswith(".csv"):
            # normalize table name
            table_name = os.path.splitext(f)[0].replace("blinkit_", "").lower()
            file_path = os.path.join(folder, f)

            df = pd.read_csv(file_path)

            # persist to DuckDB
            con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            print(f"Loaded {f} : table {table_name} ({len(df)} rows, {len(df.columns)} cols)")

    # create a base transaction view (orders + items + products)
    con.execute("""
        CREATE OR REPLACE VIEW transactions_base AS
        SELECT
            o.order_id,
            o.customer_id,
            o.order_date,
            o.order_total,
            oi.product_id,
            oi.quantity,
            oi.unit_price,
            p.category,
            p.brand,
            p.price,
            p.mrp,
            p.margin_percentage
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
    """)
    print("Created view: transactions_base")

    con.close()


if __name__ == "__main__":
    load_data_to_duckdb()
