import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from leakage_rules import run_leakage_checks

# --- Connect to DuckDB ---
@st.cache_resource
def get_connection():
    return duckdb.connect("blinkit.duckdb", read_only=True)

con = get_connection()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [])
category_filter = st.sidebar.text_input("Filter by Category (optional)")
brand_filter = st.sidebar.text_input("Filter by Brand (optional)")

# --- KPIs ---
st.title("📊 Revenue Leakage Dashboard")

orders_df = con.execute("SELECT * FROM orders").df()
transactions_df = con.execute("SELECT * FROM transactions_base").df()

total_orders = len(orders_df)
total_sales = orders_df["order_total"].sum()
avg_order_value = orders_df["order_total"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Sales", f"₹{total_sales:,.0f}")
col3.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")

# --- Revenue Leakage Findings ---
st.header("🚨 Revenue Leakage Checks")
findings = run_leakage_checks(con)

for rule, df in findings.items():
    st.subheader(rule.replace("_", " ").title())
    if df.empty:
        st.success("✅ No issues found")
    else:
        st.warning(f"⚠️ {len(df)} issues found")
        st.dataframe(df)

        # Export option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download {rule} CSV",
            data=csv,
            file_name=f"{rule}.csv",
            mime="text/csv"
        )

# --- Sales Trends ---
st.header("📈 Sales Trends")
if not orders_df.empty:
    fig = px.line(orders_df, x="order_date", y="order_total", title="Sales Over Time")
    st.plotly_chart(fig, use_container_width=True)

# --- Category Performance ---
st.header("📦 Category Performance")
if not transactions_df.empty:
    query = "SELECT category, SUM(order_total) as total_sales FROM transactions_base GROUP BY category"
    category_sales = con.execute(query).df()
    fig2 = px.bar(category_sales, x="category", y="total_sales", title="Sales by Category")
    st.plotly_chart(fig2, use_container_width=True)

# --- Brand Performance (with filter) ---
st.header("🏷️ Brand Performance")
brand_query = "SELECT brand, SUM(order_total) as total_sales FROM transactions_base GROUP BY brand"
brand_sales = con.execute(brand_query).df()

if brand_filter:
    brand_sales = brand_sales[brand_sales["brand"].str.contains(brand_filter, case=False)]

fig3 = px.bar(brand_sales, x="brand", y="total_sales", title="Sales by Brand")
st.plotly_chart(fig3, use_container_width=True)




# # app/dashboard.py

# import streamlit as st
# import duckdb
# import pandas as pd
# from leakage_rules import run_leakage_checks

# DB_PATH = "blinkit.duckdb"


# def main():
#     st.set_page_config(page_title="Blinkit Revenue Leakage Dashboard", layout="wide")

#     st.title(" Blinkit Revenue Leakage Dashboard")
#     st.markdown("Monitor and detect potential revenue leakages across operations.")

#     # Connect to DuckDB
#     con = duckdb.connect(DB_PATH, read_only=True)

#     # Run leakage rules
#     with st.spinner("Running leakage checks..."):
#         findings = run_leakage_checks(con)

#     # Tabs for each leakage rule
#     tabs = st.tabs(list(findings.keys()))

#     for tab, (rule_name, df) in zip(tabs, findings.items()):
#         with tab:
#             st.subheader(f" {rule_name.replace('_', ' ').title()}")
#             if df.empty:
#                 st.success(" No issues detected for this rule!")
#             else:
#                 st.warning(f" {len(df)} potential issues found")
#                 st.dataframe(df, use_container_width=True)

#                 # Export option
#                 csv = df.to_csv(index=False).encode("utf-8")
#                 st.download_button(
#                     label=" Download CSV",
#                     data=csv,
#                     file_name=f"{rule_name}.csv",
#                     mime="text/csv",
#                 )


# if __name__ == "__main__":
#     main()
