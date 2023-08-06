#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#####
# Author: Charlene Leong charleneleong84@gmail.com
# Created Date: Friday, October 22nd 2021, 12:05:11 am
# Last Modified: Friday, October 22nd 2021,2:55:27 am
#####



from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PATH = Path(__file__).parent
DATA_PATH = BASE_DIR / 'data'

MAX_VECTORS = 7000

data_dict = {
    # 'ecommerce-6.uniq_id.7000.product_name_imagetext.7000.max': pd.read_csv(
    #     DATA_PATH.joinpath('ecommerce-6.uniq_id.7000.product_name_imagetext.7000.csv'), 
    #     encoding='utf-8'
    # ),
    # 'ecommerce-6.uniq_id.7000.product_name_imagetext.7000.metadata': pd.read_csv(
    #     DATA_PATH.joinpath('ecommerce-6.uniq_id.7000.product_name_imagetext.7000.metadata.csv'), 
    #     encoding='utf-8'
    # ),
    # 'ecommerce-6.product_name.5362.product_name_imagetext.5000': pd.read_csv(
    #     DATA_PATH.joinpath('ecommerce-6.product_name.5362.product_name_imagetext.5000.csv'), 
    #     encoding='utf-8'
    # ),
    # 'ecommerce-6.13058.max': pd.read_json(
    #     DATA_PATH.joinpath('ecommerce-6', 'ecommerce-6.13058.max.json'), 
    #     encoding='utf-8'
    # ),
    'ecommerce-6.7000.max': pd.read_json(
        DATA_PATH.joinpath('ecommerce-6', 'ecommerce-6.7000.max.json'), 
        encoding='utf-8'
    ),
    'ecommerce-6.7000.metadata': pd.read_csv(
        DATA_PATH.joinpath('ecommerce-6', 'ecommerce-6.7000.metadata.csv'), 
        encoding='utf-8'
    ),
}
