import click
from beautifultable import BeautifulTable

from pytest_django_queries.entry import Entry, iter_entries
from pytest_django_queries.filters import format_underscore_name_to_human


def print_entries(data):
    table = BeautifulTable()
    table.columns.header = ["Module", "Tests"]
    for module_name, module_entries in iter_entries(data):
        subtable = BeautifulTable()
        subtable.columns.header = [field for _, field in Entry.FIELDS]
        for entry in module_entries:
            subtable.rows.append([getattr(entry, field) for field, _ in Entry.FIELDS])
        table.rows.append([module_name, subtable])
    click.echo(table)


def entries_to_html(data, template):
    html_content = template.render(
        data=iter_entries(data), humanize=format_underscore_name_to_human
    )
    return html_content
