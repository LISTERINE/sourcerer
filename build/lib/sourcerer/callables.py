#!env/bin/python

from base import Statement
from formatters import CallableFormatter
import inspect
from string import punctuation, maketrans
from pdb import set_trace


class FunctionObj(Statement):
    """The base of callable objects

    """

    def __init__(self,
                 name='',
                 arg_names=None,
                 kwarg_pairs=None,
                 varargs=False,
                 keywords=False, *args, **kwargs):
        """
        Args:
            name (str): The name of the callable
            arg_names (list): A list of  to become the positional argument names
            kwargs (dict): A dict of str:str to become the keyword argument names/defaults
            varargs (bool): Should the argument list contain *args
            keywords (bool): Should the argument list contain **kwargs
        """
        super(FunctionObj, self).__init__(*args, **kwargs)
        self.name = name
        self.arg_names = arg_names
        self.kwarg_pairs = kwarg_pairs
        self.varargs = varargs
        self.keywords = keywords
        self.header = "def {}{}:"

    @property
    def arg_names(self):
        return self._arg_names

    @arg_names.setter
    def arg_names(self, value):
        self._arg_names = value if value else []

    @property
    def kwarg_pairs(self):
        return self._kwarg_pairs

    @kwarg_pairs.setter
    def kwarg_pairs(self, value):
        self._kwarg_pairs = value if value else {}

    @property
    def varargs(self):
        return self._varargs

    @varargs.setter
    def varargs(self, value):
        self._varargs = value if value else None

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        self._keywords = value if value else None

    @property
    def arg_spec(self):
        return self.build_args_kwargs()

    def build_args_kwargs(self):
        """ Build the argspec for the function """
        args = self._arg_names + self._kwarg_pairs.keys()
        kwargs = self._kwarg_pairs.values()
        spec = inspect.ArgSpec(args=args,
                               varargs=self._varargs,
                               keywords=self._keywords,
                               defaults=kwargs)
        return inspect.formatargspec(*spec)

    def generate(self):
        """ Sets the def and : in a function header.

        Result will look like 'def fn(...):'
        """
        self.code = self.header.format(self.name, self.arg_spec)

    def format(self):
        CallableFormatter.apply(self)


class DecoratorObj(FunctionObj):
    """ Sets the @ on the header.
    result will look like '@fn(...)'
    """

    def __init__(self, *args, **kwargs):
        super(DecoratorObj, self).__init__(*args, **kwargs)
        self.header = "@{}{}"

    def build_renderer(self, *args, **kwargs):
        kwargs['increment'] = 0
        return self.render(*args, **kwargs)


class CallerObj(FunctionObj):
    """ Used to call functions or instatntiate Classes """

    def __init__(self, caller_list=None, *args, **kwargs):
        """
        Args:
            caller_list (list): The list of predecessor CallerObjects ex. [C1,f1,f2] = C1.f1().f2().self()
        """
        super(Caller, self).__init__(*args, **kwargs)
        self.caller_list = caller_list if caller_list else []
        self.varargs = varargs
        self.keywords = keywords
        self.header = "{}{}{}{}"

    @property
    def caller_list(self):
        return self._caller_list

    @caller_list.setter
    def caller_list(self, value):
        self._caller_list = value if value else []


    def generate(self):
        """ Set up the args and caller list for this object """
        self.code = self.header.format(self.caller_list, self.name,
                                       self.arg_spec)

    def format(self):
        CallerFormatter.apply(self)


def string_args(args):
    """ Enclose your positional arguments in strings so it can be used as an 
    argument, rather than part of the arg spec.

    Args:
        args (list/string): A string/list of strings to be quoted
    """
    if isinstance(args, basestring):
        return '"{}"'.format(args)
    return ['"{}"'.format(arg) for arg in args]
