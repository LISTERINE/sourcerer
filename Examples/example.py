from yaml import load
from sourcerer import Document, FunctionDef, DecoratorDef, Return, Str, Name, Call, Assignment, Docstring, Attribute
from sys import argv


doc = Document()

api = load(open(argv[1], 'r').read())

blueprint = Name(api['basePath'])

bp = Assignment(blueprint,
                Call(name="Blueprint",
                     arg_names=[Str(blueprint), '__name__'],
                     kwarg_pairs={'template_folder': Str('templates')}))

doc.add_child(bp)

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
    func.add_children([Docstring('\n'.join(docstrings)), returns])
    route = [DecoratorDef(name=Attribute(caller_list=[blueprint], name=Name('route')),
                          arg_names=[Str(path)], 
                          kwarg_pairs={'methods': methods}),
             func]
    doc.create_lineage(route)

doc.output()
