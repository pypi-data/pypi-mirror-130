#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####
# Author: Charlene Leong charleneleong84@gmail.com
# Created Date: Friday, October 22nd 2021, 12:41:08 am
# Last Modified: Friday, October 22nd 2021,3:59:50 am
#####


import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Literal, Tuple, Union

from vectorhub.base import Base2Vec
from vectorhub.encoders.text.sentence_transformers import SentenceTransformer2Vec
from vectorhub.bi_encoders.text_image.torch import ClipText2Vec

VectorOperation = Literal['avg', 'sum', 'min', 'max', 'add', 'subtract', None]


@dataclass
class VectorFormula:
    op: VectorOperation
    queries: List[str]

    def __len__(self):
        return len(self.queries)

    def __repr__(self):
        return f'{self.op}({self.queries})'

    def __str__(self):
        return f'{self.op} ( {", ".join(self.queries)} )'
        

    @property
    def query(self):
        if self.op is None:
            return self.queries[0] 

    def to_list(self):
        return [self.op] + self.queries
        