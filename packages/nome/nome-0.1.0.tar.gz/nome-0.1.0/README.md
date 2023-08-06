# nome

![PyPI](https://img.shields.io/pypi/v/nome?style=flat-square)

A Python CLI to check if a package name is available in [PyPI](https://pypi.org/) or [npm](https://www.npmjs.com/).

## References

- Ewen Le Bihan's [check_availability](https://github.com/ewen-lbh/check-availability) CLI.
- Anton Zhiyanov's [How to make an awesome Python package in 2021](https://antonz.org/python-packaging/) blog post ([repo](https://github.com/nalgeon/podsearch-py)).
- [Development - Contributing](https://fastapi.tiangolo.com/contributing/) page (FastAPI documentation).

## Development

Current version of Python used for development: `Python 3.6.13`.

### To set up the environment

- `python -m venv env`.
- `source ./env/bin/activate`.
  - Run `which pip` to see if it worked. The path must end in `env/bin/pip`.
  - **Note**: Whenever you install a new package with `pip` in this environment, activate it again.
- `pip install flit==3.2.0`.
  - Requests is one of the dependencies.
  - [Documentation](https://github.com/takluyver/flit/tree/3.2.0/doc).
- `flit install --deps develop --symlink`.
  - To install all dependencies and `nome` in the local environment.
  - [For Windows](https://flit.readthedocs.io/en/latest/cmdline.html#flit-install), replace `--symlink` with `--pth-file`.

### To activate the environment

- `source ./env/bin/activate`.

## Deployment

- Bump version (`nome/__init__.py` file).
- `flit publish`.

## Notes

- [Why isn't my desired project name available?](https://pypi.org/help/#project-name):
  - `requirements.txt` is a prohibited project name.
- [stdlib-list](https://github.com/jackmaney/python-stdlib-list) package.
- [Python (3.6) Module Index](https://docs.python.org/3.6/py-modindex.html).
- [Flit](https://flit.readthedocs.io/en/latest/):
  - Python packaging tool.
  - [FastAPI](https://github.com/tiangolo/fastapi) uses it ([`pyproject.toml` file](https://github.com/tiangolo/fastapi/blob/master/pyproject.toml)).
  - Flit replaces setuptools, so you don't need the `MANIFEST.in`, `setup.py`, and/or `setup.cfg` files ([source](https://github.com/scikit-hep/cookie)).
  - It is possible to add `"Private :: Do Not Upload"` to the `classifiers` list to prevent a private project from being uploaded to PyPI.
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- [IceCream](https://github.com/gruns/icecream) package: alternative to `print()` for debugging.
- `python -m venv env` or `python3 -m venv env` (virtual environment with `venv`).
- [cookiecutter-hipster-pypackage](https://github.com/frankie567/cookiecutter-hipster-pypackage): it combines Pipenv and Flit.
- [packaging](https://packaging.pypa.io/en/latest/) package:
  - `pip install packaging`.
  - [Version specifiers](https://packaging.pypa.io/en/latest/specifiers.html) documentation.
  - Run `python requests_version.py`.
- [whey](https://whey.readthedocs.io/en/latest/) (Python wheel builder).
- [Cleo 0.8.1](https://github.com/sdispater/cleo/tree/0.8.1):
  - [Does not expose verbosity flags](https://github.com/sdispater/clikit/issues/44) (open) issue.
- `nome = "nome.application:application.run"` (more info [here](https://github.com/sdispater/orator/blob/0.9/orator/commands/application.py) and [here](https://github.com/sdispater/orator/blob/0.9/pyproject.toml)).
- [VSCodeThemes](https://vscodethemes.com/) (website to preview themes).
  - [Palenight Theme](https://marketplace.visualstudio.com/items?itemName=whizkydee.material-palenight-theme).
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

### `.pypirc` file

```ini
[distutils]
index-servers =
   pypi

[pypi]
username = joaopalmeiro
```
