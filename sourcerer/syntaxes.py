from sourcerer.callables import FunctionObj, DecoratorObj
from sourcerer.simple_statements import ReturnObj, Docstring


base_map = {"functions": {'type': FunctionObj, 
                          'key': 'name',       
                          'value_map': {'args': 'arg_names',
                                        'kwargs': 'kwarg_pairs',
                                        'varargs': 'varargs',
                                        'keywords': 'keywords',
                                        'ret': 'return',
                                        'doc': 'docstring'}
                        },
            "return": {'type': ReturnObj,
                       'value_map': {'value':'val'}
                       }
}

yaml_map = base_map
