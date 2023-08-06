#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import numpy as np
from typing import List, Dict, Tuple, Union


from .encode_utils import *
from constants import *


def vector_op(
    operation: VectorOperation, 
    vectors: List[np.ndarray],
    axis: int = 0
) -> np.ndarray:
    """
    Perform vector operations (op, v1, v2)
    """
    if operation == 'avg':
        return np.mean(vectors, axis=axis)
    elif operation == 'sum':
        return np.sum(vectors, axis=axis)
    elif operation == 'min':
        return np.min(vectors, axis=axis)
    elif operation == 'max':
        return np.max(vectors, axis=axis)
    elif operation == 'add':
        return np.add.reduce(vectors, axis=axis)
    elif operation == 'subtract':
        return np.subtract.reduce(vectors, axis=axis)
    elif not isinstance(operation, VectorOperation):
        raise ValueError(f'Not a valid vector operation {operation} {VectorOperation}')



def axes_to_vector(
    axes_labels: List[str], 
    vectors_unique_lut: dict,
) -> List[np.ndarray]:
    """
    Calculate the axes vectors defined by user
    """
    axes_vectors = []
    for label in axes_labels:
        f_vector = vectors_unique_lut.get(label)
        axes_vectors.append(f_vector)
    return axes_vectors




def formulae_to_vector(
    formulae: List[str], 
    dataset_info: dict,
    encoder: Union[None, str] = None
) -> List[np.ndarray]:
    """
    Calculate the vector of the math formulae defined by the user
    """
    formulae_vectors = []
    for formula in formulae:
        op = formula[0]
        v1 = formula[1]
        v2 = formula[2]
        if not op or op not in VectorOperation:
            raise ValueError(f'Invalid operator {VectorOperation}')
        # print(encoder)
        if encoder=='clip':
            v1_encoded = clip_encode_text(v1)
            v2_encoded = clip_encode_text(v2) 
            f_vector = vector_op(operation=op, vectors=[v1_encoded, v2_encoded])
        elif encoder=='context_avg':
            v1_encoded = get_search_word_vector(v1, dataset_info=dataset_info)
            v2_encoded = get_search_word_vector(v2, dataset_info=dataset_info)
            f_vector = vector_op(operation=op, vectors=[v1_encoded, v2_encoded])
        else:
            if dataset_info['vectors_lut'].get(v1) is None:
                raise ValueError(f"{v1} not in dataset {dataset_info['dataset_id']}")
            elif dataset_info['vectors_lut'].get(v1) is None:
                raise ValueError(f"{v2} not in dataset {dataset_info['dataset_id']}")
            
            f_vector = vector_op(operation=op, 
                                vectors=[ dataset_info['vectors_lut'].get(v1), 
                                        dataset_info['vectors_lut'].get(v2) ])
        
        formulae_vectors.append(f_vector)
        
    return formulae_vectors
