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

with open('output_queries.tsv', 'w') as output_file:
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