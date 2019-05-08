import json

from click.testing import CliRunner

from pytest_django_queries import cli


def test_load_invalid_json_file_triggers_error(testdir):
    testdir.makefile('.json', test_file='')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 2
    assert (
        'Error: Invalid value for "INPUT_FILE": '
        'The file is not valid json: ') in result.stdout


def test_load_invalid_base_type_json_file_triggers_error(testdir):
    testdir.makefile('.json', test_file='[]')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 2
    assert (
        'The file is not a dictionary') in result.stdout


def test_load_invalid_test_entry_value_type_json_file_triggers_error(testdir):
    testdir.makefile('.json', test_file='{"test": 123}')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 1
    assert (
        'Error: Expected a dictionary, got int instead\n') in result.stdout


def test_load_valid_empty_json_file_is_success(testdir):
    testdir.makefile('.json', test_file='{}')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 0
    assert result.stdout.strip() == ''


VALID_DATA = {
    'module1': {
        'test1': {
            'query_count': 0
        },
        'test2': {
            'query_count': 1
        }
    },
    'module2': {
        'test1': {
            'query_count': 123
        }
    },
    'module3': {}
}


def test_load_valid_json_file_shows_correct_data(testdir):
    testdir.makefile('.json', test_file=json.dumps(VALID_DATA))
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 0, result.stdout
    assert result.stdout.strip() == ''
