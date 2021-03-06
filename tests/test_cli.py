import json
from textwrap import dedent

import mock
import pytest
from bs4 import BeautifulSoup
from click.testing import CliRunner

from pytest_django_queries import cli


def test_load_invalid_json_file_triggers_error(testdir):
    testdir.makefile(".json", test_file="")
    runner = CliRunner()
    result = runner.invoke(cli.main, ["show", "test_file.json"])
    assert result.exit_code == 2, result.stdout
    assert (
        "Error: Invalid value for '[INPUT_FILE]': The file is not valid json"
        in result.stdout
    )


def test_load_invalid_base_type_json_file_triggers_error(testdir):
    testdir.makefile(".json", test_file="[]")
    runner = CliRunner()
    result = runner.invoke(cli.main, ["show", "test_file.json"])
    assert result.exit_code == 2, result.stdout
    assert ("The file is not a dictionary") in result.stdout


@pytest.mark.parametrize("test_data", ('{"test": 123}', '{"test": {"something": 123}}'))
def test_load_invalid_test_entry_value_type_json_file_triggers_error(
    testdir, test_data
):

    testdir.makefile(".json", test_file=test_data)
    runner = CliRunner()
    result = runner.invoke(cli.main, ["show", "test_file.json"])
    assert result.exit_code == 1, result.stdout
    assert ("Error: Expected a dict, got int instead\n") in result.stdout


def test_load_invalid_test_entry_missing_value_triggers_error(testdir):
    testdir.makefile(".json", test_file='{"test": {"something": {}}}')
    runner = CliRunner()
    result = runner.invoke(cli.main, ["show", "test_file.json"])
    assert result.exit_code == 1, result.stdout
    assert (
        "Got invalid data. It is missing a required key: query-count"
    ) in result.stdout


def test_load_valid_empty_json_file_is_success(testdir):
    testdir.makefile(".json", test_file="{}")
    runner = CliRunner()
    result = runner.invoke(cli.main, ["show", "test_file.json"])
    assert result.exit_code == 0, result.stdout
    assert result.stdout.strip() == ""


VALID_DATA = {
    "module1": {"test1": {"query-count": 0}, "test2": {"query-count": 1}},
    "module2": {"test1": {"query-count": 123, "duplicates": 0}},
    "module3": {},
}


def test_load_valid_json_file_shows_correct_data(testdir):
    testdir.makefile(".json", test_file=json.dumps(VALID_DATA))
    runner = CliRunner()
    result = runner.invoke(cli.main, ["show", "test_file.json"])
    assert result.exit_code == 0, result.stdout
    assert (
        result.stdout.strip()
        == dedent(
            """
            +---------+--------------------------------------+
            | Module  |                Tests                 |
            +---------+--------------------------------------+
            | module1 | +-----------+---------+------------+ |
            |         | | Test Name | Queries | Duplicated | |
            |         | +-----------+---------+------------+ |
            |         | |   test1   |    0    |    UNK     | |
            |         | +-----------+---------+------------+ |
            |         | |   test2   |    1    |    UNK     | |
            |         | +-----------+---------+------------+ |
            +---------+--------------------------------------+
            | module2 | +-----------+---------+------------+ |
            |         | | Test Name | Queries | Duplicated | |
            |         | +-----------+---------+------------+ |
            |         | |   test1   |   123   |     0      | |
            |         | +-----------+---------+------------+ |
            +---------+--------------------------------------+
            | module3 |                                      |
            +---------+--------------------------------------+
    """
        ).strip()
    )


def test_load_valid_json_file_shows_correct_html_data(testdir):
    testdir.makefile(".json", test_file=json.dumps(VALID_DATA))
    runner = CliRunner()
    result = runner.invoke(cli.main, ["html", "test_file.json", "-o", "-"])
    assert result.exit_code == 0, result.stdout
    soup = BeautifulSoup(result.stdout, "lxml")
    sections = soup.select("section")
    assert len(sections) == len(VALID_DATA)

    for html_section, expected_data in zip(sections, sorted(VALID_DATA.items())):
        expected_title, expected_data = (
            expected_data[0],
            sorted(expected_data[1].items()),
        )
        assert html_section.select_one("h2").get_text(strip=True) == expected_title
        for html_row, test_data in zip(
            html_section.select("tbody > tr"), expected_data
        ):
            expected_test_name, expected_data = (
                test_data[0].split("test")[1],
                test_data[1],
            )
            received_test_name, received_count, duplicates = html_row.select("td")
            assert received_test_name.get_text(strip=True) == expected_test_name
            assert received_count.get_text(strip=True) == str(
                expected_data["query-count"]
            )
            assert duplicates.get_text(strip=True) == str(
                expected_data.get("duplicates", "UNK")
            )


@pytest.mark.parametrize("test_data", ({}, {"my test section": {}}))
def test_load_valid_json_without_data_is_empty_result(testdir, test_data):
    testdir.makefile(".json", test_file=json.dumps(test_data))

    runner = CliRunner()
    result = runner.invoke(cli.main, ["html", "test_file.json", "-o", "-"])
    assert result.exit_code == 0, result.stdout

    soup = BeautifulSoup(result.stdout, "lxml")
    sections = soup.select("section")

    if not test_data.keys():
        # if there is no data, no section should have been created
        assert not sections
    else:
        # if there is data, there should not have an error message
        assert not soup.select("body > p")

        # retrieve the section, should only be one
        assert len(sections) == 1
        soup = sections[0]

        # check the title
        assert soup.select_one("h2").get_text(strip=True) == "my test section"

    # test if the render says there is no data
    received_text = soup.select_one("p")
    assert received_text is not None, "No message"
    assert received_text.get_text(strip=True) == "No data."


def test_export_to_html_using_custom_path(testdir):
    testdir.makefile(".json", test_file="{}")
    results_path = testdir.tmpdir.join("results.html")

    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["html", "test_file.json", "-o", str(results_path)]
    )
    assert result.exit_code == 0, result.stdout
    assert not result.stdout
    assert results_path.check()


def test_export_to_html_using_custom_template(testdir):
    testdir.makefile(".json", test_file="{}")
    testdir.makefile(".html", test_template='{{ "hello world" }}')

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["html", "test_file.json", "-o", "-", "--template", "test_template.html"],
    )
    assert result.exit_code == 0, result.stdout
    assert result.stdout == "hello world"


@pytest.mark.parametrize(
    "additional_args, expected_save_path",
    ((["-o", "/somewhere/html"], "/somewhere/html"), ([], cli.DEFAULT_HTML_SAVE_PATH)),
)
@mock.patch.object(cli, "entries_to_html")
@mock.patch.object(cli, "_write_html_to_file")
def test_export_to_html_into_file(
    mocked_write, mocked_entries_to_html, testdir, additional_args, expected_save_path
):
    testdir.makefile(".json", test_file="{}")
    runner = CliRunner()

    mocked_entries_to_html.return_value = "hi!"

    args = ["html", "test_file.json"] + additional_args
    result = runner.invoke(cli.main, args)

    assert result.exit_code == 0, result.stdout
    assert not result.stdout

    mocked_write.assert_called_once_with("hi!", expected_save_path)


def test_export_to_html_using_invalid_custom_template_should_fail(testdir):
    testdir.makefile(".json", test_file="{}")
    testdir.makefile(".html", test_template='{% "hello world" %}')

    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["html", "test_file.json", "--template", "test_template.html"]
    )
    assert result.exit_code == 2, result.stdout
    assert (
        "Error: Invalid value for '--template': "
        "The file is not a valid jinja2 template: tag name expected" in result.stdout
    )


def test_backup_command_is_making_a_backup(testdir):
    results_file = str(testdir.tmpdir.join(".pytest-queries"))

    with open(results_file, "w") as fp:
        fp.write("hello!")

    backup_file = testdir.tmpdir.join("backup.json")

    runner = CliRunner()
    result = runner.invoke(cli.main, ["backup", "backup.json"])
    assert result.exit_code == 0, result.stdout
    assert result.stdout == ".pytest-queries -> backup.json\n"

    assert backup_file.check()
    with open(str(backup_file), "r") as fp:
        assert fp.read() == "hello!"
