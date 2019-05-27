import json

from click.testing import CliRunner

from pytest_django_queries import cli


def test_export_to_html_using_custom_template(testdir, valid_comparison_entries):
    left, right = valid_comparison_entries
    right["another_module"] = {"test_new_test": {"query-count": 1}}
    testdir.makefile("json", left=json.dumps(left))
    testdir.makefile("json", right=json.dumps(right))

    runner = CliRunner()
    result = runner.invoke(cli.main, ["diff", "left.json", "right.json"])
    assert result.exit_code == 0, result.stdout
    assert repr(result.stdout) == repr(
        u"""\
# another module
  test name          \tleft count \tright count
  -------------------\t-----------\t-----------
+ new test           \t          -\t          1

# module
  test name          \tleft count \tright count
  -------------------\t-----------\t-----------
- degraded func      \t         15\t         16
+ improved func      \t         20\t         19
  unchanged func     \t          1\t          1
"""
    )
