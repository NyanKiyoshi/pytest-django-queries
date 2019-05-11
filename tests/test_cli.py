import json
from textwrap import dedent

import pytest
from bs4 import BeautifulSoup
from click.testing import CliRunner

from pytest_django_queries import cli


def test_load_invalid_json_file_triggers_error(testdir):
    testdir.makefile('.json', test_file='')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['show', 'test_file.json'])
    assert result.exit_code == 2, result.stdout
    assert (
        'Error: Invalid value for "INPUT_FILE": '
        'The file is not valid json: ') in result.stdout


def test_load_invalid_base_type_json_file_triggers_error(testdir):
    testdir.makefile('.json', test_file='[]')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['show', 'test_file.json'])
    assert result.exit_code == 2, result.stdout
    assert (
        'The file is not a dictionary') in result.stdout


@pytest.mark.parametrize('test_data', (
    '{"test": 123}',
    '{"test": {"something": 123}}'))
def test_load_invalid_test_entry_value_type_json_file_triggers_error(
        testdir, test_data):

    testdir.makefile('.json', test_file=test_data)
    runner = CliRunner()
    result = runner.invoke(cli.main, ['show', 'test_file.json'])
    assert result.exit_code == 1, result.stdout
    assert (
        'Error: Expected a dict, got int instead\n') in result.stdout


def test_load_invalid_test_entry_missing_value_triggers_error(testdir):
    testdir.makefile('.json', test_file='{"test": {"something": {}}}')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['show', 'test_file.json'])
    assert result.exit_code == 1, result.stdout
    assert (
        'Got invalid data. It is missing a required key: query-count') in result.stdout


def test_load_valid_empty_json_file_is_success(testdir):
    testdir.makefile('.json', test_file='{}')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['show', 'test_file.json'])
    assert result.exit_code == 0, result.stdout
    assert result.stdout.strip() == ''


VALID_DATA = {
    'module1': {
        'test1': {
            'query-count': 0
        },
        'test2': {
            'query-count': 1
        }
    },
    'module2': {
        'test1': {
            'query-count': 123
        }
    },
    'module3': {}
}


def test_load_valid_json_file_shows_correct_data(testdir):
    testdir.makefile('.json', test_file=json.dumps(VALID_DATA))
    runner = CliRunner()
    result = runner.invoke(cli.main, ['show', 'test_file.json'])
    assert result.exit_code == 0, result.stdout
    assert result.stdout.strip() == dedent("""
        +---------+-------------------------+
        | Module  |          Tests          |
        +---------+-------------------------+
        | module1 | +-----------+---------+ |
        |         | | Test Name | Queries | |
        |         | +-----------+---------+ |
        |         | |   test1   |    0    | |
        |         | +-----------+---------+ |
        |         | |   test2   |    1    | |
        |         | +-----------+---------+ |
        +---------+-------------------------+
        | module2 | +-----------+---------+ |
        |         | | Test Name | Queries | |
        |         | +-----------+---------+ |
        |         | |   test1   |   123   | |
        |         | +-----------+---------+ |
        +---------+-------------------------+
        | module3 |                         |
        +---------+-------------------------+
    """).strip()


def test_load_valid_json_file_shows_correct_html_data(testdir):
    testdir.makefile('.json', test_file=json.dumps(VALID_DATA))
    runner = CliRunner()
    result = runner.invoke(cli.main, ['html', 'test_file.json'])
    assert result.exit_code == 0, result.stdout
    soup = BeautifulSoup(result.stdout, 'lxml')
    sections = soup.select('section')
    assert len(sections) == len(VALID_DATA)

    for html_section, expected_data in zip(sections, sorted(VALID_DATA.items())):
        expected_title, expected_data = \
            expected_data[0], sorted(expected_data[1].items())
        assert html_section.select_one('h2').get_text(strip=True) == expected_title
        for html_row, test_data in zip(
                html_section.select('tbody > tr'), expected_data):
            expected_test_name, expected_data = \
                test_data[0].split('test')[1], test_data[1]
            received_test_name, received_count = \
                html_row.select('td')
            assert received_test_name.get_text(strip=True) == expected_test_name
            assert (
                received_count.get_text(strip=True) == str(expected_data['query-count'])
            )
