
import sys
import os 
sys.path.append(
    os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/../../")
)

EVAL_WITH_TARGET_TEMPLATE ="""
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

EVAL_WITHOUT_TARGET_TEMPLATE = """
The following text contains a question along with some context and sevaral candidate answers.
Question:
```text
{question}
```

Candidate answers:
```text
{answers}
```

Please first answer the question independently without referring to candidate answers to obtain the correct answer, then evaluate each candidate's answer based on its accuracy, professionalism, and ability to provide necessary information without being too verbose.
Then assign a rating score between 0-1 along with brief comments.
Finally, output all [Candidate answers] scores in JSON format: {{"number": "{{score}}"}}.
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
Then assign a rating score between -1 and 1 along with brief comments.
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

Please first answer the question independently without referring to candidate answers to obtain the correct answer, then evaluate each candidate's answer based on its accuracy, professionalism, and ability to provide necessary information without being too verbose.
Then assign a rating score between -1 and 1 along with brief comments.
Finally, output all [Candidate answers] scores in JSON format: {{"number": "{{score}}"}}.
"""

