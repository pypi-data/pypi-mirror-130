#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####
# Author: Charlene Leong charleneleong84@gmail.com
# Created Date: Thursday, October 21st 2021, 11:24:13 pm
# Last Modified: Friday, October 22nd 2021,4:22:22 am
#####

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from typing import List, Dict, Tuple, Union

from nn_utils import get_nn_idx

from constants import *


## TODO: Refactor into class

def plot_projection_df(
    projection_matrix: np.ndarray,
    axes_matrix: np.ndarray,
    x_axis_value: VectorOperation,
    y_axis_value: VectorOperation,
    dataset_info: dict,
    plot_nn: Union[None, int] = None, 
    plot_labels: bool = False
):
    """
    Takes projection matrix and returns df
    """
    
    def build_projection_df():
        """
        Build project df from projection matrix
        """
        if not plot_nn:
            labels_df = pd.DataFrame(dataset_info['vectors_lut'].keys(), 
                                        columns=[dataset_info['vector_label']])
            data_df = pd.DataFrame(projection_matrix, 
                                   columns=[str(x_axis_value), str(y_axis_value)])
            legend = None
        else:
            search_vector_nn_idx_1 = get_nn_idx(vectors=dataset_info['vectors'], 
                                                selected_vec=axes_matrix[0])
            nn_1_labels = dataset_info['metadata'][[dataset_info['vector_label']]].loc[search_vector_nn_idx_1][:plot_nn]
            nn_1_labels[''] = 'x'
            
            search_vector_nn_idx_2 = get_nn_idx(vectors=dataset_info['vectors'], 
                                                selected_vec=axes_matrix[1])
            nn_2_labels = dataset_info['metadata'][[dataset_info['vector_label']]].loc[search_vector_nn_idx_2][:plot_nn]
            nn_2_labels['neighbours'] = 'y'
            
            labels_df =  pd.concat([nn_1_labels, nn_2_labels], axis=0).reset_index()
            data_df = pd.DataFrame(projection_matrix[labels_df.index], 
                                    columns=[str(x_axis_value), str(y_axis_value)])
            legend = 'neighbours'
            
        return pd.concat([labels_df, data_df], axis=1), legend
    
    

    def clean_vector_op_label(axis_value: VectorOperation) -> str:
        """
        Converting operation tuple to axis label for px scatter
        """
        return ''.join(c for c in str(axis_value).replace(',', ',<br>') if c not in set('",()\]\''))
    
    
    df, legend = build_projection_df()
    text = df[dataset_info['vector_label']] if (plot_labels) else None

    labels = {}
    for axis in [ str(x_axis_value), str(y_axis_value) ]:
        if axis.op is None:
            labels[str(axis)] = axis.query
        else:
            labels[str(axis)] = '<br>'.join(axis.to_list())

    fig = px.scatter(df, x=str(x_axis_value), y=str(y_axis_value), color=legend, text=text,
                        title=f"{dataset_info['dataset_id']}: {len(df)} points<br>{dataset_info['vector_label']}: {dataset_info['vector_name']}",
                        labels=labels
                    )
    
    """
    Adding product name to hover data
    """
    fig.update_traces(customdata=df[dataset_info['vector_label']])
    fig.update_traces(hovertemplate='%{customdata}')
    fig.update_traces(
        hovertemplate="<br>".join([
            "X: %{x}",
            "Y: %{y}",
            "Label: %{customdata}",
        ])
    )
    fig.update_traces(
        hovertemplate="<br>".join([
            "X: %{x}",
            "Y: %{y}",
            "Label: %{customdata}",
        ])
    )
    fig.update_layout(
        title_font_size=10,
    )   


    """
    Show trendline
    """
    projection_matrix = np.array(df[[str(x_axis_value), str(y_axis_value)]])
    fig.add_trace(
        go.Scatter(
            x=[projection_matrix.min(), projection_matrix.max()],
            y=[projection_matrix.min(), projection_matrix.max()],
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False)
    )

#     fig.show()
    return fig, df