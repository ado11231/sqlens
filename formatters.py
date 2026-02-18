import pandas as pd
from tabulate import tabulate

# Prints a DataFrame as a formatted table, capped at limit rows
def format_output(df, limit = 50):
    if len(df) == 0:
        print("No Results")
        return
    
    if len(df) > limit:
        print(f"Showing {limit} of {len(df)} rows")
        df = df.head(limit)
    
    clean_output = tabulate(df, headers="keys", tablefmt="grid")
    
    print(clean_output)

# Exports query results to a file at the given path
def expo_results(df, path):
    

