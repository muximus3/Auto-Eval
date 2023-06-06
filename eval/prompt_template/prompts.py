
import sys
import os 
sys.path.append(
    os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/../../")
)

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

EVAL_WITH_TARGET_TEMPLATE_ECOMMERCE = """
The following text contains a question along with some context and sevaral candidate answers. A reference answer is also provided for comparison purposes.
Question:
```text
{question}
```
Reference answer:
```text
{target}
```
Candidate answers:
```text
{answers}
```
Please evaluate each candidate's answer based on its accuracy, professionalism, and ability to provide necessary information without being too verbose.
Then assign a rating score between 0-1 along with brief comments.
Finally, output all [Candidate answers] scores in JSON format: {{"number": "{{score}}"}}.
"""

EVAL_WITHOUT_TARGET_TEMPLATE_ECOMMERCE = """
The following text contains a question along with some context and sevaral candidate answers.
Question:
```text
{question}
```
Candidate answers:
```text
{answers}
```
Please evaluate each candidate's answer based on its accuracy, professionalism, and ability to provide necessary information without being too verbose.
Then assign a rating score between 0-1 along with brief comments.
Finally, output all [Candidate answers] scores in JSON format: {{"number": "{{score}}"}}.
"""

