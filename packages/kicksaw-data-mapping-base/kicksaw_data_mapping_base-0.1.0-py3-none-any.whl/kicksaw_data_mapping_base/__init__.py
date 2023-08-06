from functools import reduce
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import json
from pycm import get_config
from kicksaw_data_mapping_base.constants import defaults
import os

# TODO
# - validate header rows
# - provid option to download the sheet as a csv
# -


def get_sheet_data():
    config = get_config(os.getenv("STAGE"), use_dotenv=False, use_secrets=False)

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    path = Path("google-service-account.json")
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    worksheet_name = config.get("WORKSHEET_NAME")
    print(worksheet_name)
    sheet = client.open(worksheet_name)

    sheet_name = config.get("SHEET_NAME", defaults.SHEET_NAME)
    worksheet = sheet.worksheet(sheet_name)
    head = worksheet.get_all_records()[0].keys()
    print(head)
    return worksheet.get_all_records()
