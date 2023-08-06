#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import numpy as np
import pandas as pd

import plotly.figure_factory as ff
import plotly.graph_objects as go

from dataclasses import dataclass

from typing import List, Optional

from vectorops.constants import *
from vectorops.utils.distance_utils import *
from vectorops.dataset_manager import DatasetManager
from vectorops.projection_manager import ProjectionManager


@dataclass 
class DistPlot(ProjectionManager):
    def __init__(self,  
            dm: DatasetManager,
            queries: List[str],
            items: List[str],
            encoder: Optional[Union[Base2Vec, SentenceTransformer2Vec]] = None,
        ):    
        """
        Initialise dataset manager from dataset info and data dict
        """
        super().__init__(dm)

        self.queries = queries
        self.items = items
        self.encoder = encoder
        self.fig = go.Figure()

    
    def plot(
        self,
        encoder: Optional[Union[Base2Vec, SentenceTransformer2Vec]] = None,
        trim: bool = False
    ):  
        """ 
        Plot Radar plot
        """
        if encoder: self.encoder = encoder
        hist_data = self._encode_items(items=self.items, encoder=self.encoder)
        
        if trim:
            hist_data_no_outliers = []
            for data in hist_data:
                data_mean, data_std = np.mean(data), np.std(data)
                cut_off = data_std * 3
                lower, upper = data_mean - cut_off, data_mean + cut_off
                hist_data_no_outliers.append([x for x in data if x > lower and x < upper])
            hist_data = hist_data_no_outliers
        
        self.fig = ff.create_distplot(hist_data, self.items, bin_size=.2)
        self.fig.update_layout(
            title_text=f"{self.dataset_id} <br>{self.vector_label}: {self.vector_name}  <br>Encoder: {self.encoder}",
            xaxis_title='Distribution',
            yaxis_title='Count',
        )
        self.fig.update_layout(legend_title_text=self.vector_label)

        return self.fig