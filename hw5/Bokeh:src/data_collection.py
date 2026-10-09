import os
import csv
import argparse
from datetime import datetime

# filters the 311 dataset to only include entries:
#   - opened in 2024
#   - has a closed date
#   - closed date > created date
#   - has a (5 digit) zip code
# outputted csv file has form (zip,start_date,end_date)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"

p = argparse.ArgumentParser(description="Filters the 311 csv down to what the dashboard needs.")
p.add_argument("input", type=str, help="path to 311 service csv file")
args = p.parse_args()

output_path = os.path.join(DATA_DIR, "311_filtered.csv")

with open(args.input, "r", encoding="utf-8", newline="") as f, \
     open(output_path, "w", encoding="utf-8", newline="") as output:

    # csv.reader handles quoted fields that contain commas
    reader = csv.reader(f)
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["zip", "start_date", "end_date"])

    # find the columns by name instead of hardcoding their positions
    header = next(reader)
    created_col = header.index("Created Date")
    closed_col = header.index("Closed Date")
    zip_col = header.index("Incident Zip")

    for feats in reader:
        # skip blank or cut-off lines
        if len(feats) <= max(created_col, closed_col, zip_col):
            continue

        zipcode = feats[zip_col].strip()

        # check if have closed date + a valid zip
        if feats[closed_col] == "" or len(zipcode) != 5 or not zipcode.isdigit():
            continue

        try:
            start = datetime.strptime(feats[created_col], DATE_FORMAT)
            end = datetime.strptime(feats[closed_col], DATE_FORMAT)
        except ValueError:
            continue

        # check if start is in 2024 and end > start
        if (start.year == 2024) and (start < end):
            writer.writerow([zipcode, feats[created_col], feats[closed_col]])

print("///Finished Filtering///")
