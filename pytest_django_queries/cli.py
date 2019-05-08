import json

import click


class JsonFileParamType(click.File):
    name = 'integer'

    def convert(self, value, param, ctx):
        fp = super(JsonFileParamType, self).convert(value, param, ctx)
        if fp is not None:
            try:
                return json.load(fp)
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
def view(input_file):
    """View a rapport."""
    click.echo()


if __name__ == '__main__':
    main()
