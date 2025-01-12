import pandas as pd
import json
import csv

data = None
with open('../output_json_qrels_train.json', 'r') as file:
    data = json.load(file)

with open('./output_query_id_to_new_id_train.json', 'r') as file:
    query_id_to_new_id = json.load(file)


data_changed = []
for index, item in enumerate(data):
    for key in data[item].keys():
        value = data[item][key]
        new_query_id = query_id_to_new_id[item]

        data_changed.append({
            'qid': new_query_id,
            'some_thing': 0,
            'doc_id': key,
            'relevance': value,
        })
# <query_id> 0 <doc_id> <relevance>
with open('output_qrels_train.tsv', 'w') as output_file:
    dict_write = csv.DictWriter(output_file, data_changed[0].keys(), delimiter='\t')
    # dict_write.writeheader()
    dict_write.writerows(data_changed)


# for key, values in data.items():
#     data_changed.append({
#         'docid': "D" + str(int(key)),
#         'url': "",
#         'title': values["title"].expandtabs(1),
#         'body': values['text'].expandtabs(1),
#     })