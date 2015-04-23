from yaml import load
from sourcerer import Document, FunctionDef, DecoratorDef, Return, Str, Name, Call, Assignment, Docstring
from sys import argv


doc = Document()

api = load(open(argv[1], 'r').read())

rapi = Assignment("rapi",
           Call(name="Blueprint",
                arg_names=[Str(api['basePath'].lstrip('/')), '__name__'],
                kwarg_pairs={'template_folder': Str('templates')}))
doc.add_child(rapi)

for path in api['paths']:
    methods = []
    docstrings = []
    returns = []
    params = []
    path_data = api['paths'][path]
    for method in path_data:
        methods.append(Str(method.upper()))
        params.extend([Name(arg['name']) for arg in path_data[method].get('parameters', [])])
        docstrings.append(method.upper()+': '+path_data[method]['summary'])
        returns.extend([Return(val=ret) for ret in path_data[method].get('responses', [])])
    func = FunctionDef(name=Name(path), arg_names=params)
    func.add_children([Docstring('\n'.join(docstrings))].extend(returns))
    route = [DecoratorDef(name="rapi.route", arg_names=[Str(path)], kwarg_pairs={"methods": methods}),
             func]

    doc.create_lineage(route)

doc.output()
