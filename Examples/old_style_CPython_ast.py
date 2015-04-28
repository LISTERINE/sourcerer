from yaml import load
from sys import argv
from pdb import set_trace
from ast import *
import re
from astunparse import unparse


def format_name(name):
    no_vars = re.sub(r'_?\{.*?\}', '', name)
    no_doubles = no_vars.replace('//', '/')
    no_inner = re.sub('(\w)\/(\w)', r'\1_\2', no_doubles)  # replace inner slashes
    return no_inner.replace("/", "")

api = None
with open(argv[1], 'r') as api_file:
    api = load(api_file.read())
    
body = []
functions = []


blueprint_raw = api['basePath']
blueprint_name = format_name(blueprint_raw)
blueprint_route = blueprint_name+".route"
blueprint = Assign(targets=[Name(id=blueprint_name, ctx=Store())], 
                   value=Call(func=Name(id='BluePrint', ctx=Load()),
                              args=[Str(s=blueprint_name), 
                                    Name(id='__name__', 
                                         ctx=Load())], 
                              keywords=[keyword(arg='template_folder', 
                                                value=Str(s=blueprint_name))], 
                              starargs=None, kwargs=None))

body.append(blueprint)


for path, path_info in api['paths'].items():

    route_dec = Call(func=Name(id=blueprint_route, ctx=Load()),
                     args=[Str(s=path)],
                     keywords=[],
                     starargs=None,
                     kwargs=None)

    method_args = arguments(args=[Name(id='methods', 
                                       ctx=Param())],
                            vararg=None,
                            kwarg=None,
                            defaults=[List(elts=[Str(s=meth) for meth in path_info.keys()],
                                           ctx=Load())])

    returns = []

    for method, method_info in path_info.items():
        for response, response_info in method_info['responses'].items():
            returns.append(Return(value=Num(n=response)))

    route_func = FunctionDef(name=format_name(path),
                             args=method_args,
                             body=returns,
                             decorator_list=[route_dec])

    functions.append(route_func)

body.append(functions)

m = Module(body=body)
print unparse(m)
