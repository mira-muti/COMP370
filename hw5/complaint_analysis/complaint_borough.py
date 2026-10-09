import argparse
import csv
import sys
from datetime import datetime


def comp_borough_count():
    # collecting command-line args
    p = argparse.ArgumentParser(
        description="Counts the number of each complaint type per borough for 311 "
                    "incidents created within a date range."
    )
    p.add_argument("-i", "--input", type=str, required=True, help="path to the input csv file")
    p.add_argument("-s", "--start", type=str, required=True,
                   help="the start date (DD/MM/YYYY) of the date filtering range (inclusive)")
    p.add_argument("-e", "--end", type=str, required=True,
                   help="the end date (DD/MM/YYYY) of the date filtering range (inclusive)")
    p.add_argument("-o", "--output", type=str, help="Optional: path to the output file (default: stdout)")
    args = p.parse_args()

    # convert dates to a datetime object for comparison
    try:
        sdate = datetime.strptime(args.start, "%d/%m/%Y")
        edate = datetime.strptime(args.end, "%d/%m/%Y")
    except ValueError:
        p.error("dates must be in DD/MM/YYYY format")

    # dictionary with key (complaint type, borough) and value = the number of occurrences
    count_log = {}

    with open(args.input, "r", encoding="utf-8", newline="") as f:
        # csv.reader handles quoted fields that contain commas
        reader = csv.reader(f)

        # find the columns by name instead of hardcoding their positions
        header = next(reader)
        created_col = header.index("Created Date")
        complaint_col = header.index("Complaint Type")
        borough_col = header.index("Borough")

        for feats in reader:
            # skip blank or cut-off lines
            if len(feats) <= max(created_col, complaint_col, borough_col):
                continue

            # convert the created date (no time) to a datetime object
            try:
                date = datetime.strptime(feats[created_col].split()[0], "%m/%d/%Y")
            except (ValueError, IndexError):
                continue

            # check if entry falls into date range
            if sdate <= date <= edate:
                key = (feats[complaint_col], feats[borough_col])
                count_log[key] = count_log.get(key, 0) + 1

    # decide where to output results
    if args.output:
        out = open(args.output, "w", encoding="utf-8", newline="")
    else:
        out = sys.stdout

    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["complaint type", "borough", "count"])

    for (complaint, borough), count in count_log.items():
        writer.writerow([complaint, borough, count])

    if args.output:
        out.close()

    # status message goes to stderr so it never ends up in the csv output
    print("///Finished Processing///", file=sys.stderr)


if __name__ == "__main__":
    comp_borough_count()
