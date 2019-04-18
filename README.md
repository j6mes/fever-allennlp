# A Pure AllenNLP Implementation of FEVER Baseline Models

This is an implenetation of the FEVER Baseline system. This is a heterogeneous system with two components: the for a short sentence (called a claim) this system firstly finds evidence (information rertrieval) and then performs an assessment whether the claim is Supported or Refuted given the evidence (natual language inference).

## Model Description
The system contains three components: an end-to-end evidence retrieval system, the NLI classifier and a training data sampling script to generate new instances to train the NLI model.

### Information Retrieval 
The information retrieval system uses Facebook's DrQA implementation for TF-IDF based document similarity.  The DrQA script runs with two phases: firstly using the Wikipedia index, it will select the `k=5` closest documents that are most similar to the claim. Each of the sentences in those documents is used to then construct a new index over the sentences to find `l=5` nearest sentences to the claim.

### Natural Language Inference
We have three models for NLI: Decomposable Attention, ESIM and ESIM with ELMO embeddings. These models concatenate the evidence sentences retrieved from the IR phase and predict a label in `Supported`, `Refuted`, or `NotEnoughInfo`.

### Evidence Sampling for Training NLI
For claims that are `NotEnoughInfo` there is no evidence labeled in the dataset. The evidence sampling script identifies the closest relevant document for `NotEnoughInfo` claims then samples a sentence uniformly at random to train the NLI classifier.

## Install
This model can be installed with either `pip` or docker. For more info about the docker image, see this repo: )[https://github.com/j6mes/fever2-sample])

### PIP install
Create and activate fever conda environment

```bash
conda create -n fever
source activate fever
```

Install dependencies
```bash
pip install -r requirements.txt
```

## Manual data install
If using the docker verison of this repo. The data will be mounted in a data folder. Otherwise it must be manually set up with the following scripts:

Download GloVe
```bash
mkdir -p data
wget http://nlp.stanford.edu/data/wordvecs/glove.6B.zip
unzip glove.6B.zip -d data/glove
gzip data/glove/*.txt
```

Download Wiki
```bash
mkdir -p data
mkdir -p data/index
mkdir -p data/fever

wget -O data/index/fever-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz https://s3-eu-west-1.amazonaws.com/fever.public/wiki_index/fever-tfidf-ngram%3D2-hash%3D16777216-tokenizer%3Dsimple.npz
wget -O data/fever/fever.db https://s3-eu-west-1.amazonaws.com/fever.public/wiki_index/fever.db
```

Download Data
```bash
mkdir -p data
mkdir -p data/fever-data
wget -O data/fever-data/train.jsonl https://s3-eu-west-1.amazonaws.com/fever.public/train.jsonl
wget -O data/fever-data/dev.jsonl https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_dev.jsonl
wget -O data/fever-data/test.jsonl https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_test.jsonl
```



## Running with Pretrained Models
The pretrained models can be used with the following scripts:

### Information Retreival
Find the 5 nearest sentences from the 5 nearest documents using the pre-computed TF-IDF index. The documents are in the database file `fever.db`.

```bash
export PYTHONPATH=src
export FEVER_ROOT=$(pwd)
mkdir -p work
export WORK_DIR=work
python -m fever_ir.evidence.retrieve \
    --database $FEVER_ROOT/data/fever/fever.db \
    --index $FEVER_ROOT/data/index/fever-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz \
    --in-file $FEVER_ROOT/data/fever-data/dev.jsonl \
    --out-file $WORK_DIR/dev.sentences.p5.s5.jsonl \
    --max-page 5 \
    --max-sent 5
```

### Natural Language Inference
There are three available model files: `https://jamesthorne.co.uk/fever/fever-esim-elmo.tar.gz`, `https://jamesthorne.co.uk/fever/fever-esim.tar.gz` and `https://jamesthorne.co.uk/fever/fever-da.tar.gz`. If you are using a pretrained model, change `$MODEL_FILE` and `$MODEL_NAME` appropriately.

```bash
export CUDA_DEVICE=-1 #Set this to appropriate value if using a GPU. -1 for CPU
export PYTHONPATH=src
export FEVER_ROOT=$(pwd)
mkdir -p work
export WORK_DIR=work
export MODEL_NAME=fever-esim-elmo
export MODEL_FILE=https://jamesthorne.co.uk/fever/$MODEL_NAME.tar.gz
python -m allennlp.run predict \
    --output-file $WORK_DIR/$MODEL_NAME.predictions.jsonl \
    --cuda-device $CUDA_DEVICE \
    --include-package fever.reader \
    $MODEL_FILE \
    $WORK_DIR/dev.sentences.p5.s5.jsonl
```

### Scoring
Dev set can be scored locally with the FEVER scorer

```bash
python -m fever_ir.submission.score \
    --predicted_labels $WORK_DIR/$MODEL_NAME.predictions.jsonl \
    --predicted_evidence $WORK_DIR/dev.sentences.p5.s5.jsonl
```

Test set can be uploaded to the scoring server for scoring - the submission can be prepared with the following script

```bash
python -m fever_ir.submission.prepare \
    --predicted_labels $WORK_DIR/$MODEL_NAME.predictions.jsonl \
    --predicted_evidence $WORK_DIR/test.sentences.p5.s5.jsonl
    --out_file $WORK_DIR/submission.jsonl
```



## Train new Models

### Sample Evidence for Training

```bash
export PYTHONPATH=src
export FEVER_ROOT=$(pwd)
mkdir -p work
export WORK_DIR=work
python -m fever_ir.evidence.retrieve \
    --index $FEVER_ROOT/data/index/fever-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz \
    --in-file $FEVER_ROOT/data/fever-data/dev.jsonl \
    --out-file $FEVER_ROOT/data/fever/train.ns.pages.p1
```

### Train Models
Decomposable Attention Model
```python
allennlp train configs/decomposable_attention.json -s log/fever_da --include-package fever
```

ESIM
```python
allennlp train configs/esim_elmo.json -s log/fever_esim --include-package fever
```

ESIM+ELMo
```python
allennlp train configs/esim_elmo.json -s log/fever_esim_elmo --include-package fever
```

