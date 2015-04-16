from sourcerer.base import Document
from sourcerer.simple_statements import ReturnObj, Docstring
from sourcerer.callables import FunctionObj, DecoratorObj
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
class DefaultGenerator(object):

    def build_from(self, file_name='sourcerer.spellbook', loader=None):
        """ Parse a spellbook file into a deserialized format
        
        Args:
            file_name (str): The name of the spec file to load as a string
            loader (function): The function to parse the file ex. yaml.load
        """
        loader = loader if loader is not None else lambda x: {}
        self.file_name = file_name
        with open(self.file_name, 'r') as my_file:
            self.ast = loader(my_file)
        self.assemble()


    def assemble(self):
        """ Abstract function for constructing the syntax tree """
        self.doc = Document()

    def output(self, output_file_name=''):
        """ Write out the syntax tree """
        syntax_string = ''.join(self.doc)
        if not output_file_name:
            stdout.write(syntax_string)
        else:
            with open(output_file_name, 'w') as output:
                output.write(syntax_string)

if __name__ == "__main__":
    gen = DefaultGenerator()
    gen.build_from(argv[1])
    gen.output()
