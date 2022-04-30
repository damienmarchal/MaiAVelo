import json
import pandas
import sys

if len(sys.argv) != 3:
        print("USAGE: re-format-data-from-xls.py in_filename.xls out_filename.json" )
        print("       Remove private data from geovelo's provided file, and rename EPCI and toatal members column.")
        print("       The resulting content is saved into a json file.")
        sys.exit(-1)

in_filename=sys.argv[1]
out_filename=sys.argv[2]

dataframe = pandas.read_excel(in_filename)
dataframe = dataframe.drop(columns=["address", "postal_code", "publication_status", "top_user_nickname"])
dataframe = dataframe.rename(columns={
        "EPCI" : "epci",
        "toatal members" : "total_members"
    })
dataframe.to_json(out_filename, orient="table", indent=4)
