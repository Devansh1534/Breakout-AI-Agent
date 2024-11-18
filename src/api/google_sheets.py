# src/api/google_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_google_sheets(credentials_path, sheet_name):
    """
    Connects to a Google Sheet and retrieves its data as a DataFrame.
    
    Args:
        credentials_path (str): Path to the JSON credentials file for Google Sheets API.
        sheet_name (str): Name of the Google Sheet.

    Returns:
        pd.DataFrame: Data from the Google Sheet as a DataFrame.
    """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None

def update_google_sheets(credentials_path, sheet_name, data_frame):
    """
    Updates a Google Sheet with new data from a DataFrame.
    
    Args:
        credentials_path (str): Path to the JSON credentials file for Google Sheets API.
        sheet_name (str): Name of the Google Sheet.
        data_frame (pd.DataFrame): DataFrame containing the data to update.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name).sheet1
        sheet.clear()  # Clear existing data
        sheet.update([data_frame.columns.values.tolist()] + data_frame.values.tolist())
        return True
    except Exception as e:
        print(f"Error updating Google Sheets: {e}")
        return False
