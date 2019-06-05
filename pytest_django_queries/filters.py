import re

BLACKLISTED_WORDS_RE = re.compile(r"(^|\.)tests?\.?", re.I)


def format_underscore_name_to_human(name):
    return re.sub(BLACKLISTED_WORDS_RE, "", name.replace("_", " ")).strip()
