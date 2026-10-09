import argparse
from datetime import datetime

def comp_borough_count():
    # dictionary with key "complaint type,borough" and value = the number of occurances
    count_log = {}
    
    # collecting command-line args
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", type=str, help="path to the input csv file")
    p.add_argument("-s", "--start", type=str, help="the start date (DD/MM/YYYY) of the date filting range (inclusive)")
    p.add_argument("-e", "--end", type=str, help="the end date (DD/MM/YYYY) of the date filting range (inclusive)")
    p.add_argument("-o", "--output", type=str, help="Optional: path to the output file")
    args = p.parse_args()


    # convert dates to a datetime object for comparison
    sdate = datetime.strptime(args.start, "%d/%m/%Y")
    edate = datetime.strptime(args.end, "%d/%m/%Y")

    #"311_Service_Requests_from_2010_to_Present_20250928.csv"
    with open(args.input, "r", encoding="utf-8") as f:
        # skip processing the header line
        f.readline()

        line = f.readline()

        while line:
            feats = line.split(',')

            # convert the created_date (no time) to a datetime object
            date = datetime.strptime(feats[1].split()[0], "%m/%d/%Y")

            # check if entry falls into date range
            if (sdate <= date) and (date <= edate):
                key = f"{feats[5]},{feats[16]}"

                # update the count log
                if count_log.get(key):
                        count_log[key] += 1
                        
                else: #new (complaint type,borough)
                    count_log[key] = 1
                    
            line = f.readline()


    # decide where to output results
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("complaint type,borough,count\n")

            for key in count_log:
                f.write(f"{key},{count_log[key]}\n")
                
    else:
        print("complaint type,borough,count")
        
        for key in count_log:
                print(f"{key},{count_log[key]}")

    print("///Finished Processing///")

if __name__ == "__main__":
    comp_borough_count()
