#!/usr/bin/env python
########################################################
## Code for the following paper:
## 
## Adler Perotte, Rimma Pivovarov, Karthik Natarajan, Nicole Weiskopf, Frank Wood, Noemie Elhadad
## Diagnosis Code Assignment: Models and Evaluation Metrics, JAMIA, to apper
## 
## Columbia University
## Biomedical Informatics
## Author: Adler Perotte
##
########################################################

import argparse
import numpy as np
## This svm light library is packed with this code, but can also be
## obtained here: https://bitbucket.org/wcauchois/pysvmlight
import svmlight
import os
import pylab
import scipy.stats as stats

##############################
# Parse command line arguments


parser = argparse.ArgumentParser(description='Test Hierarchical SVM Model.')
parser.add_argument('-testing_codes_with_ancestors', default='data/testing_codes.data', help='File location containing testing codes that have been augmented with ancestor codes.')
parser.add_argument('-testing_codes_no_ancestors', default='data/testing_codes_na.data', help='File location containing testing codes without augmentation.')
parser.add_argument('-ICD9_tree', default='data/MIMIC_parentTochild',  help='File location containing the ICD9 codes.')
parser.add_argument('predictions_file', help='File to load predictions from.')
parser.add_argument('output_directory', help='Directory to save figure to.')
parser.add_argument('-I', type=int, default=7042, help='Total number of ICD9 codes. Default=7042')
parser.add_argument('-root', type=int, default=5367, help='Index of the root ICD9 code. Default=5367')
parser.add_argument('-D',  type=int, default=2282, help='Number of testing documents. Default=2282')

args = parser.parse_args()


##############################
# Load up training data

testing_codes_filename = args.testing_codes_with_ancestors
parent_to_child_file = args.ICD9_tree
codes_no_ancestors_file = args.testing_codes_no_ancestors
I = args.I
root = args.root
TD = args.D
output_directory = args.output_directory
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
Ty_true = np.zeros((TD, I), np.bool)
Ty_true_np  = np.zeros((TD, I), np.bool)

# Load up the tree
PtoC = [[] for i in range(I)]

f = open(parent_to_child_file)
for line in f:
    line = [int(x) for x in line.strip().split('|')]
    PtoC[line[0]].append(line[1])
f.close()
CtoP = [[] for i in range(I)]

f = open(parent_to_child_file)
for line in f:
    line = [int(x) for x in line.strip().split('|')]
    CtoP[line[1]] = line[0]
f.close()



# Create ancestors array
ancestors = [[] for i in range(I)]
children = PtoC[root]
for child in children:
    ancestors[child].append(root)
while len(children) > 0:
    new_children = []
    for child in children:
        for gc in PtoC[child]:
            ancestors[gc].extend([child] + ancestors[child])
            new_children.append(gc)
    children = new_children
for i in range(len(ancestors)):
    ancestors[i] = np.array(ancestors[i] + [i])

def only_leaves(codes):
    leaves = []
    codes = np.array(codes)
    all_ancestors = set()
    for code in codes:
        all_ancestors.update(list(ancestors[code][:-1]))
    for code in codes:
        if code not in all_ancestors:
            leaves.append(code)
    return leaves



########################################
## Load predictions on test set

predictions = []
with open(args.predictions_file) as f:
    for line in f:
        line = line.strip().split('|')
        predictions.append([int(x) for x in line])


##########################################
## Evaluation


# Load up the labels
f =open(testing_codes_filename)
for d, line in enumerate(f):
    line = line.strip().split('|')[1:]
    if len(line)==0:
        line= [root]
    for code in line:
        code = int(code)
        Ty_true[d,code] = True
f.close()

# Load up the observed codes (without ancestors) for the test set
f = open(codes_no_ancestors_file)
for d, line in enumerate(f):
    line = line.strip().split('|')[1:]
    line = only_leaves([int(x) for x in line])
    for code in line:
        code = int(code)
        Ty_true_np[d,code] = True
f.close()

svm_pred_array = []
for i in range(TD):
    try:
        svm_pred_array.append(np.array(list(predictions[i])))
    except:
        svm_pred_array.append(np.array([root]))

new_svm_preds = []
for i in range(len(svm_pred_array)):
    preds = set(list(svm_pred_array[i]))
    new_preds = set([])
    for pred in preds:
        new_preds.update(list(ancestors[pred]))
    new_svm_preds.append(list(new_preds))

global_leaves = set(range(I))
for code in range(I):
    anc = ancestors[code][:-1]
    for anc_code in anc:
        if anc_code in global_leaves:
            global_leaves.remove(anc_code)

all_codes = set(range(I))


######################################################
## Baseline evaluation statistics

FPs = []
TPs = []
FNs = []
TNs = []

for doc_i in range(TD):
    ## if doc_i %20 == 0:
    ##     print doc_i
    gold_standard = set(Ty_true_np[doc_i].nonzero()[0])# only_leaves(y_T[doc_i])
    full_gs = set(Ty_true[doc_i].nonzero()[0])
    full_pred = new_svm_preds[doc_i]
    pred = set(only_leaves(full_pred))#set(predictions[doc_i])#
    TP = 0
    FP = 0
    FN = 0
    for code in gold_standard:
        if len(set(list(ancestors[code]))-set(full_pred)) > 0:
            FN += 1
        ## else:
        ##     TP += 1
    for code in pred:
        anc_set = set(list(ancestors[code]))
        if len(anc_set-set(full_gs)) > 0 and not np.any([x in anc_set for x in gold_standard]):
            FP += 1
        else:
            TP += 1
    FNs.append(FN)
    FPs.append(FP)
    TPs.append(TP)
    #TNs.append(TN)

FNs = np.array(FNs,np.float)
FPs = np.array(FPs,np.float)
TPs = np.array(TPs,np.float)

print "Baseline statistics considering hierarchy:"
print "Recall/Sensitivity"
recall = stats.nanmean(np.where(TPs+FNs>0,TPs/(TPs+FNs),0))
print recall

print "Precision"
precision = stats.nanmean(np.where(TPs+FPs>0,TPs/(TPs+FPs),0))
print precision

print "F1"
f1 = 2*(recall*precision)/(recall + precision)
print f1
print

##############################################################
## Baseline evaluation statistics where only exact gold-standard
## is considered a true positive match

FPs = []
TPs = []
FNs = []
TNs = []

for doc_i in range(TD):
    ## if doc_i %20 == 0:
    ##     print doc_i
    gold_standard = set(Ty_true_np[doc_i].nonzero()[0])# only_leaves(y_T[doc_i])
    full_gs = set(Ty_true[doc_i].nonzero()[0])
    full_pred = new_svm_preds[doc_i]
    pred = set(predictions[doc_i])-set([root])#set(only_leaves(full_pred))
    TP = 0
    FP = 0
    FN = 0
    TP = len(pred.intersection(gold_standard))
    FP = len(pred - gold_standard)
    FN = len(gold_standard - pred)
    FNs.append(FN)
    FPs.append(FP)
    TPs.append(TP)
    #TNs.append(TN)

FNs = np.array(FNs,np.float)
FPs = np.array(FPs,np.float)
TPs = np.array(TPs,np.float)


print "Baseline statistics ignoring hierarchy (only exact gold-standard matches count as true positives):"
print "Recall/Sensitivity"
recall = stats.nanmean(np.where(TPs+FNs>0,TPs/(TPs+FNs),0))
print recall

print "Precision"
precision = stats.nanmean(np.where(TPs+FPs>0,TPs/(TPs+FPs),0))
print precision

print "F1"
f1 = 2*(recall*precision)/(recall + precision)
print f1
print 


##############################################################
## Multi-label Hierarchical Evaluation Statistics


score1s = []
score2s = []
score3s = []
score1us = []
score2us = []
score3us = []
for doc_i in range(TD):
    ## if doc_i %20 == 0:
    ##     print doc_i
    gold_standard = set(Ty_true_np[doc_i].nonzero()[0])# only_leaves(y_T[doc_i])
    full_gold_standard = set()
    for code in gold_standard:
        full_gold_standard.update(list(ancestors[code]))
    old_to_omit = set()
    for code in gold_standard:
        old_to_omit.update(set(list(ancestors[code][:-1])) - gold_standard)
    full_pred = new_svm_preds[doc_i]#svm_pred_array[doc_i]#(Tpredictions_mean[doc_i]>=threshold).nonzero()[0]
    pred = set(only_leaves(full_pred))
    ds = []
    es = []
    for code in gold_standard:
        ds.append(len(set(list(ancestors[code])).intersection(set(full_pred))))
        es.append(len(ancestors[code]))
    pred_ds = []
    pred_fs = []
    for code in pred:
        pred_ds.append(len(set(list(ancestors[code])).intersection(set(full_gold_standard))))
        pred_fs.append(len(ancestors[code]))
    ds = np.array(ds,np.float)
    es = np.array(es,np.float)
    pred_ds = np.array(pred_ds,np.float)
    pred_fs = np.array(pred_fs,np.float)
    score1s.extend(list(ds/es))
    score2s.extend(list((es-ds)/es))
    score3s.extend(list((pred_fs-pred_ds)/pred_fs))
    score1us.extend(list(ds))
    score2us.extend(list((es-ds)))
    score3us.extend(list((pred_fs-pred_ds)))


pylab.figure()
raw_data = pylab.hist(score2s, bins=10)
pylab.title('Normalized Divergent Path to Gold-Standard')
pylab.xlabel('Normalized Path Length')
pylab.xlim(0,1)
pylab.ylim(0,10000)
pylab.ylabel('Count')
pylab.grid()
pylab.savefig(os.path.join(output_directory, 'dist_score_2.png'))

print 'Data for', pylab.gca().get_title()
print raw_data

pylab.figure()
raw_data = pylab.hist(score3s, bins=np.arange(0,1,0.1))
pylab.title('Normalized Divergent Path to Predicted')
pylab.xlabel('Normalized Path Length')
pylab.xlim(0,1)
pylab.ylim(0,10000)
pylab.ylabel('Count')
pylab.grid()
pylab.savefig(os.path.join(output_directory, 'dist_score_3.png'))

print 'Data for', pylab.gca().get_title()
print raw_data

pylab.figure()
raw_data = pylab.hist(score1us, bins=np.arange(10), align='left')
pylab.title('Shared Path')
pylab.xlabel('Level in ICD9 tree')
pylab.ylabel('Count')
pylab.xlim(-0.5,8.5)
pylab.ylim(0,10000)
pylab.xticks(range(9))
pylab.grid()
pylab.savefig(os.path.join(output_directory, 'dist_score_1u.png'))

print 'Data for', pylab.gca().get_title()
print raw_data

pylab.figure()
raw_data = pylab.hist(score2us, bins=np.arange(10), align='left')
pylab.title('Divergent Path to Gold-Standard')
pylab.xlabel('Level in ICD9 tree')
pylab.ylabel('Count')
pylab.xlim(-0.5,8.5)
pylab.ylim(0,10000)
pylab.xticks(range(9))
pylab.grid()
pylab.savefig(os.path.join(output_directory, 'dist_score_2u.png'))

print 'Data for', pylab.gca().get_title()
print raw_data

pylab.figure()
raw_data = pylab.hist(score3us, bins=np.arange(10), align='left')
pylab.title('Divergent Path to Predicted')
pylab.xlabel('Level in ICD9 tree')
pylab.ylabel('Count')
pylab.xlim(-0.5,8.5)
pylab.ylim(0,10000)
pylab.xticks(range(9))
pylab.grid()
pylab.savefig(os.path.join(output_directory, 'dist_score_3u.png'))

print 'Data for', pylab.gca().get_title()
print raw_data
