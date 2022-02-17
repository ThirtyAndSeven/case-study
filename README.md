# emmy-case-study

![PyPI](https://img.shields.io/pypi/v/emmy-case-study?style=flat-square)
![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/fransaci/emmy-case-study/Test%20&%20Lint/master?style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/fransaci/emmy-case-study/master?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/emmy-case-study?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/emmy-case-study?style=flat-square)

Python Data Science Boilerplate

## Requirements

* Python 3.6.2 or newer

## Development


This project uses [poetry](https://poetry.eustace.io/) for packaging and
managing all dependencies and [pre-commit](https://pre-commit.com/) to run
[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),
[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).

Additionally, [pdbpp](https://github.com/pdbpp/pdbpp) and [better-exceptions](https://github.com/qix-/better-exceptions) are installed to provide a better debugging experience.
To enable `better-exceptions` you have to run `export BETTER_EXCEPTIONS=1` in your current session/terminal.

### Install

Clone this repository and run

```bash
poetry install
poetry run nbstripout --install
poetry run pre-commit install
```

to create a virtual enviroment containing all dependencies.

### Tests

You can run the test suite using

```bash
poetry run pytest
```

This repository follows the [Conventional Commits](https://www.conventionalcommits.org/)
style.

### Cookiecutter template

This project was created using [cruft](https://github.com/cruft/cruft) and the
[cookiecutter-jupyter](https://github.com/escaped/cookiecutter-jupyter) template.
In order to update this repository to the latest template version run

```sh
cruft update
```

in the root of this repository.
