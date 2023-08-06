#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

from abc import abstractmethod
from typing import List, Tuple, Dict, Any, Optional

from pathlib import Path
from dataclasses import dataclass
from typing import List
from collections import Counter

from doc_utils import DocUtils

from vectorops.datasets import data_dict

BASE_DIR = Path.cwd().resolve().parent
DATA_PATH = BASE_DIR / 'data'


## TODO: Refactor dataset class


@dataclass
class DatasetBase:
    vector_label: str
    vector_name: str
    dataset_id: str

    @abstractmethod
    def _load_data(self, docs: Dict[str, Any]):
        """Load data from docs"""
        raise NotImplementedError
    


@dataclass
class LocalDataset(DatasetBase, DocUtils):
    def __init__(self, dataset_info: dict, k: int = -1, norm: bool = True):    
        """
        Initialise dataset manager from dataset info and data dict
        """
        self.dataset_info = dataset_info
        self.vector_label = dataset_info['vector_label']
        self.vector_name = dataset_info['vector_name']
        self.dataset_id = dataset_info['dataset_id']
        self.dataset_filename = dataset_info['dataset_filename']
        self.metadata_filename = dataset_info.get('metadata_filename')
        self.k = k
        self.norm = norm
        self._load_data()
        super().__init__(
            vector_label=self.vector_label, 
            vector_name=self.vector_name, 
            dataset_id=self.dataset_id
        )
    
    def _load_data(self):
        """
        Load vector dataset 
        """
        dataset_full = data_dict[self.dataset_filename][:self.k]

        if Path(DATA_PATH.joinpath(f'{self.metadata_filename}.csv')).exists():
            metadata = data_dict[self.metadata_filename]
        else:
            metadata_cols = [col for col in dataset_full.columns 
                            if not any(s in col for s in ['_vector_', '_id', 'insert_date_'])]
            metadata = dataset_full[metadata_cols]
            self.metadata_filename = self.dataset_filename.replace('max', 'metadata')
            metadata.to_csv(
                DATA_PATH.joinpath(f"{self.dataset_id}", f"{self.metadata_filename}.csv"), 
                encoding='utf-8', index=None
            )
        vectors = dataset_full[self.vector_name]
        vectors = np.array([x for x in vectors])
        self.vectors = vectors

        self.labels = metadata[[self.vector_label]]
        self.metadata = metadata
        if self.norm:
            self.vectors = self.vectors / np.linalg.norm(self.vectors, axis=1).reshape(-1, 1)

        labels_unique = pd.Series(metadata[self.vector_label].unique()).sort_values()
        vectors_unique = self._get_vector_unique(labels_unique)
        metadata_unique = metadata.loc[labels_unique.index]
        vectors_lut = {v: vectors_unique[i] for i, v in enumerate(labels_unique)}  
        self.labels_unique = labels_unique
        self.vectors_unique = vectors_unique
        self.metadata_unique = metadata_unique
        self.vectors_lut = vectors_lut


@dataclass
class DatasetManager(DatasetBase, DocUtils):
    def __init__(self, 
        k: int = -1, norm: bool = True, dataset_info: Optional[dict] = None
    ):    
        """
        Initialise dataset manager from dataset info and data dict
        """
        if dataset_info:
            self.dataset_info = dataset_info
            self.vector_label = dataset_info['vector_label']
            self.vector_name = dataset_info['vector_name']
            self.dataset_id = dataset_info['dataset_id']
            self.dataset_filename = dataset_info['dataset_filename']
            self.metadata_filename = dataset_info.get('metadata_filename')

        # self.docs = docs
        self.k = k
        self.norm = norm
        self._load_data()

        super().__init__(
                vector_label=self.vector_label, 
                vector_name=self.vector_name, 
                dataset_id=self.dataset_id
            )
        
    def _load_data(self):
        """
        Load vector dataset 
        """
        dataset_full = data_dict[self.dataset_filename]

        if Path(DATA_PATH.joinpath(f'{self.metadata_filename}.csv')).exists():
            metadata = data_dict[self.metadata_filename]
        else:
            metadata_cols = [col for col in dataset_full.columns 
                            if not any(s in col for s in ['_vector_', '_id', 'insert_date_'])]
            metadata = dataset_full[metadata_cols]
            self.metadata_filename = self.dataset_filename.replace('max', 'metadata')
            metadata.to_csv(
                DATA_PATH.joinpath(f"{self.dataset_id}", f"{self.metadata_filename}.csv"), 
                encoding='utf-8', index=None
            )

        vectors = dataset_full[self.vector_name]
        vectors = np.array([x for x in vectors])
        self.vectors = vectors

        self.labels = metadata[[self.vector_label]]
        self.metadata = metadata
        if self.norm:
            self.vectors = self.vectors / np.linalg.norm(self.vectors, axis=1).reshape(-1, 1)

        labels_unique = pd.Series(metadata[self.vector_label].unique()).sort_values()
        vectors_unique = self._get_vector_unique(labels_unique)
        metadata_unique = metadata.loc[labels_unique.index]
        vectors_lut = {v: vectors_unique[i] for i, v in enumerate(labels_unique)}  
        self.labels_unique = labels_unique
        self.vectors_unique = vectors_unique
        self.metadata_unique = metadata_unique
        self.vectors_lut = vectors_lut


    def __len__(self):
        return len(self.vectors)
    
    @property
    def len_unique(self):
        return len(self.vectors_unique)
    
    @property
    def shape(self):
        return self.vectors.shape
    
    @property
    def shape_unique(self):
        return self.vectors_unique.shape
    
    
    def _get_vector_unique(self, 
        labels_unique: pd.Series
    ) -> np.ndarray:
        '''
        Averaging unique vectors
        '''
        vectors_unique = self.vectors[labels_unique.index]
        labels = [l for llist in self.labels.values.tolist() for l in llist]
        c = Counter(labels)
        non_unique_labels = [k for k, v in c.items() if v>1]
        for i, v in enumerate(labels_unique):
            if v in non_unique_labels:
                vectors_unique[i] = self.get_search_word_vector(v)
        return vectors_unique


    def get_matching_items(self, 
        search_word: str, 
        metadata_cols: List = None,
        unique: bool = False
    ) -> pd.DataFrame:
        '''
        Get matching items of a given search word
        '''
        if unique:
            vector_label_lut = self.metadata_unique[self.vector_label].apply(lambda x : x.lower())
            search_word_mask = vector_label_lut.str.contains(search_word.lower())
            metadata_cols = [self.vector_label] + metadata_cols if metadata_cols else self.metadata_unique.columns
            matching_items = self.metadata_unique[metadata_cols].loc[search_word_mask]
        else:
            vector_label_lut = self.metadata[self.vector_label].apply(lambda x : x.lower())
            search_word_mask = vector_label_lut.str.contains(search_word.lower())
            metadata_cols = [self.vector_label] + metadata_cols if metadata_cols else self.metadata.columns
            matching_items = self.metadata[metadata_cols].loc[search_word_mask]
        return matching_items


    def get_search_word_vector(self,
        search_word: str,
        k: int = -1
    ) -> np.ndarray:
        '''
        Return average of search word vectors of a given search word
        '''
        vector_labels = self.labels[self.vector_label].apply(lambda x : x.lower())
        search_word_mask = vector_labels.str.contains(search_word.lower())
        search_word_vectors = self.vectors[search_word_mask][:k]
        return  np.mean(search_word_vectors, axis=0)




if __name__ == '__main__':
    dataset_info = {
        'vector_label': 'product_name',
        'vector_name': 'product_name_imagetext_vector_',
        'dataset_filename': 'ecommerce-6.uniq_id.7000.product_name_imagetext.7000.max',
        'metadata_filename': 'ecommerce-6.uniq_id.7000.product_name_imagetext.7000.metadata',
        'dataset_id':'ecommerce-6'
    }   

    dm = DatasetManager(dataset_info, data_dict)
    print(dm.vectors)
    print(len(dm))
