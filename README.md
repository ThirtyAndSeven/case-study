# emmy-case-study


## Requirements

* Python 3.8 or newer

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
pip install poetry
```

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
