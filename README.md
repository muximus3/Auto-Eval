# Auto-Eval

**Auto-Eval** utilizes ChatGPT (GPT-3.5-turbo), GPT-4, and Claude's API to evaluate language models with a single command. By default, it assesses the accuracy of language models in various aspects, including mathematical calculations, question answering, translation, classification, and more. The prompt has been thoroughly tested to maximize evaluation accuracy while using as few words as possible to save token budget, as GPT-4 is quite expensive💰.

You can also customize the prompt by adjusting it based on templates. We have integrated various GPT APIs into a unified interface using the [One-API-Tool](https://github.com/muximus3/OneAPI) library for maximum customization and further development.


## Installation
```sh
pip install -U auto-eval
```

## Usage
### 1. Set up your API Key information in the local configuration file.

OpenAI config:
```json
{
    "api_key": "YOUR_API_KEY",
    "api": "https://api.openai.com/v1",
    "api_type": "open_ai"
}
```
Azure OpenAI config:
```json
{
    "api_key": "YOUR_API_KEY",
    "api": "Replace with your Azure OpenAI resource's endpoint value.",
    "api_type": "azure"
}
```
Anthropic config:
```json
{
    "api_key": "YOUR_API_KEY",
    "api": "https://api.anthropic.com",
    "api_type": "claude"
}
```
`api_key`: Obtain your OpenAI API key from the [OpenAI website](https://platform.openai.com/account/api-keys) and your Claude API key from the [Anthropic website](https://console.anthropic.com/account/keys).

`api`: The base API used to send requests. You may also specify a proxy URL like: "https://your_proxy_domain/v1". For Azure APIs, you can find relevant information on the Azure resource dashboard. The API format is usually: `https://{your_organization}.openai.azure.com/`.

`api_type`: Currently supported values are "open_ai", "azure", or "claude".



### 2. Use with command lines
#### Evaluate one sample
```sh
auto-eval line --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--model gpt-3.5-turbo \
--prompt "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?" \
--answers 20 100 21 18 \
--target "Janet sells 16 - 3 - 4 = <<16-3-4=9>>9 duck eggs a day. She makes 9 * 2 = $<<9*2=18>>18 every day at the farmer’s market. #### 18"
```
Print output:
```text
Using prompt template:
 {
  "eval_with_target_instruction": "Please evaluate and comment each [Candidate answer] based on the [Correct answer]. Then output all [Candidate answer] scores (0-1) in a summary format of {\"number\": \"score\"}, e.g, {\"A\": \"0.2\", \"B\": \"0.8\"}",
  "eval_with_target_template": "[Question]: {q}\n\n[Correct answer]: {target}\n\n[Candidate answer]:\n{options}\n\n[System]:\n{instruction}",
  "eval_without_target_instruction": "Please solve the [Question] independently to obtain the [Correct answer], and then evaluate and comment each [Candidate answer] based on the [Correct answer]. Finally, output all [Candidate answers] scores (0-1) in a summary format of {\"number\": \"score\"}, e.g, {\"A\": \"0.2\", \"B\": \"0.8\"}",
  "eval_without_target_template": "[Question]: {q}\n\n[Candidate answer]:\n{options}\n\n[System]:\n{instruction}"
}

-------------------- prompt detail 🚀  --------------------

[Question]: Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for  per fresh duck egg. How much in dollars does she make every day at the farmers' market?

[Correct answer]: Janet sells 16 - 3 - 4 = <<16-3-4=9>>9 duck eggs a day. She makes 9 * 2 = $<<9*2=18>>18 every day at the farmer’s market. #### 18

[Candidate answer]:
A. 20
B. 100
C. 21
D. 18

[System]:
Please evaluate and comment each [Candidate answer] based on the [Correct answer]. Then output all [Candidate answer] scores (0-1) in a summary format of {"number": "score"}, e.g, {"A": "0.2", "B": "0.8"}

-------------------- prompt end --------------------
-------------------- response detail ⭐️ --------------------

 Here are the evaluations and scores for each [Candidate answer]:

A. 20 
Comment: Incorrect. The correct calculation is 16 - 3 - 4 = 9 eggs sold. 9 * $2 = $18. 
Score: 0

B. 100
Comment: Incorrect. The calculation overestimates the number of eggs sold and the price per egg. 
Score: 0  

C. 21
Comment: Incorrect. The calculation is close but rounds up the number of eggs sold to 10 instead of 9. 
Score: 0.2  

D. 18
Comment: Correct. The candidate calculates that Janet sells 9 eggs and makes $18 per day. 
Score: 1

Summary: 
{"A": "0", 
"B": "0",
"C": "0.2",
"D": "1"}

-------------------- response end --------------------


SCORE:
[0.0, 0.0, 0.2, 1.0]
```
#### Evaluate one file
```sh
auto-eval-file --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--eval_data_path   \
--output_path  \
--model gpt-3.5-turbo 
```


### Arguments Definitions:

#### Shared arguments
`--config_file` string <span style="color:orange">Required</span> <br>A local configuration file containing API key information.

`--template_path` string <span style="color:grey">Optional</span> <br> A cuatom template json file path, Please refer to the default prompt template for modification. You can define the position of instruction at the beginning or end, define the content of instruction, arrange the output of the model to be evaluated, and specify output formats. Currently, only JSON format parsing or score mode separated by spaces are supported as output formats. For example: {"A":0,"B": 0.1} or 0 0.1.
```json
{
    "eval_without_target_instruction": "Please solve the [Question] independently to obtain the [Correct answer], and then evaluate and comment each [Candidate answer] based on the [Correct answer]. Finally, output all [Candidate answers] scores (0-1) in a summary format of {\"number\": \"score\"}, e.g, {\"A\": \"0.2\", \"B\": \"0.8\"}",
    "eval_with_target_instruction": "Please evaluate and comment each [Candidate answer] based on the [Correct answer]. Then output all [Candidate answer] scores (0-1) in a summary format of {\"number\": \"score\"}, e.g, {\"A\": \"0.2\", \"B\": \"0.8\"}",
    "eval_with_target_template": "[Question]: {q}\n\n[Correct answer]: {target}\n\n[Candidate answer]:\n{options}\n\n[System]:\n{instruction}",
    "eval_without_target_template": "[Question]: {q}\n\n[Candidate answer]:\n{options}\n\n[System]:\n{instruction}" 
}
```


`--verbose` bool <span style="color:grey">Optional</span> Defaults to True <br> Whether to print every prompt and response evaluation detail.

`--model` string <span style="color:grey">Optional</span>  Defaults to GPT-3.5-turbo or Claude-v1.3 depends on `api_type`<br> Which model to perform evaluation.

`--temperature` number <span style="color:grey">Optional</span> Defaults to 1 <br>What sampling temperature to use.  Higher values like 1 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

`--max_new_tokens` integer <span style="color:grey">Optional</span> Defaults to 2048 <br>
The maximum number of tokens to generate in the chat completion.
The total length of input tokens and generated tokens is limited by the model's context length.

#### Evaluate one sample arguments

`--prompt` string <span style="color:orange">Required</span> <br>
The question that predicted by LLMs, e.g., A math question would be like: "1+1=?".

`--answers` array <span style="color:orange">Required</span> <br>
LLMs outputs correspond to the question in the prompt, answers must be separated by space.

`--target` <span style="color:grey">Optional</span> Defaults to \'\'<br> The correct answer for the question in the prompt. The prompt will be different depending on whether the target is provided, e.g., if no target is provided, the model is asked to solve the question first and then evaluate each candidate answer.

#### Evaluate file arguments

`--eval_data_path`: string <span style="color:orange">Required</span> <br>The file path of the input data to be evaluated.<br>

**Input File:**
The input file currently supports files with .json, .jsonl, .csv, and .xlsx extensions. The header of the file can be one of the following types: {'instruction', 'input', ‘output’}, {'prompt', 'output'}, {'prompt', 'target'}, {'question', 'answer'}, or {'question', 'output'}.

`--output_path`: string <span style="color:orange">Required</span> <br>The output file path for evaluation results.

**Output File:**
The output file can be specified as a .json, .jsonl, .csv or.xlsx extension. If it contains a field called "model", scores and statistics will be grouped based on this field. If it also contains fields called "model" and "category", scores and statistics will be grouped based on both fields. Any other fields will not be processed; the output will include all columns from the original input along with evaluation scores and explanations.

`--eval_categories`: array <span style="color:grey">Optional</span> Defaults to null <br> Choose specific types of question categories to evaluate. This only works when the input file contains a "category" column corresponding to each question.

`--sample_num`: number <span style="color:grey">Optional</span> Defaults to 0<br>Sample number of prompt-answer pairs to evaluate.

`--interval`: number <span style="color:grey">Optional</span> Defaults to 1 <br> Sleep interval in seconds between each request to avoid exceeding the request rate limit. A larger value like 10s is recommended for GPT-4.

`--retry`:  <span style="color:grey">Optional</span> Defaults to True <br> Whether to retry once for all failed requests. Failed requests may be due to reasons such as exceeding API request frequency, incorrect answer format parsing, or network failure.