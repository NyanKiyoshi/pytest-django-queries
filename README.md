# pytest-django-queries
Generate performance rapports from your django database performance tests.

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
