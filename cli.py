import fire
import os
import shutil
from loaders import dispatcher
from database import DatabaseManager
from formatters import format_output, export_results


class CLI:
    # Sets up the CLI with a DatabaseManager instance
    def __init__(self):
        self.db = DatabaseManager()
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print("Created 'data' folder. Drop your files there to get started.")
    

    # Loads a file into the database, using the filename as the table name if none given
    def load(self, path, name = None, sheet = 0):
        path = os.path.expanduser(path)
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

    # Makes folder for datasets, if one has not been created
    def files(self):
        data_dir = "data"
        if not os.path.exists(self.data_dir):
            print("No data folder found. Create a 'data' folder and add files to it.")
            return
    
        for file in os.listdir(self.data_dir):
            print(file)

    # Adds datasets to the data folder
    def add(self, path):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            print(f"File Not Found {path}")
            return
        
        filename = os.path.basename(path)
        destination = os.path.join(self.data_dir, filename)
        shutil.copy(path, destination)
        print(f"Added {filename} to  data folder")

    def remove(self, filename):
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            print(f"File Not Found {filename}")
            return
        
        os.remove(path)
        print(f"Removed {filename} from data folder")

if __name__ == "__main__":
    fire.Fire(CLI)
        