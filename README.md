<div align='center'>
  <h1>pytest-django-queries</h1>
  <p>Generate performance rapports from your django database performance tests.</p>
  <p>
    <a href='https://travis-ci.org/NyanKiyoshi/pytest-django-queries/'>
      <img src='https://travis-ci.org/NyanKiyoshi/pytest-django-queries.svg?branch=master' alt='Requirement Status' />
    </a>
    <a href='https://codecov.io/gh/NyanKiyoshi/pytest-django-queries'>
      <img src='https://codecov.io/gh/NyanKiyoshi/pytest-django-queries/branch/master/graph/badge.svg' alt='Coverage Status' />
    </a>
    <a href='https://pypi.python.org/pypi/pytest-django-queries'>
      <img src='https://img.shields.io/pypi/v/pytest-django-queries.svg' alt='Version' />
    </a>
    <a href='https://requires.io/github/NyanKiyoshi/pytest-django-queries/requirements/?branch=master'>
      <img src='https://requires.io/github/NyanKiyoshi/pytest-django-queries/requirements.svg?branch=master' alt='Requirement Status' />
    </a>
  </p>
  <p>
    <a href='https://github.com/pytest-dev/pytest-cov/compare/v0.0.0...master'>
      <img src='https://img.shields.io/github/commits-since/NyanKiyoshi/pytest-django-queries/v0.0.0.svg' alt='Commits since latest release' />
    </a>
    <a href='https://pypi.python.org/pypi/pytest-django-queries'>
      <img src='https://img.shields.io/pypi/pyversions/pytest-django-queries.svg' alt='Supported versions' />
    </a>
    <a href='https://pypi.python.org/pypi/pytest-django-queries'>
      <img src='https://img.shields.io/pypi/implementation/pytest-django-queries.svg' alt='Supported implementations' />
    </a>
  </p>
</div>

## Usage
Simply install `pytest-django-queries`, write your pytest tests and mark any
test that should be counted or use the `count_queries` fixture.

```python
import pytest


@pytest.mark.count_queries
def test_query_performances():
    Model.objects.all()


# Or...
def test_another_query_performances(count_queries):
    Model.objects.all()
```

## Integrating with GitHub

## Testing locally
Simply install `pytest-django-queries` through pip and run your 
tests using `pytest`. A report should have been generated in your
current working directory in a JSON file prefixed with `.pytest-queries`.

Note: to override the save path, set the `PYTEST_QUERIES_SAVE_PATH`
environment variable to any given valid path.

## Visualising Results

## Comparing results

## Development
Install the development requirements by running the below command.

```shell
pip install -e .[dev]
```
