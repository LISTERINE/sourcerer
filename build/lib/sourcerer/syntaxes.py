from sourcerer.callables import FunctionObj, DecoratorObj
from sourcerer.simple_statements import ReturnObj, Docstring


base_syntax = {"functions": {'type': FunctionObj,
                             'key': 'name',
                             'value_map': {'args': 'arg_names',
                                           'kwargs': 'kwarg_pairs',
                                           'varargs': 'varargs',
                                           'keywords': 'keywords'},
                              'children':{'ret':'return'}},
  "return": {'type': ReturnObj,
             'key': None,
             'value_map': {'value':'val'}}
 }

yaml_syntax = base_syntax
