 # -*- coding: utf-8 -*-
import re
import os
import json
import pandas as pd
import numpy as np
from typing import Union, List


def df_reader(data_path, header: Union[int, None] = 0, usecols: Union[List[Union[str, int]], None] = None ,sep='\t', sheet_name=0) -> pd.DataFrame:
    if data_path.endswith('json'):
        df_data = pd.read_json(data_path)
    elif data_path.endswith('jsonl'):
        df_data = pd.read_json(data_path, lines=True)
    elif data_path.endswith('xlsx'):
        df_data = pd.read_excel(data_path, header=header, usecols=usecols, sheet_name=sheet_name)
    elif data_path.endswith('.pkl'):
        df_data = pd.read_pickle(data_path)
    elif data_path.endswith('csv'):
        df_data = pd.read_csv(data_path, header=header, usecols=usecols, sep=sep)
    elif data_path.endswith('.parquet'):
        df_data = pd.read_parquet(data_path)
    else:
        raise AssertionError(f'not supported file type:{data_path}, suport types: json, jsonl, xlsx, csv')
    return df_data

def df_saver(df: pd.DataFrame, data_path):
    if data_path.endswith('json'):
        df.to_json(data_path, orient='records', force_ascii=False)
    if data_path.endswith('jsonl'):
        df.to_json(data_path, orient='records', force_ascii=False, lines=True)
    elif data_path.endswith('xlsx'):
        df2xlsx(df, data_path, index=False)
    elif data_path.endswith('csv'):
        df.to_csv(data_path)
    else:
        raise AssertionError(f'not supported file type:{data_path}, suport types: json, jsonl, xlsx, csv')
    

def extract_all_json(text, merged_return=True):
    json_strings = re.findall(r'\{[^}]*\}', text)
    json_dicts = [json.loads(j) for j in json_strings]
    if not merged_return:
        return json_dicts
    else:
        single_dict = {}
        for dict_obj in json_dicts:
            single_dict.update(dict_obj)
        return single_dict

def extract_last_json(text) -> dict:
    json_str = re.search(r'\{[^}]*\}(?=[^{}]*$)', text).group()
    json_data = json.loads(json_str)
    return json_data

def extract_scores_bk(text) -> dict:
    pattern = r"([A-Z])'?[:.]\s*([\d.]+)"
    result = re.findall(pattern, text)
    scores = {item[0]: float(item[1]) for item in result}    
    return scores

def extract_scores(text) -> float:
    pattern = r"([A-Z])['\"]?[:.]\s*([\d.]+|\"[\d.]+\")"
    result = re.findall(pattern, text)
    scores = {item[0]: float(item[1].replace("\"", "")) for item in result}    
    return scores 

def extract_numbers(text):
    pattern = r"[-+]?\d*\.\d+|\d+"
    result = re.findall(pattern, text)
    return [float(i) if '.' in i else int(i) for i in result]


def df2xlsx(df: pd.DataFrame, save_path: str, sheet_name='Sheet1', mode='w', index=False):
    if mode not in ['w', 'a']:
        raise AssertionError('mode not in [\'w\', \'a\']')
    if mode == 'a' and not os.path.isfile(save_path):
        mode = 'w'
    if mode == 'a':
        engine = 'openpyxl'
    else:
        engine = 'xlsxwriter'

    with pd.ExcelWriter(save_path, engine=engine, mode=mode) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=index)

        
def load_jsonl(data_path: str, obj_item: bool=True):
    if obj_item: 
        return [json.loads(l.rstrip(',')) for l in open(data_path, "r")] 
    return [l for l in open(data_path, "r")] 

    
def load_json(save_path: str) -> dict:
    with open(save_path, "r", encoding='utf8') as openfile:
        return json.load(openfile)


def save_json(json_obj, save_path: str, ensure_ascii=False):
    assert isinstance(json_obj, (dict, list))
    with open(save_path, "w", encoding='utf8') as openfile:
        json.dump(json_obj, openfile, ensure_ascii=ensure_ascii, indent=2)

        
def generate_letters(length, upcase=True):
    return [chr(ord('A' if upcase else 'a') + i) for i in range(length)]
    

def binary_cross_entropy(y_pred, y_true):
    y_true = np.array(y_true).astype(np.float32)
    y_pred = np.array(y_pred).astype(np.float32)
    y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)  # avoid log(0)
    y_true = np.clip(y_true, 1e-7, 1 - 1e-7)  # avoid log(0)
    bce = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return np.round(bce, 4)