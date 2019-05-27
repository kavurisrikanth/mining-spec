# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 18:00:38 2019

@author: Srikanth
"""

import itertools
import pandas as pd
import os

from collections import Counter

# Returns frequency counts for items and item pairs
def freq(iterable):
    if type(iterable) == pd.core.series.Series:
        return iterable.value_counts().rename("freq")
    else: 
        return pd.Series(Counter(iterable)).rename("freq")


# Returns number of unique orders
def order_count(order_item):
    return len(set(order_item.index))


def open_file(f: str, names=None) -> pd.DataFrame:
    dir_path = 'D:/data-science/datasets/movielens/ml-10M100K/'
    path = os.path.join(dir_path, f)
    if not os.path.exists(path):
        raise FileNotFoundError("Couldn't find file: {}".format(path))
        
    if names is None:
        data = pd.read_csv(path, header=None, sep='::', engine='python')
    else:
        data = pd.read_csv(path, header=None, names=names, sep='::', engine='python')
        
    return data


def generate_pairs(df: pd.DataFrame, n: int=2):
    gb = df.groupby('UserID')
    
    print()
    print('Type of gb: {}'.format(type(gb)))
    print('Type of gb[MovieID]: {}'.format(type(gb['MovieID'])))
    print()
    
    combo = gb['MovieID'].apply(lambda x: itertools.combinations(x.values, n))
    
    print('Type of combo: {}'.format(type(combo)))
    #print(combo)
    
    for i, v in combo.iteritems():
        for item_pair in v:
            yield item_pair


def merge_stats(pairs: pd.DataFrame, stats: pd.DataFrame):
    return pairs.merge(stats.rename(columns={'freq': 'freqA', 'support': 'supportA'}), left_on='itemA', right_index=True).merge(stats.rename(columns={'freq': 'freqB', 'support': 'supportB'}), left_on='itemB', right_index=True)


def apriori(df: pd.DataFrame, minsup: float=0.5):
    stats = freq(df['MovieID']).to_frame('freq')
    stats['support'] = stats['freq'] / order_count(df) * 100.0
    
    qualifying = stats[stats['support'] >= minsup].index
    df = df[df['MovieID'].isin(qualifying)]
    
    print('#Items with support >= {}: {}'.format(minsup,
          len(qualifying)))
    
    qualifying = df[df.groupby(['UserID']).count() >= 2].index
    
    print('Type of qualifying: {}'.format(type(qualifying)))
    print('Length of q: {}'.format(len(qualifying)))
    print()
    
    #df = df[df['UserID'].isin(qualifying)]
    df = df[df['UserID'].isin(qualifying)]
    
    # Recalculate support
    stats = freq(df['MovieID']).to_frame('freq')
    stats['support'] = stats['freq'] / order_count(df) * 100.0
    
    # Generate pairs and calculate support (A -> B)
    pairs = generate_pairs(df, 2)
    pairs = freq(pairs).to_frame('freqAB')
    pairs['supportAB'] = pairs['freqAB'] / len(qualifying) * 100.0
    
    # Filter pairs by support
    pairs = pairs[pairs['supportAB'] >= minsup]
    
    print('Number of pairs with support >= {}: {}'.format(minsup, len(pairs)))
    
    stats = stats.reset_index().rename(columns={'level_0': 'item'})
    print()
    print(stats.head())
    pairs = pairs.reset_index().rename(columns={'level_0': 'itemA', 'level_1': 'itemB'})
    print(pairs.head())
    print()
    
    pairs = merge_stats(pairs, stats)
    
    # Calculate confidence values
    pairs['confidenceAB'] = pairs['supportAB'] / pairs['supportA']
    pairs['confidenceBA'] = pairs['supportAB'] / pairs['supportB']
    pairs['lift'] = pairs['supportAB'] / (pairs['supportA'] * pairs['supportB'])
    
    return pairs.sort_values('lift', ascending=False)


def get_movie_name(movies: pd.DataFrame, aID: int):
    f = movies[movies['MovieID'] == aID].reset_index(drop=True)
        
    return f['Title'][0]


def display_rules(rules: pd.DataFrame):
    movies = open_file('movies.dat', names=['MovieID', 'Title', 'Genres'])
    movies.drop('Genres', axis=1, inplace=True)
    
    print()
    print('Association rules:')
    for index, row in rules.iterrows():
        aID, bID = int(row['itemA']), int(row['itemB'])
        aName, bName = get_movie_name(movies, aID), get_movie_name(movies, bID)
        
        print('{} -> {}'.format(aName, bName))
        # break
    
    print()

# Read data
ratings = open_file('ratings.dat', names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
rules = apriori(ratings.copy(), 0.07)

# Display rules
display_rules(rules)