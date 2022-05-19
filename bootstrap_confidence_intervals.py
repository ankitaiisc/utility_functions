import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import matplotlib.pyplot as plt
from random import choices
import pandas as pd

#user specified parameters
metrics = ['accuracy', 'f1', 'precision', 'recall']
num_seeds = 5
num_bootstraps = 10000
save_name = './bootsrap_scores.pickle'

def get_CI(distribution, metric):        
    bootstrap_distribution = np.mean(distribution[metric], axis=1)
    std_error = np.std(bootstrap_distribution) #Using formula in Wasserman
    percentile_interval = [np.percentile(bootstrap_distribution, 2.5), np.percentile(bootstrap_distribution, 97.5)]
    std_error_interval = [T_hat[metric]-1.96*std_error, T_hat[metric]+1.96*std_error]
    print('percentile CI: ', [np.round(p, 3) for p in percentile_interval])
    print('std error CI: ', [np.round(p, 3) for p in std_error_interval])
    print('std error: ', np.round(std_error, 4))
    return percentile_interval, std_error_interval, np.round(std_error, 4)


def get_variances(scores, metrics):
    variances = []
    for b in np.arange(len(scores[metrics])):
        variances.append(np.var(scores[metrics][b]))
    variance_model = np.mean(variances)
    
    variance_sampling = np.var(np.mean(scores[metrics], axis=1))
    
    total_variance = np.var(scores[metrics])
    return variance_model, variance_sampling, total_variance
    
    
    
#T_hat computation
T_hat = {}
for metric in metrics:
    T_hat[metric] = []
    
for seed in [0,1,2,3,4]:
    labels = prediction_matrix[:,0]
    preds = prediction_matrix[:, seed+1]
    precision, recall, f1, _ = precision_recall_fscore_support(labels,\
                                                               preds,\
                                                               average='macro')
    acc = accuracy_score(labels, preds)
    report = classification_report(labels, preds, output_dict=True)
    
    T_hat['accuracy'].append(acc)
    T_hat['f1'].append(f1)
    T_hat['precision'].append(precision)
    T_hat['recall'].append(recall)
    
for metric in metrics:
    T_hat[metric] = np.mean(T_hat[metric])
    
    

#bootstraps
scores = {}
for metric in metrics:
    scores[metric] = np.empty(shape=(num_bootstraps, num_seeds), dtype='object')
    
for bs in range(num_bootstraps):
    indexes = choices(np.arange(N), k=N)
    bootstrap = prediction_matrix[indexes]

    for seed in [0,1,2,3,4]:
        labels = bootstrap[:,0]
        preds = bootstrap[:, seed+1]
        
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro')
        acc = accuracy_score(labels, preds)
        report = classification_report(labels, preds, output_dict=True)
        
        scores['accuracy'][bs, seed] = acc
        scores['f1'][bs, seed] = f1
        scores['precision'][bs, seed] = precision
        scores['recall'][bs, seed] = recall
        
for metric in metrics:
    if metric in scores.keys():
        for bs in range(num_bootstraps):
            for seed in [0,1,2,3,4]:
                if type(scores[metric][bs, seed])==tuple:
                    scores[metric][bs, seed] = scores[metric][bs, seed][0]
                    
                    
percentile_interval, std_error_interval, std = get_CI(scores, 'f1')
print(percentile_interval, std_error_interval, std)

variance_model, variance_sampling, total_variance = get_variances(scores, 'f1')
print(variance_sampling, variance_model, total_variance)


import pickle
with open(save_name, 'wb') as handle:
    pickle.dump(scores, handle)