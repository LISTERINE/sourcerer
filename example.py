from yaml import load
from sourcerer.base import Document
from sourcerer.callables import FunctionObj, DecoratorObj
from sourcerer.simple_statements import ReturnObj
from sys import argv

# Create a docuemnt to put our code in
doc = Document()

# Open our yml file and read it in
api = load(open(argv[1], 'r').read())
for path in api['paths']:
    route = [DecoratorObj(name="route", arg_names=[path]), # A decorator: @routename("mypath")
             FunctionObj(name=path), # A function: def routename():
             ReturnObj()] # A return statement: return

    doc.create_lineage(route) # Cascade these objects into the main document scope
                              # ...
                              # @routename("mypath")
                              # def routename():
                              #     return
                              # ...

doc.output() # Send output to standard out (output to file optional)
