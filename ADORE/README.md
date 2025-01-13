# what I did to run the thing
- get 1200 questions from train with qrels with the loader from dextercqa
- create a queries.tsv and qrels.tsv with new ids for the queries in both files because the code fromm Adore does not support ids that are not integers
- create the corpus file tsv
- with these 3 files I execute preprocess.py making sure only train parts are uncommented
- after preprocess i call STAR inference (model from the github repo) to cacluate the passages.mmep, I only did this once, because if im correct, this only encodes the passages from the corpus and is hopefully not dependant on the queries or qrels, i used max length as defined on the githbub repo
- with this i ran the adore training with 6 epochs

# step 2
- I got 1200 dev questions from the dev.json with qrels from the loader from dextercqa
- create a queries.tsv and qrels.tsv with new ids for the queries in both files because the code fromm Adore does not support ids that are not integers
- use same corpus file tsv
- with these 3 files I execute preprocess.py making sure only dev parts are uncommented
- after preprocess i call STAR inference to cacluate the passages.mmep, i think it didnt recalculate anything because i just kept the passages.mmep i already had
- run the adore inference with the model I trained in step 1
- run the script to convert ids back to normal ids, this is a script provided by people from ADORE
- ENd up with a dev.rank.tsv

# calculating the scores
- using the dev.rank.tsv
- get the normal query id back
- get top 5 documents from the query
- run flant5 with these 5 documents

# What needs to be run
run the file ADORE/run2/test.py to get the EM score














# Notes / commands

## to convert back to normal ids
python ./cvt_back.py --input_dir ./data/doc/evaluate/adore-star/ --preprocess_dir ./data/doc/preprocess --output_dir ./data/doc/official_runs/adore-star --mode dev --dataset doc

## inference star
python ./star/inference.py --data_type doc --max_doc_length 512 --mode dev

## inference adore
python ./adore/inference.py --model_dir ./data/doc/trained_models/adore-star --output_dir ./data/doc/evaluate/adore-star --preprocess_dir ./data/doc/preprocess --mode dev --dmemmap_path ./data/doc/evaluate/star/passages.memmap


## training adore

python ./adore/train.py \
--metric_cut 200 \
--init_path ./data/doc/trained_models/star \
--pembed_path ./data/doc/evaluate/star/passages.memmap \
--model_save_dir ./data/doc/adore_train/models/new_run \
--log_dir ./data/doc/adore_train/log \
--preprocess_dir ./data/doc/preprocess \
--model_gpu_index 0 \
--faiss_gpu_index 0

## NOtes
changed data loader

## install faissgpu
conda install -c pytorch -c nvidia faiss-gpu=1.9.0

## run training without faiss gpu index, maybe i can still try that but for now this works without the faissgpu index
python ./adore/train.py --metric_cut 200 --init_path ./data/doc/trained_models/star --pembed_path ./data/doc/evaluate/star/passages.memmap --model_save_dir ./data/doc/adore_train/models --log_dir ./data/doc/adore_train/log --preprocess_dir ./data/doc/preprocess --model_gpu_index 0


python ./adore/inference.py --model_dir ./data/doc/trained_models/adore-6-test --output_dir ./data/doc/evaluate/adore-star --preprocess_dir ./data/doc/preprocess --mode dev --dmemmap_path ./data/doc/evaluate/star/passages.memmap

python ./cvt_back.py --input_dir ./data/doc/evaluate/adore-star/ --preprocess_dir ./data/doc/preprocess --output_dir ./data/doc/official_runs/adore-star-6 --mode dev --dataset doc

python ./adore/inference.py --model_dir ./data/doc/trained_models/adore-6-train-set --output_dir ./data/doc/evaluate/adore-star --preprocess_dir ./data/doc/preprocess --mode dev --dmemmap_path ./data/doc/evaluate/star/passages.memmap

python ./cvt_back.py --input_dir ./data/doc/evaluate/adore-star/ --preprocess_dir ./data/doc/preprocess --output_dir ./data/doc/official_runs/adore-star-6-train-dev-output --mode dev --dataset doc








