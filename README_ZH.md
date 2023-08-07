# Auto-Eval

利用 ChatGPT（GPT-3.5-turbo）、GPT-4 和 Claude 的 API，只需一行命令就可以对我们训练的语言模型进行**自动评估** 。

评估提示词经过广泛的测试，以最大限度地确保评估的准确性（即使使用GPT-3.5），同时最小化单词数量以节省字符预算，因为 GPT-4 非常贵 💰。

如果想自定义评估提示，您可以使用默认模板作为基础进行修改。有关更多信息，请参阅下面提供的文档([点击这里](#jump))。

## 原理？

假设我们已经有一个测试集，我们可以使用不同版本模型进行预测，并将预测结果保存在诸如 JSON、CSV、Excel 等格式的文件格式中。输出文件的结构如下所示：

| prompt | output | model | category |
| --- | --- | --- | --- |
| 1+1 等于多少？ | 3 | model_a | 算术 |
| 法国的首都是哪里？ | 巴黎 | model_a | 常识 |
| 1+1 等于多少？ | 2 | model_b | 算术 |
| 法国的首都是哪里？ | 巴黎 | model_b | 常识 |

其中“prompt” 列表示输入问题，而 “output” 列代表模型的输出。此外，“model” 列对应所使用的模型的名称，最后，“category” 列表示每个问题的任务类型。

下一步是利用 GPT-4 来评估我们模型的预测并为每个答案打分。我们选择这种方法是因为当前由指令微调的语言模型缺乏适当的评估指标。手动评估成本高昂且耗时，不适用于频繁的实验和评估。

要使用自动评估，只需通过命令行输入您的文件即可。

```bash
auto-eval file --config_file OPENAI_API_KEY_CONFIG_PATH \
--eval_data_path model_predictions.json \
--output_path eval_result_path.xlsx \
--model gpt-4 \
--interval 12 
```

Auto-Eval将执行以下步骤：

步骤1：根据问题列（这里对应“prompt”列）将问题分组。每组包含一个问题和多个模型答案。

步骤2：组织评估提示，帮助GPT-4理解它正在评估任务，并为每个答案输出分数。

步骤3：评估所有问题和答案后，将输出得分结果。

请注意，尽管此示例仅使用一个文件，但您也可以使用多个文件，每个文件代表一个模型的输出。

## 安装

```
pip install -U auto-eval

```

## 详细使用方法

要使用此库，您必须首先从OpenAI、Microsoft Azure或Anthropic获取API密钥。要获取OpenAI API密钥，请访问其网站 https://platform.openai.com/account/api-keys ，对Antropic API密钥，请转到Anthropic网站 https://console.anthropic.com/account/keys。

此外，需要配置API的base url。如果需要，可以指定代理URL，例如 “https://your_proxy_domain/v1”。关于Azure API的相关信息可以在Azure资源仪表板上找到，API格式为 “https://{your_organization}.openai.azure.com/”。


### 步骤1：在本地配置文件中设置API密钥信息。

**OpenAI config:**
```json
{
    "api_key": "YOUR_API_KEY",
    "api_base": "https://api.openai.com/v1",
    "api_type": "open_ai"
}
```
**Azure OpenAI config:**
```json
{
    "api_key": "YOUR_API_KEY",
    "api_base": "Replace with your Azure OpenAI resource's endpoint value.",
    "api_type": "azure"
}
```
**Anthropic config:**
```json
{
    "api_key": "YOUR_API_KEY",
    "api_base": "https://api.anthropic.com",
    "api_type": "claude"
}
```
`api_type` 可选值为 "open_ai"、"azure" 或 "claude"。

### 步骤2：使用命令行执行评估任务

### 评估单个问答
多个候选答案用空格分割，例如 "1 2 3 4"。如果您的答案中包含空格，请使用双引号将其括起来，例如 "1 2 3 4" "1 2 3 4"。


```sh
auto-eval line --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--model gpt-3.5-turbo \
--prompt "4*5-10=?" \
--answers "4*5-10=20-10=40" -10 10 40 
```

<details> <summary>输出:</summary>

```text

Using prompt template:
{
    "eval_with_target_template": "Here is the question and candidate answers:\n\n ```text\n\n[Question]: \n{question}\n\n[Candidate answer]:\n\n{answers}\n\n```\n\n Please solve the question independently without referring to the candidate answers.\nThen evaluate each [Candidate answer] and provide a rating score between 0-1 along with your comments.\nFinally, output all [Candidate answers] scores in JSON format: {{\"number\": \"{{score}}\"}}.",
    "eval_without_target_template": "Here is the question and candidate answers:\n\n ```text\n\n[Question]: \n{question}\n\n[Candidate answer]:\n\n{answers}\n\n```\n\n Please solve the question independently without referring to the candidate answers.\nThen evaluate each [Candidate answer] and provide a rating score between 0-1 along with your comments.\nFinally, output all [Candidate answers] scores in JSON format: {{\"number\": \"{{score}}\"}}."
}

-------------------- prompt detail 🚀  --------------------

Here is the question and candidate answers:


[Question]: 
4*5-10=?

[Candidate answer]:

A. 4*5-10=20-10=40

B. -10

C. 10

D. 40

Please solve the question independently without referring to the candidate answers.
Then evaluate each [Candidate answer] and provide a rating score between 0-1 along with your comments.
Finally, output all [Candidate answers] scores in JSON format: {"number": "{score}"}.

-------------------- prompt end --------------------

-------------------- response detail ⭐️ --------------------

Solution:

4*5-10=20-10=10

[Candidate answer]:

A. 4*5-10=20-10=40 - Incorrect, the calculation is incorrect.

B. -10 - Incorrect, the answer is not -10.

C. 10 - Correct, the answer is 10.

D. 40 - Incorrect, the calculation is incorrect.

{"A": "0", "B": "0", "C": "1", "D": "0"}

Comments: Only option C is correct. The other options either have incorrect calculations or incorrect answers.

-------------------- response end --------------------


SCORE:
[0.0, 0.0, 1.0, 0.0]
```

</details>


#### 基于输入文件进行评估

```sh
auto-eval file --config_file CHANGE_TO_YOUR_CONFIG_PATH \
--eval_data_path model_a_pred.json model_b_pred.json model_c_pred.json \
--output_path eval_result_path.xlsx \
--model gpt-4 
```

**输入文件格式：**

- 输入文件支持扩展名为 .json、.jsonl、.csv 和 .xlsx 的文件。
- 要对多个文件进行比较，请使用参数 `eval_data_path`，后面跟着用空格分隔的文件名。例如：`eval_data_path file1.json file2.json ... fileN.json`。文件可以具有不同的格式，只要它们遵循下面提到的其中一种格式即可。
为了简化不同模型的分数比较，建议添加一个“model”列，以区分不同模型的名称，并使得可以轻松输出来自多个模型的分数统计信息。
- 要查看更详细的参数，请在安装该存储库后使用命令 `auto-eval file -h`，或参考下面的完整文档。
- 文件的表头（列名）可以是以下类型之一：
    - `{"instruction", "input", "output"}`
    - `{"prompt", "output"}`
    - `{"question", "answer"}`
    - `{"question", "output"}`
    - `{"question", "target"}`

    "question"、"prompt" 和 "instruction" + "input" 指的是输入问题，例如 "请仔细计算：1+1=？" 或 "像我一样五岁的孩子解释登上月球"。"answer" 和 "output" 表示给定问题的模型的预测答案。如果格式为 {"instruction", "input"}，两个字段的值会被拼接以创建一个完整的问题。
    

以下是一个JSON格式的测试数据示例，包含了模型的伪预测，以便了解评估输入文件的样子。


```
[
    {"category":"数学","instruction":"'我想修理花园的围墙。帮我估算一下需要准备多少尺长的围墙。我的花园宽10米，长5米，其中一边靠着墙。'", "input":"","output":"答案是15米", "model": "模型A"},
    {"category":"数学","instruction":"将这个数字列表按升序排序", "input": "[230, 1, 4, 7000, 20, 300]","output":"[1, 4, 230, 7000, 20, 300]", "model": "模型A"},
    {"category":"数学","instruction":"将这个数字列表按降序排序", "input":"[230，1，4，7000，20 ，300]","output":"[7000, 300, 230, 20, 4, 1]", "model": "模型A"}
]

```

**输出文件格式:**

- 输出文件可以指定为 .json、.jsonl、.csv 或 .xlsx 扩展名。
- 如果输入文件包含一个名为“model”的字段，则得分和统计信息将根据此字段进行分组。
- 如果输入文件还包含名为“model”和“category”的字段，则得分和统计信息将根据这两个字段进行分组。
- 任何其他字段都不会被处理；输出将包括原始输入的所有列以及评估得分和说明。

<details open> <summary>输出日志:</summary>

其中，prompts and responses detail... 部分为详细的输出内容。

- ------------------ 模型得分情况 --------------------

| 模型 | 得分 |
| --- | --- |
| 模型A | 81.5/100 |
| 模型B | 91.3/100 |
| 模型C | 80.0/100 |
- ------------------ 模型和任务类别得分情况 --------------------

| 模型 | 任务类别 | 得分 |
| --- | --- | --- |
| 模型A | 常识问答 | 15.5/20 |
| 模型B | 常识问答 | 17.3/20 |
| 模型C | 常识问答 | 14.7/20 |
| 模型A | 初等算术 | 10.0/15 |
| 模型B | 初等算术 | 11.0/15 |
| 模型C | 初等算术 | 9.2/15 |

</details>

## 参数定义：

### 共享参数

`--config_file` string ${\color{orange}\text{必需}}$ <br>
包含 API 密钥信息的本地配置文件。

<span id="jump">`--template_path` string ${\color{grey}\text{可选}}$
<br>模板文件路径应该是 JSON 格式的，指示模型评估并评论每个答案，以及在 JSON 格式中输出摘要分数，例如 `{"A": 0, "B": 0.1}`。

如果没有指定模板，将使用下面的默认模板。

```python
EVAL_WITH_TARGET_TEMPLATE ="""
[Question]: {question}

[Correct answer]: {target}

[Candidate answer]:

{answers}

[System]:
Please evaluate and comment each [Candidate answer] based on the [Correct answer].
Then output all [Candidate answer] scores (0-1) in a summary format of
{{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}.
"""

EVAL_WITHOUT_TARGET_TEMPLATE = """
[Question]: {question}

[Candidate answer]: 
{answers}

[System]:
Please solve the [Question] independently to obtain the [Correct answer].
Then evaluate and comment each [Candidate answer] based on the [Correct answer].
Finally, output all [Candidate answers] scores (0-1) in a summary format of
{{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}.
"""
```



如果您想使用自定义模板，请确保它具有“question”、“answers”的插槽。“target”只有在您的评估数据具有名为“target”的列时才是必需的。

```json
{
    "eval_with_target_template": "[Question]: {question}\n\n[Correct answer]: {target}\n\n[Candidate answer]:\n{answers}\n\n[System]:\nPlease solve the [Question] independently to obtain the [Correct answer], and then evaluate and comment each [Candidate answer] based on the [Correct answer]. Finally, output all [Candidate answers] scores (0-1) in a summary format of {{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}",
    "eval_without_target_template": "[Question]: {question}\n\n[Candidate answer]:\n{answers}\n\n[System]:\nPlease evaluate and comment each [Candidate answer] based on the [Correct answer]. Then output all [Candidate answer] scores (0-1) in a summary format of {{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}" 
}

```



`--template_type` string ${\color{grey}\text{可选}}$ 默认为 null

用于评估的模板。默认模板如上所示。另一个可选模板特定于电子商务领域。要使用它，请传递“-template_type e_commerce”。

`--verbose` bool ${\color{grey}\text{可选}}$ 默认为 True


是否打印每个提示和响应的详细信息。
`--model` string ${\color{grey}\text{可选}}$ 默认为 gpt-3.5-turbo 或 claude-v1.3 取决于 `api_type`

要执行评估任务的模型是哪个。默认评估模型为 gpt-3.5-turbo 或 claude-v1.3，具体取决于 API 类型。您可以指定要用于评估的模型的名称，例如“gpt-4”、“claude-instant-v1”或“claude-v1.3”。

`--temperature` number ${\color{grey}\text{可选}}$ 默认为 1

使用哪个采样温度。更高的值（例如1）会使输出更随机，而较低的值（例如0.1）会使其更加集中和确定性。

`--max_new_tokens` number ${\color{grey}\text{可选}}$ 默认为 2048

生成的最大字符数。模型的上下文长度限制了输入输出的总长度。

### 评估一个样本的参数

`--prompt` string ${\color{orange}\text{必需}}$

问题，例如一个数学问题可能是这样的: "1+1=?"。

`--answers` array ${\color{orange}\text{必需}}$

问题的候选答案，答案必须用空格分隔。例如，一组四个答案看起来像这样: 1 0 -1 2

`--target` string ${\color{grey}\text{可选}}$ 默认为 null

问题的正确答案。提示将根据是否提供答案而不同，例如，如果没有提供答案，将要求模型先解决问题，然后根据正确答案评估每个候选答案。

### 评估文件的参数

`--eval_data_path`: string ${\color{orange}\text{必需}}$

这是要评估的输入数据的文件路径。如果提供了多个文件，请确保它们具有相同的列名称。

`--output_path`: string ${\color{orange}\text{必需}}$

评估结果的输出文件路径。

`--eval_categories`: array ${\color{grey}\text{可选}}$ 默认为 null

选择要评估的特定问题类别类型。仅当输入文件包含与每个问题对应的“category”列时，此选项才有效。

`--question_column_names`: array ${\color{grey}\text{可选}}$ 默认为 null

指定特定列作为问题列。如果指定了多个列，则这些列将与换行符`\n`连接起来形成完整的问题列。

`--answer_column_names`: array ${\color{grey}\text{可选}}$ 默认为 null

指定特定列作为答案列。如果指定了多个列，则这些列将与 `\n` 连接起来形成完整的答案列。

`--sample_num`: number ${\color{grey}\text{可选}}$ 默认为 0

采样要评估样本数量，提示+各个模型答案组成一个样本。

`--interval`: number ${\color{grey}\text{可选}}$ 默认为 1

每次请求之间的睡眠间隔（以秒为单位），以避免超过请求速率限制。建议为 GPT-4 使用较大的值，例如 `--interval 10`。

`--retry`: ${\color{grey}\text{可选}}$ 默认为 True

是否对所有失败的请求重试一次。失败的请求可能是由于超出 API 请求频率、错误的答案格式解析或网络故障等原因而导致的。

`--score_by`: array ${\color{grey}\text{可选}}$ 默认为 null

用于确定用于 `pandas.groupby(by=args.score_by)` 进行 groupby 分组的字段。

## 待完成事项

- [ ]  将多个 GPT 类似的模型组合进行预测: 路由或简单平均。
- [x]  支持提示评估，输出不同提示的准确性。
- [ ]  为提示评估配置默认测试集。