# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 21:34:31 2019

@author: Srikanth
"""

import pandas as pd
import numpy as np
import sys
from collections import Counter
from itertools import groupby, combinations

def size(obj):
    return '{0:.2f} MB'.format(sys.getsizeof(obj)/(1024*1024))

# Returns frequency counts for items and item pairs
def freq(iterable):
    if type(iterable) == pd.core.series.Series:
        return iterable.value_counts().rename("freq")
    else: 
        return pd.Series(Counter(iterable)).rename("freq")

    
# Returns number of unique orders
def order_count(order_item):
    return len(set(order_item.index))


# Returns generator that yields item pairs, one at a time
def get_item_pairs(order_item):
    order_item = order_item.reset_index().as_matrix()
    for order_id, order_object in groupby(order_item, lambda x: x[0]):
        item_list = [item[1] for item in order_object]
              
        for item_pair in combinations(item_list, 2):
            yield item_pair
            

# Returns frequency and support associated with item
def merge_item_stats(item_pairs, item_stats):
    return (item_pairs
                .merge(item_stats.rename(columns={'freq': 'freqA', 'support': 'supportA'}), left_on='item_A', right_index=True)
                .merge(item_stats.rename(columns={'freq': 'freqB', 'support': 'supportB'}), left_on='item_B', right_index=True))


# Returns name associated with item
def merge_item_name(rules, item_name):
    columns = ['itemA','itemB','freqAB','supportAB','freqA','supportA','freqB','supportB', 'confidenceAtoB','confidenceBtoA','lift']
    rules = (rules.merge(item_name.rename(columns={'item_name': 'itemA'}), left_on='item_A', right_on='item_id').merge(item_name.rename(columns={'item_name': 'itemB'}), left_on='item_B', right_on='item_id'))
    return rules[columns]

    
def association_rules(order_item, min_support):

    print("Starting order_item: {:22d}".format(len(order_item)))


    # Calculate item frequency and support
    item_stats = freq(order_item).to_frame("freq")
    print(item_stats)
    return
    
    item_stats['support'] = item_stats['freq'] / order_count(order_item) * 100
    
    # Filter from order_item items below min support 
    qualifying_items       = item_stats[item_stats['support'] >= min_support].index
    order_item             = order_item[order_item.isin(qualifying_items)]

    print("Items with support >= {}: {:15d}".format(min_support, len(qualifying_items)))
    print("Remaining order_item: {:21d}".format(len(order_item)))


    # Filter from order_item orders with less than 2 items
    order_size             = freq(order_item.index)
    qualifying_orders      = order_size[order_size >= 2].index
    order_item             = order_item[order_item.index.isin(qualifying_orders)]

    print("Remaining orders with 2+ items: {:11d}".format(len(qualifying_orders)))
    print("Remaining order_item: {:21d}".format(len(order_item)))

    # Recalculate item frequency and support
    item_stats             = freq(order_item).to_frame("freq")
    item_stats['support']  = item_stats['freq'] / order_count(order_item) * 100
        
    # Get item pairs generator
    item_pair_gen          = get_item_pairs(order_item)


    # Calculate item pair frequency and support
    item_pairs              = freq(item_pair_gen).to_frame("freqAB")
    item_pairs['supportAB'] = item_pairs['freqAB'] / len(qualifying_orders) * 100

    print("Item pairs: {:31d}".format(len(item_pairs)))


    # Filter from item_pairs those below min support
    item_pairs              = item_pairs[item_pairs['supportAB'] >= min_support]

    print("Item pairs with support >= {}: {:10d}\n".format(min_support, len(item_pairs)))


    # Create table of association rules and compute relevant metrics
    item_pairs = item_pairs.reset_index().rename(columns={'level_0': 'item_A', 'level_1': 'item_B'})
    item_pairs = merge_item_stats(item_pairs, item_stats)
    
    item_pairs['confidenceAtoB'] = item_pairs['supportAB'] / item_pairs['supportA']
    item_pairs['confidenceBtoA'] = item_pairs['supportAB'] / item_pairs['supportB']
    item_pairs['lift']           = item_pairs['supportAB'] / (item_pairs['supportA'] * item_pairs['supportB'])
    
    print(item_pairs)
    
    
    # Return association rules sorted by lift in descending order
    return item_pairs.sort_values('lift', ascending=False)


# Read in data
orders = pd.read_csv('data/instacart/order_products__prior.csv')

print(size(orders))
print(orders.shape)

print(orders.head())

print(orders.groupby(by=['order_id'], axis=0).head())

print(orders.set_index('order_id')['product_id'].rename('item_id'))

# Convert into proper format
orders_altered = orders.set_index('order_id')['product_id'].rename('item_id')

print(orders_altered.head())

# Print new size
print('dimensions: {0};   size: {1};   unique_orders: {2};   unique_items: {3}'.format(orders.shape, size(orders), len(orders.index.unique()), len(orders.value_counts())))
  
rules = association_rules(orders_altered, 0.1)

print(orders[orders['order_id'] == 2])





# Custom effort
def is_frequent(c_itemsets: list, orders: pd.Series, min_support:float=0.1) -> bool:
    # Get item pairs generator
    freq = 0
    for oid in set(orders.index):
        
        cur = orders[oid]
        if isinstance(cur, np.int64):
            continue
        if all(ele in list(orders[oid]) for ele in c_itemsets):
            freq += 1
    
    return (freq * 100.0 / len(orders)) >= min_support

def get_support(c_itemset, orders):
    if not type(c_itemset) == list:
        c_itemset = [c_itemset]
        
    ans = 0
        
    # print('candidate itemset: ' + str(c_itemset))
    for order in orders['order_id']:
        # print('order: ' + str(order))
        # print(orders[orders['order_id'] == order])
        
        this_order_products = list(orders[orders['order_id'] == order]['product_id'])
        # print(this_order_products)
        
        if all(e in this_order_products for e in c_itemset):
            ans += 1
        break
    
    return ans / order_count(orders) * 100

def are_lists_mergeable(one:list, two:list, n:int) -> bool:
    for i in range(n-1):
        if one[i] != two[i]:
            return False
        
    return one[n-1] != two[n-1]

'''
Generates candidate (n+1)-itemsets
'''
def generate_candidate_itemsets(n_freq, n):
    if n == 0:
        return freq(n_freq).to_frame("freq")
    if n == 1:
        for item_pair in combinations(n_freq, 2):
            yield item_pair
    else:
        for one, two in n_freq:
            if are_lists_mergeable(one, two, n):
                yield one + two[-1]

orders = pd.read_csv('data/instacart/order_products__prior.csv')
products = pd.read_csv('data/instacart/products.csv')

print(orders.head())
print(orders.columns)
print(products.head())
print(products.columns)
print(products['product_id'])
print(type(products['product_id']))

#orders_altered = orders[['order_id','product_id']]
orders = orders.set_index('order_id')['product_id'].rename('item_id')
print(len(orders))
print(type(orders))
print(orders.head())
print(orders[5])
print(set(orders.index))

item_stats = freq(orders).to_frame("freq")
item_stats['support'] = item_stats['freq'] / order_count(orders) * 100

#itemsets = products['product_id'].tolist()

min_support = 0.01
f_ones_df = item_stats[item_stats['support'] >= min_support]
f_ones = f_ones_df.index.tolist()
f_ones.sort()

c_n = generate_candidate_itemsets(f_ones, 1)
#print(freq(c_n))
print(type(c_n))
f_twos = []
for itemset in c_n:
    if is_frequent(itemset, orders, min_support):
        f_twos.append(itemset)
print(f_twos)

# Now generate candidate (n+1)-itemsets. As long as the itemset is not empty, we generate frequent (n+1)-itemsets.
# And then we refer to the book for the next step.

# *************************************************************

item_stats = freq(orders_altered).to_frame("freq")

print(item_stats.head())
print(products_altered.groupby(['order_id', 'product_id']).count().head())
print(item_stats['freq'])