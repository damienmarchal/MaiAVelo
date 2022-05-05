import json
import pandas
import sys
import pprint
import datetime

from os import listdir
from os.path import isfile, join

def clean_km(d):
    if isinstance(d, str) and d[-3:] == " km":
        d = d[:-3]
        d = int(d.replace(" ",""))
    return d

def to_dict(array):
    out = {}
    for entry in array:
        out[entry["name"]] = entry
    return out

def findClosestEntry(date, dataset):
    selectedEntry = dataset[0]
    selectedDelta = abs(datetime.timedelta(weeks=16).total_seconds())
    for entry in dataset:
        if(isinstance(entry["date"], str)):
            ddate = datetime.datetime.strptime(entry["date"], "%Y-%m-%dT%H:%M:00")
        else:
            ddate = entry["date"]

        dt = abs((ddate-date).total_seconds())
        if dt < selectedDelta:

            selectedDelta = dt
            selectedEntry = entry
    return selectedEntry

if len(sys.argv) != 4:
        print("USAGE: add-updated-data.py in_basedata_dir mel_old_data.json out_filename.json" )
        sys.exit(-1)

datapath = sys.argv[1]
mel_old_data=sys.argv[2]
out_filename=sys.argv[3]

## Load all the files.
filenames = sorted([f for f in listdir(datapath) if isfile(join(datapath, f)) and f.startswith("formatted-dump-22")])
db = []
for filename in filenames:
    print("Processing file: ", filename)
    data = to_dict(json.load(open(join(datapath, filename),"r"))["data"])
    date = datetime.datetime.strptime(filename, "formatted-dump-%y-%m-%d_%H-%M.json")
    km = clean_km(data["Métropole Européenne de Lille"]["km"])
    db.append(
        {
            "date":date,
            "progress":km
        }
    )

# compute the first time
date = datetime.datetime.strptime("2022-04-30_11-59", "%Y-%m-%d_%H-%M")

## Load CMV progression 2022
cmvdb = json.load(open(mel_old_data,"r"))["data"]
incrdate = datetime.timedelta(weeks=52, days=1)
for entry in cmvdb:
    entry["date"] = datetime.datetime.strptime(entry["date"], "%Y-%m-%dT%H:%M:00")+incrdate

outdata = []
for i in range(0,32):
    print("Processing ", date.strftime("%Y-%m-%dT%H:%M:00"))

    entry = findClosestEntry(date, db)
    cmventry = findClosestEntry(date, cmvdb)
    print(entry)
    print(cmventry)

    p = {
        "date" : date.strftime("%Y-%m-%dT%H:%M:00"),
        "progress-2022" : entry["progress"] ,
        "progress-2021" : cmventry["totalKmInsideBoundary"],
        "progress-2020" : cmventry["totalKmInsideBoundaryPreviousYear"]
    }

    outdata.append(p)
    if date >= datetime.datetime.now():
        break

    date = date + datetime.timedelta(days=1)
        
with open(out_filename,"w") as outfile:
    outfile.write(json.dumps(
        {"data" : outdata},
        indent=4, sort_keys=True))
