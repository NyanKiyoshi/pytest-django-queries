import sys

import click


def raise_error(message, exit_code=1):
    click.echo('Error: %s' % message, file=sys.stderr)
    sys.exit(exit_code)
