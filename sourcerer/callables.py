#!env/bin/python

from .base import Statement
import inspect


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
            kwarg_pairs (dict): A dict of str:str to become the keyword argument names/defaults
            varargs (str): Name of the *args argument.
            keywords (str): Name of the **kwargs argument.
        """
        super(FunctionDef, self).__init__(*args, **kwargs)
        if isinstance(name, Statement):
            name.generate()
        self.name = name
        self.__arg_names = arg_names if arg_names else []
        self.__kwarg_pairs = kwarg_pairs if kwarg_pairs else {}
        self.varargs = varargs if varargs else None
        self.keywords = keywords if keywords else None
        self.header = "def {}{}:"

    @property
    def arg_names(self):
        return [Statement.to_statement(arg) for arg in self.__arg_names]

    @property
    def kwarg_pairs(self):
        return {Statement.to_statement(k):Statement.to_statement(v) for k,v in list(self.__kwarg_pairs.items())}

    @property
    def arg_spec(self):
        return self.build_args_kwargs()

    def build_args_kwargs(self):
        """ Build the argspec for the function """
        args = self.arg_names + list(self.kwarg_pairs.keys())
        kwargs = list(self.kwarg_pairs.values())
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
        self.caller_list = caller_list if caller_list else []
        self.header = "{}{}"

    @property
    def caller_list(self):
        for call in self._caller_list:
            call.generate()
        callers = '.'.join(str(call) for call in self._caller_list)
        return "{}{}".format(callers, '.' if callers else '')

    @caller_list.setter
    def caller_list(self, value):
        self._caller_list = [Statement.to_statement(obj) for obj in value]

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