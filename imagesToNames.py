import csv
import json
import glob, os

IDtoUsername = dict()
with open("vision/photo_id_mappings.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    count = 5
    for row in rd:
        IDtoUsername[row[0]] = row[1]
        count -= 1
        if not count:
            break

files = []
os.chdir("cognism-enriched")
for file in glob.glob("*.json"):
    files.append(file)

data = []
os.chdir("../")
with open('cognism-enriched/0_0_people.json') as f:
    count = 1
    for line in f:
        data.append(json.loads(line))
        count -= 1
        if not count:
            break

print(data[0]['name'])
print(data[0]['external_id']['liid'])
print(data[0]['profile_url'])
print(data[0]['related_people'])
#print(IDtoUsername)
