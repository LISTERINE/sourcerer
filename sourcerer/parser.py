from flaskswag import route, RouteFunctionObj, RouteDecoratorObj
from codegen.base import Document
from codegen.simple_statements import ReturnObj, Docstring
from sys import stdout, argv
"""
r = RouteFunctionObj(name="test_route")
ret = ReturnObj
ret = ReturnObj()
dec = RouteDecoratorObj(name="route", arg_names=["/products"])

doc = Document()
doc.add_children(route([dec], r, ret))
doc.export()
"""
class ServerGen(object):

    def digest(self, file_name):
        """ Read in a config file """
        self.file_name = file_name
        with open(self.file_name, 'r') as my_file:
            self.ast = self.parse(my_file)

    def parse(self, file_handle):
        """ Abstract function for parsing config files into an ast """
        raise NotImplementedError

    def assemble(self, config):
        """ Abstract function for constructing the syntax tree """
        raise NotImplementedError

    def output(self, doc, output_file_name=''):
        """ Write out the syntax tree """

        syntax_string = ''.join(doc.export())
        if not output_file_name:
            stdout.write(syntax_string)
        else:
            with open(output_file_name, 'w') as output:
                output.write(syntax_string)

if __name__ == "__main__":
    gen = ServerGen()
    gen.digest(argv[1])
