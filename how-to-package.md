# How to package this
this is packaged via python setuptools

`pyproject.toml` is like the `package.json` or `pubspec.yaml`

1. `python -m build`
2. `twine upload -r pypi dist/*` This is for production
   use `twine upload -r testpypi dist/*` for testing