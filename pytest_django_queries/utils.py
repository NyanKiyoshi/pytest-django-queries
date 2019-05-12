import sys

import click


def raise_error(message, exit_code=1):
    click.echo('Error: %s' % message, file=sys.stderr)
    sys.exit(exit_code)


def assert_type(value, expected_type):
    if type(value) != expected_type:
        raise_error(
            'Expected a %s, got %s instead' % (
                expected_type.__name__, type(value).__name__))
