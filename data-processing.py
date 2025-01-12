import pandas as pd
from dexter.config.constants import Split
from dexter.data.loaders.RetrieverDataset import RetrieverDataset

# pd.read_json("./dataset/wiki_musique")

loader = RetrieverDataset("wikimultihopqa", "wikimultihopqa-corpus",
                          "config.ini", Split.DEV, tokenizer=None)