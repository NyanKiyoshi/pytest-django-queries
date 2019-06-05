import json
from os.path import abspath, dirname
from os.path import join as pathjoin

import click
from jinja2 import Template
from jinja2 import exceptions as jinja_exceptions

from pytest_django_queries.diff import DiffGenerator
from pytest_django_queries.entry import flatten_entries
from pytest_django_queries.plugin import (
    DEFAULT_OLD_RESULT_FILENAME,
    DEFAULT_RESULT_FILENAME,
)
from pytest_django_queries.tables import entries_to_html, print_entries
from pytest_django_queries.utils import create_backup

HERE = dirname(__file__)
DEFAULT_TEMPLATE_PATH = abspath(pathjoin(HERE, "templates", "default_bootstrap.jinja2"))
DEFAULT_HTML_SAVE_PATH = "django-queries-results.html"

DIFF_TERM_COLOR = {"-": "red", "+": "green"}
DEFAULT_TERM_DIFF_COLOR = None


def _write_html_to_file(content, path):
    with open(path, "w") as fp:
        fp.write(content)


class JsonReportFileParamType(click.File):
    name = "report_file"

    def convert(self, value, param, ctx):
        fp = super(JsonReportFileParamType, self).convert(value, param, ctx)
        try:
            loaded = json.load(fp)
            if type(loaded) is not dict:
                self.fail("The file is not a dictionary", param, ctx)
            return loaded
        except ValueError as e:
            self.fail("The file is not valid json: %s" % str(e), param, ctx)


class Jinja2TemplateFile(click.File):
    name = "jinja2_file"

    def convert(self, value, param, ctx):
        fp = super(Jinja2TemplateFile, self).convert(value, param, ctx)
        try:
            return Template(fp.read(), trim_blocks=True)
        except jinja_exceptions.TemplateError as e:
            self.fail(
                "The file is not a valid jinja2 template: %s" % str(e), param, ctx
            )


@click.group()
def main():
    """Command line tool for pytest-django-queries."""


@main.command()
@click.argument(
    "input_file", type=JsonReportFileParamType("r"), default=DEFAULT_RESULT_FILENAME
)
def show(input_file):
    """View a given rapport."""
    return print_entries(input_file)


@main.command()
@click.argument(
    "input_file", type=JsonReportFileParamType("r"), default=DEFAULT_RESULT_FILENAME
)
@click.option(
    "-o",
    "--output",
    type=str,
    default=DEFAULT_HTML_SAVE_PATH,
    help="The path to save the HTML file into django-queries.html by default."
    "You can pass a dash (-) to write to stdout as well.",
)
@click.option(
    "--template",
    type=Jinja2TemplateFile("r"),
    default=DEFAULT_TEMPLATE_PATH,
    help="Use a custom jinja2 template for rendering HTML results.",
)
def html(input_file, output, template):
    """
    Render the results as HTML instead of a raw table.

    Note: you can pass a dash (-) as the path to print the HTML content to stdout."""
    html_content = entries_to_html(input_file, template)

    if output == "-":
        click.echo(html_content, nl=False)
        return

    _write_html_to_file(html_content, output)


@main.command()
@click.argument(
    "left_file", type=JsonReportFileParamType("r"), default=DEFAULT_OLD_RESULT_FILENAME
)
@click.argument(
    "right_file", type=JsonReportFileParamType("r"), default=DEFAULT_RESULT_FILENAME
)
def diff(left_file, right_file):
    """Render the diff as a console table with colors."""
    left = flatten_entries(left_file)
    right = flatten_entries(right_file)
    first_line = True
    for module_name, lines in DiffGenerator(left, right):
        if not first_line:
            click.echo()
        else:
            first_line = False

        click.echo("# %s" % module_name)
        for line in lines:
            fg_color = DIFF_TERM_COLOR.get(line[0], DEFAULT_TERM_DIFF_COLOR)
            click.secho(line, fg=fg_color)


@main.command()
@click.argument("target_path", type=str, default=DEFAULT_OLD_RESULT_FILENAME)
def backup(target_path):
    source_path = DEFAULT_RESULT_FILENAME
    click.echo("{0} -> {1}".format(source_path, target_path))
    create_backup(source_path, target_path)


if __name__ == "__main__":
    main()
