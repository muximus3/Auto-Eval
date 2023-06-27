import os
from typing import List
import abc
import json
from eval.utils import load_json, generate_letters, extract_last_json, extract_scores

class Prompter(abc.ABC):
    @abc.abstractmethod
    def generate_prompt(**kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    def extract_result_from_response(response):
        raise NotImplementedError

class EvalPrompter(Prompter):
    __slots__ = ( "eval_with_target_template", "eval_without_target_template", "_verbose")

    @classmethod
    def from_config(cls, prompt_template_file: str, verbose: bool = True):
        if not os.path.exists(prompt_template_file):
            raise ValueError(f'File not exists:{prompt_template_file}')
        template_data = load_json(prompt_template_file)
        eval_with_target_template = template_data['eval_with_target_template']
        eval_without_target_template = template_data[ 'eval_without_target_template']
        if verbose:
            print(f'Using prompt template:\n {json.dumps(template_data, sort_keys=True, indent=2)}')
        return cls(eval_with_target_template, eval_without_target_template, verbose)

    def __init__(self,
                 eval_with_target_template: str,
                 eval_without_target_template: str,
                 verbose: bool = True) -> None:
        self._verbose = verbose
        self.eval_with_target_template = eval_with_target_template
        self.eval_without_target_template = eval_without_target_template

    def generate_prompt(self, question: str, target: str,
                        candidate_answers: List[str]) -> str:
        """
        Generate a prompt based on the given question, target, and candidate answers.
        """
        candidate_answer_numbers = generate_letters(len(candidate_answers))
        format_option_data = '\n\n'.join([
            f'**{candidate_answer_numbers[i]}**. {candidate_answers[i]}'
            for i in range(len(candidate_answers))
        ])

        if target:
            eval_prompt = self.eval_with_target_template.format(
                question=question, target=target, answers=format_option_data)
        else:
            eval_prompt = self.eval_without_target_template.format(
                question=question, answers=format_option_data)
        if self._verbose:
            print(
                f"\n{'-'*20} prompt detail 🚀  {'-'*20}\n\n{eval_prompt}\n\n{'-'*20} prompt end {'-'*20}"
            )
        return eval_prompt

    def extract_result_from_response(self, response: str) -> List[float]:
        """
        Extract the result (scores) from the given model response.
        """
        if self._verbose:
            print(
                f"{'-'*20} response detail ⭐️ {'-'*20}\n\n{response}\n\n{'-'*20} response end {'-'*20}\n"
            )
        try:
            result_json = extract_last_json(response.strip())
        except (AttributeError, json.decoder.JSONDecodeError):
            result_json = extract_scores(response.strip())
        scores = list(map(lambda x: float(x), result_json.values()))
        return scores