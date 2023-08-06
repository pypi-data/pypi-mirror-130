#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####
# Author: Charlene Leong charleneleong84@gmail.com
# Created Date: Thursday, October 21st 2021, 11:45:36 pm
# Last Modified: Thursday, October 21st 2021,11:46:37 pm
#####

import numpy as np
import pandas as pd

from typing import List, Dict, Tuple, Union

from distance_utils import cosine_dis, euc_dis


def get_nn_idx(
    vectors: Union[pd.DataFrame, np.ndarray],
    selected_vec: Union[pd.Series, np.ndarray],
    distance_measure_mode: str = 'cosine'
) -> np.ndarray:
    '''
    Get nearest neighbours idx
    '''
    if (selected_vec.ndim > 1):
        selected_vec = selected_vec.iloc[0]

    def compare_vector(vector: np.ndarray):
        if distance_measure_mode == 'cosine':
            return cosine_dis(selected_vec, vector)
        elif distance_measure_mode == 'euclidean':
            return euc_dis(selected_vec, vector)

    if type(vectors) == pd.DataFrame:
        distance_map = vectors.apply(compare_vector, axis=1)
        return distance_map.sort_values().index
    elif type(vectors) == np.ndarray:
        distance_map = np.array([compare_vector(v) for v in vectors])
        return np.argsort(distance_map)
        # return np.argpartition(distances, range(0, k))[:k]
