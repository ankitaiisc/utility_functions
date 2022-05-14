
def recall_at_k(trues, preds_k, labels):
    '''
       trues: list of true labels.
       preds_k: list of top k labels for each sample.
       labels: string or a list containing label names.
       Computes: how often can we get the right label in the top k predictions.
    '''
    category_wise_recall = {}
    category_support = {}
    #labels = 'ABCDEFGHIK'
    
    for cat in set(trues):
        correct_count = 0
        total_count = 0
        for t, p_k in zip(trues, preds_k):
            if t!=cat:
                continue
            if t in p_k:
                correct_count+=1
            total_count+=1
        category_wise_recall[labels[cat]] = 100*correct_count/total_count
        category_support[labels[cat]] = total_count

    count = 0
    for t, p_k, p in zip(trues, preds_k, preds):
        if t in p_k:
            count+=1
    category_wise_recall['overall'] = 100*count/len(trues)
    return category_wise_recall
