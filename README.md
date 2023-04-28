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
--target 18
```
**Evaluate one file**
```sh
one-eval-file --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--eval_data_path   \
--output_path  \
--model gpt-3.5-turbo \
--verbose True
--