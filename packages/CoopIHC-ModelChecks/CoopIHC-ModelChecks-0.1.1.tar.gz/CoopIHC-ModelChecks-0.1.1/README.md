# CoopIHC Model Checks

> Sanity checks for user modeling with CoopIHC

This work builds on the functionality provided by the [CoopIHC](https://github.com/jgori-ouistiti/CoopIHC) package to add sanity checks for user modeling workflows, specifically for...

- parameter inference,
- parameter recovery,
- model inference and
- model recovery.

## Installation

You can install the CoopIHC Model Checks from [PyPI](https://pypi.org/project/coopihc-modelchecks/):

```shell

python -m pip install coopihc-modelchecks

```

The reader is supported on Python 3.6 and above.

## Resources

- For details, see the [docs](docs/user_modeling.md).
- For a working example, see [model_checks.py](docs/code/model_checks.py).
- For the base library see [CoopIHC](https://github.com/jgori-ouistiti/CoopIHC).

## Development

If you want to contribute to this project, you can setup the project locally by cloning the repository and installing the dependencies specified in [setup.py](setup.py).

To publish a new version to PyPI, you can update the version specified in [__version__.py](modelchecks/__version__.py) and run `$ python setup.py upload` from the command line.
