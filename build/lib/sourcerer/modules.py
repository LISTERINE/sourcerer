#!env/bin/python
from sourcerer.base import Statement
from formatters import Formatter
from sys import stdout
from pdb import set_trace


class Document(Statement):
    """ All content is rooted in this base document

    All a document really is, is a statement with a blank line ending and an output method.
    """

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.line_ending = ''

    def output(self, output_file_name=''):
        """ Write out the syntax tree """

        syntax_string = ''.join(self)
        if not output_file_name:
            stdout.write(syntax_string)
        else:
            with open(output_file_name, 'w') as output:
                output.write(syntax_string)

