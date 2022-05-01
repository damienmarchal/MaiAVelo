import json
import sys

if len(sys.argv) != 3:
        print("USAGE: remove-city-from-data.py infile.json outfile.json" )
        sys.exit(-1)

in_filename=sys.argv[1]
out_filename=sys.argv[2]

data = json.load(open(in_filename))

for entry in data["data"]:
    del entry["city"]

data["schema"]["fields"].remove({"name" : "city", "type" : "string"})

with open(out_filename,"w") as outfile:
    outfile.write(json.dumps(data, indent=4, sort_keys=True))
