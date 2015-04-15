from yaml import load
from sys import stdout
from sourcerer.base import Statement, Document
from sourcerer.callables import FunctionObj, DecoratorObj, string_args
from sourcerer.simple_statements import ReturnObj, Docstring

from sys import argv
from pdb import set_trace

doc = Document()

api = load(open(argv[1], 'r').read())
for path in api['paths']:
    route = [
        DecoratorObj(name="route", arg_names=[path]),
        FunctionObj(name=path),
        ReturnObj()
    ]

    doc.create_lineage(route)
    
doc.output()
