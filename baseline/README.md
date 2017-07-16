## Document/Notes Representation
Previous research provides code for representing these documents as bag-of-words vectors [1].   
In particular, it takes the 10,000 tokens with the largest tf-idf scores from the training.   

(note: for the final model, here we could use POS tagging, parsing and entity recognition)

## ICD9-codes
Related previous work don't use all ICD9-code but only the most used. [2] [3]
*	We identify the top 20 labels based on number of patients with that label. 
*	We then remove all patients who don’t have at least one of these labels,  
*	and then filter the set of labels for each patient to only include these labels.   

(note: for the final model, do we consider the code's description and/or hierarchy?)

## Baseline Model
A neural network (not Recurrent) with one hidden layer, with relu activation on the hidden layer and sigmoid activation on the output layer.   Using cross entropy loss,which is the loss functions for multilabel classification [4]   
   
(note: not sure what will go in each cell for a recurrent network, one paper uses the last 20 notes for each admission and feeds one note to each cell.. but if we use just the discharge summary, then we could feed a sentence to each cell, or a word.. but that would be too many cells... something to consider later on)

## Evaluation
rank loss metric to evaluate performance [3] or F1 score [2] .. or both  (not sure yet)

## References
[1] Diagnosis code assignment: models and evaluation metrics. Journal of the American Medical Informatics   
[2] Applying Deep Learning to ICD-9 Multi-label Classification from Medical Records   
[3] ICD-9 Coding of Discharge Summaries   
[4] Large-scale Multi-label Text Classification - Revisiting Neural Networks   