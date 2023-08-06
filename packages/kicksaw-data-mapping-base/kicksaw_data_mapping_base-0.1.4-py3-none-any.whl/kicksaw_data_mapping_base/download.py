import csv

from kicksaw_data_mapping_base.main import get_sheet_data


def download_as_csv(filename: str):
    sheet_data = get_sheet_data()

    column_names = sheet_data[0].keys()
    with open(filename, "w", newline="") as file:
        w = csv.DictWriter(file, column_names)
        w.writeheader()
        for row in sheet_data:
            w.writerow(row)
