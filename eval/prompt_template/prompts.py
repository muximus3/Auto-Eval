
import sys
import os 
sys.path.append(
    os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/../../")
)

EVAL_WITH_TARGET_TEMPLATE = """
[Question]: {question}\n\n[Correct answer]: {target}\n\n[Candidate answer]:\n{answers}\n\n[System]:\n
Please evaluate and comment each [Candidate answer] based on the [Correct answer].
Then output all [Candidate answer] scores (0-1) in a summary format of
{{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}.
"""

EVAL_WITHOUT_TARGET_TEMPLATE = """
[Question]: {question}\n\n[Candidate answer]:\n{answers}\n\n[System]:\n
Please solve the [Question] independently without referring to candidate answers to obtain the [Correct answer],
and then evaluate and comment each [Candidate answer] based on the [Correct answer].
Finally, output all [Candidate answers] scores (0-1) in a summary format of
{{\"number\": \"score\"}}, e.g, {{\"A\": \"0.2\", \"B\": \"0.8\"}}.
"""

EVAL_WITH_TARGET_TEMPLATE_ECOMMERCE = """
The following text contains a question from the customer along with some context. A reference answer is also provided for comparison purposes.\n
\nQuestion:
\n```text\n\n{question}\n\n```\n
\nReferece answer:
\n```text\n\n{target}\n\n```
\nPlease evaluate and comment on each candidate answer based on its accurately and professionalism, 
and ability to provide necessary information without being too verbose.
\nCandidate answers:
\n```text\n\n{answers}\n\n```\n
\nFinally output all answers' scores (0-1) in a summary format of {{\"number\": \"score\"}}"""

EVAL_WITHOUT_TARGET_TEMPLATE_ECOMMERCE = """
The following text contains a question from the customer along with some context.
\nQuestion:
\n```text\n\n{question}\n\n```
\nPlease first answer the question independently without referring to candidate answers to obtain the correct answer, 
and then evaluate and comment each answer based on its accurately and professionalism, 
and ability to provide necessary information without being too verbose.
\nCandidate answers:
\n```text\n\n{answers}\n\n```\n

Finally output all answers' scores (0-1) in a summary format of {{\"number\": \"score\"}}"""

