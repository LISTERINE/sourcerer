from sourcerer.callables import FunctionObj, DecoratorObj
from sourcerer.simple_statements import ReturnObj, Docstring

__doc__ = """
Syntax maps (SM) define the schema of an input file (IF).

Example input file (YAML)
------
functions:
    func1:
        args: ['thing1', 'thing2']
        kwargs: {"key1": "val1"}
        varargs: false
        keywords: false
        ret:
            value:
                true
------
The SM to parse this may look like this:
------
{"functions": {'type': FunctionObj,
               'key': 'name',
               'value_map': {'args': 'arg_names',
                             'kwargs': 'kwarg_pairs',
                             'varargs': 'varargs',
                             'keywords': 'keywords'},
               'children':{'ret':'return'}},
 "return": {'type': ReturnObj,
            'value_map': {'value':'val'}}
}

Setting up an SM:
    Your SMs top-level keys define what your IF top-level sections are containing.
    The values of your SM top-level keys are dictionaries defining how to handle the 
    contents of your IF sections.

    In the given example, the only top-level IF section is 'functions'. In the
    SM, the 'functions' key's value says several things:
        1. For each child node encountered, create a new FunctionObj (defined by 'type')
        2. The key defining each child node is the 'name' argument for the FunctionObj
        3. The sub-keys of the child node are properties of the FunctionObj
            The values of those sub-keys are can be one of two things:
                1. If the value is in the value map, it is an argument to FunctionObj
                2. If the value is in the children map, it should be placed into the 
                    scope of the FunctionObj. The value will be looked up in the 
                    SM top-level to see if it can be be instantiated into a new 
                    sourcerer object.

The schema should consist of:
    type: The class name to instantiate
    key: what the key for the node represents
    value_map: map properties to arguments to the class
    children: values that should be instantiated and placed into the current
                nodes child scope
"""

base_map = {"functions": {'type': FunctionObj, # Each top level entry under functions is a FunctionObj
                          'key': 'name',       # The key for its parameter dict is its name argument
                          'value_map': {'args': 'arg_names', # Define what args are called in the markups schema
                                        'kwargs': 'kwarg_pairs',
                                        'varargs': 'varargs',
                                        'keywords': 'keywords',
                                        'ret': 'return', # When top-level objects are seen their values will be pared as well, building a new object from the mapping they specify and then appended to this object
                                        'doc': 'docstring'}
                        },
            "return": {'type': ReturnObj,
                       'value_map': {'value':'val'}
                       }
}

yaml_map = base_map
