import os
import pandas as pd
import json

#Function to import to CSV File, check if the file is exists first
#Then checks for other errors before returning CSV as dataframe

def csv_loader(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File Not Found {csv_path}")
    
    try:
        csv_df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        raise ValueError("File Is Empty or Invalid")
    except pd.errors.ParseError:
        raise ValueError("CSV file is corrupt or malformed")
    except OSError:
        raise OSError("File cannot be read")
    
    return csv_df

def json_loader(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"File Not Found {json_path}")
    
    try:
        with open(json_path, "r") as file:
            json_file = json.load(file)

        if isinstance(json_file, list):
            json_df = pd.DataFrame(json_file)
            return json_df
        
        elif isinstance(json_file, dict):
            
            for key, value in json_file.items():
                if isinstance(value, list):
                    json_df = pd.DataFrame(value)
                    break
            else:
                json_df = pd.json_normalize(json_file)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON file: {json_path}")
    except Exception as e:
            raise ValueError(f"Could not process JSON file: {e}")
    
    return json_df

def excel_loader(excel_path, sheet = 0):
    if not os.path.exsists(excel_path):
        raise FileNotFoundError(f"File Not Found {excel_path}")
    
    try:
        excel_df = pd.read_excel(excel_path, sheet, engine = "openpyxl")
    except ImportError:
        raise ValueError("Openpyxl Not Installed")
    except OSError:
        raise ValueError("File is Not Excel File")
        
    return excel_df