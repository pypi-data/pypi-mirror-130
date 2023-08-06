#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from dataclasses import dataclass
from doc_utils import DocUtils

from typing import List, Dict, Tuple, Union, Optional, Any

from vectorops.constants import *
from vectorops.utils.distance_utils import *
from vectorops.dataset_manager import DatasetManager
from vectorops.projection_manager import ProjectionManager
from vectorops.projection.scatter import ScatterProjection

from vectorhub.base import Base2Vec
from vectorhub.encoders.text.sentence_transformers import SentenceTransformer2Vec
from vectorhub.bi_encoders.text_image.torch import ClipText2Vec

MARKER_SIZE = 8

@dataclass
class VectorDataset(DocUtils):
    dataset_id: str
    docs: Dict[str, Any]
    vector_label: str
    vector_field: str
    encoder: Union[Base2Vec, SentenceTransformer2Vec, ClipText2Vec]
    norm: bool
        
    def __post_init__(self):
        self.vectors = np.array(self.get_field_across_documents(self.vector_field, self.docs, missing_treatment='raise_error'))
        if self.norm: self.vectors /= np.linalg.norm(self.vectors, axis=1).reshape(-1, 1)
        self.labels = np.array(self.get_field_across_documents(self.vector_label, self.docs, missing_treatment='raise_error'))
    
    def __len__(self):
        return len(self.vectors)
    
    @property
    def vector_field_len(self):
        return len(self.vectors[0])



# @dataclass
# class ComparatorDataset(DocUtils):
#     def __init__(self, 
#              vectors_1: VectorDataset, 
#              vectors_2: VectorDataset, 
#         ):
#         super().__init__()
#         self.vectors_1 = vectors_1
#         self.vectors_2 = vectors_2
#         assert self.vectors_1.vector_field_len == self.vectors_2.vector_field_len
#         self.vector_field_len = self.vectors_1.vector_field_len
    
#     @property
#     def vectors_1_len(self):
#         return len(self.vectors_1)
    
#     @property
#     def vectors_2_len(self):
#         return len(self.vectors_2)
    



@dataclass 
class EmbeddingComparator(ScatterProjection):
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
        self.x_axis_value = x_axis_value
        self.y_axis_value = y_axis_value
        self.encoder = encoder
        self.plot_unique = plot_unique
        self.plot_nn = plot_nn
        self.plot_labels = plot_labels
        super().__init__(dm=dm, 
                x_axis_value=x_axis_value, y_axis_value=y_axis_value, 
                encoder=encoder, plot_unique=plot_unique, plot_nn=plot_nn, plot_labels=plot_labels
                )

    
    def compare_vector_fields(
        self,
        dataset_id: str,
        docs: List[Dict[str, Any]],
        vector_field_1: str,
        vector_field_2: str,
        vector_label: str,
        encoder_1: Optional[Union[Base2Vec, SentenceTransformer2Vec]] = SentenceTransformer2Vec('msmarco-distilbert-dot-v5'),
        encoder_2: Optional[Union[Base2Vec, SentenceTransformer2Vec]] = SentenceTransformer2Vec('msmarco-distilbert-dot-v5'),
        norm: bool = True,
        norm_range: bool = True,

        vector_label_char_length: Union[None, int] = 20,
        plot_nn: Optional[Union[None, int]] = None, 
        plot_labels: Optional[bool] = False,
        overlap_only: bool = True,
        
        sequences: Optional[List[str]] = None,
        marker_size: int = MARKER_SIZE,
    ):
        """
        Plots scatter plot of the projection of the dataset
        """
        self.dataset_id = dataset_id
        self.vector_label_char_length = vector_label_char_length
        self.plot_nn = plot_nn
        self.plot_labels = plot_labels

        palette = ['rgb(59,216,195)', 'rgb(251,195,51)']
        plot_mode = "markers+text" if plot_labels else "markers"
        plot_title = f"<b>Embedding Comparator Plot<br></b>"
        plot_title = plot_title.replace("</b>", f"Dataset: {dataset_id}<br></b>")
        plot_title = plot_title.replace("</b>", f"Vector Label: {vector_label}<br></b>")
        if plot_nn:
            if overlap_only: 
                plot_title = plot_title.replace("</b>", f"NN: {plot_nn}</b>\t")
            else:
                plot_title = plot_title.replace("</b>", f"NN from each axis: {plot_nn}</b>\t")
        
        vectors_1 = VectorDataset(dataset_id=dataset_id, docs=docs, 
                                vector_label=vector_label, vector_field=vector_field_1, encoder=encoder_1, norm=norm)
        vectors_2 = VectorDataset(dataset_id=dataset_id, docs=docs, 
                                vector_label=vector_label, vector_field=vector_field_2, encoder=encoder_2, norm=norm)
        labels = vectors_1.labels
        label_df = pd.DataFrame(docs, columns=[vector_label])

        data = []
        comparator_df = pd.DataFrame()
        """
        Compute axes matrix
        """
        for vector_dataset in [ vectors_1, vectors_2 ]:
            """
            Plotting projection matrix
            """
            vectors = vector_dataset.vectors
            if norm_range:
                vectors =  min_max_norm( vectors, vectors.min(), vectors.max() )

            encoder = vector_dataset.encoder
            vector_field = vector_dataset.vector_field
            vector_field_len = vector_dataset.vector_field_len

            projection_matrix, axes_matrix = self._projection( vectors=vectors, encoder=encoder )
            if norm_range:
                projection_matrix = min_max_norm( projection_matrix, projection_matrix.min(), projection_matrix.max() )
                axes_matrix = min_max_norm( axes_matrix, axes_matrix.min(), axes_matrix.max() )

            """
            Preparing plot figure
            """
            df, legend = self._build_projection_df(
                projection_matrix=projection_matrix, 
                axes_matrix=axes_matrix,
                vectors=vectors,
                labels=labels,
                vector_label=vector_label,
                vector_field=vector_field,
                metadata_df=label_df,
                plot_nn=plot_nn,
                # plot_unique=self.plot_unique,
                overlap_only=overlap_only
            )
            
            if plot_nn:
                groups = df.groupby(legend)
                for idx, val in groups:
                    text = val[vector_label] if (plot_labels) else None
                    if self.vector_label_char_length:
                        text = val[vector_label].apply( lambda x: x[: self.vector_label_char_length ] + "..." )
                    
                    custom_data, hovertemplate = self._generate_hover_template(df=val, labels=[vector_label, legend])
                    scatter = go.Scatter(
                            name=idx,
                            x=val[str(self.x_axis_value)],
                            y=val[str(self.y_axis_value)],
                            mode=plot_mode,
                            marker={"size": marker_size, "symbol": "circle"},
                            text=text,
                            textposition="middle center",
                            customdata=custom_data,
                            hovertemplate=hovertemplate,
                        )
                    data.append(scatter)
                    
            else:
                # df = df.rename(columns={vector_label: vector_field})
                text = df[vector_label] if (plot_labels) else None
                if self.vector_label_char_length:
                    text = df[vector_label].apply( lambda x: x[: self.vector_label_char_length ] + "..." )
                
                custom_data, hovertemplate = self._generate_hover_template(df=df, labels=[vector_label])
                scatter = go.Scatter(
                        name=vector_field,
                        x=df[str(self.x_axis_value)],
                        y=df[str(self.y_axis_value)],
                        mode=plot_mode,
                        marker={"size": marker_size, "symbol": "circle"},
                        text=text,
                        textposition="middle center",
                        customdata=custom_data,
                        hovertemplate=hovertemplate,
                    )
                data.append(scatter)
            
            if (not comparator_df.empty) and overlap_only:
                data = []
                overlap_df = pd.merge(comparator_df, df, on=[vector_label], how="inner")
                
                vectors_1_df = overlap_df[[vector_label, f'{str(self.x_axis_value)}_x', f'{str(self.y_axis_value)}_x']]
                vectors_1_df = vectors_1_df.rename(columns={
                    f'{str(self.x_axis_value)}_x': str(self.x_axis_value), 
                    f'{str(self.y_axis_value)}_x': str(self.y_axis_value), 
                    }
                )
                vectors_1_df = vectors_1_df.groupby([vector_label], sort=False).mean().reset_index()
                vectors_1_df['vector_field'] = vector_field_1
                if plot_nn: 
                    vectors_1_df['neighbours'] = overlap_df[['neighbours_x']]
                    vectors_1_df = vectors_1_df[:plot_nn]

                vectors_2_df = overlap_df[[vector_label, f'{str(self.x_axis_value)}_y', f'{str(self.y_axis_value)}_y']]
                vectors_2_df = vectors_2_df.rename(columns={
                    f'{str(self.x_axis_value)}_y': str(self.x_axis_value), 
                    f'{str(self.y_axis_value)}_y': str(self.y_axis_value), 
                    }
                )
                vectors_2_df = vectors_2_df.groupby([vector_label], sort=False).mean().reset_index()
                vectors_2_df['vector_field'] = vector_field_2
                if plot_nn: 
                    vectors_2_df['neighbours'] = overlap_df[['neighbours_y']]
                    vectors_2_df = vectors_2_df[:plot_nn]
                
                '''
                Plot overlap dfs
                '''
                for i, vectors_df in enumerate([ vectors_1_df, vectors_2_df ]):
                    text = vectors_df[vector_label] if (plot_labels) else None
                    if self.vector_label_char_length:
                        text = vectors_df[vector_label].apply( lambda x: x[: self.vector_label_char_length ] + "..." )
                    
                    labels = [vector_label, 'neighbours'] if plot_nn else [vector_label]
                    custom_data, hovertemplate = self._generate_hover_template(df=vectors_df, labels=labels)
                    scatter = go.Scatter(
                            name=str(vectors_df.vector_field.values[0]),
                            x=vectors_df[str(self.x_axis_value)],
                            y=vectors_df[str(self.y_axis_value)],
                            mode=plot_mode,
                            marker={"size": marker_size, "symbol": "circle"},
                            text=text,
                            textposition="middle center",
                            customdata=custom_data,
                            hovertemplate=hovertemplate,
                            marker_color=palette[i]
                        )
                    data.append(scatter)

                vectors_1_df = vectors_1_df.rename(columns={vector_label: vector_field_1})
                vectors_2_df = vectors_2_df.rename(columns={vector_label: vector_field_2})
                comparator_df = pd.concat([vectors_1_df, vectors_2_df], axis=1).drop(columns='vector_field')

            else:
                comparator_df = pd.concat([comparator_df, df], axis=1)


        """
        Plot title
        """
        # plot_title = plot_title.replace("</b>", f"\tEncoder: {self.encoder}</b>")
        if self.plot_unique:
            plot_title =  plot_title.replace("</b>", f"\tUnique: {self.plot_unique}</b>\t")
        if self.vector_label_char_length:
            plot_title = plot_title.replace("</b>", f"\tChar Length: {self.vector_label_char_length}<br></b>\t")
            
        """
        Generating figure and formatting title and legend
        """
        axes = {
            "title": plot_title,
            "showgrid": True,
            "zeroline": True,
            "showticklabels": False,
        }
        layout = go.Layout(scene={"xaxis": axes, "yaxis": axes})
        fig = go.Figure(data=data, layout=layout)
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
        fig.update_layout(
            legend={
                "font": {"size": 10},
                "itemwidth": 30,
                "tracegroupgap": 1,
            }
        )

        """
        Show line between vectors 1 and vectors 2
        """
        if overlap_only:
            vectors_1_pts = list(zip(vectors_1_df[str(self.x_axis_value)].values, vectors_1_df[str(self.y_axis_value)].values))
            vectors_2_pts = list(zip(vectors_2_df[str(self.x_axis_value)].values, vectors_2_df[str(self.y_axis_value)].values))
            
            for vectors_1_xy, vectors_2_xy in zip(vectors_1_pts, vectors_2_pts):
                fig.add_trace(
                    go.Scatter(
                        x=[ vectors_1_xy[0], vectors_2_xy[0] ],
                        y=[ vectors_1_xy[1], vectors_2_xy[1] ],
                        mode="lines",
                        line=go.scatter.Line(color="darkslategray", dash="dash", width=0.5),
                        showlegend=False,
                    )
                )  

        """
        Show trendline
        """
        projection_points = np.array( comparator_df[[str(self.x_axis_value), str(self.y_axis_value)]] )
        projection_points_min = projection_points.min()
        projection_points_max = projection_points.max()

        fig.add_trace(
            go.Scatter(
                x=[ projection_points_min, projection_points_max ],
                y=[ projection_points_min, projection_points_max ],
                mode="lines",
                line=go.scatter.Line(color="dimgray", width=0.6),
                showlegend=False
            )
        )
        self.fig = fig
        self.df = comparator_df

        return fig

        