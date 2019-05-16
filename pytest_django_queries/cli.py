import json
from os.path import abspath, dirname
from os.path import join as pathjoin

import click
from jinja2 import Template
from jinja2 import exceptions as jinja_exceptions

from pytest_django_queries.plugin import DEFAULT_RESULT_FILENAME
from pytest_django_queries.tables import print_entries, print_entries_as_html

HERE = dirname(__file__)
DEFAULT_TEMPLATE_PATH = abspath(pathjoin(HERE, 'templates', 'default_bootstrap.jinja2'))


class JsonFileParamType(click.File):
    name = 'integer'

    def convert(self, value, param, ctx):
        fp = super(JsonFileParamType, self).convert(value, param, ctx)
        try:
            loaded = json.load(fp)
            if type(loaded) is not dict:
                self.fail('The file is not a dictionary', param, ctx)
            return loaded
        except ValueError as e:
            self.fail(
                'The file is not valid json: %s' % str(e),
                param,
                ctx)


class Jinja2TemplateFile(click.File):
    name = 'integer'

    def convert(self, value, param, ctx):
        fp = super(Jinja2TemplateFile, self).convert(value, param, ctx)
        try:
            return Template(fp.read())
        except jinja_exceptions.TemplateError as e:
            self.fail(
                'The file is not a valid jinja2 template: %s' % str(e),
                param,
                ctx)


@click.group()
def main():
    """Command line tool for pytest-django-queries."""


@main.command()
@click.argument(
    'input_file', type=JsonFileParamType('r'), default=DEFAULT_RESULT_FILENAME)
def show(input_file):
    """View a given rapport."""
    return print_entries(input_file)


@main.command()
@click.argument(
    'input_file', type=JsonFileParamType('r'), default=DEFAULT_RESULT_FILENAME)
@click.option('--template', type=Jinja2TemplateFile('r'), default=DEFAULT_TEMPLATE_PATH)
def html(input_file, template):
    """Render the results as HTML instead of a raw table."""
    return print_entries_as_html(input_file, template)


if __name__ == '__main__':
    main()
