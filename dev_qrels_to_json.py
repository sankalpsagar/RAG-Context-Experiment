import json

from dexter.config.constants import Split
from dexter.data.datastructures.hyperparameters.dpr import DenseHyperParams
from dexter.data.loaders.RetrieverDataset import RetrieverDataset
from dexter.llms.flant5_engine import FlanT5Engine
# from dexter.llms.llm_engine_orchestrator import LLMEngineOrchestrator
# from dexter.retriever.dense.ANCE import ANCE
from dexter.retriever.dense.Contriever import Contriever
from dexter.utils.metrics.ExactMatch import ExactMatch
from dexter.utils.metrics.SimilarityMatch import CosineSimilarity
from dexter.utils.metrics.retrieval.RetrievalMetrics import RetrievalMetrics

if __name__ == "__main__":
    # Ensure in config.ini the path to the raw data files are linked under [Data-Path]
    # ambignq = '<path to the data file>
    # ambignq-corpus = '<path to the corpus file>'

    # You can set the split to one of Split.DEV, Split.TEST or Split.TRAIN
    # Setting tokenizer=None only loads only the raw data processed into our standard data classes, if tokenizer is set, the data is also tokenized and stored in the loader.
    loader = RetrieverDataset("wikimultihopqa", "wikimultihopqa-corpus",
                              "config.ini", Split.DEV, tokenizer=None)

    # Initialize your retriever configuration
    # config_instance = DenseHyperParams(query_encoder_path="facebook/contriever",
    #                                    document_encoder_path="facebook/contriever"
    #                                    , batch_size=100, show_progress_bar=True)
    # loader.base_dataset.raw_data
    # From data loader loads list of queries, corpus and relevance labels.
    queries, qrels, corpus = loader.qrels()
    array_queries = []
    for q in queries:
        array_queries.append(q.id())

    with open('output_json_qrels_dev.json', 'w') as output_file:
        json.dump(qrels, output_file)
    with open('output_json_queries_dev.json', 'w') as output_file:
        json.dump(array_queries, output_file)
        # dict_write = csv.DictWriter(output_file, data_changed[0].keys(), delimiter='\t')
    # dict_write.writeheader()
    # dict_write.writerows(data_changed)

    # take first 1200 queries
    # todo changed import in WikiMulitHopQADataloader to only import 2 queries
