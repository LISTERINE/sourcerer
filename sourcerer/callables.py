#!env/bin/python

from base import Statement
from formatters import CallableFormatter, CallFormatter
import inspect
from string import punctuation, maketrans
from pdb import set_trace


class FunctionDef(Statement):
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
        super(FunctionDef, self).__init__(*args, **kwargs)
        if isinstance(name, Statement):
            name.generate()
        self.name = name
        self.arg_names = arg_names if arg_names else []
        self.kwarg_pairs = kwarg_pairs if kwarg_pairs else {}
        self.varargs = varargs if varargs else None
        self.keywords = keywords if keywords else None
        self.header = "def {}{}:"

    @property
    def arg_spec(self):
        return self.build_args_kwargs()

    def build_args_kwargs(self):
        """ Build the argspec for the function """
        args = self.arg_names + self.kwarg_pairs.keys()
        kwargs = self.kwarg_pairs.values()
        spec = inspect.ArgSpec(args=args,
                               varargs=self.varargs,
                               keywords=self.keywords,
                               defaults=kwargs)
        return inspect.formatargspec(*spec)

    def generate(self):
        """ Sets the def and : in a function header.

        Result will look like 'def fn(...):'
        """
        self.code = self.header.format(self.name, self.arg_spec)

    def format(self):
        pass
        #CallableFormatter.apply(self)


class DecoratorDef(FunctionDef):
    """ Sets the @ on the header.
    result will look like '@fn(...)'
    """

    def __init__(self, *args, **kwargs):
        super(DecoratorDef, self).__init__(*args, **kwargs)
        self.header = "@{}{}"

    def build_renderer(self, *args, **kwargs):
        kwargs['increment'] = 0
        return self.render(*args, **kwargs)


class ClassDef(FunctionDef):
    """ Define a class
    result will look like 'class cls(...):'
    """

    def __init__(self, *args, **kwargs):
        super(ClassDef, self).__init__(*args, **kwargs)
        self.header = "class {}{}:"


class Attribute(FunctionDef):
    """ Used to access Object attributes """

    def __init__(self, caller_list=None, *args, **kwargs):
        """
        Args:
            caller_list (list): The list of predecessor Objects ex. [C1,f1,f2] = C1.f1().f2().self
        """
        super(Attribute, self).__init__(*args, **kwargs)
        self._caller_list = caller_list if caller_list else []
        self.header = "{}{}"

    @property
    def caller_list(self):
        return self.build_caller_list()

    @caller_list.setter
    def caller_list(self, value):
        self._caller_list = value

    def build_caller_list(self):
        """ Set up the caller list for this object """
        for call in self._caller_list:

            call.generate()
        callers = '.'.join([str(call) for call in self._caller_list])
        return "{}{}".format(callers, '.' if callers else '')

    def generate(self):
        """ Format the args and caller list for this object """
        self.code = self.header.format(self.caller_list,
                                       self.name)


class Call(Attribute):
    """ Used to call functions or instantiate Classes """

    def __init__(self, *args, **kwargs):
        super(Call, self).__init__(*args, **kwargs)
        self.header = "{}{}{}"

    def generate(self):
        """ Format the args and caller list for this object """
        self.code = self.header.format(self.caller_list,
                                       self.name,
                                       self.arg_spec)

    def format(self):
        CallFormatter.apply(self)