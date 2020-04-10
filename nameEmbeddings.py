import csv
import json
import glob, os
import pickle

files = []
os.chdir("cognism-enriched")
for file in glob.glob("*.json"):
    files.append(file)

name_to_related = dict()
url_to_name = dict()
os.chdir("../")
for file in files:
    with open('cognism-enriched/' + file) as f:
        count = 1
        for line in f:
            incoming = json.loads(line)

            name_to_related[incoming['name']] = incoming['related_people']

            url_to_name[incoming['profile_url']] = incoming['name']
            count -= 1
            if not count:
                break

with open('../processed_data/name_to_related.pickle', 'wb') as handle:
    pickle.dump(name_to_related, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('../processed_data/url_to_name.pickle', 'wb') as handle:
    pickle.dump(url_to_name, handle, protocol=pickle.HIGHEST_PROTOCOL)
