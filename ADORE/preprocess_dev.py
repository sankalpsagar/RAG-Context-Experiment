import pandas as pd
import json
import csv

data = None
with open('../dataset/dev.json', 'r') as file:
    data = json.load(file)

data_changed = []
for index, item in enumerate(data):

    data_changed.append({
        'qid': index,
        'query': item["question"],
    })
data_dict = {}
for index, item in enumerate(data):
    data_dict[item["_id"]] = index


with open('output_queries_dev.tsv', 'w') as output_file:
    dict_write = csv.DictWriter(output_file, data_changed[0].keys(), delimiter='\t')
    dict_write.writerows(data_changed)

with open('output_query_id_to_new_id_dev.json', 'w') as output_file:
    json.dump(data_dict, output_file)
