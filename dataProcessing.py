import csv
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json
import glob, os
import time

files = []
os.chdir("../cognism-enriched")
for file in glob.glob("*.json"):
    files.append(file)

r = 20
name_to_related = []

for i in range(r):
    name_to_related.append(dict())

n = 5
url_to_name = []

for i in range(n):
    url_to_name.append(dict())

file_num = 0
item_count = 0
for file in files:
    file_num += 1
    print("Processing file: " + file)
    print("Progress: " + str(file_num / len(files)))

    with open(file) as f:
        for line in f:

            incoming = json.loads(line)

            name_to_related[item_count % len(name_to_related)][incoming['name']] = incoming['related_people']

            url_to_name[item_count % len(url_to_name)][incoming['profile_url']] = incoming['name']

            item_count += 1

os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/processed_data')

for i in range(len(name_to_related)):
    with open('name_to_related' + str(i) + '.json', 'w') as handle:
        json.dump(name_to_related[i], handle)

for i in range(len(url_to_name)):
    with open('url_to_name' + str(i) + '.json', 'w') as handle:
        json.dump(url_to_name[i], handle)
