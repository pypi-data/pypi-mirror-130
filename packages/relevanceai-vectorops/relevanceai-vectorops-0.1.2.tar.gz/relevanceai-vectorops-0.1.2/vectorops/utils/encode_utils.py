#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####
# Author: Charlene Leong charleneleong84@gmail.com
# Created Date: Friday, October 22nd 2021, 1:12:15 am
# Last Modified: Friday, October 22nd 2021,4:21:19 am
#####

import numpy as np
import clip
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


def clip_encode_text(sequence: str, norm: bool = False) -> np.ndarray:
    '''Computes the text vectors for text sequence'''
    with torch.no_grad():
        text_encoded = model.encode_text(clip.tokenize(sequence).to(device))
        if norm: text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    return text_encoded.cpu().numpy()[0]



def get_search_word_vector(
    search_word: str,
    dataset_info: dict
) -> np.ndarray:
    '''
    Return average of search word vectors of a given search word
    '''
    vector_labels = dataset_info['labels'][dataset_info['vector_label']].apply(lambda x : x.lower())
    search_word_mask = vector_labels.str.contains(search_word.lower())
    search_word_vectors = dataset_info['vectors'][search_word_mask]
    if search_word_vectors.shape[0] >= 5:
        search_word_vectors = search_word_vectors[:5]
    return  np.mean(search_word_vectors, axis=0)