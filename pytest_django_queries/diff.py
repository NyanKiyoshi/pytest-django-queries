# coding=utf-8
from collections import namedtuple

from pytest_django_queries.entry import Entry  # noqa
from pytest_django_queries.filters import format_underscore_name_to_human

_ROW_FIELD = namedtuple("_RowField", ("comp_field", "align_char", "length_field"))
_ROW_FIELDS = (
    _ROW_FIELD("test_name", "<", "test_name"),
    _ROW_FIELD("left_count", ">", "query_count"),
    _ROW_FIELD("right_count", ">", "query_count"),
    _ROW_FIELD("duplicate_count", ">", "duplicate_count"),
)
_ROW_PREFIX = "  "
_NA_CHAR = "-"


def entry_row(entry_comp, lengths):
    cols = []

    for field, align, length_key in _ROW_FIELDS:
        fmt = "{cmp.%s: %s%d}" % (field, align, lengths[length_key])
        cols.append(fmt.format(cmp=entry_comp, lengths=lengths))

    return "%(diff_char)s %(results)s" % (
        {"diff_char": entry_comp.diff, "results": "\t".join(cols)}
    )


def get_header_row(lengths):
    sep_row = []
    head_row = []

    for field, _, length_key in _ROW_FIELDS:
        length = lengths[length_key]
        sep_row.append("%s" % ("-" * length))
        head_row.append(
            "{field: <{length}}".format(field=field.replace("_", " "), length=length)
        )

    return "%(prefix)s%(head)s\n%(prefix)s%(sep)s" % (
        {"prefix": _ROW_PREFIX, "head": "\t".join(head_row), "sep": "\t".join(sep_row)}
    )


class DiffChars(object):
    NEGATIVE = "-"
    NEUTRAL = " "
    POSITIVE = "+"

    @classmethod
    def convert(cls, diff):
        if diff < 0:
            return DiffChars.POSITIVE
        if diff > 0:
            return DiffChars.NEGATIVE
        return DiffChars.NEUTRAL


class SingleEntryComparison(object):
    __slots__ = ["left", "right"]

    def __init__(self, left=None, right=None):
        """
        :param left: Previous version.
        :type left: Entry

        :param right: Newest version.
        :type right: Entry
        """

        self.left = left
        self.right = right

    def _diff_from_newest(self):
        """
        Returns the query count difference from the previous version.
        If there is no older version, we assume it's an "improvement" (positive output)
        If there is no new version, we assume it's not an improvement (negative output)
        """
        if self.left is None:
            return DiffChars.POSITIVE
        if self.right is None:
            return DiffChars.NEGATIVE
        return DiffChars.convert(self.right.query_count - self.left.query_count)

    @property
    def test(self):
        return self.left or self.right

    @property
    def test_name(self):
        return format_underscore_name_to_human(self.test.test_name)

    @property
    def left_count(self):
        return str(self.left.query_count) if self.left else _NA_CHAR

    @property
    def right_count(self):
        return str(self.right.query_count) if self.right else _NA_CHAR

    @property
    def duplicate_count(self):
        if self.right:
            return self.right.duplicate_count
        elif self.left:
            return self.left.duplicate_count
        return _NA_CHAR

    @property
    def diff(self):
        return self._diff_from_newest()

    def to_string(self, lengths):
        return entry_row(self, lengths=lengths)


class DiffGenerator(object):
    def __init__(self, entries_left, entries_right):
        """
        Generates the diffs from two files.

        :param entries_left:
        :type entries_left: List[Entry]
        :param entries_right:
        :type entries_right: List[Entry]
        """

        self.entries_left = entries_left
        self.entries_right = entries_right

        self._mapping = {}
        self._generate_mapping()
        self.longest_props = self._get_longest_per_prop()
        self.header_rows = get_header_row(lengths=self.longest_props)

    def _get_longest_per_prop(self):
        longest = {field.length_field: len(field.comp_field) for field in _ROW_FIELDS}
        entries = self.entries_left + self.entries_right

        for entry in entries:
            for field in _ROW_FIELDS:
                current_length = len(str(getattr(entry, field.comp_field, None)))
                if current_length > longest[field.length_field]:
                    longest[field.length_field] = current_length

        return longest

    def _map_side(self, entries, side_name):
        for entry in entries:
            module_map = self._mapping.setdefault(entry.module_name, {})

            if entry.test_name not in module_map:
                module_map[entry.test_name] = SingleEntryComparison()

            setattr(module_map[entry.test_name], side_name, entry)

    def _generate_mapping(self):
        self._map_side(self.entries_left, "left")
        self._map_side(self.entries_right, "right")

    def _iter_module(self, module_entries):
        yield self.header_rows
        for _, test_comparison in sorted(
            module_entries.items()
        ):  # type: SingleEntryComparison
            yield test_comparison.to_string(lengths=self.longest_props)

    def _iter_modules(self):
        for module_name, module_entries in sorted(self._mapping.items()):
            yield (
                format_underscore_name_to_human(module_name),
                self._iter_module(module_entries),
            )

    def __iter__(self):
        return self._iter_modules()
