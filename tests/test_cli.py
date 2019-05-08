from click.testing import CliRunner

from pytest_django_queries import cli


def test_load_invalid_json_file_triggers_error(testdir):
    testdir.makefile('.json', test_file='')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 2
    assert (
        'Error: Invalid value for "INPUT_FILE": '
        'The file is not valid json: '
        'Expecting value: line 1 column 1 (char 0)\n') in result.stdout


def test_load_valid_json_file_is_success(testdir):
    testdir.makefile('.json', test_file='{}')
    runner = CliRunner()
    result = runner.invoke(cli.main, ['view', 'test_file.json'])
    assert result.exit_code == 0
    assert result.stdout.strip() == ''
