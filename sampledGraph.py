import snap
import pandas as pd
import os
import csv
import json
import numpy as np
import networkx as nx

os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/processed_data')

df = pd.read_excel("census_2010.xlsx")
df = df.drop(["rank", "count", "prop100k", "cum_prop100k"], axis = 1)
df = df.replace({"(S)": 0})

with open('sample_adj_list_1000000.json', 'r', encoding='utf-8') as f:
    sample_adj_list = json.load(f)

def race_actual(row):
    race_id = np.argmax([row['pctwhite'],row['pctblack'],row['pctapi'],row['pcthispanic']])
    race_id_to_name = {0: "white", 1: "black", 2: "asian", 3: "hispanic"}
    race_name = race_id_to_name[race_id]
    return race_name

df["race_actual"] = df.apply(race_actual, axis = 1)

name_to_race = {}
total = 0
labeled = 0
for full_name in sample_adj_list.keys():
    total += 1

    for token in full_name.split(" "):
        pot_first_name = token.upper()

        if (df['name'] == pot_first_name).any():
            labeled += 1
            name_row = df.loc[df['name'] == pot_first_name]
            name_to_race[full_name] = name_row.race_actual.to_string(index = False)
            break


graph = nx.Graph()
for full_name in sample_adj_list.keys():
    graph.add_node(full_name)
for full_name in sample_adj_list.keys():
    for adj in sample_adj_list[full_name]:
        graph.add_edge(full_name, adj)
nx.set_node_attributes(graph, name_to_race, "race")

os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/results')
nx.write_gexf(graph, "sample_" + str(total) + ".gexf")

print("Total: " + str(total))
print("Labeled: " + str(labeled))
print("Pct Labeled: " + str(labeled / total))
