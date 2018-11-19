"""
Written for a request from my brother to collate contact information for
Advanced Practice Registered Nurses (ARNPs) in the Miami area, using public
data from https://appsmqa.doh.state.fl.us/downloadnet/Licensure.aspx
"""
from pprint import pprint
import uszipcode

zipsearch = uszipcode.SearchEngine()
TARGETZIPS = [res.zipcode for res in zipsearch.by_city("miami")]

with open("arnp_data_fl.txt", "r") as f:
    lines = [l.strip() for l in f if l]

columns = [colname for colname in lines[0].split("|") if colname]
MAILZIP = next(key for key in columns if key.startswith("Mailing") and "ZIP" in key)
PRACZIP = next(key for key in columns if key.startswith("Practice") and "ZIP" in key)
data = [
    {k: col for k, col in zip(columns, line.split("|"))} for line in lines[1:] if line
]

filtered = [
    datum
    for datum in data
    if any(z in (datum[MAILZIP], datum[PRACZIP]) for z in TARGETZIPS)
]

print("Total records: %d" % len(data))
print("Number of records in Miami: %d" % len(filtered))

with open("miami_ARNPs.txt", "w") as outf:
    print(",\t".join(columns), file=outf)
    for datum in filtered:
        print(",\t".join([datum[k] for k in columns]), file=outf, sep="\n")
