import json
import pandas
import sys
import pprint

def to_dict(array):
    out = {}
    for entry in array:
        out[entry["name"]] = entry
    return out

if len(sys.argv) != 4:
        print("USAGE: add-updated-data.py in_base_data_filename.json in_updateddata_filename.json out_filename.json" )
        sys.exit(-1)

filename_data=sys.argv[1]
filename_updates=sys.argv[2]
out_filename=sys.argv[3]

data = json.load(open(filename_data))
updated_data = json.load(open(filename_updates))
updated_data = to_dict(updated_data["data"])

old_data_as_dict = to_dict(data["data"])

# Change the content of the data dictionnary.
for entry in data["data"]:
    name = entry["name"]
    if name in updated_data:
        k = updated_data[name]["km"]
        if isinstance(k, str) and k[-3:] == " km":
            k = k[:-3]
            k = int(k.replace(" ",""))
        if k > int(entry["progress"]):
            entry["progress"] = k

for k,v in updated_data.items():
    if k not in old_data_as_dict:
        #print("NEW TEAM: ", k, v)
        k = v["km"]
        if isinstance(k, str) and k[-3:] == " km":
            k = k[:-3]
            k = k.replace(" ","")

        data["data"].append({
            "department": "",
            "epci": v["epci"],
            "group_id": 0,
            "index": 0,
            "invite": "",
            "is_local": "",
            "name": v["name"],
            "progress": k,
            "progress_since_2_days": 0,
            "progress_since_7_days": 0,
            "region": v["region"],
            "city" : "",
            "size_range": "?",
            "top_user_progress": "",
            "total_members": 0,
            "type": v["category"],
            "url": ""
        })

with open(out_filename,"w") as outfile:
    outfile.write(json.dumps(data, indent=4, sort_keys=True))
