"""Additional custom Sphinx extensions."""


import io
import os.path as pth

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives.code import LiteralInclude, CodeBlock
from sphinx.ext.autodoc.importer import import_object

from ..config import DictSerializer, save_dict_annotated
from ..jsonschema import SCHEMA_SUPPORTED_VERSIONS


__version__ = '0.1.0'


class SchemaInclude(LiteralInclude):
    """
    Like ``.. literalinclude:: <filename>`` but specifically for JSON Schema
    files.

    Includes the ability to output an example config file that conforms to the
    listed schema.
    """

    # Takes the same options as literalinclude, except for a few inapplicable
    # options which are removed
    option_spec = LiteralInclude.option_spec.copy()
    option_spec.pop('pyobject', None)
    option_spec.pop('diff', None)
    option_spec.update({
        'example': directives.unchanged_required,
        'annotated-example': directives.unchanged_required,
        'example-width': int
    })

    def run(self):
        document = self.state.document
        try:
            serializer = DictSerializer.serializer_for(self.arguments[0])
        except NotImplementedError as exc:
            return [document.reporter.warning(exc, line=self.lineno)]

        language = self.options.get('language')
        if language is None:
            # Determine the language from one of the supported file types
            language = self.options['language'] = serializer.language

        # pre-parse the specified schema to determine that it is in fact
        # valid JSON schema
        try:
            rel_filename, filename = self.env.relfn2path(self.arguments[0])
            schema = serializer.load(rel_filename)
            for validator in SCHEMA_SUPPORTED_VERSIONS:
                validator.check_schema(schema)
        except Exception as exc:
            return [document.reporter.warning(exc, line=self.lineno)]

        # Automatically give this included schema a label to reference it by,
        # if one has not been given explicitly
        name = 'schema-' + pth.splitext(pth.basename(rel_filename))[0]
        self.options.setdefault('name', name)

        # TODO: Maybe add an index entry for the schema?

        retnodes = super().run()
        if isinstance(retnodes[0], nodes.system_message):
            # A warning was produced due to an exception in the directive
            # processing
            return retnodes

        example = self.options.get('example')
        annotated_example = self.options.get('annotated-example')

        # This is a bit of a kludge--the 'width' argument is only supported by
        # the YAMLSerializer at the moment, but it sucks we have to test for
        # that explicitly; I would like it if different serializers could be
        # more easily introspected for which options they accept (or just
        # automatically ignore options they don't understand)
        if serializer.language == 'yaml':
            serializer_kwargs = {'width': self.options.get('example-width', 68)}
        else:
            serializer_kwargs = {}

        def process_example(objname, annotated=False):
            try:
                obj = import_object(objname, '')[-1]
            except Exception as exc:
                return [document.reporter.warning(exc, line=self.lineno)]

            out = io.StringIO()

            if annotated:
                save_dict_annotated(obj, out, schema=schema, validate=True,
                                    serializer=serializer,
                                    **serializer_kwargs)
            else:
                serializer.save(obj, out, **serializer_kwargs)
            content = out.getvalue().splitlines()
            options = self.options.copy()
            options.pop('example', None)
            options.pop('annoted_example', None)
            cb = CodeBlock(
                    self.name,
                    [language],
                    self.options,
                    content,
                    self.lineno,
                    self.content_offset,
                    self.block_text,
                    self.state,
                    self.state_machine)
            return cb.run()

        if example or annotated_example:
            ex_section = nodes.section()
            ex_section.document = self.state.document
            title = 'Example'
            if example and annotated_example:
                title += 's'

            exnode = nodes.container()

            if example is not None:
                exnode += process_example(example)[0]

            if annotated_example is not None:
                exnode += process_example(annotated_example, annotated=True)[0]

            old_section_level = self.state.memo.section_level
            self.state.parent += retnodes[0]
            try:
                self.state.section(
                        title, '', FauxHeading(),
                        self.state_machine.abs_line_number(),
                        [exnode])
            finally:
                self.state.memo.section_level = old_section_level
                self.state.memo.title_styles.pop()

        # TODO: Do other stuff (e.g. append example)
        return retnodes


class FauxHeading(object):
    """
    A heading level that is not defined by a string. We need this to work with
    the mechanics of
    :py:meth:`docutils.parsers.rst.states.RSTState.check_subsection`.

    The important thing is that the length can vary, but it must be equal to
    any other instance of FauxHeading.
    """

    def __len__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, FauxHeading)


def setup(app):
    app.add_directive('schema', SchemaInclude)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
