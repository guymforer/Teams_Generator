import gspread
from oauth2client.service_account import ServiceAccountCredentials

def export_participants():
    # Set up credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by title
    sheet_url = "https://docs.google.com/spreadsheets/d/1jfH0on92qA73FI_EacvjYH-EdeL1UfFYy-dglkm8wf4/edit?resourcekey#gid=11662411"
    sheet = client.open_by_url(sheet_url).worksheet("Participants")

    # Get all values from the sheet
    data = sheet.get_all_values()

    # Specify the text file path
    text_file_path = "participants.txt"

    # Write data to the text file
    with open(text_file_path, "w") as text_file:
        for row in data:
            text_file.write(",".join(row) + "\n")

    print(f"Data exported to {text_file_path}")
