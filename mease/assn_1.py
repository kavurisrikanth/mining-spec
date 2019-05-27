# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:13:57 2019

@author: Srikanth
"""

import os
from common import *
import matplotlib.pyplot as plt

def q4():
    data = pd.read_csv(os.path.join(data_dir, 'myfirstdata.csv'), header=None)
    
    # a
    unique_one, unique_two = get_num_unique(data[0]), get_num_unique(data[1])
    print('One -> len: {}, data: {}'.format(unique_one.size, unique_one))
    print('Two -> len: {}, data: {}'.format(unique_two.size, unique_two))
    
    # 0 -> Quantitative
    # 1 -> Qualitative
    
    # b
    # One of the values under column 1 is 'two'.
    
    # c
    plt.subplot(2, 1, 1)
    plt.bar(data.index, data[0])
    plt.title('Subplots')
    plt.ylabel('Data')
    
    plt.subplot(2, 1, 2)
    plt.bar(data.index, data[1])
    plt.xlabel('Index')
    plt.ylabel('Data')
    
    plt.show()
    

def q5():
    data = pd.read_csv(os.path.join(data_dir, 'onemillion.csv'), header=None)
    
    sample = data.sample(n=10000, replace=True)
    print('Sample length: {}'.format(len(sample)))
    print(sample.head())
    print()
    
    # b
    print('Sample stats')
    print_stats(sample)
    print()
    
    # c
    print('Full stats')
    print_stats(data)
    print()
    
    
def q7():
    ca = pd.read_csv(os.path.join(data_dir, 'CA_house_prices.csv'), header=None)
    oh = pd.read_csv(os.path.join(data_dir, 'OH_house_prices.csv'), header=None)
    
    print('California:\n{}'.format(ca.head()))
    print('Ohio:\n{}'.format(oh.head()))
    
    # a
    plt.boxplot(ca[0])
    plt.title('California house prices')
    plt.show()
    
    plt.boxplot(oh[0])
    plt.title('Ohio house prices')
    plt.show()
    
    # b
    plt.hist(ca[0], range=(0, 3500), rwidth=2/3)
    plt.title('California house prices')
    plt.show()
    
    plt.hist(oh[0], range=(0, 3500), rwidth=2/3)
    plt.title('Ohio house prices')
    plt.show()
    
    
def q8():
    football = pd.read_csv(os.path.join(data_dir, 'football.csv'))
    
    print('Football:\n{}'.format(football.head()))
    print()
    
    # a
    plt.scatter(x=football['2003 Wins'], y=football['2004 Wins'])
    plt.xlabel('2003 Wins')
    plt.ylabel('2004 Wins')
    plt.title('2003 vs. 2004 Wins')
    plt.show()
    
    # b - Some points are on top of each other. To solve this
    # problem, introduce some small random noise into the 
    # values.
    
    # c
    print_correlation(football)
    
    # d
    copy = football.copy()
    copy['2004 Wins'] = copy['2004 Wins'] + 10
    print_correlation(copy)
    
    # e
    copy = football.copy()
    copy['2004 Wins'] = copy['2004 Wins'] * 2
    print_correlation(copy)
    
    # f
    copy = football.copy()
    copy['2004 Wins'] = copy['2004 Wins'] * -2
    print_correlation(copy)
    
    
def q9():
    oh = pd.read_csv(os.path.join(data_dir, 'OH_house_prices.csv'), header=None)
    print('Ohio prices:\n{}'.format(oh))
    
    # a
    print_median(oh[0])
    
    # b - Since the median is positive, the distribution is
    # right-skewed.
    
    # c
    copy = oh.copy()
    copy[0] = copy[0] + 10
    print_median(copy[0])
    
    # d
    copy = oh.copy()
    copy[0] = copy[0] * 2
    print_median(copy[0])
    

def q10():
    arr = np.array([19,23,30,30,45,25,24,20])
    
    # a
    print_sd(arr)
    print()
    
    # b
    copy = np.copy(arr)
    print('Original array: {}'.format(copy))
    for i in range(copy.shape[0]):
        copy[i] += 10
    print('Altered array: {}'.format(copy))
    print_sd(copy)
    print()
    
    # c
    copy = np.copy(arr)
    print('Original array: {}'.format(copy))
    for i in range(copy.shape[0]):
        copy[i] *= 100
    print('Altered array: {}'.format(copy))
    print_sd(copy)
    print()
    
    
if __name__ == '__main__':
    # q4()
    # q5()
    # q7()
    # q8()
    # q9()
    q10()
