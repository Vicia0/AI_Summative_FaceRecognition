import csv
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def upload_to_google_sheets(filename):
    # Load the credentials
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, SCOPES)

    # Build the Google Sheets API client
    service = build('sheets', 'v4', credentials=creds)

    # Create a new Google Sheet
    spreadsheet = {
        'properties': {
            'title': os.path.splitext(filename)[0]
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    print(F'Created new spreadsheet with ID: {spreadsheet.get("spreadsheetId")}')

    # Read the attendance data from the CSV file
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    # Upload the attendance data to the Google Sheet
    body = {
        'values': data
    }
    sheet_id = spreadsheet.get("spreadsheetId")
    range_name = 'Sheet1!A1'
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print(f'Updated {result.get("updatedCells")} cells in the Google Sheet')

if __name__ == "__main__":
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'attendance.csv'
    upload_to_google_sheets(filename)
