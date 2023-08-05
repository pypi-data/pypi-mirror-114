# {{ name }}

## Test

```
$ pip install .[dev]
$ tox
```

## Release

```
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```
