# DatabricksConverter

[![Upload to pypi](https://github.com/aless10/convert-py-2-databricks/actions/workflows/publish-to-pypi.yaml/badge.svg)](https://github.com/aless10/convert-py-2-databricks/actions/workflows/publish-to-pypi.yaml)
[![Run application tests](https://github.com/aless10/convert-py-2-databricks/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/aless10/convert-py-2-databricks/actions/workflows/run-tests.yaml)


## Version

0.0.9

## Description

This cli tool helps you to work in your favourite python IDE and then converts the files in databricks notebook.
You can also do the reverse conversion. Starting from a databricks notebook, you can convert it into a python file.

## Why

I struggled a lot working in the databricks interface because you don't have a lot of IDE feature like:
- autocomplete
- code analysis
- code linting
- testing

## How it works

You can install the package with pip: ``pip install Databricks2Py``
Then you have two options:

1. if you need to convert a databricks notebook to python, simply run `` databricks-converter to-py file/folder --destination your-destination-path``
2. if you need to convert a python module to a databricks notebook, simply run `` databricks-converter to-databricks file/folder --destination your-destination-path``


The converted files have a specific suffix `_to_py.py` and `_to_databricks.py`. So, if you do not want to put these files under version control, you must add these rules to you `.gitignore` file:
```
# in .gitignore
*_to_py.py
*_to_databricks.py
```

## TODO

- Improve conversion of complex import path
