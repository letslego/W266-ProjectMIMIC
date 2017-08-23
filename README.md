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


## Appendix 
| Model | Notebook |
| --- | --- |
| NN Baseline | [baseline/mimic_icd9_baseline.ipynb](https://github.com/letslego/W266-ProjectMIMIC/blob/master/baseline/mimic_icd9_baseline.ipynb) |
| SVM Baseline | /svm_baseline/* all files in this directory, (code, readme) had been copied from https://physionet.org/works/ICD9CodingofDischargeSummaries, they were executed with MIMIC III data |
| Notes Exploration with Named Entity Recognition | /notes_exploration/* |
