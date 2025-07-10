# scripts/extract_transform_load.py
print("✅ Script is running")

import os
import json
import sqlite3

# Define paths
DB_PATH = "db/phonepe.db"
TRANSACTION_PATH = "data/aggregated/transaction/country/india"


# Connect to DB and create table
def create_connection_and_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aggregated_transaction (
            state TEXT,
            year INTEGER,
            quarter INTEGER,
            transaction_type TEXT,
            count INTEGER,
            amount REAL
        );
    ''')
    conn.commit()
    return conn

# Process one JSON file
def process_file(file_path, state, year, quarter):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        records = []
        for item in data.get("data", {}).get("transactionData", []):
            name = item.get("name")
            pi = item.get("paymentInstruments", [{}])[0]
            count = pi.get("count", 0)
            amount = pi.get("amount", 0.0)
            records.append((state, int(year), int(quarter), name, count, amount))

        return records
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

# Load all JSONs and insert into DB
def load_all_data(conn):
    cursor = conn.cursor()

    for year in os.listdir(TRANSACTION_PATH):
        year_path = os.path.join(TRANSACTION_PATH, year)
        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = file.strip(".json")
                file_path = os.path.join(year_path, file)
                print(f"📥 Loading: {file_path}")
                records = process_file(file_path, "India", year, quarter)
                cursor.executemany('''
                    INSERT INTO aggregated_transaction
                    VALUES (?, ?, ?, ?, ?, ?);
                ''', records)

    conn.commit()
s

if __name__ == "__main__":
    print("🚀 ETL started...")
    conn = create_connection_and_tables()
    load_all_data(conn)
    conn.close()
    print("✅ ETL finished. Data loaded into db/phonepe.db")
