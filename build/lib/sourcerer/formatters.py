from string import maketrans, punctuation
from traceback import format_exc


class Formatter(object):
    """ Formatting operations for syntax objects

    Name functions after the property they will be operating on.
    All function should take one argument of 'property'.
    """

    @classmethod
    def apply(cls, syntax_obj):
        """ Apply all formatters to the given object 
        
        This method will search the given syntax object for any property which
        has the same name as a formatter.

        Args:
            syntax_obj (object): The object with the attributes to be formatted
        """
        for prop_name, value in syntax_obj.__dict__.items():
            try:
                formatter = getattr(cls, prop_name)

                setattr(syntax_obj, prop_name, formatter(value))
            except AttributeError:
                pass
            except Exception as e:
                print format_exc()
                print e
                print syntax_obj, '->', prop_name


class CallableFormatter(Formatter):
    @classmethod
    def name(cls, property):
        """ Replace all punctuation in a callables name with underscores """
        filter = maketrans(punctuation, ''.join(['_' for x in punctuation]))
        return property.translate(filter)

    @classmethod
    def arg_names(cls, property):
        """ Abstract function for formatting positional arguments """
        return property

    @classmethod
    def kwarg_pairs(cls, property):
        """ Abstract function for formatting keyword arguments """
        return property
