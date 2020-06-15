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
import random

os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/processed_data')
print("Processing has begun")
start_time = time.time()

u = 5
url_to_name = dict()

for i in range(u):
    curr = 'url_to_name' + str(i) + '.json'
    with open(curr, 'r') as handle:
        url_to_name.update(json.load(handle))

        print("Finished processing " + curr)
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

r = 20
name_to_related = dict()
for i in range(r):
    curr = 'name_to_related' + str(i) + '.json'
    with open(curr, 'r') as handle:
        name_to_related.update(json.load(handle))

        print("Finished processing " + curr)
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

n = 1000000
random.seed(1)
seed_names = random.sample(name_to_related.keys(), n)

names = []

for name in seed_names:
    for related in name_to_related[name]:
        if related in url_to_name:
            names.append(url_to_name[related])
            if name not in names:
                names.append(name)

sample_adj_list = dict()
for name in names:
    sample_adj_list[name] = []

for name in names:
    for related in name_to_related[name]:
        if related in url_to_name:

            adj = url_to_name[related]
            if (adj in names) and (not adj in sample_adj_list[name]):
                sample_adj_list[name].append(adj)


print("Finished creating sample")
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()

with open('sample_adj_list_' + str(n) + '.json', 'w', encoding='utf-8') as f:
    json.dump(sample_adj_list, f)

print("Finished writing sample")
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
