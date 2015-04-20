from base import Statement, to_statement
from pdb import set_trace

class NameObj(Statement):
    """ A variable name 
    
    n = NameObj("helloworld") -> (unquoted) helloworld
    """
    pass


class StringObj(Statement):
    """ A quoted string

    s = StringObj("hello world") -> literal 'hello world'
    """
    pass

class ReturnObj(Statement):
    """ Terminate a function """

    def __init__(self, _type='return', val=None, *args, **kwargs):
        """
        Args:
            _type (str): type of terminator. Should be one of: return, pass, '' (or None)
            val (Statement): The Statement that is to be returned
        """
        super(ReturnObj, self).__init__(*args, **kwargs)
        self._type = _type if _type is not None else ''
        self.val = to_statement(val)
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
