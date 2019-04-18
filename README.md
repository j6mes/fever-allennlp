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

### Install

Create and activate fever conda environment
```bash
conda create -n fever
source activate fever
```

Install PyTorch
```bash
conda install -c pytorch pytorch
```

Install dependencies
```bash
pip install -r requirements.txt
```


### Data Preparation

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

