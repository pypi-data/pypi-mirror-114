"""Additional uncategorized utilities."""


import itertools
import os
import pathlib
import re
import string
import sys
from collections import defaultdict, deque
from fnmatch import fnmatch

import tqdm

from tqdm.utils import ObjectWrapper


def dict_slice(d, *keys, allow_missing=False):
    """
    Given a dict, return a copy of that dict with only the selected keys.
    If any of the given keys are not in the dictionary a `KeyError` will be
    raised for the first key not found, unless ``allow_missing=True``.

    Examples
    --------

    >>> from dnadna.utils.misc import dict_slice
    >>> dict_slice({})
    {}
    >>> d = {'a': 1, 'b': 2, 'c': 3}
    >>> dict_slice(d)
    {}
    >>> dict_slice(d, 'a', 'c')
    {'a': 1, 'c': 3}
    >>> dict_slice(d, 'a', 'd')
    Traceback (most recent call last):
    ...
    KeyError: 'd'
    >>> dict_slice(d, 'a', 'd', allow_missing=True)
    {'a': 1}
    """

    s = {}
    for k in keys:
        try:
            s[k] = d[k]
        except KeyError:
            if not allow_missing:
                raise

    return s


def dict_merge(d: dict, *f: dict) -> dict:
    """
    Return a copy of `dict` ``d``, with updates applied to it from zero or more
    dicts in ``f``.

    If ``d2`` is a nested `dict` then updates are applied partially, so that
    rather than completely replacing the value of the same key in ``d1``, it
    just applies a `dict.update` to value of that key in ``d1``.  If there is
    a conflict (e.g. the same key in each `dict` does not correspond to the
    same type) then that value is replaced entirely.

    Examples
    --------

    >>> from dnadna.utils.misc import dict_merge
    >>> d1 = {}
    >>> d2 = dict_merge(d1); d2
    {}
    >>> d1 is d2
    False
    >>> dict_merge({}, {'a': 1})
    {'a': 1}
    >>> dict_merge({'a': 1, 'b': 2}, {'a': 2, 'c': 3})
    {'a': 2, 'b': 2, 'c': 3}
    >>> dict_merge({'a': 1, 'b': 2}, {'a': 2}, {'a': 3, 'c': 4})
    {'a': 3, 'b': 2, 'c': 4}
    >>> dict_merge({'a': {'b': {'c': 1, 'd': 2}}}, {'a': {'b': {'c': 2}}})
    {'a': {'b': {'c': 2, 'd': 2}}}
    >>> dict_merge({'a': {'b': 1}}, {'a': 2})
    {'a': 2}
    """

    d = d.copy()
    for d2 in f:
        for k, v in d2.items():
            u = d.get(k)
            if isinstance(u, dict) and isinstance(v, dict):
                d[k] = dict_merge(u, v)
            else:
                d[k] = v

    return d


def parse_format(format_str):
    """
    Given a Python format string as parsed by `string.Formatter`, return a
    `dict` mapping field names to a list of tuples of their format spec (if
    any) and their converter (if any) for each time that field occurs in the
    format string.

    This only works for positional and keyword fields.

    Examples
    --------

    >>> from dnadna.utils.misc import parse_format
    >>> parse_format(
    ...     'scenario_{scenario:04}/{name}_{scenario}_{replicate}.npz')
    {'scenario': [('04', None), ('', None)], 'name': [('', None)],
     'replicate': [('', None)]}

    """

    formatter = string.Formatter()
    formats = defaultdict(list)

    for item in formatter.parse(format_str):
        _, field_name, spec, converter = item
        if field_name:
            formats[field_name].append((spec, converter))

    return dict(formats)


def format_to_re(format_str, **kwargs):
    r"""
    Convert a format string to a regular expression, such that any format
    fields may replaced with regular expression syntax, and any literals are
    properly escaped.

    As a special case, if a 2-tuple is given for the value of a field, the
    first time the field appears in the format string the first element of the
    tuple is used as the replacement, and the second element is used for all
    subsequence replacements.

    Examples
    --------

    >>> from dnadna.utils.misc import format_to_re

    This example uses a backslash just to add a little Windows flavor:

    >>> filename_format = \
    ...     r'scenario_{scenario}\{name}_{scenario}_{replicate}.npz'
    >>> filename_re = format_to_re(filename_format,
    ...     scenario=(r'(?P<scenario>0*\d+)', r'0*\d+'),
    ...     replicate=r'0*\d+', name=r'\w+')
    >>> filename_re
    'scenario_(?P<scenario>0*\\d+)\\\\\\w+_0*\\d+_0*\\d+\\.npz'
    >>> import re
    >>> filename_re = re.compile(filename_re)
    >>> filename_re
    re.compile(...)

    This regular expression can be used to match arbitrary filenames to
    determine whether or not they are in the format specified by the original
    ``filename_format`` template, as well as to extract the values of fields by
    using groups:

    >>> match = filename_re.match(r'scenario_000\my_model_000_000.npz')
    >>> match is not None
    True
    >>> match.group('scenario')
    '000'
    >>> filename_re.match(r'scenario_000\my_model_garbage.npz') is None
    True
    """

    formatter = string.Formatter()
    new_format = []
    seen_fields = set()

    for item in formatter.parse(format_str):
        literal, field_name, spec, converter = item
        new_format.append(re.escape(literal))

        if field_name is None:
            continue

        replacement = kwargs[field_name]

        if isinstance(replacement, tuple) and len(replacement) == 2:
            if field_name in seen_fields:
                replacement = replacement[1]
            else:
                replacement = replacement[0]

        new_format.append(replacement)
        seen_fields.add(field_name)

    return ''.join(new_format)


def reformat_format(format_str, format_replacements={}, force=False):
    """
    Given a Python format string as parsed by `string.Formatter`, return a new
    format string with new format specs for some of the fields.

    ``format_replacements`` should be a dict mapping field names in the
    original format string, to format specs that should be applied to those
    fields in the new format string.

    For any field in the original format string, if that field *does not* have
    a specified format spec, and that field name is in ``format_replacements``,
    provide, use the new format spec for that field in the output.  If
    ``force=True`` then use the new format spec even if a field has an existing
    format spec.

    Examples
    --------

    This is used in particular when guessing zero-padding to apply to scenario
    and replicate IDs in filenames.  The user can provide a very generic
    filename format which does not make assumptions about the amount of
    zero-padding, which may depend, for a given data set, on the number of
    scenarios and replicates:

    >>> filename_format = \\
    ...     'scenario_{scenario}/{name}_{scenario}_{replicate}.npz'

    Normally, given a scenario number and a replicate number this format string
    is used to produce the relevant filename like:

    >>> filename_format.format(name='MyModel', scenario=2, replicate=22)
    'scenario_2/MyModel_2_22.npz'

    However, for the given data set we might have 1000 scenarios and 100
    replicates of each scenario, so each number is zero-padded by an
    appropriate amount in the filename.  The user *may* wish to make this
    explicit by giving a filename format like:

    >>> filename_format_2 = (
    ...    'scenario_{scenario:04}/'
    ...    '{name}_{scenario:04}_{replicate:03}.npz')
    >>> filename_format_2.format(name='MyModel', scenario=2,
    ...                          replicate=22)
    'scenario_0002/MyModel_0002_022.npz'

    However, this is not required: The appropriate format specs for the
    ``scenario`` and ``replicate`` fields can be determined later by metadata
    about the simulation, and this function can be used to produce a new format
    string that includes that appropriate zero-padded format spec for those
    fields:

    >>> from dnadna.utils.misc import reformat_format
    >>> filename_format_3 = reformat_format(filename_format,
    ...    format_replacements={'scenario': '04', 'replicate': '03'})
    >>> filename_format_3 == filename_format_2
    True

    If ``force=True`` is used, this can even override fields that already have
    a format specification:

    >>> reformat_format(filename_format_2,
    ...     format_replacements={'replicate': '04'}, force=True)
    'scenario_{scenario:04}/{name}_{scenario:04}_{replicate:04}.npz'

    """

    formatter = string.Formatter()
    new_format = []

    for item in formatter.parse(format_str):
        literal, field_name, spec, converter = item
        new_format.append(literal)

        if field_name is None:
            # The case for any trailing literal text
            continue

        if (not spec or force) and field_name in format_replacements:
            spec = format_replacements[field_name]

        new_format.append('{')
        new_format.append(field_name)
        if converter:
            new_format.append('!' + converter)
        if spec:
            new_format.append(':' + spec)
        new_format.append('}')

    return ''.join(new_format)


def zero_pad_format(format_str, **fields):
    """
    For fields in a format string that do not already have a format specifier,
    zero-pad that field with enough zeros for a specified max size of that
    field.

    Examples
    --------

    >>> from dnadna.utils.misc import zero_pad_format
    >>> format_str = 'scenario_{scenario}_replicate_{replicate}'
    >>> new_format_str = zero_pad_format(format_str, scenario=101, replicate=11)
    >>> new_format_str
    'scenario_{scenario:03}_replicate_{replicate:02}'
    >>> new_format_str.format(scenario=1, replicate=2)
    'scenario_001_replicate_02'
    """

    format_replacements = {
        f: '0{}'.format(len(str(s - 1))) for f, s in fields.items()
    }

    return reformat_format(format_str, format_replacements=format_replacements)


def decamelcase(s, sep='_'):
    """
    Converts a CamelCase string to lower-case like "camel-case".

    If it consists of only one word like "Camel" it is equivalent to
    `str.lower`, otherwise each word is lower-cased and separated by
    ``sep='_'``.

    Examples
    --------

    >>> from dnadna.utils.misc import decamelcase
    >>> decamelcase('Camel')
    'camel'
    >>> decamelcase('CamelCase')
    'camel_case'
    >>> decamelcase('not_camel_case')
    'not_camel_case'

    Consecutive strings of ALLCAPS are kept together but lower-cased:

    >>> decamelcase('SPIDNA1')
    'spidna1'
    >>> decamelcase('MyDNANet')
    'my_dna_net'

    "camelCase" style strings (with the first word starting with a lower-case
    letter) are also supported:

    >>> decamelcase('camelCase')
    'camel_case'
    """

    # NOTE: Questionable whether this will work for unicode characters
    cc_re = re.compile(r'([A-Z][A-Z0-9]*[A-Z0-9](?![a-z])|[A-Z][a-z0-9]*)')
    ret = sep.join(filter(None, (w.lower() for w in cc_re.split(s))))
    if not ret:
        return s

    return ret


class _TqdmDummyFile(ObjectWrapper):
    """Dummy file-like that will write to tqdm"""
    def write(self, x, nolock=False):
        x = x.rstrip()
        if x:
            tqdm.tqdm.write(x, file=self._wrapped, nolock=nolock)


class stdio_redirect_tqdm:
    """
    Context manager to redirect stdout/stderr while a tqdm progress bar is
    running.

    Based on the recipe from https://github.com/tqdm/tqdm#redirecting-writing
    But this version is re-entrant in that if stdio is already being redirected
    by an outer with statement with this context manager, it won't re-redirect.
    """

    orig_out_err = None
    _level = 0

    @property
    def stdout(self):
        if self.orig_out_err is not None:
            return self.orig_out_err[0]

        return None

    @property
    def stderr(self):
        if self.orig_out_err is not None:
            return self.orig_out_err[1]

        return None

    def __enter__(self):
        self.__class__._level += 1

        if self.orig_out_err is not None:
            return self

        orig_out_err = sys.stdout, sys.stderr
        self.__class__.orig_out_err = orig_out_err
        sys.stdout, sys.stderr = map(_TqdmDummyFile, orig_out_err)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.__class__._level -= 1
            if self.__class__._level == 0:
                # Restory original sys.stdout/err
                sys.stdout, sys.stderr = self.orig_out_err
                self.__class__.orig_out_err = None
        finally:
            if exc_value is not None:
                raise exc_value


def unique(sequence):
    """
    Return a `list` containing all unique elements of a given ``sequence``
    or iterable while preserving order of that sequence.

    In the case of duplicate elements, only the first instance of that element
    is kept.

    Examples
    --------

    >>> from dnadna.utils.misc import unique
    >>> unique([1, 2, 3, 4, 3, 2, 5, 1, 3])
    [1, 2, 3, 4, 5]

    """

    seen = set()

    def not_seen(x):
        if x in seen:
            return False

        seen.add(x)
        return True

    return [x for x in sequence if not_seen(x)]


def consume(iterator):
    """
    Runs through an entire iterator while throwing away the items.

    This is an efficient way to exhaust an iterator without the overhead of
    saving its items.  This can be useful sometimes, especially in testing,
    to run through every element of iterators that might have some side-effect
    where we don't actually care about the return values.

    Examples
    --------

    >>> from dnadna.utils.misc import consume
    >>> class MyIter:
    ...     def __init__(self, length):
    ...         self.length = length
    ...         self.x = 0  # Incremented as a side-effect of iteration
    ...     def __iter__(self):
    ...         for x in range(self.length):
    ...             self.x += 1
    ...             yield x
    ...
    >>> it = MyIter(10)
    >>> consume(iter(it))
    >>> it.x
    10
    """

    # Using a zero-sized deque is known as an efficient, if non-obvious way to
    # do this, as it is implemented in C
    deque(iterator, maxlen=0)


def flatten(lists):
    """
    Flatten a list of lists to a single level of nesting.

    From the recipe in the Python standard library docs:
    :ref:`python:itertools-recipes`.

    Examples
    --------

    >>> from dnadna.utils.misc import flatten
    >>> flattened = flatten([[1, 2], [3, 4], [5, 6, 7], [8, 9]])
    >>> flattened
    <itertools.chain object at 0x...>
    >>> list(flattened)
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """

    return itertools.chain.from_iterable(lists)


def indent(text, indent=4, first=True):
    """
    Indent lines of text, given either as a string, or list of lines, returning
    the indented text as a string.

    Examples
    --------
    >>> from dnadna.utils.misc import indent
    >>> indent('hello\\nworld')
    '    hello\\n    world'

    If ``first=False`` the first line is not indented:

    >>> indent('hello\\nworld', first=False)
    'hello\\n    world'
    """

    if isinstance(text, str):
        text = text.splitlines()

    return '\n'.join((' ' * (indent * int(first or idx > 0)) + line
                     for idx, line in enumerate(text)))


def first_paragraph(text):
    """
    Given a block of multi-line text, return just the first paragraph of that
    text.

    That is, the first sequence of lines (not counting leading whitespace) that
    are non-empty, up to the first all-whitespace or empty line.

    Examples
    --------

    >>> from dnadna.utils.misc import first_paragraph
    >>> text = '''\\
    ... This is the first paragraph.
    ... This is the second line of the first paragraph.
    ...
    ... This is the beginning of the second paragraph and so on...
    ... '''
    >>> print(first_paragraph(text))
    This is the first paragraph.
    This is the second line of the first paragraph.
    """

    first = []
    for line in text.splitlines():
        line = line.lstrip()
        if not line:
            if first:
                # We've reached a blank line after the beginning of the
                # paragraph
                break

            continue

        first.append(line)

    return '\n'.join(first)


# naïve regular expressions which assume interpreted text and hyperlinks cannot
# contain backticks (in fact I'm not even sure it's allowed in reST)
_sphinx_hyperlink_re = re.compile(r'`(?P<text>[^`]+)`_')

# NOTE: This could also be mis-interpreted as a hyperlinke if no role is
# present, so we process hyperlinks first
_sphinx_interpeted_text_re = re.compile(
        r'(:(?P<role>[^:]+):)?`(?P<text>[^`]+)`')
_sphinx_titled_ref_re = re.compile(r'(?P<title>[^<]+) <(?P<ref>[^>]+)>')

DESPHINXIFY_REF_ROLES = ['py:*', 'ref']
"""
Role names that are recognized by `desphinxify` as recognizing interpreted
text in the format ```title <reference>```.

Roles listed in this list may use any `fnmatch.fnmatch` wildcards.
"""


def desphinxify(text, default_role='py:obj', ref_roles=DESPHINXIFY_REF_ROLES):
    """
    Replaces text containing reST/Sphinx interpreted text with the plain text
    representation of that role.

    Interpreted text is text that looks like ```foo```, that is, text between
    single-backticks, or it can have an explicit role before it like
    ``:role:`foo```

    (Note: Technically interpreted text can have a role as a suffix as well
    but we never write it this way in the documentation for this package.)

    Certain roles such as ``:py:obj:`` and ``:ref:`` can contain formatted text
    in formats like ``:ref:`title <reference>```, where the ``title`` is the
    text that is displayed when rendered, whereas ``<reference>`` is a label or
    Python object name that should be linked to.  There are likely other roles
    that are interpreted in this way, but only a few known ones are recognized
    by default.  By default this also recognizes basic reST-style hyperlinks
    formatted like ```title <uri>`_``.  In this case the URI is still output as
    well.

    .. todo::

        There already exist Python modules that do this as well, and more
        thoroughly and robustly.  There are many cases this solution does not
        yet handle.  It would be good to look into using one of the existing
        solutions instead.  But this is good enough for the limited use-cases
        so far of this package.

    Examples
    --------

    >>> from dnadna.utils.misc import desphinxify
    >>> print(desphinxify("blah blah `interpreted` blah"))
    blah blah interpreted blah
    >>> print(desphinxify("blah blah `title <objname>`"))
    blah blah title
    >>> print(desphinxify("blah blah :ref:`title <label>`"))
    blah blah title

    If a title is not specified in a ``:ref:`` we still just return
    the label; we are not accessing the full Sphinx doctree in any
    way, so this is the best we can do:

    >>> print(desphinxify("blah blah :ref:`_label`"))
    blah blah _label

    Other, arbitrary roles, do not have their text re-interpreted in any way:

    >>> print(desphinxify("blah blah :math:`a < b > c`"))
    blah blah a < b > c

    Hyperlinks still keep the URI in the output:

    >>> print(desphinxify("blah blah `Python <https://www.python.org>`_ blah"))
    blah blah Python <https://www.python.org> blah

    An real example of this used in the codebase:

    >>> from dnadna.examples.one_event import OneEventSimulator
    >>> from dnadna.utils.misc import first_paragraph
    >>> print(desphinxify(first_paragraph(OneEventSimulator.__doc__)))
    An example msprime-based simulator with demographic parameters for a model
    with one population change event.
    """

    # First replace hyperlinks, if any
    def sub_hyperlink(match):
        t = match.group('text')
        m = _sphinx_titled_ref_re.match(t)
        if m:
            title = m.group('title')
            uri = m.group('ref')
            return f'{title} <{uri}>'

        return t

    def sub_interpreted(match):
        t = match.group('text')
        r = match.group('role')
        if r is None:
            r = default_role

        if any(fnmatch(r, pat) for pat in ref_roles):
            m = _sphinx_titled_ref_re.match(t)
            if m:
                return m.group('title')

        return t

    text = _sphinx_hyperlink_re.sub(sub_hyperlink, text)
    text = _sphinx_interpeted_text_re.sub(sub_interpreted, text)
    return text


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name, fmt='f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        return f'{self.name} {self.val:{self.fmt}} ({self.avg:{self.fmt}})'


def format_docstring(*args, **kwargs):
    """
    Decorator which formats a docstring containing format variables.

    The values for variables used in the format string are passed to this
    decorator.

    Examples
    --------

    >>> from dnadna.utils.misc import format_docstring
    >>> @format_docstring(name='Celine')
    ... def hello(name):
    ...     \"\"\"Says hello.  For example, hello({name!r}).\"\"\"
    ...     print('Hello', name)
    ...
    >>> print(hello.__doc__)
    Says hello.  For example, hello('Celine').
    """

    def decorator(func_or_cls):
        doc = func_or_cls.__doc__
        if doc:
            func_or_cls.__doc__ = doc.format(*args, **kwargs)
        return func_or_cls

    return decorator


class capture_stdio:  # noqa: N801
    """Redirect the system stdout and/or stderr to a file."""

    def __init__(self, stdout_file=None, stderr_file=None):
        self._stdio_files = [stdout_file, stderr_file]
        self._close_files = [False, False]
        self._prev_stdio_fds = [None, None]
        self._prev_stdio_files = [None, None]

    def __enter__(self):
        self._prev_stdio_files = [sys.stdout, sys.stderr]
        for idx, f in enumerate(self._stdio_files):
            if f is None:
                continue

            if isinstance(f, (str, pathlib.Path)):
                f = open(f)
                self._stdio_files[idx] = f
                self._close_files[idx] = True

            stdio_file = self._prev_stdio_files[idx]
            self._prev_stdio_fds[idx] = os.dup(stdio_file.fileno())
            os.dup2(f.fileno(), stdio_file.fileno())

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for idx, f in enumerate(self._stdio_files):
            if f is None:
                continue

            os.dup2(self._prev_stdio_fds[idx],
                    self._prev_stdio_files[idx].fileno())
            if self._close_files[idx]:
                f.close()
