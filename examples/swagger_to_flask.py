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
        # Record the HTTP method
        methods.append(Str(method.upper()))
        # Collect any arguments to the routes functions
        params.extend([Name(arg['name']) for arg in path_data[method].get('parameters', [])])
        # Pull the summary and description into the doc string
        docstrings.append('\n\n'.join([path_data[method]['summary'], path_data[method]['description']]))
        # Set up any information that needs to be returned
        for ret in path_data[method].get('responses', {}):
            resp = path_data[method]['responses'][ret]
            returns.extend([Return(val=resp.get("schema", {}).get("$ref", ''))])
    # Build the function for the route
    func = FunctionDef(name=Name(path), arg_names=params)
    # Push the docstring and return into the function
    func.add_children([Docstring('\n'.join(docstrings)), returns])
    # Build the route from a decorator and loaded up function
    route = [DecoratorDef(name=Attribute(caller_list=[blueprint], name=Name('route')),
                          arg_names=[Str(path)], 
                          kwarg_pairs={'methods': str(methods)}),
             func]
    # Cascade the route into the doc
    doc.create_lineage(route)

doc.output()

# For extra fun, this could be broken out into multiple docs/blueprints by the first path component of the routes