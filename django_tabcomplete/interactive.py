import re

from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet


def _filter_kwarg_completer(shell, event, queryset):
    # TODO: handle annotations
    model = queryset.model
    prefix, sep, so_far = event.symbol.rpartition('__')
    path = prefix.split('__') if prefix else []
    prefix += sep
    field = None
    for part in path:
        if model is None:
            return []
        field = model._meta.get_field(part)
        if field.is_relation:
            model = field.related_model
        else:
            model = None
    out = []
    if field is not None and hasattr(field, 'class_lookups'):
        out.extend(prefix + l + '=' for l in field.class_lookups)

    if model is not None:
        # XXX: could return names each suffixed by '=' and '__'
        # whether this helps user may depend on frontend
        out.extend(prefix + f.name for f in model._meta.get_fields())
        if field is not None:
            # XXX: could add all class_lookups for primary key, but too messy
            out.append(prefix + 'in=')

    return out


# Cannot identify method objects directly, as BaseManager wraps QuerySet
# methods with anonymous functions.
# Will identify by parent class and attribute name
_COMPLETER_MAP = {
    'filter': _filter_kwarg_completer,
    'exclude': _filter_kwarg_completer,
    'get': _filter_kwarg_completer,
}


def _find_callable(event):
    # This is tweaked from ipython.core.completer. See IPYTHON_LICENCE.rst for
    # applicable copyrights.

    if "." in event.symbol:  # a parameter or completeable arg cannot be dotted
        return []
    try:
        regexp = django_db_complete.__funcParamsRegex
    except AttributeError:
        regexp = django_db_complete.__funcParamsRegex = re.compile(r'''
            '.*?(?<!\\)' |    # single quoted strings or
            ".*?(?<!\\)" |    # double quoted strings or
            \w+          |    # identifier
            \S                # other characters
            ''', re.VERBOSE | re.DOTALL)
    # 1. find the nearest identifier that comes before an unclosed
    # parenthesis before the cursor
    # e.g. for "foo (1+bar(x), pa<cursor>,a=1)", the candidate is "foo"
    tokens = regexp.findall(event.text_until_cursor)
    tokens.reverse()
    iterTokens = iter(tokens)
    openPar = 0

    for token in iterTokens:
        if token == ')':
            openPar -= 1
        elif token == '(':
            openPar += 1
            if openPar > 0:
                # found the last unclosed parenthesis
                break
    else:
        return []
    # 2. Concatenate dotted names ("foo.bar" for "foo.bar(x, pa" )
    ids = []
    isId = re.compile(r'\w+$').match

    while True:
        try:
            ids.append(next(iterTokens))
            if not isId(ids[-1]):
                ids.pop()
                break
            if not next(iterTokens) == '.':
                break
        except StopIteration:
            break

    return ids[::-1]


def django_db_complete(shell, event):
    ids = _find_callable(event)

    if len(ids) == 1:
        # Need . to match attribute name (unfortunately!)
        return []

    attr = ids[0]
    if attr not in _COMPLETER_MAP:
        return []

    parent_expr = '.'.join(ids[1:])
    try:
        parent = eval(parent_expr, shell.Completer.namespace)
    except:
        try:
            parent = eval(parent_expr, shell.Completer.global_namespace)
        except:
            return []

    if isinstance(parent, (QuerySet, BaseManager)):
        if not isinstance(parent, QuerySet):
            parent = parent.all()
        # TODO: also pass list of filled args or position
        return _COMPLETER_MAP[attr](shell, event, parent)


def activate():
    """Hook in as IPython completer plugin"""
    from IPython import get_ipython
    ip = get_ipython()
    if ip is None:
        return
    import sys
    print >> sys.stderr, "!!!"
    print >> open('/tmp/stderr', 'w'), "!!!"
    ip.set_hook('complete_command', django_db_complete, re_key=r'.*')
