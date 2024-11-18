# src/utils/file_handler.py

import pandas as pd

def load_csv(file):
    """
    Loads a CSV file into a DataFrame.
    
    Args:
        file: The uploaded CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded CSV data.
    """
    try:
        return pd.read_csv(file)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
