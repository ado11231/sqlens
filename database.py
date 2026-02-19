import sqlite3
import os
import re
import pandas as pd
from pathlib import Path

class DatabaseManager:
    # Initializes the DatabaseManager and opens a connection
    def __init__(self, db_path="copydata.db"):
        self.db_path = db_path
        self._connect()

    # Opens the SQLite connection to the database file
    def _connect(self):
        self.con = sqlite3.connect(self.db_path)

    # Allows use as a context manager (with statement)
    def __enter__(self):
        return self

    # Closes the connection when exiting the context manager
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    # Sanitizes a string into a valid SQLite table name
    def _clean_table_name(self, name):
        if not name:
            return "unnamed_table"

        name, ext = os.path.splitext(name)
        name = name.lower().replace(" ","_").replace("-","_")

        name = re.sub(r"[^a-z0-9_]", "", name)

        if name[0].isdigit():
            name = "table_" + name 
        
        return name

    # Loads a pandas DataFrame into the database as a table
    def load_dataframe(self, name, df: pd.DataFrame):
        if df.empty:
            print("Dataframe Empty")
            return
        
        clean = self._clean_table_name(name)

        try:
            df.to_sql(name = clean, con = self.con, if_exists = "replace", index = False)
            return {
            "Table Name": clean,
            "Rows": len(df),
            "Columns": len(df.columns)
        }
        except sqlite3.OperationalError as e:
            print(e)
            return

    def run_query(self, query):
        try:
            result = pd.read_sql_query(query, self.con)
            return result
        except (sqlite3.OperationalError, pd.errors.DatabaseError) as e:
            print(e)
            return

    def list_tables(self):
        cursor = self.con.execute("SELECT name FROM sqlite_master WHERE type='table' ")
        tables = cursor.fetchall()

        results = []

        for table in tables:
            table_name = table[0]

            cursor = self.con.execute(f"SELECT COUNT (*) FROM {table_name}")
            row = cursor.fetchone()[0]

            cursor = self.con.execute(f"PRAGMA table_info({table_name})")
            column_info = cursor.fetchall()

            columns = []
            for col in column_info:
                columns.append(col[1])


            results.append({
                "name": table_name,
                "rows": row,
                "columns": columns
            })

        return results
    
    def drop_table(self, table_name):
        try:
            clean_name = self._clean_table_name(table_name)
            cursor = self.con.execute(f"DROP TABLE IF EXISTS {clean_name}")
            self.con.commit()
        except sqlite3.OperationalError as e:
            print(e)
            return "Dropped" , table_name




 


            

