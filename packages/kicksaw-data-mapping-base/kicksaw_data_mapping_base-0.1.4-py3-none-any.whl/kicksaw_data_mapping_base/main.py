import os

import gspread

from pathlib import Path

from gspread.models import Worksheet

from oauth2client.service_account import ServiceAccountCredentials

from pycm import get_config

from kicksaw_data_mapping_base.constants import columns, defaults, scopes


def get_sheet_data():
    config = get_config(os.getenv("STAGE"), use_dotenv=False, use_secrets=False)

    scope = [
        scopes.SPREADSHEETS_FEED,
        scopes.AUTH_DRIVE,
    ]

    path = Path("google-service-account.json")
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    worksheet_name = config.get("WORKSHEET_NAME")
    sheet = client.open(worksheet_name)

    sheet_name = config.get("SHEET_NAME", defaults.SHEET_NAME)
    worksheet = sheet.worksheet(sheet_name)

    _validate_columns(worksheet=worksheet)
    return worksheet.get_all_records()


def _validate_columns(worksheet: Worksheet) -> None:
    head = worksheet.get_all_records()[0].keys()
    # https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
    result = all(elem in head for elem in columns.ALL)

    assert (
        result
    ), f"Missing Columns in spreadsheet.  Expected {columns.ALL} to exist in {head}"
