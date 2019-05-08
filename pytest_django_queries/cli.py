import json

import click

from pytest_django_queries.tables import print_entries


class JsonFileParamType(click.File):
    name = 'integer'

    def convert(self, value, param, ctx):
        fp = super(JsonFileParamType, self).convert(value, param, ctx)
        if fp is not None:
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


@click.group()
def main():
    """Command line tool for pytest-django-queries."""


@main.command()
@click.argument('input_file', type=JsonFileParamType('r'))
@click.option(
    '--html',
    is_flag=True, help='Render the results as HTML instead of a raw table.')
def view(input_file, html):
    """View a given rapport."""
    if not html:
        print_entries(input_file)
        return
    raise NotImplementedError


if __name__ == '__main__':
    main()
