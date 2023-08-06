#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from dataclasses import dataclass

from typing import List, Optional

from vectorops.constants import *
from vectorops.utils.distance_utils import *
from vectorops.dataset_manager import DatasetManager
from vectorops.projection_manager import ProjectionManager


@dataclass 
class RadarProjection(ProjectionManager):
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


    def plot(self,
        encoder: Optional[Union[Base2Vec, SentenceTransformer2Vec]] = None,
        trim: bool = True
    ):  
        """
        Plot Radar plot
        """
        if encoder: self.encoder = encoder
        theta_vectors = self._encode_items(items=self.items, encoder=self.encoder)

        plot_title = f"{self.dataset_id} <br>{self.vector_label}: {self.vector_name}  <br>Encoder: {self.encoder}"
        self.fig.update_layout(title=plot_title)
        
        r_min = 1
        r_max = 0
        for query in self.queries:
            qv = self._clip_encode_text(query, norm=self.norm)
            r = [cosine_sim(tv, qv) for tv in theta_vectors]
            r_min = min(r_min, min(r))
            r_max = max(r_max, max(r))
            self.fig.add_trace(go.Scatterpolar(
                r= r,
                theta=self.items,
                fill='toself',
                name=query,
                connectgaps=True,
                )
            )
        if trim:
            self.fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[r_min, r_max]
                    )),
                )
            
        return self.fig