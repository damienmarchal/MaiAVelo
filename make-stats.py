"""
    Make statistics for the member count and kilometric progression grouped
    by a given field provided as first argument.
"""
import json
import pandas
import sys
import pprint

if len(sys.argv) != 4:
        print("USAGE: make-stats.py fieldname in_filename.json out_filename.json" )
        sys.exit(-1)

fieldname = sys.argv[1]
in_filename=sys.argv[2]
out_filename=sys.argv[3]

dataframe = pandas.read_json(in_filename, orient="table")
dataframe = dataframe[[fieldname, "total_members", "progress"]]
datasum = dataframe.groupby(fieldname).sum()

datasum.to_json(out_filename, indent=4, orient="table")
