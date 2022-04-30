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
        print("USAGE: add-invite-url.py in_filename.json in_filename_link.json out_filename.json" )
        print("       Merge the invitation links from the in_filename_link.json file and in_filename.jsont and  save the result in out_filename.json")
        sys.exit(-1)

filename_data=sys.argv[1]
filename_link=sys.argv[2]
out_filename=sys.argv[3]

datas = json.load(open(filename_data))
links_in_array = json.load(open(filename_link))

links=to_dict(links_in_array)

for data in datas["data"]:
    name = data["name"]
    invite = ""
    url = ""
    if name in links:
        print("links, ", links[name])
        invite = links[name]["invite"]
        url = links[name]["url"]
    data["invite"] = invite
    data["url"] = url

# Add the missing entry name in the data schema
datas["schema"]["fields"].append({"name" : "invite", "type" : "string"})
datas["schema"]["fields"].append({"name" : "url", "type" : "string"})

with open(out_filename,"w") as outfile:
    outfile.write(json.dumps(datas, indent=4, sort_keys=True))
