import fire
import os
from loaders import dispatcher
from database import DatabaseManager
from formatters import format_output, export_results

class CLI:
    # Sets up the CLI with a DatabaseManager instance
    def __init__(self):
        self.db = DatabaseManager()

    # Loads a file into the database, using the filename as the table name if none given
    def load(self, path, name = None, sheet = 0):
        if name is None:
            name = os.path.basename(path)

        df = dispatcher(path, sheet)
        result = self.db.load_dataframe(name, df)
        print(f"Loaded '{result['Table Name']}' ({result['Rows']} rows, {result['Columns']} columns)")        


    # Runs a SQL query and prints the result
    def query(self, query, output = None):
        df = self.db.run_query(query)
        
        if output:
            export_results(df,output)
        else:
            format_output(df)


    # Lists all tables in the database with their row and column info
    def tables(self):
        data_table = self.db.list_tables()

        if not data_table:
            print("No Tables Found")
        else:
            for table in data_table:
                name = table["name"]
                rows = table["rows"]
                columns = ", ".join(table["columns"])
                print(f"{name}: {rows} rows | columns: {columns}")

    # Drops the specified table from the database
    def drop (self, clean_name):
        result = self.db.drop_table(clean_name)
        print(f"{result} dropped")

    # Resets the database
    def reset(self):
        self.db.reset()

if __name__ == "__main__":
    fire.Fire(CLI)
        