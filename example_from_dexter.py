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
    loader = RetrieverDataset("wikimultihopqatest", "wikimultihopqatest-corpus",
                              "config.ini", Split.TEST, tokenizer=None)

    # Initialize your retriever configuration
    config_instance = DenseHyperParams(query_encoder_path="facebook/contriever",
                                       document_encoder_path="facebook/contriever"
                                       , batch_size=1, show_progress_bar=True)
    loader.base_dataset.raw_data
    # From data loader loads list of queries, corpus and relevance labels.
    queries, qrels, corpus = loader.qrels()

    # Perform Retrieval
    contrvr_search = Contriever(config_instance)
    similarity_measure = CosineSimilarity()
    response = contrvr_search.retrieve(corpus, queries, 5, similarity_measure, chunk=True, chunksize=40000)

    # from example run_rag_zero_shot_cot.py from dexter
    # config_instance = LLMEngineOrchestrator()
    # llm_instance = config_instance.get_llm_engine(data="", llm_class="flant5")

    system_prompt = "Given the question and context, think step by step and  output final answer for the question using information in the context and give answer in form of  [Final Answer]: \n"

    # llm_instance.get_flant5_completion()

    metric = ExactMatch()
    print(response)
    print(qrels)
    flant5 = FlanT5Engine(response, model_name="google/flan-t5-small")

    for i, key in enumerate(qrels.keys()):
        current_query = queries[i]._text

        the_true_anser = loader.base_dataset.raw_data[i].answer._text # todo check if loader raw data is in the same order or that i should retrieve it in another way
        # qrel_key_list = list(qrels[i].keys())
        response_key_list = list(response[key].keys())
        # print(qrel_key_list)
        print(response_key_list)
        # new_qrel_list = list()
        retrieved_contexts = list()
        # for j in range(len(qrel_key_list)):
        #     new_qrel_list.append(corpus[int(qrel_key_list[j])].text())
        for j in range(len(response_key_list)):
            retrieved_contexts.append(corpus[int(response_key_list[j])].text())

        print(retrieved_contexts)

        # from dexter example
        user_prompt = "Given the evidence, Evidence: " + "".join(
            retrieved_contexts) + " \n use the information, think step by step  and answer the Question:" + current_query

        total_prompt = system_prompt + "\n" + user_prompt
        model_response =  flant5.get_flant5_completion(total_prompt)
        print(model_response)
        score = metric.evaluate(the_true_anser, model_response)
        print(f"score for query-id: {i}", score)
    # metric.evaluate()
    # temp = metrics.evaluate_retrieval(qrels=qrels,results=response)

    # print(temp)
