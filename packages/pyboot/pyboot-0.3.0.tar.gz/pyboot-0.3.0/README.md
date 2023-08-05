# Python project bootstrap

Basic scaffolding for python3 CLI projects

## Usage

```
$ pyboot cli --help
Usage: pyboot cli [OPTIONS] NAME

  Create project from the cli template.

Options:
  -d, --directory PATH  Destination directory.
  --help                Show this message and exit.
```

Create a CLI project in the current folder:
```
$ pyboot cli myproj
```

Load the project in a venv:
```
$ python -m venv venv
$ . venv/bin/activate
$ pip install .[dev]
$ pip list
myproj       0.1.0
...
```

Run it:
```
$ myproj --version
proj, version 0.1.0
```

Test it:
```
$ tox
```

## Contribute

`pyboot` is built from the same CLI template it generates.

Install:
```
$ pip install .[dev]
```

Test:
```
$ tox
```

Release:
```
$ pip install twine
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```

## Todo

* Waiting for a editable standardization before moving to PEP517 (See: https://discuss.python.org/t/specification-of-editable-installation/1564/40)
