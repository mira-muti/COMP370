import argparse
from datetime import datetime
import os

DATA_DIR = os.path.abspath("../data")

# calculates the monthly average response time 
p = argparse.ArgumentParser()
p.add_argument("--zip", type=int, help="Optional: zip code to filter by")
args = p.parse_args()

# check if given a valid zip code
if args.zip and (args.zip < 10000) and (args.zip > 99999):
    print("Error: Given zip code must be in [10000, 99999]")

else:
    # counts the number of incidents opened in each month
    count_log = {"Jan":0,
                 "Feb":0,
                 "Mar":0,
                 "Apr":0,
                 "May":0,
                 "Jun":0,
                 "Jul":0,
                 "Aug":0,
                 "Sep":0,
                 "Oct":0,
                 "Nov":0,
                 "Dec":0}

    # monthly sum of reponse times from incidents opened in each month
    hour_log = {"Jan":0,
                 "Feb":0,
                 "Mar":0,
                 "Apr":0,
                 "May":0,
                 "Jun":0,
                 "Jul":0,
                 "Aug":0,
                 "Sep":0,
                 "Oct":0,
                 "Nov":0,
                 "Dec":0}

    #use filtered dataset from data_collection.py
    dataset_path = os.path.join(DATA_DIR, "311_filtered.csv")

    with open(dataset_path, "r", encoding="utf-8") as f:
        # skip header line
        f.readline()

        line = f.readline()
        
        while line:
            feats = line.strip().split(',')

            # if given a zip code, ingore entries with mismatch zips
            if args.zip and (int(feats[0]) != args.zip):
                line = f.readline()
                continue

            # calculate response time in hours
            start = datetime.strptime(feats[1], "%m/%d/%Y %I:%M:%S %p")
            end = datetime.strptime(feats[2], "%m/%d/%Y %I:%M:%S %p")

            res_time = end - start
            hours = res_time.total_seconds() // 3600

            # add info to the logs
            month = start.strftime("%b")
            hour_log[month] += hours
            count_log[month] += 1

            line = f.readline()

    # calculate average response time by month and output to a file
    if args.zip:
        # change path to put in a directory (ReponseData)
        output = os.path.join(DATA_DIR, f"{args.zip}_mon_avg_reponse.csv")
    else:
        output = os.path.join(DATA_DIR, "all_mon_avg_reponse.csv")

    with open(output, "w") as f:
        f.write("month,avg_reponse_time\n")

        for key in count_log:
            if count_log[key]:
                avg = hour_log[key] / count_log[key]
                f.write(f"{key},{avg}\n")

            else: # avoid dividing by 0
                f.write("0,0\n")
    print("///Finished Calculation///")

