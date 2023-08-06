"""
Tools for customizing the `yaml <https://pyyaml.org/wiki/PyYAMLDocumentation>`_
module for advanced YAML serialization.
"""


from collections.abc import Mapping, MutableMapping
from functools import partial
from textwrap import wrap

import numpy as np
import yaml
from yaml.emitter import Emitter
from yaml.nodes import Node, ScalarNode, MappingNode
from yaml.representer import SafeRepresenter
from yaml.serializer import Serializer


__all__ = ['YAMLDumper', 'CommentedYAMLDumper', 'CommentedMapping']


class _YAMLMethod(classmethod):
    """
    Classmethod subclass factory used to register new representer methods on
    a `YAMLDumper`.

    It attaches to the method a ``.yaml_method_type`` attribute which is used
    by `BaseYAMLDumper` to collect new representers or multi_representers by
    iterating over all class members and looking for this attribute.
    """

    @classmethod
    def _decorate(cls, typeobj, yaml_method_type=None):
        """Returns a decorator function that can be used to wrap a method."""

        def decorator(func):
            meth = cls(func)
            meth.typeobj = typeobj
            meth.yaml_method_type = yaml_method_type
            return meth

        return decorator

    @classmethod
    def make_yaml_method_type(cls, method_type):
        return partial(cls._decorate, yaml_method_type=method_type)


representer = _YAMLMethod.make_yaml_method_type('representer')
multi_representer = _YAMLMethod.make_yaml_method_type('multi_representer')


class BaseYAMLDumper(yaml.SafeDumper):
    """
    A `yaml.Dumper` base class that makes it easier to register new type
    representers and multi-representers in class body.

    Simply tag methods as ``@representer`` or ``@multi_representer`` along with
    the relevant type (e.g. ``@representer(MyCustomClass)``.  Representer
    methods are treated automatically as `classmethods <classmethod>`.

    Examples
    --------
    >>> import yaml
    >>> from dnadna.utils.yaml import BaseYAMLDumper, representer
    >>> class MyClass:
    ...     def __init__(self, x):
    ...         self.x = x
    ...
    >>> class MyYAMLDumper(BaseYAMLDumper):
    ...     @representer(MyClass)
    ...     def myclass_representer(cls, dumper, obj):
    ...         return dumper.represent_int(obj.x)
    ...
    >>> m = MyClass(1)
    >>> print(yaml.dump(m, Dumper=MyYAMLDumper))
    1
    ...
    """

    def __init_subclass__(cls):
        for name, obj in list(cls.__dict__.items()):
            if isinstance(obj, _YAMLMethod):
                # Resolve the class-bound method
                method = getattr(cls, name)
                yaml_method = getattr(cls, 'add_' + obj.yaml_method_type)
                yaml_method(obj.typeobj, method)


class YAMLDumper(BaseYAMLDumper):
    """
    `yaml.SafeDumper` with representers for additional types, such as NumPy
    arrays and scalars.

    This serializes NumPy types as standard YAML types, so it does not
    round-trip back to NumPy types; hence it is primarily as a convenience for
    dumping objects that happen to contain NumPy types.

    Examples
    --------
    >>> import numpy as np
    >>> import yaml
    >>> from dnadna.utils.yaml import YAMLDumper
    >>> a = np.array([1, 2.0, 3.5])
    >>> print(yaml.dump(a, Dumper=YAMLDumper, default_flow_style=True))
    [1.0, 2.0, 3.5]
    >>> print(yaml.dump(a[0], Dumper=YAMLDumper))
    1.0
    ...
    """

    @multi_representer(np.ndarray)
    def numpy_array_representer(cls, dumper, obj):
        return dumper.represent_list(obj.tolist())

    @multi_representer(np.number)
    def numpy_scalar_representer(cls, dumper, obj):
        # TODO: This should implement support for complex numbers if necessary
        # Dumper.represent_data will automatically use the correct representer
        # and tags for known data types
        return dumper.represent_data(obj.item())


# The following classes implement dumping YAML files with comments for mappings
# and mapping items.
# The details of how and why this works are documented extensively at:
# https://stackoverflow.com/a/60508214/982257
#
# TODO: Document me!
class CommentedMapping(MutableMapping):
    """TODO: Document me!"""

    def __init__(self, d, comment=None, comments={}):
        self.mapping = d
        self.comment = comment
        self.comments = comments

    def get_comment(self, *path):
        if not path:
            return self.comment

        # Look the key up in self (recursively) and raise a
        # KeyError or other execption if such a key does not
        # exist in the nested structure
        sub = self.mapping
        for p in path:
            if isinstance(sub, CommentedMapping):
                # Subvert comment copying
                sub = sub.mapping[p]
            else:
                sub = sub[p]

        comment = None
        if len(path) == 1:
            comment = self.comments.get(path[0])
        if comment is None:
            comment = self.comments.get(path)
        return comment

    def __getitem__(self, item):
        val = self.mapping[item]
        if (isinstance(val, (dict, Mapping)) and
                not isinstance(val, CommentedMapping)):
            comment = self.get_comment(item)
            comments = {k[1:]: v for k, v in self.comments.items()
                        if isinstance(k, tuple) and len(k) > 1 and k[0] == item}
            val = self.__class__(val, comment=comment, comments=comments)
        return val

    def __setitem__(self, item, value):
        self.mapping[item] = value

    def __delitem__(self, item):
        del self.mapping[item]
        for k in list(self.comments):
            if k == item or (isinstance(k, tuple) and k and k[0] == item):
                del self.comments[k]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return (
            f'{type(self).__name__}({self.mapping}, comment={self.comment!r},'
            f'comments={self.comments})')


class CommentEvent(yaml.Event):
    """
    Simple stream event representing a comment to be output to the stream.

    Parameters
    ----------
    value : str
        The text of the comment.
    prepend : bool, optional
        If `True`, prepend a newline before outputting this comment.
    append : bool, optional
        If `True`, append a newline after outputting this comment.
    """
    def __init__(self, value, start_mark=None, end_mark=None, prepend=False,
            append=False):
        super().__init__(start_mark, end_mark)
        self.value = value
        self.prepend = prepend
        self.append = append


class CommentedEmitter(Emitter):
    """TODO: Document me!"""

    def need_more_events(self):
        if self.events and isinstance(self.events[0], CommentEvent):
            # If the next event is a comment, always break out of the event
            # handling loop so that we divert it for comment handling
            return True
        return super().need_more_events()

    def need_events(self, count):
        # Hack-y: the minimal number of queued events needed to start
        # a block-level event is hard-coded, and does not account for
        # possible comment events, so here we increase the necessary
        # count for every comment event
        comments = [e for e in self.events if isinstance(e, CommentEvent)]
        return super().need_events(count + min(count, len(comments)))

    def emit(self, event):
        if self.events and isinstance(self.events[0], CommentEvent):
            # Write the comment, then pop it off the event stream and continue
            # as normal
            ev = self.events[0]
            self.write_comment(ev.value, ev.prepend, ev.append)
            self.events.pop(0)

        super().emit(event)

    def write_comment(self, comment, prepend=False, append=False):
        indent = self.indent or 0
        width = self.best_width - indent - 2  # 2 for the comment prefix '# '

        # First split comment into paragraphs
        paragraphs = comment.split('\n\n')

        for idx, paragraph in enumerate(paragraphs):
            lines = ['# ' + line for line in wrap(paragraph, width)]

            if idx:
                # If not the first paragraph, add a blank line comment
                lines.insert(0, '#')

            for lineno, line in enumerate(lines):
                if self.encoding:
                    line = line.encode(self.encoding)
                if lineno == 0 and prepend:
                    self.write_line_break()
                    self.write_line_break()
                self.write_indent()
                self.stream.write(line)
                self.write_line_break()
                if lineno == (len(lines) - 1) and append:
                    self.write_line_break()


class CommentedNode(Node):
    """Dummy base class for all nodes with attached comments."""


class CommentedScalarNode(ScalarNode, CommentedNode):
    """TODO: Document me!"""

    def __init__(self, tag, value, start_mark=None, end_mark=None, style=None,
                 comment=None, prepend=False, append=False):
        super().__init__(tag, value, start_mark, end_mark, style)
        self.comment = comment
        self.prepend = prepend
        self.append = append


class CommentedMappingNode(MappingNode, CommentedNode):
    """TODO: Document me!"""

    def __init__(self, tag, value, start_mark=None, end_mark=None,
                 flow_style=None, comment=None, comments={}, prepend=False,
                 append=False):
        super().__init__(tag, value, start_mark, end_mark, flow_style)
        self.comment = comment
        self.comments = comments
        self.prepend = prepend
        self.append = append


class CommentedSerializer(Serializer):
    """TODO: Document me!"""

    def serialize_node(self, node, parent, index):
        if (node not in self.serialized_nodes and
                isinstance(node, CommentedNode) and
                not (isinstance(node, CommentedMappingNode) and
                     isinstance(parent, CommentedMappingNode))):
            # Emit CommentEvents, but only if the current node is not a
            # CommentedMappingNode nested in another CommentedMappingNode (in
            # which case we would have already emitted its comment via the
            # parent mapping)
            if node.comment is not None:
                self.emit(CommentEvent(node.comment, prepend=node.prepend,
                                       append=node.append))

        super().serialize_node(node, parent, index)


class CommentedRepresenter(SafeRepresenter):
    """TODO: Document me!"""

    def represent_commented_mapping(self, data):
        node = super().represent_dict(data)
        comments = {k: data.get_comment(k) for k in data}
        value = []
        for idx, (k, v) in enumerate(node.value):
            if k.value in comments:
                prepend = idx != 0
                k = CommentedScalarNode(
                        k.tag, k.value,
                        k.start_mark, k.end_mark, k.style,
                        comment=comments[k.value], prepend=prepend)
            value.append((k, v))

        node = CommentedMappingNode(
            node.tag,
            value,
            flow_style=False,  # commented dicts must be in block style
            comment=data.get_comment(),
            comments=comments,
            append=True
        )
        return node

    yaml_representers = SafeRepresenter.yaml_representers.copy()
    yaml_representers[CommentedMapping] = represent_commented_mapping


class CommentedYAMLDumper(CommentedEmitter, CommentedSerializer,
                          CommentedRepresenter, YAMLDumper):
    """
    Extension of `YAMLDumper` that supports writing `Commmented Mappings
    <CommentedMapping>` with all comments output as YAML comments.

    Examples
    --------
    >>> from dnadna.utils.yaml import CommentedMapping, CommentedYAMLDumper
    >>> import yaml
    >>> d = CommentedMapping({
    ...     'a': 1,
    ...     'b': 2,
    ...     'c': {'d': 4, 'e': 5},
    ... }, comment='my commented dict', comments={
    ...     'a': 'a comment',
    ...     'b': 'b comment',
    ...     'c': 'long string ' * 44,
    ...     ('c', 'd'): 'd comment',
    ...     ('c', 'e'): 'e comment'
    ... })
    >>> print(yaml.dump(d, Dumper=CommentedYAMLDumper))
    # my commented dict
    <BLANKLINE>
    # a comment
    a: 1
    <BLANKLINE>
    # b comment
    b: 2
    <BLANKLINE>
    # long string long string long string long string long string long string long
    # string long string long string long string long string long string long string
    # long string long string long string long string long string long string long
    # string long string long string long string long string long string long string
    # long string long string long string long string long string long string long
    # string long string long string long string long string long string long string
    # long string long string long string long string long string
    c:
      # d comment
      d: 4
    <BLANKLINE>
      # e comment
      e: 5
    """

# End commented YAML dumper implementation.
