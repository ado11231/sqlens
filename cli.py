import fire
import os
from loaders import dispatcher
from database import DatabaseManager

class CLI:
    def __init__(self):
        self.db = DatabaseManager()

    def load(self, path, name = None, sheet = 0):
        if name is None:
            name = os.path.basename(path)

        df = dispatcher(path, sheet)
        result = self.db.load_dataframe(name, df)
        print(f"Loaded '{result['Table Name']}' ({result['Rows']} rows, {result['Columns']} columns)")        


    def query(self, query):
        df = self.db.run_query(query)
        print(df)


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

    def drop (self, table_name):
        result = self.db.drop_table(table_name)
        print(f"{result} dropped")

    def reset(self):
        self.db.reset()

if
        
if __name__ == "__main__":
    fire.Fire(CLI)
        