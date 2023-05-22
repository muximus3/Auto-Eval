# -*- coding: utf-8 -*-
import os
import pandas as pd
import traceback
from typing import Union, List
import random
from tqdm import tqdm
from typing import Optional, Tuple
import time
import sys
from dataclasses import dataclass
from oneapi import OneAPITool
sys.path.append(os.path.normpath(f'{os.path.dirname(os.path.abspath(__file__))}/..'))
from eval.utils import df_saver, df_reader
from eval.prompt_template import Prompter


def eval_one_qa(
             api_tool: OneAPITool,
             eval_prompter: Prompter,
             question: str,
             candidate_answers: List[str],
             target: Union[str, None]='',
             engine: str='',
             temperature=0.1,
             max_new_tokens=2048) -> Tuple[Union[List[float], None], str]:
    raw_response = ''
    eval_prompt = eval_prompter.generate_prompt(question, target,
                                                candidate_answers)
    try:
        raw_response = api_tool.simple_chat(eval_prompt,
                                      model=engine,
                                      temperature=temperature,
                                      max_new_tokens=max_new_tokens)
        scores = eval_prompter.extract_result_from_response(raw_response)
        return scores, raw_response
    except Exception as e:
        print(f'error, request result:{raw_response}, exception:{e}')
        traceback.print_exc()
        return None, raw_response


def eval_one_group(
    api_tool: OneAPITool,
    eval_prompter: Prompter,
    data_group: pd.DataFrame,
    engine: str,
    temperature=0.1,
    max_new_tokens=2048,
) -> Union[pd.DataFrame, None]:
    group = data_group.reset_index(drop=True)
    question = group['question'].unique()[0]
    candidate_answers = group['output']
    if 'target' in data_group.keys():
        target = group['target'].unique()[0]
    else:
        target = ''
    scores, raw_response = eval_one_qa(api_tool=api_tool,
                      eval_prompter=eval_prompter,
                      question=question,
                      candidate_answers=candidate_answers,
                      target=target,
                      engine=engine,
                      temperature=temperature,
                      max_new_tokens=max_new_tokens)
    if scores is not None and len(scores) == len(candidate_answers):
        group.at[0, 'raw_response'] = raw_response
        for i in range(len(scores)):
            group.at[i, 'score'] = scores[i]
        return group
    else:
        return None



def prepare_eval_data(eval_data_path: List[str], eval_categories: Optional[List[str]] = None, sample_num: int=0, eval_models: Optional[List[str]] = None) -> Tuple[List[pd.DataFrame],List[pd.DataFrame] ]:
    eval_data = df_reader(eval_data_path[0]) if len(eval_data_path) == 1 else pd.concat([df_reader(file_path) for file_path in eval_data_path])
    eval_data = eval_data.fillna('')
    if len({'instruction', 'input', 'output'} - set(eval_data.keys())) == 0:
        eval_data['question'] = eval_data['instruction'].str.cat(
            eval_data['input'], sep=' ')
    elif len({'prompt', 'output'} - set(eval_data.keys())) == 0:
        eval_data['quesion'] = eval_data['prompt'].copy()
    elif len({'question', 'answer'} - set(eval_data.keys())) == 0:
        eval_data['output'] = eval_data['answer'].copy()
    elif len({'question', 'output'} - set(eval_data.keys())) == 0:
        pass
    else:
        raise KeyError(
            f'Eval data columns must be either: ["instruction", "input", "output"] or ["prompt", "output"] or ["question", "output"]'
        )
    # filter specific categories
    if eval_categories is not None and len(
            eval_categories) > 0 and 'category' in eval_data.keys():
        eval_data = eval_data[eval_data['category'].isin(eval_categories)]
    if eval_models is not None and len(
            eval_models) > 0 and 'model' in eval_data.keys():
        eval_data = eval_data[eval_data['model'].isin(eval_models)]
    grouped = eval_data.groupby(by=['question'])
    if sample_num > 0:
        sample_keys = random.sample(grouped.groups.keys(), sample_num)
    else:
        sample_keys = grouped.groups.keys()
    total_groups =  [grouped.get_group(key) for key in sample_keys]
    scored_groups = []
    unscored_groups = []
    for group in total_groups:
        if 'score' in group.keys() and group['score'].map(lambda x: x if x != '' and x == x else None).count() == len(group):
            group['score'] = group['score'].map(float)
            scored_groups.append(group)
        else:
            unscored_groups.append(group)
    return scored_groups, unscored_groups
     

def log_score_results(eval_results_df: pd.DataFrame, score_by: List[str]):
    if 'model' in eval_results_df.keys():
        score_models = eval_results_df.groupby('model')['score'].apply(lambda x: f'{x.sum():.1f}/{len(x)}')
        print(f'{"-"*20} Scores by \'model\' {"-"*20}\n{score_models.to_markdown()}')
        if 'category' in eval_results_df.keys():
            score_category = eval_results_df.groupby([
                'model', 'category'
            ])['score'].apply(lambda x: f'{x.sum():.1f}/{len(x)}').reset_index().sort_values(by=['category', 'model'])
            print(
                f'\n{"-"*20} Scores by [\'model\', \'category\'] {"-"*20}\n{score_category.to_markdown(index=False)}'
            )
    if score_by is not None and len(score_by) > 0:
        scores = eval_results_df.groupby(score_by)['score'].apply(lambda x: f'{x.sum():.1f}/{len(x)}').reset_index().sort_values(by=score_by)
        print(
            f'\n{"-"*20} Scores by {score_by} {"-"*20}\n{scores.to_markdown(index=False)}'
        )
        
def evaluation_prompt_acc(eval_result_df: pd.DataFrame):
    if 'targe_score' in eval_result_df.keys():
        pass

def save_results(results_df: pd.DataFrame, output_path: str):
    print(f'Saving evaluation results: {output_path}')
    df_saver(results_df, output_path)
    print(f'Saved successfully.')

@dataclass
class EvalConfig:
    api_config_file: str
    eval_prompter: Prompter
    eval_data_path: str
    output_path: str = ''
    engine: str = ''
    eval_categories: Optional[List[str]] = None
    eval_models: Optional[List[str]] = None
    score_by: Optional[List[str]] = None
    sample_num: int = 0
    request_interval: int = 1
    retry: bool = True
    temperature: float = 0.1
    max_new_tokens: int = 2048

def eval_groups(
    eval_config: EvalConfig
):
    # Preparing data
    scored_groups, unscored_groups = prepare_eval_data(eval_config.eval_data_path, eval_config.eval_categories, eval_config.sample_num, eval_config.eval_models)

    # Init api tool and prompter
    tool = OneAPITool.from_config_file(config_file=eval_config.api_config_file)

    failed_groups = []
    for group in tqdm(unscored_groups):
        result = eval_one_group(tool, eval_config.eval_prompter,  group,  eval_config.engine, eval_config.temperature, eval_config.max_new_tokens)
        if result is not None:
            scored_groups.append(result)
        else:
            failed_groups.append(group)
        time.sleep(eval_config.request_interval)

    # Retry failed requests
    if len(failed_groups) > 0 and eval_config.retry:
        for group in tqdm(failed_groups.copy(), desc='RETRY'):
            result = eval_one_group(tool, eval_config.eval_prompter,  group,  eval_config.engine, eval_config.temperature, eval_config.max_new_tokens)
            if result is not None:
                scored_groups.append(result)
                failed_groups = [df for df in failed_groups if not df.equals(group)]
            time.sleep(eval_config.request_interval)

    scored_results_df = pd.concat(scored_groups)
    log_score_results(eval_results_df=scored_results_df, score_by=eval_config.score_by)
    # Log score results
    print(f'Eval engine: {eval_config.engine}')
    print(f'Eval files: {eval_config.eval_data_path}')
    print(f'Failed requests: {len(failed_groups)}/{len(scored_groups) + len(failed_groups)}')
    results_df = pd.concat([scored_results_df, pd.concat(failed_groups)]) if len(failed_groups) > 0 else scored_results_df
    # Save results
    if eval_config.output_path:
        save_results(results_df=results_df, output_path=eval_config.output_path)
