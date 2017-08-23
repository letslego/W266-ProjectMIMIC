# W266-ProjectMIMIC

## Members:
Zenobia Liendo   
Guillaume De Roo   
Amitabha Karmakar   

Note: this repositiory does not contain files with MIMIC data because they need MIMIC authorization:
https://mimic.physionet.org/gettingstarted/access/ 

## Main Notebooks
| Model | Level| N. Records | Epochs | Notebook |
| --- | --- | --- | --- | --- |
| Baseline | First-Level | 5K| -|[pipeline/icd9_lstm_cnn_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_lstm_cnn_workbook.ipynb)|
| LSTM | First-Level | 5K| 5|[pipeline/icd9_lstm_cnn_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_lstm_cnn_workbook.ipynb)|
| LSTM with Attention| First-Level | 5K|5| [pipeline/icd9_lstm_cnn_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_lstm_cnn_workbook.ipynb)|
| CNN| First-Level | 5K| 5|[pipeline/icd9_lstm_cnn_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_lstm_cnn_workbook.ipynb)|
| CNN-ATT| First-Level | 5K| 5|[pipeline/icd9_cnn_att_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_cnn_att_workbook.ipynb)|
| Hierarchical LSTM Attention | First-level| 5k|5| [pipeline/icd9_hatt_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_hatt_workbook.ipynb)
| CNN| First-Level | 5K| 20| [pipeline/icd9_lstm_cnn_workbook.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_lstm_cnn_workbook.ipynb)|
| Basic Baseline | Leaf | 46K | - | [baseline/mimic_icd9_baseline.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/baseline/mimic_icd9_baseline.ipynb) |
| CNN for top 20 leaf icd-9 codes | Leaf | 46K | 7 | [icd9_cnn/cnn_top20_leave.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/icd9_cnn/cnn_top20_leave.ipynb) |
| CNN for first-level icd-9 codes in hierarchy | First-Level | 52.6K | - | [pipeline/icd9_cnn_50K_run.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_cnn_50K_run.ipynb) |
| CNN-ATT for first-level icd-9 codes in hierarchy | First-Level | 52.6K | - | [pipeline/icd9_cnn_att_50K_records.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_cnn_att_50K_records.ipynb) |

(Note: the different notebooks above would be re-factored as part of 'further work')

## Model Python modules

| Model | Python module |
| --- | --- |
| LSTM | [pipeline/lstm_model.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/lstm_model.py) |
| CNN | [pipeline/icd9_cnn_model.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_cnn_model.py)  |
| Attention Layer |[pipeline/attention_util.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/attention_util.py)  |
| LSTM_ATT | [pipeline/icd9_lstm_att_model.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_lstm_att_model.py)   |
| CNN_ATT | [pipeline/icd9_cnn_att.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/icd9_cnn_att.py)   |
| Hierarchical LSTM Attention | [pipeline/hatt_model.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/hatt_model.py)  |


## Helper classes for Preprocessing

| Helper | Python module |
| --- | --- |
| Filtering clinical-notes to keep the ones that have been assigned the top common N icd-9 codes (this is a multi-label),  removing any code from the label that is not in the top N | [pipeline/database_selection.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/database_selection.py) |
| Three main methods: (1) Splits input file in training, valiation and test  (2) Replace leaf icd9-code with its grandparent in the first level  (3) Calculates and Diplay F1 scores for a set of possible thresholds| [pipeline/helpers.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/helpers.py) |
| functions necessary to vectorize the ICD labels and text inputs| [pipeline/vectorization.py](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/vectorization.py) |
## Appendix 
| Model | Notebook |
| --- | --- |
| NN Baseline | [baseline/mimic_icd9_baseline.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/baseline/mimic_icd9_baseline.ipynb) |
| SVM Baseline | /svm_baseline/* all files in this directory, (code, readme) had been copied from https://physionet.org/works/ICD9CodingofDischargeSummaries, they were executed with MIMIC III data |
| Notes Exploration with Named Entity Recognition | [notes_exploration/Exploration.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/notes_exploration/Exploration.ipynb)|
| Glove training on MIMIC | [pipeline/glove_train.sh](https://github.com/letslego/W266-ProjectMIMIC/blob/master/pipeline/glove_train.sh)|
