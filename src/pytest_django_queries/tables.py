import click
from beautifultable import BeautifulTable

from pytest_django_queries.entry import Entry, iter_entries
from pytest_django_queries.filters import format_underscore_name_to_human


def print_entries(data):
    table = BeautifulTable()
    table.column_headers = ["Module", "Tests"]
    for module_name, module_entries in iter_entries(data):
        subtable = BeautifulTable()
        subtable.column_headers = [field for _, field in Entry.FIELDS]
        for entry in module_entries:
            subtable.append_row([getattr(entry, field) for field, _ in Entry.FIELDS])
        table.append_row([module_name, subtable])
    click.echo(table)


def entries_to_html(data, template):
    html_content = template.render(
        data=iter_entries(data), humanize=format_underscore_name_to_human
    )
    return html_content
