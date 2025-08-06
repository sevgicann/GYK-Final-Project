import os
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="soil_db",
    user="postgres",
    password="new.pass3",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

csv_folder = "csv_doc"

for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(csv_folder, file)
        table_name = os.path.splitext(file)[0].lower()

        print(f"Loading: {file_path} → Table: {table_name}")

        df = pd.read_csv(file_path)

        # Create the table (based on the header row)
        columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        cursor.execute(create_table_query)

        # Insert data into the table
        for i, row in df.iterrows():
            values = "', '".join([str(v).replace("'", "''") for v in row])
            insert_query = f"INSERT INTO \"{table_name}\" VALUES ('{values}');"
            cursor.execute(insert_query)

        conn.commit()

cursor.close()
conn.close()
print("All CSV files have been successfully loaded.")
