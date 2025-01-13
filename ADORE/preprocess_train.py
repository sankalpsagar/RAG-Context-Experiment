import pandas as pd
import json
import csv

data = None
with open('../dataset/train.json', 'r') as file:
    data = json.load(file)
ids_questions = None
with open('./output_json_queries_train2.json', 'r') as file:
    ids_questions = json.load(file)

data_changed = []
for index, item in enumerate(data):
    if item["_id"] in ids_questions:
        data_changed.append({
            'qid': index,
            'query': item["question"],
        })
data_dict = {}

for index, item in enumerate(data):
    if item["_id"] in ids_questions:
        data_dict[item["_id"]] = index
    # data_dict.append({
    #     '_id': item["_id"],
    #     'new_id': index,
    # })
with open('output_queries_train2.tsv', 'w') as output_file:
    dict_write = csv.DictWriter(output_file, data_changed[0].keys(), delimiter='\t')
    dict_write.writerows(data_changed)

with open('output_query_id_to_new_id_train2.json', 'w') as output_file:
    json.dump(data_dict, output_file)



# with open('output_query_id_to_new_id.tsv', 'w') as output_file:
#     dict_write = csv.DictWriter(output_file, data_dict[0].keys(), delimiter='\t')
#     # dict_write.writeheader()
#     dict_write.writerows(data_dict)
# for key, values in data.items():
#     data_changed.append({
#         'docid': "D" + str(int(key)),
#         'url': "",
#         'title': values["title"].expandtabs(1),
#         'body': values['text'].expandtabs(1),
#     })