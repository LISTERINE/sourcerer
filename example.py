from yaml import load
from sourcerer import Document, FunctionDef, DecoratorDef, Return
from sys import argv

# Create a document to put our code in
doc = Document()

# Open our yml file and read it in
api = load(open(argv[1], 'r').read())
for path in api['paths']:
    route = [DecoratorDef(name="route", arg_names=[path]), # A decorator: @routename("mypath")
             FunctionDef(name=path), # A function: def routename():
             Return()] # A return statement: return

    doc.create_lineage(route) # Cascade these objects into the main document scope
                              # ...
                              # @routename("mypath")
                              # def routename():
                              #     return
                              # ...

doc.output() # Send output to standard out (output to file optional)
