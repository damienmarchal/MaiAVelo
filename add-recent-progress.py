import json
import pandas
import sys

if len(sys.argv) != 4:
        print("USAGE: add-recent-progress.py in_filename_latest_data.json in_filename_reference_data.json out_filename.json" )
        print("       Compute the recent progression between 'latest' and 'reference' file and save the result in out_filename")
        sys.exit(-1)

filename_current_data=sys.argv[1]
filename_old_data=sys.argv[2]
out_filename=sys.argv[3]

current_data = json.load(open(filename_current_data))
old_data = json.load(open(filename_old_data))

for data in current_data["data"]:
    name = data["name"]
    progression_since_2_days = 0
    progression_since_7_days = 0
    data["progress_since_2_days"] = progression_since_2_days
    data["progress_since_7_days"] = progression_since_7_days

# Add the missing entry name in the data schema
current_data["schema"]["fields"].append({"name" : "progress_since_2_days", "type" : "string"})
current_data["schema"]["fields"].append({"name" : "progress_since_7_days", "type" : "string"})

with open(out_filename,"w") as outfile:
    outfile.write(json.dumps(current_data, indent=4, sort_keys=True))
