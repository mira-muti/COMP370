import csv
import os
from datetime import datetime

# calculates the monthly average response time (in hours) for every zip code
# and for all zip codes combined, in a single pass over the filtered dataset.
#
# output csv has form (zip,month,avg_response_time), where zip is "all" for
# the combined average. months with no incidents are left out.

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# zip -> list of 12 monthly sums of response times (hours)
hour_log = {"all": [0.0] * 12}
# zip -> list of 12 monthly incident counts
count_log = {"all": [0] * 12}

# use filtered dataset from data_collection.py
dataset_path = os.path.join(DATA_DIR, "311_filtered.csv")

with open(dataset_path, "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)

    # skip header line
    next(reader)

    for zipcode, start_str, end_str in reader:
        start = datetime.strptime(start_str, DATE_FORMAT)
        end = datetime.strptime(end_str, DATE_FORMAT)

        # response time in hours (not rounded)
        hours = (end - start).total_seconds() / 3600

        # an incident belongs to the month it was closed in
        month = end.month - 1

        if zipcode not in hour_log:
            hour_log[zipcode] = [0.0] * 12
            count_log[zipcode] = [0] * 12

        for key in (zipcode, "all"):
            hour_log[key][month] += hours
            count_log[key][month] += 1

output_path = os.path.join(DATA_DIR, "monthly_avg_response.csv")

with open(output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["zip", "month", "avg_response_time"])

    for key in sorted(hour_log):
        for m in range(12):
            # avoid dividing by 0: skip months with no incidents
            if count_log[key][m]:
                writer.writerow([key, MONTHS[m], hour_log[key][m] / count_log[key][m]])

print("///Finished Calculation///")
