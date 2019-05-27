# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:45:10 2019

@author: Srikanth
"""

import os

import numpy as np
import pandas as pd

def get_num_unique(series: pd.Series):
    assert type(series) == pd.Series
    
    unique = series.unique()
    print('Type of unique: {}'.format(type(unique)))
    
    return unique


def get_stats(df: pd.DataFrame):
    return df.mean()[0], df.max()[0], df.var()[0], df.quantile(0.25)[0]


def print_stats(df: pd.DataFrame):
    mean, maximum, var, quantile = get_stats(df)
    print('Mean: {}'.format(mean))
    print('Max: {}'.format(maximum))
    print('Variance: {}'.format(var))
    print('First quartile: {}'.format(quantile))


def print_correlation(df: pd.DataFrame):
    corr = df.corr()
    print('Correlation:\n{}'.format(corr))


def print_median(df: pd.DataFrame):
    median = df.median()
    print('Median: {}'.format(median))
    
    
def print_sd(arr: np.array):
    sd = np.std(arr)
    print('Standard deviation: {}'.format(sd))
    
data_dir = os.path.join(os.getcwd(), 'data')