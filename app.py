import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to SQLite DB (adjusted path for deployment)
conn = sqlite3.connect("db/phonepe.db")

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")
st.title("📊 PhonePe Transactions Dashboard")

# --- Sidebar ---
st.sidebar.header("🔍 Filter")
years = pd.read_sql_query("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year", conn)
selected_year = st.sidebar.selectbox("Select Year", years["year"])

# --- KPIs ---
col1, col2 = st.columns(2)

# Total transaction amount
query_amount = "SELECT SUM(amount) AS total_amount FROM aggregated_transaction WHERE year = ?"
total_amount = pd.read_sql_query(query_amount, conn, params=[selected_year])
col1.metric("💰 Total Transaction Amount", f"₹ {total_amount.iloc[0]['total_amount']:.2f}")

# Total transaction count
query_count = "SELECT SUM(count) AS total_count FROM aggregated_transaction WHERE year = ?"
total_count = pd.read_sql_query(query_count, conn, params=[selected_year])
col2.metric("🔄 Total Transactions", f"{int(total_count.iloc[0]['total_count']):,}")

# --- Bar Chart: Transaction Amount by Type ---
query_type = """
SELECT transaction_type, SUM(amount) AS amount
FROM aggregated_transaction
WHERE year = ?
GROUP BY transaction_type
"""
df_type = pd.read_sql_query(query_type, conn, params=[selected_year])
fig1 = px.bar(df_type, x="transaction_type", y="amount", title="Amount by Transaction Type", color="transaction_type")
st.plotly_chart(fig1, use_container_width=True)

# --- Line Chart: Quarterly Trends ---
query_quarter = """
SELECT quarter, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE year = ?
GROUP BY quarter
ORDER BY quarter
"""
df_quarter = pd.read_sql_query(query_quarter, conn, params=[selected_year])
fig2 = px.line(df_quarter, x="quarter", y="total_amount", markers=True, title="📈 Quarterly Transaction Trend")
st.plotly_chart(fig2, use_container_width=True)

# --- Top 5 States by Transaction Amount ---
query_states = """
SELECT state, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE year = ?
GROUP BY state
ORDER BY total_amount DESC
LIMIT 5
"""
df_states = pd.read_sql_query(query_states, conn, params=[selected_year])
fig3 = px.bar(df_states, x="state", y="total_amount", title="🏆 Top 5 States by Amount", color="state")
st.plotly_chart(fig3, use_container_width=True)

# --- Pie Chart ---
fig4 = px.pie(df_type, names='transaction_type', values='amount', title='🧁 Transaction Type Distribution')
st.plotly_chart(fig4, use_container_width=True)

conn.close()
