# OneAPI
Use a single line of code to call multiple model APIs similar to ChatGPT. Currently supported: Azure OpenAI Resource endpoint API, OpenAI Official API, and Anthropic Claude series model API.

## Installation
```sh
pip install -U one-eval
```

## Usage
### 1. Set up your API information in the local configuration file.

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
**Evaluate one sample**
```sh
one-eval-line --config_file CHANGE_TO_YOUR_CONFIG_PATH \
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
**Evaluate one file**
```sh
one-eval-file --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--eval_data_path   \
--output_path  \
--model gpt-3.5-turbo \
--verbose True
--