# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:57:12 2019

@author: Srikanth
"""

import pandas as pd
from collections import Counter
from itertools import combinations

# Returns frequency counts for items and item pairs
def freq(iterable):
    if type(iterable) == pd.core.series.Series:
        return iterable.value_counts().rename("freq")
    else: 
        return pd.Series(Counter(iterable)).rename("freq")

df = pd.read_csv('data/transactions_by_dept.csv')

df[['ProductID','ProductName']] = df['Dept'].str.split(':', n=1, expand=True)
df.drop('Dept', axis='columns', inplace=True)

print(df.head())

# This code works-ish.
iters = pd.Series(Counter(df['ProductID'])).to_frame('freq')
print(iters[1])
iters['support'] = iters['freq'] / len(df) * 100.0
iters = iters[iters['support'] >= 0.1]

frequents = list(iters.index)

candidates = combinations(frequents, 2)
iters = pd.Series(Counter(candidates)).to_frame('freq')

# ***************************************************************

orders = set(df['POS Txn'])
n = 0
for oid in orders:
    print(oid)
    cur = df[df['POS Txn'] == oid]
    print(list(cur['ProductID']))

    break
    