from base import Statement
from formatters import Formatter
from pdb import set_trace

class Name(Statement):
    """ A variable/function/class/... name 
    
    n = Name("helloworld") -> (unquoted) helloworld
    """
    pass


class Str(Statement):
    """ A quoted string

    s = Str("hello world") -> literal 'hello world'
    """
    pass

class Num(Statement):
    """ A number """

    def __init__(self, n, *args, **kwargs):

        super(Num, self).__init__(*args, **kwargs)
        self.code = n

class Return(Statement):
    """ Terminate a function """

    def __init__(self, val=None, _type='return', *args, **kwargs):
        """
        Args:
            _type (str): type of terminator. Should be one of: return, pass, '' (or None)
            val (Statement): The Statement that is to be returned
        """
        super(Return, self).__init__(*args, **kwargs)
        self._type = _type if _type is not None else ''
        self.val = Statement.to_statement(val)
        self.line_ending = ''

    def generate(self):
        self.val.generate()
        val = self.val.render()
        self.code = ' '.join([self._type, val.next()])


class Docstring(Statement):
    def __init__(self, doc_string, *args, **kwargs):
        super(Docstring, self).__init__(*args, **kwargs)
        self.doc_string = doc_string

    def generate(self):
        self.code = '"""{}"""'.format(self.doc_string)
