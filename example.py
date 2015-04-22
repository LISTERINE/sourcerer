from yaml import load
from sourcerer import Document, FunctionDef, DecoratorDef, Return, Str, Name, Call, Assignment
from sys import argv

# Create a document to put our code in
doc = Document()

# Open our yml file and read it in
api = load(open(argv[1], 'r').read())

rapi = Assignment("rapi",
           Call(name="Blueprint",
                arg_names=[Str(api['basePath'].lstrip('/')), '__name__'],
                kwarg_pairs={'template_folder': Str('templates')}))
doc.add_child(rapi)

for path in api['paths']:
    route = [DecoratorDef(name="rapi.route", arg_names=[Str(path)]), # A decorator: @routename("mypath")
             FunctionDef(name=Name(path)), # A function: def routename():
             Return()] # A return statement: return

    doc.create_lineage(route) # Cascade these objects into the main document scope
                              # ...
                              # @routename("mypath")
                              # def routename():
                              #     return
                              # ...

doc.output() # Send output to standard out (output to file optional)
