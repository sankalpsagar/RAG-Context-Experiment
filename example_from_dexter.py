from dexter.config.constants import Split
from dexter.data.datastructures.hyperparameters.dpr import DenseHyperParams
from dexter.data.loaders.RetrieverDataset import RetrieverDataset
from dexter.llms.flant5_engine import FlanT5Engine
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
    loader = RetrieverDataset("wikimultihopqatest","wikimultihopqatest-corpus",
                              "config.ini", Split.TEST,tokenizer=None)

    # Initialize your retriever configuration
    config_instance = DenseHyperParams(query_encoder_path="facebook/contriever",
                                       document_encoder_path="facebook/contriever"
                                       ,batch_size=1,show_progress_bar=True)

    # From data loader loads list of queries, corpus and relevance labels.
    queries, qrels, corpus = loader.qrels()

    #Perform Retrieval
    contrvr_search = Contriever(config_instance)
    similarity_measure = CosineSimilarity()
    response = contrvr_search.retrieve(corpus,queries,5,similarity_measure,chunk=True,chunksize=40000)

    metric = ExactMatch()
    print(response)
    print(qrels)
    flant5 = FlanT5Engine(response)
    flant5.get_flant5_completion("Hey")
    for i in qrels.keys():
        qrel_key_list = list(qrels[i].keys())
        response_key_list = list(response[i].keys())
        print(qrel_key_list)
        print(response_key_list)
        new_qrel_list = list()
        new_response_list = list()
        for j in range(len(qrel_key_list)):
            new_qrel_list.append(corpus[int(qrel_key_list[j])].text())
        for j in range(len(response_key_list)):
            new_response_list.append(corpus[int(response_key_list[j])].text())

        score = metric.evaluate(new_qrel_list, new_response_list)
        print(f"score for query-id: {i}", score)
    # metric.evaluate()
    # temp = metrics.evaluate_retrieval(qrels=qrels,results=response)

    # print(temp)