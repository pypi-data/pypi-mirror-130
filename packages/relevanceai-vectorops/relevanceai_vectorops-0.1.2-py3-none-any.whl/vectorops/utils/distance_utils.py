#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import numpy as np
from scipy.spatial.distance import cdist

from typing import List, Dict, Tuple, Union


def cosine_dis(v1: Union[float, np.ndarray], v2: Union[float, np.ndarray]) -> np.ndarray:
    '''
    Calculates Cosine distance between two 1D arrays or two floats
    '''
    return 1 - (np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def cosine_sim(v1: Union[float, np.ndarray], v2: Union[float, np.ndarray]) -> np.ndarray:
    '''
    Calculates Cosine similarity between two 1D arrays or two floats
    '''
    return (np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def euc_dis(v1: Union[float, np.ndarray], v2: Union[float, np.ndarray]) -> np.ndarray:
    '''
    Calculates Euclidean distance between two 1D arrays or two floats
    '''
    return np.linalg.norm(v1-v2)


def cosine_sim_matrix(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    '''
    Calculates Cosine similarity matrix between each pair of the two collections of inputs
    '''
    return 1 - cdist(x, y, metric='cosine')


def cosine_dist_matrix(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    '''
    Calculates Cosine distance matrix between each pair of the two collections of inputs
    '''
    return cdist(x, y, metric='cosine')


# def min_max_norm(vectors: np.ndarray, min: float, max: float) -> np.ndarray:
#     '''
#     Performs min max normalisation on an array
#     '''
#     return np.frompyfunc(lambda x, min, max: (x - min) / (max - min), 3, 1)


min_max_norm = np.frompyfunc(lambda x, min, max: (x - min) / (max - min), 3, 1)