import os
import sys
import argparse
from oneapi import OneAPITool
sys.path.append( os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/../../"))
from eval.prompt_template import prompter, prompts
from eval.utils.data_utils import df_reader
from eval.auto_llms_eval import eval_one_group, eval_one_qa, eval_groups, EvalConfig


def add_shared_arguments(parser):
    parser.add_argument(
        "-c", "--config_files",
        default=None,
        nargs="+", 
        help="config file path", 
        required=True
    )
    parser.add_argument(
        "-tp",
        "--template_path",
        type=str,
        default=None,
        help="eval prompt template path",
        required=False,
    )
    parser.add_argument(
        "-tt",
        "--template_type",
        type=str,
        default=None,
        help="Chosing default template_type: g means \"general\", ec means \"e_commerce\"",
        required=False,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=False,
        help="print every prompt and response detail",
        required=False,
    )
    parser.add_argument(
        "-m",
        "--model",
        default='',
        help="evaluate model name, e.g., gpt-35-turbo, gpt-4, please using larger models like GPT-4 for more difficult questions and faster models like GPT-3.5-turbo for simpler ones.",
        required=False,
    )
    parser.add_argument(
        "-te",
        "--temperature",
        type=float,
        default=0.1,
        help="0-1, higher temperature more random result",
        required=False,
    )
    parser.add_argument(
        "-mnt",
        "--max_new_tokens",
        type=int,
        default=2048,
        help="max output token length",
        required=False,
    )


def main():
    parser = argparse.ArgumentParser(description="auto-eval <command> [<args>]")
    subparsers = parser.add_subparsers(dest="command")

    # auto-eval line
    line_parser = subparsers.add_parser("line", help="auto-eval line [<args>]")
    add_shared_arguments(line_parser)
    line_parser.add_argument("-p", "--prompt", type=str, help="question", required=True)
    line_parser.add_argument(
        "-a", "--answers", nargs="+", help="candidate answers", required=True
    )
    line_parser.add_argument(
        "-ta", "--target", type=str, default="", help="standard answer", required=False
    )

    # auto-eval file
    file_parser = subparsers.add_parser("file", help="auto-eval file [<args>]")
    add_shared_arguments(file_parser)
    file_parser.add_argument(
        "-edp",
        "--eval_data_path",
        nargs="+",
        help="one or more eval data path",
        required=True,
    )
    file_parser.add_argument(
        "-qcn",
        "--question_column_names",
        default=None,
        nargs="+",
        help="one or more column names for question",
        required=False,
    )
    file_parser.add_argument(
        "-acn",
        "--answer_column_names",
        default=None,
        nargs="+",
        help="one or more column names for answer",
        required=False,
    )
    file_parser.add_argument(
        "-op", "--output_path", type=str, default="", help="", required=False
    )
    file_parser.add_argument(
        "-ec",
        "--eval_categories",
        default=None,
        nargs="+",
        help="only evaluate chosen categories",
        required=False,
    )
    file_parser.add_argument(
        "-sb",
        "--score_by",
        default=None,
        nargs="+",
        help="group by [columns] and sum the socre for log output",
        required=False,
    )
    file_parser.add_argument(
        "-em",
        "--eval_models",
        default=None,
        nargs="+",
        help="only evaluate chosen models' output",
        required=False,
    )
    file_parser.add_argument(
        "-sn", "--sample_num", type=int, default=0, help="", required=False
    )
    file_parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=1,
        help="request interval, gpt-4 need longer interval, e.g.,10s",
        required=False,
    )
    file_parser.add_argument(
        "-r", "--retry", type=bool, default=True, help="", required=False
    )

    args = parser.parse_args()
    if args.template_path:
        eval_prompter = prompter.EvalPrompter.from_config(args.template_path, verbose=args.verbose)
    else:
        if args.template_type in ['ec', 'e_commerce']:
            eval_prompter = prompter.EvalPrompter(prompts.EVAL_WITH_TARGET_TEMPLATE_ECOMMERCE, prompts.EVAL_WITHOUT_TARGET_TEMPLATE_ECOMMERCE, args.verbose)
        else:
            eval_prompter = prompter.EvalPrompter(prompts.EVAL_WITH_TARGET_TEMPLATE, prompts.EVAL_WITHOUT_TARGET_TEMPLATE, args.verbose)

    if args.command == "line":
        tool = OneAPITool.from_config_file(args.config_files[0])
        score, raw_response = eval_one_qa(
            api_tool=tool,
            eval_prompter=eval_prompter,
            question=args.prompt,
            candidate_answers=args.answers,
            target=args.target,
            engine=args.model,
            temperature=args.temperature,
            max_new_tokens=args.max_new_tokens,
        )
        print(f"\nSCORE:\n{score}")

    elif args.command == "file":
        eval_groups(
            EvalConfig(
                api_config_files=args.config_files,
                eval_prompter=eval_prompter,
                eval_data_path=args.eval_data_path,
                question_column_names=args.question_column_names,
                answer_column_names=args.answer_column_names,
                output_path=args.output_path,
                engine=args.model,
                eval_categories=args.eval_categories,
                eval_models=args.eval_models,
                sample_num=args.sample_num,
                request_interval=args.interval,
                retry=args.retry,
                score_by = args.score_by,
                temperature=args.temperature,
                max_new_tokens=args.max_new_tokens,
            )
        )


if __name__ == "__main__":
    main()
