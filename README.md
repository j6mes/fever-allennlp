# A Pure AllenNLP Implementation of FEVER Baseline Models

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

