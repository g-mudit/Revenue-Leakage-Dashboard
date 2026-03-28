# Business Finance & Revenue Risk Analytics Platform
Uncover hidden revenue losses and empower data-driven decisions with an end-to-end analytics solution for e-commerce sales data.
This production-ready project provides a robust framework to detect revenue leakages (mispricing, duplicates, inventory shrinkage, delivery issues) and delivers an interactive Streamlit dashboard for triage, drill-down, and export. Built with modularity and scalability in mind, it combines automated data ingestion, rule-based leakage detection, and rich visualizations to help business teams, analysts, and decision-makers optimize operations and recover lost revenue.

## ✨ Features

Automated Data Ingestion: Seamlessly loads sales data from CSV files into a DuckDB database, creating a unified transactions_base view for analysis.
Revenue Leakage Detection: Identifies inefficiencies like misapplied discounts, invalid orders, duplicate transactions, inventory shrinkage, and delayed deliveries using SQL-based rules.
Interactive Streamlit Dashboard:
KPI Cards: Total Revenue, Orders, Avg. Order Value, Flagged Issues, Estimated Leakage.
Dynamic Filters: Filter by date range, product categories, or stores.
Visualizations: Sales trends, leakage by rule, category/brand performance with Plotly charts.
Rule-Specific Tabs: Drill down into flagged issues with interactive tables and export findings as CSV/Excel.


Modular Architecture: Easily extend with new rules, charts, or KPIs.
Exportable Insights: Download filtered data for business reporting or further analysis.


##📂 Project Structure
Analyst_Dashboard/
├── dashboard.py                    # Streamlit dashboard for visualization and triage
├── data_loader.py                 # Loads CSVs into DuckDB and creates transactions_base view
├── leakage_rules.py               # SQL-based revenue leakage detection rules
├── data/
│   └── sales/                     # Folder for sales CSV files
│       ├── orders.csv
│       ├── order_items.csv
│       ├── products.csv
│       ├── customers.csv
│       ├── delivery_performance.csv
│       └── ... (other CSVs)
├── analytics.duckdb               # DuckDB database (auto-generated)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation


##🚀 Getting Started
Prerequisites

Python 3.8+
Git
DuckDB, Streamlit, Plotly, and other dependencies (listed in requirements.txt)

##Installation

###Clone the repository:
git clone [https://github.com/g-mudit/revenue-leakage-detection.git](https://github.com/g-mudit/Revenue-Leakage-Dashboard.git) <\br>
cd revenue-leakage-detection


Install dependencies:
pip install -r requirements.txt


Prepare data:

Place your sales CSV files (e.g., orders.csv, products.csv) in the data/sales/ folder.


Load data into DuckDB:
python data_loader.py

This creates the analytics.duckdb database and the transactions_base view.

Launch the dashboard:
streamlit run dashboard.py

Open the provided URL (e.g., http://localhost:8501) in your browser to explore the dashboard.



## 🧩 Components
1. Data Loader (data_loader.py)

Purpose: Reads CSV files from data/sales/ and persists them into DuckDB tables (orders, order_items, products, etc.).
Key Output: Creates a transactions_base view by joining orders, items, and product metadata for seamless analysis.
Run: python data_loader.py

2. Revenue Leakage Rules (leakage_rules.py)

Purpose: Applies SQL-based rules to detect revenue leakages, including:
Misapplied Discounts: unit_price < 50% of MRP
Invalid Order Totals: Orders with zero or negative totals
Duplicate Orders: Same customer, total, and date
Inventory Shrinkage: Damaged stock > 20% of received stock
Delayed Deliveries: Actual delivery time exceeds promised time


Run: python leakage_rules.py

3. Interactive Dashboard (dashboard.py)

Purpose: A Streamlit-powered UI for exploring KPIs, trends, and leakage details.
## Features:
📊 KPIs: Total orders, sales, average order value, flagged issues, estimated leakage.
🚨 Leakage Analysis: Rule-specific tabs with interactive tables and export options.
📈 Trends: Sales over time, leakage trends, category/brand performance.
📦 Filters: Date range, product categories, stores.


Run: streamlit run dashboard.py


## 💡 Why This Project?

For Business Teams: Quickly identify and address revenue losses from pricing errors, fraud, or operational inefficiencies.
For Data Analysts: Centralized DuckDB tables enable custom queries and deeper exploration.
For Developers: Modular design makes it easy to add new rules, visualizations, or integrations.
For Decision Makers: Intuitive dashboards with exportable insights support strategic decision-making.


## 🔮 Future Enhancements

Multi-page dashboard for dedicated Sales, Inventory, Delivery, and Customer views.
Automated alerts (email/Slack) for high-impact leakage events.
Real-time data integration for live monitoring.
ML-based anomaly detection to complement rule-based checks.


## 👨‍💻 Author

Developed by Mudit Gaur

