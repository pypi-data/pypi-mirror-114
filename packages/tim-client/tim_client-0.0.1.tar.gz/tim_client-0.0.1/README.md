# TIM Python Client V5

# Project setup

Run `pip3 install -e '.[dev]'` to install dependencies from the setup.cfg.
Run `pre-commit install` to setup the git pre-hooks.

# Build and upload to TestPyPi

1. Remove dist folder
2. python3 -m build
3. python3 -m twine upload --repository testpypi dist/*
