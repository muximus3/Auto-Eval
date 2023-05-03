from setuptools import setup, find_packages

setup(
    name="one-eval",
    version="0.1.2",
    packages=find_packages(),
    package_data={
      "prompt_template":["eval_prompt_template.json"]  
    },
    install_requires=[
        # Add your library's dependencies here
        "one-api-tool",
        "pandas",
        "openpyxl",
        "tabulate",
        "XlsxWriter"
    ],
    entry_points={
        "console_scripts": [
            "one-eval-file=commands.one_api_eval_file:main",
            "one-eval-line=commands.one_api_eval_one:main",
        ]
    },
    description="Using only one line of commmands to evaluate multiple models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/muximus3/OneEval",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)