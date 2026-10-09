import os
import argparse
from datetime import datetime

#filters the 311 dataset to only include entries:
#   - opened in 2024
#   - has a closed date
#   - closed date > created date
#   - has a zip code
# outputed csv file has form (zip,start_date,end_date)

def is_int(s):
   # check if a string is an int
    try:
        s = int(s)
        return True

    except ValueError as e:
        return False


p = argparse.ArgumentParser()
p.add_argument("input", type=str, help="path to 311 service csv file")
args = p.parse_args()


output = open(os.path.abspath("../data/311_filtered.csv"), "w", encoding="utf-8")
output.write("zip,start_date,end_date\n")

with open(args.input, "r", encoding="utf-8") as f:
    # skip processing the header line
    f.readline()

    line = f.readline()

    while line:
        feats = line.split(',')

        # check if have closed date + zip
        if (feats[2] != "") and (feats[8] !="") and is_int(feats[8]):
            start = datetime.strptime(feats[1], "%m/%d/%Y %I:%M:%S %p")
            end = datetime.strptime(feats[2], "%m/%d/%Y %I:%M:%S %p")

            #check if start is in 2020 and end > start
            if (start.year == 2024) and (start < end):
                output.write(f"{feats[8]},{feats[1]},{feats[2]}\n")

        line = f.readline()

output.close()

print("///Finsihed Filtering///")
