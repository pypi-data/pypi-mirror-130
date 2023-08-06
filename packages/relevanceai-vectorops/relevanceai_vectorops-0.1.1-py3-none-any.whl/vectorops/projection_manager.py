#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####
# Author: Charlene Leong charleneleong84@gmail.com
# Created Date: Thursday, October 21st 2021, 11:26:29 pm
# Last Modified: Friday, October 22nd 2021,4:21:14 am
#####

import numpy as np
import pandas as pd
import torch

from dataclasses import dataclass
from abc import ABC, abstractmethod

from typing import List, Dict, Tuple, Union, Optional, Any

from doc_utils import DocUtils
from vectorops.constants import *
from vectorops.utils.distance_utils import *
from vectorops.dataset_manager import DatasetManager

import clip
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

from vectorhub.base import Base2Vec
from vectorhub.encoders.text.sentence_transformers import SentenceTransformer2Vec
from vectorhub.bi_encoders.text_image.torch import ClipText2Vec

@dataclass 
class ProjectionManager(DocUtils):
    def __init__(self, 
            dm: Optional[DatasetManager] = None,
    ):    
        """
        Initialise dataset manager from dataset info and data dict
        """
        super().__init__()
        if dm: 
            self.vector_label = dm.vector_label
            self.vector_name =  dm.vector_name
            self.metadata_filename = dm.metadata_filename
            self.dataset_id = dm.dataset_id
            self.vectors = dm.vectors
            self.labels = dm.labels
            self.metadata = dm.metadata

            self.vectors_unique = dm.vectors_unique
            self.metadata_unique = dm.metadata_unique
            self.labels_unique = dm.labels_unique
            self.vectors_lut = dm.vectors_lut
            self.norm = dm.norm
        
        self.fig = None


    def _formulae_to_vector(
        self,
        formulae: List[VectorFormula], 
        encoder: Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec],
    ) -> List[np.ndarray]:
        """
        Calculate the vector of the math formulae defined by the user
        
        VectorFormula is of type
        ```
        {< VECTOR_OP >: [v1, v2, v3,  ...]}
        ```

        where VECTOR_OP is of type
        VECTOR_OPS = Literal['avg', 'sum', 'min', 'max', 'add', 'subtract', None]
        """
        formulae_vectors = []
        for formula in formulae:
            if not isinstance(formula, VectorFormula):
                raise ValueError(f'Invalid vector operation {formula} {VectorFormula}')
            op = formula.op
            queries = formula.queries
            if encoder is None:
                try:
                    if op is None:
                        f_vector = self.vectors_lut[queries[0]]
                    else:
                        qv = [self.vectors_lut[q] for q in queries]
                        f_vector = self._vector_op(operation=op, vectors=qv)
                except KeyError as e:
                    raise ValueError(f"{e} not in dataset {self.dataset_id}")

            elif (isinstance(encoder, SentenceTransformer2Vec) or isinstance(encoder, ClipText2Vec)):
                if op is None:
                    f_vector = self._encode_text(encoder, queries)
                else:
                    qv_encoded = [self._encode_text(encoder=encoder, text=q) for q in queries]
                    f_vector = self._vector_op(operation=op, vectors=qv_encoded)
            else:
                raise ValueError(f'Invalid encoder {encoder}. Must be of type [Base2Vec, SentenceTransformer2Vec, ClipText2Vec]')
                
            formulae_vectors.append(f_vector)
        return formulae_vectors


    
    def _encode_items(
        self,
        items: List[str],
        encoder: Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec] = None,
    ) -> List[np.ndarray]:  
        """
        Encodes list of items to vectors
        """
        items_encoded = []
        for i in items:
            if encoder is None:
                try:
                    items_encoded.append(self.vectors_lut[i])
                except KeyError as e:
                    raise ValueError(f"{e} not in dataset {self.dataset_id}")

            elif (isinstance(encoder, SentenceTransformer2Vec) or isinstance(encoder, ClipText2Vec)):
                text_encoded = self._encode_text(encoder, i)
                items_encoded.append(text_encoded)

        return items_encoded
        

    @staticmethod
    def _vector_op(
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


    @staticmethod
    def _encode_text(
        encoder: Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec], 
        text: str, 
        norm=True
    ) -> np.ndarray:
        '''
        Computes the text vectors for text sequence using Sentence Transformers
        '''
        text_encoded = np.array(encoder.encode(text))
        if norm: text_encoded /= np.linalg.norm(text_encoded)
        return text_encoded


    @staticmethod
    def _get_nn_idx(
        vectors: Union[pd.DataFrame, np.ndarray],
        selected_vec: Union[pd.Series, np.ndarray],
        distance_measure_mode: str = 'cosine'
    ) -> Union[pd.DataFrame, np.ndarray]:
        '''
        Gets nearest neighbours idx of a given selected vector within a vector matrix
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
        else:
            raise ValueError(f'{vectors} is not valid type (pd.DataFrame or np.ndarray)')


    @abstractmethod
    def plot(self):
        pass