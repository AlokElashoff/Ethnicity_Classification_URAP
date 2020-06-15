import snap
import pandas as pd
import os
import csv
import json
import numpy as np
import networkx as nx
from langdetect import detect

os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/processed_data')

df = pd.read_excel("census_2010.xlsx")
df = df.drop(["rank", "count", "prop100k", "cum_prop100k"], axis = 1)
df = df.replace({"(S)": 0})

with open('sample_adj_list_1000000.json', 'r', encoding='utf-8') as f:
    sample_adj_list = json.load(f)

# Label based on census
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

# Label based on charset
lang_to_race = {
"af": "black",
"ar": "white",
"bg": "white",
"bn": "black",
"ca": "white",
"cs": "white",
"cy": "white",
"da": "white",
"de": "white",
"el": "white",
"en": None,
"es": "hispanic",
"et": "white",
"fa": "white",
"fi": "white",
"fr": "white",
"gu": "asian",
"he": "white",
"hi": "asian",
"hr": "white",
"hu": "white",
"id": "asian",
"it": "white",
"ja": "asian",
"kn": "asian",
"ko": "asian",
"lt": "white",
"lv": "white",
"mk": "white",
"ml": "asian",
"mr": "asian",
"ne": "asian",
"nl": "white",
"no": "white",
"pa": "asian",
"pl": "white",
"pt": "white",
"ro": "white",
"ru": "white",
"sk": "white",
"sl": "white",
"so": "black",
"sq": "white",
"sv": "white",
"sw": "black",
"ta": "asian",
"te": "asian",
"th": "asian",
"tl": "asian",
"tr": "white",
"uk": "white",
"ur": "asian",
"vi": "asian",
"zh-cn": "asian",
"zh-tw": "asian"
}

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

char_label = 0
char_set = []
for full_name in sample_adj_list.keys():
    if full_name not in name_to_race:
        try:
            lang = detect(full_name)
            if not (lang == "en") and not (isEnglish(full_name)):
                char_label += 1
                name_to_race[full_name] = lang_to_race[lang]
                char_set.append(full_name)
                print("Name: " + str(full_name), "Lang: " + str(lang), "Race: " + str(lang_to_race[lang]))
        except:
            continue


# Create Graph
graph = nx.Graph()
for full_name in sample_adj_list.keys():
    graph.add_node(full_name)
for full_name in sample_adj_list.keys():
    for adj in sample_adj_list[full_name]:
        graph.add_edge(full_name, adj)

# Calculate Erroneous Neighbor PCT
neighbors = 0
erroneous_neighbors = 0
for full_name in name_to_race.keys():
    race = name_to_race[full_name]
    neighbors += len(list(graph.neighbors(full_name)))
    erroneous_neighbors += sum([(race == name_to_race[neighbor]) for neighbor in graph.neighbors(full_name) if neighbor in name_to_race])
print("Erroneous neighbors: " + str(erroneous_neighbors))
print("Total neighbors: " + str(neighbors))
print("Percent erroneous neighbors: " + str(erroneous_neighbors / neighbors))

# Prediction based on decision rule
def most_frequent(List):
    return max(set(List), key = List.count)

name_to_race2 = dict()

predicted = 0
for full_name in sample_adj_list.keys():
    if full_name not in name_to_race:
        neighbor_classes = [name_to_race[neighbor] for neighbor in graph.neighbors(full_name) if neighbor in name_to_race]
        if neighbor_classes:
            predicted += 1
            name_to_race2[full_name] = "p_" + most_frequent(neighbor_classes)

name_to_race.update(name_to_race2)

# Update char set labels
for full_name in char_set:
    name_to_race[full_name] = "c_" + name_to_race[full_name]

# Create graph output file
nx.set_node_attributes(graph, name_to_race, "race")
os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/results')
nx.write_gexf(graph, "sample_" + str(total) + "_decision_rule.gexf")

# Print Stats
print("Total: " + str(total))
print("Labeled: " + str(labeled))
print("Labeled Char Set: " + str(char_label))
print("Predicted: " + str(predicted))
print("Pct Labeled: " + str(labeled / total))
print("Pct Char Set: " + str(char_label / total))
print("Pct Predicted: " + str(predicted / total))
print("Pct Labeled + Predicted + Char Set: " + str((labeled + predicted + char_label) / total))
