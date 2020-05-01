import snap
import pandas as pd
import os
import csv
import json

os.chdir('/DATA-0/home/campus.berkeley.edu/alok_elashoff/processed_data')

df = pd.read_excel("census_2010.xlsx")
print(df.head())
df = df.drop(["rank", "count", "prop100k", "cum_prop100k"], axis = 1)

with open('sample_adj_list.json', 'r', encoding='utf-8') as f:
    sample_adj_list = json.load(f)

for name in sample_adj_list.keys():
    if name in df.index:
        print(df.loc[name].tolist())
