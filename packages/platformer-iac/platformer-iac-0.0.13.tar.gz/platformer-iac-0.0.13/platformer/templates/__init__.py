from jinja2.filters import FILTERS, environmentfilter

@environmentfilter
def filter_quote(environment, value):
    return f'"{value}"'

@environmentfilter
def filter_indent(environment, value, size=2):
    indent = " " * size
    return f'{indent} {value}'


FILTERS["quote"] = filter_quote
FILTERS["indent"] = filter_indent
