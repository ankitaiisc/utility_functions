import random
import pandas
import collections

def stratifiedkfold(k, df):
  folds = {}
  categories = list(set(df.cat))
  for cat in categories:
      df_cat = df[df.cat==cat]

      start = 0
      diff = int(len(df_cat)/k)
      for fold in range(k):
          if fold not in folds:
              folds[fold] = df_cat[start:start+diff]
          else:
              folds[fold] = pd.concat([folds[fold], df_cat[start:start+diff]])
          start = start+diff

      if k-1 not in folds:
          folds[k-1] = df_cat[start:]
      else:
          folds[k-1] = pd.concat([folds[fold], df_cat[start:]])
          
 return folds
 
#testing
for f in range(5):
  fold_counter=collections.Counter(folds[f].cat)
  for k, v in fold_counter.items():
      fold_counter[k] = 100*v/len(folds[f])
  print(list(fold_counter.values()))
