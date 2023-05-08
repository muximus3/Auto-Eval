# Auto-Eval

**Auto-Eval** utilizes ChatGPT (GPT-3.5-turbo), GPT-4, and Claude's API to evaluate language models with a single command. 

The evaluation prompt has been extensively tested to ensure maximum accuracy even when using GPT-3.5 while minimizing word usage to save token budget since GPT-4 can be quite expensive 💰.

To further personalize the prompt, you can modify it using the default templates as a basis. For additional information, please refer to the documentation provided below ([click here](#jump)).

## Installation
```sh
pip install -U auto-eval
```

## Usage
To utilize this repository, you must first obtain API keys from OpenAI, Microsoft Azure, or Anthropic. To acquire your OpenAI API key, visit their website at https://platform.openai.com/account/api-keys. For your Claude API key, go to the Anthropic website at https://console.anthropic.com/account/keys.

Additionally, ensure that the base API for sending requests is provided. If necessary, specify a proxy URL such as "https://your_proxy_domain/v1". Relevant information for Azure APIs can be found on the Azure resource dashboard with an API format of `https://{your_organization}.openai.azure.com/`.

The currently supported values for `api_type` are "open_ai", "azure", or "claude".

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

### 2. Usage with command lines
#### Evaluate one sample
```sh
auto-eval line --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--model gpt-3.5-turbo \
--prompt "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?" \
--answers 20 100 21 18 \
--target "Janet sells 16 - 3 - 4 = <<16-3-4=9>>9 duck eggs a day. She makes 9 * 2 = $<<9*2=18>>18 every day at the farmer’s market. #### 18"
```
<details> <summary>log output example:</summary>

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

</details>


#### Evaluate files
```sh
auto-eval file --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--eval_data_path model_a_pred.json model_b_pred.json model_c_pred.json \
--output_path eval_result_path.xlsx \
--model gpt-4 
```

**Input file format:**<br>
The input file currently supports files with .json, .jsonl, .csv, and .xlsx extensions. The headers(column names) of the file can be one of the following types: `{'instruction', 'input', ‘output’}`, `{'prompt', 'output'}`, `{'question', 'answer'}`, or `{'question', 'output'}`.

**Output File format:**<br>
The output file can be specified as a .json, .jsonl, .csv or.xlsx extension. If it contains a field called "model", scores and statistics will be grouped based on this field. If it also contains fields called "model" and "category", scores and statistics will be grouped based on both fields. Any other fields will not be processed; the output will include all columns from the original input along with evaluation scores and explanations.

<details open> <summary>log output example:</summary>

<br>
prompts and responses detail...

-------------------- Scores by Model --------------------
| model                      | score   |
|:---------------------------|:--------|
| model A       | 81.5/100   |
| model B |91.3/100   |
| model C          | 80.0/100   |

-------------------- Scores by Model and Task Category --------------------
| model                      | category   | score   |
|:---------------------------|:-----------|:--------|
| model A       | Common sense QA   | 15.5/20   |
| model A       | Elementary arithmetic   | 10.0/15   |
| model B | Common sense QA   | 17.3/20   |
| model B | Elementary arithmetic   | 11.0/15   |
| model C           | Common sense QA   | 14.7/20   |
| model C           | Elementary arithmetic   | 9.2/15   |


</details>

## Arguments Definitions:

### Shared arguments
`--config_file` string ${\color{orange}\text{Required}}$ <br>A local configuration file containing API key information.

 <span id="jump">`--template_path`${\color{grey}\text{Optional}}$ <br>
The template file path should be in JSON format and instructs the model to evaluate and comment on each answer, as well as output summary scores in JSON format, such as `{"A": 0, "B": 0.1}`.<br>
If no specific template is available, the default one provided below will be used.<br>
If you want to use a custom template, make sure it has slots for "question", "answers", and "target". The first two are required, while "target" is only necessary if your evaluation data has a column named "target".
```json
{
    "eval_with_target_template": "[Question]: {question}\n\n[Correct answer]: {target}\n\n[Candidate answer]:\n{answers}\n\n[System]:\nPlease solve the [Question] independently to obtain the [Correct answer], and then evaluate and comment each [Candidate answer] based on the [Correct answer]. Finally, output all [Candidate answers] scores (0-1) in a summary format of {{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}",
    "eval_without_target_template": "[Question]: {question}\n\n[Candidate answer]:\n{answers}\n\n[System]:\nPlease evaluate and comment each [Candidate answer] based on the [Correct answer]. Then output all [Candidate answer] scores (0-1) in a summary format of {{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}" 
}
```


`--verbose` bool ${\color{grey}\text{Optional}}$ Defaults to True <br> Whether to print every prompt and response evaluation detail.

`--model` string ${\color{grey}\text{Optional}}$  Defaults to gpt-3.5-turbo or claude-v1.3 depends on `api_type`<br> Which model to perform evaluation, The default model for evaluation is either gpt-3.5-turbo or claude-v1.3, depending on the API type. You can specify which model to use for evaluation by providing its name, such as "gpt-4", "claude-instant-v1", or "claude-v1.3".

`--temperature` number ${\color{grey}\text{Optional}}$ Defaults to 1 <br>What sampling temperature to use.  Higher values like 1 will make the output more random, while lower values like 0.1 will make it more focused and deterministic.

`--max_new_tokens` integer ${\color{grey}\text{Optional}}$ Defaults to 2048 <br>
The maximum number of tokens to generate in the chat completion.
The total length of input tokens and generated tokens is limited by the model's context length.

### Evaluate one sample arguments

`--prompt` string ${\color{orange}\text{Required}}$ <br>
The question that predicted by LLMs, e.g., A math question would be like: "1+1=?".

`--answers` array ${\color{orange}\text{Required}}$ <br>
LLMs outputs correspond to the question in the prompt, answers must be separated by space. e.g., A set of four answers would look like this: 1 0 -1 2

`--target` ${\color{grey}\text{Optional}}$ Defaults to \'\'<br> The correct answer for the question. The prompt will be different depending on whether the target is provided, e.g., if no target is provided, the model is asked to solve the question first and then evaluate each candidate answer.

### Evaluate file arguments

`--eval_data_path`: string ${\color{orange}\text{Required}}$ <br>This refers to the file paths of the input data that will be evaluated. If multiple paths are provided, please ensure that they have identical column names.



`--output_path`: string ${\color{orange}\text{Required}}$ <br>The output file path for evaluation results.



`--eval_categories`: array ${\color{grey}\text{Optional}}$ Defaults to null <br> Choose specific types of question categories to evaluate. This only works when the input file contains a "category" column corresponding to each question.

`--sample_num`: number ${\color{grey}\text{Optional}}$ Defaults to 0<br>Sample number of prompt-answer pairs to evaluate.

`--interval`: number ${\color{grey}\text{Optional}}$ Defaults to 1 <br> Sleep interval in seconds between each request to avoid exceeding the request rate limit. A larger value like 10 is recommended for GPT-4.

`--retry`:  ${\color{grey}\text{Optional}}$ Defaults to True <br> Whether to retry once for all failed requests. Failed requests may be due to reasons such as exceeding API request frequency, incorrect answer format parsing, or network failure.