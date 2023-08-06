#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from dataclasses import dataclass
from doc_utils import DocUtils

from typing import List, Dict, Tuple, Union, Optional, Any

from vectorhub.base import Base2Vec

from vectorops.constants import *
from vectorops.utils.distance_utils import *
from vectorops.dataset_manager import DatasetManager
from vectorops.projection_manager import ProjectionManager

from vectorhub.base import Base2Vec
from vectorhub.encoders.text.sentence_transformers import SentenceTransformer2Vec
from vectorhub.bi_encoders.text_image.torch import ClipText2Vec

MARKER_SIZE = 5

@dataclass
class VectorDataset(DocUtils):
    dataset_id: str
    docs: Dict[str, Any]
    vector_label: str
    vector_field: str
        
    def __post_init__(self):
        self.vectors = self.get_field_across_documents(self.vector_field, self.docs)
    
    def __len__(self):
        return len(self.vectors)
    
    @property
    def vector_field_len(self):
        return len(self.vectors[0])



@dataclass
class ComparatorDataset:
    def __init__(self, 
             vectors_1: VectorDataset, 
             vectors_2: VectorDataset, 
        ):
        super().__init__()
        self.vectors_1 = vectors_1
        self.vectors_2 = vectors_2
        assert self.vectors_1.vector_field_len == self.vectors_2.vector_field_len
        self.vector_field_len = self.vectors_1.vector_field_len
    
    @property
    def vectors_1_len(self):
        return len(self.vectors_1)
    
    @property
    def vectors_2_len(self):
        return len(self.vectors_2)
    



@dataclass 
class ScatterProjection(ProjectionManager):
    def __init__(self,  
            x_axis_value: VectorOperation,
            y_axis_value: VectorOperation,
            encoder: Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec] = None,
            plot_unique: bool = False,
            plot_nn: Union[None, int] = None, 
            plot_labels: bool = False,
            dm: Optional[DatasetManager] = None,
        ):    
        """
        Initialise dataset manager from dataset info and data dict
        """
        super().__init__(dm)
        self.x_axis_value = x_axis_value
        self.y_axis_value = y_axis_value
        self.encoder = encoder
        self.plot_unique = plot_unique
        self.plot_nn = plot_nn
        self.plot_labels = plot_labels


    def _projection(
        self,
        encoder: Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec],
        vectors: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        formulae = [ self.x_axis_value, self.y_axis_value ]
        axes_vectors_list = self._formulae_to_vector(formulae=formulae, encoder=encoder)

        # if self.plot_unique:
        #     vectors_matrix = np.stack(self.vectors_unique)  # num_embeds x hidden
        # else:
        vectors_matrix = np.stack(vectors)              # num_embeds x hidden
        axes_vectors = np.stack(axes_vectors_list)      # num_axes x hidden_dimension
        
        assert axes_vectors.shape[0] == 2
        assert vectors_matrix.shape[1] == axes_vectors.shape[1]

        projection_matrix = cosine_sim_matrix(vectors_matrix, axes_vectors)
        return projection_matrix, axes_vectors


    def _build_projection_df(self,
        projection_matrix: np.ndarray,
        axes_matrix: np.ndarray,
        vectors: np.ndarray,
        labels: np.ndarray,
        vector_label: str,
        metadata_df: pd.DataFrame,
        vector_field: Union[None, str] = None,
        plot_nn: Optional[Union[None, int]] = None, 
        plot_unique: Optional[bool] = False,
        overlap_only: bool = False,
    ) -> Tuple[pd.DataFrame, List]:
        """
        Build project df from axes matrix
        """
        if overlap_only:
            '''
            Project vectors onto axes and find overlap
            '''
            search_vector_nn_idx_1 = self._get_nn_idx(vectors=vectors, selected_vec=axes_matrix[0])
            nn_1_labels = metadata_df[[vector_label]].loc[search_vector_nn_idx_1]
            
            search_vector_nn_idx_2 = self._get_nn_idx(vectors=vectors, selected_vec=axes_matrix[1])
            nn_2_labels = metadata_df[[vector_label]].loc[search_vector_nn_idx_2]

            if plot_nn:
                nn_1_labels = nn_1_labels[:int(len(labels)/2)]
                nn_1_labels['neighbours'] = 'x' if not vector_field else f'{vector_field}_x'
                nn_2_labels = nn_2_labels[:int(len(labels)/2)]
                nn_2_labels['neighbours'] = 'y' if not vector_field else f'{vector_field}_y' 
                legend = 'neighbours'
            
            labels_df =  pd.concat([ nn_1_labels, nn_2_labels ], axis=0).reset_index()      
            data_df = pd.DataFrame( projection_matrix[labels_df.index], 
                                    columns=[ str(self.x_axis_value), str(self.y_axis_value) ])

        elif plot_nn:
            '''
            Show nearest neighbours of each axis
            '''
            search_vector_nn_idx_1 = self._get_nn_idx(vectors=vectors, selected_vec=axes_matrix[0])
            nn_1_labels = metadata_df[[vector_label]].loc[search_vector_nn_idx_1][:plot_nn]
            nn_1_labels['neighbours'] = 'x' if not vector_field else f'{vector_field}_x'

            search_vector_nn_idx_2 = self._get_nn_idx(vectors=vectors, selected_vec=axes_matrix[1])
            nn_2_labels = metadata_df[[vector_label]].loc[search_vector_nn_idx_2][:plot_nn]
            nn_2_labels['neighbours'] = 'y' if not vector_field else f'{vector_field}_y' 

            labels_df =  pd.concat([nn_1_labels, nn_2_labels], axis=0).reset_index()
            data_df = pd.DataFrame(projection_matrix[labels_df.index], 
                                    columns=[ str(self.x_axis_value), str(self.y_axis_value) ])
            legend = 'neighbours'

        else:
            if plot_unique:
                labels_df = pd.DataFrame(list(set(labels)), columns=[vector_label])
            else:
                labels_df = pd.DataFrame(labels, columns=[vector_label])

            data_df = pd.DataFrame(projection_matrix, 
                                    columns=[ str(self.x_axis_value), str(self.y_axis_value) ])
            legend = None

        return pd.concat([labels_df, data_df], axis=1), legend



    def get_neighbours_info(self,
        columns: Optional[Union[List, None]] = None,
        axis: Literal['x', 'y'] = 'x',
    ):
        if self.df is None:
            raise ValueError(f'Please call `pm.plot_scatter()`')
        if columns:
            columns = [self.vector_label] + columns
        else:
            columns = self.metadata.columns
        return self.metadata[columns].loc[self.df[self.df.neighbours==axis]['index']]


    def plot(
        self,
        plot_unique: Optional[bool] = False,
        plot_nn: Optional[Union[None, int]] = None, 
        plot_labels: Optional[bool] = False,
        encoder: Optional[Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec]] = None,
    ):
        """
        Plots scatter plot of the projection of the dataset
        """
        self.plot_unique = plot_unique
        self.plot_nn = plot_nn
        self.plot_labels = plot_labels
        self.encoder = encoder
        
        """
        Plotting projection matrix
        """
        self.projection_matrix, self.axes_matrix = self._projection(vectors=self.vectors, encoder=encoder)
        
        """
        Preparing plot figure
        """
        df, legend = self._build_projection_df(
            projection_matrix=self.projection_matrix, 
            axes_matrix=self.axes_matrix,
            vectors=self.vectors,
            labels=self.labels,
            vector_label=self.vector_label,
            metadata_df=self.metadata,
            plot_nn=self.plot_nn,
            plot_unique=self.plot_unique
        )
        text = df[self.vector_label] if (self.plot_labels) else None

        plot_title = f"{self.dataset_id}: {len(df)} points<br>{self.vector_label}: {self.vector_name}"
        plot_title += f"<br>Encoder: {self.encoder.__name__}"
        if self.plot_unique: 
            plot_title += f"\tUnique: {self.plot_unique}"

        fig = px.scatter(df, 
                        x=str(self.x_axis_value), y=str(self.y_axis_value), 
                        color=legend, text=text,
                        title=plot_title
                        )
        fig.update_traces(
            hovertemplate="<br>".join([
                "X: %{x}",
                "Y: %{y}",
                "Label: %{customdata}",
            ])
        )
    
        """
        Adding vector label to hover data
        """
        fig.update_traces(customdata=df[self.vector_label])
        fig.update_traces(hovertemplate='%{customdata}')
        fig.update_traces(
            hovertemplate="<br>".join([
                "X: %{x}",
                "Y: %{y}",
                f"{self.vector_label}: %{{customdata}}",
            ])
        )
        fig.update_layout(
            title={
                "text": plot_title,
                "y": 0.9,
                "x": 0.05,
                "xanchor": "left",
                "yanchor": "top",
                "font": {"size": 12},
            },
            xaxis_title=str(self.x_axis_value),
            yaxis_title=str(self.y_axis_value),
        )

        """
        Show trendline
        """
        projection_matrix = np.array(df[[str(self.x_axis_value), str(self.y_axis_value)]])
        fig.add_trace(
            go.Scatter(
                x=[projection_matrix.min(), projection_matrix.max()],
                y=[projection_matrix.min(), projection_matrix.max()],
                mode="lines",
                line=go.scatter.Line(color="gray"),
                showlegend=False
            )
        )
        self.fig = fig
        self.df = df
        
        return self.fig

    
    def _generate_hover_template(
        self, 
        df: pd.DataFrame,
        labels: List[str]
    ) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Generating hover template
        """
        custom_data = df[labels]
        custom_data_hover = [
            f"{c}: %{{customdata[{i}]}}"
            for i, c in enumerate(labels)
        ]
        hovertemplate = (
            "<br>".join(
                ["X: %{x}   Y: %{y}"]
                + custom_data_hover
            )
            + "<extra></extra>"
        )

        return custom_data, hovertemplate

        