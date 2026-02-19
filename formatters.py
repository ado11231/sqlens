import pandas as pd
import os
from rich.console import Console
from rich.table import Table


# Prints a DataFrame as a formatted table, capped at limit rows
def format_output(df, limit = 50):
    if len(df) == 0:
        print("No Results")
        return

    if len(df) > limit:
        print(f"Showing {limit} of {len(df)} rows")
        df = df.head(limit)

    console = Console()
    table = Table(show_lines=True)

    for column in df.columns:
        table.add_column(str(column))

    for index, row in df.iterrows():
        table.add_row(*[str(val) for val in row.tolist()])
        
    console.print(table)


# Exports query results to a file at the given path
def export_results(df, path):
    name, ext = os.path.splitext(path)

    if ext == ".csv":
        df.to_csv(path, index = False)
    elif ext == ".json":
        df.to_json(path)
    elif ext in (".xlsx", ".xls", ".xlsm"):
        df.to_excel(path, index = False)
    else:
        raise ValueError(f"Unsupported File Type {ext}")
    
    print(f"Saved to {path}")
    

    

