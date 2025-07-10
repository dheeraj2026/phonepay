# scripts/queries.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("db/phonepe.db")

# Example Query 1: Total amount per year
query1 = """
SELECT year, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY year
ORDER BY year;
"""
df1 = pd.read_sql_query(query1, conn)
print(df1)

# Plotting
plt.figure(figsize=(10,5))
plt.plot(df1['year'], df1['total_amount'], marker='o', color='purple')
plt.title("📈 Total Transaction Amount per Year")
plt.xlabel("Year")
plt.ylabel("Amount (INR)")
plt.grid(True)
plt.tight_layout()
plt.show()

conn.close()
