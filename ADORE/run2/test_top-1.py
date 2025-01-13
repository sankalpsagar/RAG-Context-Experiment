import csv
import json

import pandas as pd
from dexter.llms.flant5_engine import FlanT5Engine

from dexter.config.constants import Split
from dexter.data.loaders.RetrieverDataset import RetrieverDataset
from dexter.utils.metrics.ExactMatch import ExactMatch
import pandas as pd

# load dev.rank.tsv
# convert query ids to the real ids with the output_query_id_to_new_id.tsv
#
query_id_to_new_id = None
with open('../dataset_1_dev/output_query_id_to_new_id_dev.json', 'r') as file:
    query_id_to_new_id = json.load(file)

inv_map_query_id = {value: key for key, value in query_id_to_new_id.items()}
# tsv_file = None
new_data = {}
with open("./dev.rank.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")

    for line in tsv_file:
        # print(line)
        the_id = inv_map_query_id[int(line[0])]
        doc_id = line[1][1:]
        rank = int(line[2])
        if the_id not in new_data.keys():
            new_data[the_id] = []
        new_data[the_id].append({'doc_id': doc_id, 'rank': rank})


data_dev = None
with open('../../dataset/dev.json', 'r') as file:
    data_dev = json.load(file)

queries_dev = {}
for index, query in enumerate(data_dev):
    # print(query)
    queries_dev[query['_id']] = query

corpus_data = None
with open('../../dataset/wiki_musique_corpus.json', 'r') as file:
    corpus_data = json.load(file)

response = {}
similarity_measure = ExactMatch()

question_df = {"questions":[], "answers":[]}
system_prompt = "Given the question and context, think step by step and output final answer for the question using information in the context and give answer in form of [Final Answer]: \n"
matches = 0
mismatches = 0
ids = []
count = 0
raw_data = []
flant5 = FlanT5Engine([]) # todo is it okay that data is an empty array here
for index_key, key in enumerate(new_data.keys()):
    print(index_key)
    documents_dev = []
    query = queries_dev[key]
    # get all doc ids for this query
    top_1_doc_ids = []
    for index, item in enumerate(new_data[key]):
        if item["rank"] <= 1:
            top_1_doc_ids.append(item["doc_id"])
        else:
            break
    # top_5_doc_ids = new_data[key][:5] # get first 5 documents, todo hopefully sorted
    for doc_id in top_1_doc_ids:
        # document = corpus_data[doc_id]
        documents_dev.append(corpus_data[doc_id]["text"])



    top_1 = " ".join(documents_dev)
    # print(top_3)
    user_prompt = "[Question]: When does monsoon season end in the state the area code 575 is located? \
[Final Answer]: mid-September. \
[Question]: What is the current official currency in the country where Ineabelle Diaz is a citizen? \
[Final Answer]: United States dollar. \
[Question]: Where was the person who founded the American Institute of Public Opinion in 1935 born? \
[Final Answer]: Jefferson. \
[Question]: What language is used by the director of Tiffany Memorandum? \
[Final Answer]: Italian. \
[Question]: What is the sports team the person played for who scored the first touchdown in Superbowl 1? \
[Final Answer]: Green Bay Packers. \
[Question]: The birth country of Jayantha Ketagoda left the British Empire when? \
[Final Answer]: February 4, 1948.\n\n Follow the above example and given the evidence, evidence: " + top_1 + " \n use this information, think step by step and answer the question:" + query["question"]
    # print(user_prompt)
    chain_answer = flant5.get_flant5_completion(system_prompt + " " + user_prompt)
    if "not possible" in chain_answer.lower():
        mismatches+=1
        continue
    elif "unknown" in chain_answer.lower():
        mismatches+=1
        continue
    elif "?" in chain_answer.lower():
        mismatches+=1
        continue
    elif "no answer" in chain_answer.lower():
        mismatches+=1
        continue
    elif len(chain_answer.split("[Final Answer]:")) >1:
        answer = chain_answer.split("[Final Answer]:")[-1]
        print("Generated Answer: {0}, Actual Answer: {1}".format(answer, query["answer"]))
        #if row.answer.text().lower() in answer.lower():
        if similarity_measure.evaluate(query["answer"].lower(), answer.lower()):
            matches+=1
        else:
            mismatches+=1
    else:
        mismatches+=1
    question_df["answers"].append(chain_answer)
    question_df["questions"].append(query["question"])

final_questions = pd.DataFrame(question_df)
EM = matches/(matches+mismatches)
print("EM: ", EM)
final_questions.to_csv("flant5_small_few_shot_top1_adore.tsv", sep="\t", index=False)