# Automated Documentation

Currently works for Python projects only.
This project is in a private beta.
for more information on using the tool,
to provide feedback,
or request access for a friend or colleague,
contact the beta runners.
**N.b.** this project calls an AWS API
with snippets of code
in order to generate documentation.
No code is stored.
Only your API key and a hash of your project name,
for the purposes of identifying usage,
are logged.

## Get started

### Requirements

* `python 3.8` or greater
* `pip install jaepeto`
* In the base directory of your project, create a `.jaepeto.ini` config file

```
[project]
name = <a project name>
description = <a short project description>
language = python
api_key = <an access key unique to a user. Given to you during onboarding>
srcdir = <the folder name where source code is stored. Typically 'src' or your project name>

[docs]
docdir = <folder where documentation will be stored. MUST EXIST>
```

Set `docdir = .` to generate documentation in the root directory.

### Generate documentation

**Via CLI:**

In a terminal/command prompt,
navigate to the root directory of your project
and run `jaepeto`.

**VSCode:**

There is a VSCode extension for this tool.
Search for `jaepeto` in the marketplace.
Use the command `Generate Technical Doc`
once installed.

## Development - Get started

### Requirements

- Developed with `python 3.9`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `pip install -e .`

## Style Guide

- Use `black` to format code
- Other than `black` niches, adhere to PEP
- Use `isort` to sort imports
- Use numpy-style docstrings
- Use type hints and verify with `mypy`

### Testing

Testing performed with `pytest`.
Run `python -m pytest`
to run unit tests.
